"""
Unit tests for the metadata parts.
"""

import logging
import sys

from lxml import html
from lxml.etree import XPath

from trafilatura.metadata import check_authors, extract_metadata, extract_metainfo, extract_title, extract_url, normalize_tags

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_titles():
    """Test the extraction of titles"""
    tests = [
        ('<html><body><h3 class="title">T</h3><h3 id="title"></h3></body></html>', None),
        (
            '<html><head><title>Test Title</title><meta property="og:title" content=" " /></head><body><h1>First</h1></body></html>',
            "First",
        ),
        (
            '<html><head><title>Test Title</title><meta name="title" content=" " /></head><body><h1>First</h1></body></html>',
            "First",
        ),
        ("<html><head><title>Test Title</title></head><body></body></html>", "Test Title"),
        ("<html><body><h1>First</h1><h1>Second</h1></body></html>", "First"),
        ('<html><body><h1>   </h1><div class="post-title">Test Title</div></body></html>', "Test Title"),
        (
            '<html><body><h2 class="block-title">Main menu</h2><h1 class="article-title">Test Title</h1></body></html>',
            "Test Title",
        ),
        ("<html><body><h2>First</h2><h1>Second</h1></body></html>", "Second"),
        ("<html><body><h2>First</h2><h2>Second</h2></body></html>", "First"),
        ("<html><body><title></title></body></html>", None),
        # head title is preferred over h1s when it exists and is not a domain
        (
            "<html><head><title>Head Title</title></head><body><h1>First</h1><h1>Second</h1></body></html>",
            "Head Title",
        ),
        # domain-like head titles are ignored, falling back to the first h1
        (
            "<html><head><title>example.com</title></head><body><h1>First</h1><h1>Second</h1></body></html>",
            "First",
        ),
        # the first non-empty h1 is used when earlier h1s are blank
        ("<html><body><h1>   </h1><h1>Real Title</h1></body></html>", "Real Title"),
        # all-blank h1s fall through to nothing
        ("<html><body><h1>   </h1><h1>   </h1></body></html>", None),
    ]

    for doc, expected_title in tests:
        metadata = extract_metadata(doc)
        assert metadata.title == expected_title

    metadata = extract_metadata(r"""<html><body><script type="application/ld+json">{"@context":"https:\/\/schema.org","@type":"Article","name":"Semantic satiation","url":"https:\/\/en.wikipedia.org\/wiki\/Semantic_satiation","sameAs":"http:\/\/www.wikidata.org\/entity\/Q226007","mainEntity":"http:\/\/www.wikidata.org\/entity\/Q226007","author":{"@type":"Organization","name":"Contributors to Wikimedia projects"},"publisher":{"@type":"Organization","name":"Wikimedia Foundation, Inc.","logo":{"@type":"ImageObject","url":"https:\/\/www.wikimedia.org\/static\/images\/wmf-hor-googpub.png"}},"datePublished":"2006-07-12T09:27:14Z","dateModified":"2020-08-31T23:55:26Z","headline":"psychological phenomenon in which repetition causes a word to temporarily lose meaning for the listener"}</script>
<script>(RLQ=window.RLQ||[]).push(function(){mw.config.set({"wgBackendResponseTime":112,"wgHostname":"mw2373"});});</script></html>""")
    assert metadata.title == "Semantic satiation"
    metadata = extract_metadata("<html><head><title> - Home</title></head><body/></html>")
    assert metadata.title == "- Home"
    metadata = extract_metadata("<html><head><title>My Title » My Website</title></head><body/></html>")
    assert metadata.title == "My Title"  # TODO: and metadata.sitename == "My Website"


def test_author_blacklist():
    """Filtering of author names against a blacklist"""
    metadata = extract_metadata(
        '<html><head><meta itemprop="author" content="Jenny Smith"/></head><body></body></html>',
        author_blacklist={"Jenny Smith"},
    )
    assert metadata.author is None
    # a JSON-LD author is filtered (first check, before the markup fallback)
    metadata = extract_metadata(
        '<html><body><script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","author":{"name":"Jane Doe"}}</script></body></html>',
        author_blacklist={"Jane Doe"},
    )
    assert metadata.author is None
    # a markup-extracted author is filtered on the recheck pass
    metadata = extract_metadata('<html><body><a class="author">Jane Doe</a></body></html>', author_blacklist={"Jane Doe"})
    assert metadata.author is None
    # a single-word meta author is discarded
    assert extract_metadata('<html><head><meta name="author" content="Cher"/></head><body/></html>').author is None
    blacklist = {"A", "b"}
    assert check_authors("a; B; c; d", blacklist) == "c; d"
    assert check_authors("a;B;c;d", blacklist) == "c; d"


