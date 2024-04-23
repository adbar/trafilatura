# pylint:disable-msg=E0611,I1101
"""
Extraction configuration and processing functions.
"""

import logging
import sys
import warnings

from copy import copy, deepcopy

from lxml.etree import XPath, strip_tags

# own
from .baseline import baseline
from .external import compare_extraction
from .filters import (LANGID_FLAG, check_html_lang, duplicate_test,
                      language_filter)
from .hashing import content_fingerprint
from .htmlprocessing import convert_tags, prune_unwanted_nodes, tree_cleaning
from .main_extractor import extract_comments, extract_content
from .metadata import Document, extract_metadata
from .settings import DEFAULT_CONFIG, Extractor, use_config
from .utils import load_html, normalize_unicode
from .xml import build_json_output, control_xml_output, xmltotxt, xmltocsv
from .xpaths import REMOVE_COMMENTS_XPATH


LOGGER = logging.getLogger(__name__)


def determine_returnstring(document, options):
    '''Convert XML tree to chosen format, clean the result and output it as a string'''
    # XML (TEI) steps
    if 'xml' in options.format:
        # last cleaning
        for element in document.body.iter('*'):
            if element.tag != 'graphic' and len(element) == 0 and not element.text and not element.tail:
                parent = element.getparent()
                # do not remove elements inside <code> to preserve formatting
                if parent is not None and parent.tag != 'code':
                    parent.remove(element)
        # build output tree
        returnstring = control_xml_output(document, options)
    # CSV
    elif options.format == 'csv':
        returnstring = xmltocsv(document, options.formatting)
    # JSON
    elif options.format == 'json':
        returnstring = build_json_output(document)
    # Markdown and TXT
    else:
        returnstring = xmltotxt(document.body, options.formatting)
        if document.commentsbody is not None:
            returnstring = f"{returnstring}\n{xmltotxt(document.commentsbody, options.formatting)}".strip()
    # normalize Unicode format (defaults to NFC)
    return normalize_unicode(returnstring)


