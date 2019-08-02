# -*- coding: utf-8 -*-
"""
X-Path expressions needed to extract and filter the main text content
"""
## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


BODY_XPATH = ['//*[(self::div or self::section)][starts-with(@id, "entry-content") or starts-with(@class, "entry-content") or starts-with(@id, "article-content") or starts-with(@class, "article-content") or starts-with(@id, "article__content") or starts-with(@class, "article__content")]', \
            "//*[(self::div or self::section)][contains(@class, 'post-text') or contains(@class, 'post_text')]", \
            "//*[(self::div or self::section)][contains(@class, 'post-body')]", \
            "//*[(self::div or self::section)][contains(@class, 'post-content') or contains(@class, 'post_content') or contains(@class, 'postcontent')]", \
            "//*[(self::div or self::section)][contains(@class, 'post-entry') or contains(@class, 'postentry')]", \
            "//*[(self::div or self::section)][starts-with(@id, 'story')]", \
            "//*[(self::div or self::section)][starts-with(@class, 'entry')]", \
            '//*[(self::div or self::section)][@id="content-main" or @id="content" or @class="content"]', \
            '//article', \
            "//*[(self::article or self::div or self::section)][@id='article' or @class='article']", \
            "//*[(self::article or self::div or self::section)][starts-with(@id, 'main') or starts-with(@class, 'main') or starts-with(@role, 'main')]", \
            '//*[(self::div or self::section)][@class="text"]', \
            "//*[(self::div or self::section)][starts-with(@class, 'post-bodycopy')]", \
            "//*[(self::div or self::section)][@class='postarea']", \
            '//*[(self::div or self::section)][contains(@class, "storycontent")]', \
            "//*[(self::div or self::section)][starts-with(@id, 'primary')]", \
            "//*[(self::div or self::section)][starts-with(@class, 'theme-content') or starts-with(@class, 'blog-content') or starts-with(@class, 'section-content') or starts-with(@class, 'single-content')]", \
            '//*[(self::div or self::section)][@class="art-postcontent"]', \
            '//*[(self::div or self::section)][@class="post"]', \
            '//div[contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "fulltext")]', \
            "//*[(self::div or self::section)][starts-with(@class, 'wpb_text_column')]", \
            '//div[@class="cell"]', \
            '//*[(self::div or self::section)][@itemprop="articleBody"]', \
           ]
#             '//*[(self::div or self::section)][contains(@id, "entry-content") or contains(@class, "entry-content") or contains(@id, "article-content") or contains(@class, "article-content") or contains(@id, "article__content") or contains(@class, "article__content")]', \


COMMENTS_XPATH = ["//*[(self::div or self::section or self::ol or self::ul)][contains(@id, 'commentlist') or contains(@class, 'commentlist')]", \
                "//*[(self::div or self::section or self::ol or self::ul)][starts-with(@id, 'comments') or starts-with(@class, 'comments') or starts-with(@class, 'Comments')]", \
                "//*[(self::div or self::section or self::ol)][starts-with(@id, 'comment-') or starts-with(@class, 'comment-')]", \
                "//*[(self::div or self::section)][starts-with(@id, 'comol')]", \
                "//*[(self::div or self::section)][starts-with(@id, 'disqus_thread')]", \
                "//ul[starts-with(@id, 'dsq-comments')]" \
                "//*[(self::div or self::section)][starts-with(@id, 'social')]" \
                "//*[(self::div or self::section)][contains(@class, 'comment')]", \
               ]
# '//*[(self::div or self::section)][@id="comments" or @class="comments"]', \


DISCARD_XPATH = ['.//*[(self::div or self::section or self::ul)][contains(@id, "sidebar") or contains(@class, "sidebar")]', \
                 './/footer', \
                 './/*[(self::div or self::p or self::section)][contains(@id, "footer") or contains(@class, "footer")]', \
                 './/header', \
                 './/*[(self::div or self::section)][contains(@id, "header") or contains(@class, "header")]', \
                 './/*[(self::a or self::div or self::p or self::section or self::ul)][contains(@id, "tags") or contains(@class, "tags")]', \
                 # news outlets
                 './/*[(self::div or self::p or self::section)][contains(@id, "teaser") or contains(@class, "teaser")]', \
                 './/*[(self::div or self::p or self::section)][contains(@id, "newsletter") or contains(@class, "newsletter")]', \
                 './/*[(self::div or self::p or self::section)][contains(@id, "cookie") or contains(@class, "cookie")]', \
                 # navigation
                 './/*[(self::div or self::section)][starts-with(@id, "nav-") or starts-with(@class, "nav-")]', \
                 './/*[starts-with(@id, "breadcrumbs")]',\
                 './/*[contains(@id, "breadcrumb") or contains(@class, "breadcrumb") or contains(@id, "bread-crumb") or contains(@class, "bread-crumb")]',\
                 # related posts
                 './/*[(self::div or self::section)][contains(@id, "related") or contains(@class, "related")]', \
                 './/*[(self::div or self::section)][contains(@id, "viral") or contains(@class, "viral")]', \
                 # sharing jp-post-flair jp-relatedposts
                 './/*[(self::div or self::section or self::ul)][starts-with(@class, "author-") or starts-with(@id, "shar") or starts-with(@class, "shar") or contains(@class, "share-") or contains(@id, "social") or contains(@class, "social") or contains(@id, "syndication") or contains(@class, "syndication") or starts-with(@id, "jp-") or starts-with(@id, "dpsp-content")]', \
                 './/*[(self::div or self::section)][contains(@id, "author") or contains(@class, "author")]', \
                 './/*[(self::div or self::section or self::span)][contains(@id, "button") or contains(@class, "button")]', \
                 # conflicts: contains(@id, "hidden") or contains(@class, "hidden") or
                 './/*[(self::div or self::section)][contains(@style, "hidden")]', \
                ]
                 # optional??
#                './/*[(self::div or self::section)][contains(@id, "caption") or contains(@class, "caption")]', \
#                './/aside', \ # conflicts with text extraction


COMMENTS_DISCARD_XPATH = ['.//*[(self::div or self::section)][starts-with(@id, "respond")]', \
                          './/cite', \
                          './/quote', \
                          './/*[starts-with(@id, "reply-") or starts-with(@class, "reply-title")]', \
                          './/*[contains(@id, "akismet") or contains(@class, "akismet")]', \
                         ]
