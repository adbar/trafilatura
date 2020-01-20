"""
X-Path expressions needed to extract and filter the main text content
"""
## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


BODY_XPATH = [
    '''//*[(self::div or self::section)][contains(@id, "content-main")  or
    contains(@class, "content-main") or contains(@class, "content_main") or 
    contains(@id, "content-body")  or contains(@class, "content-body") or
    @id="article" or @id="articleContent" or @itemprop="articleBody" or
    @class="post" or  @class="entry" or @id="story" or @class="story" or
    starts-with(@id, "story")]''',
    '''//*[(self::div or self::section)][contains(@id, "entry-content") or
    contains(@class, "entry-content") or contains(@id, "article-content") or
    contains(@class, "article-content") or contains(@id, "article__content") or
    contains(@class, "article__content") or contains(@id, "article-body") or
    contains(@class, "article-body") or contains(@id, "article__body") or
    contains(@class, "article__body") or contains(@class, "post-text") or
    contains(@class, "post_text") or contains(@class, "post-body") or
    contains(@class, "post-content") or contains(@class, "post_content") or
    contains(@class, "postcontent") or contains(@class, "post-entry") or
    contains(@class, "postentry")]''',
    '''//*[(self::div or self::main or self::section)][@id="content" or
    contains(@class, "ArticleContent") or contains(@class, "page-content") or
    contains(@class, "text-content") or contains(@class, "content__body")]''',
    '//article',
    """//*[(self::article or self::div or self::section)][starts-with(@id, 'article')
    or starts-with(@class, 'article') or starts-with(@id, 'main') or
    starts-with(@class, 'main') or starts-with(@role, 'main') or starts-with(@class, 'entry')
    or @class='text' or starts-with(@id, 'primary')]""",
    """//*[(self::div or self::section)][starts-with(@class, 'post-bodycopy') or
    contains(@class, 'storycontent') or @class='postarea' or @class='art-postcontent']""",
    """//*[(self::div or self::section)][starts-with(@class, 'theme-content') or
    starts-with(@class, 'blog-content') or starts-with(@class, 'section-content')
    or starts-with(@class, 'single-content')]""",
    '//div[contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "fulltext")]',
    """//*[(self::div or self::section)][starts-with(@class, 'wpb_text_column')
    or contains(@class, 'single-post')]""",
    '//div[@class="cell"]',
    '''//*[(self::div or self::section)][starts-with(@class, "content ") or
    contains(@class, " content") or @class="content" or class="story-content"]''',
    '//main',
]
# '//*[(self::div or self::section)][]', \
#  or contains(@class, "story")
# '//*[(self::div or self::section)][starts-with(@class, "main") or starts-with(@id, "main")]', \
#  , \ '//main', \


COMMENTS_XPATH = [
    """//*[(self::div or self::section or self::ol or self::ul)][contains(@id, 'commentlist')
    or contains(@class, 'commentlist') or contains(@class, 'comments-content')]""",
    """//*[(self::div or self::section or self::ol or self::ul)][starts-with(@id, 'comments')
    or starts-with(@class, 'comments') or starts-with(@class, 'Comments') or
    starts-with(@id, 'comment-') or starts-with(@class, 'comment-') or
    contains(@class, 'article-comments')]""",
    """//*[(self::div or self::section or self::ul)][starts-with(@id, 'comol') or
    starts-with(@id, 'disqus_thread') or starts-with(@id, 'dsq-comments')]""",
    """//*[(self::div or self::section)][starts-with(@id, 'social') or contains(@class, 'comment')]"""
]
# or contains(@class, 'Comments')


DISCARD_XPATH = [
    '''.//*[(self::div or self::section or self::ul)][contains(@id, "sidebar") or
    contains(@class, "sidebar") or contains(@id, "banner") or contains(@class, "banner")]''',
    './/header',
    './/*[@class="meta" or contains(@class, "meta-") or contains(@class, "-meta")]',
    # |.//footer
    '''.//*[(self::div or self::p or self::section)][contains(@id, "header") or
    contains(@class, "header") or contains(@id, "footer") or contains(@class, "footer") or
    contains(@id, "bottom") or contains(@class, "bottom")]''',
    '''.//*[(self::a or self::div or self::p or self::section or self::ul)][contains(@id, "tags")
    or contains(@class, "tags")]''',
    # news outlets
    '''.//*[(self::div or self::p or self::section)][contains(@id, "teaser") or
    contains(@class, "teaser") or contains(@id, "newsletter") or contains(@class, "newsletter")
    or contains(@id, "cookie") or contains(@class, "cookie")]''',
    #'.//*[(self::div or self::p or self::section)][]',
    # navigation
    '''.//*[(self::div or self::ol or self::section or self::ul)][starts-with(@id, "nav-")
    or starts-with(@class, "nav-") or starts-with(@id, "nav ") or starts-with(@class, "nav ")
    or starts-with(@class, "post-nav") or starts-with(@id, "breadcrumbs")
    or contains(@id, "breadcrumb") or contains(@class, "breadcrumb") or
    contains(@id, "bread-crumb") or contains(@class, "bread-crumb")]''',
    # related posts
    '''.//*[(self::div or self::section or self::ul)][contains(@id, "related") or
    contains(@class, "related") or contains(@id, "viral") or contains(@class, "viral")]''',
    # sharing jp-post-flair jp-relatedposts
    '''.//*[(self::div or self::section or self::ul)][starts-with(@id, "shar") or
    starts-with(@class, "shar") or contains(@class, "share-") or contains(@id, "social")
    or contains(@class, "social") or contains(@class, "sociable") or contains(@id, "syndication")
    or contains(@class, "syndication") or starts-with(@id, "jp-") or starts-with(@id, "dpsp-content")]''',
    '''.//*[(self::div or self::p or self::section or self::span or self::ul)][contains(@id, "author")
    or contains(@class, "author") or contains(@id, "button") or contains(@class, "button")
    or starts-with(@class, "hide-") or contains(@class, "hide-print") or contains(@id, "hidden")
    or contains(@style, "hidden") or contains(@class, "noprint")]''',
    '''.//*[(self::div or self::p or self::section)][contains(@id, "caption") or
    contains(@class, "caption")]''',
    './/*[starts-with(@class, "widget")]',
    # other content
    './/*[(self::div or self::section or self::ul)][contains(@class, "ratings")]',
    '''.//*[contains(@class, "attachment") or contains(@class, "timestamp") or
    contains(@class, "user-info") or contains(@class, "user-profile") or
    contains(@class, "-ad-") or contains(@class, "-icon") or contains(@class, "navbox")
    or contains(@class, "submeta")]''',
    '''.//*[(self::div or self::p or self::ul)][contains(@class, "byline") or
    contains(@class, 'Byline')]''',
]
# optional?
# *[contains(@class, "article-infos")  or contains(@class, "author")
# div/section[contains(@class, "clearfix")
# conflicts: './/aside', contains(@class, "hidden")
#  or contains(@id, "menu") or contains(@class, "menu")
# class contains cats


COMMENTS_DISCARD_XPATH = [
    './/*[(self::div or self::section)][starts-with(@id, "respond")]',
    './/cite',
    './/quote',
    './/*[@class="comments-title" or contains(@class, "comments-title")]',
    '''.//*[starts-with(@id, "reply-") or starts-with(@class, "reply-") or
    contains(@class, "-reply-")]''',
    './/*[contains(@id, "akismet") or contains(@class, "akismet")]',
]
