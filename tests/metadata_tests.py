"""
Unit tests for the metadata parts.
"""


import logging
import sys

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

from lxml import html

from trafilatura.json_metadata import normalize_json
from trafilatura.metadata import extract_metadata, extract_meta_json, extract_url
from trafilatura.utils import normalize_authors

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_titles():
    '''Test the extraction of titles'''
    # too short/empty
    metadata = extract_metadata('<html><body><h3 class="title">T</h3><h3 id="title"></h3></body></html>')
    assert metadata.title is None
    
    metadata = extract_metadata('<html><head><title>Test Title</title></head><body></body></html>')
    assert metadata.title == 'Test Title'
    metadata = extract_metadata('<html><body><h1>First</h1><h1>Second</h1></body></html>')
    assert metadata.title == 'First'
    metadata = extract_metadata('<html><body><h1>   </h1><div class="post-title">Test Title</div></body></html>')
    assert metadata.title == 'Test Title'
    metadata = extract_metadata('<html><body><h2 class="block-title">Main menu</h2><h1 class="article-title">Test Title</h1></body></html>')
    assert metadata.title == 'Test Title'
    metadata = extract_metadata('<html><body><h2>First</h2><h1>Second</h1></body></html>')
    assert metadata.title == 'Second'
    metadata = extract_metadata('<html><body><h2>First</h2><h2>Second</h2></body></html>')
    assert metadata.title == 'First'
    metadata = extract_metadata('<html><body><title></title></body></html>')
    assert metadata.title is None
    metadata = extract_metadata(r'''<html><body><script type="application/ld+json">{"@context":"https:\/\/schema.org","@type":"Article","name":"Semantic satiation","url":"https:\/\/en.wikipedia.org\/wiki\/Semantic_satiation","sameAs":"http:\/\/www.wikidata.org\/entity\/Q226007","mainEntity":"http:\/\/www.wikidata.org\/entity\/Q226007","author":{"@type":"Organization","name":"Contributors to Wikimedia projects"},"publisher":{"@type":"Organization","name":"Wikimedia Foundation, Inc.","logo":{"@type":"ImageObject","url":"https:\/\/www.wikimedia.org\/static\/images\/wmf-hor-googpub.png"}},"datePublished":"2006-07-12T09:27:14Z","dateModified":"2020-08-31T23:55:26Z","headline":"psychological phenomenon in which repetition causes a word to temporarily lose meaning for the listener"}</script>
<script>(RLQ=window.RLQ||[]).push(function(){mw.config.set({"wgBackendResponseTime":112,"wgHostname":"mw2373"});});</script></html>''')
    assert metadata.title == 'Semantic satiation'
    metadata = extract_metadata('<html><head><title> - Home</title></head><body/></html>')
    assert metadata.title == '- Home'
    metadata = extract_metadata('<html><head><title>My Title » My Website</title></head><body/></html>')
    assert metadata.title == "My Title"  # TODO: and metadata.sitename == "My Website"