def test_author_from_meta():
    """Author extraction from <head> meta tags"""
    begin, end = "<html><head>", "</head><body></body></html>"
    cases = [
        (f'{begin}<meta itemprop="author" content="Jenny Smith"/>{end}', "Jenny Smith"),
        (
            f'{begin}<meta itemprop="author" content="Jenny Smith"/><meta itemprop="author" content="John Smith"/>{end}',
            "Jenny Smith; John Smith",
        ),
        (f'{begin}<meta itemprop="author" content="Jenny Smith und John Smith"/>{end}', "Jenny Smith; John Smith"),
        (
            f'{begin}<meta name="author" content="Jenny Smith"/><meta name="author" content="John Smith"/>{end}',
            "Jenny Smith; John Smith",
        ),
        (f'{begin}<meta name="author" content="Jenny Smith and John Smith"/>{end}', "Jenny Smith; John Smith"),
        (f'{begin}<meta name="author" content="Jenny Smith"/>{end}', "Jenny Smith"),
        (f'{begin}<meta name="author" content="Hank O&#39;Hop"/>{end}', "Hank O'Hop"),
        (f'{begin}<meta name="author" content="Jenny Smith ❤️"/>{end}', "Jenny Smith"),
        (f'{begin}<meta name="citation_author" content="Jenny Smith and John Smith"/>{end}', "Jenny Smith; John Smith"),
        (
            f'{begin}<meta property="author" content="Jenny Smith"/><meta property="author" content="John Smith"/>{end}',
            "Jenny Smith; John Smith",
        ),
        (f'{begin}<meta itemprop="author" content="Jenny Smith and John Smith"/>{end}', "Jenny Smith; John Smith"),
        (f'{begin}<meta name="article:author" content="Jenny Smith"/>{end}', "Jenny Smith"),
    ]
    for doc, expected in cases:
        assert extract_metadata(doc).author == expected


