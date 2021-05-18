# pylint:disable-msg=W1401
"""
Unit tests for the spidering part of the trafilatura library.
"""

import logging
import sys


from trafilatura import spider

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_redirections():
    "Test redirection detection."
    _, _, baseurl = spider.probe_alternative_homepage('1234')
    assert baseurl is None
    _, _, baseurl = spider.probe_alternative_homepage('https://httpbin.org/gzip')
    assert baseurl == 'https://httpbin.org'
    #_, _, baseurl = spider.probe_alternative_homepage('https://httpbin.org/redirect-to?url=https%3A%2F%2Fhttpbin.org%2Fhtml&status_code=302')



def test_meta_redirections():
    "Test redirection detection using meta tag."
    htmlstring, homepage = '<html></html>', 'https://httpbin.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage
    htmlstring, homepage = '<html>REDIRECT!</html>', 'https://httpbin.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="0; url=1234"/></html>', 'https://httpbin.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 is None and homepage2 is None
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="0; url=https://httpbin.org/status/200"/></html>', 'http://test.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == '' and homepage2 == 'https://httpbin.org/status/200'



if __name__ == '__main__':
    test_redirections()
    test_meta_redirections()