def bare_extraction(filecontent, url=None, no_fallback=False,  # fast=False,
                    favor_precision=False, favor_recall=False,
                    include_comments=True, output_format="python", target_language=None,
                    include_tables=True, include_images=False, include_formatting=False,
                    include_links=False, deduplicate=False,
                    date_extraction_params=None,
                    only_with_metadata=False, with_metadata=False,
                    max_tree_size=None, url_blacklist=None, author_blacklist=None,
                    as_dict=True, prune_xpath=None,
                    config=DEFAULT_CONFIG, options=None):
    """Internal function for text extraction returning bare Python variables.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        no_fallback: Use faster heuristics and skip backup extraction.
        favor_precision: prefer less text but correct extraction.
        favor_recall: prefer more text even when unsure.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format, Python being the default
            and the interest of this internal function.
            Other values: "csv", "json", "markdown", "txt", "xml", and "xmltei".
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (present in XML format, converted to markdown otherwise).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        only_with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        max_tree_size: Discard documents with too many elements.
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.
        as_dict: Legacy option, return a dictionary instead of a class with attributes.
        prune_xpath: Provide an XPath expression to prune the tree before extraction.
            can be str or list of str.
        config: Directly provide a configparser configuration.
        options: Directly provide a whole extractor configuration.

    Returns:
        A Python dict() containing all the extracted information or None.

    Raises:
        ValueError: Extraction problem.
    """

    # deprecation warnings
    if with_metadata is True:
        only_with_metadata = with_metadata
        warnings.warn(
            '"with_metadata" will be deprecated in a future version, use "only_with_metadata instead"',
            PendingDeprecationWarning
        )
    #if no_fallback is True:
    #    fast = no_fallback
        #warnings.warn(
        #    '"no_fallback" will be deprecated in a future version, use "fast" instead',
        #    PendingDeprecationWarning
        #)

    # load data
    try:
        tree = load_html(filecontent)
        if tree is None:
            LOGGER.error('empty HTML tree: %s', url)
            raise ValueError

        # regroup extraction options
        if not options or not isinstance(options, Extractor):
            options = Extractor(
                          config=config, output_format=output_format,
                          fast=no_fallback, precision=favor_precision, recall=favor_recall,
                          comments=include_comments, formatting=include_formatting, links=include_links,
                          images=include_images, tables=include_tables,
                          dedup=deduplicate, lang=target_language, max_tree_size=max_tree_size,
                          url=url, only_with_metadata=only_with_metadata,
                          author_blacklist=author_blacklist, url_blacklist=url_blacklist,
                          date_params=date_extraction_params
                      )

        # quick and dirty HTML lang check
        if options.lang and (options.fast or LANGID_FLAG is False):
            if check_html_lang(tree, options.lang) is False:
                LOGGER.error('wrong HTML meta language: %s', options.source)
                raise ValueError

        # extract metadata if necessary
        if options.format not in ("markdown", "txt"):

            document = extract_metadata(tree, options.url, options.date_params, options.fast, options.author_blacklist)

            # cut short if extracted URL in blacklist
            if document.url in options.url_blacklist:
                LOGGER.warning('blacklisted URL: %s', document.url)
                raise ValueError

            # cut short if core elements are missing
            if options.only_with_metadata and any(
                    x is None for x in
                    [document.date, document.title, document.url]
            ):
                LOGGER.error('no metadata: %s', options.source)
                raise ValueError

        else:
            document = Document()

        # prune all xpath expressions that user specified
        # no backup as this is unetre full control of the user
        if prune_xpath is not None:
            if isinstance(prune_xpath, str):
                prune_xpath = [prune_xpath]
            tree = prune_unwanted_nodes(tree, [XPath(x) for x in prune_xpath])

        # backup for further processing
        tree_backup = copy(tree)

        # clean
        cleaned_tree = tree_cleaning(tree, options)
        cleaned_tree_backup = copy(cleaned_tree)

        # convert tags, the rest does not work without conversion
        cleaned_tree = convert_tags(cleaned_tree, options, options.url or document.url)

        # comments first, then remove
        if options.comments:
            commentsbody, temp_comments, len_comments, cleaned_tree = extract_comments(cleaned_tree, options)
        else:
            commentsbody, temp_comments, len_comments = None, '', 0
        if options.focus == "precision":
            cleaned_tree = prune_unwanted_nodes(cleaned_tree, REMOVE_COMMENTS_XPATH)

        # extract content
        postbody, temp_text, len_text = extract_content(cleaned_tree, options)

        # compare if necessary
        if not options.fast:
            postbody, temp_text, len_text = compare_extraction(cleaned_tree_backup, deepcopy(tree_backup), postbody, temp_text, len_text, options)
        # add baseline as additional fallback
        # rescue: try to use original/dirty tree # and favor_precision is False=?
        if len_text < options.min_extracted_size:
            postbody, temp_text, len_text = baseline(deepcopy(tree_backup))
            LOGGER.debug('non-clean extracted length: %s (extraction)', len_text)

        # tree size sanity check
        if options.max_tree_size:
            # strip tags
            if len(postbody) > options.max_tree_size:
                LOGGER.debug('output tree too long: %s', len(postbody))
                strip_tags(postbody, 'hi')
            # still too long, raise an error
            if len(postbody) > options.max_tree_size:
                LOGGER.debug('output tree too long: %s, discarding %s', len(postbody), options.source)
                raise ValueError
        # size checks
        if options.comments and len_comments < options.min_extracted_comm_size:
            LOGGER.debug('not enough comments: %s', options.source)
        if len_text < options.min_output_size and \
           len_comments < options.min_output_comm_size:
            LOGGER.debug('text and comments not long enough: %s %s %s', len_text, len_comments, options.source)
            raise ValueError

        # check duplicates at body level
        if options.dedup and duplicate_test(postbody, options) is True:
            LOGGER.debug('discarding duplicate document: %s', options.source)
            raise ValueError

        # sanity check on language
        if options.lang:
            is_not_target_lang, document = language_filter(temp_text, temp_comments, options.lang, document)
            if is_not_target_lang is True:
                LOGGER.debug('wrong language: %s', options.source)
                raise ValueError

    except (TypeError, ValueError):
        LOGGER.warning('discarding data: %s', options.source)
        return None

    # special case: python variables
    if options.format == 'python':
        document.text = xmltotxt(postbody, options.formatting)
        if options.comments:
            document.comments = xmltotxt(commentsbody, options.formatting)
            document.commentsbody = commentsbody
        document.raw_text = document.text
    else:
        document.raw_text, document.commentsbody = temp_text, commentsbody
    document.body = postbody

    return document if not as_dict else document.as_dict()


