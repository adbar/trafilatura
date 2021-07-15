"""
File containing XPath expressions to extract metadata.
"""

# code available from https://github.com/adbar/trafilatura/
# under GNU GPLv3+ license

attr_types = {
    'class': 'translate(@class,"ABCDEFGHIJKLMNOPURSTUWXYZ","abcdefghijklmnopurstuwxyz")',
    'id': 'translate(@id,"ABCDEFGHIJKLMNOPURSTUWXYZ","abcdefghijklmnopurstuwxyz")',
    'itemprop': 'translate(@itemprop,"ABCDEFGHIJKLMNOPURSTUWXYZ","abcdefghijklmnopurstuwxyz")',
    'rel': 'translate(@rel,"ABCDEFGHIJKLMNOPURSTUWXYZ","abcdefghijklmnopurstuwxyz")',
}

author_xpaths = [
    '//*[(self::a or self::address or self::link or self::p or self::span)][' + attr_types['rel'] + '="author" or ' +
    attr_types['id'] + '="author" or ' + attr_types['class'] + '="author" or ' + attr_types['rel'] + '="me"]|//author',
    '//*[(self::a or self::span)][contains(' + attr_types['class'] + ', "authors") or (contains(' + attr_types[
        'class'] + ', "author") and not(contains(' + attr_types['class'] + ', "prefix"))) or contains(' + attr_types[
        'class'] + ', "posted-by") or contains(' + attr_types['itemprop'] + ', "author")]',
    '//*[(self::a or self::div or self::p or self::span)][contains(' + attr_types[
        'class'] + ', "byline") or contains(' + attr_types['class'] + ', "journalist")]',
    '//*[contains(' + attr_types['class'] + ', "author") or contains(' + attr_types['class'] + ', "screenname")]',
]

categories_xpaths = [
    '//div[starts-with(' + attr_types['class'] + ', "post-info") or starts-with(' + attr_types[
        'class'] + ', "postinfo") or starts-with(' + attr_types['class'] + ', "post-meta") or starts-with(' +
    attr_types['class'] + ', "postmeta") or starts-with(' + attr_types['class'] + ', "meta") or starts-with(' +
    attr_types['class'] + ', "entry-meta") or starts-with(' + attr_types['class'] + ', "entry-info") or starts-with(' +
    attr_types['class'] + ', "entry-utility") or starts-with(' + attr_types['id'] + ', "postpath")]//a',
    '//p[starts-with(' + attr_types['class'] + ', "postmeta") or starts-with(' + attr_types[
        'class'] + ', "entry-categories") or ' + attr_types['class'] + '="postinfo" or ' + attr_types[
        'id'] + '="filedunder"]//a',
    '//footer[starts-with(' + attr_types['class'] + ', "entry-meta") or starts-with(' + attr_types[
        'class'] + ', "entry-footer")]//a',
    '//*[(self::li or self::span)][' + attr_types['class'] + '="post-category" or ' + attr_types[
        'class'] + '="postcategory" or ' + attr_types['class'] + '="entry-category"]//a',
    '//header[' + attr_types['class'] + '="entry-header"]//a',
    '//div[' + attr_types['class'] + '="row" or ' + attr_types['class'] + '="tags"]//a',
]
# "//div[contains(@class, 'byline')]",
# "//p[contains(@class, 'byline')]",
# span class cat-links


tags_xpaths = [
    '//div[' + attr_types['class'] + '="tags"]//a',
    '//p[starts-with(' + attr_types['class'] + ', "entry-tags")]//a',
    '//div[' + attr_types['class'] + '="row" or ' + attr_types['class'] + '="jp-relatedposts" or ' + attr_types[
        'class'] + '="entry-utility" or starts-with(' + attr_types['class'] + ', "tag") or starts-with(' + attr_types[
        'class'] + ', "postmeta") or starts-with(' + attr_types['class'] + ', "meta")]//a',
    '//*[' + attr_types['class'] + '="entry-meta" or contains(' + attr_types['class'] + ', "topics")]//a',
]
# span class tag-links
# "related-topics"
# https://github.com/grangier/python-goose/blob/develop/goose/extractors/tags.py


title_xpaths = [
    '//*[(self::h1 or self::h2)][contains(' + attr_types['class'] + ', "post-title") or contains(' + attr_types[
        'class'] + ', "entry-title") or contains(' + attr_types['class'] + ', "headline") or contains(' + attr_types[
        'id'] + ', "headline") or contains(' + attr_types['itemprop'] + ', "headline") or contains(' + attr_types[
        'class'] + ', "post__title")]',
    '//*[' + attr_types['class'] + '="entry-title" or ' + attr_types['class'] + '="post-title"]',
    '//h1[contains(' + attr_types['class'] + ', "title") or contains(' + attr_types['id'] + ', "title")]',
]
# json-ld headline
# '//header/h1',
