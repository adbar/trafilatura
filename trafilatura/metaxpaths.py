"""
File containing XPath expressions to extract metadata.
"""

# code available from https://github.com/adbar/trafilatura/
# under GNU GPLv3+ license


# the order or depth of XPaths could be changed after exhaustive testing
author_xpaths = [
    '//*[(self::a or self::address or self::div or self::link or self::p or self::span or self::strong)][@rel="author" or @id="author" or @class="author" or @itemprop="author name" or rel="me" or contains(@class, "author-name") or contains(@class, "AuthorName") or contains(@class, "authorName") or contains(@class, "author name")]|//author', # specific and almost specific
    '//*[(self::a or self::div or self::h3 or self::h4 or self::p or self::span)][contains(@class, "author") or contains(@id, "author") or contains(@itemprop, "author") or @class="byline" or contains(@id, "zuozhe") or contains(@class, "zuozhe") or contains(@id, "bianji") or contains(@class, "bianji") or contains(@id, "xiaobian") or contains(@class, "xiaobian") or contains(@class, "submitted-by") or contains(@class, "posted-by") or @class="username" or @class="BBL" or contains(@class, "journalist-name")]', # almost generic and generic, last ones not common
    '//*[contains(translate(@id, "A", "a"), "author") or contains(translate(@class, "A", "a"), "author") or contains(@class, "screenname") or contains(@data-component, "Byline") or contains(@itemprop, "author") or contains(@class, "writer") or contains(translate(@class, "B", "b"), "byline")]', # last resort: any element
]


author_discard_xpaths = [
    """.//*[(self::a or self::div or self::section or self::span)][@id='comments' or @class='comments' or @class='title' or @class='date' or
    contains(@id, 'commentlist') or contains(@class, 'commentlist') or contains(@class, 'sidebar') or contains(@class, 'is-hidden') or contains(@class, 'quote')
    or contains(@id, 'comment-list') or contains(@class, 'comments-list') or contains(@class, 'embedly-instagram') or contains(@id, 'ProductReviews') or
    starts-with(@id, 'comments') or contains(@data-component, "Figure") or contains(@class, "article-share") or contains(@class, "article-support") or contains(@class, "print") or contains(@class, "category") or contains(@class, "meta-date") or contains(@class, "meta-reviewer")
    or starts-with(@class, 'comments') or starts-with(@class, 'Comments')
    ]""",
    '//time|//figure',
]


categories_xpaths = [
    """//div[starts-with(@class, 'post-info') or starts-with(@class, 'postinfo') or
    starts-with(@class, 'post-meta') or starts-with(@class, 'postmeta') or
    starts-with(@class, 'meta') or starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-info') or
    starts-with(@class, 'entry-utility') or starts-with(@id, 'postpath')]//a[@href]""",
    "//p[starts-with(@class, 'postmeta') or starts-with(@class, 'entry-categories') or @class='postinfo' or @id='filedunder']//a[@href]",
    "//footer[starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-footer')]//a[@href]",
    '//*[(self::li or self::span)][@class="post-category" or @class="postcategory" or @class="entry-category" or contains(@class, "cat-links")]//a[@href]',
    '//header[@class="entry-header"]//a[@href]',
    '//div[@class="row" or @class="tags"]//a[@href]',
]
# "//*[(self::div or self::p)][contains(@class, 'byline')]",


tags_xpaths = [
    '//div[@class="tags"]//a[@href]',
    "//p[starts-with(@class, 'entry-tags')]//a[@href]",
    '''//div[@class="row" or @class="jp-relatedposts" or
    @class="entry-utility" or starts-with(@class, 'tag') or
    starts-with(@class, 'postmeta') or starts-with(@class, 'meta')]//a[@href]''',
    '//*[@class="entry-meta" or contains(@class, "topics") or contains(@class, "tags-links")]//a[@href]',
]
# "related-topics"
# https://github.com/grangier/python-goose/blob/develop/goose/extractors/tags.py


title_xpaths = [
    '//*[(self::h1 or self::h2)][contains(@class, "post-title") or contains(@class, "entry-title") or contains(@class, "headline") or contains(@id, "headline") or contains(@itemprop, "headline") or contains(@class, "post__title")]',
    '//*[@class="entry-title" or @class="post-title"]',
    '//*[(self::h1 or self::h2 or self::h3)][contains(@class, "title") or contains(@id, "title")]',
]
# json-ld headline
# '//header/h1',
