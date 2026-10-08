"""Regression coverage for primary infinite-scroll article shells (issue #961).

Synthetic prose preserves the reported DOM structure without copying news text.
"""

import pytest
from lxml import html

from trafilatura import extract
from trafilatura.xpaths import RAW_TREE_PRUNE_XPATH

MODES = ({}, {"favor_precision": True}, {"fast": True})
PARAGRAPHS = (
    "The neighborhood repair workshop opened its doors on Saturday. Volunteers inspected several bicycles and recorded the spare parts needed for each repair.",
    "A new tool station provides clearly labeled storage for equipment. Organizers explained the borrowing procedure and demonstrated how to return every item safely.",
    "Several visitors helped rebuild a damaged bench beside the entrance. The team measured the boards carefully and tested the completed structure before opening the area.",
    "An afternoon class introduced simple maintenance techniques for household equipment. Participants practiced each procedure and wrote down questions for the next session.",
    "The library donated a collection of illustrated repair manuals. Volunteers catalogued the books and placed them on a shelf where future visitors can find them.",
    "At the end of the event, the organizers reviewed the completed repairs. They agreed to repeat the workshop next month and publish a list of useful materials.",
)


def paragraphs(count=6):
    return "".join(f"<p>{text}</p>" for text in PARAGRAPHS[:count])


def shell(count):
    return (
        "<div class='infinite-scroll'><nav><a href='/'>Home</a>"
        "<a href='/news'>News</a></nav><div class='article'>"
        "<h2>Community repair workshop opens</h2><div id='content'>"
        f"{paragraphs(count)}</div></div></div>"
    )


@pytest.mark.parametrize("mode", MODES, ids=("default", "precision", "fast"))
@pytest.mark.parametrize("count", [4, 6])
def test_primary_h2_shell_extracts_all_article_paragraphs(mode, count):
    result = extract(f"<html><body>{shell(count)}</body></html>", **mode) or ""
    for text in PARAGRAPHS[:count]:
        assert text in result
    assert "Home" not in result
    assert "News" not in result


@pytest.mark.parametrize("mode", MODES, ids=("default", "precision", "fast"))
def test_rendered_shell_excludes_page_chrome(mode):
    page = (
        "<html><body><noscript><p>Enable JavaScript to view the page.</p>"
        "</noscript>"
        + shell(6).replace(
            "</div></div></div>",
            "</div></div><div class='recommender'><h3>Recommended reads</h3>"
            "<p>Another workshop announces a separate event.</p></div></div>",
        )
        + "<footer><p>Copyright test publisher. All rights reserved.</p></footer>"
        "</body></html>"
    )
    result = extract(page, **mode) or ""
    for text in PARAGRAPHS:
        assert text in result
    for unwanted in ("Enable JavaScript", "separate event", "Copyright", "Home"):
        assert unwanted not in result


@pytest.mark.parametrize(
    "document, expected",
    [
        (
            "<div id='preview' class='infinite-scroll'><h2>Preview</h2></div><article><h1>Actual title</h1></article>",
            {"preview"},
        ),
        ("<h2>Navigation heading</h2><div id='primary' class='infinite-scroll'><h1>Actual title</h1></div>", set()),
        (
            (
                "<div id='primary' class='infinite-scroll'><h2>Actual title</h2></div>"
                "<div id='append' class='infinite-scroll'><h2>Next title</h2></div>"
            ),
            {"append"},
        ),
        ("<div id='append' class='infinite-scroll'><p>No heading</p></div>", {"append"}),
        ("<div id='mvp-post-add-box'><h1>Next title</h1></div>", {"mvp-post-add-box"}),
        ("<div id='mvp' class='mvp-post-add-wrap'><h2>Next title</h2></div>", {"mvp"}),
        (
            (
                "<section id='primary' class='infinite-scroll'><h2>Actual title</h2>"
                "</section><aside id='append' class='infinite-scroll'><h2>Next</h2>"
                "</aside>"
            ),
            {"append"},
        ),
        ("<div id='infinite-scroll'><h2>Actual title</h2></div>", set()),
    ],
    ids=(
        "preview-before-h1",
        "h1-after-other-h2",
        "first-h2-only",
        "no-heading",
        "mvp-h1",
        "mvp-h2",
        "section-aside",
        "id-shell",
    ),
)
def test_raw_pruning_matches_primary_heading_rule(document, expected):
    tree = html.fromstring(f"<html><body>{document}</body></html>")
    assert {element.get("id") for element in RAW_TREE_PRUNE_XPATH[0](tree)} == expected


@pytest.mark.parametrize("mode", MODES, ids=("default", "precision", "fast"))
@pytest.mark.parametrize("placement", ["after", "before", "mvp"])
def test_follow_up_regions_do_not_leak_into_article(mode, placement):
    real = "<article><h1>Repair workshop</h1>" + paragraphs() + "</article>"
    follow_up = (
        "<div class='infinite-scroll'><h2>Next story</h2>"
        "<p>This appended story concerns an unrelated museum exhibit and must "
        "not be included in the workshop article.</p></div>"
    )
    if placement == "mvp":
        follow_up = follow_up.replace("class='infinite-scroll'", "id='mvp-post-add-box'").replace(
            "<h2>Next story</h2>", "<h1>Next story</h1>"
        )
    body = follow_up + real if placement == "before" else real + follow_up
    result = extract(f"<html><body>{body}</body></html>", **mode) or ""
    assert PARAGRAPHS[0] in result
    assert "unrelated museum" not in result


@pytest.mark.parametrize("mode", MODES, ids=("default", "precision", "fast"))
def test_nav_only_shell_is_not_an_article(mode):
    page = (
        "<html><body><div class='infinite-scroll'><nav><a href='/'>Home</a><a href='/news'>News</a></nav></div></body></html>"
    )
    assert extract(page, **mode) is None
