"""
Element tree API over turbohtml, shaped after the lxml subset trafilatura uses.

turbohtml parses to a WHATWG DOM, where text lives in text nodes. The extraction code
is written against the ElementTree model (``.text`` and ``.tail`` strings, elements
that carry their tail when moved), so this module maps one onto the other: ``.text``
is the run of text nodes before the first child element, ``.tail`` the run after the
element, and a detached element sits in an empty holder element so its tail has
somewhere to live.
"""

import functools
import re
import weakref
from collections.abc import Callable, Iterable, Iterator, MutableMapping
from contextvars import ContextVar
from copy import deepcopy as _deepcopy
from typing import Any, Literal, ParamSpec, TypeVar, overload

import turbohtml
from lxml import etree as _etree
from lxml import html as _lxml_html
from lxml.html import defs as _lxml_defs
from turbohtml import Axis, Document, Text
from turbohtml import Element as _Node
from turbohtml import Html as _Html

_XML_SERIALIZATION = _Html(xml=True)

_HOLDER = "trafilatura-holder"

_P = ParamSpec("_P")
_R = TypeVar("_R")


_ORIGINS: ContextVar[dict[_Node, Any] | None] = ContextVar("_ORIGINS", default=None)


def document_context(func: Callable[_P, _R]) -> Callable[_P, _R]:
    "Keep detached elements associated with their documents during extraction, as lxml does."

    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        if _ORIGINS.get() is not None:
            return func(*args, **kwargs)
        token = _ORIGINS.set({})
        try:
            return func(*args, **kwargs)
        finally:
            _ORIGINS.reset(token)

    return wrapper


_INVALID_NAME = re.compile(r"[^\w.:-]|^[^A-Za-z_]")


def _new_node(tag: str, attrs: dict[str, str] | None = None) -> _Node:
    try:
        return _create(tag, attrs)
    except ValueError:
        # libxml2 keeps tag names turbohtml refuses, e.g. 'ahref="https:' from a missing space
        return _create(_INVALID_NAME.sub("_", tag), attrs)


def _create(tag: str, attrs: dict[str, str] | None) -> _Node:
    node = _Node(tag)
    if attrs:
        _set_attributes(node, attrs)
    return node


def _set_attributes(node: Any, attrs: dict[str, Any]) -> None:
    for key, value in attrs.items():
        try:
            node.set(key, value) if hasattr(node, "set") else node.attrs.__setitem__(key, value)
        except ValueError:  # noqa: PERF203 - Invalid names must not discard later attributes.
            continue


# one wrapper per node, so identity checks (``is``) behave as with lxml proxies
_REGISTRY: dict[_Node, weakref.ref["HtmlElement"]] = {}


def _wrap(node: _Node) -> "HtmlElement":
    ref = _REGISTRY.get(node)
    if ref is not None and (elem := ref()) is not None:
        return elem
    elem = object.__new__(HtmlElement)
    elem.node = node

    def forget(ref: weakref.ref["HtmlElement"]) -> None:
        if _REGISTRY.get(node) is ref:
            del _REGISTRY[node]

    _REGISTRY[node] = weakref.ref(elem, forget)
    return elem


def _tag_filter(tag: Any, tags: tuple[Any, ...]) -> str | list[Any] | Literal[True]:
    "Normalize lxml's tag arguments (strings, iterables of strings, None or '*') to a turbohtml filter."
    names: list[Any] = []
    for item in (tag, *tags):
        if item is None:
            continue
        if isinstance(item, str):
            if item == "*":
                return True
            names.append(item)
        else:
            for name in item:
                if name == "*":
                    return True
                names.append(name)
    return names[0] if len(names) == 1 else names or True


def _matches(node: _Node, flt: str | list[Any] | Literal[True]) -> bool:
    return flt is True or (node.tag == flt if isinstance(flt, str) else node.tag in flt)


def _next_element(node: Any) -> _Node | None:
    sibling = node.next_sibling
    while sibling is not None and type(sibling) is not _Node:
        sibling = sibling.next_sibling
    return sibling


