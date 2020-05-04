# pylint:disable-msg=W1401
"""
Unit tests for the trafilatura library.
"""

import logging
import os
import sys

from collections import namedtuple
from unittest.mock import patch

import pytest
# https://docs.pytest.org/en/latest/


from lxml import etree, html

try:
    import cchardet as chardet
except ImportError:
    import chardet
    
# language detection
try:
    import langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

import trafilatura.filters
from trafilatura.core import baseline, extract, process_record, trim
from trafilatura.filters import duplicate_test, put_in_cache, textfilter
from trafilatura.lru import LRUCache
from trafilatura import cli, utils, xml

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

MOCK_PAGES = {
'http://exotic_tags': 'exotic_tags.html',
'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/': 'die-partei.net.luebeck.html',
'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html': 'bmjv.de.konsum.html',
'http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/': 'kulinariaathome.com.mandelplätzchen.html',
'https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/': 'denkanstoos.com.2012.html',
'https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft': 'demokratiewebstatt.at.luft.html',
'http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html': 'toralin.de.schmierfett.html',
'https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess': 'ebrosia.de.zinfandel.html',
'https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html': 'landwirt.com.sensortechnik.html',
'http://schleifen.ucoz.de/blog/briefe/2010-10-26-18': 'schleifen.ucoz.de.briefe.html',
'http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung': 'rs-ingenieure.de.tragwerksplanung.html',
'http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html': 'simplyscience.ch.erdoel.html',
'http://www.shingon-reiki.de/reiki-und-schamanismus/': 'shingon-reiki.de.schamanismus.html',
'http://love-hina.ch/news/0409.html': 'love-hina.ch.0409.html',
'http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html': 'cdu-fraktion-erfurt.de.waldorfschule.html',
'http://www.wehranlage-horka.de/veranstaltung/887/': 'wehranlage-horka.de.887.html',
'https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/': 'de.creativecommons.org.endlich.html',
'https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/': 'piratenpartei-mv.de.grundeinkommen.html',
'https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/': 'spektrum.de.engelbart.html',
'https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html': 'rnz.de.witzel.html',
'https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg': 'austria.info.radfahren.html',
'https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/': 'buchperlen.wordpress.com.html',
'https://www.fairkom.eu/about': 'fairkom.eu.about.html',
'https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461': 'futurezone.at.lyft.html',
'http://www.hundeverein-kreisunna.de/unserverein.html': 'hundeverein-kreisunna.de.html',
'https://viehbacher.com/de/steuerrecht': 'viehbacher.com.steuerrecht.html',
'http://www.jovelstefan.de/2011/09/11/gefallt-mir/': 'jovelstefan.de.gefallt.html',
'https://www.stuttgart.de/item/show/132240/1': 'stuttgart.de.html',
'https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/': 'modepilot.de.duschkopf.html',
'https://www.otto.de/twoforfashion/strohtasche/': 'otto.de.twoforfashion.html',
'http://iloveponysmag.com/2018/05/24/barbour-coastal/': 'iloveponysmag.com.barbour.html',
'https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/': 'moritz-meyer.net.vreni.html',
'http://www.womencantalksports.com/top-10-women-talking-sports/': 'womencantalksports.com.top10.html',
'https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html': 'plentylife.blogspot.pamela-reif.html',
'https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html': 'luxuryhaven.co.hyatt.html',
'https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/': 'luxuriousmagazine.com.polo.html',
'https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5': 'chip.de.tests.html',
'https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/': 'gruen-digital.de.jahrestagung.html',
'https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/': 'rechtambild.de.kochbuch.html',
'http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html': 'internet-law.de.pseudonymen.html',
'https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html': 'telemedicus.info.rezension.html',
'https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen': 'cnet.de.schutz.html',
'https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage': 'correctiv.org.zusage.html',
'https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845': 'sueddeutsche.de.flixtrain.html',
'https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/': 'adac.de.kindersitze.html',
'https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/': 'caktusgroup.com.django.html',
'https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/': 'computerbase.de.htc.html',
'http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html': 'chineselyrics4u.com.zhineng.html',
'https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/': 'basicthinking.de.tweets.html',
'https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/': 'meedia.de.freenet.html',
'https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/': 'incurvy.de.wellness.html',
'https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843': 'dw.com.uncork.html',
'https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html': 'jolie.de.adele.html',
'https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx': 'speicherguide.de.schwierige.html',
'https://novalanalove.com/ear-candy/': 'novalanalove.com.ear-candy.html',
'http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/': 'franziska-elea.de.vuitton.html',
'https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html': 'gofeminin.de.abnehmen.html',
'https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html': 'brigitte.de.ikigai.html',
'https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/': 'changelog.blog.zwischenbilanz.html',
'https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/': 'threatpost.com.android.html',
'https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space': 'vice.com.amazon.html',
'https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html': 'heise.de.lithium.html',
'https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact': 'theverge.com.ios13.html',
'https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/': 'crazy-julia.de.tipps.html',
'https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis': 'brandenburg.de.homo-brandenburgensis.html',
'https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html': 'skateboardmsm.de.dormhagen.html',
'https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/': 'knowtechie.com.rally.html',
'https://boingboing.net/2013/07/19/hating-millennials-the-preju.html': 'boingboing.net.millenials.html',
'https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding': 'en.wikipedia.org.tsne.html',
'https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/': 'mixed.de.vrodo.html',
'http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/': 'spreeblick.com.habeck.html',
'https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/': 'majkaswelt.com.fashion.html',
'https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/': 'erp-news.info.interview.html',
'https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/': 'github.blog.spiceland.html',
'https://lady50plus.de/2019/06/19/sekre-mystery-bag/': 'lady50plus.de.sekre.html',
'https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer': 'sonntag-sachsen.de.emanuel.html',
'https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite': 'psl.eu.luniversite.html',
'https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html': 'chip.de.beef.html',
'http://www.sauvonsluniversite.fr/spip.php?article8532': 'sauvonsluniversite.com.spip.html',
'https://www.spiegel.de/spiegel/print/d-161500790.html': 'spiegel.de.albtraum.html',
'https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/': 'lemire.me.json.html',
'https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission': 'zeit.de.zugverkehr.html',
'https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020': 'franceculture.fr.idees.html',
'https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/': 'wikimediafoundation.org.turkey.html',
'https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH': 'reuters.com.parasite.html',
'https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2': 'vancouversun.com.microsoft.html',
}
# '': '', \


TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def load_mock_page(url, xml_flag=False, langcheck=None, tei_output=False):
    '''load mock page from samples'''
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = chardet.detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    result = extract(htmlstring, url,
                     record_id='0000',
                     no_fallback=False,
                     xml_output=xml_flag,
                     tei_output=tei_output,
                     target_language=langcheck)
    return result


def test_trim():
    '''test string trimming'''
    assert trim('	Test  ') == 'Test'
    assert trim('\t\tTest  Test\r\n') == 'Test Test'
    my_elem = etree.Element('body')
    my_elem.text = 'Test Text'
    assert textfilter(my_elem) is False
    # my_elem.text = 'Tags: Arbeit, Urlaub'
    my_elem.text = 'Instagram'
    assert textfilter(my_elem) is True


def test_input():
    '''test if loaded strings/trees are handled properly'''
    assert utils.load_html(123) is None
    assert utils.load_html('<html><body>XYZ</body></html>') is not None
    #assert utils.load_html(b'0'*int(10e3)) is None
    assert extract(None, 'url', '0000', xml_output=False, tei_output=False, target_language=None) is None
    # legacy
    assert process_record(None, 'url', '0000', xml_output=False, tei_output=False, target_language=None) is None


def test_parser():
    '''test argument parsing for the command-line interface'''
    testargs = ['', '-fv', '--xmltei', '--notables', '-u', 'https://www.example.org']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
        assert args.fast is True
        assert args.verbose is True
        assert args.notables is False
        assert args.xmltei is True
        assert args.URL == 'https://www.example.org'


def test_climain():
    '''test arguments and main CLI entrypoint'''
    assert os.system('trafilatura --help') == 0  # exit status
    # assert os.system('trafilatura -f -u https://httpbin.org/html') == 0
    # assert os.system('curl -s https://httpbin.org/html | trafilatura') == 0
    # input directory walking and processing
    assert os.system('trafilatura --inputdir "trafilatura/data/"') == 0
    assert os.system('trafilatura --inputdir "tests/resources/"') == 0
    #testargs = ['--inputdir tests/resources/']
    #with patch.object(sys, 'argv', testargs):
    #    result = cli.main()
    #print(result)


def test_input_type():
    '''test input type errors'''
    testfile = 'docs/trafilatura-demo.gif'
    with open(testfile, 'rb') as f:
        teststring = f.read(1024)
    assert cli.examine(teststring) is None
    testfile = 'docs/index.rst'
    with open(testfile, 'r') as f:
        teststring = f.read()
    assert cli.examine(teststring) is None


def test_sysoutput():
    '''test output: ...'''
    testargs = ['', '--csv', '-o', '/root/forbidden/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    filename = cli.determine_filename(args)
    assert len(filename) >= 10 and filename.endswith('.csv')
    assert cli.check_outputdir_status(args) is False


def test_txttocsv():
    Metadata = namedtuple('Metadata', ['title', 'author', 'url', 'description', 'sitename', 'date', 'categories', 'tags'])
    mymeta = Metadata._make((None,) * len(Metadata._fields))
    assert utils.txttocsv('', '', mymeta) == 'None\tNone\tNone\t\t\n'
    mymeta = mymeta._replace(title='Test title')
    mymeta = mymeta._replace(url='https://example.org')
    assert utils.txttocsv('Test text', 'Test comment', mymeta) == 'https://example.org\tTest title\tNone\tTest text\tTest comment\n'


def test_download():
    '''test page download and command-line interface'''
    assert cli.examine(' ') is None
    assert cli.examine('0'*int(10e7), True) is None
    assert utils.fetch_url('https://httpbin.org/status/404') is None
    url = 'https://httpbin.org/status/200'
    teststring = utils.fetch_url(url)
    assert teststring is None  # too small
    assert cli.examine(teststring, url) is None
    url = 'https://httpbin.org/links/2/2'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, url) is None
    url = 'https://httpbin.org/html'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, url) is not None


