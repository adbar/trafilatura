# pylint:disable-msg=W1401
"""
Unit tests for the trafilatura library.
Not included in releases due to cached pages.
"""


import logging
import os
import sys

import pytest
# https://docs.pytest.org/en/latest/


try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

from trafilatura import extract
from trafilatura.metadata import extract_metadata


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
SAMPLE_META = dict.fromkeys(['title', 'author', 'url', 'description', 'sitename', 'date', 'categories', 'tags', 'id'])


MOCK_PAGES = {
    'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/': 'die-partei.net.luebeck.html',
    'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html': 'bmjv.de.konsum.html',
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
    'https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/': 'piratenpartei-mv.de.grundeinkommen.html',
    'https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html': 'rnz.de.witzel.html',
    'https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg': 'austria.info.radfahren.html',
    'https://www.fairkom.eu/about': 'fairkom.eu.about.html',
    'https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461': 'futurezone.at.lyft.html',
    'http://www.hundeverein-kreisunna.de/unserverein.html': 'hundeverein-kreisunna.de.html',
    'https://viehbacher.com/de/steuerrecht': 'viehbacher.com.steuerrecht.html',
    'http://www.jovelstefan.de/2011/09/11/gefallt-mir/': 'jovelstefan.de.gefallt.html',
    'https://www.stuttgart.de/item/show/132240/1': 'stuttgart.de.html',
    'https://www.otto.de/twoforfashion/strohtasche/': 'otto.de.twoforfashion.html',
    'http://www.womencantalksports.com/top-10-women-talking-sports/': 'womencantalksports.com.top10.html',
    'https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html': 'luxuryhaven.co.hyatt.html',
    'https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/': 'luxuriousmagazine.com.polo.html',
    'https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5': 'chip.de.tests.html',
    'https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/': 'gruen-digital.de.jahrestagung.html',
    'https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/': 'rechtambild.de.kochbuch.html',
    'http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html': 'internet-law.de.pseudonymen.html',
    'https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage': 'correctiv.org.zusage.html',
    'https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845': 'sueddeutsche.de.flixtrain.html',
    'https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/': 'adac.de.kindersitze.html',
    'https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/': 'caktusgroup.com.django.html',
    'https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/': 'basicthinking.de.tweets.html',
    'https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/': 'incurvy.de.wellness.html',
    'https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843': 'dw.com.uncork.html',
    'https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html': 'jolie.de.adele.html',
    'https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx': 'speicherguide.de.schwierige.html',
    'https://novalanalove.com/ear-candy/': 'novalanalove.com.ear-candy.html',
    'http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/': 'franziska-elea.de.vuitton.html',
    'https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html': 'brigitte.de.ikigai.html',
    'https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/': 'changelog.blog.zwischenbilanz.html',
    'https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/': 'threatpost.com.android.html',
    'https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact': 'theverge.com.ios13.html',
    'https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding': 'en.wikipedia.org.tsne.html',
    'https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/': 'mixed.de.vrodo.html',
    'https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/': 'majkaswelt.com.fashion.html',
    'https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/': 'erp-news.info.interview.html',
    'https://lady50plus.de/2019/06/19/sekre-mystery-bag/': 'lady50plus.de.sekre.html',
    'https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite': 'psl.eu.luniversite.html',
    'http://www.sauvonsluniversite.fr/spip.php?article8532': 'sauvonsluniversite.com.spip.html',
    'https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020': 'franceculture.fr.idees.html',
    'https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2': 'vancouversun.com.microsoft.html',
    'https://www.lanouvellerepublique.fr/indre-et-loire/commune/saint-martin-le-beau/family-park-la-derniere-saison-a-saint-martin-le-beau': 'lanouvellerepublique.fr.martin.html',
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
    "https://www.mercurynews.com/2023/01/16/letters-1119/": "mercurynews.com.2023.01.16.letters-1119.html"
}
# '': '', \


def load_mock_page(url, xml_flag=False, langcheck=None, tei_output=False):
    '''load mock page from samples'''
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r', encoding='utf-8') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    output_format = 'txt'
    if xml_flag is True:
        output_format = 'xml'
    if tei_output is True:
        output_format = 'tei'
    return extract(htmlstring, url,
                     record_id='0000',
                     no_fallback=False,
                     output_format=output_format,
                     target_language=langcheck)


def load_mock_page_meta(url):
    '''Load mock page from samples'''
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r', encoding='utf-8') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    return htmlstring