def test_author_from_markup():
    """Author extraction from body markup"""
    begin, end = "<html><body>", "</body></html>"
    cases = [
        (f'{begin}<a href="" rel="author">Jenny Smith</a>{end}', "Jenny Smith"),
        (f'{begin}<a href="" rel="author">Jenny "The Author" Smith</a>{end}', "Jenny Smith"),
        (f'{begin}<span class="author">Jenny Smith</span>{end}', "Jenny Smith"),
        (f'{begin}<h4 class="author">Jenny Smith</h4>{end}', "Jenny Smith"),
        (f'{begin}<h4 class="author">Jenny Smith — Trafilatura</h4>{end}', "Jenny Smith"),
        (f'{begin}<span class="wrapper--detail__writer">Jenny Smith</span>{end}', "Jenny Smith"),
        (f'{begin}<span id="author-name">Jenny Smith</span>{end}', "Jenny Smith"),
        (f'{begin}<figure data-component="Figure"><div class="author">Jenny Smith</div></figure>{end}', None),
        (f'{begin}<div class="sidebar"><div class="author">Jenny Smith</div></figure>{end}', None),
        (
            f'{begin}<div class="quote"><p>My quote here</p><p class="quote-author"><span>—</span> Jenny Smith</p></div>{end}',
            None,
        ),
        (f'{begin}<span class="author">Jenny Smith and John Smith</span>{end}', "Jenny Smith; John Smith"),
        (f'{begin}<a class="author">Jenny Smith</a>{end}', "Jenny Smith"),
        (f'{begin}<a class="author">Jenny Smith <div class="title">Editor</div></a>{end}', "Jenny Smith"),
        (f'{begin}<a class="author">Jenny Smith from Trafilatura</a>{end}', "Jenny Smith"),
        (
            f'{begin}<meta itemprop="author" content="Fake Author"/><a class="author">Jenny Smith from Trafilatura</a>{end}',
            "Jenny Smith",
        ),
        (f'{begin}<a class="username">Jenny Smith</a>{end}', "Jenny Smith"),
        (f'{begin}<div class="submitted-by"><a>Jenny Smith</a></div>{end}', "Jenny Smith"),
        (
            f'{begin}<div class="byline-content"><div class="byline"><a>Jenny Smith</a></div><time>July 12, 2021 08:05</time></div>{end}',
            "Jenny Smith",
        ),
        (f'{begin}<h3 itemprop="author">Jenny Smith</h3>{end}', "Jenny Smith"),
        (
            f'{begin}<div class="article-meta article-meta-byline article-meta-with-photo article-meta-author-and-reviewer" itemprop="author" itemscope="" itemtype="http://schema.org/Person"><span class="article-meta-photo-wrap"><img src="" alt="Jenny Smith" itemprop="image" class="article-meta-photo"></span><span class="article-meta-contents"><span class="article-meta-author">By <a href="" itemprop="url"><span itemprop="name">Jenny Smith</span></a></span><span class="article-meta-date">May 18 2022</span><span class="article-meta-reviewer">Reviewed by <a href="">Robert Smith</a></span></span></div>{end}',
            "Jenny Smith",
        ),
        (f'{begin}<div data-component="Byline">Jenny Smith</div>{end}', "Jenny Smith"),
        (f'{begin}<span id="author">Jenny Smith</span>{end}', "Jenny Smith"),
        (f'{begin}<span id="author">Jenny Smith – The Moon</span>{end}', "Jenny Smith"),
        (f'{begin}<span id="author">Jenny_Smith</span>{end}', "Jenny Smith"),
        (
            f'{begin}<span itemprop="author name">Shannon Deery, Mitch Clarke, Susie O’Brien, Laura Placella, Kara Irving, Jordy Atkinson, Suzan Delibasic</span>{end}',
            "Shannon Deery; Mitch Clarke; Susie O’Brien; Laura Placella; Kara Irving; Jordy Atkinson; Suzan Delibasic",
        ),
        (f'{begin}<address class="author">Jenny Smith</address>{end}', "Jenny Smith"),
        (f"{begin}<author>Jenny Smith</author>{end}", "Jenny Smith"),
        (
            f'<html><head><meta data-rh="true" property="og:author" content="By &lt;a href=&quot;/profiles/amir-vera&quot;&gt;Amir Vera&lt;/a&gt;, Seán Federico O&#x27;Murchú, &lt;a href=&quot;/profiles/tara-subramaniam&quot;&gt;Tara Subramaniam&lt;/a&gt; and Adam Renton, CNN"/></head><body>{end}',
            "Amir Vera; Seán Federico O'Murchú; Tara Subramaniam; Adam Renton; CNN",
        ),
        (
            f'{begin}<div class="author"><span class="profile__name"> Jenny Smith </span> <a href="https://twitter.com/jenny_smith" class="profile__social" target="_blank"> @jenny_smith </a> <span class="profile__extra lg:hidden"> 11:57AM </span> </div>{end}',
            "Jenny Smith",
        ),
        (
            f'{begin}<p class="author-section byline-plain">By <a class="author" rel="nofollow">Jenny Smith For Daily Mail Australia</a></p>{end}',
            "Jenny Smith",
        ),
        (
            f'{begin}<div class="o-Attribution__a-Author"><span class="o-Attribution__a-Author--Label">By:</span><span class="o-Attribution__a-Author--Prefix"><span class="o-Attribution__a-Name"><a href="//web.archive.org/web/20210707074846/https://www.discovery.com/profiles/ian-shive">Ian Shive</a></span></span></div>{end}',
            "Ian Shive",
        ),
        (
            f'{begin}<div class="ArticlePage-authors"><div class="ArticlePage-authorName" itemprop="name"><span class="ArticlePage-authorBy">By&nbsp;</span><a aria-label="Ben Coxworth" href="https://newatlas.com/author/ben-coxworth/"><span>Ben Coxworth</span></a></div></div>{end}',
            "Ben Coxworth",
        ),
        (
            f'{begin}<div><strong><a class="d1dba0c3091a3c30ebd6" data-testid="AuthorURL" href="/by/p535y1">AUTHOR NAME</a></strong></div>{end}',
            "AUTHOR NAME",
        ),
    ]
    for doc, expected in cases:
        assert extract_metadata(doc).author == expected


