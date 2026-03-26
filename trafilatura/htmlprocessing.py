# pylint:disable-msg=C0301,E0611,I1101
"""
Functions to process nodes in HTML code.
"""

import base64
import logging
import re
from urllib.parse import urlparse

from copy import deepcopy
from typing import List, Optional, Tuple

from courlan.urlutils import fix_relative_urls, get_base_url
from lxml import html as lxml_html
from lxml.etree import (
    _Element,
    Element,
    SubElement,
    XPath,
    strip_tags,
    tostring,
    fromstring,
)
from lxml.html import HtmlElement
import json

from .deduplication import duplicate_test
from .settings import (
    Document,
    Extractor,
    CUT_EMPTY_ELEMS,
    MANUALLY_CLEANED,
    MANUALLY_STRIPPED,
)
from .utils import textfilter, trim, is_image_element
from .xml import META_ATTRIBUTES, delete_element


LOGGER = logging.getLogger(__name__)

REND_TAG_MAPPING = {
    "em": "#i",
    "i": "#i",
    "b": "#b",
    "strong": "#b",
    "u": "#u",
    "kbd": "#t",
    "samp": "#t",
    "tt": "#t",
    "var": "#t",
    "sub": "#sub",
    "sup": "#sup",
}

HTML_TAG_MAPPING = {v: k for k, v in REND_TAG_MAPPING.items()}

PRESERVE_IMG_CLEANING = {"figure", "picture", "source", "audio", "video", "track", "svg"}

CODE_INDICATORS = ["{", "(\"", "('", "\n    "]

SVG_NS_HREF = "{http://www.w3.org/1999/xlink}href"


