"""
Test for transformation to TEI.
"""
from lxml.etree import Element

from trafilatura.metadata import Document
from trafilatura.xml import write_fullheader


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


if __name__ == "__main__":
    test_publisher_added_before_availability_in_publicationStmt()