@pytest.mark.parametrize("xmloutput", [False, True])
def test_extract(xmloutput):
    '''test extraction from HTML'''
    result = load_mock_page('https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/', xmloutput)
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result

    result = load_mock_page('https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html', xmloutput)
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result

    result = load_mock_page('https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/', xmloutput)
    assert 'Two or three 10-15 min' in result and 'What type? Etc. (30 mins)' in result and 'Dieser Eintrag wurde veröffentlicht' not in result and 'Mit anderen Teillen' not in result

    result = load_mock_page('https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess', xmloutput)
    assert 'Das Bukett präsentiert sich' in result and 'Kunden kauften auch' not in result and 'Gutschein sichern' not in result and 'Besonders gut passt er zu asiatischen Gerichten' in result

    result = load_mock_page('https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html', xmloutput)
    assert 'Überwachung der somatischen Zellen' in result and 'tragbaren Ultraschall-Geräten' in result and 'Kotkonsistenz' in result  and 'Anzeigentarife' not in result and 'Aktuelle Berichte aus dieser Kategorie' not in result

    result = load_mock_page('http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung', xmloutput)
    if xmloutput is False:
        assert 'Wir bearbeiten alle Leistungsbilder' in result and 'Brückenbau' not in result

    result = load_mock_page('http://www.shingon-reiki.de/reiki-und-schamanismus/', xmloutput)
    assert 'Catch Evolution' not in result and 'und gekennzeichnet mit' not in result and 'Heut geht es' in result and 'Ich komme dann zu dir vor Ort.' in result

    result = load_mock_page('http://love-hina.ch/news/0409.html', xmloutput)
    assert 'Kapitel 121 ist' in result and 'Besucher online' not in result and 'Kommentare schreiben' not in result

    result = load_mock_page('http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html', xmloutput)
    assert 'der steigenden Nachfrage gerecht zu werden.' in result and 'Zurück zur Übersicht' not in result and 'Erhöhung für Zoo-Eintritt' not in result

    result = load_mock_page('https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/', xmloutput)
    assert 'das letzte Wort sein kann.' in result and 'Ähnliche Beiträge' not in result  # and 'Michael Blahm' not in result # comments

    result = load_mock_page('https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/', xmloutput)
    assert 'Unter diesem Motto findet am 14. September' in result and 'Volksinitiative Schweiz zum Grundeinkommen.' in result and 'getaggt mit:' not in result and 'Was denkst du?' not in result

    result = load_mock_page('https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/', xmloutput)
    assert 'Zweitens wird der Genderstern' in result and 'alldem leider – nichts.' in result  # and 'Beitragsbild' not in result

    result = load_mock_page('http://www.wehranlage-horka.de/veranstaltung/887/', xmloutput)
    assert 'In eine andere Zeit' in result and 'Während Sie über den Markt schlendern' in result and 'Infos zum Verein' not in result and 'nach oben' not in result and 'Datenschutzerklärung' not in result

    # modified by taking only 1st article element...
    result = load_mock_page('https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft', xmloutput)
    # print(result)
    assert 'Millionen Menschen fahren jeden Tag' in result and 'Clipdealer' not in result and 'Teste dein Wissen' not in result and 'Thema: Fußball' not in result  # and 'Eines der großen Probleme,' in result and 'versteinerte Dinosaurierknochen.' in result

    result = load_mock_page('http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html', xmloutput)
    assert 'Erdöl bildet nach Millionen' in result and 'Warum wird das Erdöl knapp?' in result and 'Die Natur ist aus chemischen Elementen aufgebaut' not in result

    result = load_mock_page('https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html', xmloutput)
    assert 'Für einen Roman' in result and 'Auszeichnung der Branche.' in result

    result = load_mock_page('https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/', xmloutput)
    #print(result)
    if xmloutput is False:
        assert 'Dann sollten Sie erst recht' in result and 'als saure Gürkchen entlarvte Ex-Boyfriends.' in result and 'Ähnliche Beiträge' not in result

    result = load_mock_page('http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html', xmloutput)
    assert 'künftig das XADO-Schutzfett verwenden.' in result and 'bis zu 50% Verschleiß.' in result and 'Die Lebensdauer von Bauteilen erhöht sich beträchtlich.' in result and 'Newsletter' not in result and 'Sie könnten auch an folgenden Artikeln interessiert sein' not in result

    result = load_mock_page('https://www.fairkom.eu/about', xmloutput)
    assert 'ein gemeinwohlorientiertes Partnerschaftsnetzwerk' in result and 'Stimmberechtigung bei der Generalversammlung.' in result and 'support@fairkom.eu' not in result

    result = load_mock_page('https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461', xmloutput)
    assert 'Einige Kunden des Fahrdienst-Vermittler Lyft' in result and 'zeitweise rund vier Prozent.' in result and 'Allgemeine Nutzungsbedingungen' not in result and 'Waymo bittet Autohersteller um Geld' not in result

    result = load_mock_page('http://www.hundeverein-kreisunna.de/unserverein.html', xmloutput)
    assert 'Beate und Norbert Olschewski' in result and 'ein Familienmitglied und unser Freund.' in result and 'zurück zur Startseite' not in result

    result = load_mock_page('https://viehbacher.com/de/steuerrecht', xmloutput)
    assert 'und wirtschaftlich orientierte Privatpersonen' in result and 'rund um die Uhr.' in result and 'Mensch im Mittelpunkt.' in result and 'Was sind Cookies?' not in result

    result = load_mock_page('http://www.jovelstefan.de/2011/09/11/gefallt-mir/', xmloutput)
    assert 'Manchmal überrascht einen' in result and 'kein Meisterwerk war!' in result and 'Pingback von' not in result and 'Kommentare geschlossen' not in result

    result = load_mock_page('https://www.stuttgart.de/item/show/132240/1', xmloutput)
    assert 'Das Bohnenviertel entstand' in result and 'sich herrlich entspannen.' in result and 'Nützliche Links' not in result and 'Mehr zum Thema' not in result

    result = load_mock_page('http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/', xmloutput)
    assert 'zu einem glatten Teig verarbeiten.' in result and 'goldbraun sind.' in result and '200 g Zucker' in result and 'Ein Backblech mit Backpapier auslegen.' in result and 'Sei der Erste' not in result and 'Gefällt mir' not in result and 'Trotz sorgfältiger inhaltlicher Kontrolle' not in result

    # justext performs better here
    result = load_mock_page('http://schleifen.ucoz.de/blog/briefe/2010-10-26-18', xmloutput)
    assert 'Es war gesagt,' in result and 'Symbol auf dem Finger haben' in result and 'Aufrufe:' not in result

    result = load_mock_page('https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg', xmloutput)
    assert 'Salzburg liebt seine Radfahrer.' in result and 'Puls einsaugen zu lassen.' in result and 'Das könnte Sie auch interessieren ...' not in result and 'So macht Radfahren sonst noch Spaß' not in result  # and 'Radfahren in der Fußgängerzone der Innenstadt ist erlaubt' in result

    result = load_mock_page('https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/', xmloutput)
    assert 'Allerdings sieht es wie ein Dildo aus,' in result and 'gibt Bescheid, ne?' in result and 'Ähnliche Beiträge' not in result and 'Deine E-Mail (bleibt natürlich unter uns)' not in result

    result = load_mock_page('https://www.otto.de/twoforfashion/strohtasche/', xmloutput)
    assert 'Ob rund oder kastenförmig, ob dezent oder auffällig' in result and 'XX, Die Redaktion' in result and ' Kommentieren' not in result and 'Dienstag, 4. Juni 2019' not in result

    result = load_mock_page('http://iloveponysmag.com/2018/05/24/barbour-coastal/', xmloutput)
    assert 'Eine meiner besten Entscheidungen bisher:' in result and 'Verlassenes Gewächshaus meets versteckter Deich' in result and 'Der Hundestrand in Stein an der Ostsee' in result and 'Tags: Barbour,' not in result and 'Bitte (noch) mehr Bilder von Helle' in result and 'Hinterlasse einen Kommentar' not in result

    result = load_mock_page('https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/', xmloutput)
    assert 'Das ist alles nicht gekennzeichnet, wie soll ich wissen' in result and 'Instagramshops machen es Abmahnanwälten leicht' in result and 'Diese Geschichte teilen' not in result and 'Ähnliche Beiträge ' not in result and 'Ich bin der Ansicht, abwarten und Tee trinken.' in result and 'Danke für dein Feedback. Auch zum Look meiner Seite.' in result and 'Diese Website verwendet Akismet, um Spam zu reduzieren.' not in result

    result = load_mock_page('http://www.womencantalksports.com/top-10-women-talking-sports/', xmloutput)
    assert 'Keep Talking Sports!' in result and 'Category: Blog Popular' not in result and 'Copyright Women Can Talk Sports.' not in result and 'Submit your sports question below' not in result and '3.Charlotte Jones Anderson' in result

    result = load_mock_page('https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html', xmloutput)
    assert 'Schönheit kommt für Pamela von Innen und Außen' in result and 'Die Workout Übungen kannte ich bereits' in result and 'Great post, I like your blog' in result and 'Links zu diesem Post' not in result and 'mehr über mich ♥' not in result and 'Bitte beachte auch die Datenschutzerklärung von Google.' not in result  # and 'Vielen Dank an den den Verlag' in result

    result = load_mock_page('https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html', xmloutput)
    assert 'Grounded in sustainable architecture and refined Vietnamese craftsmanship,' in result and 'and Carmelo Resort' in result and 'OMG what a beautiful place to stay! ' in result and 'Food Advertising by' not in result and 'Dining and Drinking' in result and 'A lovely note makes a beautiful day!' not in result  # and 'Reply' not in result

    result = load_mock_page('https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/', xmloutput)
    assert 'Argentina, the birthplace of polo.' in result and 'Simon Wittenberg travels to the Eternal City in Italy' in result and 'Luxury and lifestyle articles' not in result and 'Pinterest' not in result

    #result = load_mock_page('https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5', xmloutput)
    #print(result)
    #assert result == '???'

    result = load_mock_page('https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/', xmloutput)
    assert 'Prof. Dr. Caja Thimm' in result and 'zur Anmeldung.' in result and 'Next post' not in result and 'Aus den Ländern' not in result

    result = load_mock_page('https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/', xmloutput)
    assert 'Leitsätze des Gerichts' in result and 'III. Die Revision der Beklagten' and 'twittern' not in result and 'Ähnliche Beiträge' not in result and 'd.toelle[at]rechtambild.de' not in result

    result = load_mock_page('http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html', xmloutput)
    # print(result)
    assert 'Wann Blogs einer Impressumspflicht unterliegen,' in result and 'Über mich' not in result and 'Gesetzes- und Rechtsprechungszitate werden automatisch' not in result and 'Mit Verlaub, ich halte das für groben Unsinn.' in result
    ## comments!
    # and 'Comment by' not in result

    result = load_mock_page('https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html', xmloutput)
    #print(result)
    if xmloutput is False:
        assert 'Aufbau und Inhalt' in result and 'Verlag Dr. Otto Schmidt' in result and 'Handbuch' not in result and 'Drucken' not in result and 'Ähnliche Artikel' not in result and 'Anzeige:' not in result  # and 'Kommentar schreiben' not in result

    result = load_mock_page('https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen', xmloutput)
    assert 'Auch der Verweis auf ehrverletzende Bewertungen' in result and 'Fanden Sie diesen Artikel nützlich?' not in result and 'Kommentar hinzufügen' not in result  # and 'Zu seinen Tätigkeitsfeldern zählen' not in result
    if xmloutput is False:
        assert 'Anja Schmoll-Trautmann' not in result and 'Aktuell' not in result

    result = load_mock_page('https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage', xmloutput)
    assert 'Alle Artikel zu unseren Recherchen' not in result and 'Vorweg: Die beteiligten AfD-Politiker' in result and 'ist heute Abend um 21 Uhr auch im ZDF-Magazin Frontal' in result and 'Wir informieren Sie regelmäßig zum Thema Neue Rechte' not in result and 'Kommentar verfassen' not in result and 'weiterlesen' not in result

    result = load_mock_page('https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845', xmloutput)
    assert '05:28 Uhr' not in result and 'Bahn-Konkurrenten wie Flixbus fürchten durch den geplanten Deutschlandtakt' in result and 'ICE im S-Bahn-Takt' not in result and 'Diskussion zu diesem Artikel auf:' not in result and 'Berater-Affäre bringt Bahnchef Lutz in Bedrängnis' not in result and 'auch der Bus ein klimafreundliches Verkehrsmittel sei' in result

    result = load_mock_page('https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/', xmloutput)
    assert 'Rund ums Fahrzeug' not in result and 'in punkto Sicherheit, Bedienung, Ergonomie' in result and 'Grenzwert der Richtlinie 2014/79/EU' in result and 'Diesel-Umtauschprämien' not in result and 'Besonders bei Babyschalen sollte geprüft werden' in result

    result = load_mock_page('https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/', xmloutput)
    assert 'Was I losing my mind?' in result and 'being cached after their first access.' in result and 'Finding a Fix' in result and 'from django.conf import settings' in result and 'New Call-to-action' not in result and 'Contact us' not in result and 'Back to blog' not in result and 'You might also like:' not in result

    result = load_mock_page('https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/', xmloutput)
    assert 'Vor knapp zwei Wochen' in result and 'gibt es in der dazugehörigen Vorstellungs-News.' in result and 'Themen:' not in result and 'bis Januar 2009 Artikel für ComputerBase verfasst.' not in result and 'Warum Werbebanner?' not in result and '71 Kommentare' not in result

    result = load_mock_page('http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html', xmloutput)
    assert '就放心去吧' in result and 'Repeat Chorus' in result and 'Older post' not in result and 'Thank you for your support!' not in result

    result = load_mock_page('https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/', xmloutput)
    assert 'Frank Thelen, Investor' in result and 'Female founders must constantly consider' in result and 'Thema des öffentlichen Interesses' in result and 'Nach langjähriger Tätigkeit im Ausland' not in result and 'Schaut man ganz genau hin, ist der Habeck-Kommentar' in result and 'Mit Absendung des Formulars willige ich' not in result and 'Kommentieren' not in result  # and 'Auch interessant' not in result and 'Wir tun jeden Tag, was wir lieben.' not in result

    result = load_mock_page('https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/', xmloutput)
    assert 'Welche Werbeeinnahmen erwarten Sie hier langfristig?' in result and 'wir haben keinerlei Pläne, das zu verändern.' in result and 'Nachrichtenüberblick abonnieren' not in result and 'über alle aktuellen Entwicklungen auf dem Laufenden.' not in result and 'Schlagworte' not in result and 'Teilen' not in result and 'Dauerzoff um drohenden UKW-Blackout' not in result and 'Mobilcom Debitel has charged me for third party' in result

    result = load_mock_page('https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/', xmloutput)
    assert 'Zeit für Loslassen und Entspannung.' in result and 'Wie sieht dein Alltag aus?' in result and 'Erfrischende, abschwellende Augencreme Phyto Contour' in result and 'Vielen Dank Anja für deine Tipps rund um Beauty' in result and 'Betreiberin von incurvy Plus Size' not in result and 'Wir verwenden Cookies' not in result  # and 'Das Thema könnte dich auch interessieren:' not in result

    result = load_mock_page('https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843', xmloutput)
    assert 'No grape variety invites as much intrigue' in result and 'With just 0.9 hectares' in result and 'Related Subjects' not in result and 'Audios and videos on the topic' not in result  # and 'But boozers in Berlin' not in result

    result = load_mock_page('https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html', xmloutput)
    assert 'Adele feierte ausgelassen mit den Spice Girls' in result and 'wie sich Adele weiterentwickelt.' in result and 'Sommerzeit ist Urlaubszeit,' not in result and 'Lade weitere Inhalte' not in result

    result = load_mock_page('https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx', xmloutput)
    assert 'Konflikte mag keiner.' in result and 'Gespräche meistern können.' in result and 'Weiterführender Link' not in result and 'Flexible Wege in die' not in result and 'Storage für den Mittelstand' not in result

    result = load_mock_page('https://novalanalove.com/ear-candy/', xmloutput)
    assert 'Earcuff: Zoeca' in result and 'mit längeren Ohrringen (:' in result and 'Kreole: Stella Hoops' in result and 'Jetzt heißt es schnell sein:' not in result and 'Diese Website speichert Cookies' not in result and 'VON Sina Giebel' not in result

    result = load_mock_page('http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/', xmloutput)
    assert 'Zuerst dachte ich, ich könnte das' in result and 'x Franzi' in result and 'Flauschjacke: Bershka' in result and 'Palm Springs Mini (links)' not in result and 'Diese Website verwendet Akismet' not in result and 'New York, New York' not in result

    result = load_mock_page('https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html', xmloutput)
    assert 'Die Psyche spielt eine nicht unerhebliche Rolle' in result and 'Sportskanone oder Sportmuffel' not in result and 'PINNEN' not in result and '2. Satt essen bei den Mahlzeiten' in result and 'Bringt die Kilos zum Purzeln!' not in result and 'Crash-Diäten ziehen meist den Jojo-Effekt' not in result

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
    assert 'Die Ökobilanz von Elektroautos' in result and 'Nur die Folie bleibt zurück' in result and 'Forum zum Thema:' not in result  # and 'Highlights aus dem Heft:' not in result and 'TR 7/2019' not in result 

    result = load_mock_page('https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact', xmloutput)
    assert 'Normally, video calls tend to' in result and 'across both the eyes and nose.' in result and 'Added ARKit explanation and tweet.' in result and 'Singapore’s public health program' not in result and 'Command Line delivers daily updates' not in result

    result = load_mock_page('https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/', xmloutput)
    assert 'in keinem Braut-Beauty-Programm fehlen darf?' in result and 'nicht nur vor der Hochzeit ein absolutes Muss.' in result and 'Gesundes, glänzendes Haar' in result and 'Neue Wandbilder von Posterlounge' not in result and 'mit meinen Texten und mit meinen Gedanken.' not in result and 'Erforderliche Felder sind mit * markiert.' not in result

    result = load_mock_page('https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis', xmloutput)
    assert 'Stilles Rackern, statt lautem Deklamieren.' in result and 'Watt jibt’s n hier zu lachen?' in result and 'Das Brandenbuch. Ein Land in Stichworten.' in result and 'Bürgerbeteiligung' not in result and 'Anmelden' not in result and 'Foto: Timur' not in result and 'Schlagworte' not in result and 'Zeilenumbrüche und Absätze werden automatisch erzeugt.' not in result

    result = load_mock_page('https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html', xmloutput)
    assert 'Wakebeach 257' in result and 'Be there or be square!' in result and 'Hier geht’s zur Facebook Veranstaltung' in result and 'More from News' not in result and 'von Redaktion MSM' not in result and 'add yours.' not in result  # and 'Blue Tomato präsentiert die dritte' in result

    result = load_mock_page('https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/', xmloutput)
    assert 'Rocket Pass 4 will begin at 10:00 a.m. PDT' in result and 'Holy shit, Mortal Kombat 11' in result and 'Let us know down below in the comments' in result and 'Related Topics' not in result and 'You can keep up with me on Twitter' not in result and 'Hit the track today with Mario Kart Tour' not in result  # and 'what to do with thousands of crates tho' in result

    result = load_mock_page('https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding', xmloutput)
    assert 'Given a set of high-dimensional objects' in result and 'Herein a heavy-tailed Student t-distribution' in result and 'Categories:' not in result and 'Conditional random field' not in result

    result = load_mock_page('https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/', xmloutput)
    assert 'Niedlicher Roboter-Spielkamerad: Anki Cozmo' in result and 'Empfehlungen von Dennis:' in result and 'Unterstütze unsere Arbeit' not in result and 'Deepfake-Hollywood' not in result and 'Avengers' not in result and 'Katzenschreck' not in result

    result = load_mock_page('http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/', xmloutput)
    assert 'Hunderttausende von jungen Paaren' in result and 'wie flatterhaft das Mädl ist? :)' in result and 'Malte Welding' not in result and 'YouTube und die Alten' not in result and 'Autokorrektur' not in result

    result = load_mock_page('https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/', xmloutput)
    assert 'Rüschen und Volants.' in result and 'ihr jedes Jahr tragen könnt?' in result and 'Das könnte dich auch interessieren' not in result and 'Catherine Classic Lac 602' not in result  # and 'mein Lieblingskleid vereint' in result

    result = load_mock_page('https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/', xmloutput)
    assert 'Einblicke in die Vision zukünftiger Softwaregenerationen.' in result and 'Frage 4: Welche Rolle spielt Big Data in Bezug auf Assistenz-Systeme und KI?' in result and 'von The unbelievable Machine Company (*um) zur Verfügung gestellt.' in result and 'Matthias Weber ist ERP-Experte mit langjähriger Berufserfahrung.' not in result and 'Die Top 5 digitalen Trends für den Mittelstand' not in result and ', leading edge,' not in result  # and 'Lesen Sie hier einen weiteren spannenden Beitrag' not in result

    result = load_mock_page('https://boingboing.net/2013/07/19/hating-millennials-the-preju.html', xmloutput)
    assert 'Click through for the whole thing.' in result and 'The generation we love to dump on' in result and 'GET THE BOING BOING NEWSLETTER' not in result  # and 'happy mutants' not in result and 'Patti Smith and Stewart Copeland' not in result

    result = load_mock_page('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/', xmloutput)
    assert 'Erin Spiceland is a Software Engineer for SpaceX.' in result and 'make effective plans and goals for the future' in result and 'looking forward to next?' in result and 'Research Consultant at Adelard LLP' in result and 'Related posts' not in result and 'Jeremy Epling' not in result and 'Missed the main event?' not in result and 'Privacy' not in result

    result = load_mock_page('https://lady50plus.de/2019/06/19/sekre-mystery-bag/', xmloutput)
    assert 'ist eine echte Luxushandtasche' in result and 'Insgesamt 160 weibliche „Designerinnen“' in result and 'Sei herzlich gegrüßt' in result and 'Ein Mann alleine hätte niemals' in result and 'Erforderliche Felder sind mit' not in result and 'Benachrichtige mich' not in result and 'Reisen ist meine große Leidenschaft' not in result and 'Styling Tipps für Oktober' not in result and 'in den Bann ziehen!' in result

    result = load_mock_page('https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer', xmloutput)
    assert 'Neuer Geschäftsführender Leiter' in result and 'nach Leipzig wechseln.' in result and 'Mehr zum Thema' not in result and 'Folgen Sie uns auf Facebook und Twitter' not in result and 'Aktuelle Ausgabe' not in result

    result = load_mock_page('https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite', xmloutput)
    assert 'Le décret n°2019-1130 validant' in result and 'restructurant à cet effet ».' in result and ' utilise des cookies pour' not in result and 'En savoir plus' not in result  # and 'CNRS, Inserm, Inria.' not in result

    result = load_mock_page('https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html', xmloutput)
    assert 'Starke Hitze nur in der Mitte' in result and 'ca. 35,7×29,4 cm' in result and 'Wir sind im Steak-Himmel!' in result and 'Samsung Galaxy S10 128GB' not in result and 'Für Links auf dieser Seite' not in result  # and 'Inga Buller ist Head of Social' not in result

    result = load_mock_page('http://www.sauvonsluniversite.fr/spip.php?article8532', xmloutput)
    assert 'L’AG Éducation Île-de-France inter-degrés' in result and 'Grève et mobilisation pour le climat' in result and 'suivi.reformes.blanquer@gmail.com' in result and 'Sauvons l’Université !' not in result and 'La semaine de SLU' not in result

    result = load_mock_page('https://www.spiegel.de/spiegel/print/d-161500790.html', xmloutput)
    assert 'Wie konnte es dazu kommen?' in result and 'Die Geschichte beginnt am 26. Oktober' in result and 'Es stützt seine Version.' in result and 'und Vorteile sichern!' not in result and 'Verschickt' not in result and 'Die digitale Welt der Nachrichten.' not in result and 'Vervielfältigung nur mit Genehmigung' not in result

    result = load_mock_page('https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/', xmloutput)
    assert 'I use a Skylake processor with GNU GCC 8.3.' in result and 'gsoc-2018' in result and '0.091 GB/s' in result and 'version 0.2 on vcpkg.' in result and 'Leave a Reply' not in result and 'Science and Technology links' not in result and 'Proudly powered by WordPress' not in result

    result = load_mock_page('https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission', xmloutput)
    assert '36 Stunden.' in result and 'Nationale Egoismen' in result and 'Deutschland kaum beschleunigt.' in result and 'Durchgehende Tickets fehlen' not in result and 'geprägte Fehlentscheidung.' in result and 'horrende Preise für miserablen Service bezahlen?' in result and 'Bitte melden Sie sich an, um zu kommentieren.' not in result

    result = load_mock_page('https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020', xmloutput)
    assert 'Performativité' in result and 'Les individus productifs communiquent' in result and 'de nos espoirs et de nos désirs.' in result and 'A la tribune je monterai' not in result and 'À découvrir' not in result and 'Le fil culture' not in result

    result = load_mock_page('https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/', xmloutput)
    assert 'as further access is restored.' in result and 'Read further in the pursuit of knowledge' not in result and 'Here’s what that means.' not in result and 'Stay up-to-date on our work.' not in result and 'Photo credits' not in result  # and 'Bu yazının Türkçe’sini buradan okuyabilirsiniz' in result

    result = load_mock_page('https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH', xmloutput)
    assert '4 Min Read' not in result and 'Factbox: Key winners' not in result and 'Despite an unknown cast,' in result and 'Additional reporting by' in result  # and 'The Thomson Reuters Trust Principles' not in result

    result = load_mock_page('https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2', xmloutput)
    # print(result)
    assert 'Microsoft Corp said on Thursday' in result and 'Postmedia is committed' in result and 'I consent to receiving' not in result and 'It was not immediately clear if' in result and 'turns CO2 into soap' not in result
    if xmloutput is False:
        assert 'Reuters files' not in result

    #result = load_mock_page('https://www.lanouvellerepublique.fr/indre-et-loire/commune/saint-martin-le-beau/family-park-la-derniere-saison-a-saint-martin-le-beau', xmloutput)
    #print(result)
    #assert result == '???'

    #result = load_mock_page('', xmloutput)
    #assert '' in result and '' in result and '' not in result and '' not in result and '' not in result

    # try:
    # ...
    # except AssertionError as err:
    #    if platform.system() == 'Windows':
    #        pass
    #    else:
    #        raise AssertionError(err)


