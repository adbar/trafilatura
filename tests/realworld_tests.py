# pylint:disable-msg=W1401
"""
Unit tests for the trafilatura library.
Not included in releases due to cached pages.
"""

import functools
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
SAMPLE_META = dict.fromkeys(["title", "author", "url", "description", "sitename", "date", "categories", "tags", "id"])


MOCK_PAGES = {
    "https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/": "die-partei.net.luebeck.html",
    "https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html": "bmjv.de.konsum.html",
    "https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/": "denkanstoos.com.2012.html",
    "https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft": "demokratiewebstatt.at.luft.html",
    "http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html": "toralin.de.schmierfett.html",
    "https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess": "ebrosia.de.zinfandel.html",
    "https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html": "landwirt.com.sensortechnik.html",
    "http://schleifen.ucoz.de/blog/briefe/2010-10-26-18": "schleifen.ucoz.de.briefe.html",
    "http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung": "rs-ingenieure.de.tragwerksplanung.html",
    "http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html": "simplyscience.ch.erdoel.html",
    "http://www.shingon-reiki.de/reiki-und-schamanismus/": "shingon-reiki.de.schamanismus.html",
    "http://love-hina.ch/news/0409.html": "love-hina.ch.0409.html",
    "http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html": "cdu-fraktion-erfurt.de.waldorfschule.html",
    "http://www.wehranlage-horka.de/veranstaltung/887/": "wehranlage-horka.de.887.html",
    "https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/": "piratenpartei-mv.de.grundeinkommen.html",
    "https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html": "rnz.de.witzel.html",
    "https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg": "austria.info.radfahren.html",
    "https://www.fairkom.eu/about": "fairkom.eu.about.html",
    "https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461": "futurezone.at.lyft.html",
    "http://www.hundeverein-kreisunna.de/unserverein.html": "hundeverein-kreisunna.de.html",
    "https://viehbacher.com/de/steuerrecht": "viehbacher.com.steuerrecht.html",
    "http://www.jovelstefan.de/2011/09/11/gefallt-mir/": "jovelstefan.de.gefallt.html",
    "https://www.stuttgart.de/item/show/132240/1": "stuttgart.de.html",
    "https://www.otto.de/twoforfashion/strohtasche/": "otto.de.twoforfashion.html",
    "http://www.womencantalksports.com/top-10-women-talking-sports/": "womencantalksports.com.top10.html",
    "https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html": "luxuryhaven.co.hyatt.html",
    "https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/": "luxuriousmagazine.com.polo.html",
    "https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5": "chip.de.tests.html",
    "https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/": "gruen-digital.de.jahrestagung.html",
    "https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/": "rechtambild.de.kochbuch.html",
    "http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html": "internet-law.de.pseudonymen.html",
    "https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage": "correctiv.org.zusage.html",
    "https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845": "sueddeutsche.de.flixtrain.html",
    "https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/": "adac.de.kindersitze.html",
    "https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/": "caktusgroup.com.django.html",
    "https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/": "basicthinking.de.tweets.html",
    "https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/": "incurvy.de.wellness.html",
    "https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843": "dw.com.uncork.html",
    "https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html": "jolie.de.adele.html",
    "https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx": "speicherguide.de.schwierige.html",
    "https://novalanalove.com/ear-candy/": "novalanalove.com.ear-candy.html",
    "http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/": "franziska-elea.de.vuitton.html",
    "https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html": "brigitte.de.ikigai.html",
    "https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/": "changelog.blog.zwischenbilanz.html",
    "https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/": "threatpost.com.android.html",
    "https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact": "theverge.com.ios13.html",
    "https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding": "en.wikipedia.org.tsne.html",
    "https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/": "mixed.de.vrodo.html",
    "https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/": "majkaswelt.com.fashion.html",
    "https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/": "erp-news.info.interview.html",
    "https://lady50plus.de/2019/06/19/sekre-mystery-bag/": "lady50plus.de.sekre.html",
    "https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite": "psl.eu.luniversite.html",
    "http://www.sauvonsluniversite.fr/spip.php?article8532": "sauvonsluniversite.com.spip.html",
    "https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020": "franceculture.fr.idees.html",
    "https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2": "vancouversun.com.microsoft.html",
    "https://www.lanouvellerepublique.fr/indre-et-loire/commune/saint-martin-le-beau/family-park-la-derniere-saison-a-saint-martin-le-beau": "lanouvellerepublique.fr.martin.html",
    "http://blog.python.org/2016/12/python-360-is-now-available.html": "blog.python.org.html",
    "https://creativecommons.org/about/": "creativecommons.org.html",
    "https://www.creativecommons.at/faircoin-hackathon": "creativecommons.at.faircoin.html",
    "https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/": "blog.wordpress.com.diverse.html",
    "https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/": "netzpolitik.org.abmahnungen.html",
    "https://www.befifty.de/home/2017/7/12/unter-uns-montauk": "befifty.montauk.html",
    "https://www.soundofscience.fr/1927": "soundofscience.fr.1927.html",
    "https://laviedesidees.fr/L-evaluation-et-les-listes-de.html": "laviedesidees.fr.evaluation.html",
    "https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens": "theguardian.com.academics.html",
    "https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html": "phys.org.tool.html",
    "https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/": "gregoryszorc.com.python3.html",
    "https://www.pluralsight.com/tech-blog/managing-python-environments/": "pluralsight.com.python.html",
    "https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/": "stackoverflow.com.rust.html",
    "https://www.dw.com/en/berlin-confronts-germanys-colonial-past-with-new-initiative/a-52060881": "dw.com.colonial.html",
    "https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/": "theplanetarypress.com.forestlands.html",
    "https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/": "wikimediafoundation.org.turkey.html",
    "https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH": "reuters.com.parasite.html",
    "https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being": "nationalgeographic.co.uk.goats.html",
    "https://www.nature.com/articles/d41586-019-02790-3": "nature.com.telescope.html",
    "https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/": "salon.com.emissions.html",
    "https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html": "gofeminin.de.abnehmen.html",
    "https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/": "crazy-julia.de.tipps.html",
    "https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis": "brandenburg.de.homo-brandenburgensis.html",
    "https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html": "skateboardmsm.de.dormhagen.html",
    "https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/": "knowtechie.com.rally.html",
    "https://boingboing.net/2013/07/19/hating-millennials-the-preju.html": "boingboing.net.millenials.html",
    "http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/": "spreeblick.com.habeck.html",
    "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/": "github.blog.spiceland.html",
    "https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer": "sonntag-sachsen.de.emanuel.html",
    "https://www.spiegel.de/spiegel/print/d-161500790.html": "spiegel.de.albtraum.html",
    "https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/": "lemire.me.json.html",
    "https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission": "zeit.de.zugverkehr.html",
    "https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/": "computerbase.de.htc.html",
    "http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html": "chineselyrics4u.com.zhineng.html",
    "https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/": "meedia.de.freenet.html",
    "https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html": "telemedicus.info.rezension.html",
    "https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen": "cnet.de.schutz.html",
    "https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space": "vice.com.amazon.html",
    "https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html": "heise.de.lithium.html",
    "https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html": "chip.de.beef.html",
    "https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html": "plentylife.blogspot.pamela-reif.html",
    "https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/": "modepilot.de.duschkopf.html",
    "http://iloveponysmag.com/2018/05/24/barbour-coastal/": "iloveponysmag.com.barbour.html",
    "https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/": "moritz-meyer.net.vreni.html",
    "https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/": "spektrum.de.engelbart.html",
    "https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/": "buchperlen.wordpress.com.html",
    "http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/": "kulinariaathome.com.mandelplätzchen.html",
    "https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/": "de.creativecommons.org.endlich.html",
    "https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be": "scmp.com.playbook.html",
    "https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html": "faz.net.streaming.html",
    "https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html": "ndr.de.podcastcoronavirus140.html",
    "https://www.mercurynews.com/2023/01/16/letters-1119/": "mercurynews.com.2023.01.16.letters-1119.html",
    "http://www.pcgamer.com/2012/08/09/skyrim-part-1/": "pcgamer.com.skyrim.html",
}
# '': '', \


