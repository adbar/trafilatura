"""
Compare extraction results with other libraries of the same kind.
"""

import logging
import os
import sys
import time


from lxml import etree, html

try:
    import cchardet as chardet
except ImportError:
    import chardet

import justext
from goose3 import Goose
from trafilatura import extract


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


MOCK_PAGES = {
'http://exotic_tags': 'exotic_tags.html',
'https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/': 'piratenpartei-mv.de.grundeinkommen.html',
'https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/': 'spektrum.de.engelbart.html',
'https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975': 'sueddeutsche.de.genderdebatte.html',
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


EVAL_PAGES = {
'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/': {
    'file': 'die-partei.net.luebeck.html',
    'with': ['Die GEMA dreht völlig am Zeiger!'],
    'without': ['Impressum'],
},
'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html': {
    'file': 'bmjv.de.konsum.html',
    'with': ['Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol'],
    'without': ['Impressum'],
},
'http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/': {
    'file': 'kulinariaathome.com.mandelplätzchen.html',
    'with': ['zu einem glatten Teig verarbeiten.', 'goldbraun sind.', '200 g Zucker', 'Ein Backblech mit Backpapier auslegen.'],
    'without': ['Sei der Erste', 'Gefällt mir', 'Trotz sorgfältiger inhaltlicher Kontrolle'],
},
'https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/': {
    'file': 'denkanstoos.com.2012.html',
    'with': ['Two or three 10-15 min', 'What type? Etc. (30 mins)'],
    'without': ['Dieser Eintrag wurde veröffentlicht', 'Mit anderen Teillen'],
},
'https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft': {
    'file': 'demokratiewebstatt.at.luft.html',
    'with': ['Eines der großen Probleme,', 'Millionen Menschen fahren jeden Tag', 'versteinerte Dinosaurierknochen.'],
    'without': ['Clipdealer', 'Teste dein Wissen', 'Thema: Fußball'],
},
'http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html': {
    'file': 'toralin.de.schmierfett.html',
    'with': ['künftig das XADO-Schutzfett verwenden.', 'bis zu 50% Verschleiß.', 'Die Lebensdauer von Bauteilen erhöht sich beträchtlich.'],
    'without': ['Newsletter', 'Sie könnten auch an folgenden Artikeln interessiert sein'],
},
'https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess': {
    'file': 'ebrosia.de.zinfandel.html',
    'with': ['Das Bukett präsentiert sich', 'Besonders gut passt er zu asiatischen Gerichten'],
    'without': ['Kunden kauften auch', 'Gutschein sichern'],
},
'https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html': {
    'file': 'landwirt.com.sensortechnik.html',
    'with': ['Überwachung der somatischen Zellen', 'tragbaren Ultraschall-Geräten', 'Kotkonsistenz'],
    'without': ['Anzeigentarife', 'Aktuelle Berichte aus dieser Kategorie'],
},
'http://schleifen.ucoz.de/blog/briefe/2010-10-26-18': {
    'file': 'schleifen.ucoz.de.briefe.html',
    'with': ['Es war gesagt,', 'Symbol auf dem Finger haben'],
    'without': ['Aufrufe:'],
},
'http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung': {
    'file': 'rs-ingenieure.de.tragwerksplanung.html',
    'with': ['Wir bearbeiten alle Leistungsbilder'],
    'without': ['Brückenbau'],
},
'http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html': {
    'file': 'simplyscience.ch.erdoel.html',
    'with': ['Erdöl bildet nach Millionen', 'in unserem Artikel "Warum wird das Erdöl knapp?".'],
    'without': ['Die Natur ist aus chemischen Elementen aufgebaut'],
},
'http://www.shingon-reiki.de/reiki-und-schamanismus/': {
    'file': 'shingon-reiki.de.schamanismus.html',
    'with': ['Heut geht es', 'Ich komme dann zu dir vor Ort.'],
    'without': ['Catch Evolution', 'und gekennzeichnet mit'],
},
'http://love-hina.ch/news/0409.html': {
    'file': 'love-hina.ch.0409.html',
    'with': ['Kapitel 121 ist'],
    'without': ['Besucher online', 'Kommentare schreiben'],
},
'http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html': {
    'file': 'cdu-fraktion-erfurt.de.waldorfschule.html',
    'with': ['der steigenden Nachfrage gerecht zu werden.'],
    'without': ['Zurück zur Übersicht', 'Erhöhung für Zoo-Eintritt'],
},
'http://www.wehranlage-horka.de/veranstaltung/887/': {
    'file': 'wehranlage-horka.de.887.html',
    'with': ['In eine andere Zeit', 'Während Sie über den Markt schlendern'],
    'without': ['Infos zum Verein', 'nach oben', 'Datenschutzerklärung'],
},
'https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/': {
    'file': 'de.creativecommons.org.endlich.html',
    'with': ['das letzte Wort sein kann.'],
    'without': ['Ähnliche Beiträge', 'Michael Blahm'],
},
}
#'http://exotic_tags': 'exotic_tags.html',


def load_document(filename):
    '''load mock page from samples'''
    try:
        with open(os.path.join(TEST_DIR, 'cache', filename), 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, 'cache', filename), 'rb') as inputf:
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


