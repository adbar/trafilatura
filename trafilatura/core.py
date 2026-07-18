# pylint:disable-msg=E0611,I1101
"""
Extraction configuration and processing functions.
"""

import json
import logging
import re
import warnings
from configparser import ConfigParser
from copy import copy
from typing import Any

from lxml.etree import Element, XPath, _Element, strip_tags
from lxml.html import HtmlElement

# own
from .baseline import baseline, html2txt
from .deduplication import content_fingerprint, duplicate_test
from .external import compare_extraction, justext_rescue
from .htmlprocessing import (
    build_html_output,
    convert_tags,
    prune_unwanted_nodes,
    tree_cleaning,
)
from .main_extractor import _elem_text, extract_comments, extract_content
from .metadata import Document, extract_metadata
from .settings import DEFAULT_CONFIG, Extractor, use_config
from .utils import (
    LANGID_FLAG,
    check_html_lang,
    language_filter,
    load_html,
    normalize_unicode,
)
from .xml import build_json_output, control_xml_output, xmltocsv, xmltotxt
from .xpaths import REMOVE_COMMENTS_XPATH

LOGGER = logging.getLogger(__name__)

# recall escalation (see trafilatura_sequence, stage 4): retry a short balanced extraction
# in recall mode. Calibrated as a set against the benchmark suite (own-bench/WMB/WCXB/AEB) —
# don't tune one value in isolation, and re-run the full suite after any change.
ESCALATION_MAX_LENGTH = 3000  # only consider extractions below this size
ESCALATION_PAGE_SHARE = 0.2  # ... covering less than this share of the page text
ESCALATION_ACCEPT_RATIO = 1.5  # accept the retry if it is this much longer
# justext tends to over-include (whole pricing tables, unrelated sections) rather than stop at
# page boundaries the way the rule-based retry does, so it needs a stricter bar than the
# retry's own 1.5x: swept 1.5-10x, 2.0x is the best balance across the full suite.
ESCALATION_JUSTEXT_RATIO = 2.0

TXT_FORMATS = {"markdown", "txt"}

# Metadata is emitted as a YAML-style Markdown header; values such as a title
# containing ": " (or a leading indicator, or a reserved word) otherwise produce
# invalid YAML or get reinterpreted as a non-string. See GH #814.
_YAML_RESERVED = frozenset({"true", "false", "yes", "no", "on", "off", "y", "n", "null", "none", "~"})


def _yaml_scalar(value: str) -> str:
    "Render a metadata string as a plain or double-quoted YAML-safe scalar."
    if (
        value
        and value == value.strip()
        and value[0].isalpha()
        and ": " not in value
        and " #" not in value
        and not value.endswith(":")
        and value.lower() not in _YAML_RESERVED
        and all(ch >= " " and ch != "\x7f" for ch in value)
    ):
        return value
    # a JSON string is always a valid, exactly round-tripping YAML double-quoted scalar
    return json.dumps(value, ensure_ascii=False)


def determine_returnstring(document: Document, options: Extractor) -> str:
    """Convert XML tree to chosen format, clean the result and output it as a string"""
    # XML (TEI) steps
    if "xml" in options.format:
        # last cleaning
        for element in document.body.iter("*"):
            if element.tag != "graphic" and len(element) == 0 and not element.text and not element.tail:
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
                value = getattr(document, attr)
                if value:
                    # quote scalar strings when needed; categories/tags are lists
                    # rendered as their (already valid) flow-sequence repr
                    if isinstance(value, str):
                        value = _yaml_scalar(value)
                    header += f"{attr}: {value}\n"
            header += "---\n"
        else:
            header = ""
        returnstring = f"{header}{xmltotxt(document.body, options.formatting)}"
        if document.commentsbody is not None:
            returnstring = f"{returnstring}\n{xmltotxt(document.commentsbody, options.formatting)}".strip()
    # normalize Unicode format (defaults to NFC)
    return normalize_unicode(returnstring)


# matches "@type": "DiscussionForumPosting" or an @type array containing it, anchored to the
# key so it can't fire on the words appearing in ordinary prose (e.g. a description field)
_DISCUSSION_FORUM_POSTING_RE = re.compile(
    r'"@type"\s*:\s*"DiscussionForumPosting"|"@type"\s*:\s*\[[^\]]*"DiscussionForumPosting"'
)