def load_mock_page(url, xml_flag=False, langcheck=None, tei_output=False, formatting=False, links=False):
    """load mock page from samples"""
    try:
        with open(os.path.join(TEST_DIR, "cache", MOCK_PAGES[url]), encoding="utf-8") as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, "cache", MOCK_PAGES[url]), "rb") as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)["encoding"]
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print("Encoding error")
    output_format = "txt"
    if xml_flag is True:
        output_format = "xml"
    if tei_output is True:
        output_format = "tei"
    return extract(
        htmlstring,
        url,
        record_id="0000",
        no_fallback=False,
        output_format=output_format,
        target_language=langcheck,
        include_formatting=formatting,
        include_links=links,
    )


def load_mock_page_meta(url):
    """Load mock page from samples"""
    try:
        with open(os.path.join(TEST_DIR, "cache", MOCK_PAGES[url]), encoding="utf-8") as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, "cache", MOCK_PAGES[url]), "rb") as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)["encoding"]
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print("Encoding error")
    return htmlstring


@pytest.mark.parametrize("xmloutput,formatting", [(True, False), (False, False), (False, True)])
def test_extract(xmloutput, formatting):
    """test extraction from HTML"""
    do_load_page = functools.partial(load_mock_page, xml_flag=xmloutput, formatting=formatting)

    result = do_load_page("https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/")
    assert "Impressum" not in result
    assert "Die GEMA dreht völlig am Zeiger!" in result

    result = do_load_page(
        "https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html"
    )
    assert "Impressum" not in result
    assert "Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol" in result

    result = do_load_page("https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/")
    assert "Two or three 10-15 min" in result
    assert "What type? Etc. (30 mins)" in result
    assert "Dieser Eintrag wurde veröffentlicht" not in result
    assert "Mit anderen Teillen" not in result

    result = do_load_page("https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess")
    assert "Das Bukett präsentiert sich" in result
    assert "Kunden kauften auch" not in result
    assert "Gutschein sichern" not in result
    assert "Besonders gut passt er zu asiatischen Gerichten" in result

    result = do_load_page("https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html")
    assert "Überwachung der somatischen Zellen" in result
    assert "tragbaren Ultraschall-Geräten" in result
    assert "Kotkonsistenz" in result
    assert "Anzeigentarife" not in result
    assert "Aktuelle Berichte aus dieser Kategorie" not in result

    result = do_load_page("http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung")
    if xmloutput is False:
        assert "Wir bearbeiten alle Leistungsbilder" in result
        assert "Brückenbau" not in result

    result = do_load_page("http://www.shingon-reiki.de/reiki-und-schamanismus/")
    assert "Catch Evolution" not in result
    assert "und gekennzeichnet mit" not in result
    assert "Heut geht es" in result
    assert "Ich komme dann zu dir vor Ort." in result

    result = do_load_page("http://love-hina.ch/news/0409.html")
    assert "Kapitel 121 ist" in result
    assert "Besucher online" not in result
    assert "Kommentare schreiben" not in result

    result = do_load_page(
        "http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html"
    )
    assert "der steigenden Nachfrage gerecht zu werden." in result
    assert "Zurück zur Übersicht" not in result
    assert "Erhöhung für Zoo-Eintritt" not in result

    result = do_load_page(
        "https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/"
    )
    assert "das letzte Wort sein kann." in result
    assert "Ähnliche Beiträge" not in result

    result = do_load_page("https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/")
    assert "Unter diesem Motto findet am 14. September" in result
    assert "Volksinitiative Schweiz zum Grundeinkommen." in result
    assert "getaggt mit:" not in result
    assert "Was denkst du?" not in result

    result = do_load_page("https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/")
    assert "Zweitens wird der Genderstern" in result
    assert "alldem leider – nichts." in result

    result = do_load_page("http://www.wehranlage-horka.de/veranstaltung/887/")
    assert "In eine andere Zeit" in result
    assert "Während Sie über den Markt schlendern" in result
    assert "Infos zum Verein" not in result
    assert "nach oben" not in result
    assert "Datenschutzerklärung" not in result

    # modified by taking only 1st article element...
    result = do_load_page("https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft")
    # print(result)
    assert "Millionen Menschen fahren jeden Tag" in result
    assert "Clipdealer" not in result
    assert "Teste dein Wissen" not in result
    assert "Thema: Fußball" not in result

    result = do_load_page("http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html")
    assert "Erdöl bildet nach Millionen" in result
    assert "Warum wird das Erdöl knapp?" in result
    assert "Die Natur ist aus chemischen Elementen aufgebaut" not in result

    result = do_load_page(
        "https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html"
    )
    assert "Für einen Roman" in result
    assert "Auszeichnung der Branche." in result

    result = do_load_page(
        "https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/"
    )
    if xmloutput is False:
        assert "Dann sollten Sie erst recht" in result
        assert "als saure Gürkchen entlarvte Ex-Boyfriends." in result
        assert "Ähnliche Beiträge" not in result

    result = do_load_page("http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html")
    assert "künftig das XADO-Schutzfett verwenden." in result
    assert "bis zu 50% Verschleiß." in result
    assert "Die Lebensdauer von Bauteilen erhöht sich beträchtlich." in result
    assert "Newsletter" not in result
    assert "Sie könnten auch an folgenden Artikeln interessiert sein" not in result

    result = do_load_page("https://www.fairkom.eu/about")
    assert "ein gemeinwohlorientiertes Partnerschaftsnetzwerk" in result
    assert "Stimmberechtigung bei der Generalversammlung." in result
    assert "support@fairkom.eu" not in result

    result = do_load_page(
        "https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461"
    )
    assert "Einige Kunden des Fahrdienst-Vermittler Lyft" in result
    assert "zeitweise rund vier Prozent." in result
    assert "Allgemeine Nutzungsbedingungen" not in result
    assert "Waymo bittet Autohersteller um Geld" not in result

    result = do_load_page("http://www.hundeverein-kreisunna.de/unserverein.html")
    assert "Beate und Norbert Olschewski" in result
    assert "ein Familienmitglied und unser Freund." in result
    assert "zurück zur Startseite" not in result

    result = do_load_page("https://viehbacher.com/de/steuerrecht")
    assert "und wirtschaftlich orientierte Privatpersonen" in result
    assert "rund um die Uhr." in result
    assert "Mensch im Mittelpunkt." in result
    assert "Was sind Cookies?" not in result

    result = do_load_page("http://www.jovelstefan.de/2011/09/11/gefallt-mir/")
    assert "Manchmal überrascht einen" in result
    assert "kein Meisterwerk war!" in result
    assert "Pingback von" not in result
    assert "Kommentare geschlossen" not in result

    result = do_load_page("https://www.stuttgart.de/item/show/132240/1")
    assert "Das Bohnenviertel entstand" in result
    assert "sich herrlich entspannen." in result
    assert "Nützliche Links" not in result
    assert "Mehr zum Thema" not in result

    result = do_load_page("http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/")
    assert "zu einem glatten Teig verarbeiten." in result
    assert "goldbraun sind." in result
    assert "200 g Zucker" in result
    assert "Ein Backblech mit Backpapier auslegen." in result
    assert "Sei der Erste" not in result
    assert "Gefällt mir" not in result
    assert "Trotz sorgfältiger inhaltlicher Kontrolle" not in result

    # justext performs better here
    result = do_load_page("http://schleifen.ucoz.de/blog/briefe/2010-10-26-18")
    assert "Es war gesagt," in result
    assert "Symbol auf dem Finger haben" in result
    assert "Aufrufe:" not in result

    result = do_load_page("https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg")
    assert "Salzburg liebt seine Radfahrer." in result
    assert "Puls einsaugen zu lassen." in result
    assert "Das könnte Sie auch interessieren ..." not in result
    assert "So macht Radfahren sonst noch Spaß" not in result

    result = do_load_page("https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/")
    assert "Allerdings sieht es wie ein Dildo aus," in result
    assert "gibt Bescheid, ne?" in result
    assert "Ähnliche Beiträge" not in result
    assert "Deine E-Mail (bleibt natürlich unter uns)" not in result

    result = do_load_page("https://www.otto.de/twoforfashion/strohtasche/")
    assert "Ob rund oder kastenförmig, ob dezent oder auffällig" in result
    assert "XX, Die Redaktion" in result
    assert " Kommentieren" not in result
    assert "Dienstag, 4. Juni 2019" not in result

    result = do_load_page("http://iloveponysmag.com/2018/05/24/barbour-coastal/")
    assert "Eine meiner besten Entscheidungen bisher:" in result
    assert "Verlassenes Gewächshaus meets versteckter Deich" in result
    assert "Der Hundestrand in Stein an der Ostsee" in result
    assert "Tags: Barbour," not in result
    assert "Bitte (noch) mehr Bilder von Helle" in result
    assert "Hinterlasse einen Kommentar" not in result

    result = do_load_page("https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/")
    assert "Das ist alles nicht gekennzeichnet, wie soll ich wissen" in result
    assert "Instagramshops machen es Abmahnanwälten leicht" in result
    assert "Diese Geschichte teilen" not in result
    assert "Ähnliche Beiträge " not in result
    assert "Ich bin der Ansicht, abwarten und Tee trinken." in result
    assert "Danke für dein Feedback. Auch zum Look meiner Seite." in result
    assert "Diese Website verwendet Akismet, um Spam zu reduzieren." not in result

    result = do_load_page("http://www.womencantalksports.com/top-10-women-talking-sports/")
    assert "Keep Talking Sports!" in result
    assert "Category: Blog Popular" not in result
    assert "Copyright Women Can Talk Sports." not in result
    assert "Submit your sports question below" not in result
    assert "3.Charlotte Jones Anderson" in result

    result = do_load_page("https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html")
    assert "Schönheit kommt für Pamela von Innen und Außen" in result
    assert "Die Workout Übungen kannte ich bereits" in result
    assert "Great post, I like your blog" in result
    assert "Links zu diesem Post" not in result
    assert "mehr über mich ♥" not in result
    assert "Bitte beachte auch die Datenschutzerklärung von Google." not in result

    result = do_load_page(
        "https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html"
    )
    assert "Grounded in sustainable architecture and refined Vietnamese craftsmanship," in result
    assert "and Carmelo Resort" in result
    assert "OMG what a beautiful place to stay! " in result
    assert "Food Advertising by" not in result
    assert "Dining and Drinking" in result
    assert "A lovely note makes a beautiful day!" not in result

    result = do_load_page("https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/")
    assert "Argentina, the birthplace of polo." in result
    assert "Simon Wittenberg travels to the Eternal City in Italy" in result
    assert "Luxury and lifestyle articles" not in result
    assert "Pinterest" not in result

    result = do_load_page("https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5")
    assert "Werkzeug für Heimwerker und Baumarkt-Artikel" in result
    assert "Newsletter" not in result

    result = do_load_page(
        "https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/"
    )
    assert "Prof. Dr. Caja Thimm" in result
    assert "zur Anmeldung." in result
    assert "Next post" not in result
    assert "Aus den Ländern" not in result

    result = do_load_page("https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/")
    assert "Leitsätze des Gerichts" in result
    assert "III. Die Revision der Beklagten"
    assert "twittern" not in result
    assert "Ähnliche Beiträge" not in result
    assert "d.toelle[at]rechtambild.de" not in result

    result = do_load_page(
        "http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html"
    )
    # print(result)
    assert "Wann Blogs einer Impressumspflicht unterliegen," in result
    assert "Über mich" not in result
    assert "Gesetzes- und Rechtsprechungszitate werden automatisch" not in result
    assert "Mit Verlaub, ich halte das für groben Unsinn." in result
    ## comments!
    # and 'Comment by' not in result

    result = do_load_page("https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html")
    if xmloutput is False:
        assert "Aufbau und Inhalt" in result
        assert "Verlag Dr. Otto Schmidt" in result
        assert "Handbuch" not in result
        assert "Drucken" not in result
        assert "Ähnliche Artikel" not in result
        assert "Anzeige:" not in result

    result = do_load_page(
        "https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen"
    )
    assert "Auch der Verweis auf ehrverletzende Bewertungen" in result
    assert "Fanden Sie diesen Artikel nützlich?" not in result
    assert "Kommentar hinzufügen" not in result
    if xmloutput is False:
        assert "Anja Schmoll-Trautmann" not in result
        assert "Aktuell" not in result

    result = do_load_page("https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage")
    assert "Alle Artikel zu unseren Recherchen" not in result
    assert "Vorweg: Die beteiligten AfD-Politiker" in result
    assert "ist heute Abend um 21 Uhr auch im ZDF-Magazin Frontal" in result
    assert "Wir informieren Sie regelmäßig zum Thema Neue Rechte" not in result
    assert "Kommentar verfassen" not in result
    assert "weiterlesen" not in result

    result = do_load_page(
        "https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845"
    )
    assert "05:28 Uhr" not in result
    assert "Bahn-Konkurrenten wie Flixbus fürchten durch den geplanten Deutschlandtakt" in result
    assert "ICE im S-Bahn-Takt" not in result
    assert "Diskussion zu diesem Artikel auf:" not in result
    assert "Berater-Affäre bringt Bahnchef Lutz in Bedrängnis" not in result
    assert "auch der Bus ein klimafreundliches Verkehrsmittel sei" in result

    result = do_load_page("https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/")
    assert "Rund ums Fahrzeug" not in result
    assert "in punkto Sicherheit, Bedienung, Ergonomie" in result
    assert "Grenzwert der Richtlinie 2014/79/EU" in result
    assert "Diesel-Umtauschprämien" not in result
    assert "Besonders bei Babyschalen sollte geprüft werden" in result

    result = do_load_page("https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/")
    assert "Was I losing my mind?" in result
    assert "being cached after their first access." in result
    assert "Finding a Fix" in result
    assert "from django.conf import settings" in result
    assert "New Call-to-action" not in result
    assert "Contact us" not in result
    assert "Back to blog" not in result
    assert "You might also like:" not in result

    result = do_load_page("https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/")
    assert "Vor knapp zwei Wochen" in result
    assert "gibt es in der dazugehörigen Vorstellungs-News." in result
    assert "Themen:" not in result
    assert "bis Januar 2009 Artikel für ComputerBase verfasst." not in result
    assert "Warum Werbebanner?" not in result
    assert "71 Kommentare" not in result

    result = do_load_page("http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html")
    assert "就放心去吧" in result
    assert "Repeat Chorus" in result
    assert "Older post" not in result
    assert "Thank you for your support!" not in result

    result = do_load_page("https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/")
    assert "Frank Thelen, Investor" in result
    assert "Female founders must constantly consider" in result
    assert "Thema des öffentlichen Interesses" in result
    assert "Nach langjähriger Tätigkeit im Ausland" not in result
    assert "Schaut man ganz genau hin, ist der Habeck-Kommentar" in result
    assert "Mit Absendung des Formulars willige ich" not in result
    assert "Kommentieren" not in result

    result = do_load_page(
        "https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/"
    )
    assert "Welche Werbeeinnahmen erwarten Sie hier langfristig?" in result
    assert "wir haben keinerlei Pläne, das zu verändern." in result
    assert "Nachrichtenüberblick abonnieren" not in result
    assert "über alle aktuellen Entwicklungen auf dem Laufenden." not in result
    assert "Schlagworte" not in result
    assert "Teilen" not in result
    assert "Dauerzoff um drohenden UKW-Blackout" not in result
    assert "Mobilcom Debitel has charged me for third party" in result

    result = do_load_page("https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/")
    assert "Zeit für Loslassen und Entspannung." in result
    assert "Wie sieht dein Alltag aus?" in result
    assert "Erfrischende, abschwellende Augencreme Phyto Contour" in result
    assert "Vielen Dank Anja für deine Tipps rund um Beauty" in result
    assert "Betreiberin von incurvy Plus Size" not in result
    assert "Wir verwenden Cookies" not in result

    result = do_load_page("https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843")
    assert "No grape variety invites as much intrigue" in result
    assert "With just 0.9 hectares" in result
    assert "Related Subjects" not in result
    assert "Audios and videos on the topic" not in result

    result = do_load_page("https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html")
    assert "Adele feierte ausgelassen mit den Spice Girls" in result
    assert "wie sich Adele weiterentwickelt." in result
    assert "Sommerzeit ist Urlaubszeit," not in result
    assert "Lade weitere Inhalte" not in result

    result = do_load_page(
        "https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx"
    )
    assert "Konflikte mag keiner." in result
    assert "Gespräche meistern können." in result
    assert "Weiterführender Link" not in result
    assert "Flexible Wege in die" not in result
    assert "Storage für den Mittelstand" not in result

    result = do_load_page("https://novalanalove.com/ear-candy/")
    assert "Earcuff: Zoeca" in result
    assert "mit längeren Ohrringen (:" in result
    assert "Kreole: Stella Hoops" in result
    assert "Jetzt heißt es schnell sein:" not in result
    assert "Diese Website speichert Cookies" not in result
    assert "VON Sina Giebel" not in result

    result = do_load_page("http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/")
    assert "Zuerst dachte ich, ich könnte das" in result
    assert "x Franzi" in result
    if not formatting:
        assert "Flauschjacke: Bershka" in result
    else:
        assert "Flauschjacke: **Bershka**" in result
    assert "Palm Springs Mini (links)" not in result
    assert "Diese Website verwendet Akismet" not in result
    assert "New York, New York" not in result

    result = do_load_page("https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html")
    assert "Die Psyche spielt eine nicht unerhebliche Rolle" in result
    assert "Sportskanone oder Sportmuffel" not in result
    assert "PINNEN" not in result
    assert "2. Satt essen bei den Mahlzeiten" in result
    assert "Bringt die Kilos zum Purzeln!" not in result
    assert "Crash-Diäten ziehen meist den Jojo-Effekt" not in result

    result = do_load_page("https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html")
    assert "Glücks-Trend Konkurrenz" in result
    assert "Praktiziere Dankbarkeit" in result
    assert "dein Ikigai schon gefunden?" in result
    assert "14,90 Euro." in result
    assert "Neu in Liebe" not in result
    assert "Erfahre mehr" not in result
    assert "Erfahrung mit privater Arbeitsvermittlung?" not in result

    result = do_load_page(
        "https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/"
    )
    assert "Gibt es weitere Top-Maßnahmen für Multi-Channel?" in result
    assert "Vielen Dank für das interessante Interview!" in result
    assert "akzeptiere die Datenschutzbestimmungen" not in result
    assert "Diese Beiträge solltest du nicht verpassen" not in result
    if xmloutput is False:
        assert "Annette Henkel" not in result

    result = do_load_page(
        "https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/"
    )
    assert "These messages include links to the ransomware" in result
    assert "using novel techniques to exfiltrate data." in result
    assert "Share this article:" not in result
    assert "Write a comment" not in result
    assert "Notify me when new comments are added." not in result
    assert "uses Akismet to reduce spam." not in result

    result = do_load_page(
        "https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space"
    )
    assert "Brazil went dark." in result
    assert "the highest number of deforestation warnings.”" in result
    assert "Tagged:" not in result
    assert "to the VICE newsletter." not in result
    assert "Watch this next" not in result

    result = do_load_page("https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html")
    assert "Die Ökobilanz von Elektroautos" in result
    assert "Nur die Folie bleibt zurück" in result
    assert "Forum zum Thema:" not in result

    result = do_load_page("https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact")
    assert "Normally, video calls tend to" in result
    assert "across both the eyes and nose." in result
    assert "Added ARKit explanation and tweet." in result
    assert "Singapore’s public health program" not in result
    assert "Command Line delivers daily updates" not in result

    result = do_load_page("https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/")
    assert "in keinem Braut-Beauty-Programm fehlen darf?" in result
    assert "nicht nur vor der Hochzeit ein absolutes Muss." in result
    assert "Gesundes, glänzendes Haar" in result
    assert "Neue Wandbilder von Posterlounge" not in result
    assert "mit meinen Texten und mit meinen Gedanken." not in result
    assert "Erforderliche Felder sind mit * markiert." not in result

    result = do_load_page("https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis")
    assert "Stilles Rackern, statt lautem Deklamieren." in result
    assert "Watt jibt’s n hier zu lachen?" in result
    assert "Das Brandenbuch. Ein Land in Stichworten." in result
    assert "Bürgerbeteiligung" not in result
    assert "Anmelden" not in result
    assert "Foto: Timur" not in result
    assert "Schlagworte" not in result
    assert "Zeilenumbrüche und Absätze werden automatisch erzeugt." not in result

    result = do_load_page(
        "https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html"
    )
    assert "Wakebeach 257" in result
    assert "Be there or be square!" in result
    assert "Hier geht’s zur Facebook Veranstaltung" in result
    assert "More from News" not in result
    assert "von Redaktion MSM" not in result
    assert "add yours." not in result

    result = do_load_page("https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/")
    assert "Rocket Pass 4 will begin at 10:00 a.m. PDT" in result
    assert "Holy shit, Mortal Kombat 11" in result
    assert "Let us know down below in the comments" in result
    assert "Related Topics" not in result
    assert "You can keep up with me on Twitter" not in result
    assert "Hit the track today with Mario Kart Tour" not in result

    result = do_load_page("https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding")
    assert "Given a set of high-dimensional objects" in result
    assert "Herein a heavy-tailed Student t-distribution" in result
    assert "Categories:" not in result
    assert "Conditional random field" not in result

    result = do_load_page(
        "https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/"
    )
    assert "Niedlicher Roboter-Spielkamerad: Anki Cozmo" in result
    assert "Empfehlungen von Dennis:" in result
    assert "Unterstütze unsere Arbeit" not in result
    assert "Deepfake-Hollywood" not in result
    assert "Avengers" not in result
    assert "Katzenschreck" not in result

    result = do_load_page("http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/")
    assert "Hunderttausende von jungen Paaren" in result
    assert "wie flatterhaft das Mädl ist? :)" in result
    assert "Malte Welding" not in result
    assert "YouTube und die Alten" not in result
    assert "Autokorrektur" not in result

    result = do_load_page("https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/")
    assert "Rüschen und Volants." in result
    assert "ihr jedes Jahr tragen könnt?" in result
    assert "Das könnte dich auch interessieren" not in result
    assert "Catherine Classic Lac 602" not in result

    result = do_load_page("https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/")
    if formatting is False:
        assert "Einblicke in die Vision zukünftiger Softwaregenerationen." in result
    else:
        assert "Einblicke in die **Vision zukünftiger Softwaregenerationen**.\n" in result
    assert "Frage 4: Welche Rolle spielt Big Data in Bezug auf Assistenz-Systeme und KI?" in result
    if formatting is False:
        assert "von The unbelievable Machine Company (*um) zur Verfügung gestellt." in result
    else:
        assert "von **The unbelievable Machine Company (*um)** zur Verfügung gestellt.\n" in result
    assert "Matthias Weber ist ERP-Experte mit langjähriger Berufserfahrung." not in result
    assert "Die Top 5 digitalen Trends für den Mittelstand" not in result
    assert ", leading edge," not in result  # and 'Lesen Sie hier einen weiteren spannenden Beitrag' not in result

    result = do_load_page("https://boingboing.net/2013/07/19/hating-millennials-the-preju.html")
    assert "Click through for the whole thing." in result
    assert "The generation we love to dump on" in result
    assert "GET THE BOING BOING NEWSLETTER" not in result

    result = do_load_page("https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/")
    assert "Erin Spiceland is a Software Engineer for SpaceX." in result
    assert "make effective plans and goals for the future" in result
    assert "looking forward to next?" in result
    assert "Research Consultant at Adelard LLP" in result
    assert "Related posts" not in result
    assert "Jeremy Epling" not in result
    assert "Missed the main event?" not in result
    assert "Privacy" not in result

    result = do_load_page("https://lady50plus.de/2019/06/19/sekre-mystery-bag/")
    assert "ist eine echte Luxushandtasche" in result
    assert "Insgesamt 160 weibliche „Designerinnen“" in result
    assert "Sei herzlich gegrüßt" in result
    assert "Ein Mann alleine hätte niemals" in result
    assert "Erforderliche Felder sind mit" not in result
    assert "Benachrichtige mich" not in result
    assert "Reisen ist meine große Leidenschaft" not in result
    assert "Styling Tipps für Oktober" not in result
    assert "in den Bann ziehen!" in result

    result = do_load_page("https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer")
    assert "Neuer Geschäftsführender Leiter" in result
    assert "nach Leipzig wechseln." in result
    assert "Mehr zum Thema" not in result
    assert "Folgen Sie uns auf Facebook und Twitter" not in result
    assert "Aktuelle Ausgabe" not in result

    result = do_load_page("https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite")
    assert "Le décret n°2019-1130 validant" in result
    assert "restructurant à cet effet »." in result
    assert " utilise des cookies pour" not in result
    assert "En savoir plus" not in result

    result = do_load_page("https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html")
    assert "Starke Hitze nur in der Mitte" in result
    assert "ca. 35,7×29,4 cm" in result
    assert "Wir sind im Steak-Himmel!" in result
    assert "Samsung Galaxy S10 128GB" not in result
    assert "Für Links auf dieser Seite" not in result

    result = do_load_page("http://www.sauvonsluniversite.fr/spip.php?article8532")
    assert "L’AG Éducation Île-de-France inter-degrés" in result
    assert "Grève et mobilisation pour le climat" in result
    assert "suivi.reformes.blanquer@gmail.com" in result
    assert "Sauvons l’Université !" not in result
    assert "La semaine de SLU" not in result

    result = do_load_page("https://www.spiegel.de/spiegel/print/d-161500790.html")
    assert "Wie konnte es dazu kommen?" in result
    assert "Die Geschichte beginnt am 26. Oktober" in result
    assert "Es stützt seine Version." in result
    assert "und Vorteile sichern!" not in result
    assert "Verschickt" not in result
    assert "Die digitale Welt der Nachrichten." not in result
    assert "Vervielfältigung nur mit Genehmigung" not in result

    result = do_load_page("https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/")
    assert "I use a Skylake processor with GNU GCC 8.3." in result
    assert "gsoc-2018" in result
    assert "0.091 GB/s" in result
    assert "version 0.2 on vcpkg." in result
    assert "Leave a Reply" not in result
    assert "Science and Technology links" not in result
    assert "Proudly powered by WordPress" not in result

    result = do_load_page(
        "https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission"
    )
    assert "36 Stunden." in result
    assert "Nationale Egoismen" in result
    assert "Deutschland kaum beschleunigt." in result
    assert "Durchgehende Tickets fehlen" not in result
    assert "geprägte Fehlentscheidung." in result
    assert "horrende Preise für miserablen Service bezahlen?" in result
    assert "Bitte melden Sie sich an, um zu kommentieren." not in result

    result = do_load_page(
        "https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020"
    )
    assert "Performativité" in result
    assert "Les individus productifs communiquent" in result
    assert "de nos espoirs et de nos désirs." in result
    assert "A la tribune je monterai" not in result
    assert "À découvrir" not in result
    assert "Le fil culture" not in result

    result = do_load_page(
        "https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/"
    )
    assert "as further access is restored." in result
    assert "Read further in the pursuit of knowledge" not in result
    assert "Here’s what that means." not in result
    assert "Stay up-to-date on our work." not in result
    assert "Photo credits" not in result

    result = do_load_page(
        "https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH"
    )
    assert "4 Min Read" not in result
    assert "Factbox: Key winners" not in result
    assert "Despite an unknown cast," in result
    assert "Additional reporting by" in result

    result = do_load_page(
        "https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2"
    )
    # print(result)
    assert "Microsoft Corp said on Thursday" in result
    assert "Postmedia is committed" in result
    assert "I consent to receiving" not in result
    assert "It was not immediately clear if" in result
    assert "turns CO2 into soap" not in result
    if xmloutput is False:
        assert "Reuters files" not in result

    # result = do_load_page('https://www.lanouvellerepublique.fr/indre-et-loire/commune/saint-martin-le-beau/family-park-la-derniere-saison-a-saint-martin-le-beau')
    # diff: no real assertion possible — the article is client-side rendered, so
    # static extraction returns only AngularJS template placeholders
    # ('{{nrco.contentDetailController.content.status === "published" ? ...}}')


