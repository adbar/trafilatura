"""
Unit tests for baseline functions of the trafilatura library.
"""

import json
import sys
from html import escape

import pytest
from lxml import html
from trafilatura import baseline, html2txt


def jsonld_doc(payload: str, body: str = "") -> str:
    "Wrap a JSON-LD payload (and optional body HTML) into a minimal page."
    return f'<html><head><script type="application/ld+json">{payload}</script></head><body>{body}</body></html>'


def test_baseline():
    # Empty input
    result = baseline(b"")
    assert isinstance(result, tuple) and len(result) == 3
    assert result[0].tag == "body"
    assert result[1] == ""
    assert result[2] == 0

    result = baseline("")
    assert isinstance(result, tuple) and len(result) == 3
    assert result[0].tag == "body"
    assert result[1] == ""
    assert result[2] == 0

    # Invalid HTML
    _, result, _ = baseline(b"<invalid html>")
    assert result == ""

    tests = [
        (
            "<html><body><article>" + "The article consists of this text." * 10 + "</article></body></html>",
            "The article consists of this text.",
        ),
        (
            "<html><body><article><b>The article consists of this text.</b></article></body></html>",
            "The article consists of this text.",
        ),
        (
            "<html><body><quote>This is only a quote but it is better than nothing.</quote></body></html>",
            "This is only a quote but it is better than nothing.",
        ),
    ]
    for doc, expected in tests:
        _, result, _ = baseline(doc)
        assert expected in result

    # Invalid JSON
    filecontent = b"""
        <html>
            <body>
                <script type="application/ld+json">
                    {"articleBody": "This is the article body, it has to be long enough to fool the length threshold which is set at len 100."  # invalid JSON
                </script>
            </body>
        </html>
    """
    _, result, _ = baseline(filecontent)
    assert result == ""

    # JSON OK
    filecontent = b"""
        <html>
            <body>
                <script type="application/ld+json">
                    {
                        "@type": "Article",
                        "articleBody": "This is the article body, it has to be long enough to fool the length threshold which is set at len 100."
                    }
                </script>
            </body>
        </html>
    """
    _, result, _ = baseline(filecontent)
    assert len(result) > 100

    # articleBody wrapped in a single paragraph: markup is parsed, not returned literally
    filecontent = rb"""
        <html>
            <body>
                <script type="application/ld+json">
                    {
                        "@type": "Article",
                        "articleBody": "<p>This is the article body, it has to be long enough to fool the length threshold which is set at len 100.<\/p>"
                    }
                </script>
            </body>
        </html>
    """
    _, result, _ = baseline(filecontent)
    assert result.startswith("This is the article body") and "<p>" not in result

    # Real-world examples
    my_document = r'<html><body><script type="application/ld+json">{"description":"In letzter Zeit kam man am Begriff \"Hygge\", was so viel wie \"angenehm\" oder \"gemütlich\" bedeutet, ja nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend ...","image":[{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/uncropped-0-0\/7d00b2658fd0a3b19e1b161f4657cc20\/Xw\/ikigai--1-.jpg","width":"2048","height":"1366","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-1280-720\/bf947c7c24167d7c0adae0be10942d57\/Uf\/ikigai--1-.jpg","width":"1280","height":"720","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-938-528\/bf947c7c24167d7c0adae0be10942d57\/JK\/ikigai--1-.jpg","width":"938","height":"528","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/large1x1-622-622\/f5544b7d67e1be04f7729b130e7e0485\/KN\/ikigai--1-.jpg","width":"622","height":"622","@type":"ImageObject"}],"mainEntityOfPage":{"@id":"https:\/\/www.brigitte.de\/liebe\/persoenlichkeit\/ikigai-macht-dich-sofort-gluecklicher--10972896.html","@type":"WebPage"},"headline":"Ikigai macht dich sofort glücklicher!","datePublished":"2019-06-19T14:29:08+0000","dateModified":"2019-06-19T14:29:10+0000","author":{"name":"BRIGITTE.de","@type":"Organization"},"publisher":{"name":"BRIGITTE.de","logo":{"url":"https:\/\/image.brigitte.de\/11476842\/uncropped-0-0\/f19537e97b9189bf0f25ce924168bedb\/kK\/bri-logo-schema-org.png","width":"167","height":"60","@type":"ImageObject"},"@type":"Organization"},"articleBody":"In letzter Zeit kam man am Begriff \"Hygge\" (\"gemütlich\" oder \"angenehm\") nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend Konkurrenz: \"Ikigai\". Bist du glücklich? Schwierige Frage, nicht wahr? Viele von uns müssen da erst mal überlegen.","@type":"NewsArticle"}</script></body></html>'
    _, result, _ = baseline(my_document)
    assert result.startswith("In letzter Zeit kam man") and result.endswith("erst mal überlegen.")

    my_document = "<html><body><div>   Document body...   </div><script> console.log('Hello world') </script></body></html>"
    _, result, _ = baseline(my_document)
    assert result == "Document body..."


