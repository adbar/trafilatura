"""
File containing XPath expressions to extract metadata.
"""

# code available from https://giuthub.com/adbar/kontext/
# under GNU GPLv3+ license


author_xpaths = [
    '//*[(self::a or self::address or self::link)][@rel="author" or @class="author" or rel="me"]',
    '//author',
    '//a[contains(@class, "author")]',
    '//span[contains(@class, "authors") or contains(@class, "author") or contains(@class, "posted-by") or contains(@itemprop, "author")]',
    '//span[contains(@class, "byline")]',
]
# json author
# '//address[@class="author"]',
# screenname
# '//*[@rel="author" or @class="author" or rel="me"]',


categories_xpaths = [
    """//div[starts-with(@class, 'post-info') or starts-with(@class, 'postinfo') or
    starts-with(@class, 'post-meta') or starts-with(@class, 'postmeta') or
    starts-with(@class, 'meta')]//a""",
    '//div[@class="row"]//a',
    """//div[starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-info') or
    starts-with(@class, 'entry-utility')]//a""",
    "//div[starts-with(@id, 'postpath')]//a",
    "//p[starts-with(@class, 'postmeta') or starts-with(@class, 'entry-categories')]//a",
    '//p[@class="postinfo" or @id="filedunder"]//a',
    "//footer[starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-footer')]//a",
    '//li[@class="post-category"]//a',
    '//span[@class="postcategory"]//a',
    '//span[@class="entry-category"]//a',
    '//header[@class="entry-header"]//a',
    '//div[@class="tags"]//a',
]
# "//div[contains(@class, 'byline')]",
# "//p[contains(@class, 'byline')]",
# span class cat-links


tags_xpaths = [
    '//div[@class="tags"]//a',
    "//p[starts-with(@class, 'entry-tags')]//a",
    '''//div[@class="row" or @class="jp-relatedposts" or @class="entry-utility" or
    starts-with(@class, 'tag') or starts-with(@class, 'postmeta') or
    starts-with(@class, 'meta')]//a''',
    '//*[@class="entry-meta"]//a'
]
# span class tag-links

title_xpaths = [
    '//h1',
    '//h1[contains(@class, "title") or contains(@id, "title")]',
    '//*[contains(@class, "post-title") or contains(@class, "entry-title")]',
    '//head/title',
    '//h2',
]
# json headline
