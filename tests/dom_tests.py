from types import ModuleType

import pytest
from lxml import html

from trafilatura import dom


@pytest.mark.parametrize("backend", [dom, html], ids=["turbohtml", "lxml"])
def test_remove_preserves_detached_tail_and_descendant_identity(backend: ModuleType) -> None:
    root = backend.fromstring("<div><p>A<b>B</b></p>tail<em>C</em></div>")
    removed = root[0]
    descendant = removed[0]

    root.remove(removed)

    assert (removed.tail, root.text_content(), removed[0] is descendant) == ("tail", "C", True)


@pytest.mark.parametrize("backend", [dom, html], ids=["turbohtml", "lxml"])
def test_replace_preserves_both_tails(backend: ModuleType) -> None:
    root = backend.fromstring("<div><p>A</p>old<em>C</em></div>")
    removed = root[0]
    replacement = backend.Element("strong")
    replacement.tail = "new"

    root.replace(removed, replacement)

    assert (removed.tail, replacement.tail, root.text_content()) == ("old", "new", "newC")


@pytest.mark.parametrize("backend", [dom, html], ids=["turbohtml", "lxml"])
def test_drop_tree_keeps_tail_in_parent(backend: ModuleType) -> None:
    root = backend.fromstring("<div><p>A<b>B</b></p>tail<em>C</em></div>")
    removed = root[0]
    descendant = removed[0]

    removed.drop_tree()

    assert (removed.tail, root.text_content(), removed[0] is descendant) == ("tail", "tailC", True)


@pytest.mark.parametrize("backend", [dom, html], ids=["turbohtml", "lxml"])
def test_detached_element_can_set_tail(backend: ModuleType) -> None:
    element = backend.Element("p")

    element.tail = "tail"

    assert element.tail == "tail"


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        pytest.param("remove_current", ["b", "c"], id="remove-current-subtree"),
        pytest.param("drop_current", ["b", "c"], id="drop-current-subtree"),
        pytest.param("remove_next", ["b"], id="remove-prefetched-child"),
        pytest.param("insert_after", ["b", "c", "x", "d", "e", "f"], id="insert-after-current"),
    ],
)
@pytest.mark.parametrize("descendants", [False, True], ids=["include-root", "descendants-only"])
@pytest.mark.parametrize("backend", [dom, html], ids=["turbohtml", "lxml"])
def test_iter_mutation_matches_lxml(mutation: str, expected: list[str], descendants: bool, backend: ModuleType) -> None:
    root = backend.fromstring("<div><a><b></b><c></c></a><d><e></e></d><f></f></div>")
    walk = root.iterdescendants("*") if descendants else root.iter("*")
    if not descendants:
        next(walk)
    current = next(walk)
    if mutation == "remove_current":
        root.remove(current)
    elif mutation == "drop_current":
        current.drop_tree()
    elif mutation == "remove_next":
        current.remove(current[0])
    else:
        current.addnext(backend.Element("x"))
    assert [element.tag for element in walk] == expected


@pytest.mark.parametrize("backend", [dom, html], ids=["turbohtml", "lxml"])
def test_iter_filtered_detached_subtree(backend: ModuleType) -> None:
    root = backend.fromstring("<div><a><b></b><c></c></a><d></d></div>")
    walk = root.iter("a", "c")
    root.remove(next(walk))
    assert [element.tag for element in walk] == ["c"]


@pytest.mark.parametrize(
    "invalid_name",
    [pytest.param("", id="empty"), pytest.param("bad name", id="space"), pytest.param("bad\x00name", id="null")],
)
def test_element_invalid_attribute_keeps_later_attributes(invalid_name: str) -> None:
    element = dom.Element("p", {"id": "before", invalid_name: "invalid", "title": "after"})

    assert dict(element.attrib) == {"id": "before", "title": "after"}


def test_to_lxml_invalid_attribute_keeps_later_attributes() -> None:
    element = dom.Element("g:p", {"id": "before", 'x":': "invalid", "title": "after"})

    assert dict(dom.to_lxml(element).attrib) == {"id": "before", "title": "after"}