def _previous_element(node: Any) -> _Node | None:
    sibling = node.previous_sibling
    while sibling is not None and type(sibling) is not _Node:
        sibling = sibling.previous_sibling
    return sibling


def _element_children(node: _Node) -> list[_Node]:
    children = []
    child = node[0] if len(node) else None
    while child is not None:
        if type(child) is _Node:
            children.append(child)
        child = child.next_sibling
    return children


def _tail_nodes(node: _Node) -> list[Text]:
    nodes = []
    sibling = node.next_sibling
    while type(sibling) is Text:
        nodes.append(sibling)
        sibling = sibling.next_sibling
    return nodes


def _top(node: Any) -> Any:
    "The topmost ancestor, stopping below a holder."
    parent = node.parent
    while parent is not None and not (type(parent) is _Node and parent.tag == _HOLDER):
        node, parent = parent, parent.parent
    return node


def _remember_origin(node: _Node) -> None:
    "lxml keeps a removed element in its document, where absolute paths still search."
    if (origins := _ORIGINS.get()) is not None:
        top = _top(node)
        origins[node] = origins.get(top, top)


def _detach(node: _Node, with_tail: bool = True, keep_origin: bool = True) -> None:
    "Move the node (and its tail) into a holder of its own, as lxml keeps a removed element's tail."
    if keep_origin:
        _remember_origin(node)
    tail = _tail_nodes(node) if with_tail else []
    holder = _holder(node)
    holder.append(node)
    for text in tail:
        holder.append(text)
    holder.extract()


def _holder(node: _Node) -> _Node:
    holder = _Node(_HOLDER)
    if node.parent is not None and type(node.parent) is not Document:
        node.insert_before(holder)
    return holder


