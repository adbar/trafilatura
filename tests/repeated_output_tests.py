"""Synthetic pages where every word is unique, so any word repeated in the output is a duplicate."""

import itertools
import re
from collections import Counter

import pytest

from trafilatura import extract

# each @ becomes a unique word
INLINE = {
    "a": '<a href="/x">@ @</a>',
    "b": "<b>@ @</b>",
    "br": "<br/>",
    "code": "<code>@</code>",
    "em": "<em>@ @</em>",
    "img": '<img src="/x.png" alt="@ @"/>',
    "span": "<span>@ @</span>",
    "sup": "<sup>@</sup>",
    "a_code": '<a href="/x"><code>@</code></a>',
    "b_code": "<b><code>@</code></b>",
}
# {} is replaced by a run of text with inline elements
BLOCKS = {
    "p": "<p>{}</p>",
    "div": "<div>{}</div>",
    "span_p": '<span data-as="p">{}</span>',
    "span_p_holds_p": '<span data-as="p">{}<p>{}</p></span>@ @ @',
    "span_p_then_p": '<span data-as="p">{}</span><p>{}</p>@ @ @',
    "li": "<ul><li>{}</li><li>{}</li></ul>@ @ @",
    "nested_li": "<ul><li>{}<ul><li>{}</li><li>@ @ @</li></ul></li></ul>",
    "p_in_li": "<ul><li><p>{}</p></li><li>@ @</li></ul>@ @ @",
    "table_in_li": "<ul><li>@ @<table><tr><td>{}</td></tr></table></li></ul>@ @ @",
    "blockquote_in_li": "<ul><li><blockquote><p>{}</p></blockquote>@ @ @</li><li>@ @</li></ul>@ @ @",
    "ol": "<ol><li>{}</li><li>@ @ @</li></ol>@ @ @",
    "table": "<table><tr><th>@</th><th>@</th></tr><tr><td>{}</td><td>@ @</td></tr></table>@ @ @",
    "table_in_td": "<table><tr><td><table><tr><td>{}</td><td>@ @</td></tr></table>@ @ @</td><td>@ @</td></tr></table>@ @ @",
    "caption": "<table><caption><p>{}</p></caption><tr><td>@ @</td><td>@ @</td></tr></table>@ @ @",
    "blockquote": "<blockquote><p>{}</p></blockquote>@ @ @",
    "pre": "<p>{}</p><pre>@ @ @</pre>@ @ @",
    "figure": '<figure><img src="/f.png" alt="@ @"/><figcaption>{}</figcaption></figure>@ @ @',
    "figure_then_p": '<figure><img src="/f.png" alt="@ @"/><figcaption>{}</figcaption></figure>@ @ @<p>{}</p>',
    "hidden": "<p>{}</p><div style='display:none'>" + "@ " * 60 + "</div>",
    "h2": "<h2>@ @ {}</h2>@ @ @",
}
WRAPPERS = {
    "bare": "{}",
    "nested": '<div class="page"><div class="col"><main><div class="content">{}</div></main></div></div>',
    "article": "<main id='content'><article>{}</article><p>@ @ @</p></main>",
}
CONFIGS = {
    "markdown": {"output_format": "markdown", "include_formatting": True, "include_links": True, "include_images": True},
    "recall": {"favor_recall": True},
    "precision": {"favor_precision": True},
}
FILLER = ("<p>" + "@ " * 25 + "</p>") * 3
# precision drops these short pages entirely, which would make the test pass vacuously
EMPTY = {
    ("span_p", "a", True, "nested", "precision"),
    ("li", "a", True, "nested", "precision"),
    ("nested_li", "a", True, "bare", "precision"),
    ("nested_li", "a", True, "nested", "precision"),
}
KNOWN_DUPLICATES = {
    **{
        (block, inline, True, "nested", "recall"): "recovery container re-emits consumed fragments"
        for block in ("span_p_holds_p", "span_p_then_p")
        for inline in ("br", "code", "b_code")
    },
    ("blockquote", "a_code", True, "article", "precision"): "dropped blockquote, its tail emitted twice",
}


class RepeatedWordsError(AssertionError):
    "Only raised for repeated words, so a known duplicate cannot fail for another reason."


def _assert_unique(result):
    words = re.findall(r"w\d+x", result)
    repeated = [w for w, c in Counter(words).items() if c > 1]
    if repeated:
        raise RepeatedWordsError(repeated[:5])
    return words


def _number(body):
    ids = itertools.count()
    return re.sub("@", lambda _: f"w{next(ids)}x", f"<html><body>{body}</body></html>")


def _page(block, inline, wrapper, short):
    run = f"@ @ @ @ {INLINE[inline]} @ @ @ {INLINE[inline]} @ @ @ @."
    body = BLOCKS[block].replace("{}", run)
    if not short:
        body = FILLER + body + FILLER
    return _number(WRAPPERS[wrapper].replace("{}", body))