def test_baseline_strategy_fallthrough():
    "regression: a too-short JSON-LD body must not leave a stale postbody that blocks later strategies."
    para = "Real paragraph content that should be extracted by the paragraph strategy, comfortably long enough for the gate."
    _, result, length = baseline(jsonld_doc('{"articleBody": "Too short."}', body=f"<p>{para}</p>"))
    assert para in result and length > 100


def test_baseline_jsonld_shapes():
    "regression: articleBody must be found in list-wrapped and @graph-nested JSON-LD, not just flat dicts."
    body_text = (
        "Body text from structured data, made comfortably long enough to pass the one hundred character length threshold."
    )
    flat = '{"articleBody": "%s"}' % body_text
    graph = '{"@context": "https://schema.org", "@graph": [{"@type": "Article", "articleBody": "%s"}]}' % body_text
    wrapped = '[{"@type": "Article", "articleBody": "%s"}]' % body_text
    for payload in (flat, graph, wrapped):
        assert baseline(jsonld_doc(payload))[1].count(body_text) == 1


def test_baseline_jsonld_content():
    "regression: articleBody with raw control chars, p-less markup or HTML-escaped markup yields clean text."

    def run(body: str) -> str:
        return baseline(jsonld_doc('{"articleBody": "%s"}' % body))[1]

    # raw newline/tab inside the JSON string (invalid in strict mode but common in the wild)
    ctrl = "First line of the body text\n\twith a raw newline and a tab inside the JSON string, comfortably long enough to pass the gate."
    assert "First line of the body text with a raw newline" in run(ctrl)
    # markup without <p> must not leak literal tags
    markup = "Opening text<br/>more after a break element<div>and inside a div</div> comfortably long enough to pass the one hundred character gate."
    assert "<" not in run(markup) and "Opening text" in run(markup)
    # HTML-escaped markup must be unescaped and parsed, not emitted as entities
    escaped = "&lt;p&gt;Escaped paragraph body text that should come out clean, comfortably long enough to pass the one hundred character gate.&lt;/p&gt;"
    result = run(escaped)
    assert "&lt;" not in result and "Escaped paragraph body text" in result
    # a lone comparison operator in plain prose stays intact
    prose = "Comparing a < b in plain prose should stay intact, with padding to exceed the one hundred character gate."
    assert "a < b" in run(prose)
    # tag-shaped comparison expressions (a letter right after "<") must not be swallowed either
    expr = "For x<y and z>0 the series converges absolutely, with plenty of extra padding to exceed the length gate here."
    assert "x<y and z>0" in run(expr)
    # regression (review round 3): the letters after "<" are single-letter TAG names (p, q, u, s,
    # i, b) -- the old greedy [^>]* matched "<q ... c>" as one tag and deleted the whole span
    tagletters = (
        "If p<q then u<s or i<b and c>d holds, with extra padding to comfortably exceed the one hundred character gate."
    )
    assert "p<q" in run(tagletters) and "i<b and c>d holds" in run(tagletters)


def test_baseline_teaser_does_not_shadow_longer_body():
    "regression (review round 3): a schema.org Product/VideoObject description is a short teaser \
    and must not preempt a longer whole-body dump carrying the real content in bare divs (no \
    <article>, no <p>-family, so no earlier tier reaches it)."
    desc = (
        "Short marketing product blurb standing in as a JSON-LD teaser, just past the one hundred character content gate here."
    )
    divs = "".join(
        f"<div>Real article paragraph number {i} with genuine sentence content that only the "
        f"whole-body dump captures from these bare div elements on the page.</div>"
        for i in range(5)
    )
    jsonld = '{"@type": "Product", "description": "%s"}' % desc
    _, text, _ = baseline(jsonld_doc(jsonld, body=divs))
    assert "Real article paragraph number 3" in text


