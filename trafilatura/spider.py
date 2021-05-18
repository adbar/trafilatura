# pylint:disable-msg=E0611,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging


#from courlan import extract_links
from lxml import etree
#from time import sleep


#from .feeds import determine_feed
#from .settings import LANG, MAX_CRAWLED_PAGES, MAX_URLS_BEFORE_SITECHECK, MAX_PAGES_PER_CRAWLED_SITE, MAX_URLS_TO_CHECK, SLEEPTIME, MIN_PAGES_PER_CRAWLED_SITE
from .utils import decode_response, fetch_url, fix_relative_urls, get_hostinfo, load_html



def refresh_detection(htmlstring, homepage):
    "Check if there could be a redirection by meta-refresh tag."
    if '"refresh"' in htmlstring or '"REFRESH"' in htmlstring:
        try:
            html_tree = load_html(htmlstring)
            # test meta-refresh redirection
            # https://stackoverflow.com/questions/2318446/how-to-follow-meta-refreshes-in-python
            attr = html_tree.xpath('//meta[@http-equiv="refresh"]/@content|//meta[@http-equiv="REFRESH"]/@content')[0]
            _, text = attr.split(';')
            text = text.strip().lower()
            if text.startswith('url=') or text.startswith('URL='):
                url2 = text[4:]
                if not url2.startswith('http'):
                    # Relative URL, adapt
                    _, baseurl = get_hostinfo(url2)
                    url2 = fix_relative_urls(baseurl, url2)
                # second fetch
                newhtmlstring = fetch_url(url2)
                if newhtmlstring is None:
                    logging.warning('failed redirect: %s', url2)
                    return None, None
                #else:
                htmlstring, homepage = newhtmlstring, url2
                logging.info('successful redirect: %s', url2)
        except (IndexError, etree.ParserError, etree.XMLSyntaxError, etree.XPathEvalError) as err:
            logging.info('no redirect found: %s %s', homepage, err)
    return htmlstring, homepage


def probe_alternative_homepage(homepage):
    "Check if the homepage is redirected and return appropriate values."
    response = fetch_url(homepage, decode=False)
    if response is None or response == '':
        return None, None, None
    # get redirected URL here?
    if response.geturl() != homepage:
        logging.info('followed redirect: %s', response.geturl())
        homepage = response.geturl()
    # decode response
    htmlstring = decode_response(response.data)
    # is there a meta-refresh on the page?
    htmlstring, homepage = refresh_detection(htmlstring, homepage)
    logging.info('fetching homepage OK: %s', homepage)
    _, baseurl = get_hostinfo(homepage)
    return htmlstring, homepage, baseurl