@pytest.mark.parametrize(
    "block,inline,short,wrapper,config", list(itertools.product(BLOCKS, INLINE, (False, True), WRAPPERS, CONFIGS))
)
def test_no_repeated_words(block, inline, short, wrapper, config, request):
    key = (block, inline, short, wrapper, config)
    if reason := KNOWN_DUPLICATES.get(key):
        request.applymarker(pytest.mark.xfail(strict=True, raises=RepeatedWordsError, reason=reason))
    result = extract(_page(block, inline, wrapper, short), **CONFIGS[config])
    if key in EMPTY:
        assert result is None
    else:
        assert result
        _assert_unique(result)


@pytest.mark.parametrize("fast", [False, True])
@pytest.mark.parametrize(
    "run,expected",
    [
        (
            "Mira builds <b><code>sampleAlpha</code></b> inside <b><code>sampleBeta</code></b> today.",
            "Mira builds **`sampleAlpha`** inside **`sampleBeta`** today.",
        ),
        (
            "Useful <a href='/guide'><code>guideMarker</code></a> inside prose remains linked.",
            "Useful [`guideMarker`](/guide) inside prose remains linked.",
        ),
        (
            "Mira builds <b><code>sampleAlpha</code></b> inside <b><code>sampleAlpha</code></b> today.",
            "Mira builds **`sampleAlpha`** inside **`sampleAlpha`** today.",
        ),
    ],
    ids=["bold-code", "linked-code", "genuine-repeat"],
)
def test_recovered_inline_content_kept_once(run, expected, fast):
    "Recovery keeps formatting, missing outside text and distinct source occurrences."
    page = (
        f"<html><body><main id='content'><article><div>{run}</div></article><p>Outside marker stays.</p></main></body></html>"
    )
    assert extract(page, fast=fast, **CONFIGS["markdown"]) == expected + "\n\nOutside marker stays."


@pytest.mark.parametrize("config", ["markdown", "precision"])
@pytest.mark.parametrize("wrapper", ["nested", "article"])
@pytest.mark.parametrize("block", ["p_in_li", "blockquote_in_li", "table_in_li"])
def test_over_pruned_page_not_repeated(block, wrapper, config):
    "A sidebar holding most of the text trips the over-pruning guard, recovery still skips consumed elements."
    tokens = (f"s{n}x" for n in itertools.count())
    sidebar = (
        "<div class='sidebar'>" + "".join(f"<p>{' '.join(next(tokens) for _ in range(40))}</p>" for _ in range(12)) + "</div>"
    )
    page = _page(block, "br", wrapper, True).replace("</body>", sidebar + "</body>")
    result = extract(page, **CONFIGS[config])
    assert result
    assert _assert_unique(result)


@pytest.mark.parametrize("frame", ["article", "main"])
@pytest.mark.parametrize("inline", ["a", "b", "code", "em"])
def test_inline_only_frame_kept(frame, inline):
    "A non-div frame holding a single formatted text run must not lose it to a sidebar."
    run = f"{INLINE[inline]} @ @ @ {INLINE[inline]} @ @ @ @. " * 3
    result = extract(_number(f"<{frame}>{run}</{frame}><div>{FILLER}</div>"), **CONFIGS["markdown"])
    assert result
    assert "w0x" in result


@pytest.mark.parametrize("config", CONFIGS)
@pytest.mark.parametrize("child", ["<br/>", "<p>@ @ @ @ @ @ @ @ @ @.</p>"])
def test_frame_lead_text_kept(config, child):
    "The frame's own text before its first child is part of the content (Blogger post bodies)."
    sentence = "@ @ @ @ @ @ @ @ @ @. " * 3
    body = f'<div class="post-body entry-content">{sentence}{child}{FILLER}</div>'
    result = extract(_number(body), **CONFIGS[config])
    assert result
    assert _assert_unique(result)[0] == "w0x"


@pytest.mark.parametrize("config", [{}, {"fast": True}, {"favor_recall": True}, {"favor_precision": True}])
@pytest.mark.parametrize("tag,cls", [("ol", "commentlist"), ("ul", "comment-list")])
def test_short_article_comment_list_not_repeated(tag, cls, config, request):
    "Replies of a captured comment list appear once, even when the article is too short."
    if "favor_precision" not in config:
        request.applymarker(
            pytest.mark.xfail(strict=True, raises=RepeatedWordsError, reason="the replies also land in the body")
        )
    replies = "".join("<li><p>" + "@ " * 25 + "</p></li>" for _ in range(8))
    body = f"<article><p>@ @ @ @ @ @ @ @ @ @.</p></article><{tag} class='{cls}'>{replies}</{tag}>"
    result = extract(_number(body), **config)
    assert result
    assert len(_assert_unique(result)) == body.count("@")
