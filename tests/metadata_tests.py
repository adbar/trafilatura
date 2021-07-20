"""
Unit tests for the kontext library.
"""


import logging
import sys

from os import path

try:
    import cchardet as chardet
except ImportError:
    import chardet

from lxml import html

from trafilatura.metadata import extract_metadata, extract_json, normalize_authors, METADATA_LIST


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = path.abspath(path.dirname(__file__))


MOCK_PAGES = {
'http://blog.python.org/2016/12/python-360-is-now-available.html': 'blog.python.org.html',
'https://creativecommons.org/about/': 'creativecommons.org.html',
'https://www.creativecommons.at/faircoin-hackathon': 'creativecommons.at.faircoin.html',
'https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/': 'blog.wordpress.com.diverse.html',
'https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/': 'netzpolitik.org.abmahnungen.html',
'https://www.befifty.de/home/2017/7/12/unter-uns-montauk': 'befifty.montauk.html',
'https://www.soundofscience.fr/1927': 'soundofscience.fr.1927.html',
'https://laviedesidees.fr/L-evaluation-et-les-listes-de.html': 'laviedesidees.fr.evaluation.html',
'https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens': 'theguardian.com.academics.html',
'https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html': 'phys.org.tool.html',
'https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/': 'gregoryszorc.com.python3.html',
'https://www.pluralsight.com/tech-blog/managing-python-environments/': 'pluralsight.com.python.html',
'https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/': 'stackoverflow.com.rust.html',
'https://www.dw.com/en/berlin-confronts-germanys-colonial-past-with-new-initiative/a-52060881': 'dw.com.colonial.html',
'https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/': 'theplanetarypress.com.forestlands.html',
'https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/': 'wikimediafoundation.org.turkey.html',
'https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH': 'reuters.com.parasite.html',
'https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being': 'nationalgeographic.co.uk.goats.html',
'https://www.nature.com/articles/d41586-019-02790-3': 'nature.com.telescope.html',
'https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/': 'salon.com.emissions.html',
'https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html': 'gofeminin.de.abnehmen.html',
'https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/': 'crazy-julia.de.tipps.html',
'https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis': 'brandenburg.de.homo-brandenburgensis.html',
'https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html': 'skateboardmsm.de.dormhagen.html',
'https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/': 'knowtechie.com.rally.html',
'https://boingboing.net/2013/07/19/hating-millennials-the-preju.html': 'boingboing.net.millenials.html',
'http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/': 'spreeblick.com.habeck.html',
'https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/': 'github.blog.spiceland.html',
'https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer': 'sonntag-sachsen.de.emanuel.html',
'https://www.spiegel.de/spiegel/print/d-161500790.html': 'spiegel.de.albtraum.html',
'https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/': 'lemire.me.json.html',
'https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission': 'zeit.de.zugverkehr.html',
'https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/': 'computerbase.de.htc.html',
'http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html': 'chineselyrics4u.com.zhineng.html',
'https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/': 'meedia.de.freenet.html',
'https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html': 'telemedicus.info.rezension.html',
'https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen': 'cnet.de.schutz.html',
'https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space': 'vice.com.amazon.html',
'https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html': 'heise.de.lithium.html',
'https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html': 'chip.de.beef.html',
'https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html': 'plentylife.blogspot.pamela-reif.html',
'https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/': 'modepilot.de.duschkopf.html',
'http://iloveponysmag.com/2018/05/24/barbour-coastal/': 'iloveponysmag.com.barbour.html',
'https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/': 'moritz-meyer.net.vreni.html',
'https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/': 'spektrum.de.engelbart.html',
'https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/': 'buchperlen.wordpress.com.html',
'http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/': 'kulinariaathome.com.mandelplätzchen.html',
'https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/': 'de.creativecommons.org.endlich.html',
'https://blog.mondediplo.net/turpitude-et-architecture': 'mondediplo.net.turpitude.html',
'https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be': 'scmp.com.playbook.html',
'https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html': 'faz.net.streaming.html',
'https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html': 'ndr.de.podcastcoronavirus140.html',
}


