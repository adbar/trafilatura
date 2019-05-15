# -*- coding: utf-8 -*-
"""
Unit tests for the html-extractor library.
"""

import logging
import os
import sys
# https://docs.pytest.org/en/latest/

import html_extractor
from html_extractor import cli

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
}
# '': '', \

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def load_mock_page(url, txtoutput=False, langcheck=False):
    '''load mock page from samples'''
    # TODO: https://chardet.readthedocs.io/en/latest/usage.html
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    except UnicodeDecodeError:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r', encoding='ISO-8859-1') as inputf:
            htmlstring = inputf.read()
    result = html_extractor.process_record(htmlstring, url, '0000', tei_output=False, txt_output=txtoutput, language_check=langcheck)
    return result


def test_trim():
    '''test string trimming'''
    assert html_extractor.trim('	Test  ') == 'Test'
    assert html_extractor.trim('\t\tTest  Test\r\n') == 'Test Test'


def test_download():
    '''test page download'''
    assert cli.fetch_url('https://httpbin.org/status/404') is None
    teststring = cli.fetch_url('https://httpbin.org/status/200')
    assert teststring is not None
    assert cli.examine(teststring, False, True) is None
    teststring = cli.fetch_url('https://httpbin.org/links/2/2')
    assert teststring is not None
    assert cli.examine(teststring, False, True) is None
    teststring = cli.fetch_url('https://httpbin.org/html')
    assert teststring is not None
    assert cli.examine(teststring, False, True) is not None


def test_main(txtoutput):
    '''test extraction from HTML'''
    result = load_mock_page('https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/', txtoutput)
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result

    result = load_mock_page('https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html', txtoutput)
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result

    result = load_mock_page('https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/', txtoutput)
    assert '10-15 min lightning talks' in result and 'What type? Etc. (30 mins)' in result and 'Dieser Eintrag wurde veröffentlicht' not in result # and 'Mit anderen Teillen' not in result

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

    result = load_mock_page('http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html', txtoutput)
    assert 'der steigenden Nachfrage gerecht zu werden.' in result and 'Zurück zur Übersicht' not in result and 'Erhöhung für Zoo-Eintritt' not in result

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
        result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975', langcheck=True)
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

    # print(html_extractor.lrutest)


if __name__ == '__main__':
    test_trim()
    test_main(txtoutput=False)
    test_main(txtoutput=True)
    test_download()