@pytest.mark.parametrize("xmloutput", [False, True])
def test_extract(xmloutput): # xmloutput=False
    '''test extraction from HTML'''
    result = load_mock_page('https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/', xmloutput)
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result

    result = load_mock_page('https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html', xmloutput)
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result

    result = load_mock_page('https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/', xmloutput)
    assert 'Two or three 10-15 min' in result and 'What type? Etc. (30 mins)' in result and 'Dieser Eintrag wurde veröffentlicht' not in result and 'Mit anderen Teillen' not in result

    result = load_mock_page('https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess', xmloutput)
    assert 'Das Bukett präsentiert sich' in result and 'Kunden kauften auch' not in result and 'Gutschein sichern' not in result # and 'Besonders gut passt er zu asiatischen Gerichten' in result

    result = load_mock_page('https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html', xmloutput)
    assert 'Überwachung der somatischen Zellen' in result and 'tragbaren Ultraschall-Geräten' in result and 'Kotkonsistenz' in result  and 'Anzeigentarife' not in result # and 'Aktuelle Berichte aus dieser Kategorie' not in result

    result = load_mock_page('http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung', xmloutput)
    #print(result)
    if xmloutput is False:
        assert 'Wir bearbeiten alle Leistungsbilder' in result and 'Brückenbau' not in result

    result = load_mock_page('http://www.shingon-reiki.de/reiki-und-schamanismus/', xmloutput)
    assert 'Catch Evolution' not in result and 'und gekennzeichnet mit' not in result and 'Heut geht es' in result and 'Ich komme dann zu dir vor Ort.' in result

    result = load_mock_page('http://love-hina.ch/news/0409.html', xmloutput)
    assert 'Kapitel 121 ist' in result and 'Besucher online' not in result and 'Kommentare schreiben' not in result

    result = load_mock_page('http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html', xmloutput)
    assert 'der steigenden Nachfrage gerecht zu werden.' in result and 'Zurück zur Übersicht' not in result # and 'Erhöhung für Zoo-Eintritt' not in result

    result = load_mock_page('https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/', xmloutput)
    assert 'das letzte Wort sein kann.' in result and 'Ähnliche Beiträge' not in result # and 'Michael Blahm' not in result # comments

    result = load_mock_page('https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/', xmloutput)
    assert 'Unter diesem Motto findet am 14. September' in result and 'Volksinitiative Schweiz zum Grundeinkommen.' in result and 'getaggt mit:' not in result # and 'Was denkst du?' not in result

    result = load_mock_page('https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/', xmloutput)
    assert 'Zweitens wird der Genderstern' in result and 'alldem leider – nichts.' in result # and 'Beitragsbild' not in result

    result = load_mock_page('http://www.wehranlage-horka.de/veranstaltung/887/', xmloutput)
    assert 'In eine andere Zeit' in result and 'Während Sie über den Markt schlendern' in result and 'Infos zum Verein' not in result and 'nach oben' not in result and 'Datenschutzerklärung' not in result

    result = load_mock_page('https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft', xmloutput)
    assert 'Millionen Menschen fahren jeden Tag' in result and 'Clipdealer' not in result and 'Teste dein Wissen' not in result and 'Thema: Fußball' not in result # and 'Eines der großen Probleme,' in result and 'versteinerte Dinosaurierknochen.' in result

    result = load_mock_page('http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html', xmloutput)
    assert 'Erdöl bildet nach Millionen' in result and 'Warum wird das Erdöl knapp?' in result and 'Die Natur ist aus chemischen Elementen aufgebaut' not in result

    result = load_mock_page('https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html', xmloutput)
    assert 'Für einen Roman' in result and 'Auszeichnung der Branche.' in result

    result = load_mock_page('https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/', xmloutput)
    #print(result)
    if xmloutput is False:
        assert 'Dann sollten Sie erst recht' in result and 'als saure Gürkchen entlarvte Ex-Boyfriends.' in result and 'Ähnliche Beiträge' not in result

    result = load_mock_page('http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html', xmloutput)
    assert 'künftig das XADO-Schutzfett verwenden.' in result and 'bis zu 50% Verschleiß.' in result and 'Die Lebensdauer von Bauteilen erhöht sich beträchtlich.' in result and 'Newsletter' not in result # and 'Sie könnten auch an folgenden Artikeln interessiert sein' not in result

    result = load_mock_page('https://www.fairkom.eu/about', xmloutput)
    assert 'ein gemeinwohlorientiertes Partnerschaftsnetzwerk' in result and 'Stimmberechtigung bei der Generalversammlung.' in result and 'support@fairkom.eu' not in result

    result = load_mock_page('https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461', xmloutput)
    assert 'Einige Kunden des Fahrdienst-Vermittler Lyft' in result and 'zeitweise rund vier Prozent.' in result and 'Allgemeine Nutzungsbedingungen' not in result # and 'Waymo bittet Autohersteller um Geld' not in result

    result = load_mock_page('http://www.hundeverein-kreisunna.de/unserverein.html', xmloutput)
    assert 'Beate und Norbert Olschewski' in result and 'ein Familienmitglied und unser Freund.' in result # and 'zurück zur Startseite' not in result

    result = load_mock_page('https://viehbacher.com/de/steuerrecht', xmloutput)
    assert 'und wirtschaftlich orientierte Privatpersonen' in result and 'rund um die Uhr.' in result and 'Mensch im Mittelpunkt.' in result and 'Was sind Cookies?' not in result

    result = load_mock_page('http://www.jovelstefan.de/2011/09/11/gefallt-mir/', xmloutput)
    assert 'Manchmal überrascht einen' in result and 'kein Meisterwerk war!' in result and 'Pingback von' not in result and 'Kommentare geschlossen' not in result

    result = load_mock_page('https://www.stuttgart.de/item/show/132240/1', xmloutput)
    assert 'Das Bohnenviertel entstand' in result and 'sich herrlich entspannen.' in result and 'Nützliche Links' not in result # and 'Mehr zum Thema' not in result

    result = load_mock_page('http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/', xmloutput)
    assert 'zu einem glatten Teig verarbeiten.' in result and 'goldbraun sind.' in result and '200 g Zucker' in result and 'Ein Backblech mit Backpapier auslegen.' in result and 'Sei der Erste' not in result and 'Gefällt mir' not in result and 'Trotz sorgfältiger inhaltlicher Kontrolle' not in result

    # justext performs better here
    result = load_mock_page('http://schleifen.ucoz.de/blog/briefe/2010-10-26-18', xmloutput)
    assert 'Es war gesagt,' in result and 'Symbol auf dem Finger haben' in result # and 'Aufrufe:' not in result

    result = load_mock_page('https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg', xmloutput)
    assert 'Salzburg liebt seine Radfahrer.' in result and 'Puls einsaugen zu lassen.' in result and 'Das könnte Sie auch interessieren ...' not in result and 'So macht Radfahren sonst noch Spaß' not in result # and 'Radfahren in der Fußgängerzone der Innenstadt ist erlaubt' in result

    result = load_mock_page('https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/', xmloutput)
    assert 'Allerdings sieht es wie ein Dildo aus,' in result and 'gibt Bescheid, ne?' in result and 'Ähnliche Beiträge' not in result and 'Deine E-Mail (bleibt natürlich unter uns)' not in result

    result = load_mock_page('https://www.otto.de/twoforfashion/strohtasche/', xmloutput)
    assert 'Ob rund oder kastenförmig, ob dezent oder auffällig' in result and 'XX, Die Redaktion' in result and ' Kommentieren' not in result and 'Dienstag, 4. Juni 2019' not in result

    result = load_mock_page('http://iloveponysmag.com/2018/05/24/barbour-coastal/', xmloutput)
    assert 'Eine meiner besten Entscheidungen bisher:' in result and 'Verlassenes Gewächshaus meets versteckter Deich' in result and 'Der Hundestrand in Stein an der Ostsee' in result and 'Tags: Barbour,' not in result and 'Bitte (noch) mehr Bilder von Helle' in result and 'Hinterlasse einen Kommentar' not in result

    result = load_mock_page('https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/', xmloutput)
    assert 'Das ist alles nicht gekennzeichnet, wie soll ich wissen' in result and 'Instagramshops machen es Abmahnanwälten leicht' in result and 'Diese Geschichte teilen' not in result and 'Ähnliche Beiträge ' not in result and 'Ich bin der Ansicht, abwarten und Tee trinken.' in result and 'Danke für dein Feedback. Auch zum Look meiner Seite.' in result and 'Diese Website verwendet Akismet, um Spam zu reduzieren.' not in result

    result = load_mock_page('http://www.womencantalksports.com/top-10-women-talking-sports/', xmloutput)
    assert 'Keep Talking Sports!' in result and 'Category: Blog Popular' not in result and 'Copyright Women Can Talk Sports.' not in result and 'Submit your sports question below' not in result # '3.Charlotte Jones Anderson' in result and

    result = load_mock_page('https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html', xmloutput)
    assert 'Schönheit kommt für Pamela von Innen und Außen' in result and 'Die Workout Übungen kannte ich bereits' in result and 'Great post, I like your blog' in result and 'Links zu diesem Post' not in result and 'mehr über mich ♥' not in result and 'Bitte beachte auch die Datenschutzerklärung von Google.' not in result # and 'Vielen Dank an den den Verlag' in result

    result = load_mock_page('https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html', xmloutput)
    assert 'Grounded in sustainable architecture and refined Vietnamese craftsmanship,' in result and 'and Carmelo Resort' in result and 'OMG what a beautiful place to stay! ' in result and 'Food Advertising by' not in result and 'Dining and Drinking' in result and 'A lovely note makes a beautiful day!' not in result # and 'Reply' not in result

    result = load_mock_page('https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/', xmloutput)
    assert 'Argentina, the birthplace of polo.' in result and 'Simon Wittenberg travels to the Eternal City in Italy' in result and 'Luxury and lifestyle articles' not in result and 'Pinterest' not in result

    #result = load_mock_page('https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5', xmloutput)
    #print(result)
    #assert result is None

    result = load_mock_page('https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/', xmloutput)
    assert 'Prof. Dr. Caja Thimm' in result and 'zur Anmeldung.' in result and 'Next post' not in result and 'Aus den Ländern' not in result

    result = load_mock_page('https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/', xmloutput)
    assert 'Leitsätze des Gerichts' in result and 'III. Die Revision der Beklagten' and 'twittern' not in result and 'Ähnliche Beiträge' not in result and 'd.toelle[at]rechtambild.de' not in result

    result = load_mock_page('http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html', xmloutput)
    # print(result)
    assert 'Wann Blogs einer Impressumspflicht unterliegen,' in result and 'Über mich' not in result and 'Gesetzes- und Rechtsprechungszitate werden automatisch' not in result
    ## comments!
    # and 'Mit Verlaub, ich halte das für groben Unsinn.' in result
    # and 'Comment by' not in result

    result = load_mock_page('https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html', xmloutput)
    #print(result)
    if xmloutput is False:
        assert 'Aufbau und Inhalt' in result and 'Verlag Dr. Otto Schmidt' in result and 'Handbuch' not in result and 'Drucken' not in result and 'Ähnliche Artikel' not in result and 'Anzeige:' not in result # and 'Kommentar schreiben' not in result

    result = load_mock_page('https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen', xmloutput)
    assert 'Auch der Verweis auf ehrverletzende Bewertungen' in result and 'Fanden Sie diesen Artikel nützlich?' not in result and 'Kommentar hinzufügen' not in result # and 'Zu seinen Tätigkeitsfeldern zählen' not in result
    if xmloutput is False:
        assert 'Anja Schmoll-Trautmann' not in result and 'Aktuell' not in result 

    result = load_mock_page('https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage', xmloutput)
    assert 'Alle Artikel zu unseren Recherchen' not in result and 'Vorweg: Die beteiligten AfD-Politiker' in result and 'ist heute Abend um 21 Uhr auch im ZDF-Magazin Frontal' in result and 'Wir informieren Sie regelmäßig zum Thema Neue Rechte' not in result and 'Kommentar verfassen' not in result and 'weiterlesen' not in result

    result = load_mock_page('https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845', xmloutput)
    assert '05:28 Uhr' not in result and 'Bahn-Konkurrenten wie Flixbus fürchten durch den geplanten Deutschlandtakt' in result and 'ICE im S-Bahn-Takt' not in result and 'Diskussion zu diesem Artikel auf:' not in result and 'Berater-Affäre bringt Bahnchef Lutz in Bedrängnis' not in result and 'auch der Bus ein klimafreundliches Verkehrsmittel sei' in result

    result = load_mock_page('https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/', xmloutput)
    assert 'Rund ums Fahrzeug' not in result and 'in punkto Sicherheit, Bedienung, Ergonomie' in result and 'Grenzwert der Richtlinie 2014/79/EU' in result and 'Diesel-Umtauschprämien' not in result and 'Besonders bei Babyschalen sollte geprüft werden' in result

    result = load_mock_page('https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/', xmloutput)
    assert 'Was I losing my mind?' in result and 'being cached after their first access.' in result and 'Finding a Fix' in result and 'from django.conf import settings' in result and 'New Call-to-action' not in result and 'Contact us' not in result and 'Back to blog' not in result # and 'You might also like:' not in result

    result = load_mock_page('https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/', xmloutput)
    assert 'Vor knapp zwei Wochen' in result and 'gibt es in der dazugehörigen Vorstellungs-News.' in result and 'Themen:' not in result and 'bis Januar 2009 Artikel für ComputerBase verfasst.' not in result and 'Warum Werbebanner?' not in result and '71 Kommentare' not in result

    result = load_mock_page('http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html', xmloutput)
    assert '就放心去吧' in result and 'Repeat Chorus' in result and 'Older post' not in result and 'Thank you for your support!' not in result

    result = load_mock_page('https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/', xmloutput)
    assert 'Frank Thelen, Investor' in result and 'Female founders must constantly consider' in result and 'Thema des öffentlichen Interesses' in result and 'Nach langjähriger Tätigkeit im Ausland' not in result and 'Schaut man ganz genau hin, ist der Habeck-Kommentar' in result and 'Mit Absendung des Formulars willige ich' not in result and 'Kommentieren' not in result # and 'Auch interessant' not in result and 'Wir tun jeden Tag, was wir lieben.' not in result

    result = load_mock_page('https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/', xmloutput)
    assert 'Welche Werbeeinnahmen erwarten Sie hier langfristig?' in result and 'wir haben keinerlei Pläne, das zu verändern.' in result and 'Nachrichtenüberblick abonnieren' not in result and 'über alle aktuellen Entwicklungen auf dem Laufenden.' not in result and 'Schlagworte' not in result and 'Teilen' not in result and 'Dauerzoff um drohenden UKW-Blackout' not in result and 'Mobilcom Debitel has charged me for third party' in result

    result = load_mock_page('https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/', xmloutput)
    assert 'Zeit für Loslassen und Entspannung.' in result and 'Wie sieht dein Alltag aus?' in result and 'Erfrischende, abschwellende Augencreme Phyto Contour' in result and 'Vielen Dank Anja für deine Tipps rund um Beauty' in result and 'Betreiberin von incurvy Plus Size' not in result and 'Wir verwenden Cookies' not in result # and 'Das Thema könnte dich auch interessieren:' not in result

    result = load_mock_page('https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843', xmloutput)
    assert 'No grape variety invites as much intrigue' in result and 'With just 0.9 hectares' in result and 'Related Subjects' not in result and 'Audios and videos on the topic' not in result # and 'But boozers in Berlin' not in result

    result = load_mock_page('https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html', xmloutput)
    assert 'Adele feierte ausgelassen mit den Spice Girls' in result and 'wie sich Adele weiterentwickelt.' in result and 'Sommerzeit ist Urlaubszeit,' not in result and 'Lade weitere Inhalte' not in result

    result = load_mock_page('https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx', xmloutput)
    assert 'Konflikte mag keiner.' in result and 'Gespräche meistern können.' in result and 'Weiterführender Link' not in result and 'Flexible Wege in die' not in result

    result = load_mock_page('https://novalanalove.com/ear-candy/', xmloutput)
    assert 'Earcuff: Zoeca' in result and 'mit längeren Ohrringen (:' in result and 'Kreole: Stella Hoops' in result and 'Jetzt heißt es schnell sein:' not in result and 'Diese Website speichert Cookies' not in result and 'VON Sina Giebel' not in result

    result = load_mock_page('http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/', xmloutput)
    assert 'Zuerst dachte ich, ich könnte das' in result and 'x Franzi' in result and 'Flauschjacke: Bershka' in result and 'Palm Springs Mini (links)' not in result and 'Diese Website verwendet Akismet' not in result and 'New York, New York' not in result

    result = load_mock_page('https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html', xmloutput)
    assert 'Die Psyche spielt eine nicht unerhebliche Rolle' in result and 'Sportskanone oder Sportmuffel' not in result and 'PINNEN' not in result and '2. Satt essen bei den Mahlzeiten' in result and 'Bringt die Kilos zum Purzeln!' not in result # 'Crash-Diäten ziehen meist den Jojo-Effekt' in result and 

    result = load_mock_page('https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html', xmloutput)
    assert 'Glücks-Trend Konkurrenz' in result and 'Praktiziere Dankbarkeit' in result and 'dein Ikigai schon gefunden?' in result and '14,90 Euro.' in result and 'Neu in Liebe' not in result and 'Erfahre mehr' not in result and 'Erfahrung mit privater Arbeitsvermittlung?' not in result

    result = load_mock_page('https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/', xmloutput)
    assert 'Gibt es weitere Top-Maßnahmen für Multi-Channel?' in result and 'Vielen Dank für das interessante Interview!' in result and 'akzeptiere die Datenschutzbestimmungen' not in result and 'Diese Beiträge solltest du nicht verpassen' not in result
    if xmloutput is False:
        assert 'Annette Henkel' not in result

    result = load_mock_page('https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/', xmloutput)
    assert 'These messages include links to the ransomware' in result and 'using novel techniques to exfiltrate data.' in result and 'Share this article:' not in result and 'Write a comment' not in result and 'Notify me when new comments are added.' not in result and 'uses Akismet to reduce spam.' not in result

    result = load_mock_page('https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space', xmloutput)
    assert 'Brazil went dark.' in result and 'the highest number of deforestation warnings.”' in result and 'Tagged:' not in result and 'to the VICE newsletter.' not in result and 'Watch this next' not in result

    result = load_mock_page('https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html', xmloutput)
    assert 'Die Ökobilanz von Elektroautos' in result and 'Nur die Folie bleibt zurück' in result and 'TR 7/2019' not in result and 'Forum zum Thema:' not in result # and 'Highlights aus dem Heft:' not in result

    result = load_mock_page('https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact', xmloutput)
    assert 'Normally, video calls tend to' in result and 'across both the eyes and nose.' in result and 'Added ARKit explanation and tweet.' in result and 'Singapore’s public health program' not in result and 'Command Line delivers daily updates' not in result

    result = load_mock_page('https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/', xmloutput)
    assert 'in keinem Braut-Beauty-Programm fehlen darf?' in result and 'nicht nur vor der Hochzeit ein absolutes Muss.' in result and 'Gesundes, glänzendes Haar' in result and 'Neue Wandbilder von Posterlounge' not in result and 'mit meinen Texten und mit meinen Gedanken.' not in result and 'Erforderliche Felder sind mit * markiert.' not in result

    result = load_mock_page('https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis', xmloutput)
    assert 'Stilles Rackern, statt lautem Deklamieren.' in result and 'Watt jibt’s n hier zu lachen?' in result and 'Das Brandenbuch. Ein Land in Stichworten.' in result and 'Bürgerbeteiligung' not in result and 'Anmelden' not in result and 'Foto: Timur' not in result and 'Schlagworte' not in result and 'Zeilenumbrüche und Absätze werden automatisch erzeugt.' not in result

    result = load_mock_page('https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html', xmloutput)
    assert 'Wakebeach 257' in result and 'Be there or be square!' in result and 'Hier geht’s zur Facebook Veranstaltung' in result and 'More from News' not in result and 'von Redaktion MSM' not in result and 'add yours.' not in result # and 'Blue Tomato präsentiert die dritte' in result

    result = load_mock_page('https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/', xmloutput)
    assert 'Rocket Pass 4 will begin at 10:00 a.m. PDT' in result and 'Holy shit, Mortal Kombat 11' in result and 'Let us know down below in the comments' in result and 'Related Topics' not in result and 'You can keep up with me on Twitter' not in result and 'Hit the track today with Mario Kart Tour' not in result # and 'what to do with thousands of crates tho' in result

    result = load_mock_page('https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding', xmloutput)
    assert 'Given a set of high-dimensional objects' in result and 'Herein a heavy-tailed Student t-distribution' in result and 'Categories:' not in result # and 'Conditional random field' not in result

    result = load_mock_page('https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/', xmloutput)
    assert 'Niedlicher Roboter-Spielkamerad: Anki Cozmo' in result and 'Empfehlungen von Dennis:' in result and 'Unterstütze unsere Arbeit' not in result and 'Deepfake-Hollywood' not in result and 'Avengers' not in result and 'Katzenschreck' not in result

    result = load_mock_page('http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/', xmloutput)
    assert 'Hunderttausende von jungen Paaren' in result and 'wie flatterhaft das Mädl ist? :)' in result and 'Malte Welding' not in result and 'YouTube und die Alten' not in result and 'Autokorrektur' not in result

    result = load_mock_page('https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/', xmloutput)
    assert 'Rüschen und Volants.' in result and 'ihr jedes Jahr tragen könnt?' in result and 'Das könnte dich auch interessieren' not in result and 'Catherine Classic Lac 602' not in result # and 'mein Lieblingskleid vereint' in result

    result = load_mock_page('https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/', xmloutput)
    assert 'Einblicke in die Vision zukünftiger Softwaregenerationen.' in result and 'Frage 4: Welche Rolle spielt Big Data in Bezug auf Assistenz-Systeme und KI?' in result and 'von The unbelievable Machine Company (*um) zur Verfügung gestellt.' in result and 'Matthias Weber ist ERP-Experte mit langjähriger Berufserfahrung.' not in result and 'Die Top 5 digitalen Trends für den Mittelstand' not in result and ', leading edge,' not in result # and 'Lesen Sie hier einen weiteren spannenden Beitrag' not in result

    #result = load_mock_page('https://boingboing.net/2013/07/19/hating-millennials-the-preju.html', xmloutput)
    #print(result)
    #assert 'Click through for the whole thing.' in result and 'The generation we love to dump on' in result and 'GET THE BOING BOING NEWSLETTER' not in result # and 'happy mutants' not in result and 'Patti Smith and Stewart Copeland' not in result

    result = load_mock_page('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/', xmloutput)
    assert 'Erin Spiceland is a Software Engineer for SpaceX.' in result and 'make effective plans and goals for the future' in result and 'looking forward to next?' in result and 'Research Consultant at Adelard LLP' in result and 'Related posts' not in result and 'Jeremy Epling' not in result and 'Missed the main event?' not in result and 'Privacy' not in result

    result = load_mock_page('https://lady50plus.de/2019/06/19/sekre-mystery-bag/', xmloutput)
    assert 'ist eine echte Luxushandtasche' in result and 'Insgesamt 160 weibliche „Designerinnen“' in result and 'Sei herzlich gegrüßt' in result and 'Ein Mann alleine hätte niemals' in result and 'Erforderliche Felder sind mit' not in result and 'Benachrichtige mich' not in result and 'Reisen ist meine große Leidenschaft' not in result and 'Styling Tipps für Oktober' not in result and 'in den Bann ziehen!' in result

    result = load_mock_page('https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer', xmloutput)
    assert 'Neuer Geschäftsführender Leiter' in result and 'nach Leipzig wechseln.' in result and 'Mehr zum Thema' not in result and 'Folgen Sie uns auf Facebook und Twitter' not in result # and 'Aktuelle Ausgabe' not in result

    result = load_mock_page('https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite', xmloutput)
    assert 'Le décret n°2019-1130 validant' in result and 'restructurant à cet effet ».' in result and ' utilise des cookies pour' not in result and 'En savoir plus' not in result # and 'CNRS, Inserm, Inria.' not in result

    result = load_mock_page('https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html', xmloutput)
    assert 'Starke Hitze nur in der Mitte' in result and 'ca. 35,7×29,4 cm' in result and 'Wir sind im Steak-Himmel!' in result and 'Samsung Galaxy S10 128GB' not in result and 'Für Links auf dieser Seite' not in result # and 'Inga Buller ist Head of Social' not in result 

    result = load_mock_page('http://www.sauvonsluniversite.fr/spip.php?article8532', xmloutput)
    assert 'L’AG Éducation Île-de-France inter-degrés' in result and 'Grève et mobilisation pour le climat' in result and 'suivi.reformes.blanquer@gmail.com' in result and 'Sauvons l’Université !' not in result and 'La semaine de SLU' not in result

    result = load_mock_page('https://www.spiegel.de/spiegel/print/d-161500790.html', xmloutput)
    assert 'Wie konnte es dazu kommen?' in result and 'Die Geschichte beginnt am 26. Oktober' in result and 'Es stützt seine Version.' in result and 'und Vorteile sichern!' not in result and 'Verschickt' not in result # and 'Die digitale Welt der Nachrichten.' not in result and 'Vervielfältigung nur mit Genehmigung' not in result

    result = load_mock_page('https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/', xmloutput)
    assert 'I use a Skylake processor with GNU GCC 8.3.' in result and 'gsoc-2018' in result and '0.091 GB/s' in result and 'version 0.2 on vcpkg.' in result and 'Leave a Reply' not in result and 'Science and Technology links' not in result and 'Proudly powered by WordPress' not in result

    result = load_mock_page('https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission', xmloutput)
    assert '36 Stunden.' in result and 'Nationale Egoismen' in result and 'Deutschland kaum beschleunigt.' in result and 'Durchgehende Tickets fehlen' not in result and 'geprägte Fehlentscheidung.' in result and 'horrende Preise für miserablen Service bezahlen?' in result and 'Bitte melden Sie sich an, um zu kommentieren.' not in result

    result = load_mock_page('https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020', xmloutput)
    assert 'Performativité' in result and 'Les individus productifs communiquent' in result and 'de nos espoirs et de nos désirs.' in result and 'A la tribune je monterai' not in result and 'À découvrir' not in result and 'Le fil culture' not in result

    result = load_mock_page('https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/', xmloutput)
    assert 'as further access is restored.' in result and 'Read further in the pursuit of knowledge' not in result and 'Here’s what that means.' not in result and 'Stay up-to-date on our work.' not in result and 'Photo credits' not in result # 'Bu yazının Türkçe’sini buradan okuyabilirsiniz' in result and

    result = load_mock_page('https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH', xmloutput)
    assert '4 Min Read' not in result and 'The Thomson Reuters Trust Principles' not in result and 'Factbox: Key winners' not in result and 'Despite an unknown cast,' in result and 'Additional reporting by' in result

    result = load_mock_page('https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2', xmloutput)
    print(result)
    assert 'Microsoft Corp said on Thursday' in result and 'Postmedia is committed' in result and 'I consent to receiving' not in result and 'It was not immediately clear if' in result and 'turns CO2 into soap' not in result
    if xmloutput is False:
        assert 'Reuters files' not in result

    #result = load_mock_page('', xmloutput)
    #assert '' in result and '' in result and '' not in result and '' not in result and '' not in result

    # try:
    # ...
    # except AssertionError as err:
    #    if platform.system() == 'Windows':
    #        pass
    #    else:
    #        raise AssertionError(err)