def test_url():
    """Test URL extraction"""
    expected = "https://example.org"
    cases = [
        ('<html><head><meta property="og:url" content="https://example.org"/></head><body></body></html>', None),
        ('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>', None),
        ('<html><head><meta name="twitter:url" content="https://example.org"/></head><body></body></html>', None),
        (
            '<html><head><link rel="alternate" hreflang="x-default" href="https://example.org"/></head><body></body></html>',
            None,
        ),
        (
            '<html><head><link rel="canonical" href="/article/medical-record"/></head><body></body></html>',
            "https://example.org",
        ),
        ('<html><head><base href="https://example.org" target="_blank"/></head><body></body></html>', None),
    ]
    for doc, default_url in cases:
        assert extract_metadata(doc, default_url).url == expected

    # relative canonical joined via a twitter:url or og:url base
    assert (
        extract_url(
            html.fromstring(
                '<html><head><link rel="canonical" href="/article/medical-record"/><meta name="twitter:url" content="https://example.org"/></head><body></body></html>'
            )
        )
        == "https://example.org/article/medical-record"
    )
    assert (
        extract_url(
            html.fromstring(
                '<html><head><link rel="canonical" href="/p"/><meta property="og:url" content="https://example.org"/></head><body></body></html>'
            )
        )
        == "https://example.org/p"
    )


def test_description():
    """Test the extraction of descriptions"""
    metadata = extract_metadata('<html><head><meta itemprop="description" content="Description"/></head><body></body></html>')
    assert metadata.description == "Description"
    metadata = extract_metadata(
        '<html><head><meta property="og:description" content="&amp;#13; A Northern Territory action plan, which includes plans to support development and employment on Aboriginal land, has received an update. &amp;#13..." /></head><body></body></html>'
    )
    assert (
        metadata.description
        == "A Northern Territory action plan, which includes plans to support development and employment on Aboriginal land, has received an update. ..."
    )


def test_dates():
    """Simple tests for date extraction (most of the tests are carried out externally for htmldate module)"""
    tests = [
        (
            '<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>',
            "2017-09-01",
            False,
        ),
        (
            '<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>',
            "2017-09-01",
            False,
        ),
        (
            '<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>',
            "2017-09-01",
            False,
        ),
        ("<html><body><p>Veröffentlicht am 1.9.17</p></body></html>", "2017-09-01", True),
        ("<html><body><p>Veröffentlicht am 1.9.17</p></body></html>", "2017-09-01", False),
    ]

    for doc, expected, extensive in tests:
        metadata = extract_metadata(doc, extensive=extensive)
        assert metadata.date == expected


def test_sitename():
    """Test extraction of site name"""
    tests = [
        ('<html><head><meta name="article:publisher" content="@"/></head><body/></html>', None),
        ('<html><head><meta name="article:publisher" content="The Newspaper"/></head><body/></html>', "The Newspaper"),
        ('<html><head><meta property="article:publisher" content="The Newspaper"/></head><body/></html>', "The Newspaper"),
        ("<html><head><title>sitemaps.org - Home</title></head><body/></html>", "sitemaps.org"),
        # fallback: derive the site name from the URL host
        (
            '<html><head><meta property="og:url" content="https://www.example.org/article"/></head><body/></html>',
            "example.org",
        ),
        # backup site name from application-name
        ('<html><head><meta name="application-name" content="MySite"/></head><body/></html>', "MySite"),
        # a no-dot lowercase publisher is title-cased
        ('<html><head><meta name="article:publisher" content="newspaper"/></head><body/></html>', "Newspaper"),
    ]

    for doc, expected in tests:
        metadata = extract_metadata(doc)
        assert metadata.sitename == expected