def _forum_thread_page(tree: HtmlElement) -> bool:
    """Detect a thread-forum page where posts live in the same containers
    REMOVE_COMMENTS_XPATH would otherwise prune -- comments are content here, unlike on
    a blog or article. Seeded by schema.org DiscussionForumPosting alone. Q&A forums
    (StackExchange, schema.org QAPage) are deliberately not matched: their answers live
    outside comment containers. Misses forums that don't emit DiscussionForumPosting
    (e.g. old Reddit) -- an accepted gap. Meant as a reusable seed for a future page-type
    router, not a one-off check.
    """
    return any(
        script.text and _DISCUSSION_FORUM_POSTING_RE.search(script.text)
        for script in tree.iterfind('.//script[@type="application/ld+json"]')
    )


def _prepare_tree(tree: HtmlElement, options: Extractor, url: str | None) -> tuple[HtmlElement, HtmlElement]:
    "Clean and convert a raw tree, returning (converted, pre-conversion backup)."
    cleaned = tree_cleaning(copy(tree), options)
    backup = copy(cleaned)
    cleaned = convert_tags(cleaned, options, url)
    return cleaned, backup


def _recall_retry(esc_tree: HtmlElement, r_options: Extractor, url: str | None) -> tuple[_Element, str, int]:
    """Stage-4 retry: re-run cascade stages 1-2 in recall mode on the escalation input
    (arrives comment-pruned, or intact on a thread-forum where posts are content).
    Deliberately no comment capture, no baseline (it already ran on the full page; on a
    comment-pruned tree it only yields an indistinguishable boilerplate dump), no escalation."""
    cleaned_tree, cleaned_tree_backup = _prepare_tree(esc_tree, r_options, url)
    postbody, temp_text, len_text = extract_content(cleaned_tree, r_options)
    if not r_options.fast:
        postbody, temp_text, len_text = compare_extraction(
            cleaned_tree_backup, copy(esc_tree), postbody, temp_text, len_text, r_options
        )
    return postbody, temp_text, len_text