@patch('trafilatura.core.MIN_OUTPUT_SIZE', 0)
@patch('trafilatura.core.MIN_OUTPUT_COMM_SIZE', 0)
def test_exotic_tags(xmloutput=False):
    # cover some edge cases with a specially crafted file
    result = load_mock_page('http://exotic_tags', xmloutput, tei_output=True)
    assert 'Teletype text' in result
    assert 'My new car is silver.' in result
    filepath = os.path.join(TEST_DIR, 'cache', 'exotic_tags_tei.html')
    with open(filepath) as f:
        content = etree.fromstring(f.read())
    res = xml.check_tei(content, 'http://dummy')
    assert etree.tostring(res).startswith(b'<html>\n<text>\n<body>\n<div>\n\n<hi>Hello</hi>\n<p>Teletype text</p>')


def test_lrucache():
    '''test basic duplicate detection'''
    lru_test = LRUCache(maxsize=2)
    trafilatura.filters.LRU_TEST = lru_test
    my_body = etree.Element('body')
    ### element too short
    #my_element = html.fromstring('<p>AAAA BBBB</p>')
    #my_body.append(my_element)
    #put_in_cache(my_body)
    #assert duplicate_test(my_element) is False
    ### cached element
    my_element = html.fromstring('<p>AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB</p>')
    my_body.append(my_element)
    assert duplicate_test(my_element) is False
    put_in_cache(my_body)
    assert duplicate_test(my_element) is False
    put_in_cache(my_body)
    assert duplicate_test(my_element) is False
    put_in_cache(my_body)
    assert duplicate_test(my_element) is True
    other_body = etree.Element('body')
    other_element = html.fromstring('<p>CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD</p>')
    other_body.append(other_element)
    put_in_cache(other_body)
    put_in_cache(other_body)
    put_in_cache(other_body)
    assert duplicate_test(other_element) is True
    yet_another_body = etree.Element('body')
    yet_another_element = html.fromstring('<p>EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF</p>')
    yet_another_body.append(yet_another_element)
    put_in_cache(yet_another_body)
    put_in_cache(yet_another_body)
    put_in_cache(yet_another_body)
    # 2 elements in cache, original element has been cleared?
    # print(LRU_TEST.maxsize, LRU_TEST.full)
    assert duplicate_test(other_element) is True
    assert duplicate_test(yet_another_element) is True
    assert duplicate_test(my_element) is False
    # clear the cache
    lru_test.clear()
    assert duplicate_test(other_element) is False
    # get wrong key
    assert lru_test.get('tralala') == -1