def test_authors():
    '''Test the extraction of author names'''
    # normalization
    assert normalize_authors(None, 'abc') == 'Abc'
    assert normalize_authors(None, 'Steve Steve 123') == 'Steve Steve'
    assert normalize_authors(None, 'By Steve Steve') == 'Steve Steve'
    assert normalize_json('Test \\nthis') == 'Test this'
    # blacklist
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith"/></head><body></body></html>', author_blacklist={'Jenny Smith'})
    assert metadata.author is None
    # extraction
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith"/><meta itemprop="author" content="John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith und John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith"/><meta name="author" content="John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith and John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Hank O&#39;Hop"/></head><body></body></html>')
    assert metadata.author == 'Hank O\'Hop'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith ❤️"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><head><meta name="citation_author" content="Jenny Smith and John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta property="author" content="Jenny Smith"/><meta property="author" content="John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith and John Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="article:author" content="Jenny Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a href="" rel="author">Jenny Smith</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a href="" rel="author">Jenny "The Author" Smith</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span class="author">Jenny Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><h4 class="author">Jenny Smith</h4></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><h4 class="author">Jenny Smith — Trafilatura</h4></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span class="wrapper--detail__writer">Jenny Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span id="author-name">Jenny Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><figure data-component="Figure"><div class="author">Jenny Smith</div></figure></body></html>')
    assert metadata.author is None
    metadata = extract_metadata('<html><body><div class="sidebar"><div class="author">Jenny Smith</div></figure></body></html>')
    assert metadata.author is None
    metadata = extract_metadata('<html><body><div class="quote"><p>My quote here</p><p class="quote-author"><span>—</span> Jenny Smith</p></div></body></html>')
    assert metadata.author is None
    metadata = extract_metadata('<html><body><span class="author">Jenny Smith and John Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><body><a class="author">Jenny Smith</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a class="author">Jenny Smith <div class="title">Editor</div></a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a class="author">Jenny Smith from Trafilatura</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><meta itemprop="author" content="Fake Author"/><a class="author">Jenny Smith from Trafilatura</a></body></html>', author_blacklist={'Fake Author'})
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a class="username">Jenny Smith</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="submitted-by"><a>Jenny Smith</a></div></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="byline-content"><div class="byline"><a>Jenny Smith</a></div><time>July 12, 2021 08:05</time></div></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><h3 itemprop="author">Jenny Smith</h3></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="article-meta article-meta-byline article-meta-with-photo article-meta-author-and-reviewer" itemprop="author" itemscope="" itemtype="http://schema.org/Person"><span class="article-meta-photo-wrap"><img src="" alt="Jenny Smith" itemprop="image" class="article-meta-photo"></span><span class="article-meta-contents"><span class="article-meta-author">By <a href="" itemprop="url"><span itemprop="name">Jenny Smith</span></a></span><span class="article-meta-date">May 18 2022</span><span class="article-meta-reviewer">Reviewed by <a href="">Robert Smith</a></span></span></div></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div data-component="Byline">Jenny Smith</div></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span id="author">Jenny Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span id="author">Jenny_Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span itemprop="author name">Shannon Deery, Mitch Clarke, Susie O’Brien, Laura Placella, Kara Irving, Jordy Atkinson, Suzan Delibasic</span></body></html>')
    assert metadata.author == 'Shannon Deery; Mitch Clarke; Susie O’Brien; Laura Placella; Kara Irving; Jordy Atkinson; Suzan Delibasic'
    metadata = extract_metadata('<html><body><address class="author">Jenny Smith</address></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><author>Jenny Smith</author></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="author"><span class="profile__name"> Jenny Smith </span> <a href="https://twitter.com/jenny_smith" class="profile__social" target="_blank"> @jenny_smith </a> <span class="profile__extra lg:hidden"> 11:57AM </span> </div></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><p class="author-section byline-plain">By <a class="author" rel="nofollow">Jenny Smith For Daily Mail Australia</a></p></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="o-Attribution__a-Author"><span class="o-Attribution__a-Author--Label">By:</span><span class="o-Attribution__a-Author--Prefix"><span class="o-Attribution__a-Name"><a href="//web.archive.org/web/20210707074846/https://www.discovery.com/profiles/ian-shive">Ian Shive</a></span></span></div></body></html>')
    assert metadata.author == 'Ian Shive'
    metadata = extract_metadata('<html><body><div class="ArticlePage-authors"><div class="ArticlePage-authorName" itemprop="name"><span class="ArticlePage-authorBy">By&nbsp;</span><a aria-label="Ben Coxworth" href="https://newatlas.com/author/ben-coxworth/"><span>Ben Coxworth</span></a></div></div></body></html>')
    assert metadata.author == 'Ben Coxworth'


