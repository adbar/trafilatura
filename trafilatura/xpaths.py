# pylint:disable-msg=E0611
"""
X-Path expressions used to extract or filter the main text content,
and to extract metadata.
"""

from lxml.etree import XPath


### 1. CONTENT


BODY_XPATH = [XPath(x) for x in (
    '''.//*[self::article or self::div or self::main or self::section][
    @class="post" or @class="entry" or
    contains(@class, "post-text") or contains(@class, "post_text") or
    contains(@class, "post-body") or contains(@class, "post-entry") or contains(@class, "postentry") or
    contains(@class, "post-content") or contains(@class, "post_content") or
    contains(@class, "postcontent") or contains(@class, "postContent") or contains(@class, "post_inner_wrapper") or
    contains(@class, "article-text") or contains(@class, "articletext") or contains(@class, "articleText")
    or contains(@id, "entry-content") or
    contains(@class, "entry-content") or contains(@id, "article-content") or
    contains(@class, "article-content") or contains(@id, "article__content") or
    contains(@class, "article__content") or contains(@id, "article-body") or
    contains(@class, "article-body") or contains(@id, "article__body") or
    contains(@class, "article__body") or @itemprop="articleBody" or
    contains(translate(@id, "B", "b"), "articlebody") or contains(translate(@class, "B", "b"), "articlebody")
    or @id="articleContent" or contains(@class, "ArticleContent") or
    contains(@class, "page-content") or contains(@class, "text-content") or
    contains(@id, "body-text") or contains(@class, "body-text") or
    contains(@class, "article__container") or contains(@id, "art-content") or contains(@class, "art-content")][1]''',
    # (…)[1] = first occurrence
    '(.//article)[1]',
    """(.//*[self::article or self::div or self::main or self::section][
    contains(@class, 'post-bodycopy') or
    contains(@class, 'storycontent') or contains(@class, 'story-content') or
    @class='postarea' or @class='art-postcontent' or
    contains(@class, 'theme-content') or contains(@class, 'blog-content') or
    contains(@class, 'section-content') or contains(@class, 'single-content') or
    contains(@class, 'single-post') or
    contains(@class, 'main-column') or contains(@class, 'wpb_text_column') or
    starts-with(@id, 'primary') or starts-with(@class, 'article ') or @class="text" or
    @id="article" or @class="cell" or @id="story" or @class="story" or
    contains(@class, "story-body") or contains(@id, "story-body") or contains(@class, "field-body") or
    contains(translate(@class, "FULTEX","fultex"), "fulltext")
    or @role='article'])[1]""",
    '''(.//*[self::article or self::div or self::main or self::section][
    contains(@id, "content-main") or contains(@class, "content-main") or contains(@class, "content_main") or
    contains(@id, "content-body") or contains(@class, "content-body") or contains(@id, "contentBody")
    or contains(@class, "content__body") or contains(translate(@id, "CM","cm"), "main-content") or contains(translate(@class, "CM","cm"), "main-content")
    or contains(translate(@class, "CP","cp"), "page-content") or
    @id="content" or @class="content"])[1]''',
    '(.//*[self::article or self::div or self::section][starts-with(@class, "main") or starts-with(@id, "main") or starts-with(@role, "main")])[1]|(.//main)[1]',
)]
# starts-with(@id, "article") or
# or starts-with(@id, "story") or contains(@class, "story")
# starts-with(@class, "content ") or contains(@class, " content")
# '//div[contains(@class, "text") or contains(@class, "article-wrapper") or contains(@class, "content-wrapper")]',
# '//div[contains(@class, "article-wrapper") or contains(@class, "content-wrapper")]',
# |//*[self::article or self::div or self::main or self::section][contains(@class, "article") or contains(@class, "Article")]
# @id="content"or @class="content" or @class="Content"
# or starts-with(@class, 'post ')
# './/span[@class=""]', # instagram?


