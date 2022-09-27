"""
Test for transformation to TEI.
"""
from lxml.etree import Element, fromstring, tostring

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


def test_unwanted_siblings_of_div_removed():
    xml_doc = fromstring("<TEI><text><body><div><div><p>text1</p></div><p>text2</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result =  [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "div", "p", "div", "p"]
    assert result == expected
    result_str = tostring(cleaned.find(".//body"), encoding="unicode")
    expected_str = "<body><div><div><p>text1</p></div><div><p>text2</p></div></div></body>"
    assert result_str == expected_str
    xml_doc = fromstring("<TEI><text><body><div><div/><list><item>text</item></list></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "div", "div", "list", "item"]
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><div/><table><row><cell>text</cell></row></table></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "div", "div", "table", "row", "cell"]
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><p>text1</p><div/><div/><p>text2</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = tostring(cleaned.find(".//body"), encoding="unicode")
    expected = "<body><div><p>text1</p><div/><div/><div><p>text2</p></div></div></body>"
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><div><p>text1</p></div><p>text2</p><p>text3</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "div", "p", "div", "p", "p"]
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><p>text1</p><div/><p>text2</p><div/><p>text3</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "p", "div", "div", "p", "div", "div", "p"]
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><p>text1</p><div/><p>text2</p><div/><list/></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "p", "div", "div", "p", "div", "div", "list"]
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><p/><div/><p>text1</p><fw/><p>text2</p></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result_str = tostring(cleaned.find(".//body"), encoding="unicode")
    expected_str = "<body><div><p/><div/><div><p>text1</p></div><fw/><div><p>text2</p></div></div></body>"
    assert result_str == expected_str
    xml_doc = fromstring("<TEI><text><body><div><div/><ab/></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result_str = tostring(cleaned.find(".//body"), encoding="unicode")
    expected_str = "<body><div><div/><div><ab/></div></div></body>"
    assert result_str == expected_str
    xml_doc = fromstring("<TEI><text><body><div><div/><quote>text</quote></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    expected = ["div", "div", "div", "quote"]
    assert result == expected
    xml_doc = fromstring("<TEI><text><body><div><div/><lb/></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    assert result == ["div", "div", "lb"]
    xml_doc = fromstring("<TEI><text><body><div><div/><fw/></div></body></text></TEI>")
    cleaned = check_tei(xml_doc, "fake_url")
    result = [elem.tag for elem in cleaned.find(".//div").iter()]
    assert result == ["div", "div", "fw"]


if __name__ == "__main__":
    test_publisher_added_before_availability_in_publicationStmt()
    test_unwanted_siblings_of_div_removed()