def test_meta():
    """Test extraction out of meta-elements"""
    doc = html.fromstring("<html><p class='test'>a</p><p class='other'>b</p><p type='this'>cde</p></html>")
    assert extract_metainfo(doc, [XPath(".//p[@class]")]) is None
    assert extract_metainfo(doc, [XPath(".//p[@type]")]) == "cde"

    metadata = extract_metadata(
        '<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/><meta property="og:site_name" content="My first site"/><meta property="og:url" content="https://example.org/test"/><meta property="og:type" content="Open Graph Type"/></head><body><a rel="license" href="https://creativecommons.org/">Creative Commons</a></body></html>'
    )
    assert metadata.pagetype == "Open Graph Type"
    assert metadata.title == "Open Graph Title"
    assert metadata.author == "Jenny Smith"
    assert metadata.description == "This is an Open Graph description"
    assert metadata.sitename == "My first site"
    assert metadata.url == "https://example.org/test"
    assert metadata.license == "Creative Commons"

    # all OpenGraph fields present -> early return before the meta loop
    metadata = extract_metadata(
        '<html><head><meta property="og:title" content="T"/><meta property="og:author" content="A B"/><meta property="og:url" content="https://e.org"/><meta property="og:description" content="D"/><meta property="og:site_name" content="S"/><meta property="og:image" content="https://e.org/i.jpg"/></head><body/></html>'
    )
    assert metadata.title == "T" and metadata.image == "https://e.org/i.jpg"

    metadata = extract_metadata(
        '<html><head><meta name="dc.title" content="Open Graph Title"/><meta name="dc.creator" content="Jenny Smith"/><meta name="dc.description" content="This is an Open Graph description"/></head><body></body></html>'
    )
    assert metadata.title == "Open Graph Title"
    assert metadata.author == "Jenny Smith"
    assert metadata.description == "This is an Open Graph description"

    metadata = extract_metadata('<html><head><meta itemprop="headline" content="Title"/></head><body></body></html>')
    assert metadata.title == "Title"

    # catch errors
    metadata = extract_metadata("")
    target_slots = set(metadata.__slots__) - {"body", "commentsbody"}
    assert all(getattr(metadata, a) is None for a in target_slots)
    metadata = extract_metadata("<html><title></title></html>")
    assert metadata.sitename is None
    metadata = extract_metadata("<html><head><title>" + "AAA" * 10000 + "</title></head></html>")
    assert metadata.title.endswith("…") and len(metadata.title) == 10000
    assert extract_metadata('<html><head><meta otherkey="example" content="Unknown text"/></head></html>').title is None
    assert extract_metadata("<html><head><title></title><title></title><title></title></head></html>").title is None
    assert extract_metadata('<html><body><script type="application/ld+json"></script></body></html>').title is None


def test_catstags():
    """Test extraction of categories and tags"""
    assert normalize_tags("   ") == ""
    assert normalize_tags(" 1 &amp; 2 ") == "1 & 2"

    cases = [
        (
            '<html><body><p class="entry-categories"><a href="https://example.org/category/cat1/">Cat1</a>, <a href="https://example.org/category/cat2/">Cat2</a></p></body></html>',
            "categories",
            ["Cat1", "Cat2"],
        ),
        (
            '<html><body><div class="postmeta"><a href="https://example.org/category/cat1/">Cat1</a></div></body></html>',
            "categories",
            ["Cat1"],
        ),
        (
            '<html><body><p class="entry-tags"><a href="https://example.org/tags/tag1/">Tag1</a>, <a href="https://example.org/tags/tag2/">Tag2</a></p></body></html>',
            "tags",
            ["Tag1", "Tag2"],
        ),
        (
            '<html><head><meta name="keywords" content="sodium, salt, paracetamol, blood, pressure, high, heart, &amp;quot, intake, warning, study, &amp;quot, medicine, dissolvable, cardiovascular" /></head></html>',
            "tags",
            [
                "sodium, salt, paracetamol, blood, pressure, high, heart, intake, warning, study, medicine, dissolvable, cardiovascular"
            ],
        ),
        # plural "/categories/" in the href must be recognised
        (
            '<html><body><p class="entry-categories"><a href="https://example.org/categories/cat1/">Cat1</a></p></body></html>',
            "categories",
            ["Cat1"],
        ),
        # article:tag meta -> tags
        ('<html><head><meta property="article:tag" content="Sports"/></head><body/></html>', "tags", ["Sports"]),
        # category fallback via article:section meta (no category links)
        ('<html><head><meta property="article:section" content="Politics"/></head><body/></html>', "categories", ["Politics"]),
    ]
    for doc, attr, expected in cases:
        assert getattr(extract_metadata(doc), attr) == expected


def test_date_config():
    "A user date_config without 'max_date' must not raise, and must not be mutated."
    cfg = {"original_date": True, "extensive_search": False}
    doc = "<html><head><title>T</title></head><body><p>x</p></body></html>"
    assert extract_metadata(doc, date_config=cfg) is not None
    assert "url" not in cfg


def test_extract_title_fallbacks():
    "Fallback titles are trimmed; nothing found returns None."
    assert extract_title(html.fromstring("<html><body><h1>  A  </h1><h1>B</h1></body></html>")) == "A"
    assert extract_title(html.fromstring("<html><body><p>x</p></body></html>")) is None