def run_trafilatura(htmlstring):
    '''run trafilatura (without fallback) on content'''
    result = extract(htmlstring, no_fallback=True)
    return result


def run_justext(htmlstring):
    '''try with the generic algorithm justext'''
    valid = list()
    paragraphs = justext.justext(htmlstring, justext.get_stoplist("German"))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            valid.append(paragraph.text)
    result = ' '.join(valid)
    return result


def run_goose(htmlstring):
    '''try with the goose justext'''
    g = Goose()
    article = g.extract(raw_html=htmlstring)
    return article.cleaned_text


def evaluate_result(result, EVAL_PAGES, item):
    '''evaluate result contents'''
    true_positives = false_negatives = false_positives = true_negatives = 0
    for to_include in EVAL_PAGES[item]['with']:
        if result is not None:
            if to_include in result:
                true_positives += 1
            else:
                false_negatives += 1
        else:
            false_negatives += 1
    for to_exclude in EVAL_PAGES[item]['without']:
        if result is not None:
            if to_exclude in result:
                false_positives += 1
            else:
                true_negatives += 1
        else:
            true_negatives += 1
    return true_positives, false_negatives, false_positives, true_negatives


def calculate_f_score(mydict):
    '''output weighted result score'''
    tp, fn, fp, tn = mydict['true positives'], mydict['false negatives'], mydict['false positives'], mydict['true negatives']
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    fscore = (2*tp)/(2*tp + fp + fn)  # 2*((precision*recall)/(precision+recall))
    return precision, recall, fscore

    
everything = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
nothing = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
trafilatura_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
justext_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
goose_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}


for item in EVAL_PAGES:
    htmlstring = load_document(EVAL_PAGES[item]['file'])
    # null hypotheses
    tp, fn, fp, tn = evaluate_result('', EVAL_PAGES, item)
    nothing['true positives'] += tp
    nothing['false positives'] += fp
    nothing['true negatives'] += tn
    nothing['false negatives'] += fn
    tp, fn, fp, tn = evaluate_result(htmlstring, EVAL_PAGES, item)
    everything['true positives'] += tp
    everything['false positives'] += fp
    everything['true negatives'] += tn
    everything['false negatives'] += fn
    # trafilatura
    start = time.time()
    result = run_trafilatura(htmlstring)
    trafilatura_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    trafilatura_result['true positives'] += tp
    trafilatura_result['false positives'] += fp
    trafilatura_result['true negatives'] += tn
    trafilatura_result['false negatives'] += fn
    # justext
    start = time.time()
    result = run_justext(htmlstring)
    justext_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    justext_result['true positives'] += tp
    justext_result['false positives'] += fp
    justext_result['true negatives'] += tn
    justext_result['false negatives'] += fn
    # goose
    start = time.time()
    result = run_goose(htmlstring)
    goose_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    goose_result['true positives'] += tp
    goose_result['false positives'] += fp
    goose_result['true negatives'] += tn
    goose_result['false negatives'] += fn

print(nothing)
# print(calculate_f_score(nothing))
print(everything)
print(calculate_f_score(everything))
print(trafilatura_result)
print(calculate_f_score(trafilatura_result))
print(justext_result)
print(calculate_f_score(justext_result))
print(goose_result)
print(calculate_f_score(goose_result))
