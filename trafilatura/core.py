# pylint:disable-msg=E0611,I1101
"""
Extraction configuration and processing functions.
"""

import logging

from copy import copy
from typing import Any, Optional




from .htmlprocessing import (
    build_html_output,
    convert_tags,
    tree_cleaning,
)
from .main_extractor import  extract_content
from .settings import Document, Extractor
from .utils import (
    load_html,
    normalize_unicode,
)
from .xml import build_json_output, control_xml_output, xmltotxt, xmltocsv



LOGGER = logging.getLogger(__name__)

TXT_FORMATS = {"markdown", "txt"}


def determine_returnstring(document: Document, options: Extractor) -> str:
    """Convert XML tree to chosen format, clean the result and output it as a string"""
    # XML (TEI) steps
    if "xml" in options.format:
        # last cleaning
        for element in document.body.iter("*"):
            if (
                element.tag != "graphic"
                and len(element) == 0
                and not element.text
                and not element.tail
            ):
                parent = element.getparent()
                # do not remove elements inside <code> to preserve formatting
                if parent is not None and parent.tag != "code":
                    parent.remove(element)
        # build output tree
        returnstring = control_xml_output(document, options)
    # CSV
    elif options.format == "csv":
        returnstring = xmltocsv(document, options.formatting)
    # JSON
    elif options.format == "json":
        returnstring = build_json_output(document, options.with_metadata)
    # HTML
    elif options.format == "html":
        returnstring = build_html_output(document, options.with_metadata)
    # Markdown and TXT
    else:
        if options.with_metadata:
            header = "---\n"
            for attr in (
                "title",
                "author",
                "url",
                "hostname",
                "description",
                "sitename",
                "date",
                "categories",
                "tags",
                "fingerprint",
                "id",
                "license",
            ):
                if getattr(document, attr):
                    header += f"{attr}: {str(getattr(document, attr))}\n"
            header += "---\n"
        else:
            header = ""
        returnstring = f"{header}{xmltotxt(document.body, options.formatting)}"
        if document.commentsbody is not None:
            returnstring = \
                f"{returnstring}\n{xmltotxt(document.commentsbody, options.formatting)}".strip()
    # normalize Unicode format (defaults to NFC)
    return normalize_unicode(returnstring)



def _internal_extraction(
        filecontent: Any,
        output_format: str,
        include_tables: bool = True,
        include_images: bool = False,
        include_formatting: bool = False,
        include_links: bool = False,
) -> Optional[Document]:
    options = Extractor(
        output_format=output_format,
        formatting=include_formatting,
        links=include_links,
        images=include_images,
        tables=include_tables,
    )

    
    try:
        tree = load_html(filecontent)
        if tree is None:
            LOGGER.error("empty HTML tree: %s", url)
            raise ValueError        
        document = Document()

        cleaned_tree = tree_cleaning(copy(tree), options)
        cleaned_tree = convert_tags(cleaned_tree, options, options.url or document.url)

        
        # postbody  = trafilatura_sequence(
        #     cleaned_tree,
        #     options
        # )
        postbody = extract_content(cleaned_tree, options)
        

    except (TypeError, ValueError):
        LOGGER.warning("discarding data: %s", options.source)
        return None

    # document.raw_text, document.commentsbody = temp_text, commentsbody
    document.body = postbody



    document.text = determine_returnstring(document, options)
    return document
