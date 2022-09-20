"""
Test for transformation to TEI.
"""
from lxml.etree import Element, fromstring

from trafilatura.metadata import Document
from trafilatura.xml import check_tei, write_fullheader


def test_publisher_added_before_availability_in_publicationStmt():
    # add publisher string
    teidoc = Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    metadata = Document()
    metadata.sitename = "The Publisher"
    metadata.license = "CC BY-SA 4.0"
    metadata.categories = metadata.tags = ["cat"]
    header = write_fullheader(teidoc, metadata)
    publicationstmt = header.find(".//{*}fileDesc/{*}publicationStmt")
    assert [child.tag for child in publicationstmt.getchildren()] == [
        "publisher",
        "availability",
    ]
    assert publicationstmt[0].text == "The Publisher"

    teidoc = Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    metadata = Document()
    metadata.hostname = "example.org"
    metadata.license = "CC BY-SA 4.0"
    metadata.categories = metadata.tags = ["cat"]
    header = write_fullheader(teidoc, metadata)
    publicationstmt = header.find(".//{*}fileDesc/{*}publicationStmt")
    assert [child.tag for child in publicationstmt.getchildren()] == [
        "publisher",
        "availability",
    ]
    assert publicationstmt[0].text == "example.org"

    teidoc = Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    metadata = Document()
    metadata.hostname = "example.org"
    metadata.sitename = "Example"
    metadata.license = "CC BY-SA 4.0"
    metadata.categories = metadata.tags = ["cat"]
    header = write_fullheader(teidoc, metadata)
    publicationstmt = header.find(".//{*}fileDesc/{*}publicationStmt")
    assert [child.tag for child in publicationstmt.getchildren()] == [
        "publisher",
        "availability",
    ]
    assert publicationstmt[0].text == "Example (example.org)"
    # no publisher, add "N/A"
    teidoc = Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    metadata = Document()
    metadata.categories = metadata.tags = ["cat"]
    metadata.license = "CC BY-SA 4.0"
    header = write_fullheader(teidoc, metadata)
    publicationstmt = header.find(".//{*}fileDesc/{*}publicationStmt")
    assert [child.tag for child in publicationstmt.getchildren()] == [
        "publisher",
        "availability",
    ]
    assert publicationstmt[0].text == "N/A"
    # no license, add nothing
    teidoc = Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    metadata = Document()
    metadata.categories = metadata.tags = ["cat"]
    header = write_fullheader(teidoc, metadata)
    publicationstmt = header.find(".//{*}fileDesc/{*}publicationStmt")
    assert [child.tag for child in publicationstmt.getchildren()] == ["p"]


def test_head_with_children_converted_to_ab():
    xml_doc = fromstring("<text><head>heading</head><p>some text</p></text>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [
        (child.tag, child.text) if child.text is not None else child.tag
        for child in cleaned.iter()
    ]
    assert result == ["text", ("fw", "heading"), ("p", "some text")]
    xml_doc = fromstring("<text><head><p>text</p></head></text>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [(child.tag, child.text, child.tail) for child in cleaned.iter()]
    assert result == [("text", None, None), ("ab", "text", None)]
    head_with_mulitple_p = fromstring(
        "<text><head><p>first</p><p>second</p><p>third</p></head></text>"
    )
    cleaned = check_tei(head_with_mulitple_p, "fake_url")
    result = [(child.tag, child.text, child.tail) for child in cleaned.iter()]
    # print(result)
    assert result == [
        ("text", None, None),
        ("ab", "first", None),
        ("lb", None, "second"),
        ("lb", None, "third"),
    ]
    xml_with_complex_head = fromstring(
        "<text><head><p>first</p><list><item>text</item></list><p>second</p><p>third</p></head></text>"
    )
    cleaned = check_tei(xml_with_complex_head, "fake_url")
    result = [(child.tag, child.text, child.tail) for child in cleaned.iter()]
    assert result == [
        ("text", None, None),
        ("ab", "first", None),
        ("list", None, "second"),
        ("item", "text", None),
        ("lb", None, "third"),
    ]
    xml_doc = fromstring("<text><head><list><item>text1</item></list><p>text2</p></head></text>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [(child.tag, child.text, child.tail) for child in cleaned.iter()]
    assert result == [
        ("text", None, None),
        ("ab", None, None),
        ("list", None, "text2"),
        ("item", "text1", None)
    ]
    xml_doc = fromstring("<text><head>heading</head><p>some text</p></text>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = cleaned[0].attrib
    assert result == {"type":"header"}
    xml_doc = fromstring("<text><head rend='h3'>heading</head><p>some text</p></text>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = cleaned[0].attrib
    assert result == {"type":"header", "rend":"h3"}


if __name__ == "__main__":
    test_publisher_added_before_availability_in_publicationStmt()
    test_head_with_children_converted_to_ab()