COMMENTS_XPATH = [XPath(x) for x in (
    """.//*[self::div or self::list or self::section][contains(@id|@class, 'commentlist')
    or contains(@class, 'comment-page') or
    contains(@id|@class, 'comment-list') or
    contains(@class, 'comments-content') or contains(@class, 'post-comments')]""",
    """.//*[self::div or self::section or self::list][starts-with(@id|@class, 'comments')
    or starts-with(@class, 'Comments') or
    starts-with(@id|@class, 'comment-') or
    contains(@class, 'article-comments')]""",
    """.//*[self::div or self::section or self::list][starts-with(@id, 'comol') or
    starts-with(@id, 'disqus_thread') or starts-with(@id, 'dsq-comments')]""",
    ".//*[self::div or self::section][starts-with(@id, 'social') or contains(@class, 'comment')]",
)]
# or contains(@class, 'Comments')


REMOVE_COMMENTS_XPATH = [XPath(
    """.//*[self::div or self::list or self::section][
    starts-with(translate(@id, "C","c"), 'comment') or
    starts-with(translate(@class, "C","c"), 'comment') or
    contains(@class, 'article-comments') or contains(@class, 'post-comments')
    or starts-with(@id, 'comol') or starts-with(@id, 'disqus_thread')
    or starts-with(@id, 'dsq-comments')
    ]"""
)]
# or self::span
# or contains(@class, 'comment') or contains(@id, 'comment')


OVERALL_DISCARD_XPATH = [XPath(x) for x in (
    # navigation + footers, news outlets related posts, sharing, jp-post-flair jp-relatedposts
    # paywalls
    '''.//*[self::div or self::item or self::list
            or self::p or self::section or self::span][
    contains(translate(@id, "F","f"), "footer") or contains(translate(@class, "F","f"), "footer")
    or contains(@id, "related") or contains(@class, "elated") or
    contains(@id|@class, "viral") or
    starts-with(@id|@class, "shar") or
    contains(@class, "share-") or
    contains(translate(@id, "S", "s"), "share") or
    contains(@id|@class, "social") or contains(@class, "sociable") or
    contains(@id|@class, "syndication") or
    starts-with(@id, "jp-") or starts-with(@id, "dpsp-content") or
    contains(@class, "embedded") or contains(@class, "embed") or
    contains(@id|@class, "newsletter") or
    contains(@class, "subnav") or
    contains(@id|@class, "cookie") or
    contains(@id|@class, "tags") or contains(@class, "tag-list") or
    contains(@id|@class, "sidebar") or
    contains(@id|@class, "banner") or contains(@class, "bar") or
    contains(@class, "meta") or contains(@id, "menu") or contains(@class, "menu") or
    contains(translate(@id, "N", "n"), "nav") or contains(translate(@role, "N", "n"), "nav")
    or starts-with(@class, "nav") or contains(@class, "avigation") or
    contains(@class, "navbar") or contains(@class, "navbox") or starts-with(@class, "post-nav")
    or contains(@id|@class, "breadcrumb") or
    contains(@id|@class, "bread-crumb") or
    contains(@id|@class, "author") or
    contains(@id|@class, "button")
    or contains(translate(@class, "B", "b"), "byline")
    or contains(@class, "rating") or contains(@class, "widget") or
    contains(@class, "attachment") or contains(@class, "timestamp") or
    contains(@class, "user-info") or contains(@class, "user-profile") or
    contains(@class, "-ad-") or contains(@class, "-icon")
    or contains(@class, "article-infos") or
    contains(@class, "nfoline")
    or contains(@data-component, "MostPopularStories")
    or contains(@class, "outbrain") or contains(@class, "taboola")
    or contains(@class, "criteo") or contains(@class, "options") or contains(@class, "expand")
    or contains(@class, "consent") or contains(@class, "modal-content")
    or contains(@class, " ad ") or contains(@class, "permission")
    or contains(@class, "next-") or contains(@class, "-stories")
    or contains(@class, "most-popular") or contains(@class, "mol-factbox")
    or starts-with(@class, "ZendeskForm") or contains(@id|@class, "message-container")
    or contains(@class, "yin") or contains(@class, "zlylin")
    or contains(@class, "xg1") or contains(@id, "bmdh")
    or contains(@class, "slide") or contains(@class, "viewport")
    or @data-lp-replacement-content
    or contains(@id, "premium") or contains(@class, "overlay")
    or contains(@class, "paid-content") or contains(@class, "paidcontent")
    or contains(@class, "obfuscated") or contains(@class, "blurred")]''',

    # comment debris + hidden parts
    '''.//*[@class="comments-title" or contains(@class, "comments-title") or
    contains(@class, "nocomments") or starts-with(@id|@class, "reply-") or
    contains(@class, "-reply-") or contains(@class, "message") or contains(@id, "reader-comments")
    or contains(@id, "akismet") or contains(@class, "akismet") or contains(@class, "suggest-links") or
    starts-with(@class, "hide-") or contains(@class, "-hide-") or contains(@class, "hide-print") or
    contains(@id|@style, "hidden") or contains(@class, " hidden") or contains(@class, " hide")
    or contains(@class, "noprint") or contains(@style, "display:none") or contains(@style, "display: none")
    or @aria-hidden="true" or contains(@class, "notloaded")]''',
)]
# conflicts:
# contains(@id, "header") or contains(@class, "header") or
# class contains "cats" (categories, also tags?)
# or contains(@class, "hidden ")  or contains(@class, "-hide")
# or contains(@class, "paywall")
# contains(@class, "content-info") or contains(@class, "content-title")
# contains(translate(@class, "N", "n"), "nav") or
# contains(@class, "panel") or
# or starts-with(@id, "comment-")