def test_url():
    '''Test URL extraction'''
    metadata = extract_metadata('<html><head><meta property="og:url" content="https://example.org"/></head><body></body></html>')
    assert metadata.url == 'https://example.org'
    metadata = extract_metadata('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>')
    assert metadata.url == 'https://example.org'
    metadata = extract_metadata('<html><head><meta name="twitter:url" content="https://example.org"/></head><body></body></html>')
    assert metadata.url == 'https://example.org'
    metadata = extract_metadata('<html><head><link rel="alternate" hreflang="x-default" href="https://example.org"/></head><body></body></html>')
    assert metadata.url == 'https://example.org'
    metadata = extract_metadata('<html><head><link rel="canonical" href="/article/medical-record"/></head><body></body></html>', default_url="https://example.org")
    assert metadata.url == 'https://example.org'
    url = extract_url(html.fromstring('<html><head><link rel="canonical" href="/article/medical-record"/><meta name="twitter:url" content="https://example.org"/></head><body></body></html>'))
    assert url == 'https://example.org/article/medical-record'


def test_description():
    '''Test the extraction of descriptions'''
    metadata = extract_metadata('<html><head><meta itemprop="description" content="Description"/></head><body></body></html>')
    assert metadata.description == 'Description'
    metadata = extract_metadata('<html><head><meta property="og:description" content="&amp;#13; A Northern Territory action plan, which includes plans to support development and employment on Aboriginal land, has received an update. &amp;#13..." /></head><body></body></html>')
    assert metadata.description == 'A Northern Territory action plan, which includes plans to support development and employment on Aboriginal land, has received an update. ...'


