# -*- coding: utf-8 -*-
"""
Unit tests for the html-extractor library.
"""

import logging
import os
import sys
# https://docs.pytest.org/en/latest/

import html_extractor

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
}
# '': '', \


TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def load_mock_page(url):
    '''load mock page from samples'''
    # TODO: https://chardet.readthedocs.io/en/latest/usage.html
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    except UnicodeDecodeError:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r', encoding='ISO-8859-1') as inputf:
            htmlstring = inputf.read()
    result = html_extractor.process_record(htmlstring, url, '0000', tei_output=False)
    return result

def test_trim():
    '''test string trimming'''
    assert html_extractor.trim('	Test  ') == 'Test'
    assert html_extractor.trim('\t\tTest  Test\r\n') == 'Test Test'

def test_main():
    '''test extraction from HTML'''
    result = load_mock_page('https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/')
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result

    result = load_mock_page('https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html')
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result

    result = load_mock_page('https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/')
    assert result is None

    result = load_mock_page('http://bunterepublik.wordpress.com/2012/04/13/schwafelrunde-ohne-ritter/')
    assert 'Abgelegt unter' not in result and 'Nächster Beitrag' not in result and 'Die Schwafelrunde' in result and 'zusammen.' in result

    result = load_mock_page('https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess')
    assert 'Das Bukett präsentiert sich' in result and 'Besonders gut passt er zu asiatischen Gerichten' in result and 'Kunden kauften auch' not in result and 'Gutschein sichern' not in result

    result = load_mock_page('https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html')
    assert 'Überwachung der somatischen Zellen' in result and 'Kotkonsistenz' in result and 'tragbaren Ultraschall-Geräten' in result and 'Anzeigentarife' not in result and 'Aktuelle Berichte aus dieser Kategorie' not in result

    result = load_mock_page('http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung')
    assert 'Wir bearbeiten alle Leistungsbilder' in result and 'Brückenbau' not in result

    result = load_mock_page('http://www.shingon-reiki.de/reiki-und-schamanismus/')
    assert 'Heut geht es' in result and 'Ich komme dann zu dir vor Ort.' in result and 'Catch Evolution' not in result and 'und gekennzeichnet mit' not in result

    result = load_mock_page('http://love-hina.ch/news/0409.html')
    assert 'Kapitel 121 ist' in result and 'Kommentare schreiben' not in result and 'Besucher online' not in result

    result = load_mock_page('http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html')
    assert 'der steigenden Nachfrage gerecht zu werden.' in result and 'Zurück zur Übersicht' not in result and 'Erhöhung für Zoo-Eintritt' not in result

    result = load_mock_page('https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/')
    assert 'das letzte Wort sein kann.' in result and 'Ähnliche Beiträge' not in result
    #  and 'Michael Blahm' not in result # comments

    result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975')
    assert 'Es ist erstaunlich:' in result and 'Damaris Nübling ist Professorin' in result and 'Der Fall Weinstein' not in result and 'Leser empfehlen' not in result

    result = load_mock_page('https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/')
    assert 'Volksinitiative Schweiz zum Grundeinkommen.' in result and 'getaggt mit:' not in result and 'Was denkst du?' not in result

    result = load_mock_page('https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/')
    assert 'Zweitens wird der Genderstern' in result and 'alldem leider – nichts.' in result
    # and 'Beitragsbild' not in result

    result = load_mock_page('http://www.wehranlage-horka.de/veranstaltung/887/')
    assert 'In eine andere Zeit' in result and 'Infos zum Verein' not in result
    # and 'Groß­vä­ter' in result # segmented words

    result = load_mock_page('https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft')
    assert 'Eines der großen Probleme,' in result and 'versteinerte Dinosaurierknochen.' in result and 'Clipdealer' not in result and 'Teste dein Wissen' not in result and 'Thema: Fußball' not in result

    result = load_mock_page('http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html')
    assert 'Erdöl bildet nach Millionen' in result and 'in unserem Artikel "Warum wird das Erdöl knapp?".' # and 'Die Natur ist aus chemischen Elementen aufgebaut' not in result
    print(result)



    #result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975')
    #print(result)
    #result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975')
    #print(result)
    #result = load_mock_page('https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975')
    #print(result)




    #result = load_mock_page('http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html')
    #print(result)

    #result = load_mock_page('http://schleifen.ucoz.de/blog/briefe/2010-10-26-18')
    #print(result)

    #result = load_mock_page('http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/')
    #print(result)
    #assert 'Gefällt mir' not in result and 'Trotz sorgfältiger inhaltlicher Kontrolle' not in result and '200 g Zucker' in result and 'Ein Backblech mit Backpapier auslegen.' in result



    # print(html_extractor.lrutest)


if __name__ == '__main__':
    test_trim()
    test_main()