def test_extract_links_formatting():
    result = load_mock_page("http://www.pcgamer.com/2012/08/09/skyrim-part-1/", formatting=True, links=True)
    assert "In [Skyrim](https://www.pcgamer.com/best-skyrim-mods/), a mage" in result
    # the source has a trailing space inside the em tag; it must stay outside the markers (valid CommonMark)
    assert "*Legends* don't destroy *houses*," in result


def test_pages():
    """Test on real web pages"""
    metadata = extract_metadata(load_mock_page_meta("http://blog.python.org/2016/12/python-360-is-now-available.html"))
    assert metadata.title == "Python 3.6.0 is now available!"
    assert (
        metadata.description
        == "Python 3.6.0 is now available! Python 3.6.0 is the newest major release of the Python language, and it contains many new features and opti..."
    )
    assert metadata.author == "Ned Deily"
    assert metadata.url == "http://blog.python.org/2016/12/python-360-is-now-available.html"
    assert metadata.sitename == "blog.python.org"

    metadata = extract_metadata(
        load_mock_page_meta(
            "https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/"
        )
    )
    assert metadata.title == "Want to See a More Diverse WordPress Contributor Community? So Do We."
    assert (
        metadata.description
        == "More diverse speakers at WordCamps means a more diverse community contributing to WordPress — and that results in better software for everyone."
    )
    assert metadata.sitename == "The WordPress.com Blog"
    assert (
        metadata.url
        == "https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/"
    )

    metadata = extract_metadata(load_mock_page_meta("https://creativecommons.org/about/"))
    assert metadata.title == "What we do - Creative Commons"
    assert (
        metadata.description
        == 'What is Creative Commons? Creative Commons helps you legally share your knowledge and creativity to build a more equitable, accessible, and innovative world. We unlock the full potential of the internet to drive a new era of development, growth and productivity. With a network of staff, board, and affiliates around the world, Creative Commons provides … Read More "What we do"'
    )
    assert metadata.sitename == "Creative Commons"
    assert metadata.url == "https://creativecommons.org/about/"
    # date None

    metadata = extract_metadata(load_mock_page_meta("https://www.creativecommons.at/faircoin-hackathon"))
    assert metadata.title == "FairCoin hackathon beim Sommercamp"
    # assert metadata.url == '/faircoin-hackathon'  # currently None

    metadata = extract_metadata(
        load_mock_page_meta(
            "https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/"
        )
    )
    assert metadata.title == "Die Cider Connection: Abmahnungen gegen Nutzer von Creative-Commons-Bildern"
    assert metadata.author == "Markus Reuter"
    assert (
        metadata.description
        == "Seit Dezember 2015 verschickt eine Cider Connection zahlreiche Abmahnungen wegen fehlerhafter Creative-Commons-Referenzierungen. Wir haben recherchiert und legen jetzt das Netzwerk der Abmahner offen."
    )
    assert metadata.sitename == "netzpolitik.org"
    # cats + tags
    assert (
        metadata.url
        == "https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/"
    )

    metadata = extract_metadata(load_mock_page_meta("https://www.befifty.de/home/2017/7/12/unter-uns-montauk"))
    assert metadata.title == "Das vielleicht schönste Ende der Welt: Montauk"
    assert metadata.author == "Beate Finken"
    assert (
        metadata.description
        == "Ein Strand, ist ein Strand, ist ein Strand Ein Strand, ist ein Strand, ist ein Strand. Von wegen! In Italien ist alles wohl organisiert, Handtuch an Handtuch oder Liegestuhl an Liegestuhl. In der Karibik liegt man unter Palmen im Sand und in Marbella dominieren Beton und eine kerzengerade Promenade"
    )
    assert metadata.sitename == "BeFifty"
    assert metadata.categories == ["Travel", "Amerika"]
    assert metadata.url == "https://www.befifty.de/home/2017/7/12/unter-uns-montauk"

    metadata = extract_metadata(load_mock_page_meta("https://www.soundofscience.fr/1927"))
    assert metadata.title == "Une candidature collective à la présidence du HCERES"
    assert metadata.author == "Martin Clavey"
    assert metadata.description.startswith("En réaction à la candidature du conseiller recherche")
    assert metadata.sitename == "The Sound Of Science"
    assert metadata.categories == ["Politique scientifique française"]
    assert metadata.tags == ["évaluation", "HCERES"]
    assert metadata.url == "https://www.soundofscience.fr/1927"

    metadata = extract_metadata(load_mock_page_meta("https://laviedesidees.fr/L-evaluation-et-les-listes-de.html"))
    assert metadata.title == "L’évaluation et les listes de revues"
    assert metadata.author == "Florence Audier"
    assert metadata.description.startswith("L'évaluation, et la place")
    assert metadata.sitename == "La Vie des idées"
    # assert metadata.categories == ['Essai', 'Économie']  # currently []
    assert metadata.tags == []
    # <meta property="og:type" content="article" />
    # <meta name="DC:type" content="journalArticle">
    assert metadata.url == "http://www.laviedesidees.fr/L-evaluation-et-les-listes-de.html"

    metadata = extract_metadata(
        load_mock_page_meta(
            "https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens"
        )
    )
    assert metadata.title == "Thousands of UK academics 'treated as second-class citizens'"
    assert metadata.author == "Richard Adams"
    assert metadata.description.startswith("Report claims higher education institutions")
    assert metadata.sitename == "The Guardian"  # originally "the Guardian"
    assert metadata.categories == ["Education"]
    assert "Higher education" in metadata.tags[0]
    # meta name="keywords"
    assert (
        metadata.url
        == "http://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens"
    )

    metadata = extract_metadata(load_mock_page_meta("https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html"))
    assert metadata.title == "Flint flake tool partially covered by birch tar adds to evidence of Neanderthal complex thinking"
    assert metadata.author == "Bob Yirka"
    assert (
        metadata.description
        == "A team of researchers affiliated with several institutions in The Netherlands has found evidence in small a cutting tool of Neanderthals using birch tar. In their paper published in Proceedings of the National Academy of Sciences, the group describes the tool and what it revealed about Neanderthal technology."
    )
    assert metadata.sitename == "Phys.org"
    # assert metadata.categories == ['Archaeology', 'Fossils']  # currently []
    assert metadata.tags == [
        "Science, Physics News, Science news, Technology News, Physics, Materials, Nanotech, Technology, Science"
    ]
    assert metadata.url == "https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html"

    metadata = extract_metadata(
        load_mock_page_meta("https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/")
    )
    assert metadata.title == "Mercurial's Journey to and Reflections on Python 3"
    # assert metadata.author == 'Gregory Szorc'  # currently None
    # assert metadata.sitename == 'gregoryszorc'  # currently None
    # assert metadata.categories == ['Mercurial', 'Python']  # currently []

    metadata = extract_metadata(load_mock_page_meta("https://www.pluralsight.com/tech-blog/managing-python-environments/"))
    assert metadata.title == "Managing Python Environments"
    assert metadata.author == "John Walk"
    assert metadata.description.startswith("If you're not careful,")
    assert metadata.sitename == "pluralsight.com"  # 'Pluralsight'
    # assert metadata.categories == ['practices']  # currently []
    # assert metadata.tags == ['python', 'docker', ' getting started']  # currently []
    assert metadata.url == "https://www.pluralsight.com/tech-blog/managing-python-environments/"

    url = "https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "What is Rust and why is it so popular? - Stack Overflow Blog"
    assert metadata.author == "Jake Goulding"
    assert metadata.sitename == "Stack Overflow Blog"
    assert metadata.categories == ["Bulletin"]
    assert metadata.tags == ["programming", "rust"]
    assert metadata.url == url

    url = "https://www.dw.com/en/berlin-confronts-germanys-colonial-past-with-new-initiative/a-52060881"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert "Berlin confronts Germany's colonial past with new initiative" in metadata.title
    assert metadata.author == "Deutsche Welle"  # actually 'Ben Knight'
    assert (
        metadata.description
        == "The German capital has launched a five-year project to mark its part in European colonialism. Streets which still honor leaders who led the Reich's imperial expansion will be renamed — and some locals aren't happy."
    )
    assert metadata.sitename == "DW.COM"  # 'DW - Deutsche Welle'
    assert "Africa" in metadata.tags[0]
    assert metadata.url == url

    metadata = extract_metadata(
        load_mock_page_meta(
            "https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/"
        )
    )
    assert metadata.title.startswith("Management of Intact Forestlands by Indigenous Peoples Key to Protecting Climate")
    assert metadata.author == "The Planetary Press"  # actually 'Julie Mollins'
    assert metadata.sitename == "The Planetary Press"
    assert "Climate" in metadata.categories
    assert (
        metadata.url
        == "https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/"
    )

    url = "https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Access to Wikipedia restored in Turkey after more than two and a half years"
    assert metadata.author == "Wikimedia Foundation"
    assert metadata.description.startswith("Today, on Wikipedia’s 19th birthday")
    assert metadata.sitename == "Wikimedia Foundation"
    # assert metadata.categories == ['Politics', 'Turkey', 'Wikipedia']  # currently []
    assert metadata.url == url

    url = "https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title.endswith("scores historic upset at SAG awards, boosting Oscar chances")  # &#039;Parasite&#039;
    assert metadata.author == "Jill Serjeant"
    assert metadata.date == "2020-01-20"
    # assert metadata.description == '“Parasite,” the Korean language social satire about the wealth gap in South Korea, was the first film in a foreign language to win the top prize of best cast ensemble in the 26 year-history of the SAG awards.'  # currently is the lead paragraph ("South Korean thriller ...frontrunners at the Oscars next month.")
    assert metadata.sitename == "Reuters"
    assert "Media" in metadata.categories[0]  # ['Parasite', 'SAG awards', 'Cinema']
    assert metadata.url == "https://www.reuters.com/article/us-awards-sag-idUSKBN1ZI0EH"

    url = "https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Ravenous wild goats ruled this island for over a century. Now, it's being reborn."
    assert metadata.author == "Michael Hingston"
    assert metadata.description.startswith("The rocky island of Redonda, once stripped of its flora and fauna")
    assert metadata.sitename == "National Geographic"
    assert metadata.categories == ["Environment and Conservation"]  # ['Goats', 'Environment', 'Redonda']
    assert metadata.url == url

    url = "https://www.nature.com/articles/d41586-019-02790-3"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Gigantic Chinese telescope opens to astronomers worldwide"
    assert metadata.author == "Elizabeth Gibney"
    assert (
        metadata.description
        == "FAST has superior sensitivity to detect cosmic phenomena, including fast radio bursts and pulsars."
    )
    assert metadata.sitename == "Nature"
    assert "Exoplanets" in metadata.categories  # ['Astronomy', 'Telescope', 'China']
    assert metadata.url == url

    url = "https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert (
        metadata.title == "Carrie Lam should study Tsai Ing-wen’s playbook"
    )  # '<h1 data-v-1223d442="" class="inner__main-headline main-headline">Taiwanese President Tsai Ing-wen’s political playbook should be essential reading for Hong Kong leader Carrie Lam</h1>'
    # author in JSON-LD
    assert metadata.author == "Alice Wu"
    assert metadata.url == url

    url = "https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Nutzerbasierte Abrechnung: Musik-Stars fordern neues Streaming-Modell"
    # author overridden from JSON-LD + double name
    assert "Benjamin Fischer" in metadata.author
    assert metadata.sitename == "Frankfurter Allgemeine Zeitung"
    assert metadata.url == "https://www.faz.net/1.6604622"

    url = "https://boingboing.net/2013/07/19/hating-millennials-the-preju.html"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Hating Millennials - the prejudice you're allowed to boast about"
    assert metadata.author == "Cory Doctorow"
    assert metadata.sitename == "Boing Boing"
    assert metadata.url == url

    url = "https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Wie kann ich schnell abnehmen? Der Schlachtplan zum Wunschgewicht"
    assert metadata.author == "Diane Buckstegge"
    assert metadata.sitename == "Gofeminin"  # originally "gofeminin"
    assert metadata.url == url

    url = "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Leader spotlight: Erin Spiceland"
    assert metadata.author == "Jessica Rudder"
    assert metadata.description.startswith("We’re spending Women’s History")
    assert metadata.sitename == "The GitHub Blog"
    assert metadata.categories == ["Community"]
    assert metadata.url == url

    url = "https://www.spiegel.de/spiegel/print/d-161500790.html"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Ein Albtraum"
    # assert metadata.author == 'Clemens Höges'  # currently 'SPIEGEL ONLINE; Hamburg; Germany'

    url = "https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/"
    metadata = extract_metadata(load_mock_page_meta(url))
    assert metadata.title == "Despite everything, U.S. emissions dipped in 2019"
    # in JSON-LD
    assert metadata.author == "Nathanael Johnson"
    assert metadata.sitename == "Salon.com"
    # in header
    assert "Science & Health" in metadata.categories
    assert "Gas Industry" in metadata.tags
    assert "coal emissions" in metadata.tags
    assert metadata.url == url

    url = "https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html"
    corrected_url = "https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html"
    metadata = extract_metadata(load_mock_page_meta(url), default_url=url)
    assert metadata.url == corrected_url
    assert "Korinna Hennig" in metadata.author
    assert "Ältere Menschen" in str(metadata.tags)

    url = "https://www.mercurynews.com/2023/01/16/letters-1119/"
    # regression #299: an empty-list JSON-LD "@type" must not crash extract_metadata
    metadata = extract_metadata(load_mock_page(url, xml_flag=True))
    assert metadata is not None
