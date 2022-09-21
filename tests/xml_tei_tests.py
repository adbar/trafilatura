"""
Test for transformation to TEI.
"""
from lxml.etree import Element, fromstring

from trafilatura.metadata import Document
from trafilatura.xml import write_fullheader, check_tei


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


def test_tail_on_p_like_elements_removed():
    xml_doc = fromstring(
        """
    <TEI><text><body>
      <div>
        <p>text</p>former link
        <p>more text</p>former span
        <p>even more text</p>another span
      </div>
    </body></text></TEI>""")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [(el.text, el.tail) for el in cleaned.iter('p')]
    assert result == [("text former link", None), ("more text former span", None), ("even more text another span", None)]
    xml_doc = fromstring("<TEI><text><body><div><head>title</head>some text<p>article</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text, elem.tail) for elem in cleaned.find(".//div").iterdescendants()]
    assert result == [("fw", "title", None), ("p", "some text", None), ("p", "article", None)]
    xml_doc = fromstring("<TEI><text><body><div><ab>title</ab>tail<p>more text</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text, elem.tail) for elem in cleaned.find(".//div").iterdescendants()]
    assert result == [("ab", "title", None), ("p", "tail", None), ("p", "more text", None)]
    xml_doc = fromstring("<TEI><text><body><div><p>text</p><lb/>tail</div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text, elem.tail) for elem in cleaned.find(".//div").iterdescendants()]
    assert result == [("p", "text", None), ("p", "tail", None)]


if __name__ == "__main__":
    test_publisher_added_before_availability_in_publicationStmt()
    test_tail_on_p_like_elements_removed()
