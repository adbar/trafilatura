"""
Unit tests for the jusText-derived fallback (trafilatura/justext_lite.py, try_justext, justext_rescue).
"""

from lxml import etree, html

from trafilatura import core
from trafilatura.external import justext_rescue, try_justext
from trafilatura.justext_lite import extract_paragraphs
from trafilatura.utils import trim


def test_justext_hardening():
    "Unusable input gives an empty body."
    my_html = '<html><head><meta http-equiv="content-language" content="EN"/></head><body><div="article-body"><p>Text.<!-- comment --><?php echo "This is a PHP processing instruction"; ?></p></div></body></html>'
    assert etree.tostring(try_justext(html.fromstring(my_html), None)) == b"<body/>"
    assert etree.tostring(try_justext(None, None)) == b"<body/>"


def test_justext_lite():
    "block segmentation, link density, copyright and select rules, context revision of short blocks, block kinds"

    def texts(tree):
        return [text for text, *_ in extract_paragraphs(tree)]

    long = "This sentence is long enough to be classified as content by itself. " * 3
    my_html = (
        f"<html><body><div><p>{long}</p><p>Short line.</p><p>{long}<!-- note -->More.</p>"
        '<ul><li><a href="#">Home</a></li><li><a href="#">About</a></li></ul>'
        f"<p>© 2026 Company</p><select><option>{long}</option></select><div><br></div></div></body></html>"
    )
    assert texts(html.fromstring(my_html)) == [long.strip(), "Short line.", long + "More."]
    # text after a select is not part of it
    my_html = f"<html><body><div><select><option>{long}</option></select>{long}</div></body></html>"
    assert texts(html.fromstring(my_html)) == [long.strip()]
    # a short block next to boilerplate only is dropped
    my_html = f'<html><body><p>{long}</p><div><a href="#">{long}</a></div><p>Short line.</p></body></html>'
    assert texts(html.fromstring(my_html)) == [long.strip()]
    # a short block after a near-good one is kept, the near-good one follows its good neighbour
    mid = "A medium paragraph, longer than fifty characters but short."
    my_html = f'<html><body><div><a href="#">Home</a> <a href="#">About us</a></div><p>{mid}</p><p>Short line.</p><p>{long}</p></body></html>'
    assert texts(html.fromstring(my_html)) == [mid, "Short line.", long.strip()]
    # same on the right side
    my_html = f'<html><body><p>{long}</p><p>Short line.</p><p>{mid}</p><div><a href="#">Home</a> <a href="#">About us</a></div></body></html>'
    assert texts(html.fromstring(my_html)) == [long.strip(), "Short line.", mid]
    # whitespace between inline elements separates words
    my_html = f"<html><body><p>{long}<b>one</b> <i>two</i></p></body></html>"
    assert texts(html.fromstring(my_html)) == [long + "one two"]
    # line breaks are kept, other whitespace is collapsed
    root = etree.Element("body")
    etree.SubElement(root, "p").text = f"{long}\r  {long}"
    assert texts(root) == [f"{long.strip()}\n{long.strip()}"]
    # nested link text counts towards link density
    my_html = f'<html><body><p>{long}</p><p><a href="#">x <b>{long}</b></a> tail</p></body></html>'
    assert texts(html.fromstring(my_html)) == [long.strip()]
    # hidden data blobs and scrolling link farms are skipped, their tail stays
    my_html = f"<html><body><p>{long}</p><textarea hidden>{long}</textarea>{long}<marquee>{long}</marquee></body></html>"
    assert texts(html.fromstring(my_html)) == [long.strip(), long.strip()]
    my_html = f"<html><body><p>{long}foo<textarea>x</textarea>bar<marquee>x</marquee>baz</p></body></html>"
    assert texts(html.fromstring(my_html)) == [long + "foo bar baz"]
    # markup held as text in raw-text fallbacks is skipped, a noscript with children or plain text stays
    markup = f"&lt;div class='ad'&gt;{long}&lt;/div&gt;"
    my_html = f"<html><body><p>{long}<iframe>{markup}</iframe>after</p><noscript>{markup}</noscript></body></html>"
    assert texts(html.fromstring(my_html)) == [long + "after"]
    my_html = f"<html><body><noscript><p>{long}</p></noscript><noscript>{long}</noscript></body></html>"
    assert texts(html.fromstring(my_html)) == [long.strip(), long.strip()]
    # hidden blocks are skipped with their tail kept, click-to-open panels stay
    my_html = (
        f'<html><body><div>{long}<div style="display: none">{long}</div>after</div>'
        f'<div class="faq-answer" style="display:none">{long}</div></body></html>'
    )
    assert texts(html.fromstring(my_html)) == [long + "after", long.strip()]
    # the page and the root of the walk are never skipped
    my_html = f'<html style="display:none"><body style="display: none"><p>{long}</p></body></html>'
    assert texts(html.fromstring(my_html)) == [long.strip()]
    root = etree.Element("div", style="display:none")
    etree.SubElement(root, "p").text = long
    assert texts(root) == [long.strip()]
    # no stopwords: scripts without a jusText stoplist are classified like the others
    thai = "ภาษาไทยเป็นภาษาราชการของประเทศไทยและมีผู้พูดหลายสิบล้านคนทั่วประเทศ " * 3
    amharic = "አማርኛ የኢትዮጵያ የሥራ ቋንቋ ሲሆን በብዙ ሚሊዮን ሰዎች ይነገራል። " * 4
    my_html = f'<html><body><div><a href="#">หน้าแรก</a></div><p>{thai}</p><p>{amharic}</p></body></html>'
    assert texts(html.fromstring(my_html)) == [thai.strip(), amharic.strip()]
    # namespaced tags, deep trees
    my_html = f'<html xmlns="http://www.w3.org/1999/xhtml"><body><p>{long}</p><p>{long}</p></body></html>'
    assert len(texts(etree.fromstring(my_html))) == 2
    root = elem = etree.Element("body")
    for _ in range(5000):
        elem = etree.SubElement(elem, "div")
    etree.SubElement(elem, "p").text = long
    assert texts(root) == [long.strip()]
    # basic_cleaning targets are skipped with their tail kept, the input tree is left untouched
    my_html = f'<html><body><div>{long}<aside>{long}</aside>tail</div><div id="cookie-banner"><p>{long}</p></div><p>{long}</p></body></html>'
    tree = html.fromstring(my_html)
    before = etree.tostring(tree)
    assert texts(tree) == [long + "tail", long.strip()]
    assert etree.tostring(tree) == before
    # block kinds from the enclosing tags, lists grouped in the output
    my_html = (
        f"<html><body><h2><span>{long}</span></h2><ul><li>{long}</li><li><p>{long}</p></li></ul>"
        f"<pre>{long}</pre><blockquote><p>{long}</p></blockquote><div>{long}</div></body></html>"
    )
    assert [kind for _, kind, *_ in extract_paragraphs(html.fromstring(my_html))] == ["h2", "ul", "ul", "code", "quote", "p"]
    result = try_justext(html.fromstring(my_html), None)
    assert [elem.tag for elem in result.iter()] == ["body", "head", "list", "item", "item", "code", "quote", "p"]
    assert result[0].get("rend") == "h2"
    # list types, an ol next to a ul starts a new list
    my_html = f"<html><body><ol><li>{long}</li><li>{long}</li></ol><ul><li>{long}</li></ul></body></html>"
    result = try_justext(html.fromstring(my_html), None)
    assert [(elem.get("rend"), len(elem)) for elem in result] == [("ol", 2), ("ul", 1)]
    # adjacent lists of the same type stay apart, code in a list item stays code
    my_html = f"<html><body><ul><li>{long}</li></ul><ul><li>{long}</li><li><pre>{long}</pre></li></ul></body></html>"
    result = try_justext(html.fromstring(my_html), None)
    assert [(elem.tag, len(elem)) for elem in result] == [("list", 1), ("list", 1), ("code", 0)]
    # a nested list is flattened into its outermost list, which keeps its type
    my_html = f"<html><body><ul><li>{long}<ol><li>{long}</li></ol></li><li>{long}</li></ul></body></html>"
    result = try_justext(html.fromstring(my_html), None)
    assert [(elem.get("rend"), len(elem)) for elem in result] == [("ul", 3)]
    # adjacent definition lists stay apart
    my_html = f"<html><body><dl><dt>{long}</dt><dd>{long}</dd></dl><dl><dt>{long}</dt></dl></body></html>"
    result = try_justext(html.fromstring(my_html), None)
    assert [(elem.tag, len(elem)) for elem in result] == [("list", 2), ("list", 1)]
    # characters lxml rejects are removed from the text, the rest of the output stays
    result = try_justext(html.fromstring(f"<html><body><p>{long}</p><p>{long}x\x01y‌z</p></body></html>"), None)
    assert [elem.text[-4:] for elem in result] == ["elf.", "xy‌z"]
    # only the direct parent makes a heading: an unclosed one can hold the rest of the page
    my_html = f"<html><body><h1>{long}<div>{long}</div></h1></body></html>"
    assert [kind for _, kind, *_ in extract_paragraphs(html.fromstring(my_html))] == ["h1", "p"]
    # code keeps its indentation and line breaks, also between inline elements
    code = f"def f(x):\n    if x:\n        return x  # {long}"
    my_html = f"<html><body><pre>\n{code}<br><span>a</span>\n    <span>b</span>\n</pre></body></html>"
    assert texts(html.fromstring(my_html)) == [f"{code}\na\n    b"]
    # hidden styles in any case and spacing
    my_html = f'<html><body><p>{long}</p><div style="DISPLAY : NONE">{long}</div></body></html>'
    assert texts(html.fromstring(my_html)) == [long.strip()]
    # the page title is left out, HTML5 sections end a block
    my_html = f"<html><head><title>{long}</title></head><body><section>{long}</section><section>{long}</section></body></html>"
    assert texts(html.fromstring(my_html)) == [long.strip(), long.strip()]