def trafilatura_sequence(
    tree: HtmlElement,
    options: Extractor,
    url: str | None = None,
) -> tuple[_Element, str, int, _Element, str, int]:
    """Prepare the raw tree (cleaning, tag conversion, comment handling), then execute the
    standard cascade of extractors used by Trafilatura, each stage only engaging if the
    previous one under-delivered:
    1. main extractor (includes wild-text recovery for short documents)
    2. comparison with external extractors (readability/justext), skipped in fast mode
    3. baseline rescue on the original, uncleaned tree
    4. recall escalation, if the result still covers little of the page: stages 1-2 re-run
       in recall mode (_recall_retry), plus a justext candidate tried alongside (a different
       algorithm, not just stricter rules, so it reaches content the rule-based retry cannot)
    Returns the body triple and the comments triple.

    Internal helper: its signature and 6-tuple return are not a stable API — call
    ``bare_extraction``/``extract`` instead.
    """
    is_forum = _forum_thread_page(tree)
    # comments off: prune on the raw tree so all stages inherit it (only precision did before)
    if not options.comments and (options.focus == "precision" or not is_forum):
        tree = prune_unwanted_nodes(copy(tree), REMOVE_COMMENTS_XPATH)
    cleaned_tree, cleaned_tree_backup = _prepare_tree(tree, options, url)

    commentsbody, temp_comments, len_comments = Element("body"), "", 0
    forum_posts = None
    if options.comments:
        commentsbody, temp_comments, len_comments, cleaned_tree = extract_comments(cleaned_tree, options)
        if len_comments > 0 and is_forum:
            # thread-forum: the "comments" are the posts -> route into the body (backup predates
            # capture); keep the capture aside, salvaged below if the cascade drops the posts
            forum_posts = commentsbody
            commentsbody, temp_comments, len_comments = Element("body"), "", 0
            cleaned_tree = convert_tags(copy(cleaned_tree_backup), options, url)
    if options.focus == "precision" and not is_forum:
        # NOT redundant with the raw-tree prune above: this runs POST-conversion, where
        # <ul id="comments"> has become <list ...> and now matches the xpath's self::list
        cleaned_tree = prune_unwanted_nodes(cleaned_tree, REMOVE_COMMENTS_XPATH)

    # 1. Trafilatura's main extractor
    postbody, temp_text, len_text = extract_content(cleaned_tree, options)

    # 2. comparison with external extractors
    if not options.fast:
        postbody, temp_text, len_text = compare_extraction(
            cleaned_tree_backup,
            copy(tree),  # lxml copy() is already a deep, independent copy
            postbody,
            temp_text,
            len_text,
            options,
        )

    # 3. rescue: baseline on the original tree
    if len_text < options.min_extracted_size and options.focus != "precision":
        postbody, temp_text, len_text = baseline(tree)  # baseline copies element inputs
        LOGGER.debug("non-clean extracted length: %s (extraction)", len_text)
        forum_posts = None  # the dump saw the whole page: missing posts are boilerplate, not lost

    # 4. recall escalation: a short extraction covering little of the page suggests
    # under-extraction (non-article layout) — retry in recall mode, keep if clearly bigger.
    # NOTE: the page measure html2txt(tree) is coupled to BASIC_CLEAN_XPATH — see settings.py.
    if (
        options.focus == "balanced"
        and 0 < len_text < ESCALATION_MAX_LENGTH
        and len_text < ESCALATION_PAGE_SHARE * len(html2txt(tree))
    ):
        # a copy so a shared Extractor never leaks the "recall" focus back to the caller
        r_options = copy(options)
        r_options.focus = "recall"
        # strip comments from the escalation input (dup risk if captured, reader comments if not);
        # keep them on a thread-forum, where the retry rescues the posts
        esc_tree = tree if is_forum else prune_unwanted_nodes(copy(tree), REMOVE_COMMENTS_XPATH)
        r_len = 0
        try:
            r_body, r_text, r_len = _recall_retry(esc_tree, r_options, url)
        except Exception as err:  # pragma: no cover
            LOGGER.warning("recall retry failed: %s %s", err, url)
        # justext reaches div-buried content the rule retry misses (gated: ungated regressed
        # own-fallback). No region scoping of its own -> esc_tree is comment-pruned above
        j_len = 0
        if not options.fast:
            try:
                j_body, j_text, j_len = justext_rescue(copy(esc_tree), options)
            except Exception as err:  # pragma: no cover
                LOGGER.warning("justext candidate failed: %s %s", err, url)

        # floor on the retry: a result below the pipeline's own minimum is noise (the retry's
        # former internal baseline used to displace such outputs). cookie/consent banners justext
        # could pick up are pruned from its input in basic_cleaning. An accepted candidate saw the
        # full page, so its exclusions are deliberate -> drop the forum-post salvage.
        if j_len > r_len and j_len > ESCALATION_JUSTEXT_RATIO * len_text:
            postbody, temp_text, len_text, forum_posts = j_body, j_text, j_len, None
        elif r_len >= options.min_extracted_size and r_len > ESCALATION_ACCEPT_RATIO * len_text:
            postbody, temp_text, len_text, forum_posts = r_body, r_text, r_len, None

    if forum_posts is not None:
        # a gate (escalation length, precision) blocked the cascade from restoring the posts:
        # append the ones missing from the body
        existing = "\n".join(filter(None, (_elem_text(el) for el in postbody)))
        salvaged = [el for el in forum_posts if (t := _elem_text(el)) and t not in existing]
        if salvaged:
            LOGGER.debug("thread-forum salvage: %s captured posts appended to the body", len(salvaged))
            postbody.extend(salvaged)
            temp_text = " ".join(postbody.itertext()).strip()
            len_text = len(temp_text)

    return postbody, temp_text, len_text, commentsbody, temp_comments, len_comments


