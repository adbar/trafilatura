import re
from bs4 import BeautifulSoup
from trafilatura import html2txt

MARKDOWN_FORMATTING_REGEX = re.compile(r"[\*\_\[\]\(\)\~\`\>\#\+\-\=\|\.!\?]")


def remove_markdown_formatting(text):
    """
    Remove Markdown formatting from text
    """
    # Remove Markdown formatting
    text = re.sub(MARKDOWN_FORMATTING_REGEX, "", text)

    return text


def unique_words(text):
    """
    Get unique words from text
    """
    # Split text into words and convert to set to get unique words
    words = re.findall(r"\w+", text.lower())
    unique_words = set(words)

    return unique_words


def unique_words_html(html):
    """
    Get unique words from HTML.
    Remove semantic elements and relative links.
    """
    if not html:
        return 0

    soup = BeautifulSoup(html, "html.parser")

    # Remove semantic elements
    for elem in soup.find_all(["header", "nav", "footer"]):
        elem.decompose()

    # TODO delete relative links or absolute links to the same domain

    plain = html2txt(str(soup))
    plain = remove_markdown_formatting(plain)

    return len(unique_words(plain))


def unique_words_markdown(markdown):
    """
    Get unique word count from Markdown.
    Remove markdown formatting.
    """
    if not markdown:
        return 0

    plain = remove_markdown_formatting(markdown)

    return len(unique_words(plain))


def confidence_score(html, markdown):
    """
    Calculate confidence score between HTML and Markdown
    """
    words_html = unique_words_html(html)
    words_markdown = unique_words_markdown(markdown)

    # TODO add multiple markdowns to compare and use the average count?

    return float(words_markdown) / words_html if words_html > 0 else 0
