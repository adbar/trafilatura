# -*- coding: utf-8 -*-
"""
Unit tests for the html-extractor library.
"""

import logging
import os
import sys
# https://docs.pytest.org/en/latest/

import html_extractor
from html_extractor import cli, utils

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)




MOCK_PAGES = { \
'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/': 'die-partei.net.luebeck.html', \
'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html': 'bmjv.de.konsum.html', \
'http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/': 'kulinariaathome.com.mandelplätzchen.html', \
'https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/': 'denkanstoos.com.2012.html', \
'http://bunterepublik.wordpress.com/2012/04/13/schwafelrunde-ohne-ritter/': 'bunterepublik.com.schwafelrunde.html', \
'https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft': 'demokratiewebstatt.at.luft.html', \
'http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html': 'toralin.de.schmierfett.html', \
'https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess': 'ebrosia.de.zinfandel.html', \
'https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html': 'landwirt.com.sensortechnik.html', \
'http://schleifen.ucoz.de/blog/briefe/2010-10-26-18': 'schleifen.ucoz.de.briefe.html', \
'http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung': 'rs-ingenieure.de.tragwerksplanung.html', \
'http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html': 'simplyscience.ch.erdoel.html', \
'http://www.shingon-reiki.de/reiki-und-schamanismus/': 'shingon-reiki.de.schamanismus.html', \
'http://love-hina.ch/news/0409.html': 'love-hina.ch.0409.html', \
'http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html': 'cdu-fraktion-erfurt.de.waldorfschule.html', \
'http://www.wehranlage-horka.de/veranstaltung/887/': 'wehranlage-horka.de.887.html',
'https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/': 'de.creativecommons.org.endlich.html', \
'https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/': 'piratenpartei-mv.de.grundeinkommen.html', \
'https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/': 'spektrum.de.engelbart.html', \
'https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975': 'sueddeutsche.de.genderdebatte.html', \
'https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html': 'rnz.de.witzel.html',
'https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg': 'austria.info.radfahren.html',
'https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/': 'buchperlen.wordpress.com.html', \
'https://www.greenpeace.de/themen/artenvielfalt/loechrige-lebensversicherung': 'greenpeace.org.artenvielfalt.html', \
'https://www.fairkom.eu/about': 'fairkom.eu.about.html', \
'https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461': 'futurezone.at.lyft.html', \
'http://www.hundeverein-kreisunna.de/unserverein.html': 'hundeverein-kreisunna.de.html', \
'https://viehbacher.com/de/steuerrecht': 'viehbacher.com.steuerrecht.html', \
'http://www.jovelstefan.de/2011/09/11/gefallt-mir/': 'jovelstefan.de.gefallt.html', \
'https://www.stuttgart.de/item/show/132240/1': 'stuttgart.de.html', \
'https://www.heise.de/newsticker/meldung/Zahlen-bitte-100-scheinbare-Kanaele-die-den-Hype-um-Marsmenschen-ausloesten-4438438.html': 'heise.de.marsmenschen.html', \
'https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/': 'modepilot.de.duschkopf.html', \
'https://www.otto.de/twoforfashion/strohtasche/': 'otto.de.twoforfashion.html', \
'http://iloveponysmag.com/2018/05/24/barbour-coastal/': 'iloveponysmag.com.barbour.html', \
'https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/': 'moritz-meyer.net.vreni.html', \
'http://www.womencantalksports.com/top-10-women-talking-sports/': 'womencantalksports.com.top10.html', \
'https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html': 'plentylife.blogspot.pamela-reif.html', \
'https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html': 'luxuryhaven.co.hyatt.html', \
'https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/': 'luxuriousmagazine.com.polo.html', \
'https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5': 'chip.de.tests.html', \
'https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/': 'gruen-digital.de.jahrestagung.html', \
'https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/': 'rechtambild.de.kochbuch.html', \
'http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html': 'internet-law.de.pseudonymen.html', \
'https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html': 'telemedicus.info.rezension.html', \
'https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen': 'cnet.de.schutz.html', \
'https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage': 'correctiv.org.zusage.html', \
'https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845': 'sueddeutsche.de.flixtrain.html', \
'https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/': 'adac.de.kindersitze.html', \
'https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/': 'caktusgroup.com.django.html', \
'https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/': 'computerbase.de.htc.html', \
'http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html': 'chineselyrics4u.com.zhineng.html', \
'https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/': 'basicthinking.de.tweets.html', \
'https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/': 'meedia.de.freenet.html', \
'https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/': 'incurvy.de.wellness.html', \
}
# '': '', \

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def load_mock_page(url, txtoutput=False, langcheck=None):
    '''load mock page from samples'''
    # TODO: https://chardet.readthedocs.io/en/latest/usage.html
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    except UnicodeDecodeError:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r', encoding='ISO-8859-1') as inputf:
            htmlstring = inputf.read()
    result = html_extractor.process_record(htmlstring, url, '0000', tei_output=False, txt_output=txtoutput, target_language=langcheck)
    return result