def bare_extraction(
    filecontent: Any,
    url: str | None = None,
    fast: bool = False,
    no_fallback: bool = False,
    favor_precision: bool = False,
    favor_recall: bool = False,
    include_comments: bool = True,
    output_format: str = "python",
    target_language: str | None = None,
    include_tables: bool = True,
    include_images: bool = False,
    include_formatting: bool | None = None,
    include_links: bool = False,
    deduplicate: bool = False,
    date_extraction_params: dict[str, Any] | None = None,
    with_metadata: bool = False,
    only_with_metadata: bool = False,
    max_tree_size: int | None = None,
    url_blacklist: set[str] | None = None,
    author_blacklist: set[str] | None = None,
    as_dict: bool = False,
    prune_xpath: str | list[str] | None = None,
    config: ConfigParser = DEFAULT_CONFIG,
    options: Extractor | None = None,
) -> Document | dict[str, Any] | None:
    """Internal function for text extraction returning bare Python variables.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        fast: Use faster heuristics and skip backup extraction.
        no_fallback: Deprecated, use "fast" instead.
        favor_precision: prefer less text but correct extraction.
        favor_recall: prefer more text even when unsure.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format, Python being the default
            and the interest of this internal function.
            Other values: "csv", "html", "json", "markdown", "txt", "xml", and "xmltei".
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (kept in XML, rendered as markdown for text formats; ignored for JSON).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        with_metadata: Extract metadata fields and add them to the output.
        only_with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.
        as_dict: Deprecated, use the .as_dict() method instead.
        prune_xpath: Provide an XPath expression to prune the tree before extraction.
            can be str or list of str.
        config: Directly provide a configparser configuration.
        options: Directly provide a whole extractor configuration.

    Returns:
        A Python dict() containing all the extracted information or None.

    Raises:
        ValueError: Extraction problem.

    Note:
        Low-level primitive: returns a Document with an unserialized .body tree; tei_validation only applies when serializing via extract().
        In the default balanced mode, a short extraction covering little of the page is automatically retried with recall settings.
    """

    # deprecations: stacklevel=3 → user → bare_extraction → _check_deprecation
    fast = _check_deprecation(
        fast,
        no_fallback=no_fallback,
        as_dict=as_dict,
        max_tree_size=max_tree_size,
        stacklevel=3,
    )

    # regroup extraction options
    if not options or not isinstance(options, Extractor):
        options = Extractor(
            config=config,
            output_format=output_format,
            fast=fast,
            precision=favor_precision,
            recall=favor_recall,
            comments=include_comments,
            formatting=include_formatting,
            links=include_links,
            images=include_images,
            tables=include_tables,
            dedup=deduplicate,
            lang=target_language,
            url=url,
            with_metadata=with_metadata,
            only_with_metadata=only_with_metadata,
            author_blacklist=author_blacklist,
            url_blacklist=url_blacklist,
            date_params=date_extraction_params,
        )

    try:
        # load the HTML tree
        tree = load_html(filecontent)
        if tree is None:
            LOGGER.error("empty HTML tree: %s", url)
            raise ValueError

        # quick and dirty HTML lang check
        if options.lang and (options.fast or not LANGID_FLAG):
            if check_html_lang(tree, options.lang) is False:
                LOGGER.error("wrong HTML meta language: %s", options.source)
                raise ValueError

        # extract metadata if necessary
        if options.with_metadata:
            document = extract_metadata(
                tree,
                options.url,
                options.date_params,
                options.fast,
                options.author_blacklist,
            )

            # cut short if extracted URL in blacklist
            if document.url in options.url_blacklist:
                LOGGER.warning("blacklisted URL: %s", document.url)
                raise ValueError

            # cut short if core elements are missing
            if options.only_with_metadata and not (document.date and document.title and document.url):
                LOGGER.error("no metadata: %s", options.source)
                raise ValueError

        else:
            document = Document()

        # prune all xpath expressions that user specified
        # no backup as this is unetre full control of the user
        if prune_xpath is not None:
            if isinstance(prune_xpath, str):
                prune_xpath = [prune_xpath]
            tree = prune_unwanted_nodes(tree, [XPath(x) for x in prune_xpath])

        postbody, temp_text, len_text, commentsbody, temp_comments, len_comments = trafilatura_sequence(
            tree, options, options.url or document.url
        )

        # tree size sanity check
        if options.max_tree_size:
            # strip tags
            if len(postbody) > options.max_tree_size:
                LOGGER.debug("output tree too long: %s", len(postbody))
                strip_tags(postbody, "hi")
            # still too long, raise an error
            if len(postbody) > options.max_tree_size:
                LOGGER.debug(
                    "output tree too long: %s, discarding %s",
                    len(postbody),
                    options.source,
                )
                raise ValueError
        # size checks
        if options.comments and len_comments < options.min_extracted_comm_size:
            LOGGER.debug("not enough comments: %s", options.source)
        if len_text < options.min_output_size and len_comments < options.min_output_comm_size:
            LOGGER.debug(
                "text and comments not long enough: %s %s %s",
                len_text,
                len_comments,
                options.source,
            )
            raise ValueError

        # check duplicates at body level
        if options.dedup and duplicate_test(postbody, options) is True:
            LOGGER.debug("discarding duplicate document: %s", options.source)
            raise ValueError

        # sanity check on language
        if options.lang:
            is_not_target_lang, document = language_filter(temp_text, temp_comments, options.lang, document)
            if is_not_target_lang is True:
                LOGGER.debug("wrong language: %s", options.source)
                raise ValueError

    except (TypeError, ValueError):
        LOGGER.warning("discarding data: %s", options.source)
        return None

    # special case: python variables
    if options.format == "python":
        document.text = xmltotxt(postbody, options.formatting)
        if options.comments:
            document.comments = xmltotxt(commentsbody, options.formatting)
            document.commentsbody = commentsbody
        document.raw_text = document.text
    else:
        document.raw_text, document.commentsbody = temp_text, commentsbody
    document.body = postbody

    return document if not as_dict else document.as_dict()


