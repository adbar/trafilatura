"""
Compare extraction results with other libraries of the same kind.
"""

#import logging
#logging.basicConfig(level=logging.DEBUG)

import html2text
import html_text
import justext
from boilerpy3 import extractors
from bs4 import BeautifulSoup
from goose3 import Goose
from inscriptis import get_text
from newspaper import fulltext
from newsplease import NewsPlease
# from readabilipy import simple_json_from_html_string
from readability import Document
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import bytes_to_str, detect_encoding
from resiliparse.parse.html import HTMLTree

from trafilatura import baseline, extract, html2txt

boilerpipe_extractor = extractors.ArticleExtractor()  # ArticleExtractor DefaultExtractor LargestContentExtractor

g = Goose()


def run_baseline(htmlstring):
    '''run bare text extraction within lxml'''
    _, result, _ = baseline(htmlstring)
    return result


def run_html2txt(htmlstring):
   '''run Trafilatura's html2txt function'''
   return html2txt(htmlstring)


def run_trafilatura(htmlstring):
    '''run trafilatura (without fallback) on content'''
    return extract(
        htmlstring,
        no_fallback=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_justext(htmlstring):
    '''try with the generic algorithm justext'''
    paragraphs = justext.justext(htmlstring, justext.get_stoplist("German"),
                                 50, 200, 0.1, 0.2, 0.2, 200, True)  # stop_words
    valid = [
        paragraph.text
        for paragraph in paragraphs
        if not paragraph.is_boilerplate
    ]

    return ' '.join(valid)   # sanitize(result)


def run_trafilatura_fallback(htmlstring):
    '''run trafilatura (with fallback) on content'''
    return extract(
        htmlstring,
        no_fallback=False,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_trafilatura_precision(htmlstring):
    '''run trafilatura with preference for precision'''
    return extract(
        htmlstring,
        no_fallback=False,
        favor_precision=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_trafilatura_recall(htmlstring):
    '''run trafilatura with preference for recall'''
    return extract(
        htmlstring,
        no_fallback=False,
        favor_recall=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_goose(htmlstring):
    '''try with the goose algorithm'''
    try:
        article = g.extract(raw_html=htmlstring)
        return article.cleaned_text  # sanitize(article.cleaned_text)
    except ValueError:
        return ''


def run_readability(htmlstring):
    '''try with the Python3 port of readability.js'''
    try:
        doc = Document(htmlstring)
        return doc.summary()  # sanitize(doc.summary())
    except Exception as err:
        print('Exception:', err)
        return ''

def run_inscriptis(htmlstring):
    '''try with the inscriptis module'''
    try:
        text = get_text(htmlstring)
    except TypeError:
        text = ''
    return text # sanitize(text)


def run_html2text(htmlstring):
    '''try with the html2text module'''
    try:
        text = html2text.html2text(htmlstring)
        # sanitize(text)
    except TypeError:
        text = ''
    return text


def run_html_text(htmlstring):
    '''try with the html2text module'''
    try:
        text = html_text.extract_text(htmlstring, guess_layout=False)
    except TypeError:
        text = ''
    return text


def run_newspaper(htmlstring):
    '''try with the newspaper module'''
    try:
        text = fulltext(htmlstring)  # sanitize(fulltext(htmlstring))
    except AttributeError:
        return ''
    return text


def run_boilerpipe(htmlstring):
    '''try with the boilerpipe algorithm'''
    try:
        content = boilerpipe_extractor.get_content(htmlstring)
        # sanitize(boilerpipe_extractor.get_content(htmlstring))
    except Exception:
        content = ''
    return content


def run_newsplease(htmlstring):
    '''try with newsplease'''
    try:
        article = NewsPlease.from_html(htmlstring, url=None)
        return article.maintext # sanitize(article.maintext)
    except Exception as err:
        #print('Newsplease exception:', err)
        return ''


#def run_readabilipy(htmlstring):
#    '''try with the readability.py module'''
#    try:
#        article = simple_json_from_html_string(htmlstring, use_readability=True)
#        returnlist = [textelem['text'] for textelem in article['plain_text']]
#        return '\n'.join(returnlist) # sanitize(content)
#    except Exception as err:
#        #print('Readabilipy exception:', err)
#        return ''


def run_resiliparse(htmlstring):
    '''try with the resiliparse package'''
    try:
        decoded = bytes_to_str(htmlstring, detect_encoding(htmlstring))
    except TypeError:  # already a string
        decoded = htmlstring
    tree = HTMLTree.parse(decoded)
    return extract_plain_text(tree, main_content=True)


def run_bs4(htmlstring):
    '''try with the BeautifulSoup module'''
    return BeautifulSoup(htmlstring, features='lxml').get_text(strip=True)


def run_nothing(htmlstring):
    return ''


def run_everything(htmlstring):
    return htmlstring
