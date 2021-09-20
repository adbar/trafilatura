"""
X-Path expressions needed to extract and filter the main text content
"""
## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


BODY_XPATH = [
    '''.//*[(self::article or self::div or self::main or self::section)][contains(@id, "content-main") or
    contains(@class, "content-main") or contains(@class, "content_main") or
    contains(@id, "content-body") or contains(@class, "content-body") or
    contains(@class, "story-body") or
    @id="article" or @class="post" or @class="entry"]''',
    # contains(@class, "main-content") or
    '''.//*[(self::article or self::div or self::main or self::section)][
    contains(@class, "post-text") or contains(@class, "post_text") or
    contains(@class, "post-body") or contains(@class, "post-entry") or contains(@class, "postentry") or
    contains(@class, "post-content") or contains(@class, "post_content") or
    contains(@class, "postcontent") or contains(@class, "postContent") or
    contains(@class, "article-text") or contains(@class, "articletext") or contains(@class, "articleText") or contains(@class, "field-body")]''',
    '''.//*[(self::article or self::div or self::main or self::section)][contains(@id, "entry-content") or
    contains(@class, "entry-content") or contains(@id, "article-content") or
    contains(@class, "article-content") or contains(@id, "article__content") or
    contains(@class, "article__content") or contains(@id, "article-body") or
    contains(@class, "article-body") or contains(@id, "article__body") or
    contains(@class, "article__body") or @itemprop="articleBody" or @id="articleContent" or
    contains(@class, "ArticleContent") or contains(@class, "page-content") or
    contains(@class, "text-content") or contains(@class, "content__body") or
    contains(@id, "body-text") or contains(@class, "body-text") or
    contains(@class, "article__container") or contains(@id, "art-content") or contains(@class, "art-content")
    or contains(@id, "contentBody")]''',
    './/article',
    """.//*[(self::article or self::div or self::main or self::section)][contains(@class, 'post-bodycopy') or
    contains(@class, 'storycontent') or contains(@class, 'story-content') or
    @class='postarea' or @class='art-postcontent' or
    contains(@class, 'theme-content') or contains(@class, 'blog-content') or
    contains(@class, 'section-content') or contains(@class, 'single-content') or
    contains(@class, 'single-post') or
    contains(@class, 'main-column') or contains(@class, 'wpb_text_column') or
    starts-with(@id, 'primary') or starts-with(@class, 'article ') or @class="text" or
    @class="cell" or @id="story" or @class="story" or
    contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "fulltext")]""",
    '''.//*[(self::article or self::div or self::main or self::section)][contains(@id, "main-content") or
    contains(@class, "main-content") or contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "page-content")]''',
    './/*[(self::article or self::div or self::section)][starts-with(@class, "main") or starts-with(@id, "main") or starts-with(@role, "main")]|//main',

]
# starts-with(@id, "article") or
# or starts-with(@id, "story") or contains(@class, "story")
# or @class="content" or @id="content"
# starts-with(@class, "content ") or contains(@class, " content")
# '//div[contains(@class, "text") or contains(@class, "article-wrapper") or contains(@class, "content-wrapper")]',
# '//div[contains(@class, "article-wrapper") or contains(@class, "content-wrapper")]',
# |//*[(self::article or self::div or self::main or self::section)][contains(@class, "article") or contains(@class, "Article")]
# or @class="content" or @class="Content"
# or starts-with(@class, 'post ')
# './/span[@class=""]', # instagram?


COMMENTS_XPATH = [
    """.//*[(self::div or self::section or self::list)][contains(@id, 'commentlist')
    or contains(@class, 'commentlist') or contains(@class, 'comment-page') or
    contains(@id, 'comment-list') or contains(@class, 'comments-list') or
    contains(@class, 'comments-content')]""",
    """.//*[(self::div or self::section or self::list)][starts-with(@id, 'comments')
    or starts-with(@class, 'comments') or starts-with(@class, 'Comments') or
    starts-with(@id, 'comment-') or starts-with(@class, 'comment-') or
    contains(@class, 'article-comments')]""",
    """.//*[(self::div or self::section or self::list)][starts-with(@id, 'comol') or
    starts-with(@id, 'disqus_thread') or starts-with(@id, 'dsq-comments')]""",
    """.//*[(self::div or self::section)][starts-with(@id, 'social') or contains(@class, 'comment')]"""
]
# or contains(@class, 'Comments')