def test_baseline_teaser_used_when_body_shorter():
    "the teaser still wins when the body dump is shorter than it (near-empty body, e.g. a JS shell)."
    desc = "Full product description carrying the actual page content, comfortably longer than the sparse body below and past the gate."
    jsonld = '{"@type": "Product", "description": "%s"}' % desc
    _, text, _ = baseline(jsonld_doc(jsonld, body="<div>x</div>"))
    assert "Full product description" in text


@pytest.mark.parametrize("teaser_type", ["Product", "VideoObject"])
def test_baseline_description_teaser_tier(teaser_type):
    "Product/VideoObject descriptions are last-resort teasers: used when alone on the page, \
    outranked by any full-text source (a JSON articleBody or an HTML paragraph)."
    teaser = "Description teaser standing in for page content, comfortably longer than the one hundred character gate here."
    fulltext = "The full body text which must take precedence over the description teaser and clears the gate comfortably."
    teaser_json = json.dumps({"@type": teaser_type, "description": teaser})
    assert teaser in baseline(jsonld_doc(teaser_json))[1]  # alone -> used
    both = json.dumps([{"@type": teaser_type, "description": teaser}, {"@type": "Article", "articleBody": fulltext}])
    outranked = baseline(jsonld_doc(both))[1]  # JSON full-text property wins
    assert fulltext in outranked and teaser not in outranked
    outranked = baseline(jsonld_doc(teaser_json, body=f"<p>{fulltext}</p>"))[1]  # HTML paragraph wins
    assert fulltext in outranked and teaser not in outranked


def test_baseline_jsonld_double_embed():
    "regression: the same JSON-LD block embedded twice (theme and SEO plugin both emitting \
    it) must not duplicate the article body; same for duplicated teaser descriptions."
    body = "Article body text embedded twice via duplicated JSON-LD scripts, comfortably longer than the one hundred character strategy gate."
    desc = "Video description standing in for page content here, comfortably longer than the one hundred character gate."
    for content, payload in (
        (body, '{"articleBody": "%s"}'),
        (desc, '{"@type": "VideoObject", "description": "%s"}'),
    ):
        script = f'<script type="application/ld+json">{payload % content}</script>'
        _, text, _ = baseline(f"<html><head>{script}{script}</head><body></body></html>")
        assert text.count(content) == 1


_CTRL = "before\x01after, with plenty of padding words to pass the one hundred character strategy gate comfortably."


@pytest.mark.parametrize(
    "doc",
    [
        jsonld_doc('{"articleBody": "%s"}' % _CTRL),
        f"<html><body><p>{_CTRL}</p></body></html>",
        f"<html><body><div>{_CTRL}</div></body></html>",
    ],
    ids=["json_build_body", "paragraph_build_body", "default_dump"],
)
def test_baseline_control_chars_tree_input(doc):
    "regression: non-whitespace control chars survive json.loads(strict=False) and caller-built trees \
    (trafilatura's parser strips them from str input, lxml.html.fromstring does not); they must not \
    crash the lxml .text assignment at any baseline sink (JSON/paragraph _build_body, whole-body dump)."
    _, text, length = baseline(html.fromstring(doc))
    assert length > 100 and "\x01" not in text and "before" in text and "after" in text


def test_baseline_nested_paragraph_not_duplicated():
    "regression: a <p> nested in a <blockquote> with surrounding text must not be emitted twice \
    by the paragraph strategy (its text is a substring of the container's, not an exact match)."
    para = "Quoted paragraph text repeated by nesting here, made comfortably longer than the one hundred character strategy gate threshold."
    doc = f"<html><body><blockquote>Attribution line: <p>{para}</p></blockquote></body></html>"
    _, text, _ = baseline(doc)
    assert text.count(para) == 1


def test_baseline_paragraph_dedup_keeps_short_repeats():
    "regression: the paragraph strategy's substring dedup must not drop a short, distinct \
    paragraph just because its text recurs inside earlier, unrelated prose."
    long_para = "The annual conference will be held in Berlin this coming September, organizers said today."
    short_para = "held in Berlin"
    doc = f"<html><body><p>{long_para}</p><p>{short_para}</p></body></html>"
    _, text, _ = baseline(doc)
    assert text.count(short_para) == 2  # once inside long_para, once standalone