# the following conditions focus on extraction precision
TEASER_DISCARD_XPATH = [XPath(
    '''.//*[self::div or self::item or self::list
             or self::p or self::section or self::span][
        contains(translate(@id, "T", "t"), "teaser") or contains(translate(@class, "T", "t"), "teaser")
    ]'''
)]


PRECISION_DISCARD_XPATH = [XPath(x) for x in (
    './/header',
    '''.//*[self::div or self::item or self::list
             or self::p or self::section or self::span][
        contains(@id|@class, "bottom") or
        contains(@id|@class, "link") or
        contains(@style, "border")
    ]''',
)]
# or contains(@id, "-comments") or contains(@class, "-comments")


DISCARD_IMAGE_ELEMENTS = [XPath(
    '''.//*[self::div or self::item or self::list
             or self::p or self::section or self::span][
             contains(@id, "caption") or contains(@class, "caption")
            ]
    '''
)]


COMMENTS_DISCARD_XPATH = [XPath(x) for x in (
    './/*[self::div or self::section][starts-with(@id, "respond")]',
    './/cite|.//quote',
    '''.//*[@class="comments-title" or contains(@class, "comments-title") or
    contains(@class, "nocomments") or starts-with(@id|@class, "reply-") or
    contains(@class, "-reply-") or contains(@class, "message")
    or contains(@class, "signin") or
    contains(@id|@class, "akismet") or contains(@style, "display:none")]''',
)]



### 2. METADATA


