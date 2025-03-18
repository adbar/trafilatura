# pylint:disable-msg=E0611
"""
X-Path expressions used to extract or filter the main text content,
and to extract metadata.
"""

from lxml.etree import XPath



regexpNS = 'http://exslt.org/regular-expressions'


### 1. CONTENT

BODY_XPATH = [
    XPath(
    '''
        .//*[self::article or self::div or self::main or self::section][
        @class='post' or @class='entry' or
        @itemprop='articleBody' or @id='articleContent' or
        re:test(@id, '(?:entry|article|art)-content|article__content|article(?:-|__)?body|articleBody|body-text') or
        re:test(@class, 'post[-_]text|post-body|post-?entry|post[-_]?content|postContent|post_inner_wrapper|article-?text|articleText|(?:entry|page|text|article|art)-content|article__content|article(?:-|__)?body|articleBody|ArticleContent|body-text|article__container')
        ][1]
        ''',
        namespaces={'re': regexpNS}
    ),
    # (…)[1] = first occurrence
    XPath('(.//article)[1]'),
    XPath(
        '''
        (.//*[self::article or self::div or self::main or self::section][
        @role='article' or
        @id='article' or @id='story' or
        @class='postarea' or @class='art-postcontent' or @class='text' or @class='cell' or @class='story' or
        re:test(@id, '^primary|story-body') or
        contains(translate(@class, 'FULTEX','fultex'), 'fulltext') or
        re:test(@class, '^article |post-bodycopy|story-?content|(?:theme|blog|section|single)-content|single-post|main-column|wpb_text_column|story-body|field-body')
        ])[1]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        '''
        (.//*[self::article or self::div or self::main or self::section][
        @id='content' or @class='content' or
        re:test(@id, 'content-main|content-body|contentBody') or
        re:test(@class, 'content[-_]main|content(?:-|__)body') or
        contains(translate(@id, 'CM','cm'), 'main-content') or contains(translate(@class, 'CM','cm'), 'main-content') or
        contains(translate(@class, 'CP','cp'), 'page-content')
        ])[1]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        '''
        (.//*[self::article or self::div or self::section][
        starts-with(@class, 'main') or starts-with(@id, 'main') or starts-with(@role, 'main')])[1]|(.//main)[1]
        '''
    )
]
# starts-with(@id, "article") or
# or starts-with(@id, "story") or contains(@class, "story")
# starts-with(@class, "content ") or contains(@class, " content")
# '//div[contains(@class, "text") or contains(@class, "article-wrapper") or contains(@class, "content-wrapper")]',
# '//div[contains(@class, "article-wrapper") or contains(@class, "content-wrapper")]',
# |//*[self::article or self::div or self::main or self::section][contains(@class, "article") or contains(@class, "Article")]
# @id="content"or @class="content" or @class="Content"
# or starts-with(@class, 'post ')
# './/span[@class=""]', # instagram?


COMMENTS_XPATH = [
    XPath(
        '''
        .//*[self::div or self::list or self::section][
        re:test(@id|@class, 'comment-?list') or
        re:test(@class, 'comment-page|comments-content|post-comments')]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        '''
        .//*[self::div or self::section or self::list][
        re:test(@id|@class, '^comment[s-]') or
        re:test(@class, '^Comments|article-comments')]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        '''
        .//*[self::div or self::section or self::list][
        re:test(@id, '^(?:comol|disqus_thread|dsq-comments)')]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        '''
        .//*[self::div or self::section][
        starts-with(@id, 'social') or contains(@class, 'comment')]
        '''
    )
]
# or contains(@class, 'Comments')

REMOVE_COMMENTS_XPATH = [
    XPath(
        '''
        .//*[self::div or self::list or self::section][
        re:test(@id, '^(?:[Cc]omment|comol|disqus_thread|dsq-comments)') or
        re:test(@class, '^[Cc]omment|(?:article|post)-comments')]
        ''',
        namespaces={'re': regexpNS}
    )
]
# or self::span
# or contains(@class, 'comment') or contains(@id, 'comment')


OVERALL_DISCARD_XPATH = [
    XPath(
        '''
        .//*[self::div or self::item or self::list or self::p or self::section or self::span][
        @data-lp-replacement-content or
        contains(translate(@role, 'N', 'n'), 'nav') or
        contains(@data-component, 'MostPopularStories') or
        re:test(@id|@class, '^shar|viral|social|syndication|newsletter|cookie|tags|sidebar|banner|bread-?crumb|author|button') or
        re:test(@id, '^(?:jp-|dpsp-content)|footer|Footer|share|Share|nav|Nav|related|menu|message-container|bmdh|premium') or
        re:test(@class, '^(?:nav|post-nav|ZendeskForm)| ad |footer|Footer|byline|Byline|elated|share-|sociable|embedded|embed|subnav|tag-list|bar|meta|menu|avigation|navbar|navbox|rating|widget|attachment|timestamp|user-info|user-profile|-ad-|-icon|article-infos|nfoline|outbrain|taboola|criteo|options|expand|consent|modal-content|permission|next-|-stories|most-popular|mol-factbox|message-container|yin|zlylin|xg1|slide|viewport|overlay|paid-?content|obfuscated|blurred')]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        '''
        .//*[@class='comments-title' or
        starts-with(@id|@class, 'reply-') or
        re:test(@id|@style, 'hidden') or
        contains(@style, 'display:none') or contains(@style, 'display: none') or
        re:test(@id, 'reader-comments|akismet') or
        re:test(@class, '^hide-|comments-title|nocomments|-reply-|message|akismet|suggest-links|-hide-|hide-print| hidden| hide|noprint|notloaded') or @aria-hidden='true']
        ''',
        namespaces={'re': regexpNS}
    )
]

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
    '''
    .//*[self::div or self::item or self::list or self::p or self::section or self::span][
    contains(translate(@id, 'T', 't'), 'teaser') or contains(translate(@class, 'T', 't'), 'teaser')]
    '''
)]