def test_trim():
    '''test string trimming'''
    assert html_extractor.trim('	Test  ') == 'Test'
    assert html_extractor.trim('\t\tTest  Test\r\n') == 'Test Test'


def test_download():
    '''test page download'''
    assert utils.fetch_url('https://httpbin.org/status/404') is None
    url = 'https://httpbin.org/status/200'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, url, False, True) is None
    url = 'https://httpbin.org/links/2/2'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, url, False, True) is None
    url = 'https://httpbin.org/html'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, url, False, True) is not None


def test_main(txtoutput=False):
    '''test extraction from HTML'''
    result = load_mock_page('https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/', txtoutput)
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result

    result = load_mock_page('https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html', txtoutput)
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result

    result = load_mock_page('https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/', txtoutput)
    assert 'Two or three 10-15 min' in result and 'What type? Etc. (30 mins)' in result and 'Dieser Eintrag wurde veröffentlicht' not in result # and 'Mit anderen Teillen' not in result

    result = load_mock_page('http://bunterepublik.wordpress.com/2012/04/13/schwafelrunde-ohne-ritter/', txtoutput)
    assert 'Abgelegt unter' not in result and 'Nächster Beitrag' not in result and 'Die Schwafelrunde' in result and 'zusammen.' in result

    result = load_mock_page('https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess', txtoutput)
    assert 'Das Bukett präsentiert sich' in result and 'Besonders gut passt er zu asiatischen Gerichten' in result and 'Kunden kauften auch' not in result and 'Gutschein sichern' not in result

    result = load_mock_page('https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html', txtoutput)
    assert 'Überwachung der somatischen Zellen' in result and 'tragbaren Ultraschall-Geräten' in result and 'Kotkonsistenz' in result  and 'Anzeigentarife' not in result # and 'Aktuelle Berichte aus dieser Kategorie' not in result

    result = load_mock_page('http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung', txtoutput)
    assert 'Wir bearbeiten alle Leistungsbilder' in result and 'Brückenbau' not in result

    result = load_mock_page('http://www.shingon-reiki.de/reiki-und-schamanismus/', txtoutput)
    assert 'Catch Evolution' not in result and 'und gekennzeichnet mit' not in result and 'Heut geht es' in result and 'Ich komme dann zu dir vor Ort.' in result

    result = load_mock_page('http://love-hina.ch/news/0409.html', txtoutput)
    assert 'Kapitel 121 ist' in result and 'Besucher online' not in result and 'Kommentare schreiben' not in result

    #result = load_mock_page('http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html', txtoutput)
    #print(result)
    #assert 'der steigenden Nachfrage gerecht zu werden.' in result and 'Zurück zur Übersicht' not in result and 'Erhöhung für Zoo-Eintritt' not in result

    result = load_mock_page('https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/', txtoutput)
    assert 'das letzte Wort sein kann.' in result and 'Ähnliche Beiträge' not in result
    #  and 'Michael Blahm' not in result # comments

    result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975', txtoutput)
    assert 'Es ist erstaunlich:' in result and 'Damaris Nübling ist Professorin' in result and 'Der Fall Weinstein' not in result and 'Leser empfehlen' not in result

    result = load_mock_page('https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/', txtoutput)
    assert 'Unter diesem Motto findet am 14. September' in result and 'Volksinitiative Schweiz zum Grundeinkommen.' in result and 'getaggt mit:' not in result # and 'Was denkst du?' not in result

    result = load_mock_page('https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/', txtoutput)
    assert 'Zweitens wird der Genderstern' in result and 'alldem leider – nichts.' in result
    # and 'Beitragsbild' not in result

    result = load_mock_page('http://www.wehranlage-horka.de/veranstaltung/887/', txtoutput)
    assert 'In eine andere Zeit' in result and 'Infos zum Verein' not in result
    # and 'Groß­vä­ter' in result # segmented words

    result = load_mock_page('https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft', txtoutput)
    assert 'Eines der großen Probleme,' in result and 'Millionen Menschen fahren jeden Tag' in result and 'versteinerte Dinosaurierknochen.' in result and 'Clipdealer' not in result and 'Teste dein Wissen' not in result and 'Thema: Fußball' not in result

    result = load_mock_page('http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html', txtoutput)
    assert 'Erdöl bildet nach Millionen' in result and 'in unserem Artikel "Warum wird das Erdöl knapp?".' in result # and 'Die Natur ist aus chemischen Elementen aufgebaut' not in result

    result = load_mock_page('https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html', txtoutput)
    assert 'Für einen Roman' in result and 'Auszeichnung der Branche.' in result

    result = load_mock_page('https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/', txtoutput)
    # print(result)
    assert 'Dann sollten Sie erst recht' in result and 'als saure Gürkchen entlarvte Ex-Boyfriends.' in result and 'Ähnliche Beiträge' not in result

    # bug here
    if txtoutput is False:
        result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975', langcheck='de')
        assert 'Es ist erstaunlich:'in result and 'Foto: rclassen' not in result and '(Narr-Verlag).' in result and 'Diskussion zu diesem Artikel auf:' not in result

    result = load_mock_page('http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html', txtoutput)
    assert 'künftig das XADO-Schutzfett verwenden.' in result and 'bis zu 50% Verschleiß.' in result and 'Die Lebensdauer von Bauteilen erhöht sich beträchtlich.' in result and 'Newsletter' not in result # and 'Sie könnten auch an folgenden Artikeln interessiert sein' not in result

    result = load_mock_page('https://www.greenpeace.de/themen/artenvielfalt/loechrige-lebensversicherung', txtoutput)
    assert 'Wir erodieren global' in result and 'Pummelige Hummeln, schillernde Schmetterlinge' not in result and 'Doch daran arbeitet wir.' in result and 'Menschenrechtsverletzungen bei Frauen und Kindern' not in result

    result = load_mock_page('https://www.fairkom.eu/about', txtoutput)
    assert 'ein gemeinwohlorientiertes Partnerschaftsnetzwerk' in result and 'Stimmberechtigung bei der Generalversammlung.' in result and 'support@fairkom.eu' not in result

    result = load_mock_page('https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461', txtoutput)
    assert 'Einige Kunden des Fahrdienst-Vermittler Lyft' in result and 'zeitweise rund vier Prozent.' in result and 'Allgemeine Nutzungsbedingungen' not in result # and 'Waymo bittet Autohersteller um Geld' not in result

    result = load_mock_page('http://www.hundeverein-kreisunna.de/unserverein.html', txtoutput)
    assert 'Beate und Norbert Olschewski' in result and 'ein Familienmitglied und unser Freund.' in result and 'zurück zur Startseite' not in result

    result = load_mock_page('https://viehbacher.com/de/steuerrecht', txtoutput)
    assert 'und wirtschaftlich orientierte Privatpersonen' in result and 'rund um die Uhr.' in result and 'Was sind Cookies?' not in result # and 'Mensch im Mittelpunkt.' in result

    result = load_mock_page('http://www.jovelstefan.de/2011/09/11/gefallt-mir/', txtoutput)
    assert 'Manchmal überrascht einen' in result and 'kein Meisterwerk war!' in result and 'Pingback von' not in result # and 'Kommentare geschlossen' not in result

    result = load_mock_page('https://www.stuttgart.de/item/show/132240/1', txtoutput)
    assert 'Das Bohnenviertel entstand' in result and 'sich herrlich entspannen.' in result and 'Nützliche Links' not in result # and 'Mehr zum Thema' not in result

    result = load_mock_page('http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/', txtoutput)
    assert 'zu einem glatten Teig verarbeiten.' in result and 'goldbraun sind.' in result and 'Sei der Erste' not in result and 'Gefällt mir' not in result and 'Trotz sorgfältiger inhaltlicher Kontrolle' not in result
    #assert and '200 g Zucker' in result and 'Ein Backblech mit Backpapier auslegen.' in result

    result = load_mock_page('http://schleifen.ucoz.de/blog/briefe/2010-10-26-18', txtoutput)
    assert 'Es war gesagt,' in result and 'Symbol auf dem Finger haben' in result and 'Aufrufe:' not in result

    result = load_mock_page('https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg', txtoutput)
    assert 'Salzburg liebt seine Radfahrer.' in result and 'Puls einsaugen zu lassen.' in result and 'Das könnte Sie auch interessieren ...' not in result and 'So macht Radfahren sonst noch Spaß' not in result # and 'Radfahren in der Fußgängerzone der Innenstadt ist erlaubt' in result

    result = load_mock_page('https://www.heise.de/newsticker/meldung/Zahlen-bitte-100-scheinbare-Kanaele-die-den-Hype-um-Marsmenschen-ausloesten-4438438.html', txtoutput)
    assert 'Nicht selten sorgen' in result and '(mawi)' in result and 'Mehr zum Thema' not in result and 'Lesezeit' not in result

    result = load_mock_page('https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/', txtoutput)
    assert 'Allerdings sieht es wie ein Dildo aus,' in result and 'gibt Bescheid, ne?' in result and 'Ähnliche Beiträge' not in result and 'Deine E-Mail (bleibt natürlich unter uns)' not in result

    result = load_mock_page('https://www.otto.de/twoforfashion/strohtasche/', txtoutput)
    assert 'Ob rund oder kastenförmig, ob dezent oder auffällig' in result and 'XX, Die Redaktion' in result and ' Kommentieren' not in result and 'Dienstag, 4. Juni 2019' not in result

    result = load_mock_page('http://iloveponysmag.com/2018/05/24/barbour-coastal/', txtoutput)
    assert 'Eine meiner besten Entscheidungen bisher:' in result and 'Verlassenes Gewächshaus meets versteckter Deich' in result and 'Der Hundestrand in Stein an der Ostsee' in result and 'Tags: Barbour,' not in result and 'Bitte (noch) mehr Bilder von Helle' in result and 'Hinterlasse einen Kommentar' not in result

    result = load_mock_page('https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/', txtoutput)
    #print(result)
    assert 'Das ist alles nicht gekennzeichnet, wie soll ich wissen' in result and 'Instagramshops machen es Abmahnanwälten leicht' in result and 'Diese Geschichte teilen' not in result and 'Ähnliche Beiträge ' not in result and 'Ich bin der Ansicht, abwarten und Tee trinken.' in result and 'Danke für dein Feedback. Auch zum Look meiner Seite.' in result and 'Diese Website verwendet Akismet, um Spam zu reduzieren.' not in result

    result = load_mock_page('http://www.womencantalksports.com/top-10-women-talking-sports/', txtoutput)
    assert '3.Charlotte Jones Anderson' in result and 'Keep Talking Sports!' in result and 'Category: Blog Popular' not in result and 'Copyright Women Can Talk Sports.' not in result and 'Submit your sports question below' not in result

    result = load_mock_page('https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html', txtoutput)
    assert 'Schönheit kommt für Pamela von Innen und Außen' in result and 'Die Workout Übungen kannte ich bereits' in result and 'Great post, I like your blog' in result and 'Links zu diesem Post' not in result and 'mehr über mich ♥' not in result
    # 'Vielen Dank an den den Verlag' in result
    # and 'Bitte beachte auch die Datenschutzerklärung von Google.' not in result

    result = load_mock_page('https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html', txtoutput)
    assert 'Grounded in sustainable architecture and refined Vietnamese craftsmanship,' in result and 'and Carmelo Resort' in result and 'OMG what a beautiful place to stay! ' in result and 'Food Advertising by' not in result
   # 'Dining and Drinking' in result
   # 'Reply' not in result and 'A lovely note makes a beautiful day!' not in result

    result = load_mock_page('https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/', txtoutput)
    assert 'Argentina, the birthplace of polo.' in result and 'Simon Wittenberg travels to the Eternal City in Italy' in result and 'Luxury and lifestyle articles' not in result
   # 'Pinterest' not in result

    result = load_mock_page('https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5', txtoutput)
    assert result is None

    result = load_mock_page('https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/', txtoutput)
    assert 'Prof. Dr. Caja Thimm' in result and 'zur Anmeldung.' in result and 'Next post' not in result and 'Aus den Ländern' not in result

    result = load_mock_page('https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/', txtoutput)
    assert 'Leitsätze des Gerichts' in result and 'III. Die Revision der Beklagten' and 'twittern' not in result and 'Ähnliche Beiträge' not in result and 'd.toelle[at]rechtambild.de' not in result

    result = load_mock_page('http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html', txtoutput)
    assert 'Wann Blogs einer Impressumspflicht unterliegen,' in result and 'Mit Verlaub, ich halte das für groben Unsinn.' in result and 'Über mich' not in result and 'Gesetzes- und Rechtsprechungszitate werden automatisch' not in result
    # and 'Comment by' not in result

    result = load_mock_page('https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html', txtoutput)
    assert 'Aufbau und Inhalt' in result and 'Verlag Dr. Otto Schmidt' in result and 'Handbuch' not in result and 'Drucken' not in result and 'Ähnliche Artikel' not in result
    # and 'Anzeige:' not in result and 'Kommentar schreiben' not in result

    result = load_mock_page('https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen', txtoutput)
    assert 'Auch der Verweis auf ehrverletzende Bewertungen' in result and 'Anja Schmoll-Trautmann' not in result and 'Fanden Sie diesen Artikel nützlich?' not in result and 'Aktuell' not in result
    # and 'Zu seinen Tätigkeitsfeldern zählen' not in result and 'Kommentar hinzufügen' not in result

    result = load_mock_page('https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage', txtoutput)
    assert 'Alle Artikel zu unseren Recherchen' not in result and 'Vorweg: Die beteiligten AfD-Politiker' in result and 'ist heute Abend um 21 Uhr auch im ZDF-Magazin Frontal' in result and 'Wir informieren Sie regelmäßig zum Thema Neue Rechte' not in result and 'Kommentar verfassen' not in result and 'weiterlesen' not in result

    result = load_mock_page('https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845', txtoutput)
    assert '05:28 Uhr' not in result and 'Bahn-Konkurrenten wie Flixbus fürchten durch den geplanten Deutschlandtakt' in result and 'ICE im S-Bahn-Takt' not in result and 'Diskussion zu diesem Artikel auf:' not in result and 'Berater-Affäre bringt Bahnchef Lutz in Bedrängnis' not in result
    # and 'auch der Bus ein klimafreundliches Verkehrsmittel sei' in result

    result = load_mock_page('https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/', txtoutput)
    assert 'Rund ums Fahrzeug' not in result and 'in punkto Sicherheit, Bedienung, Ergonomie' in result and 'Grenzwert der Richtlinie 2014/79/EU' in result and 'Diesel-Umtauschprämien' not in result
    # 'Besonders bei Babyschalen sollte geprüft werden' in result # ul/li

    result = load_mock_page('https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/', txtoutput)
    assert 'Was I losing my mind?' in result and 'being cached after their first access.' in result and 'New Call-to-action' not in result and 'You might also like:' not in result and 'Contact us' not in result and 'Back to blog' not in result
    # 'Finding a Fix' in result # h4
    # 'from django.conf import settings' in result # code

    result = load_mock_page('https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/', txtoutput)
    assert 'Vor knapp zwei Wochen' in result and 'gibt es in der dazugehörigen Vorstellungs-News.' in result and 'Themen:' not in result and 'bis Januar 2009 Artikel für ComputerBase verfasst.' not in result and 'Warum Werbebanner?' not in result and '71 Kommentare' not in result

    result = load_mock_page('http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html', txtoutput)
    assert '就放心去吧' in result and 'Repeat Chorus' in result and 'Older post' not in result and 'Thank you for your support!' not in result

    result = load_mock_page('https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/', txtoutput)
    assert 'Frank Thelen, Investor' in result and 'Female founders must constantly consider' in result and 'Thema des öffentlichen Interesses' in result and 'Nach langjähriger Tätigkeit im Ausland' not in result and 'Schaut man ganz genau hin, ist der Habeck-Kommentar' in result and 'Mit Absendung des Formulars willige ich' not in result and 'Kommentieren' not in result
    # and 'Auch interessant' not in result and 'Wir tun jeden Tag, was wir lieben.' not in result

    result = load_mock_page('https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/', txtoutput)
    assert 'Welche Werbeeinnahmen erwarten Sie hier langfristig?' in result and 'wir haben keinerlei Pläne, das zu verändern.' in result and 'Nachrichtenüberblick abonnieren' not in result and 'über alle aktuellen Entwicklungen auf dem Laufenden.' not in result and 'Schlagworte' not in result and 'Teilen' not in result and 'Dauerzoff um drohenden UKW-Blackout' not in result and 'Mobilcom Debitel has charged me for third party' in result

    result = load_mock_page('https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/', txtoutput)
    assert 'Zeit für Loslassen und Entspannung.' in result and 'Erfrischende, abschwellende Augencreme Phyto Contour' in result and 'Wie sieht dein Alltag aus?' in result and 'Vielen Dank Anja für deine Tipps rund um Beauty' in result and 'Betreiberin von incurvy Plus Size' not in result and 'Wellness Gesichtsbehandlung: Plaisir D’Aromes' not in result
    # and 'Das Thema könnte dich auch interessieren:' not in result


    # print(html_extractor.lrutest)


if __name__ == '__main__':
    test_trim()
    test_main(txtoutput=False)
    test_main(txtoutput=True)
    test_download()