def test_dates():
    '''Simple tests for date extraction (most of the tests are carried out externally for htmldate module)'''
    metadata = extract_metadata('<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>')
    assert metadata.date == '2017-09-01'
    metadata = extract_metadata('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    assert metadata.date == '2017-09-01'
    metadata = extract_metadata('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    assert metadata.date == '2017-09-01'
    mystring = '<html><body><p>Veröffentlicht am 1.9.17</p></body></html>'
    metadata = extract_metadata(mystring, fastmode=False)
    assert metadata.date == '2017-09-01'
    metadata = extract_metadata(mystring, fastmode=True)
    assert metadata.date is None


def test_sitename():
    '''Test extraction of site name'''
    metadata = extract_metadata('<html><head><meta name="article:publisher" content="@"/></head><body/></html>')
    assert metadata.sitename is None
    metadata = extract_metadata('<html><head><meta name="article:publisher" content="The Newspaper"/></head><body/></html>')
    assert metadata.sitename == 'The Newspaper'
    metadata = extract_metadata('<html><head><meta property="article:publisher" content="The Newspaper"/></head><body/></html>')
    assert metadata.sitename == 'The Newspaper'
    metadata = extract_metadata('<html><head><title>sitemaps.org - Home</title></head><body/></html>')
    assert metadata.sitename == 'sitemaps.org'

def test_meta():
    '''Test extraction out of meta-elements'''
    metadata = extract_metadata('<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/><meta property="og:site_name" content="My first site"/><meta property="og:url" content="https://example.org/test"/></head><body><a rel="license" href="https://creativecommons.org/">Creative Commons</a></body></html>')
    assert metadata.title == 'Open Graph Title'
    assert metadata.author == 'Jenny Smith'
    assert metadata.description == 'This is an Open Graph description'
    assert metadata.sitename == 'My first site'
    assert metadata.url == 'https://example.org/test'
    assert metadata.license == 'Creative Commons'
    metadata = extract_metadata('<html><head><meta name="dc.title" content="Open Graph Title"/><meta name="dc.creator" content="Jenny Smith"/><meta name="dc.description" content="This is an Open Graph description"/></head><body></body></html>')
    assert metadata.title == 'Open Graph Title'
    assert metadata.author == 'Jenny Smith'
    assert metadata.description == 'This is an Open Graph description'
    metadata = extract_metadata('<html><head><meta itemprop="headline" content="Title"/></head><body></body></html>')
    assert metadata.title == 'Title'
    # catch errors
    assert extract_metadata('') is None
    metadata = extract_metadata('<html><title></title></html>')
    assert metadata.sitename is None
    metadata = extract_metadata('<html><head><title>' + 'AAA'*10000 + '</title></head></html>')
    assert metadata.title.endswith('…') and len(metadata.title) == 10000
    assert extract_metadata('<html><head><meta otherkey="example" content="Unknown text"/></head></html>') is not None
    assert extract_metadata('<html><head><title></title><title></title><title></title></head></html>') is not None


def test_catstags():
    '''Test extraction of categories and tags'''
    metadata = extract_metadata('<html><body><p class="entry-categories"><a href="https://example.org/category/cat1/">Cat1</a>, <a href="https://example.org/category/cat2/">Cat2</a></p></body></html>')
    assert metadata.categories == ['Cat1', 'Cat2']
    metadata = extract_metadata('<html><body><div class="postmeta"><a href="https://example.org/category/cat1/">Cat1</a></div></body></html>')
    assert metadata.categories == ['Cat1']
    metadata = extract_metadata('<html><body><p class="entry-tags"><a href="https://example.org/tags/tag1/">Tag1</a>, <a href="https://example.org/tags/tag2/">Tag2</a></p></body></html>')
    assert metadata.tags == ['Tag1', 'Tag2']
    metadata = extract_metadata('<html><head><meta name="keywords" content="sodium, salt, paracetamol, blood, pressure, high, heart, &amp;quot, intake, warning, study, &amp;quot, medicine, dissolvable, cardiovascular" /></head></html>')
    assert metadata.tags == ['sodium, salt, paracetamol, blood, pressure, high, heart, intake, warning, study, medicine, dissolvable, cardiovascular']


def test_license():
    '''Test extraction of CC licenses'''
    # a rel
    metadata = extract_metadata('<html><body><p><a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="license">CC BY-SA</a></p></body></html>')
    assert metadata.license == 'CC BY-SA 4.0'
    metadata = extract_metadata('<html><body><p><a href="https://licenses.org/unknown" rel="license">Unknown</a></p></body></html>')
    assert metadata.license == 'Unknown'
    # footer
    metadata = extract_metadata('<html><body><footer><a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA</a></footer></body></html>')
    assert metadata.license == 'CC BY-SA 4.0'
    # footer: netzpolitik.org
    metadata = extract_metadata('''<html><body>
<div class="footer__navigation">
<p class="footer__licence">
            <strong>Lizenz: </strong>
            Die von uns verfassten Inhalte stehen, soweit nicht anders vermerkt, unter der Lizenz
            <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons BY-NC-SA 4.0.</a>
        </p>
    </div>
</body></html>''')
    assert metadata.license == 'CC BY-NC-SA 4.0'
    # this is not a license
    metadata = extract_metadata('''<html><body><footer class="entry-footer">
	<span class="cat-links">Posted in <a href="https://sallysbakingaddiction.com/category/seasonal/birthday/" rel="category tag">Birthday</a></span>
	</footer></body></html>''')
    assert metadata.license is None
    # this is a license
    metadata = extract_metadata('''<html><body><footer class="entry-footer">
	<span>The license is <a href="https://example.org/1">CC BY-NC</a></span>
	</footer></body></html>''')
    assert metadata.license == 'CC BY-NC'


def test_images():
    '''Image extraction from meta SEO tags'''
    metadata = extract_metadata('<html><head><meta property="image" content="https://example.org/example.jpg"></html>')
    assert metadata.image == 'https://example.org/example.jpg'
    metadata = extract_metadata('<html><head><meta property="og:image" content="https://example.org/example-opengraph.jpg" /><body/></html>')
    assert metadata.image == 'https://example.org/example-opengraph.jpg'
    metadata = extract_metadata('<html><head><meta property="twitter:image" content="https://example.org/example-twitter.jpg"></html>')
    assert metadata.image == 'https://example.org/example-twitter.jpg'



if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()
    test_url()
    test_description()
    test_catstags()
    test_sitename()
    test_license()
    test_images()