def load_mock_page(url):
    '''Load mock page from samples'''
    try:
        with open(path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = chardet.detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    return htmlstring


def test_titles():
    '''Test the extraction of titles'''
    metadata = extract_metadata('<html><head><title>Test Title</title></head><body></body></html>')
    assert metadata['title'] == 'Test Title'
    metadata = extract_metadata('<html><body><h1>First</h1><h1>Second</h1></body></html>')
    assert metadata['title'] == 'First'
    metadata = extract_metadata('<html><body><h1>   </h1><div class="post-title">Test Title</div></body></html>')
    assert metadata['title'] == 'Test Title'
    metadata = extract_metadata('<html><body><h2>First</h2><h1>Second</h1></body></html>')
    assert metadata['title'] == 'Second'
    metadata = extract_metadata('<html><body><h2>First</h2><h2>Second</h2></body></html>')
    assert metadata['title'] == 'First'
    metadata = extract_metadata('<html><body><title></title></body></html>')
    assert metadata['title'] is None
    metadata = extract_metadata(r'''<html><body><script type="application/ld+json">{"@context":"https:\/\/schema.org","@type":"Article","name":"Semantic satiation","url":"https:\/\/en.wikipedia.org\/wiki\/Semantic_satiation","sameAs":"http:\/\/www.wikidata.org\/entity\/Q226007","mainEntity":"http:\/\/www.wikidata.org\/entity\/Q226007","author":{"@type":"Organization","name":"Contributors to Wikimedia projects"},"publisher":{"@type":"Organization","name":"Wikimedia Foundation, Inc.","logo":{"@type":"ImageObject","url":"https:\/\/www.wikimedia.org\/static\/images\/wmf-hor-googpub.png"}},"datePublished":"2006-07-12T09:27:14Z","dateModified":"2020-08-31T23:55:26Z","headline":"psychological phenomenon in which repetition causes a word to temporarily lose meaning for the listener"}</script>
<script>(RLQ=window.RLQ||[]).push(function(){mw.config.set({"wgBackendResponseTime":112,"wgHostname":"mw2373"});});</script></html>''')
    assert metadata['title'] == 'Semantic satiation'


def test_authors():
    '''Test the extraction of author names'''
    # normalization
    assert normalize_authors(None, 'abc') == 'Abc'
    assert normalize_authors(None, 'Steve Steve 123') == 'Steve Steve'
    assert normalize_authors(None, 'By Steve Steve') == 'Steve Steve'
    # extraction
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith"/><meta itemprop="author" content="John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith und John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith"/><meta name="author" content="John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith and John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><head><meta name="author" content="Jenny Smith ❤️"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><head><meta name="citation_author" content="Jenny Smith and John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta property="author" content="Jenny Smith"/><meta property="author" content="John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><head><meta itemprop="author" content="Jenny Smith and John Smith"/></head><body></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><body><a href="" rel="author">Jenny Smith</a></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span class="author">Jenny Smith</span></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span id="author-name">Jenny Smith</span></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span class="author">Jenny Smith and John Smith</span></body></html>')
    assert metadata['author'] == 'Jenny Smith; John Smith'
    metadata = extract_metadata('<html><body><a class="author">Jenny Smith</a></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a class="author">Jenny Smith from Trafilatura</a></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><a class="username">Jenny Smith</a></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="submitted-by"><a>Jenny Smith</a></div></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span id="author">Jenny Smith</span></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><span itemprop="author name">Shannon Deery, Mitch Clarke, Susie O’Brien, Laura Placella, Kara Irving, Jordy Atkinson, Suzan Delibasic</span></body></html>')
    assert metadata['author'] == 'Shannon Deery; Mitch Clarke; Susie O’Brien; Laura Placella; Kara Irving; Jordy Atkinson; Suzan Delibasic'
    metadata = extract_metadata('<html><body><address class="author">Jenny Smith</address></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><author>Jenny Smith</author></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><p class="author-section byline-plain">By <a class="author" rel="nofollow">Jenny Smith For Daily Mail Australia</a></p></body></html>')
    assert metadata['author'] == 'Jenny Smith'
    metadata = extract_metadata('<html><body><div class="o-Attribution__a-Author"><span class="o-Attribution__a-Author--Label">By:</span><span class="o-Attribution__a-Author--Prefix"><span class="o-Attribution__a-Name"><a href="//web.archive.org/web/20210707074846/https://www.discovery.com/profiles/ian-shive">Ian Shive</a></span></span></div></body></html>')
    assert metadata['author'] == 'Ian Shive'
    metadata = extract_metadata('<html><body><div class="ArticlePage-authors"><div class="ArticlePage-authorName" itemprop="name"><span class="ArticlePage-authorBy">By&nbsp;</span><a aria-label="Ben Coxworth" href="https://newatlas.com/author/ben-coxworth/"><span>Ben Coxworth</span></a></div></div></body></html>')
    assert metadata['author'] == 'Ben Coxworth'
    
    
    ## JSON extraction
    metadata = extract_metadata('''<html><body><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsArticle","description":"The president and his campaign competed again on Monday, with his slash-and-burn remarks swamping news coverage even as his advisers used conventional levers to try to lift his campaign.","image":[{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/2020/10/19/us/politics/19campaign/19campaign-videoSixteenByNineJumbo1600.jpg","height":900,"width":1600,"caption":"In Arizona on Monday, President Trump aired grievances against people including former President Barack Obama and Michelle Obama; Joseph R. Biden Jr. and Hunter Biden; Dr. Anthony S. Fauci; and two female NBC News hosts. "},{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/2020/10/19/us/politics/19campaign/merlin_178764738_11d22ae6-9e7e-4d7a-b28a-20bf52b23e86-superJumbo.jpg","height":1365,"width":2048,"caption":"In Arizona on Monday, President Trump aired grievances against people including former President Barack Obama and Michelle Obama; Joseph R. Biden Jr. and Hunter Biden; Dr. Anthony S. Fauci; and two female NBC News hosts. "},{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/2020/10/19/us/politics/19campaign/19campaign-mediumSquareAt3X.jpg","height":1800,"width":1800,"caption":"In Arizona on Monday, President Trump aired grievances against people including former President Barack Obama and Michelle Obama; Joseph R. Biden Jr. and Hunter Biden; Dr. Anthony S. Fauci; and two female NBC News hosts. "}],"mainEntityOfPage":"https://www.nytimes.com/2020/10/19/us/politics/trump-ads-biden-election.html","url":"https://www.nytimes.com/2020/10/19/us/politics/trump-ads-biden-election.html","inLanguage":"en","author":[{"@context":"http://schema.org","@type":"Person","url":"https://www.nytimes.com/by/maggie-haberman","name":"Maggie Haberman"},{"@context":"http://schema.org","@type":"Person","url":"https://www.nytimes.com/by/shane-goldmacher","name":"Shane Goldmacher"},{"@context":"http://schema.org","@type":"Person","url":"https://www.nytimes.com/by/michael-crowley","name":"Michael Crowley"}],"dateModified":"2020-10-20T01:22:07.000Z","datePublished":"2020-10-19T22:24:02.000Z","headline":"Trump Team Unveils $55 Million Ad Blitz on a Day of Scattershot Attacks","publisher":{"@id":"https://www.nytimes.com/#publisher"},"copyrightHolder":{"@id":"https://www.nytimes.com/#publisher"},"sourceOrganization":{"@id":"https://www.nytimes.com/#publisher"},"copyrightYear":2020,"isAccessibleForFree":false,"hasPart":{"@type":"WebPageElement","isAccessibleForFree":false,"cssSelector":".meteredContent"},"isPartOf":{"@type":["CreativeWork","Product"],"name":"The New York Times","productID":"nytimes.com:basic"}}</script><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsMediaOrganization","name":"The New York Times","logo":{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png","height":40,"width":250},"url":"https://www.nytimes.com/","@id":"https://www.nytimes.com/#publisher","diversityPolicy":"https://www.nytco.com/diversity-and-inclusion-at-the-new-york-times/","ethicsPolicy":"https://www.nytco.com/who-we-are/culture/standards-and-ethics/","masthead":"https://www.nytimes.com/interactive/2019/admin/the-new-york-times-masthead.html","foundingDate":"1851-09-18","sameAs":"https://en.wikipedia.org/wiki/The_New_York_Times"}</script><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"BreadcrumbList","itemListElement":[{"@context":"http://schema.org","@type":"ListItem","name":"U.S.","position":1,"item":"https://www.nytimes.com/section/us"},{"@context":"http://schema.org","@type":"ListItem","name":"Politics","position":2,"item":"https://www.nytimes.com/section/politics"}]}</script></body></html>''')
    assert metadata['author'] == 'Maggie Haberman; Shane Goldmacher; Michael Crowley'
    metadata = extract_metadata('''<html><body><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsArticle","mainEntityOfPage":{"@type":"WebPage","@id":"https://www.perthnow.com.au/news/government-defends-graphic-covid-19-ad-after-backlash-c-3376985"},"dateline":null,"publisher":{"@type":"Organization","name":"PerthNow","url":"https://www.perthnow.com.au","logo":{"@type":"ImageObject","url":"https://www.perthnow.com.au/static/publisher-logos/publisher-logo-60px-high.png","width":575,"height":60}},"keywords":["News","News","Australia","Politics","Federal Politics","News","TAS News"],"articleSection":"News","headline":"Government defends graphic Covid-19 ad after backlash","description":"A graphic COVID-19 ad showing a young woman apparently on the verge of death has prompted a backlash, but the government insists it wasn’t done lightly.","dateCreated":"2021-07-12T00:11:50.000Z","datePublished":"2021-07-12T00:11:50.000Z","dateModified":"2021-07-12T01:25:20.617Z","isAccessibleForFree":"True","articleBody":"The man tasked with co-ordinating Australia&rsquo;s Covid-19 vaccine rollout insists a confronting ad depicting a woman on the verge of death was not run lightly. The 30-second clip, depicting a woman apparently in her 20s or 30s gasping for air on a hospital bed, was filmed last year, but the federal government held off running it as no outbreak was deemed serious enough to warrant it. The government has been forced to defend the ad, reminiscent of the &ldquo;Grim Reaper&rdquo; HIV ads in the 1980s, after it prompted a backlash over claims it was too confronting. A more temperate series of ads, depicting arms on ordinary Australians with the moniker &ldquo;Arm Yourself&rdquo;, began last week, but Covid-19 taskforce commander Lieutenant General John Frewen said the escalating situation in Sydney called for a more explicit response. &ldquo;It is absolutely confronting and we didn&rsquo;t use it lightly. There was serious consideration given to whether it was required and we took expert advice,&rdquo; he told Today on Monday. &ldquo;It is confronting but leaves people in no doubt about the seriousness of getting Covid, and it seeks to have people stay home, get tested and get vaccinated as quickly as they can.&rdquo; NSW on Sunday confirmed another 77 cases, 31 of which had been in the community while infectious, and Premier Gladys Berejiklian warned she would be &ldquo;shocked&rdquo; if the number did not exceed 100 on Monday. General Frewen said the &ldquo;concerning situation&rdquo; had prompted the government to shift an additional 300,000 doses to NSW over the coming fortnight. &ldquo;The Delta variant is proving to be very difficult to contain, so we&rsquo;re working very closely with NSW authorities and standing ready to help them in any way we can,&rdquo; he said. Agriculture Minister David Littleproud said the ad was designed to shock Sydneysiders into action as the situation deteriorated. &ldquo;This is about shooting home that this is a serious situation and can get anybody. The fact we&rsquo;re actually debating this I think says to me that the campaign we&rsquo;ve approved is working,&rdquo; he said. The age of the woman in the ad has sparked controversy, with most younger Australians still ineligible to receive their vaccine. But with 11 of the 52 people in hospital across NSW under 35, Labor frontbencher Tanya Plibersek warned the Delta variant was &ldquo;hitting younger people as well&rdquo;. Labor had long demanded a national Covid-19 advertising campaign, which Ms Plibersek said was delayed as a result of the government&rsquo;s sluggish vaccine rollout. &ldquo;Perhaps the reason it&rsquo;s taken so long is if you encourage people to go and get vaccinated, you&rsquo;ve got to have enough of the vaccine available. We simply haven&rsquo;t; we&rsquo;ve been absolutely behind the eight ball in getting another vaccine for Australians,&rdquo; she told Sunrise. Labor frontbencher Chris Bowen, whose western Sydney electorate was in the grip of the outbreak, said the issue was &ldquo;not vaccine hesitancy so much, it&rsquo;s vaccine scarcity&rdquo;. He accepted there was a role for &ldquo;pointing out the consequences of not getting vaccinated&rdquo; to those that were hesitant about the jab, but said the new campaign lacked the &ldquo;creative spark&rdquo; of the Grim Reaper ads. &ldquo;That was a very tough message, a very stark message, but in a very creative way. I think the government really needs to rethink this advertising campaign from scratch; it&rsquo;s too late, and it&rsquo;s pretty low impact,&rdquo; he told ABC radio. He also dismissed the &ldquo;Arm Yourself&rdquo; campaign as &ldquo;very low energy&rdquo;. &ldquo;I don&rsquo;t think that&rsquo;s going to have any impact,&rdquo; he said.","image":[{"@type":"ImageObject","url":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-16x9-x0y444w1151h647.jpg","width":1151,"height":647},{"@type":"ImageObject","url":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-4x3-x0y336w1151h863.jpg","width":1151,"height":863}],"thumbnailUrl":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-16x9-x0y444w1151h647.jpg","url":"https://www.perthnow.com.au/news/government-defends-graphic-covid-19-ad-after-backlash-c-3376985","author":{"@type":"Organization","name":"NCA NewsWire"},"name":"Government defends graphic Covid-19 ad after backlash"}</script><span itemprop="author name">Jenny Smith</span></span></body></html>''')
    assert metadata['author'] == 'Jenny Smith'
    metadata = dict.fromkeys(METADATA_LIST)
    metadata = extract_json(html.fromstring('''<html><body><script type="application/ld+json" class="yoast-schema-graph">{"@context":"https://schema.org",{"@type":"WebPage","@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage","url":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/","name":"Jean S\u00e9villia : \"L'\u00c9tat fran\u00e7ais et l'\u00c9tat alg\u00e9rien doivent reconna\u00eetre les crimes commis des deux c\u00f4t\u00e9s\" - Boulevard Voltaire","datePublished":"2018-09-13T12:21:13+00:00","dateModified":"2018-09-14T12:33:14+00:00","inLanguage":"fr-FR"},{"@type":"Article","@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#article","isPartOf":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage"},"author":{"@id":"https://www.bvoltaire.fr/#/schema/person/96c0ed8f089950c46afc2044cb23e8da"},"headline":"Jean S\u00e9villia : &#8220;L&#8217;\u00c9tat fran\u00e7ais et l&#8217;\u00c9tat alg\u00e9rien doivent reconna\u00eetre les crimes commis des deux c\u00f4t\u00e9s&#8221;","datePublished":"2018-09-13T12:21:13+00:00","dateModified":"2018-09-14T12:33:14+00:00","mainEntityOfPage":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage"},"publisher":{"@id":"https://www.bvoltaire.fr/#organization"},"image":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#primaryimage"},"keywords":"Guerre d'Alg\u00e9rie","articleSection":"Audio,Editoriaux,Entretiens,Histoire","inLanguage":"fr-FR"},{"@type":"Person","@id":"https://www.bvoltaire.fr/#/schema/person/96c0ed8f089950c46afc2044cb23e8da","name":"Jean S\u00e9villia","image":{"@type":"ImageObject","@id":"https://www.bvoltaire.fr/#personlogo","inLanguage":"fr-FR","url":"https://secure.gravatar.com/avatar/1dd0ad5cb1fc3695880af1725477b22e?s=96&d=mm&r=g","caption":"Jean S\u00e9villia"},"description":"R\u00e9dacteur en chef adjoint au Figaro Magazine, membre du comit\u00e9 scientifique du Figaro Histoire, et auteur de biographies et d\u2019essais historiques.","sameAs":["https://www.bvoltaire.fr/"]}]}</script></body></html>'''), metadata)
    assert metadata['author'] == "Jean Sévillia"


def test_url():
    '''Test URL extraction'''
    metadata = extract_metadata('<html><head><meta property="og:url" content="https://example.org"/></head><body></body></html>')
    assert metadata['url'] == 'https://example.org'
    metadata = extract_metadata('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>')
    assert metadata['url'] == 'https://example.org'
    metadata = extract_metadata('<html><head><meta name="twitter:url" content="https://example.org"/></head><body></body></html>')
    assert metadata['url'] == 'https://example.org'
    metadata = extract_metadata('<html><head><link rel="alternate" hreflang="x-default" href="https://example.org"/></head><body></body></html>')
    assert metadata['url'] == 'https://example.org'


def test_description():
    '''Test the extraction of descriptions'''
    metadata = extract_metadata('<html><head><meta itemprop="description" content="Description"/></head><body></body></html>')
    assert metadata['description'] == 'Description'


def test_dates():
    '''Simple tests for date extraction (most of the tests are carried out externally for htmldate module)'''
    metadata = extract_metadata('<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>')
    assert metadata['date'] == '2017-09-01'
    metadata = extract_metadata('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    assert metadata['date'] == '2017-09-01'
    metadata = extract_metadata('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    assert metadata['date'] == '2017-09-01'
    mystring = '<html><body><p>Veröffentlicht am 1.9.17</p></body></html>'
    metadata = extract_metadata(mystring, fastmode=False)
    assert metadata['date'] == '2017-09-01'
    metadata = extract_metadata(mystring, fastmode=True)
    assert metadata['date'] is None


def test_sitename():
    '''Test extraction of site name'''
    metadata = extract_metadata('<html><head><title>sitemaps.org - Home</title></head><body/></html>')
    assert metadata['sitename'] == 'sitemaps.org'


def test_meta():
    '''Test extraction out of meta-elements'''
    metadata = extract_metadata('<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/><meta property="og:site_name" content="My first site"/><meta property="og:url" content="https://example.org/test"/></head><body><a rel="license" href="https://creativecommons.org/">Creative Commons</a></body></html>')
    assert metadata['title'] == 'Open Graph Title'
    assert metadata['author'] == 'Jenny Smith'
    assert metadata['description'] == 'This is an Open Graph description'
    assert metadata['sitename'] == 'My first site'
    assert metadata['url'] == 'https://example.org/test'
    assert metadata['license'] == 'Creative Commons'
    metadata = extract_metadata('<html><head><meta name="dc.title" content="Open Graph Title"/><meta name="dc.creator" content="Jenny Smith"/><meta name="dc.description" content="This is an Open Graph description"/></head><body></body></html>')
    assert metadata['title'] == 'Open Graph Title'
    assert metadata['author'] == 'Jenny Smith'
    assert metadata['description'] == 'This is an Open Graph description'
    metadata = extract_metadata('<html><head><meta itemprop="headline" content="Title"/></head><body></body></html>')
    assert metadata['title'] == 'Title'
    # catch errors
    assert extract_metadata('') is None
    metadata = extract_metadata('<html><title></title></html>')
    assert metadata['sitename'] is None


def test_catstags():
    '''Test extraction of categories and tags'''
    metadata = extract_metadata('<html><body><p class="entry-categories"><a href="https://example.org/category/cat1/">Cat1</a>, <a href="https://example.org/category/cat2/">Cat2</a></p></body></html>')
    assert metadata['categories'] == ['Cat1', 'Cat2']
    metadata = extract_metadata('<html><body><p class="entry-tags"><a href="https://example.org/tags/tag1/">Tag1</a>, <a href="https://example.org/tags/tag2/">Tag2</a></p></body></html>')
    assert metadata['tags'] == ['Tag1', 'Tag2']


def test_pages():
    '''Test on real web pages'''
    metadata = extract_metadata(load_mock_page('http://blog.python.org/2016/12/python-360-is-now-available.html'))
    assert metadata['title'] == 'Python 3.6.0 is now available!'
    assert metadata['description'] == 'Python 3.6.0 is now available! Python 3.6.0 is the newest major release of the Python language, and it contains many new features and opti...'
    assert metadata['author'] == 'Ned Deily'
    assert metadata['url'] == 'http://blog.python.org/2016/12/python-360-is-now-available.html'
    assert metadata['sitename'] == 'blog.python.org'

    metadata = extract_metadata(load_mock_page('https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/'))
    assert metadata['title'] == 'Want to See a More Diverse WordPress Contributor Community? So Do We.'
    assert metadata['description'] == 'More diverse speakers at WordCamps means a more diverse community contributing to WordPress — and that results in better software for everyone.'
    assert metadata['sitename'] == 'The WordPress.com Blog'
    assert metadata['url'] == 'https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/'

    metadata = extract_metadata(load_mock_page('https://creativecommons.org/about/'))
    assert metadata['title'] == 'What we do - Creative Commons'
    assert metadata['description'] == 'What is Creative Commons? Creative Commons helps you legally share your knowledge and creativity to build a more equitable, accessible, and innovative world. We unlock the full potential of the internet to drive a new era of development, growth and productivity. With a network of staff, board, and affiliates around the world, Creative Commons provides … Read More "What we do"'
    assert metadata['sitename'] == 'Creative Commons'
    assert metadata['url'] == 'https://creativecommons.org/about/'
    # date None

    metadata = extract_metadata(load_mock_page('https://www.creativecommons.at/faircoin-hackathon'))
    assert metadata['title'] == 'FairCoin hackathon beim Sommercamp'
    # assert metadata['url']='/faircoin-hackathon'

    metadata = extract_metadata(load_mock_page('https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/'))
    assert metadata['title'] == 'Die Cider Connection: Abmahnungen gegen Nutzer von Creative-Commons-Bildern'
    assert metadata['author'] == 'Markus Reuter'
    assert metadata['description'] == 'Seit Dezember 2015 verschickt eine Cider Connection zahlreiche Abmahnungen wegen fehlerhafter Creative-Commons-Referenzierungen. Wir haben recherchiert und legen jetzt das Netzwerk der Abmahner offen.'
    assert metadata['sitename'] == 'netzpolitik.org'
    # cats + tags
    assert metadata['url'] == 'https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/'

    metadata = extract_metadata(load_mock_page('https://www.befifty.de/home/2017/7/12/unter-uns-montauk'))
    assert metadata['title'] == 'Das vielleicht schönste Ende der Welt: Montauk'
    assert metadata['author'] == 'Beate Finken'
    assert metadata['description'] == 'Ein Strand, ist ein Strand, ist ein Strand Ein Strand, ist ein Strand, ist ein Strand. Von wegen! In Italien ist alles wohl organisiert, Handtuch an Handtuch oder Liegestuhl an Liegestuhl. In der Karibik liegt man unter Palmen im Sand und in Marbella dominieren Beton und eine kerzengerade Promenade'
    assert metadata['sitename'] == 'BeFifty'
    assert metadata['categories'] == ['Travel', 'Amerika']
    assert metadata['url'] == 'https://www.befifty.de/home/2017/7/12/unter-uns-montauk'

    metadata = extract_metadata(load_mock_page('https://www.soundofscience.fr/1927'))
    assert metadata['title'] == 'Une candidature collective à la présidence du HCERES'
    assert metadata['author'] == 'Martin Clavey'
    assert metadata['description'].startswith('En réaction à la candidature du conseiller recherche')
    assert metadata['sitename'] == 'The Sound Of Science'
    assert metadata['categories'] == ['Politique scientifique française']
    # assert metadata['tags'] == ['évaluation', 'HCERES']
    assert metadata['url'] == 'https://www.soundofscience.fr/1927'

    url = 'https://laviedesidees.fr/L-evaluation-et-les-listes-de.html'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'L’évaluation et les listes de revues'
    assert metadata['author'] == 'Florence Audier'
    assert metadata['description'].startswith("L'évaluation, et la place")
    assert metadata['sitename'] == 'La Vie des idées'
    # assert metadata['categories'] == ['Essai', 'Économie']
    assert metadata['tags'] == []
    # <meta property="og:type" content="article" />
    # <meta name="DC:type" content="journalArticle">
    assert metadata['url'] == 'http://www.laviedesidees.fr/L-evaluation-et-les-listes-de.html'

    metadata = extract_metadata(load_mock_page('https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens'))
    assert metadata['title'] == "Thousands of UK academics 'treated as second-class citizens'"
    assert metadata['author'] == 'Richard Adams'
    assert metadata['description'].startswith('Report claims higher education institutions')
    assert metadata['sitename'] == 'The Guardian' # originally "the Guardian"
    assert metadata['categories'] == ['Education']
    #assert metadata['tags'] == [] ## TODO: check tags
    # meta name="keywords"
    assert metadata['url'] == 'http://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens'

    metadata = extract_metadata(load_mock_page('https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html'))
    assert metadata['title'] == 'Flint flake tool partially covered by birch tar adds to evidence of Neanderthal complex thinking'
    assert metadata['author'] == 'Bob Yirka'
    assert metadata['description'] == 'A team of researchers affiliated with several institutions in The Netherlands has found evidence in small a cutting tool of Neanderthals using birch tar. In their paper published in Proceedings of the National Academy of Sciences, the group describes the tool and what it revealed about Neanderthal technology.'
    # assert metadata['sitename'] == 'Phys'
    # assert metadata['categories'] == ['Archaeology', 'Fossils']
    assert metadata['tags'] == ["Science, Physics News, Science news, Technology News, Physics, Materials, Nanotech, Technology, Science"]
    assert metadata['url'] == 'https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html'

    # metadata = extract_metadata(load_mock_page('https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/'))
    # assert metadata['title'] == "Mercurial's Journey to and Reflections on Python 3"
    # assert metadata['author'] == 'Gregory Szorc'
    # assert metadata['description'] == 'Description of the experience of making Mercurial work with Python 3'
    # assert metadata['sitename'] == 'gregoryszorc'
    # assert metadata['categories'] == ['Python', 'Programming']

    metadata = extract_metadata(load_mock_page('https://www.pluralsight.com/tech-blog/managing-python-environments/'))
    assert metadata['title'] == 'Managing Python Environments'
    assert metadata['author'] == 'John Walk'
    assert metadata['description'].startswith("If you're not careful,")
    # assert metadata['sitename'] == 'Pluralsight'
    # assert metadata['categories'] == ['Python', 'Programming']
    assert metadata['url'] == 'https://www.pluralsight.com/tech-blog/managing-python-environments/'

    url = 'https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'What is Rust and why is it so popular? - Stack Overflow Blog'
    # assert metadata['author'] == 'Jake Goulding'
    assert metadata['sitename'] == 'Stack Overflow Blog'
    assert metadata['categories'] == ['Bulletin']
    assert metadata['tags'] == ['programming', 'rust']
    assert metadata['url'] == url

    url = 'https://www.dw.com/en/berlin-confronts-germanys-colonial-past-with-new-initiative/a-52060881'
    metadata = extract_metadata(load_mock_page(url))
    assert "Berlin confronts Germany's colonial past with new initiative" in metadata['title']
    # assert metadata['author'] == 'Ben Knight' # "Deutsche Welle (www.dw.com)"
    assert metadata['description'] == "The German capital has launched a five-year project to mark its part in European colonialism. Streets which still honor leaders who led the Reich's imperial expansion will be renamed — and some locals aren't happy."
    assert metadata['sitename'] == 'DW.COM' # 'DW - Deutsche Welle'
    # assert metadata['categories'] == ['Colonialism', 'History', 'Germany']
    assert metadata['url'] == url

    metadata = extract_metadata(load_mock_page('https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/'))
    #print(metadata)
    #sys.exit()
    # assert metadata['title'] == 'Management of Intact Forestlands by Indigenous Peoples Key to Protecting Climate'
    # assert metadata['author'] == 'Julie Mollins'
    assert metadata['sitename'] == 'The Planetary Press'
    # assert metadata['categories'] == ['Indigenous People', 'Environment']
    assert metadata['url'] == 'https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/'

    url = 'https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Access to Wikipedia restored in Turkey after more than two and a half years'
    assert metadata['author'] == 'Wikimedia Foundation'
    # assert metadata['description'] == 'Report about the restored accessibility of Wikipedia in Turkey'
    assert metadata['sitename'] == 'Wikimedia Foundation'
    # assert metadata['categories'] == ['Politics', 'Turkey', 'Wikipedia']
    assert metadata['url'] == url

    url = 'https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'].endswith('scores historic upset at SAG awards, boosting Oscar chances') # &#039;Parasite&#039;
    assert metadata['author'] == 'Jill Serjeant'
    assert metadata['date'] == '2020-01-20'
    # assert metadata['description'] == '“Parasite,” the Korean language social satire about the wealth gap in South Korea, was the first film in a foreign language to win the top prize of best cast ensemble in the 26 year-history of the SAG awards.'
    # assert metadata['sitename'] == 'Reuters'
    # assert metadata['categories'] == ['Parasite', 'SAG awards', 'Cinema']
    # print(metadata)
    # assert metadata['url'] == 'https://www.reuters.com/article/us-awards-sag-idUSKBN1ZI0EH'

    url = 'https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == "Ravenous wild goats ruled this island for over a century. Now, it's being reborn."
    assert metadata['author'] == 'Michael Hingston'
    assert metadata['description'].startswith('The rocky island of Redonda, once stripped of its flora and fauna')
    assert metadata['sitename'] == 'National Geographic'
    # assert metadata['categories'] == ['Goats', 'Environment', 'Redonda']
    assert metadata['url'] == url

    url = 'https://www.nature.com/articles/d41586-019-02790-3'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Gigantic Chinese telescope opens to astronomers worldwide'
    assert metadata['author'] == 'Elizabeth Gibney'
    assert metadata['description'] == 'FAST has superior sensitivity to detect cosmic phenomena, including fast radio bursts and pulsars.'
    # assert metadata['sitename'] == 'Nature'
    # assert metadata['categories'] == ['Astronomy', 'Telescope', 'China']
    assert metadata['url'] == url

    url = 'https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Carrie Lam should study Tsai Ing-wen’s playbook' # '<h1 data-v-1223d442="" class="inner__main-headline main-headline">Taiwanese President Tsai Ing-wen’s political playbook should be essential reading for Hong Kong leader Carrie Lam</h1>'
    # author in JSON-LD
    assert metadata['author'] == 'Alice Wu'
    assert metadata['url'] == url

    url = 'https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Nutzerbasierte Abrechnung: Musik-Stars fordern neues Streaming-Modell'
    # author overriden from JSON-LD + double name
    assert 'Benjamin Fischer' in metadata['author']
    assert metadata['sitename'] == 'Frankfurter Allgemeine Zeitung'
    assert metadata['url'] == 'https://www.faz.net/1.6604622'

    url = 'https://boingboing.net/2013/07/19/hating-millennials-the-preju.html'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == "Hating Millennials - the prejudice you're allowed to boast about"
    assert metadata['author'] == 'Cory Doctorow'
    assert metadata['sitename'] == 'Boing Boing'
    assert metadata['url'] == url

    url = 'https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Wie kann ich schnell abnehmen? Der Schlachtplan zum Wunschgewicht'
    assert metadata['author'] == 'Diane Buckstegge'
    assert metadata['sitename'] == 'Gofeminin' # originally "gofeminin"
    assert metadata['url'] == url

    url = 'https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Leader spotlight: Erin Spiceland'
    assert metadata['author'] == 'Jessica Rudder'
    assert metadata['description'].startswith('We’re spending Women’s History')
    assert metadata['sitename'] == 'The GitHub Blog'
    assert metadata['categories'] == ['Community']
    assert metadata['url'] == url

    url = 'https://www.spiegel.de/spiegel/print/d-161500790.html'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Ein Albtraum'
    # print(metadata)
    # assert metadata['author'] == 'Clemens Höges'

    url = 'https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['title'] == 'Despite everything, U.S. emissions dipped in 2019'
    # in JSON-LD
    assert metadata['author'] == 'Nathanael Johnson'
    assert metadata['sitename'] == 'Salon.com'
    # in header
    assert 'Science & Health' in metadata['categories']
    assert 'Gas Industry' in metadata['tags'] and 'coal emissions' in metadata['tags']
    assert metadata['url'] == url

    url = 'https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html'
    metadata = extract_metadata(load_mock_page(url))
    assert metadata['url'] == url
    assert 'Korinna Hennig' in metadata['author']
    assert 'Ältere Menschen' in str(metadata['tags'])


if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()
    test_url()
    test_description()
    test_catstags()
    test_sitename()
    test_pages()