@patch('trafilatura.core.MIN_OUTPUT_SIZE', 0)
def test_formatting():
    '''Test HTML formatting conversion and extraction'''
    # simple
    my_document = html.fromstring('<html><body><p><b>This here is in bold font.</b></p></body></html>')
    my_result = extract(my_document, xml_output=True, include_formatting=True)
    assert '<hi rend="#b">This here is in bold font.</hi>' in my_result
    # nested
    my_document = html.fromstring('<html><body><p><b>This here is in bold and <i>italic</i> font.</b></p></body></html>')
    my_result = extract(my_document, xml_output=True, include_formatting=True)
    assert '<hi rend="#b">This here is in bold and italic font.</hi>' in my_result
    # empty
    my_document = html.fromstring('<html><body><p><b><i></i></b></p></body></html>')
    my_result = extract(my_document, xml_output=True, include_formatting=True)
    assert '<main/>' in my_result
    # wild div
    my_document = html.fromstring('<html><body><article><div><strong>Wild text</strong></div></article></body></html>')
    my_result = extract(my_document, xml_output=True, include_formatting=True)
    assert '<p>' in my_result and '<hi>Wild text</hi>' in my_result  # no rend so far
    my_result = extract(my_document)
    assert my_result == 'Wild text'


@patch('trafilatura.core.MIN_OUTPUT_SIZE', 0)
def test_jsontext():
    my_document = r'<html><body><script type="application/ld+json">{"description":"In letzter Zeit kam man am Begriff \"Hygge\", was so viel wie \"angenehm\" oder \"gemütlich\" bedeutet, ja nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend ...","image":[{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/uncropped-0-0\/7d00b2658fd0a3b19e1b161f4657cc20\/Xw\/ikigai--1-.jpg","width":"2048","height":"1366","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-1280-720\/bf947c7c24167d7c0adae0be10942d57\/Uf\/ikigai--1-.jpg","width":"1280","height":"720","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-938-528\/bf947c7c24167d7c0adae0be10942d57\/JK\/ikigai--1-.jpg","width":"938","height":"528","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/large1x1-622-622\/f5544b7d67e1be04f7729b130e7e0485\/KN\/ikigai--1-.jpg","width":"622","height":"622","@type":"ImageObject"}],"mainEntityOfPage":{"@id":"https:\/\/www.brigitte.de\/liebe\/persoenlichkeit\/ikigai-macht-dich-sofort-gluecklicher--10972896.html","@type":"WebPage"},"headline":"Ikigai macht dich sofort glücklicher!","datePublished":"2019-06-19T14:29:08+0000","dateModified":"2019-06-19T14:29:10+0000","author":{"name":"BRIGITTE.de","@type":"Organization"},"publisher":{"name":"BRIGITTE.de","logo":{"url":"https:\/\/image.brigitte.de\/11476842\/uncropped-0-0\/f19537e97b9189bf0f25ce924168bedb\/kK\/bri-logo-schema-org.png","width":"167","height":"60","@type":"ImageObject"},"@type":"Organization"},"articleBody":"In letzter Zeit kam man am Begriff \"Hygge\" (\"gemütlich\" oder \"angenehm\") nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend Konkurrenz: \"Ikigai\". Bist du glücklich? Schwierige Frage, nicht wahr? Viele von uns müssen da erst mal überlegen.","@type":"NewsArticle"}</script></body></html>'
    _, _, result = baseline(my_document)
    assert result.startswith('In letzter Zeit kam man') and result.endswith('erst mal überlegen.')


