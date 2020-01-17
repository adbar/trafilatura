"""
File containing XPath expressions to extract metadata.
"""

# code available from https://giuthub.com/adbar/kontext/
# under GNU GPLv3+ license


author_xpaths = [
'//a[@rel="author"]',
'//a[@class="author"]',
'//span[@class="author"]',
'//address[@class="author"]',
'//author',
]
# rel="me"

categories_xpaths = [
"//div[starts-with(@class, 'post-info')]//a",
"//div[starts-with(@class, 'postinfo')]//a",
"//div[starts-with(@class, 'post-meta')]//a",
'//div[@class="row"]//a',
'//div[@class="byline"]//a',
"//div[starts-with(@class, 'postmeta')]//a",
"//div[starts-with(@class, 'entry-meta')]//a",
"//div[starts-with(@class, 'entry-info')]//a",
"//div[starts-with(@class, 'entry-utility')]//a",
"//div[starts-with(@id, 'postpath')]//a",
"//p[starts-with(@class, 'postmeta')]//a",
"//p[starts-with(@class, 'entry-categories')]//a",
'//p[@class="postinfo"]//a',
'//p[@id="filedunder"]//a',
'//p[@class="postdate"]//a',
"//footer[starts-with(@class, 'entry-meta')]//a",
"//footer[starts-with(@class, 'entry-footer')]//a",
'//li[@class="post-category"]//a',
'//span[@class="postcategory"]//a',
'//span[@class="entry-category"]//a',
'//header[@class="entry-header"]//a',
'//div[@class="tags"]//a',
"//div[starts-with(@class, 'meta')]//a",
]

tags_xpaths = [
"//p[starts-with(@class, 'entry-tags')]//a",
'//div[@class="row"]//a',
'//div[@class="jp-relatedposts"]//a',
"//div[starts-with(@class, 'tag')]//a",
'//div[@class="entry-utility"]//a',
"//div[starts-with(@class, 'meta')]//a",
'//*[@class="entry-meta"]//a'
]
# , "//div[starts-with(@class, 'postmeta')]//a"