def test_justext_lite_markup():
    "links, formatting and images follow the options, the plain text stays the same"
    long = "This sentence is long enough to be classified as content by itself. " * 3
    my_html = (
        f'<html><body><p>{long}<b>bold</b>, <a href="/x">a <i>link</i></a><span> and</span> <img src="a.jpg"> end.</p>'
        f"<em><div>{long}</div><div>{long}</div></em><p>{long}x <code>y </code>\n z</p></body></html>"
    )
    plain = try_justext(html.fromstring(my_html), None)
    assert [len(elem) for elem in plain] == [0, 0, 0, 1]
    assert plain[0].text == long + "bold, a link and end."
    assert etree.tostring(plain[3], encoding=str) == f"<p>{long}x <code>y</code>\nz</p>"
    options = core.Extractor(output_format="xml", links=True, formatting=True, images=True)
    options.url = "https://example.org/a/"
    body, text = justext_rescue(html.fromstring(my_html), options)
    assert etree.tostring(body[0], encoding=str) == (
        f'<p>{long}<hi rend="#b">bold</hi>, <ref target="https://example.org/x">a <hi rend="#i">link</hi></ref> and '
        '<graphic src="https://example.org/a/a.jpg"/>end.</p>'
    )
    # formatting around blocks is reopened in each of them
    assert [etree.tostring(elem, encoding=str) for elem in body[1:3]] == [f'<p><hi rend="#i">{long.strip()}</hi></p>'] * 2
    # the length is the one of the plain text, without spaces at element boundaries
    assert text == trim(" ".join("".join(elem.itertext()) for elem in plain))
    # headings and list items keep their markup, an image leaves its link, attributes lose control characters
    my_html = (
        f"<html><body><h2>{long}<b>h</b></h2><ul><li>{long}<b>i</b></li></ul>"
        f'<p>{long}<a href="/z\x01"><img src="b.jpg" alt="p\x0bq">pic</a></p></body></html>'
    )
    body, _ = justext_rescue(html.fromstring(my_html), options)
    assert [etree.tostring(elem, encoding=str) for elem in body] == [
        f'<head rend="h2">{long}<hi rend="#b">h</hi></head>',
        f'<list rend="ul"><item>{long}<hi rend="#b">i</hi></item></list>',
        f'<p>{long}<graphic src="https://example.org/a/b.jpg" alt="pq"/><ref target="https://example.org/z">pic</ref></p>',
    ]
    # lazy-loaded images, as in image_src
    body, _ = justext_rescue(html.fromstring(f'<html><body><p>{long}<img data-src-large="c.jpg"></p></body></html>'), options)
    assert etree.tostring(body[0], encoding=str) == f'<p>{long.strip()}<graphic src="https://example.org/a/c.jpg"/></p>'
