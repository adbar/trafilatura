// General settings for package execution.

// https://www.alexa.com/topsites/countries/DE
// https://www.alexa.com/topsites/countries/US
var BLACKLIST = new Set([
    "360", "akamai", "aliexpress", "amzn", "amazon", "amazonaws", "baidu", "bit",
    "bongacams", "chaturbate", "cloudfront", "daftsex", "delicious", "digg", "ebay",
    "ebay-kleinanzeigen", "facebook", "feedburner", "flickr", "gettyimages", "gmx",
    "google", "gravatar", "http", "imgur", "immobilienscout24", "instagr", "instagram",
    "jd", "last", "linkedin", "live", "livejasmin", "localhost", "mail", "naver",
    "netflix", "office", "ok", "onlyfans", "otto", "paypal", "pinterest", "pornhub",
    "postbank", "qq", "reddit", "redtube", "sina", "sohu", "soundcloud", "spankbang",
    "taobao", "telegram", "tiktok", "tmall", "tnaflix", "twitch", "twitter", "twitpic",
    "txxx", "vk", "vkontakte", "vimeo", "web", "weibo", "whatsapp", "xhamster", "xnxx",
    "xvideos", "yahoo", "yandex", "youjizz", "youporn", "youtube", "youtu", "zoom"
]);

var ALLOWED_PARAMS = new Set([
    "aid", "article_id", "artnr", "id", "itemid", "objectid", "p", "page", "pagenum",
    "page_id", "pid", "post", "postid", "product_id"
]);

var LANG_PARAMS = new Set(["lang", "language"]);

var TARGET_LANGS = {
    "de": new Set(["de", "deutsch", "ger", "german"]),
    "en": new Set(["en", "english", "eng"]) // 'en_US'
};

module.exports = {
    BLACKLIST,
    ALLOWED_PARAMS,
    LANG_PARAMS,
    TARGET_LANGS
};