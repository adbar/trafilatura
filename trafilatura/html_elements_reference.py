"""
Frozen list of HTML elements (snapshot 2025-06-08)
=================================================

The set is taken verbatim from the MDN HTML-elements reference page:
https://developer.mozilla.org/en-US/docs/Web/HTML/Element

Keeping it in-tree removes any run-time network dependency and gives
the test-suite a stable target.
"""

from typing import Set

MDN_ELEMENTS: Set[str] = {
    # ——— Document root ———
    "html",

    # ——— Document metadata ———
    "base", "head", "link", "meta", "style", "title",

    # ——— Sectioning root ———
    "body",

    # ——— Content sectioning ———
    "address", "article", "aside", "footer", "header", "h1", "h2", "h3", "h4",
    "h5", "h6", "hgroup", "main", "nav", "section", "search",

    # ——— Text content ———
    "blockquote", "dd", "div", "dl", "dt", "figcaption", "figure", "hr", "li",
    "menu", "ol", "p", "pre", "ul",

    # ——— Inline text semantics ———
    "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "dfn", "em",
    "i", "kbd", "mark", "q", "rp", "rt", "ruby", "s", "samp", "small", "span",
    "strong", "sub", "sup", "time", "u", "var", "wbr",

    # ——— Image & multimedia ———
    "area", "audio", "img", "map", "track", "video",

    # ——— Embedded content ———
    "embed", "fencedframe", "iframe", "object", "picture", "source",

    # ——— SVG and MathML ———
    "svg", "math",

    # ——— Scripting ———
    "canvas", "noscript", "script",

    # ——— Demarcating edits ———
    "del", "ins",

    # ——— Table content ———
    "caption", "col", "colgroup", "table", "tbody", "td", "tfoot",
    "th", "thead", "tr",

    # ——— Forms ———
    "button", "datalist", "fieldset", "form", "input", "label", "legend",
    "meter", "optgroup", "option", "output", "progress", "select",
    "selectedcontent", "textarea",

    # ——— Interactive elements ———
    "details", "dialog", "summary",

    # ——— Web Components ———
    "slot", "template",

    # ——— Obsolete/deprecated (included for completeness) ———
    "acronym", "big", "center", "content", "dir", "font", "frame", "frameset",
    "image", "marquee", "menuitem", "nobr", "noembed", "noframes", "param",
    "plaintext", "rb", "rtc", "shadow", "strike", "tt", "xmp",
}