def test_filters():
    '''Test content filtering'''
    if LANGID_FLAG is True:
        # main text
        assert trafilatura.filters.language_filter('Hier ist ein Text auf Deutsch', '', 'de', None, None) is False
        assert trafilatura.filters.language_filter('Hier ist ein Text auf Deutsch', '', 'en', None, None) is True
        # comments
        assert trafilatura.filters.language_filter('Hier ist ein Text.', 'Die Kommentare sind aber etwas länger.', 'de', None, None) is False
    else:
        # no detection
        assert trafilatura.filters.language_filter('Hier ist ein Text.', '', 'en', None, None) is False 


def test_tei():
    '''test TEI-related functions'''
    # open local resources to avoid redownloading at each run
    resources_dir = os.path.join(TEST_DIR, 'resources')
    html_filepath = os.path.join(resources_dir, 'httpbin_sample.html')
    with open(html_filepath) as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result = extract(teststring, "mocked", no_fallback=True, tei_output=True, tei_validation=True)
    assert result is not None
    mytree = etree.fromstring(result)
    assert xml.validate_tei(mytree) is True


if __name__ == '__main__':
    test_trim()
    test_lrucache()
    test_input()
    test_sysoutput()
    test_parser()
    test_climain()
    test_input_type()
    test_formatting()
    test_filters()
    test_jsontext()
    test_txttocsv()
    test_exotic_tags()
    test_extract(False)
    test_extract(True)
    test_download()
    test_tei()