def extract(filecontent, url=None, record_id=None, no_fallback=False,
            favor_precision=False, favor_recall=False,
            include_comments=True, output_format="txt",
            tei_validation=False, target_language=None,
            include_tables=True, include_images=False, include_formatting=False,
            include_links=False, deduplicate=False,
            date_extraction_params=None,
            only_with_metadata=False, with_metadata=False,
            max_tree_size=None, url_blacklist=None, author_blacklist=None,
            settingsfile=None, prune_xpath=None,
            config=DEFAULT_CONFIG, options=None,
            **kwargs):
    """Main function exposed by the package:
       Wrapper for text extraction and conversion to chosen output format.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        record_id: Add an ID to the metadata.
        no_fallback: Skip the backup extraction with readability-lxml and justext.
        favor_precision: prefer less text but correct extraction.
        favor_recall: when unsure, prefer more text.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format:
            "csv", "json", "markdown", "txt", "xml", and "xmltei".
        tei_validation: Validate the XML-TEI output with respect to the TEI standard.
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (only valuable if output_format is set to XML).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        only_with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        max_tree_size: Discard documents with too many elements.
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.
        settingsfile: Use a configuration file to override the standard settings.
        prune_xpath: Provide an XPath expression to prune the tree before extraction.
            can be str or list of str.
        config: Directly provide a configparser configuration.
        options: Directly provide a whole extractor configuration.

    Returns:
        A string in the desired format or None.

    """
    # older, deprecated functions
    if kwargs and any([
        # output formats
            'csv_output' in kwargs,
            'json_output' in kwargs,
            'tei_output' in kwargs,
            'xml_output' in kwargs
        ]):
        raise NameError(
            'Deprecated argument: use output_format instead, e.g. output_format="xml"'
            )
        # todo: add with_metadata later

    # regroup extraction options
    if not options or not isinstance(options, Extractor):
        options = Extractor(
                      config=use_config(settingsfile, config), output_format=output_format,
                      fast=no_fallback, precision=favor_precision, recall=favor_recall,
                      comments=include_comments, formatting=include_formatting, links=include_links,
                      images=include_images, tables=include_tables,
                      dedup=deduplicate, lang=target_language, max_tree_size=max_tree_size,
                      url=url, only_with_metadata=only_with_metadata,
                      tei_validation=tei_validation,
                      author_blacklist=author_blacklist, url_blacklist=url_blacklist,
                      date_params=date_extraction_params
                  )

    # markdown switch
    include_formatting = include_formatting or output_format == "markdown"

    # extraction
    try:
        document = bare_extraction(
            filecontent, options=options,
            with_metadata=with_metadata,
            as_dict=False, prune_xpath=prune_xpath,
        )
    except RuntimeError:
        LOGGER.error('Processing timeout for %s', url)
        document = None

    # post-processing
    if document is None:
        return None

    if options.format not in ("markdown", "txt"):
        # add record ID to metadata
        document.id = record_id
        # calculate fingerprint
        if document.raw_text is not None:
            document.fingerprint = content_fingerprint(str(document.title) + " " + str(document.raw_text))

    # return
    return determine_returnstring(document, options)


def process_record(*args, **kwargs):
    "Deprecated extraction function."
    sys.exit("process_record() is deprecated, use extract() instead")