# the order or depth of XPaths could be changed after exhaustive testing
AUTHOR_XPATHS = [XPath(x) for x in (
    # specific and almost specific
    '//*[self::a or self::address or self::div or self::link or self::p or self::span or self::strong][@rel="author" or @id="author" or @class="author" or @itemprop="author name" or rel="me" or contains(@class, "author-name") or contains(@class, "AuthorName") or contains(@class, "authorName") or contains(@class, "author name") or @data-testid="AuthorCard" or @data-testid="AuthorURL"]|//author',
    # almost generic and generic, last ones not common
    '//*[self::a or self::div or self::h3 or self::h4 or self::p or self::span][contains(@class, "author") or contains(@id, "author") or contains(@itemprop, "author") or @class="byline" or contains(@class, "channel-name") or contains(@id, "zuozhe") or contains(@class, "zuozhe") or contains(@id, "bianji") or contains(@class, "bianji") or contains(@id, "xiaobian") or contains(@class, "xiaobian") or contains(@class, "submitted-by") or contains(@class, "posted-by") or @class="username" or @class="byl" or @class="BBL" or contains(@class, "journalist-name")]',
     # last resort: any element
    '//*[contains(translate(@id, "A", "a"), "author") or contains(translate(@class, "A", "a"), "author") or contains(@class, "screenname") or contains(@data-component, "Byline") or contains(@itemprop, "author") or contains(@class, "writer") or contains(translate(@class, "B", "b"), "byline")]',
)]


AUTHOR_DISCARD_XPATHS = [XPath(x) for x in (
    """.//*[self::a or self::div or self::section or self::span][@id='comments' or @class='comments' or @class='title' or @class='date' or
    contains(@id, 'commentlist') or contains(@class, 'commentlist') or contains(@class, 'sidebar') or contains(@class, 'is-hidden') or contains(@class, 'quote')
    or contains(@id, 'comment-list') or contains(@class, 'comments-list') or contains(@class, 'embedly-instagram') or contains(@id, 'ProductReviews') or
    starts-with(@id, 'comments') or contains(@data-component, "Figure") or contains(@class, "article-share") or contains(@class, "article-support") or contains(@class, "print") or contains(@class, "category") or contains(@class, "meta-date") or contains(@class, "meta-reviewer")
    or starts-with(@class, 'comments') or starts-with(@class, 'Comments')
    ]""",
    '//time|//figure',
)]


CATEGORIES_XPATHS = [XPath(x) for x in (
    """//div[starts-with(@class, 'post-info') or starts-with(@class, 'postinfo') or
    starts-with(@class, 'post-meta') or starts-with(@class, 'postmeta') or
    starts-with(@class, 'meta') or starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-info') or
    starts-with(@class, 'entry-utility') or starts-with(@id, 'postpath')]//a[@href]""",
    "//p[starts-with(@class, 'postmeta') or starts-with(@class, 'entry-categories') or @class='postinfo' or @id='filedunder']//a[@href]",
    "//footer[starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-footer')]//a[@href]",
    '//*[self::li or self::span][@class="post-category" or @class="postcategory" or @class="entry-category" or contains(@class, "cat-links")]//a[@href]',
    '//header[@class="entry-header"]//a[@href]',
    '//div[@class="row" or @class="tags"]//a[@href]',
)]
# "//*[self::div or self::p][contains(@class, 'byline')]",


TAGS_XPATHS = [XPath(x) for x in (
    '//div[@class="tags"]//a[@href]',
    "//p[starts-with(@class, 'entry-tags')]//a[@href]",
    '''//div[@class="row" or @class="jp-relatedposts" or
    @class="entry-utility" or starts-with(@class, 'tag') or
    starts-with(@class, 'postmeta') or starts-with(@class, 'meta')]//a[@href]''',
    '//*[@class="entry-meta" or contains(@class, "topics") or contains(@class, "tags-links")]//a[@href]',
)]
# "related-topics"
# https://github.com/grangier/python-goose/blob/develop/goose/extractors/tags.py


TITLE_XPATHS = [XPath(x) for x in (
    '//*[self::h1 or self::h2][contains(@class, "post-title") or contains(@class, "entry-title") or contains(@class, "headline") or contains(@id, "headline") or contains(@itemprop, "headline") or contains(@class, "post__title") or contains(@class, "article-title")]',
    '//*[@class="entry-title" or @class="post-title"]',
    '//*[self::h1 or self::h2 or self::h3][contains(@class, "title") or contains(@id, "title")]',
)]
# json-ld headline
# '//header/h1',