class _Attrib(MutableMapping[str, str]):
    "Attribute mapping with lxml's string values (turbohtml splits class, rel and the like into lists)."

    __slots__ = ("node",)

    def __init__(self, node: _Node) -> None:
        self.node = node

    def __getitem__(self, key: str) -> str:
        value = self.node.attr(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        self.node.attrs[key] = value

    def __delitem__(self, key: str) -> None:
        del self.node.attrs[key]

    def __iter__(self) -> Iterator[str]:
        return iter(list(self.node.attrs))

    def __len__(self) -> int:
        return len(self.node.attrs)

    def __contains__(self, key: object) -> bool:
        return key in self.node.attrs

    def get(self, key: str, default: Any = None) -> Any:
        value = self.node.attr(key)
        return default if value is None else value

    def clear(self) -> None:
        self.node.attrs.clear()


# a location path that starts at the root: at the start, or after "|" or "("
_ABSOLUTE_PATH = re.compile(r"(^|[|(])(\s*)//")


class _Expression:
    """A compiled expression. Absolute paths (//x) need a document at the top of the
    tree; on a copied or newly built tree the top element stands in for it, as the
    root of lxml's per-copy document does."""

    __slots__ = ("_absolute", "_compiled", "_relative")

    def __init__(self, path: str) -> None:
        self._compiled = turbohtml.XPath(path)
        rewritten = _ABSOLUTE_PATH.sub(r"\1\2descendant-or-self::node()/", path)
        self._absolute = rewritten != path
        self._relative = turbohtml.XPath(rewritten) if self._absolute else None

    def __call__(self, node: _Node, **variables: Any) -> Any:
        if self._absolute:
            top = _top(node)
            if (origins := _ORIGINS.get()) is not None:
                top = origins.get(top, top)
            if type(top) is Document:
                return self._compiled(top, **variables)
            return self._relative(top, **variables)  # type: ignore[misc]
        return self._compiled(node, **variables)


def _elements(result: Any) -> list[_Node]:
    "The elements of an XPath node-set result."
    return [item for item in result if type(item) is _Node] if isinstance(result, list) else []


_XPATH_CACHE: dict[str, _Expression] = {}


def _compiled(path: str) -> _Expression:
    compiled = _XPATH_CACHE.get(path)
    if compiled is None:
        compiled = _XPATH_CACHE[path] = _Expression(path)
    return compiled


def _wrap_result(result: Any) -> Any:
    if isinstance(result, list):
        return [_wrap(item) if type(item) is _Node else item for item in result]
    return result


class _RootTree:
    __slots__ = ("_root",)

    def __init__(self, root: "HtmlElement") -> None:
        self._root = root

    def getroot(self) -> "HtmlElement":
        return self._root


class HtmlElement:
    "An element of a turbohtml tree behind the lxml element API."

    __slots__ = ("__weakref__", "node")

    node: _Node

    def __repr__(self) -> str:
        return f"<Element {self.tag} at 0x{id(self):x}>"

    def __bool__(self) -> bool:
        return len(self) != 0

    def __len__(self) -> int:
        node = self.node
        count = 0
        child = node[0] if len(node) else None
        while child is not None:
            if type(child) is _Node:
                count += 1
            child = child.next_sibling
        return count

    def __iter__(self) -> Iterator["HtmlElement"]:
        child = self.node[0] if len(self.node) else None
        while child is not None and type(child) is not _Node:
            child = child.next_sibling
        while child is not None:
            following = _next_element(child)
            yield _wrap(child)
            child = following

    def __getitem__(self, index: int | slice) -> Any:
        children = _element_children(self.node)
        if isinstance(index, slice):
            return [_wrap(child) for child in children[index]]
        return _wrap(children[index])

    def __copy__(self) -> "HtmlElement":
        return self.__deepcopy__({})

    def __deepcopy__(self, memo: dict[int, Any]) -> "HtmlElement":
        clone = _deepcopy(self.node)
        if (tail := self.tail) is not None:
            holder = _Node(_HOLDER)
            holder.append(clone)
            holder.append(Text(tail))
        return _wrap(clone)

    @property
    def tag(self) -> str:
        return self.node.tag

    @tag.setter
    def tag(self, value: str) -> None:
        self.node.tag = value

    @property
    def attrib(self) -> _Attrib:
        return _Attrib(self.node)

    def get(self, key: str, default: Any = None) -> Any:
        value = self.node.attr(key)
        return default if value is None else value

    def set(self, key: str, value: str) -> None:
        self.node.attrs[key] = value

    def keys(self) -> list[str]:
        return list(self.node.attrs)

    def items(self) -> list[tuple[str, str]]:
        node = self.node
        return [(key, node.attr(key)) for key in node.attrs]  # type: ignore[misc]

    def values(self) -> list[str]:
        node = self.node
        return [node.attr(key) for key in node.attrs]  # type: ignore[misc]

    @property
    def text(self) -> str | None:
        node = self.node
        if not len(node):
            return None
        child: Any = node[0]
        if type(child) is not Text:
            return None
        parts = []
        while type(child) is Text:
            parts.append(child.data)
            child = child.next_sibling
        return "".join(parts)

    @text.setter
    def text(self, value: str | None) -> None:
        node = self.node
        child = node[0] if len(node) else None
        while type(child) is Text:
            following = child.next_sibling
            child.extract()
            child = following
        if value is not None:
            node.insert(0, Text(value))

    @property
    def tail(self) -> str | None:
        sibling = self.node.next_sibling
        if type(sibling) is not Text:
            return None
        parts = []
        while type(sibling) is Text:
            parts.append(sibling.data)
            sibling = sibling.next_sibling
        return "".join(parts)

    @tail.setter
    def tail(self, value: str | None) -> None:
        node = self.node
        for text in _tail_nodes(node):
            text.extract()
        if value is not None:
            parent = node.parent
            if parent is None:
                _detach(node)
            elif type(parent) is Document:
                return
            node.insert_after(Text(value))

    def text_content(self) -> str:
        return self.node.text

    def getparent(self) -> "HtmlElement | None":
        parent = self.node.parent
        return _wrap(parent) if type(parent) is _Node and parent.tag != _HOLDER else None

    def getnext(self) -> "HtmlElement | None":
        sibling = _next_element(self.node)
        return _wrap(sibling) if sibling is not None else None

    def getprevious(self) -> "HtmlElement | None":
        sibling = _previous_element(self.node)
        return _wrap(sibling) if sibling is not None else None

    def getchildren(self) -> list["HtmlElement"]:
        return list(self)

    def getroottree(self) -> _RootTree:
        top = _top(self.node)
        if (origins := _ORIGINS.get()) is not None:
            top = origins.get(top, top)
        if type(top) is Document:
            top = top.root
        return _RootTree(_wrap(top))

    def index(self, child: "HtmlElement") -> int:
        return _element_children(self.node).index(child.node)

    def iter(self, tag: Any = None, *tags: Any) -> Iterator["HtmlElement"]:
        tag_filter = _tag_filter(tag, tags)
        return (_wrap(node) for node in self.node.iter_elements(None if tag_filter is True else tag_filter, include_self=True))

    def iterdescendants(self, tag: Any = None, *tags: Any) -> Iterator["HtmlElement"]:
        tag_filter = _tag_filter(tag, tags)
        return (_wrap(node) for node in self.node.iter_elements(None if tag_filter is True else tag_filter))

    def iterchildren(self, tag: Any = None, *tags: Any, reversed: bool = False) -> Iterator["HtmlElement"]:  # noqa: A002
        flt = _tag_filter(tag, tags)
        children = [_wrap(child) for child in _element_children(self.node) if _matches(child, flt)]
        yield from children[::-1] if reversed else children

    def itersiblings(self, tag: Any = None, *tags: Any, preceding: bool = False) -> Iterator["HtmlElement"]:
        flt = _tag_filter(tag, tags)
        step = _previous_element if preceding else _next_element
        sibling = step(self.node)
        while sibling is not None:
            following = step(sibling)
            following_elem = _wrap(following) if following is not None else None
            if _matches(sibling, flt):
                yield _wrap(sibling)
            sibling = following_elem.node if following_elem is not None else None

    def iterancestors(self, tag: Any = None, *tags: Any) -> Iterator["HtmlElement"]:
        flt = _tag_filter(tag, tags)
        parent = self.node.parent
        while type(parent) is _Node and parent.tag != _HOLDER:
            if _matches(parent, flt):
                yield _wrap(parent)
            parent = parent.parent

    def itertext(self, tag: Any = None, *tags: Any, with_tail: bool = True) -> Iterator[str]:
        """Text pieces as lxml yields them: an element's text, then its children's content and
        tails, each run of adjacent text nodes being one piece."""
        flt = None if tag is None and not tags else _tag_filter(tag, tags)
        frames: list[list[Any]] = [[self.node.children, 0, self.node, None]]
        while frames:
            frame = frames[-1]
            children, position, owner, previous = frame
            run = []
            while position < len(children) and type(children[position]) is Text:
                run.append(children[position].data)
                position += 1
            if run:
                if previous is None:
                    if flt is None or _matches(owner, flt):
                        yield "".join(run)
                elif with_tail and (flt is None or type(previous) is not _Node or _matches(previous, flt)):
                    yield "".join(run)
            if position >= len(children):
                frames.pop()
                continue
            child = children[position]
            frame[1], frame[3] = position + 1, child
            if type(child) is _Node:
                frames.append([child.children, 0, child, None])

    def xpath(self, path: str, **variables: Any) -> Any:
        return _wrap_result(_compiled(path)(self.node, **variables))

    def find(self, path: str) -> "HtmlElement | None":
        elements = _elements(_compiled(path)(self.node))
        return _wrap(elements[0]) if elements else None

    def findall(self, path: str) -> list["HtmlElement"]:
        return [_wrap(item) for item in _elements(_compiled(path)(self.node))]

    def iterfind(self, path: str) -> Iterator["HtmlElement"]:
        return iter(self.findall(path))

    def append(self, child: "HtmlElement") -> None:
        node = child.node
        tail = _tail_nodes(node)
        self.node.append(node)
        if tail:
            node.insert_after(*tail)

    def extend(self, children: Iterable["HtmlElement"]) -> None:
        for child in list(children):
            self.append(child)

    def insert(self, index: int, child: "HtmlElement") -> None:
        children = _element_children(self.node)
        if index < 0:
            index = max(len(children) + index, 0)
        if index >= len(children):
            self.append(child)
            return
        node = child.node
        tail = _tail_nodes(node)
        children[index].insert_before(node, *tail)

    def remove(self, child: "HtmlElement") -> None:
        node = child.node
        if node.parent != self.node:
            raise ValueError("Element is not a child of this node.")
        _detach(node)

    def clear(self, keep_tail: bool = False) -> None:
        node = self.node
        node.attrs.clear()
        if not keep_tail:
            for text in _tail_nodes(node):
                text.extract()
        node.clear()

    def replace(self, old: "HtmlElement", new: "HtmlElement") -> None:
        old_node, new_node = old.node, new.node
        if old_node.parent != self.node:
            raise ValueError("Element is not a child of this node.")
        new_tail = _tail_nodes(new_node)
        old_node.insert_before(new_node, *new_tail)
        _detach(old_node)

    def addnext(self, elem: "HtmlElement") -> None:
        node = self.node
        if type(node.parent) is Document:
            return
        own_tail = _tail_nodes(node)
        anchor: Any = own_tail[-1] if own_tail else node
        moved = elem.node
        tail = _tail_nodes(moved)
        anchor.insert_after(moved, *tail)

    def addprevious(self, elem: "HtmlElement") -> None:
        moved = elem.node
        tail = _tail_nodes(moved)
        self.node.insert_before(moved, *tail)

    def drop_tree(self) -> None:
        node = self.node
        tail = self.tail
        _remember_origin(node)
        holder = _holder(node)
        holder.append(node)
        if tail is not None:
            holder.append(Text(tail))
        holder.extract()

    def drop_tag(self) -> None:
        self.node.unwrap()

    def makeelement(self, tag: str, attrib: dict[str, str] | None = None) -> "HtmlElement":
        return Element(tag, attrib)


_Element = HtmlElement


def Element(tag: str, attrib: dict[str, str] | None = None, **extra: str) -> HtmlElement:  # noqa: N802
    attrs = dict(attrib) if attrib else {}
    attrs.update(extra)
    return _wrap(_new_node(tag, attrs))


def SubElement(parent: HtmlElement, tag: str, attrib: dict[str, str] | None = None, **extra: str) -> HtmlElement:  # noqa: N802
    attrs = dict(attrib) if attrib else {}
    attrs.update(extra)
    node = _new_node(tag, attrs)
    parent.node.append(node)
    return _wrap(node)


class XPath:
    "A compiled XPath expression returning wrapped elements, like lxml.etree.XPath."

    __slots__ = ("_compiled", "path")

    def __init__(self, path: str) -> None:
        self.path = path
        self._compiled = _compiled(path)

    def __call__(self, elem: HtmlElement, **variables: Any) -> Any:
        return _wrap_result(self._compiled(elem.node, **variables))

    def __str__(self) -> str:
        return self.path


def strip_tags(tree: HtmlElement, *tags: Any) -> None:
    "Remove the matching descendants but keep their text and children."
    if not any(tags):
        return
    flt = _tag_filter(None, tags)
    top = tree.node
    for node in list(top.find_all(flt, axis=Axis.DESCENDANTS)):
        node.unwrap()


def strip_elements(tree: HtmlElement, *tags: Any, with_tail: bool = True) -> None:
    "Remove the matching descendants with their content (and tail)."
    if not any(tags):
        return
    flt = _tag_filter(None, tags)
    top = tree.node
    for node in list(top.find_all(flt, axis=Axis.DESCENDANTS)):
        parent = node.parent
        while parent is not None and parent != top:
            parent = parent.parent
        if parent is None:
            continue
        if with_tail:
            for text in _tail_nodes(node):
                text.extract()
        node.extract()


@overload
def tostring(
    elem: "HtmlElement", encoding: type[str] | Literal["unicode"], method: str = "xml", with_tail: bool = True
) -> str: ...
@overload
def tostring(
    elem: "HtmlElement", encoding: Literal["ascii", "utf-8"] | None = None, method: str = "xml", with_tail: bool = True
) -> bytes: ...
def tostring(
    elem: "HtmlElement",
    encoding: type[str] | str | None = None,
    method: str = "xml",
    with_tail: bool = True,
) -> str | bytes:
    "Serialize like lxml.etree.tostring: XML, or plain text with method='text'."
    node = elem.node
    output = node.text if method == "text" else node.serialize(_XML_SERIALIZATION)
    if with_tail and (tail := elem.tail):
        output += tail
    if encoding is str or encoding == "unicode":
        return output
    return output.encode(encoding or "ascii", "xmlcharrefreplace")  # type: ignore[arg-type]


def _strip_comments(root: Any) -> None:
    for node in root.xpath(".//comment()|.//processing-instruction()"):
        node.extract()


def document_fromstring(markup: str | bytes) -> HtmlElement | None:
    """Parse a whole page and return its root element, without comments and processing
    instructions. The HTML parser always creates head and body; empty ones are dropped,
    so a tree only holds the sections the page has."""
    root = _parse_document(markup)
    for section in _element_children(root):
        if section.tag in ("head", "body") and not len(section) and not len(section.attrs):
            section.extract()
    return _wrap(root)


_FULL_HTML = re.compile(r"^\s*<(?:html|!doctype)", re.IGNORECASE)


def fromstring(markup: str | bytes) -> HtmlElement:
    """Parse a document or a snippet, like lxml.html.fromstring: a full page gives its
    root, a single element that element, anything else a div or span around it."""
    text = markup.decode("utf-8", "replace") if isinstance(markup, bytes) else markup
    if _FULL_HTML.match(text):
        return document_fromstring(text)  # type: ignore[return-value]
    root = _wrap(_parse_document(text))
    body = root.find("body")
    if body is None or ((head := root.find("head")) is not None and len(head)):
        return root
    if len(body) == 1 and not (body.text or "").strip() and not (body[-1].tail or "").strip():
        return body[0]  # type: ignore[no-any-return]
    body.tag = "div" if any(elem.tag in _lxml_defs.block_tags for elem in body.iter()) else "span"
    return body


_HEAD_TAG = re.compile(r"<head[\s/>]", re.IGNORECASE)
_BODY_TAG = re.compile(r"<body[\s/>]", re.IGNORECASE)
_HEAD_ONLY = "self::meta or self::link or self::title or self::base"


def _parse_document(markup: str | bytes) -> _Node:
    document = turbohtml.parse(markup)
    _strip_comments(document)
    root: _Node = document.root  # type: ignore[assignment]
    _restore_head(root, markup if isinstance(markup, str) else markup.decode("utf-8", "replace"))
    # a stray </p> makes the HTML parser create an empty paragraph, which carries nothing
    # and shifts the sibling-based heuristics
    for paragraph in _elements(root.xpath(".//p[not(node())][not(@*)]")):
        if paragraph.position is None:
            paragraph.extract()
    root.normalize()
    return root


def _restore_head(root: _Node, markup: str) -> None:
    """Put back into head what the page wrote between <head> and <body>. A body-only element
    there (a stray <li>, an <img> in <noscript>) makes the HTML parser start the body early,
    and everything after it lands in the body: out of reach of the head-scoped metadata
    queries, and in front of the content."""
    head = root.find("head", axis=Axis.CHILDREN)
    body = root.find("body", axis=Axis.CHILDREN)
    head_match, body_match = _HEAD_TAG.search(markup), _BODY_TAG.search(markup)
    if head is None or body is None or head_match is None or body_match is None:
        return
    start_offset, end_offset = head_match.start(), body_match.start()
    start = markup.count("\n", 0, start_offset) + 1, start_offset - markup.rfind("\n", 0, start_offset) - 1
    end = markup.count("\n", 0, end_offset) + 1, end_offset - markup.rfind("\n", 0, end_offset) - 1
    moved = [
        child
        for child in _element_children(body)
        if (position := child.position) is not None
        and start < position < end
        # an unclosed element before <body> swallows the page: leave it
        and all(elem.position is None or elem.position < end for elem in _elements(child.xpath(".//*")))
    ]
    moved.extend(
        elem
        for elem in _elements(body.xpath(f".//*[{_HEAD_ONLY}]"))
        if (position := elem.position) is not None and start < position < end
    )
    for elem in moved:
        head.append(elem)


def fragment_fromstring(markup: str, create_parent: str | bool = False) -> HtmlElement:
    "Parse a fragment, like lxml.html.fragment_fromstring."
    container = turbohtml.parse_fragment(markup, positions=False)
    _strip_comments(container)
    container.normalize()
    if create_parent:
        parent = _wrap(container)
        parent.tag = create_parent if isinstance(create_parent, str) else "div"
        return parent
    children = _element_children(container)
    if len(children) != 1:
        raise ValueError(f"Multiple elements found ({len(children)})" if children else "No elements found")
    node = children[0]
    # a parsed fragment is a tree of its own, as lxml's is
    _detach(node, keep_origin=False)
    return _wrap(node)


def from_lxml(tree: _etree._Element) -> HtmlElement:
    "Copy an lxml tree into turbohtml, dropping comments and processing instructions like the HTML parser does."
    root = _create(tree.tag, {str(key): str(value) for key, value in tree.attrib.items()})  # type: ignore[arg-type]
    stack = [(tree, root)]
    while stack:
        source, target = stack.pop()
        if source.text:
            target.append(Text(source.text))
        for child in source:
            if isinstance(child.tag, str):
                copied = _new_node(child.tag, {str(key): str(value) for key, value in child.attrib.items()})
                target.append(copied)
                stack.append((child, copied))
            if child.tail:
                target.append(Text(child.tail))
    root.normalize()
    return _wrap(root)


def to_lxml(elem: Any) -> Any:
    "Copy a tree into lxml.etree elements; lxml elements pass through."
    if not isinstance(elem, HtmlElement):
        return elem
    return _copy_to_lxml(elem.node, _etree.Element)


def to_lxml_html(elem: HtmlElement) -> _lxml_html.HtmlElement:
    "Copy a tree into lxml.html elements, for libraries that expect them (htmldate, justext)."
    return _copy_to_lxml(elem.node, _lxml_html.html_parser.makeelement)  # type: ignore[no-any-return]


def _copy_to_lxml(node: _Node, factory: Callable[..., Any]) -> Any:
    target = _lxml_element(factory, node)
    stack = [(node, target)]
    while stack:
        source, parent = stack.pop()
        last = None
        texts: list[str] = []
        for child in source.children:
            if type(child) is Text:
                texts.append(child.data)
                continue
            if type(child) is not _Node:
                continue
            if texts:
                if last is None:
                    parent.text = "".join(texts)
                else:
                    last.tail = "".join(texts)
                texts = []
            copied = _lxml_element(parent.makeelement, child)
            parent.append(copied)
            stack.append((child, copied))
            last = copied
        if texts:
            if last is None:
                parent.text = "".join(texts)
            else:
                last.tail = "".join(texts)
    return target


_LXML_NAME_INVALID = re.compile(r"[^\w.-]|^[^A-Za-z_]")


def _lxml_element(factory: Callable[..., Any], node: _Node) -> Any:
    "An lxml element for the node; lxml refuses some names the HTML parser accepts, e.g. 'g:plusone'."
    attrs = {key: node.attr(key) for key in node.attrs}
    try:
        return factory(node.tag, attrs)
    except ValueError:
        elem = factory(_LXML_NAME_INVALID.sub("_", node.tag))
        _set_attributes(elem, attrs)
        return elem


__all__ = [
    "Element",
    "HtmlElement",
    "SubElement",
    "XPath",
    "_Element",
    "document_context",
    "document_fromstring",
    "fragment_fromstring",
    "from_lxml",
    "fromstring",
    "strip_elements",
    "strip_tags",
    "to_lxml",
    "to_lxml_html",
    "tostring",
]