def test_baseline_dedup_keeps_cross_boundary_paragraph():
    "regression (review round 3): the substring dedup accumulator must not drop a distinct \
    paragraph whose text spans the join boundary of two earlier consecutive paragraphs -- a \
    space-joined accumulator saw it as a repeat (fixed by joining on a newline, which trimmed \
    paragraph text never contains). Asserts on emitted paragraphs, not the joined string, \
    which would still contain the phrase as a cross-boundary substring."
    from trafilatura.baseline import _build_body

    p1 = "The meeting concluded with remarks about the annual budget"
    p2 = "planning process that begins next week according to officials."
    p3 = "annual budget planning process that begins next week"  # tail of p1 + head of p2, >50 chars
    body, _ = _build_body([p1, p2, p3], dedupe=True)
    assert len(body) == 3
    assert body[2].text == p3


def test_baseline_article_nested_not_duplicated():
    "regression: a nested <article> (article-in-article shell) must not be counted both \
    inside its ancestor's text and again standalone by the article strategy."
    inner = "Inner article content sentence repeated to build a properly long body text here. " * 3
    doc = f"<html><body><article>Outer wrapper. <article>{inner}</article></article></body></html>"
    _, text, _ = baseline(doc)
    assert text.count(inner.strip()) == 1


def test_baseline_schema_properties():
    "schema.org text properties beyond articleBody: recipe steps and FAQ answers."
    recipe = json.dumps(
        {
            "@type": "Recipe",
            "recipeInstructions": [
                {
                    "@type": "HowToStep",
                    "text": "Mix the flour with sugar and butter until the dough is smooth and pliable in texture.",
                },
                {
                    "@type": "HowToStep",
                    "text": "Bake for thirty five minutes at one hundred eighty degrees until golden brown on top.",
                },
            ],
        }
    )
    _, result, _ = baseline(jsonld_doc(recipe))
    assert "Mix the flour" in result and "Bake for thirty five minutes" in result

    faq = json.dumps(
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "How?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "This is the accepted answer to the question, written with a comfortable amount of words to pass the one hundred character gate.",
                    },
                }
            ],
        }
    )
    _, result, _ = baseline(jsonld_doc(faq))
    assert "This is the accepted answer" in result


def test_baseline_discourse_preload():
    "Discourse forums: posts live as JSON in the data-preloaded attribute of an empty page."
    topic = json.dumps(
        {
            "post_stream": {
                "posts": [
                    {"cooked": "<p>First forum post with a good amount of substantive discussion content in it.</p>"},
                    {"cooked": "<p>Second forum post continuing the thread with more useful information for everyone.</p>"},
                ]
            }
        }
    )
    preloaded = escape(json.dumps({"topic_12": topic}), quote=True)
    doc = f'<html><body><div id="data-preloaded" data-preloaded="{preloaded}"></div></body></html>'
    _, result, _ = baseline(doc)
    assert "First forum post" in result and "Second forum post" in result
    assert "<p>" not in result


def test_baseline_discourse_preload_malformed():
    "regression: valid but non-dict JSON in data-preloaded (or a non-dict post entry) must not crash \
    baseline() -- it should just fall through to the next strategy."
    para = "Real paragraph content that should be extracted by the paragraph strategy, comfortably long enough for the gate."
    for preloaded in ("[]", '"just a string"', escape(json.dumps({"topic_12": '["not", "a", "dict"]'}), quote=True)):
        doc = f'<html><body><div id="data-preloaded" data-preloaded="{preloaded}"></div><p>{para}</p></body></html>'
        _, result, _ = baseline(doc)
        assert para in result


def test_build_body_dedupe_cap(monkeypatch):
    "past DEDUPE_SCAN_CAP the paragraph strategy skips the substring scan and keeps potential repeats (cf. recover_wild_text)."
    from trafilatura.baseline import _build_body

    # the package re-exports the baseline() function, shadowing the submodule attribute
    bl_module = sys.modules["trafilatura.baseline"]
    filler = "Opening paragraph content long enough to push the accumulated text past a tiny cap."
    dup = "This exact paragraph repeats and is well above the duplicate length gate for sure."

    monkeypatch.setattr(bl_module, "DEDUPE_SCAN_CAP", 50)
    _, text = _build_body([filler, dup, dup], dedupe=True)
    assert text.count(dup) == 2  # past the cap: scan skipped, repeat kept

    monkeypatch.setattr(bl_module, "DEDUPE_SCAN_CAP", 200_000)
    _, text = _build_body([filler, dup, dup], dedupe=True)
    assert text.count(dup) == 1  # under the cap: substring dedup fires