def extract(
    filecontent: Any,
    url: str | None = None,
    record_id: str | None = None,
    fast: bool = False,
    no_fallback: bool = False,
    favor_precision: bool = False,
    favor_recall: bool = False,
    include_comments: bool = True,
    output_format: str = "txt",
    tei_validation: bool = False,
    target_language: str | None = None,
    include_tables: bool = True,
    include_images: bool = False,
    include_formatting: bool | None = None,
    include_links: bool = False,
    deduplicate: bool = False,
    date_extraction_params: dict[str, Any] | None = None,
    with_metadata: bool = False,
    only_with_metadata: bool = False,
    max_tree_size: int | None = None,
    url_blacklist: set[str] | None = None,
    author_blacklist: set[str] | None = None,
    settingsfile: str | None = None,
    prune_xpath: str | list[str] | None = None,
    config: ConfigParser = DEFAULT_CONFIG,
    options: Extractor | None = None,
) -> str | None:
    """Main function exposed by the package:
       Wrapper for text extraction and conversion to chosen output format.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        record_id: Add an ID to the metadata.
        fast: Use faster heuristics and skip backup extraction.
        no_fallback: Deprecated, use "fast" instead.
        favor_precision: prefer less text but correct extraction.
        favor_recall: when unsure, prefer more text.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format:
            "csv", "html", "json", "markdown", "txt", "xml", and "xmltei".
        tei_validation: Validate the XML-TEI output with respect to the TEI standard.
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (kept in XML, rendered as markdown for text formats; ignored for JSON).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        with_metadata: Extract metadata fields and add them to the output.
        only_with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
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
    document = _internal_extraction(
        filecontent=filecontent,
        url=url,
        record_id=record_id,
        fast=fast,
        no_fallback=no_fallback,
        favor_precision=favor_precision,
        favor_recall=favor_recall,
        include_comments=include_comments,
        output_format=output_format,
        tei_validation=tei_validation,
        target_language=target_language,
        include_tables=include_tables,
        include_images=include_images,
        include_formatting=include_formatting,
        include_links=include_links,
        deduplicate=deduplicate,
        date_extraction_params=date_extraction_params,
        with_metadata=with_metadata,
        only_with_metadata=only_with_metadata,
        max_tree_size=max_tree_size,
        url_blacklist=url_blacklist,
        author_blacklist=author_blacklist,
        settingsfile=settingsfile,
        prune_xpath=prune_xpath,
        config=config,
        options=options,
    )
    return document.text if document is not None else None


def extract_with_metadata(
    filecontent: Any,
    url: str | None = None,
    record_id: str | None = None,
    fast: bool = False,
    favor_precision: bool = False,
    favor_recall: bool = False,
    include_comments: bool = True,
    output_format: str = "txt",
    tei_validation: bool = False,
    target_language: str | None = None,
    include_tables: bool = True,
    include_images: bool = False,
    include_formatting: bool | None = None,
    include_links: bool = False,
    deduplicate: bool = False,
    date_extraction_params: dict[str, Any] | None = None,
    url_blacklist: set[str] | None = None,
    author_blacklist: set[str] | None = None,
    settingsfile: str | None = None,
    prune_xpath: str | list[str] | None = None,
    config: ConfigParser = DEFAULT_CONFIG,
    options: Extractor | None = None,
) -> Document | None:
    """Main function exposed by the package:
       Wrapper for text extraction and conversion to chosen output format.
       This method also returns document metadata.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        record_id: Add an ID to the metadata.
        fast: Use faster heuristics and skip backup extraction.
        favor_precision: prefer less text but correct extraction.
        favor_recall: when unsure, prefer more text.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format:
            "csv", "html", "json", "markdown", "txt", "xml", and "xmltei".
        tei_validation: Validate the XML-TEI output with respect to the TEI standard.
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (kept in XML, rendered as markdown for text formats; ignored for JSON).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.
        settingsfile: Use a configuration file to override the standard settings.
        prune_xpath: Provide an XPath expression to prune the tree before extraction.
            can be str or list of str.
        config: Directly provide a configparser configuration.
        options: Directly provide a whole extractor configuration.

    Returns:
        Document metadata with content string in the desired format or None.
    """
    return _internal_extraction(
        filecontent=filecontent,
        url=url,
        record_id=record_id,
        fast=fast,
        favor_precision=favor_precision,
        favor_recall=favor_recall,
        include_comments=include_comments,
        output_format=output_format,
        tei_validation=tei_validation,
        target_language=target_language,
        include_tables=include_tables,
        include_images=include_images,
        include_formatting=include_formatting,
        include_links=include_links,
        deduplicate=deduplicate,
        date_extraction_params=date_extraction_params,
        with_metadata=True,
        only_with_metadata=False,
        url_blacklist=url_blacklist,
        author_blacklist=author_blacklist,
        settingsfile=settingsfile,
        prune_xpath=prune_xpath,
        config=config,
        options=options,
    )


def _check_deprecation(
    fast: bool = False,
    *,
    no_fallback: bool = False,
    as_dict: bool = False,
    max_tree_size: int | None = None,
    stacklevel: int = 2,
) -> bool:
    """Check deprecated params and return the effective "fast" flag."""
    if no_fallback:
        warnings.warn(
            '"no_fallback" will be removed, use "fast" instead',
            DeprecationWarning,
            stacklevel=stacklevel,
        )
    if as_dict:
        warnings.warn(
            '"as_dict" will be removed, use the .as_dict() method instead',
            DeprecationWarning,
            stacklevel=stacklevel,
        )
    if max_tree_size:
        raise ValueError('"max_tree_size" will be removed, use settings.cfg instead')
    return fast or no_fallback


def _internal_extraction(
    filecontent: Any,
    url: str | None = None,
    record_id: str | None = None,
    fast: bool = False,
    no_fallback: bool = False,
    favor_precision: bool = False,
    favor_recall: bool = False,
    include_comments: bool = True,
    output_format: str = "txt",
    tei_validation: bool = False,
    target_language: str | None = None,
    include_tables: bool = True,
    include_images: bool = False,
    include_formatting: bool | None = None,
    include_links: bool = False,
    deduplicate: bool = False,
    date_extraction_params: dict[str, Any] | None = None,
    with_metadata: bool = False,
    only_with_metadata: bool = False,
    max_tree_size: int | None = None,
    url_blacklist: set[str] | None = None,
    author_blacklist: set[str] | None = None,
    settingsfile: str | None = None,
    prune_xpath: str | list[str] | None = None,
    config: ConfigParser = DEFAULT_CONFIG,
    options: Extractor | None = None,
) -> Document | None:
    """Internal method to do the extraction"""
    # stacklevel=4 → user → extract → _internal_extraction → _check_deprecation
    fast = _check_deprecation(
        fast,
        no_fallback=no_fallback,
        as_dict=False,
        max_tree_size=max_tree_size,
        stacklevel=4,
    )

    # regroup extraction options
    if not options or not isinstance(options, Extractor):
        options = Extractor(
            config=use_config(settingsfile) if settingsfile else config,
            output_format=output_format,
            fast=fast,
            precision=favor_precision,
            recall=favor_recall,
            comments=include_comments,
            formatting=include_formatting,
            links=include_links,
            images=include_images,
            tables=include_tables,
            dedup=deduplicate,
            lang=target_language,
            url=url,
            with_metadata=with_metadata,
            only_with_metadata=only_with_metadata,
            tei_validation=tei_validation,
            author_blacklist=author_blacklist,
            url_blacklist=url_blacklist,
            date_params=date_extraction_params,
        )

    # extraction
    document = bare_extraction(
        filecontent,
        options=options,
        as_dict=False,
        prune_xpath=prune_xpath,
    )

    # post-processing
    if not document or not isinstance(document, Document):
        return None

    if options.format not in TXT_FORMATS:
        # control output
        if options.format == "python":
            raise ValueError("'python' format only usable in bare_extraction() function")
        # add record ID to metadata
        document.id = record_id
        # calculate fingerprint
        if document.raw_text is not None:
            document.fingerprint = content_fingerprint(str(document.title) + " " + str(document.raw_text))

    # return
    document.text = determine_returnstring(document, options)
    return document