def test_pages():
    '''Test on real web pages'''
    metadata = extract_metadata(load_mock_page_meta('http://blog.python.org/2016/12/python-360-is-now-available.html'))
    assert metadata.title == 'Python 3.6.0 is now available!'
    assert metadata.description == 'Python 3.6.0 is now available! Python 3.6.0 is the newest major release of the Python language, and it contains many new features and opti...'
    assert metadata.author == 'Ned Deily'
    assert metadata.url == 'http://blog.python.org/2016/12/python-360-is-now-available.html'
    assert metadata.sitename == 'blog.python.org'

    metadata = extract_metadata(load_mock_page_meta('https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/'))
    assert metadata.title == 'Want to See a More Diverse WordPress Contributor Community? So Do We.'
    assert metadata.description == 'More diverse speakers at WordCamps means a more diverse community contributing to WordPress — and that results in better software for everyone.'
    assert metadata.sitename == 'The WordPress.com Blog'
    assert metadata.url == 'https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/'

    metadata = extract_metadata(load_mock_page_meta('https://creativecommons.org/about/'))
    assert metadata.title == 'What we do - Creative Commons'
    assert metadata.description == 'What is Creative Commons? Creative Commons helps you legally share your knowledge and creativity to build a more equitable, accessible, and innovative world. We unlock the full potential of the internet to drive a new era of development, growth and productivity. With a network of staff, board, and affiliates around the world, Creative Commons provides … Read More "What we do"'
    assert metadata.sitename == 'Creative Commons'
    assert metadata.url == 'https://creativecommons.org/about/'
    # date None

    metadata = extract_metadata(load_mock_page_meta('https://www.creativecommons.at/faircoin-hackathon'))
    assert metadata.title == 'FairCoin hackathon beim Sommercamp'
    # assert metadata.url == '/faircoin-hackathon'

    metadata = extract_metadata(load_mock_page_meta('https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/'))
    assert metadata.title == 'Die Cider Connection: Abmahnungen gegen Nutzer von Creative-Commons-Bildern'
    assert metadata.author == 'Markus Reuter'
    assert metadata.description == 'Seit Dezember 2015 verschickt eine Cider Connection zahlreiche Abmahnungen wegen fehlerhafter Creative-Commons-Referenzierungen. Wir haben recherchiert und legen jetzt das Netzwerk der Abmahner offen.'
    assert metadata.sitename == 'netzpolitik.org'
    # cats + tags
    assert metadata.url == 'https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/'

    metadata = extract_metadata(load_mock_page_meta('https://www.befifty.de/home/2017/7/12/unter-uns-montauk'))
    assert metadata.title == 'Das vielleicht schönste Ende der Welt: Montauk'
    assert metadata.author == 'Beate Finken'
    assert metadata.description == 'Ein Strand, ist ein Strand, ist ein Strand Ein Strand, ist ein Strand, ist ein Strand. Von wegen! In Italien ist alles wohl organisiert, Handtuch an Handtuch oder Liegestuhl an Liegestuhl. In der Karibik liegt man unter Palmen im Sand und in Marbella dominieren Beton und eine kerzengerade Promenade'
    assert metadata.sitename == 'BeFifty'
    assert metadata.categories == ['Travel', 'Amerika']
    assert metadata.url == 'https://www.befifty.de/home/2017/7/12/unter-uns-montauk'

    metadata = extract_metadata(load_mock_page_meta('https://www.soundofscience.fr/1927'))
    assert metadata.title == 'Une candidature collective à la présidence du HCERES'
    assert metadata.author == 'Martin Clavey'
    assert metadata.description.startswith('En réaction à la candidature du conseiller recherche')
    assert metadata.sitename == 'The Sound Of Science'
    assert metadata.categories == ['Politique scientifique française']
    assert metadata.tags == ['évaluation', 'HCERES']
    assert metadata.url == 'https://www.soundofscience.fr/1927'

    metadata = extract_metadata(load_mock_page_meta('https://laviedesidees.fr/L-evaluation-et-les-listes-de.html'))
    assert metadata.title == 'L’évaluation et les listes de revues'
    assert metadata.author == 'Florence Audier'
    assert metadata.description.startswith("L'évaluation, et la place")
    assert metadata.sitename == 'La Vie des idées'
    # assert metadata.categories == ['Essai', 'Économie']
    assert metadata.tags == []
    # <meta property="og:type" content="article" />
    # <meta name="DC:type" content="journalArticle">
    assert metadata.url == 'http://www.laviedesidees.fr/L-evaluation-et-les-listes-de.html'

    metadata = extract_metadata(load_mock_page_meta('https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens'))
    assert metadata.title == "Thousands of UK academics 'treated as second-class citizens'"
    assert metadata.author == 'Richard Adams'
    assert metadata.description.startswith('Report claims higher education institutions')
    assert metadata.sitename == 'The Guardian' # originally "the Guardian"
    assert metadata.categories == ['Education']
    assert 'Higher education' in metadata.tags[0]
    # meta name="keywords"
    assert metadata.url == 'http://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens'

    metadata = extract_metadata(load_mock_page_meta('https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html'))
    assert metadata.title == 'Flint flake tool partially covered by birch tar adds to evidence of Neanderthal complex thinking'
    assert metadata.author == 'Bob Yirka'
    assert metadata.description == 'A team of researchers affiliated with several institutions in The Netherlands has found evidence in small a cutting tool of Neanderthals using birch tar. In their paper published in Proceedings of the National Academy of Sciences, the group describes the tool and what it revealed about Neanderthal technology.'
    assert metadata.sitename == 'Phys.org'
    # assert metadata.categories == ['Archaeology', 'Fossils']
    assert metadata.tags == ["Science, Physics News, Science news, Technology News, Physics, Materials, Nanotech, Technology, Science"]
    assert metadata.url == 'https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html'

    metadata = extract_metadata(load_mock_page_meta('https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/'))
    assert metadata.title == "Mercurial's Journey to and Reflections on Python 3"
    # assert metadata.author == 'Gregory Szorc'
    # assert metadata.sitename == 'gregoryszorc'
    # assert metadata.categories == ['Mercurial', 'Python']

    metadata = extract_metadata(load_mock_page_meta('https://www.pluralsight.com/tech-blog/managing-python-environments/'))
    assert metadata.title == 'Managing Python Environments'
    assert metadata.author == 'John Walk'
    assert metadata.description.startswith("If you're not careful,")
    assert metadata.sitename == 'pluralsight.com'  # 'Pluralsight'
    # assert metadata.categories == ['practices']
    # assert metadata.tags == ['python', 'docker', ' getting started']
    assert metadata.url == 'https://www.pluralsight.com/tech-blog/managing-python-environments/'

    url = 'https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'What is Rust and why is it so popular? - Stack Overflow Blog'
    assert metadata.author == 'Jake Goulding'
    assert metadata.sitename == 'Stack Overflow Blog'
    assert metadata.categories == ['Bulletin']
    assert metadata.tags == ['programming', 'rust']
    assert metadata.url == url

    url = 'https://www.dw.com/en/berlin-confronts-germanys-colonial-past-with-new-initiative/a-52060881'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert "Berlin confronts Germany's colonial past with new initiative" in metadata.title
    assert metadata.author == 'Deutsche Welle'  # actually 'Ben Knight'
    assert metadata.description == "The German capital has launched a five-year project to mark its part in European colonialism. Streets which still honor leaders who led the Reich's imperial expansion will be renamed — and some locals aren't happy."
    assert metadata.sitename == 'DW.COM'  # 'DW - Deutsche Welle'
    assert 'Africa' in metadata.tags[0]
    assert metadata.url == url

    metadata = extract_metadata(load_mock_page_meta('https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/'))
    assert metadata.title.startswith('Management of Intact Forestlands by Indigenous Peoples Key to Protecting Climate')
    assert metadata.author == 'The Planetary Press'  # actually 'Julie Mollins'
    assert metadata.sitename == 'The Planetary Press'
    assert 'Climate' in metadata.categories
    assert metadata.url == 'https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/'

    url = 'https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Access to Wikipedia restored in Turkey after more than two and a half years'
    assert metadata.author == 'Wikimedia Foundation'
    assert metadata.description.startswith('Today, on Wikipedia’s 19th birthday')
    assert metadata.sitename == 'Wikimedia Foundation'
    # assert metadata.categories == ['Politics', 'Turkey', 'Wikipedia']
    assert metadata.url == url

    url = 'https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title.endswith('scores historic upset at SAG awards, boosting Oscar chances') # &#039;Parasite&#039;
    assert metadata.author == 'Jill Serjeant'
    assert metadata.date == '2020-01-20'
    # assert metadata.description == '“Parasite,” the Korean language social satire about the wealth gap in South Korea, was the first film in a foreign language to win the top prize of best cast ensemble in the 26 year-history of the SAG awards.'
    assert metadata.sitename == 'Reuters'
    assert 'Media' in metadata.categories[0]  # ['Parasite', 'SAG awards', 'Cinema']
    assert metadata.url == 'https://www.reuters.com/article/us-awards-sag-idUSKBN1ZI0EH'

    url = 'https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Ravenous wild goats ruled this island for over a century. Now, it's being reborn."
    assert metadata.author == 'Michael Hingston'
    assert metadata.description.startswith('The rocky island of Redonda, once stripped of its flora and fauna')
    assert metadata.sitename == 'National Geographic'
    assert metadata.categories == ['Environment and Conservation']  # ['Goats', 'Environment', 'Redonda']
    assert metadata.url == url

    url = 'https://www.nature.com/articles/d41586-019-02790-3'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Gigantic Chinese telescope opens to astronomers worldwide'
    assert metadata.author == 'Elizabeth Gibney'
    assert metadata.description == 'FAST has superior sensitivity to detect cosmic phenomena, including fast radio bursts and pulsars.'
    assert metadata.sitename == 'Nature'
    assert 'Exoplanets' in metadata.categories  # ['Astronomy', 'Telescope', 'China']
    assert metadata.url == url

    url = 'https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Carrie Lam should study Tsai Ing-wen’s playbook' # '<h1 data-v-1223d442="" class="inner__main-headline main-headline">Taiwanese President Tsai Ing-wen’s political playbook should be essential reading for Hong Kong leader Carrie Lam</h1>'
    # author in JSON-LD
    assert metadata.author == 'Alice Wu'
    assert metadata.url == url

    url = 'https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Nutzerbasierte Abrechnung: Musik-Stars fordern neues Streaming-Modell'
    # author overriden from JSON-LD + double name
    assert 'Benjamin Fischer' in metadata.author
    assert metadata.sitename == 'Frankfurter Allgemeine Zeitung'
    assert metadata.url == 'https://www.faz.net/1.6604622'

    url = 'https://boingboing.net/2013/07/19/hating-millennials-the-preju.html'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Hating Millennials - the prejudice you're allowed to boast about"
    assert metadata.author == 'Cory Doctorow'
    assert metadata.sitename == 'Boing Boing'
    assert metadata.url == url

    url = 'https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Wie kann ich schnell abnehmen? Der Schlachtplan zum Wunschgewicht'
    assert metadata.author == 'Diane Buckstegge'
    assert metadata.sitename == 'Gofeminin' # originally "gofeminin"
    assert metadata.url == url

    url = 'https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Leader spotlight: Erin Spiceland'
    assert metadata.author == 'Jessica Rudder'
    assert metadata.description.startswith('We’re spending Women’s History')
    assert metadata.sitename == 'The GitHub Blog'
    assert metadata.categories == ['Community']
    assert metadata.url == url

    url = 'https://www.spiegel.de/spiegel/print/d-161500790.html'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Ein Albtraum'
    # assert metadata.author == 'Clemens Höges'

    url = 'https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/'
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == 'Despite everything, U.S. emissions dipped in 2019'
    # in JSON-LD
    assert metadata.author == 'Nathanael Johnson'
    assert metadata.sitename == 'Salon.com'
    # in header
    assert 'Science & Health' in metadata.categories
    assert 'Gas Industry' in metadata.tags and 'coal emissions' in metadata.tags
    assert metadata.url == url

    url = 'https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html'
    metadata = extract_metadata(load_mock_page_meta(url), default_url=url)
    assert metadata.url == url
    assert 'Korinna Hennig' in metadata.author
    assert 'Ältere Menschen' in str(metadata.tags)

    url = "https://www.mercurynews.com/2023/01/16/letters-1119/"
    metadata = extract_metadata(load_mock_page(url, xml_flag=True))

    
if __name__ == '__main__':
    test_extract(False)
    test_extract(True)
    test_pages()