REMOVE_COMMENTS_XPATH = [
    """.//*[(self::div or self::section)][@id='comments' or @class='comments' or
    contains(@id, 'commentlist') or contains(@class, 'commentlist')
    or contains(@id, 'comment-list') or contains(@class, 'comments-list') or
    starts-with(@id, 'comments')
    or starts-with(@class, 'comments') or starts-with(@class, 'Comments')
    ]""",
]
# or self::list
# or contains(@id, 'commentlist') or contains(@class, 'commentlist') or
#    contains(@id, 'comment-list') or contains(@class, 'comments-list') or
#    contains(@class, 'comments-content')
#  or starts-with(@id, 'comment-') or starts-with(@class, 'comment-') or
#    contains(@class, 'article-comments')
#  or contains(@class, 'comment-page') or


DISCARD_XPATH = [
    '''.//*[contains(@id, "footer") or contains(@class, "footer") or
    contains(@id, "bottom") or contains(@class, "bottom")]''',
    # related posts, sharing jp-post-flair jp-relatedposts, news outlets + navigation
    #'''.//*[
    # self::article or self::link
    '''.//*[(self::div or self::item or self::list
             or self::p or self::section or self::span)][
    contains(@id, "related") or contains(translate(@class, "R","r"), "related") or
    contains(@id, "viral") or contains(@class, "viral") or
    starts-with(@id, "shar") or starts-with(@class, "shar") or contains(@class, "share-") or
    contains(@id, "social") or contains(@class, "social") or contains(@class, "sociable") or
    contains(@id, "syndication") or contains(@class, "syndication") or
    starts-with(@id, "jp-") or starts-with(@id, "dpsp-content") or
    contains(@class, "embedded") or contains(@class, "embed")
    or contains(@id, "teaser") or contains(@class, "teaser") or
    contains(translate(@class, "T","t"), "teaser")
    or contains(@id, "newsletter") or contains(@class, "newsletter") or
    contains(@id, "cookie") or contains(@class, "cookie") or contains(@id, "tags")
    or contains(@class, "tags")  or contains(@id, "sidebar") or
    contains(@class, "sidebar") or contains(@id, "banner") or contains(@class, "banner")
    or contains(@class, "meta") or
    contains(@id, "menu") or contains(@class, "menu") or
    starts-with(@id, "nav") or starts-with(@class, "nav") or
    contains(@id, "navigation") or contains(translate(@class, "N","n"), "navigation")
    or contains(@role, "navigation") or contains(@class, "navbar")
    or contains(@class, "navbox") or starts-with(@class, "post-nav")
    or contains(@id, "breadcrumb") or contains(@class, "breadcrumb") or
    contains(@id, "bread-crumb") or contains(@class, "bread-crumb") or
    contains(@id, "author") or contains(@class, "author") or
    contains(@id, "button") or contains(@class, "button")
    or contains(translate(@class, "B","b"), "byline")
    or contains(@class, "rating") or starts-with(@class, "widget") or
    contains(@class, "attachment") or contains(@class, "timestamp") or
    contains(@class, "user-info") or contains(@class, "user-profile") or
    contains(@class, "-ad-") or contains(@class, "-icon")
    or contains(@class, "article-infos") or
    contains(translate(@class, "I","i"), "infoline")
    or contains(@data-component, "MostPopularStories")
    or contains(@class, "options")
    or contains(@class, "consent") or contains(@class, "modal-content")
    or contains(@class, "paid-content") or contains(@class, "paidcontent")
    or contains(@class, " ad ")]''',
    # comment debris
    '''.//*[@class="comments-title" or contains(@class, "comments-title") or contains(@class, "nocomments") or starts-with(@id, "reply-") or starts-with(@class, "reply-") or
    contains(@class, "-reply-") or contains(@class, "message") or contains(@id, "akismet") or contains(@class, "akismet")]''',
    # hidden
    '''.//*[starts-with(@class, "hide-") or contains(@class, "hide-print") or contains(@id, "hidden")
    or contains(@style, "hidden") or contains(@hidden, "hidden") or contains(@class, "noprint") or contains(@style, "display:none") or contains(@class, " hidden")]''',
]

DISCARD_IMAGE_ELEMENTS = [
    '''.//*[(self::div or self::item or self::list
             or self::p or self::section or self::span)][
             contains(@id, "caption") or contains(@class, "caption")
            ]
    '''
]
# conflicts:
# .//header # contains(@id, "header") or contains(@class, "header") or
# contains(@id, "link") or contains(@class, "link")
# class contains cats
# or contains(@class, "hidden ")  or contains(@class, "-hide")


COMMENTS_DISCARD_XPATH = [
    './/*[(self::div or self::section)][starts-with(@id, "respond")]',
    './/cite|.//quote',
    '''.//*[@class="comments-title" or contains(@class, "comments-title") or contains(@class, "nocomments") or starts-with(@id, "reply-") or starts-with(@class, "reply-") or
    contains(@class, "-reply-") or contains(@class, "message") or
    contains(@id, "akismet") or contains(@class, "akismet") or contains(@style, "display:none")]''',
]
