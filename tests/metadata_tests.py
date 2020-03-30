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

from trafilatura.metadata import scrape


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
    metadata = scrape('<html><head><title>Test Title</title></head><body></body></html>')
    assert metadata.title == 'Test Title'
    metadata = scrape('<html><body><h1>First</h1><h1>Second</h1></body></html>')
    assert metadata.title == 'First'
    metadata = scrape('<html><body><h2>First</h2><h1>Second</h1></body></html>')
    assert metadata.title == 'Second'
    metadata = scrape('<html><body><h2>First</h2><h2>Second</h2></body></html>')
    assert metadata.title == 'First'


def test_authors():
    '''Test the extraction of author names'''
    metadata = scrape('<html><head><meta itemprop="author" content="Jenny Smith"/></head><body></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = scrape('<html><body><a href="" rel="author">Jenny Smith</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = scrape('<html><body><span class="author">Jenny Smith</span></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = scrape('<html><body><a class="author">Jenny Smith</a></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = scrape('<html><body><address class="author">Jenny Smith</address></body></html>')
    assert metadata.author == 'Jenny Smith'
    metadata = scrape('<html><body><author>Jenny Smith</author></body></html>')
    assert metadata.author == 'Jenny Smith'


def test_url():
    '''Test the extraction of author names'''
    metadata = scrape('<html><head><meta property="og:url" content="https://example.org"/></head><body></body></html>')
    assert metadata.url == 'https://example.org'
    metadata = scrape('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>')
    assert metadata.url == 'https://example.org'


def test_dates():
    '''Simple tests for date extraction (most of the tests are carried out externally for htmldate module)'''
    metadata = scrape('<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>')
    assert metadata.date == '2017-09-01'
    metadata = scrape('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    print(metadata)
    assert metadata.date == '2017-09-01'


def test_meta():
    '''Test extraction out of meta-elements'''
    metadata = scrape('<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/><meta property="og:site_name" content="My first site"/></head><body></body></html>')
    assert metadata.title == 'Open Graph Title'
    assert metadata.author == 'Jenny Smith'
    assert metadata.description == 'This is an Open Graph description'
    assert metadata.sitename == 'My first site'
    metadata = scrape('<html><head><meta name="dc.title" content="Open Graph Title"/><meta name="dc.creator" content="Jenny Smith"/><meta name="dc.description" content="This is an Open Graph description"/></head><body></body></html>')
    assert metadata.title == 'Open Graph Title'
    assert metadata.author == 'Jenny Smith'
    assert metadata.description == 'This is an Open Graph description'


def test_catstags():
    '''Test extraction of categories and tags'''
    metadata = scrape('<html><body><p class="entry-categories"><a href="https://example.org/category/cat1/">Cat1</a>, <a href="https://example.org/category/cat2/">Cat2</a></p></body></html>')
    assert metadata.categories == ['Cat1', 'Cat2']
    metadata = scrape('<html><body><p class="entry-tags"><a href="https://example.org/tags/tag1/">Tag1</a>, <a href="https://example.org/tags/tag2/">Tag2</a></p></body></html>')
    assert metadata.tags == ['Tag1', 'Tag2']


def test_pages():
    '''Test on real web pages'''
    metadata = scrape(load_mock_page('http://blog.python.org/2016/12/python-360-is-now-available.html'))
    assert metadata.title == 'Python 3.6.0 is now available!'
    assert metadata.description == 'Python 3.6.0 is now available! Python 3.6.0 is the newest major release of the Python language, and it contains many new features and opti...'
    # author = span class="post-author"

    metadata = scrape(load_mock_page('https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/'))
    assert metadata.title == 'Want to See a More Diverse WordPress Contributor Community? So Do We.'
    assert metadata.description == 'More diverse speakers at WordCamps means a more diverse community contributing to WordPress — and that results in better software for everyone.'
    assert metadata.sitename == 'The WordPress.com Blog'

    metadata = scrape(load_mock_page('https://creativecommons.org/about/'))
    assert metadata.title == 'What we do - Creative Commons'
    assert metadata.description == 'What is Creative Commons? Creative Commons helps you legally share your knowledge and creativity to build a more equitable, accessible, and innovative world. We unlock the full potential of the internet to drive a new era of development, growth and productivity. With a network of staff, board, and affiliates around the world, Creative Commons provides … Read More "What we do"'
    assert metadata.sitename == 'Creative Commons'
    # date None

    metadata = scrape(load_mock_page('https://www.creativecommons.at/faircoin-hackathon'))
    assert metadata.title == 'FairCoin hackathon beim Sommercamp'
    # url='/faircoin-hackathon'
    # print(metadata)

    metadata = scrape(load_mock_page('https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/'))
    assert metadata.title == 'Die Cider Connection: Abmahnungen gegen Nutzer von Creative-Commons-Bildern'
    assert metadata.author == 'Markus Reuter'
    assert metadata.description == 'Seit Dezember 2015 verschickt eine Cider Connection zahlreiche Abmahnungen wegen fehlerhafter Creative-Commons-Referenzierungen. Wir haben recherchiert und legen jetzt das Netzwerk der Abmahner offen.'
    assert metadata.sitename == 'netzpolitik.org'
    # cats + tags

    metadata = scrape(load_mock_page('https://www.befifty.de/home/2017/7/12/unter-uns-montauk'))
    assert metadata.title == 'Das vielleicht schönste Ende der Welt: Montauk'
    assert metadata.author == 'Beate Finken'
    assert metadata.description == 'Ein Strand, ist ein Strand, ist ein Strand Ein Strand, ist ein Strand, ist ein Strand. Von wegen! In Italien ist alles wohl organisiert, Handtuch an Handtuch oder Liegestuhl an Liegestuhl. In der Karibik liegt man unter Palmen im Sand und in Marbella dominieren Beton und eine kerzengerade Promenade'
    assert metadata.sitename == 'BeFifty'
    assert metadata.categories == ['Travel', 'Amerika']
 
    metadata = scrape(load_mock_page('https://www.soundofscience.fr/1927'))
    assert metadata.title == 'Une candidature collective à la présidence du HCERES'
    # assert metadata.author == 'Martin Clavey'
    assert metadata.description.startswith('En réaction à la candidature du conseiller recherche')
    assert metadata.sitename == 'The Sound Of Science'
    assert metadata.categories == ['Politique scientifique française']
    # assert metadata.tags == ['évaluation', 'HCERES']

    metadata = scrape(load_mock_page('https://laviedesidees.fr/L-evaluation-et-les-listes-de.html'))
    assert metadata.title == 'L’évaluation et les listes de revues'
    assert metadata.author == 'Florence Audier'
    assert metadata.description.startswith("L'évaluation, et la place")
    assert metadata.sitename == 'La Vie des idées'
    # assert metadata.categories == ['Essai', 'Économie']
    assert metadata.tags == []
    # <meta property="og:type" content="article" />
    # <meta name="DC:type" content="journalArticle">

    metadata = scrape(load_mock_page('https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens'))
    assert metadata.title == "Thousands of UK academics 'treated as second-class citizens'"
    # assert metadata.author == 'Richard Adams'
    assert metadata.description.startswith('Report claims higher education institutions')
    assert metadata.sitename == 'the Guardian'
    assert metadata.categories == []
    assert metadata.tags == []
    # meta name="keywords"

    metadata = scrape(load_mock_page('https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html'))
    assert metadata.title == 'Flint flake tool partially covered by birch tar adds to evidence of Neanderthal complex thinking'
    assert metadata.author == 'Bob Yirka'
    assert metadata.description == 'A team of researchers affiliated with several institutions in The Netherlands has found evidence in small a cutting tool of Neanderthals using birch tar. In their paper published in Proceedings of the National Academy of Sciences, the group describes the tool and what it revealed about Neanderthal technology.'
    # assert metadata.sitename == 'Phys'
    # assert metadata.categories == ['Archaeology', 'Fossils']

    # metadata = scrape(load_mock_page('https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/'))
    # assert metadata.title == "Mercurial's Journey to and Reflections on Python 3"
    # assert metadata.author == 'Gregory Szorc'
    # assert metadata.description == 'Description of the experience of making Mercurial work with Python 3'
    # assert metadata.sitename == 'gregoryszorc'
    # assert metadata.categories == ['Python', 'Programming']
    
    metadata = scrape(load_mock_page('https://www.pluralsight.com/tech-blog/managing-python-environments/'))
    assert metadata.title == 'Managing Python Environments'
    # assert metadata.author == 'John Walk'
    # assert metadata.description == 'pros and cons of available tools for python setup'
    # assert metadata.sitename == 'Pluralsight'
    # assert metadata.categories == ['Python', 'Programming']
    
    # metadata = scrape(load_mock_page('https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/'))
    # assert metadata.title == 'What is Rust and why is it so popular?'
    # assert metadata.author == 'Jake Goulding'
    # assert metadata.description == 'Description of the Programming Language Rust'
    # assert metadata.sitename == 'Stack Overflow'
    # assert metadata.categories == ['Rust', 'Programming']
    
    # metadata = scrape(load_mock_page('https://www.dw.com/en/berlin-confronts-germanys-colonial-past-with-new-initiative/a-52060881'))
    # print(metadata)
    # sys.exit()
    # assert metadata.title == "Berlin confronts Germany's colonial past with new initiative"
    # assert metadata.author == 'Ben Knight'
    # assert metadata.description == "The German capital has launched a five-year project to mark its part in European colonialism. Streets which still honor leaders who led the Reich's imperial expansion will be renamed — and some locals aren't happy."
    # assert metadata.sitename == 'DW - Deutsche Welle'
    # assert metadata.categories == ['Colonialism', 'History', 'Germany']
    
    # metadata = scrape(load_mock_page('https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/'))
    # print(metadata)
    # sys.exit()
    # assert metadata.title == 'Management of Intact Forestlands by Indigenous Peoples Key to Protecting Climate'
    # assert metadata.author == 'Julie Mollins'
    # assert metadata.description == 'Advantages of Management of Intact Forestlands by Indigenous Peoples for the Climate'
    # assert metadata.sitename == 'The Planetary Press'
    # assert metadata.categories == ['Indigenous People', 'Environment']
    
    metadata = scrape(load_mock_page('https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/'))
    assert metadata.title == 'Access to Wikipedia restored in Turkey after more than two and a half years'
    assert metadata.author == 'Wikimedia Foundation'
    # assert metadata.description == 'Report about the restored accessibility of Wikipedia in Turkey'
    assert metadata.sitename == 'Wikimedia Foundation'
    # assert metadata.categories == ['Politics', 'Turkey', 'Wikipedia']
    
    metadata = scrape(load_mock_page('https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH'))
    assert metadata.title == "'Parasite' scores historic upset at SAG awards, boosting Oscar chances"
    assert metadata.author == 'Jill Serjeant'
    assert metadata.date == '2020-01-20'
    # assert metadata.description == '“Parasite,” the Korean language social satire about the wealth gap in South Korea, was the first film in a foreign language to win the top prize of best cast ensemble in the 26 year-history of the SAG awards.'
    # assert metadata.sitename == 'Reuters'
    # assert metadata.categories == ['Parasite', 'SAG awards', 'Cinema']
    
    metadata = scrape(load_mock_page('https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being'))
    assert metadata.title == "Ravenous wild goats ruled this island for over a century. Now, it's being reborn."
    # assert metadata.author == 'Michael Hingston' # National Geographic
    # assert metadata.description == 'The rocky island of Redonda, once stripped of its flora and fauna by invasive species, makes an astonishingly quick comeback. What’s the secret to its recovery?'
    assert metadata.sitename == 'National Geographic'
    # assert metadata.categories == ['Goats', 'Environment', 'Redonda']
    
    metadata = scrape(load_mock_page('https://www.nature.com/articles/d41586-019-02790-3'))
    assert metadata.title == 'Gigantic Chinese telescope opens to astronomers worldwide'
    assert metadata.author == 'Elizabeth Gibney'
    assert metadata.description == 'FAST has superior sensitivity to detect cosmic phenomena, including fast radio bursts and pulsars.'
    # assert metadata.sitename == 'Nature'
    # assert metadata.categories == ['Astronomy', 'Telescope', 'China']
    
    metadata = scrape(load_mock_page('https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/'))
    assert metadata.title == 'Despite everything, U.S. emissions dipped in 2019'
    # author in JSON-LD
    assert metadata.author == 'Nathanael Johnson'
    assert metadata.description == 'Coal has been in a slow-motion death spiral over the past ten years'
    assert metadata.sitename == 'Salon'
    # assert metadata.categories == ['Coal', 'Emmisions', 'Climate']

    metadata = scrape(load_mock_page('https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be'))
    # author in JSON-LD
    assert metadata.author == 'Alice Wu'

    metadata = scrape(load_mock_page('https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html'))
    # author overriden from JSON-LD + double name
    assert 'Benjamin Fischer' in metadata.author


if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()
    test_url()
    test_catstags()
    test_pages()