def _sanitize_svg_length(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    match = re.match(r"\s*([0-9]*\.?[0-9]+)", value)
    if not match:
        return None
    number = match.group(1)
    if "." in number:
        number = number.rstrip("0").rstrip(".")
    return number


def _extract_svg_dimensions(svg_elem: Element) -> Tuple[Optional[str], Optional[str]]:
    width = _sanitize_svg_length(svg_elem.get("width"))
    height = _sanitize_svg_length(svg_elem.get("height"))
    if width and height:
        return width, height
    viewbox = svg_elem.get("viewBox") or svg_elem.get("viewbox")
    if viewbox:
        parts = viewbox.replace(",", " ").split()
        if len(parts) == 4:
            w_candidate = _sanitize_svg_length(parts[2])
            h_candidate = _sanitize_svg_length(parts[3])
            width = width or w_candidate
            height = height or h_candidate
    return width, height


def _absolutize_svg_links(svg_elem: Element, base_url: Optional[str]) -> None:
    if not base_url:
        return
    for node in svg_elem.iter():
        for attr, value in list(node.attrib.items()):
            if not value:
                continue
            attr_lower = attr.lower()
            if (
                attr_lower.endswith("href")
                or attr_lower in ("src", "xlink:href")
                or attr == SVG_NS_HREF
            ):
                if value.startswith(("http://", "https://", "data:", "#", "url(")):
                    continue
                node.set(attr, fix_relative_urls(base_url, value))


def _clean_svg_element(svg_elem: Element, base_url: Optional[str]) -> Element:
    svg_copy = deepcopy(svg_elem)
    for junk in svg_copy.xpath(
        ".//script|.//iframe|.//foreignObject|.//object"
    ):
        delete_element(junk, keep_tail=False)
    _absolutize_svg_links(svg_copy, base_url)
    return svg_copy


def _serialize_svg(svg_elem: Element, base_url: Optional[str]) -> Optional[str]:
    cleaned = _clean_svg_element(svg_elem, base_url)
    markup = tostring(cleaned, encoding="unicode")
    if not markup:
        return None
    encoded = base64.b64encode(markup.encode("utf-8")).decode("ascii")
    return encoded


def _build_svg_graphic(
    svg_elem: Element, base_url: Optional[str], caption: str = ""
) -> Optional[Element]:
    inline = _serialize_svg(svg_elem, base_url)
    if not inline:
        return None
    graphic = Element("graphic")
    graphic.set("data-type", "svg")
    graphic.set("data-inline-svg", inline)
    width, height = _extract_svg_dimensions(svg_elem)
    if width:
        graphic.set("width", width)
    if height:
        graphic.set("height", height)
    label = svg_elem.get("aria-label") or svg_elem.get("title")
    if label:
        graphic.set("alt", label)
    if caption:
        graphic.set("caption", caption)
    return graphic


def _build_mathml_graphic(node: Element, display: str) -> Optional[Element]:
    markup = tostring(node, encoding="unicode", with_tail=False)
    if not markup:
        return None
    encoded = base64.b64encode(markup.encode("utf-8")).decode("ascii")
    graphic = Element("graphic")
    graphic.set("data-type", "mathml")
    graphic.set("data-inline-html", encoded)
    graphic.set("data-display", display)
    return graphic

# Remove CSS-like garbage sequences at the beginning of captions


def tree_cleaning(tree: HtmlElement, options: Extractor) -> HtmlElement:
    "Prune the tree by discarding unwanted elements."
    # determine cleaning strategy, use lists to keep it deterministic
    cleaning_list, stripping_list = MANUALLY_CLEANED.copy(), MANUALLY_STRIPPED.copy()
    if not options.tables:
        cleaning_list.extend(["table", "td", "th", "tr"])
    else:
        # prevent this issue: https://github.com/adbar/trafilatura/issues/301
        for elem in tree.xpath(".//figure[descendant::table]"):
            elem.tag = "div"
    if options.images:
        # Many websites have <img> inside <figure>/<picture>/<source>, and media inside <audio>/<video>
        cleaning_list = [e for e in cleaning_list if e not in PRESERVE_IMG_CLEANING]
        if "img" in stripping_list:
            stripping_list.remove("img")

    # strip targeted elements
    strip_tags(tree, stripping_list)

    # prevent removal of paragraphs
    if options.focus == "recall" and tree.find(".//p") is not None:
        tcopy = deepcopy(tree)
        for expression in cleaning_list:
            for element in tree.iter(expression):
                delete_element(element)
        if tree.find(".//p") is None:
            tree = tcopy
    # delete targeted elements
    else:
        for expression in cleaning_list:
            for element in tree.iter(expression):
                delete_element(element)

    return prune_html(tree, options.focus)


def prune_html(tree: HtmlElement, focus: str = "balanced") -> HtmlElement:
    "Delete selected empty elements to save space and processing time."
    tails = focus != "precision"
    # .//comment() needed for date extraction
    for element in tree.xpath(".//processing-instruction()|.//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            delete_element(element, keep_tail=tails)
    return tree


def prune_unwanted_nodes(
    tree: HtmlElement, nodelist: List[XPath], with_backup: bool = False
) -> HtmlElement:
    "Prune the HTML tree by removing unwanted sections."
    if with_backup:
        old_len = len(tree.text_content())  # ' '.join(tree.itertext())
        backup = deepcopy(tree)

    for expression in nodelist:
        for subtree in expression(tree):
            # preserve tail text from deletion
            # tail is by default preserved by delete_element()
            # remove the node
            delete_element(subtree)

    if with_backup:
        new_len = len(tree.text_content())
        # todo: adjust for recall and precision settings
        return tree if new_len > old_len / 7 else backup
    return tree


def collect_link_info(
    links_xpath: List[HtmlElement],
) -> Tuple[int, int, int, List[str]]:
    "Collect heuristics on link text"
    mylist = [e for e in (trim(elem.text_content()) for elem in links_xpath) if e]
    lengths = list(map(len, mylist))
    # longer strings impact recall in favor of precision
    shortelems = sum(1 for l in lengths if l < 10)
    return sum(lengths), len(mylist), shortelems, mylist


def link_density_test(
    element: HtmlElement, text: str, favor_precision: bool = False
) -> Tuple[bool, List[str]]:
    "Remove sections which are rich in links (probably boilerplate)"
    links_xpath = element.findall(".//ref")
    if not links_xpath:
        return False, []
    mylist: List[str] = []
    # shortcut
    if len(links_xpath) == 1:
        len_threshold = 10 if favor_precision else 100
        link_text = trim(links_xpath[0].text_content())
        if len(link_text) > len_threshold and len(link_text) > len(text) * 0.9:
            return True, []
    if element.tag == "p":
        limitlen = 60 if element.getnext() is None else 30
    else:
        if element.getnext() is None:
            limitlen = 300
        # elif re.search(r'[.?!:]', element.text_content()):
        #    limitlen, threshold = 150, 0.66
        else:
            limitlen = 100
    elemlen = len(text)
    if elemlen < limitlen:
        linklen, elemnum, shortelems, mylist = collect_link_info(links_xpath)
        if elemnum == 0:
            return True, mylist
        LOGGER.debug(
            "list link text/total: %s/%s – short elems/total: %s/%s",
            linklen,
            elemlen,
            shortelems,
            elemnum,
        )
        if linklen > elemlen * 0.8 or (elemnum > 1 and shortelems / elemnum > 0.8):
            return True, mylist
    return False, mylist


def link_density_test_tables(element: HtmlElement) -> bool:
    "Remove tables which are rich in links (probably boilerplate)."
    links_xpath = element.findall(".//ref")

    if not links_xpath:
        return False

    elemlen = len(trim(element.text_content()))
    if elemlen < 200:
        return False

    linklen, elemnum, _, _ = collect_link_info(links_xpath)
    if elemnum == 0:
        return True

    LOGGER.debug("table link text: %s / total: %s", linklen, elemlen)
    return linklen > 0.8 * elemlen if elemlen < 1000 else linklen > 0.5 * elemlen


def delete_by_link_density(
    subtree: HtmlElement,
    tagname: str,
    backtracking: bool = False,
    favor_precision: bool = False,
    base_url: Optional[str] = None,
) -> HtmlElement:
    """Determine the link density of elements with respect to their length,
    and remove the elements identified as boilerplate."""
    deletions = []
    len_threshold = 200 if favor_precision else 100
    depth_threshold = 1 if favor_precision else 3
    base_host = _safe_host(base_url)

    for elem in subtree.iter(tagname):
        if base_host and _has_same_origin_media(elem, base_host):
            # Keep media-only blocks when the media is hosted on the same origin/subdomain.
            continue
        elemtext = trim(elem.text_content())
        result, templist = link_density_test(elem, elemtext, favor_precision)
        if result or (
            backtracking
            and templist
            and 0 < len(elemtext) < len_threshold
            and len(elem) >= depth_threshold
        ):
            deletions.append(elem)
            # else: # and not re.search(r'[?!.]', text):
            # print(elem.tag, templist)

    for elem in dict.fromkeys(deletions):
        delete_element(elem)

    return subtree


def _safe_host(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    try:
        parsed = urlparse(url)
        return parsed.hostname.lower() if parsed.hostname else None
    except Exception:
        return None


def _host_matches(base_host: str, other: str) -> bool:
    other = other.lower()
    return other == base_host or other.endswith("." + base_host)


def _has_same_origin_media(elem: HtmlElement, base_host: str) -> bool:
    """Return True if the element contains a graphic pointing to the same origin/subdomain."""
    for graphic in elem.xpath(".//graphic[@src]"):
        src = graphic.get("src")
        if not src:
            continue
        try:
            host = urlparse(src).hostname
        except Exception:
            host = None
        if host and _host_matches(base_host, host):
            return True
    return False


def _has_math_markup(elem: _Element) -> bool:
    """Return True if the node (or any descendant) carries MathML/KaTeX markup."""
    for node in elem.iter():
        if node.tag == "math":
            return True
        class_attr = node.get("class")
        if class_attr:
            if isinstance(class_attr, (list, tuple)):
                classes = " ".join(map(str, class_attr))
            else:
                classes = str(class_attr)
            if "katex" in classes:
                return True
    return False


def handle_textnode(
    elem: _Element,
    options: Extractor,
    comments_fix: bool = True,
    preserve_spaces: bool = False,
) -> Optional[_Element]:
    "Convert, format, and probe potential text elements."
    if elem.tag == "graphic":
        # pass through if it's a valid image, KaTeX placeholder, or declared AV media
        if is_image_element(elem) or elem.get("data-type") in ("video", "audio", "mathml"):
            return elem
    if elem.tag == "done" or (len(elem) == 0 and not elem.text and not elem.tail):
        return None

    # lb bypass
    if not comments_fix and elem.tag == "lb":
        if not preserve_spaces:
            elem.tail = trim(elem.tail) or None
        # if textfilter(elem) is True:
        #     return None
        # duplicate_test(subelement)?
        return elem

    if not elem.text and len(elem) == 0:
        # try the tail
        # LOGGER.debug('using tail for element %s', elem.tag)
        elem.text, elem.tail = elem.tail, ""
        # handle differently for br/lb
        if comments_fix and elem.tag == "lb":
            elem.tag = "p"

    # trim
    if not preserve_spaces:
        elem.text = trim(elem.text) or None
        if elem.tail:
            elem.tail = trim(elem.tail) or None

    # filter content
    # or not re.search(r'\w', element.text):  # text_content()?
    has_math = _has_math_markup(elem)
    has_graphic = elem.tag == "graphic" or elem.find(".//graphic") is not None
    if not has_math and not has_graphic and not elem.text and textfilter(elem):
        return None
    if options.dedup and duplicate_test(elem, options):
        return None
    return elem


def process_node(elem: _Element, options: Extractor) -> Optional[_Element]:
    "Convert, format, and probe potential text elements (light format)."
    if elem.tag == "done" or (len(elem) == 0 and not elem.text and not elem.tail):
        return None

    # trim
    elem.text, elem.tail = trim(elem.text) or None, trim(elem.tail) or None

    # adapt content string
    if elem.tag != "lb" and not elem.text and elem.tail:
        elem.text, elem.tail = elem.tail, None

    # content checks
    if elem.text or elem.tail:
        if textfilter(elem) or (options.dedup and duplicate_test(elem, options)):
            return None

    return elem


def convert_lists(elem: _Element) -> None:
    "Convert <ul> and <ol> to <list> and underlying <li> elements to <item>."
    elem.set("rend", elem.tag)
    elem.tag = "list"
    i = 1
    for subelem in elem.iter("dd", "dt", "li"):
        # keep track of dd/dt items
        if subelem.tag in ("dd", "dt"):
            subelem.set("rend", f"{str(subelem.tag)}-{i}")
            # increment counter after <dd> in description list
            if subelem.tag == "dd":
                i += 1
        # convert elem tag (needs to happen after the rest)
        subelem.tag = "item"


def convert_quotes(elem: _Element) -> None:
    "Convert quoted elements while accounting for nested structures."
    code_flag = False
    if elem.tag == "pre":
        # detect if there could be code inside
        # pre with a single span is more likely to be code
        if len(elem) == 1 and elem[0].tag == "span":
            code_flag = True
        # find hljs elements to detect if it's code
        code_elems = elem.xpath(".//span[starts-with(@class,'hljs')]")
        if code_elems:
            code_flag = True
            for subelem in code_elems:
                subelem.attrib.clear()
        if _is_code_block(elem.text):
            code_flag = True
    elem.tag = "code" if code_flag else "quote"

def _is_code_block(text: Optional[str]) -> bool:
    "Check if the element text is part of a code block."
    if not text:
        return False
    for indicator in CODE_INDICATORS:
        if indicator in text:
            return True
    return False

def convert_headings(elem: _Element) -> None:
    "Add head tags and delete attributes."
    elem.attrib.clear()
    elem.set("rend", elem.tag)
    elem.tag = "head"


def convert_line_breaks(elem: _Element) -> None:
    "Convert <br> and <hr> to <lb>"
    elem.tag = "lb"


def convert_deletions(elem: _Element) -> None:
    'Convert <del>, <s>, <strike> to <del rend="overstrike">'
    elem.tag = "del"
    elem.set("rend", "overstrike")


def convert_details(elem: _Element) -> None:
    "Handle details and summary."
    elem.tag = "div"
    for subelem in elem.iter("summary"):
        subelem.tag = "head"


CONVERSIONS = {
    "dl": convert_lists,
    "ol": convert_lists,
    "ul": convert_lists,
    "h1": convert_headings,
    "h2": convert_headings,
    "h3": convert_headings,
    "h4": convert_headings,
    "h5": convert_headings,
    "h6": convert_headings,
    "br": convert_line_breaks,
    "hr": convert_line_breaks,
    "blockquote": convert_quotes,
    "pre": convert_quotes,
    "q": convert_quotes,
    "del": convert_deletions,
    "s": convert_deletions,
    "strike": convert_deletions,
    "details": convert_details,
    # wbr
}


def convert_link(elem: HtmlElement, base_url: Optional[str]) -> None:
    "Replace link tags and href attributes, delete the rest."
    elem.tag = "ref"
    target = elem.get("href")  # defaults to None
    link_id = elem.get("id")
    elem.attrib.clear()
    if target:
        # convert relative URLs
        if base_url:
            target = fix_relative_urls(base_url, target)
        elem.set("target", target)
    if link_id:
        # Preserve anchor IDs (e.g., footnote targets) for round-trip output.
        elem.set("id", link_id)


def convert_tags(
    tree: HtmlElement, options: Extractor, url: Optional[str] = None
) -> HtmlElement:
    "Simplify markup and convert relevant HTML tags to an XML standard."
    # base URL detection (used for links and media src)
    base_url = url and get_base_url(url)
    # delete links for faster processing
    if not options.links:
        xpath_expr = ".//*[self::div or self::li or self::p]//a"
        if options.tables:
            xpath_expr += "|.//table//a"
        # necessary for further detection
        for elem in tree.xpath(xpath_expr):
            elem.tag = "ref"
        # strip the rest
        strip_tags(tree, "a")
    else:
        # get base URL for converting relative URLs
        for elem in tree.iter("a", "ref"):
            convert_link(elem, base_url)

    if options.formatting:
        for elem in tree.iter(REND_TAG_MAPPING.keys()):
            elem.attrib.clear()
            elem.set("rend", REND_TAG_MAPPING[elem.tag])  # type: ignore[index]
            elem.tag = "hi"
    else:
        strip_tags(tree, *REND_TAG_MAPPING.keys())

    # iterate over all concerned elements
    for elem in tree.iter(CONVERSIONS.keys()):
        CONVERSIONS[elem.tag](elem)  # type: ignore[index]
    # images and media
    if options.images:
        # 1) Normalize <figure> with <img>/<video>/<audio> + optional <figcaption>
        for fig in list(tree.iter("figure")):
            # extract caption text if present
            cap_nodes = fig.xpath('.//figcaption')
            caption_el = cap_nodes[0] if cap_nodes else None
            if caption_el is not None:
                # drop garbage elements inside caption (e.g., style/script)
                for junk in caption_el.xpath('.//style|.//script|.//noscript|.//link|.//meta|.//iframe|.//object|.//svg'):
                    delete_element(junk, keep_tail=True)
            caption = " ".join(caption_el.itertext()).strip() if caption_el is not None else ""
            if caption_el is not None and caption_el.getparent() is not None:
                caption_el.getparent().remove(caption_el)

            # prefer <img>, then <picture><img>, then <video>, then <audio>, then inline <svg>
            media_nodes = fig.xpath('.//img | .//picture/img | .//video | .//audio | .//svg')
            media = media_nodes[0] if media_nodes else None
            if media is None:
                continue

            g = Element("graphic")
            # image
            if media.tag == "img":
                g.set("data-type", "image")
                src = media.get("src")
                if src and base_url:
                    src = fix_relative_urls(base_url, src)
                if src:
                    g.set("src", src)
                if media.get("alt"):
                    g.set("alt", media.get("alt", ""))
                if media.get("title"):
                    g.set("title", media.get("title", ""))
            elif media.tag == "svg":
                svg_graphic = _build_svg_graphic(media, base_url, caption)
                if svg_graphic is None:
                    continue
                for attr, value in svg_graphic.attrib.items():
                    g.set(attr, value)
            else:
                # video or audio
                g.set("data-type", "video" if media.tag == "video" else "audio")
                if media.get("src"):
                    src = media.get("src")
                    if src and base_url:
                        src = fix_relative_urls(base_url, src)
                    if src:
                        g.set("src", src)
                # collect <source> children
                sources = []
                for s in media.xpath(".//source"):
                    ssrc = s.get("src")
                    if ssrc:
                        if base_url:
                            ssrc = fix_relative_urls(base_url, ssrc)
                        sources.append({
                            "src": ssrc,
                            "type": s.get("type", ""),
                            "media": s.get("media", ""),
                        })
                if sources:
                    g.set("data-sources", json.dumps(sources, ensure_ascii=False))
                # copy common media attributes if present
                for attr in (
                    "poster",
                    "controls",
                    "autoplay",
                    "muted",
                    "loop",
                    "preload",
                    "playsinline",
                    "crossorigin",
                ):
                    if media.get(attr) is not None:
                        g.set(attr, media.get(attr) or "")

            if caption and media.tag != "svg":
                g.set("caption", caption)
            # replace figure element in place with <graphic>
            fig.tag = "graphic"
            fig.attrib.clear()
            # remove all children
            for child in list(fig):
                fig.remove(child)
            for k, v in g.attrib.items():
                fig.set(k, v)

        # 2) Standalone <video>/<audio>
        for media in list(tree.xpath(".//video|.//audio")):
            # replace media in place with <graphic>
            media_attrs = {"data-type": ("video" if media.tag == "video" else "audio")}
            if media.get("src"):
                src = media.get("src")
                if src and base_url:
                    src = fix_relative_urls(base_url, src)
                if src:
                    media_attrs["src"] = src
            sources = []
            for s in media.findall(".//source"):
                ssrc = s.get("src")
                if ssrc:
                    if base_url:
                        ssrc = fix_relative_urls(base_url, ssrc)
                    sources.append({
                        "src": ssrc,
                        "type": s.get("type", ""),
                        "media": s.get("media", ""),
                    })
            if sources:
                media_attrs["data-sources"] = json.dumps(sources, ensure_ascii=False)
            for attr in (
                "poster",
                "controls",
                "autoplay",
                "muted",
                "loop",
                "preload",
                "playsinline",
                "crossorigin",
            ):
                if media.get(attr) is not None:
                    media_attrs[attr] = media.get(attr) or ""
            media.tag = "graphic"
            media.attrib.clear()
            # remove potential children
            for child in list(media):
                media.remove(child)
            for k, v in media_attrs.items():
                media.set(k, v)

        # 3) Remaining <img>
        for elem in tree.iter("img"):
            elem.tag = "graphic"

        # 4) Inline SVG without figures
        for svg in list(tree.xpath(".//svg")):
            parent = svg.getparent()
            if parent is None:
                continue
            if parent.tag == "graphic":
                continue
            graphic_svg = _build_svg_graphic(svg, base_url)
            if graphic_svg is None:
                continue
            idx = parent.index(svg)
            graphic_svg.tail = svg.tail
            parent.remove(svg)
            parent.insert(idx, graphic_svg)

    _replace_mathml_with_graphics(tree)
    return tree


def _replace_mathml_with_graphics(tree: HtmlElement) -> None:
    """Capture MathML markup as <graphic data-type="mathml"> placeholders."""
    xpath = ".//*[local-name()='math']"
    for node in list(tree.xpath(xpath)):
        display_attr = (node.get("display", "") or "").lower()
        if not display_attr:
            style_attr = (node.get("style", "") or "").replace(" ", "").lower()
            if "display:block" in style_attr:
                display_attr = "block"
        inferred_display = "block" if display_attr == "block" else "inline"
        _replace_node_with_graphic(node, inferred_display)


def _replace_node_with_graphic(node: Element, display: str) -> None:
    graphic = _build_mathml_graphic(node, display)
    if graphic is None:
        return
    parent = node.getparent()
    if parent is None:
        return
    idx = parent.index(node)
    graphic.tail = node.tail
    node.tail = None
    parent.remove(node)
    parent.insert(idx, graphic)


HTML_CONVERSIONS = {
    "list": "ul",
    "item": "li",
    "code": "pre",
    "quote": "blockquote",
    "head": lambda elem: f"h{int(elem.get('rend', 'h3')[1:])}",
    "lb": "br",
    # convert internal link back to HTML
    "ref": "a",
    "hi": lambda elem: HTML_TAG_MAPPING[elem.get("rend", "#i")],
}


def convert_to_html(tree: _Element) -> _Element:
    "Convert XML to simplified HTML. Also rebuild media/figures for HTML."
    # First, rebuild <graphic> elements into HTML media/img nodes
    for g in list(tree.iter("graphic")):
        dtype = g.get("data-type") or "image"
        caption = g.get("caption") or ""

        # helper to optionally wrap in figure
        def wrap_in_figure(node: _Element) -> _Element:
            if caption:
                fig = Element("figure")
                fig.append(node)
                SubElement(fig, "figcaption").text = caption
                return fig
            return node

        replacement: Optional[_Element] = None
        if dtype == "image":
            img = Element("img")
            if g.get("src"):
                img.set("src", g.get("src", ""))
            if g.get("alt"):
                img.set("alt", g.get("alt", ""))
            if g.get("title"):
                img.set("title", g.get("title", ""))
            replacement = wrap_in_figure(img)
        elif dtype == "svg":
            inline_data = g.get("data-inline-svg")
            if not inline_data:
                continue
            try:
                svg_elem = fromstring(base64.b64decode(inline_data))
            except Exception:
                continue
            if g.get("width") and not svg_elem.get("width"):
                svg_elem.set("width", g.get("width", ""))
            if g.get("height") and not svg_elem.get("height"):
                svg_elem.set("height", g.get("height", ""))
            if g.get("alt") and not svg_elem.get("aria-label"):
                svg_elem.set("aria-label", g.get("alt", ""))
            replacement = wrap_in_figure(svg_elem)
        elif dtype in ("katex", "mathml"):
            raw_html = g.get("data-inline-html")
            if not raw_html:
                continue
            try:
                decoded = base64.b64decode(raw_html).decode("utf-8")
                fragment = lxml_html.fragment_fromstring(decoded, create_parent=True)
            except Exception:
                continue
            nodes = list(fragment)
            if not nodes:
                continue
            if len(nodes) == 1:
                replacement = nodes[0]
            else:
                wrapper = Element("span")
                for child in nodes:
                    wrapper.append(child)
                replacement = wrapper
        else:
            tagname = "video" if dtype == "video" else "audio"
            media_el = Element(tagname)
            # copy relevant attrs
            for k in (
                "src",
                "poster",
                "controls",
                "autoplay",
                "muted",
                "loop",
                "preload",
                "playsinline",
                "crossorigin",
            ):
                if g.get(k) is not None:
                    media_el.set(k, g.get(k, ""))
            # add <source> children from data-sources
            try:
                sources = json.loads(g.get("data-sources", "[]"))
            except Exception:
                sources = []
            for s in sources:
                sattrs = {"src": s.get("src", "")}
                if s.get("type"):
                    sattrs["type"] = s["type"]
                if s.get("media"):
                    sattrs["media"] = s["media"]
                SubElement(media_el, "source", **sattrs)
            # ensure non-selfclosing tags in XML serialization
            if len(media_el) == 0:
                media_el.text = ""
            replacement = wrap_in_figure(media_el)

        # replace in tree
        parent = g.getparent()
        if parent is not None and replacement is not None:
            idx = parent.index(g)
            # preserve tail text when replacing
            if g.tail:
                replacement.tail = g.tail
                g.tail = None
            parent.remove(g)
            parent.insert(idx, replacement)

    # Then, convert remaining internal tags to HTML
    for elem in tree.iter(HTML_CONVERSIONS.keys()):
        conversion = HTML_CONVERSIONS[str(elem.tag)]
        if callable(conversion):
            elem.tag = conversion(elem)
        else:
            elem.tag = conversion  # type: ignore[assignment]
        # handle attributes for links
        if elem.tag == "a":
            elem.set("href", elem.attrib.pop("target", ""))
        else:
            elem.attrib.clear()

    # After conversion, split paragraphs that contain block-level <figure>
    for fig in list(tree.iter("figure")):
        parent = fig.getparent()
        if parent is not None and parent.tag == "p":
            p = parent
            idx_fig = p.index(fig)
            # left part
            p_before = Element("p")
            p_before.text = p.text
            for _ in range(idx_fig):
                left_child: _Element = p[0]
                p.remove(left_child)
                p_before.append(left_child)
            # right part
            p_after = Element("p")
            # figure tail belongs to the right paragraph
            if fig.tail:
                p_after.text = fig.tail
                fig.tail = None
            # move remaining children to right paragraph
            while len(p) > 0:
                right_child: _Element = p[0]
                p.remove(right_child)
                p_after.append(right_child)

            # insert p_before, fig, p_after around original p
            grand = p.getparent()
            if grand is not None:
                idx_p = grand.index(p)
                # remove original p
                grand.remove(p)
                # insert in reverse order to preserve positions
                if len(p_after) > 0 or (p_after.text and p_after.text.strip()):
                    grand.insert(idx_p, p_after)
                grand.insert(idx_p, fig)
                if len(p_before) > 0 or (p_before.text and p_before.text.strip()):
                    grand.insert(idx_p, p_before)

    tree.tag = "body"
    root = Element("html")
    root.append(tree)
    return root


def build_html_output(document: Document, with_metadata: bool = False) -> str:
    "Convert the document to HTML and return a string."
    html_tree = convert_to_html(document.body)

    if with_metadata:
        head = Element("head")
        for item in META_ATTRIBUTES:
            if value := getattr(document, item):
                SubElement(head, "meta", name=item, content=value)
        html_tree.insert(0, head)

    return tostring(html_tree, pretty_print=True, encoding="unicode").strip()