PRECISION_DISCARD_XPATH = [XPath(x) for x in (
    '''.//header''',
    '''
    .//*[self::div or self::item or self::list or self::p or self::section or self::span][
    contains(@id|@class, 'bottom') or contains(@id|@class, 'link') or contains(@style, 'border')]
    ''',
)]
# or contains(@id, "-comments") or contains(@class, "-comments")


DISCARD_IMAGE_ELEMENTS = [XPath(
    '''
    .//*[self::div or self::item or self::list or self::p or self::section or self::span][
    contains(@id, 'caption') or contains(@class, 'caption')]
    '''
)]


COMMENTS_DISCARD_XPATH = [
    XPath('''.//*[self::div or self::section][starts-with(@id, 'respond')]'''),
    XPath('''.//cite|.//quote'''),
    XPath(
        '''
        .//*[
        @class='comments-title' or 
        contains(@style, 'display:none') or
        re:test(@class, 'comments-title|nocomments|-reply-|message|signin') or
        re:test(@id|@class, '^reply-|akismet')]
        ''',
        namespaces={'re': regexpNS}
    )
]



### 2. METADATA


# the order or depth of XPaths could be changed after exhaustive testing
AUTHOR_XPATHS = [
    XPath(
        # specific and almost specific
        '''
        //*[self::a or self::address or self::div or self::link or self::p or self::span or self::strong][
        @rel='author' or @id='author' or @class='author' or @itemprop='author name' or rel='me' or
        @data-testid='AuthorCard' or @data-testid='AuthorURL' or
        re:test(@class, 'author-name|AuthorName|authorName|author name')]|//author
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath(
        # almost generic and generic, last ones not common
        '''
        //*[self::a or self::div or self::h3 or self::h4 or self::p or self::span][
        @class='byline' or @class='username' or @class='byl' or @class='BBL' or
        contains(@itemprop, 'author') or
        re:test(@id, 'author|zuozhe|bianji|xiaobian') or
        re:test(@class, 'author|channel-name|zuozhe|bianji|xiaobian|submitted-by|posted-by|journalist-name')]
        '''
    ),
    XPath(
         # last resort: any element
        '''
        //*[
        contains(@data-component, 'Byline') or contains(@itemprop, 'author') or
        re:test(@id, '[Aa]uthor') or
        re:test(@class, '[Aa]uthor|screenname|writer|[Bb]yline')]
        ''',
        namespaces={'re': regexpNS}
    )
]


AUTHOR_DISCARD_XPATHS = [
    XPath(
        '''
        .//*[self::a or self::div or self::section or self::span][
        @id='comments' or @class='comments' or @class='title' or @class='date' or
        re:test(@id, '^comments|comment-?list|ProductReviews') or
        re:test(@class, '^[Cc]omments|commentlist|comments-list|sidebar|is-hidden|quote|embedly-instagram|article-(?:share|support)|print|category|meta-date|meta-reviewer') or
        contains(@data-component, 'Figure')]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath('//time|//figure')]


CATEGORIES_XPATHS = [
    XPath(
        '''
        //div[
        re:test(@class, '^(?:post-?info|post-?meta|meta|entry-(?:meta|info|utility))') or
        starts-with(@id, 'postpath')]//a[@href]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath('''//p[starts-with(@class, 'postmeta') or starts-with(@class, 'entry-categories') or
     @class='postinfo' or @id='filedunder']//a[@href]'''),
    XPath('''//footer[starts-with(@class, 'entry-meta') or starts-with(@class, 'entry-footer')]//a[@href]'''),
    XPath('''//*[self::li or self::span][@class='post-category' or @class='postcategory' or
     @class='entry-category' or contains(@class, 'cat-links')]//a[@href]'''),
    XPath('''//header[@class='entry-header']//a[@href]'''),
    XPath('''//div[@class='row' or @class='tags']//a[@href]''')]
# "//*[self::div or self::p][contains(@class, 'byline')]",


TAGS_XPATHS = [
    XPath('''//div[@class='tags']//a[@href]'''),
    XPath('''//p[starts-with(@class, 'entry-tags')]//a[@href]'''),
    XPath('''//div[@class='row' or @class='jp-relatedposts' or @class='entry-utility' or 
    re:test(@class, '^(?:tag|postmeta|meta)')]//a[@href]'''),
    XPath('''//*[@class='entry-meta' or contains(@class, 'topics') or
     contains(@class, 'tags-links')]//a[@href]''')
]
# "related-topics"
# https://github.com/grangier/python-goose/blob/develop/goose/extractors/tags.py


TITLE_XPATHS = [
    XPath(
        '''
        //*[self::h1 or self::h2][
        re:test(@class, '(?:post-|entry-|article-|post__)title|headline') or 
        contains(@id, 'headline') or contains(@itemprop, 'headline')]
        ''',
        namespaces={'re': regexpNS}
    ),
    XPath('''//*[@class='entry-title' or @class='post-title']'''),
    XPath('''//*[self::h1 or self::h2 or self::h3][
    contains(@class, 'title') or contains(@id, 'title')]''')
]
# json-ld headline
# '//header/h1',
