"""
File containing XPath expressions to extract metadata.
"""

# code available from https://giuthub.com/adbar/kontext/
# under GNU GPLv3+ license


author_xpaths = [
'//a[@rel="author" or @class="author" or rel="me"]',
'//*[@rel="author" or @class="author" or rel="me"]',
'//author',
'//a[contains(@class, "author")]',
]
# json author
# '//address[@class="author"]',
# screenname
# @class, 'byline'


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


tags_xpaths = [
'//div[@class="tags"]//a',
"//p[starts-with(@class, 'entry-tags')]//a",
'''//div[@class="row" or @class="jp-relatedposts" or @class="entry-utility" or
    starts-with(@class, 'tag') or starts-with(@class, 'postmeta') or
    starts-with(@class, 'meta')]//a''',
'//*[@class="entry-meta"]//a'
]


title_xpaths = [
'//h1',
'//h1[contains(@class, "title") or contains(@id, "title")]',
'//*[contains(@class, "post-title") or contains(@class, "entry-title")]',
'//head/title',
'//h2',
]
# json headline