def test_license():
    """Test extraction of CC licenses"""
    # a rel
    metadata = extract_metadata(
        '<html><body><p><a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="license">CC BY-SA</a></p></body></html>'
    )
    assert metadata.license == "CC BY-SA 4.0"
    metadata = extract_metadata(
        '<html><body><p><a href="https://licenses.org/unknown" rel="license">Unknown</a></p></body></html>'
    )
    assert metadata.license == "Unknown"
    # footer
    metadata = extract_metadata(
        '<html><body><footer><a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA</a></footer></body></html>'
    )
    assert metadata.license == "CC BY-SA 4.0"
    # footer: netzpolitik.org
    metadata = extract_metadata("""<html><body>
<div class="footer__navigation">
<p class="footer__licence">
            <strong>Lizenz: </strong>
            Die von uns verfassten Inhalte stehen, soweit nicht anders vermerkt, unter der Lizenz
            <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons BY-NC-SA 4.0.</a>
        </p>
    </div>
</body></html>""")
    assert metadata.license == "CC BY-NC-SA 4.0"
    # this is not a license
    metadata = extract_metadata("""<html><body><footer class="entry-footer">
	<span class="cat-links">Posted in <a href="https://sallysbakingaddiction.com/category/seasonal/birthday/" rel="category tag">Birthday</a></span>
	</footer></body></html>""")
    assert metadata.license is None
    # this is a license
    metadata = extract_metadata("""<html><body><footer class="entry-footer">
	<span>The license is <a href="https://example.org/1">CC BY-NC</a></span>
	</footer></body></html>""")
    assert metadata.license == "CC BY-NC"
    # license text wrapped in nested markup (text_content, not .text)
    metadata = extract_metadata('<html><body><footer><a href="/x"><span>CC BY-SA 4.0</span></a></footer></body></html>')
    assert metadata.license == "CC BY-SA 4.0"
    # a rel=license link with no href/text cue yields no license
    metadata = extract_metadata('<html><body><p><a rel="license" href="/x"></a></p></body></html>')
    assert metadata.license is None


def test_images():
    """Image extraction from meta SEO tags"""
    cases = [
        (
            '<html><head><meta property="image" content="https://example.org/example.jpg"></html>',
            "https://example.org/example.jpg",
        ),
        ('<html><head><meta property="og:image:url" content="example.jpg"></html>', "example.jpg"),
        (
            '<html><head><meta property="og:image" content="https://example.org/example-opengraph.jpg" /><body/></html>',
            "https://example.org/example-opengraph.jpg",
        ),
        (
            '<html><head><meta property="twitter:image" content="https://example.org/example-twitter.jpg"></html>',
            "https://example.org/example-twitter.jpg",
        ),
        ('<html><head><meta property="twitter:image:src" content="example-twitter.jpg"></html>', "example-twitter.jpg"),
        (
            '<html><head><meta name="twitter:image" content="https://example.org/example-name.jpg"></html>',
            "https://example.org/example-name.jpg",
        ),
        (
            '<html><head><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" /></html>',
            None,
        ),
    ]
    for doc, expected in cases:
        assert extract_metadata(doc).image == expected


def test_document_as_dict():
    """Tests that the dict serialization works and preserves data."""

    htmldoc = """
    <html>
    <head>
        <title>Test Title</title>
        <meta itemprop="author" content="Jenny Smith" />
        <meta property="og:url" content="https://example.org" />
        <meta itemprop="description" content="Description" />
        <meta property="og:published_time" content="2017-09-01" />
        <meta name="article:publisher" content="The Newspaper" />
        <meta property="image" content="https://example.org/example.jpg" />
    </head>
    <body>
        <p class="entry-categories">
        <a href="https://example.org/category/cat1/">Cat1</a>,
        <a href="https://example.org/category/cat2/">Cat2</a>
        </p>
        <p>
        <a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="license"
            >CC BY-SA</a
        >
        </p>
    </body>
    </html>
    """

    document = extract_metadata(htmldoc)
    dict_ = document.as_dict()
    assert dict_["title"] == "Test Title"
    assert dict_["author"] == "Jenny Smith"
    assert dict_["url"] == "https://example.org"
    assert dict_["description"] == "Description"
    assert dict_["sitename"] == "The Newspaper"
    assert dict_["date"] == "2017-09-01"
    assert dict_["categories"] == ["Cat1", "Cat2"]
    assert dict_["license"] == "CC BY-SA 4.0"
    assert dict_["image"] == "https://example.org/example.jpg"
