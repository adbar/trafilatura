import re
from bs4 import BeautifulSoup

REGEXPS = {
    "unlikelyCandidates": re.compile(
        r"-ad-|ai2html|banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|footer|gdpr|header|"
        r"legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|"
        r"ad-break|agegate|pagination|pager|popup|yom-remote",
        re.I,
    ),
    "okMaybeItsACandidate": re.compile(
        r"and|article|body|column|content|main|shadow", re.I
    ),
}

DISPLAY_NONE = re.compile(r"display:\s*none", re.I)


def is_node_visible(node):
    # This will handle visibility checking in the context of BeautifulSoup nodes
    style = node.get("style", "")

    is_hidden = DISPLAY_NONE.search(style) is not None or node.get("hidden") is not None
    aria_hidden = node.get(
        "aria-hidden"
    ) == "true" and "fallback-image" not in node.get("class", "")
    return not is_hidden and not aria_hidden


def is_probably_readerable(doc, options=None):
    if callable(options):
        options = {"visibilityChecker": options}
    elif options is None:
        options = {}

    default_options = {
        "minScore": 20,
        "minContentLength": 140,
        "visibilityChecker": is_node_visible,
    }
    default_options.update(options)
    options = default_options

    soup = BeautifulSoup(doc, "html.parser")
    nodes = soup.select("p, pre, article")

    # Include divs that directly contain <br> tags
    for node in soup.select("div > br"):
        nodes.append(node.parent)

    score = 0
    for node in nodes:
        if not options["visibilityChecker"](node):
            continue

        class_id_string = f"{node.get('class', '')} {node.get('id', '')}"
        if REGEXPS["unlikelyCandidates"].search(class_id_string) and not REGEXPS[
            "okMaybeItsACandidate"
        ].search(class_id_string):
            continue

        if node.name == "li" and node.find("p"):
            continue

        text_content_length = len(node.get_text(strip=True))
        if text_content_length < options["minContentLength"]:
            continue

        score += (text_content_length - options["minContentLength"]) ** 0.5
        if score > options["minScore"]:
            return True

    return False