def test_baseline_howto():
    "HowTo step/itemListElement text is content (own text and nested itemListElement both kept)."
    step_text = "Measure the table and add the overhang you want on every side before cutting any fabric at all."
    howto = json.dumps(
        {
            "@type": "HowTo",
            "step": [
                {
                    "@type": "HowToSection",
                    "itemListElement": {
                        "@type": "HowToDirection",
                        "text": step_text + " Then hem the edges neatly all around the cloth.",
                    },
                }
            ],
        }
    )
    _, result, _ = baseline(jsonld_doc(howto))
    assert step_text in result

    # a step carrying BOTH its own text and an itemListElement keeps both
    both = json.dumps(
        {
            "@type": "HowTo",
            "step": [
                {
                    "@type": "HowToStep",
                    "text": "Own step text: preheat the oven to a moderate temperature first.",
                    "itemListElement": [
                        {"@type": "HowToDirection", "text": "Set the dial to one hundred and eighty degrees."}
                    ],
                }
            ],
        }
    )
    _, result, _ = baseline(jsonld_doc(both))
    assert "preheat the oven" in result and "one hundred and eighty" in result


def test_baseline_element_input_not_mutated():
    "the public baseline() must not modify a caller-supplied tree (mirrors html2txt's guard)"
    doc = "<html><body><aside>side text</aside><p>" + "Real paragraph content on the page. " * 4 + "</p></body></html>"
    tree = html.fromstring(doc)
    _, text, _ = baseline(tree)
    assert "Real paragraph content" in text and "side text" not in text
    assert tree.find(".//aside") is not None  # basic_cleaning ran on a copy


def test_baseline_article_dominance():
    "article strategy: a dominant article drops much smaller siblings (teasers), similar-sized ones all stay."
    main = "Main article content sentence repeated to build a properly dominant body. " * 8  # ~600 chars
    teaser = "Related article teaser text that comfortably exceeds the length gate...."  # >100, < max/5
    doc = f"<html><body><article>{main}</article><article>{teaser}{teaser[:40]}</article></body></html>"
    _, result, _ = baseline(doc)
    assert "Main article content" in result and "Related article teaser" not in result

    post = "Forum post number {} with a comparable amount of discussion text in every single post here."
    doc2 = "<html><body>" + "".join(f"<article>{post.format(i)}</article>" for i in range(3)) + "</body></html>"
    _, result2, _ = baseline(doc2)
    assert all(post.format(i) in result2 for i in range(3))


def test_html2txt():
    mydoc = "<html><body>Here is the body text</body></html>"
    assert html2txt(mydoc) == "Here is the body text"
    assert html2txt(html.fromstring(mydoc)) == "Here is the body text"
    assert html2txt("") == ""
    assert html2txt("123") == ""
    assert html2txt("<html></html>") == ""
    assert html2txt("<html><body/></html>") == ""
    assert html2txt("<html><body><style>font-size: 8pt</style><p>ABC</p></body></html>") == "ABC"
    # block boundaries stay separated on minified pages, inline runs stay joined
    minified = "<html><body><p>First block.</p><p>Second block.</p><h2>Heading</h2>line<br>break</body></html>"
    assert html2txt(minified) == "First block. Second block. Heading line break"
    assert html2txt("<html><body><div>a<p>b</p></div></body></html>") == "a b"
    assert html2txt("<html><body><p>Hyper<b>link</b></p></body></html>") == "Hyperlink"
    # an element input is left untouched by the cleaning
    tree = html.fromstring("<html><body><aside>side</aside><p>content</p></body></html>")
    assert html2txt(tree) == "content"
    assert "side" in tree.text_content()
    # an element without a body still yields its text
    assert html2txt(html.fromstring("<div><p>bare element text</p></div>")) == "bare element text"
    # ... but a parsed document without a body (e.g. a feed) is not HTML text:
    # cli --probe relies on "" here to skip non-HTML URLs
    feed = (
        '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Feed title</title>'
        "<entry><title>Entry one</title><summary>Summary one</summary></entry>"
        "<entry><title>Entry two</title><summary>Summary two</summary></entry></feed>"
    )
    assert html2txt(feed) == ""
    # spec-invisible content is not text: template is never rendered, svg text is graphical
    invisible = "<html><body><svg><title>Icon name</title></svg><template><p>markup</p></template><p>visible</p></body></html>"
    assert html2txt(invisible) == "visible"
    # regression (review round 3): a caller-supplied tree can hold control chars lxml rejects on
    # write; html2txt must not raise (it would null the whole extract via the escalation gate).
    # the control char is dropped (as load_html does for string input), joining the two words
    ctrl_tree = html.fromstring("<html><body><p>before\x01after visible text</p></body></html>")
    assert html2txt(ctrl_tree) == "beforeafter visible text"
