"""
Unit tests for baseline functions of the trafilatura library.
"""

from lxml import html
from trafilatura import baseline, html2txt


def test_baseline():
    # Empty input
    result = baseline(b'')
    assert isinstance(result, tuple) and len(result) == 3
    assert result[0].tag == 'body'
    assert result[1] == ''
    assert result[2] == 0

    result = baseline('')
    assert isinstance(result, tuple) and len(result) == 3
    assert result[0].tag == 'body'
    assert result[1] == ''
    assert result[2] == 0

    # Invalid HTML
    _, result, _ = baseline(b'<invalid html>')
    assert result == ''

    tests = [
        '<html><body><article>' + 'The article consists of this text.'*10 + '</article></body></html>',
        '<html><body><article><b>The article consists of this text.</b></article></body></html>',
        '<html><body><quote>This is only a quote but it is better than nothing.</quote></body></html>',
    ]
    for doc in tests:
        _, result, _ = baseline(doc)
        assert result is not None

    # Invalid JSON
    filecontent = b'''
        <html>
            <body>
                <script type="application/ld+json">
                    {"articleBody": "This is the article body, it has to be long enough to fool the length threshold which is set at len 100."  # invalid JSON
                </script>
            </body>
        </html>
    '''
    _, result, _ = baseline(filecontent)
    assert result == ''

    # JSON OK
    filecontent = b'''
        <html>
            <body>
                <script type="application/ld+json">
                    {
                        "@type": "Article",
                        "articleBody": "This is the article body, it has to be long enough to fool the length threshold which is set at len 100."
                    }
                </script>
            </body>
        </html>
    '''
    _, result, _ = baseline(filecontent)
    assert len(result) > 100

    # JSON malformed
    filecontent = br'''
        <html>
            <body>
                <script type="application/ld+json">
                    {
                        "@type": "Article",
                        "articleBody": "<p>This is the article body, it has to be long enough to fool the length threshold which is set at len 100.<\/p>"
                    }
                </script>
            </body>
        </html>
    '''
    _, result, _ = baseline(filecontent)
    assert result == ''

    # Real-world examples
    my_document = r'<html><body><script type="application/ld+json">{"description":"In letzter Zeit kam man am Begriff \"Hygge\", was so viel wie \"angenehm\" oder \"gemütlich\" bedeutet, ja nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend ...","image":[{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/uncropped-0-0\/7d00b2658fd0a3b19e1b161f4657cc20\/Xw\/ikigai--1-.jpg","width":"2048","height":"1366","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-1280-720\/bf947c7c24167d7c0adae0be10942d57\/Uf\/ikigai--1-.jpg","width":"1280","height":"720","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-938-528\/bf947c7c24167d7c0adae0be10942d57\/JK\/ikigai--1-.jpg","width":"938","height":"528","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/large1x1-622-622\/f5544b7d67e1be04f7729b130e7e0485\/KN\/ikigai--1-.jpg","width":"622","height":"622","@type":"ImageObject"}],"mainEntityOfPage":{"@id":"https:\/\/www.brigitte.de\/liebe\/persoenlichkeit\/ikigai-macht-dich-sofort-gluecklicher--10972896.html","@type":"WebPage"},"headline":"Ikigai macht dich sofort glücklicher!","datePublished":"2019-06-19T14:29:08+0000","dateModified":"2019-06-19T14:29:10+0000","author":{"name":"BRIGITTE.de","@type":"Organization"},"publisher":{"name":"BRIGITTE.de","logo":{"url":"https:\/\/image.brigitte.de\/11476842\/uncropped-0-0\/f19537e97b9189bf0f25ce924168bedb\/kK\/bri-logo-schema-org.png","width":"167","height":"60","@type":"ImageObject"},"@type":"Organization"},"articleBody":"In letzter Zeit kam man am Begriff \"Hygge\" (\"gemütlich\" oder \"angenehm\") nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend Konkurrenz: \"Ikigai\". Bist du glücklich? Schwierige Frage, nicht wahr? Viele von uns müssen da erst mal überlegen.","@type":"NewsArticle"}</script></body></html>'
    _, result, _  = baseline(my_document)
    assert result.startswith('In letzter Zeit kam man') and result.endswith('erst mal überlegen.')

    my_document = "<html><body><div>   Document body...   </div><script> console.log('Hello world') </script></body></html>"
    _, result, _ = baseline(my_document)
    assert result == 'Document body...'


def test_html2txt():
    mydoc = "<html><body>Here is the body text</body></html>"
    assert html2txt(mydoc) == "Here is the body text"
    assert html2txt(html.fromstring(mydoc)) == "Here is the body text"
    assert html2txt("") == ""
    assert html2txt("123") == ""
    assert html2txt("<html></html>") == ""
    assert html2txt("<html><body/></html>") == ""
    assert html2txt("<html><body><style>font-size: 8pt</style><p>ABC</p></body></html>") == "ABC"


if __name__ == '__main__':
    test_baseline()
    test_html2txt()
