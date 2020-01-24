"""
Compare extraction results with other libraries of the same kind.
"""

# import logging
import os
import sys
import time

from lxml import etree, html

try:
    import cchardet as chardet
except ImportError:
    import chardet

import html2text
import justext
from goose3 import Goose
from inscriptis import get_text
from newspaper import fulltext
from readability import Document
from trafilatura import extract


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


EVAL_PAGES = {
'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/': {
    'file': 'die-partei.net.luebeck.html',
    'with': ['Die GEMA dreht völlig am Zeiger!', 'http://www.openpetition.de'],
    'without': ['31. Mai', 'Impressum', 'Steuerdarling'],
},
'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html': {
    'file': 'bmjv.de.konsum.html',
    'with': ['Auch hier gilt der Grundsatz,', 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol', '(Billigkeitskontrolle nach § 315 BGB)'],
    'without': ['Impressum', 'Weitere Informationen', 'Transparenz bei Preisanpassungen', 'Twitter'],
},
'http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/': {
    'file': 'kulinariaathome.com.mandelplätzchen.html',
    'with': ['(+ 15 Minuten backen)', '200 g Zucker', 'zu einem glatten Teig verarbeiten.', 'Ein Backblech mit Backpapier auslegen.'],
    'without': ['Sharen mit', 'Creative Commons', 'Trotz sorgfältiger inhaltlicher Kontrolle'],
},
'https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/': {
    'file': 'denkanstoos.com.2012.html',
    'with': ['Moderator: Hass Chapman', 'Two or three 10-15 min', 'What type? Etc. (30 mins)'],
    'without': ['Dieser Eintrag wurde veröffentlicht', 'Mit anderen Teillen', 'In "DenkanStoos-Treffen"'],
},
'https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft': {
    'file': 'demokratiewebstatt.at.luft.html',
    'with': ['Eines der großen Probleme,', 'Millionen Menschen fahren jeden Tag', 'versteinerte Dinosaurierknochen.'],
    'without': ['Clipdealer', 'Teste dein Wissen', 'Thema: Fußball'],
},
'http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html': {
    'file': 'toralin.de.schmierfett.html',
    'with': ['Die Lebensdauer von Bauteilen erhöht sich beträchtlich.', 'bis zu 50% Verschleiß.', 'Li-Seifen/Mineralöl'],
    'without': ['Newsletter', 'Wie bewerten Sie diesen Artikel?', 'Meander 151', 'Sie könnten auch an folgenden Artikeln interessiert sein'],
},
'https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess': {
    'file': 'ebrosia.de.zinfandel.html',
    'with': ['Das Bukett präsentiert sich', 'Besonders gut passt er zu asiatischen Gerichten', 'Details zum Artikel', 'Dekantieren nicht notwendig'],
    'without': ['Kunden kauften auch', 'Gutschein sichern', 'wurde erfolgreich hinzugefügt.', 'Bitte geben Sie die Zahlenfolge'],
},
'https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html': {
    'file': 'landwirt.com.sensortechnik.html',
    'with': ['b) Überwachung der somatischen Zellen', 'Wiederkauverhalten und Kotkonsistenz.', 'Köllitsch (D)'],
    'without': ['Anzeigentarife', 'weiterempfehlen', 'New Holland T6050', 'Aktuelle Berichte aus dieser Kategorie'],
},
'http://schleifen.ucoz.de/blog/briefe/2010-10-26-18': {
    'file': 'schleifen.ucoz.de.briefe.html',
    'with': ['Es war gesagt,', 'Jedes Mädchen träumt von Justin', 'Symbol auf dem Finger haben'],
    'without': ['3:59 PM', 'Aufrufe:', 'Kommentare insgesamt:'],
},
'http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung': {
    'file': 'rs-ingenieure.de.tragwerksplanung.html',
    'with': ['Wir bearbeiten alle Leistungsbilder'],
    'without': ['Brückenbau'],
},
'http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html': {
    'file': 'simplyscience.ch.erdoel.html',
    'with': ['Erdöl bildet nach Millionen', 'Plankton zersetzt sich', 'in unserem Artikel "Warum wird das Erdöl knapp?".'],
    'without': ['TebNad/Shutterstock.com', 'Empfiehl dies deinen Freunden.', 'Die Natur ist aus chemischen Elementen aufgebaut'],
    'comments': ['Sehr cooles Thema!'],
},
'http://www.shingon-reiki.de/reiki-und-schamanismus/': {
    'file': 'shingon-reiki.de.schamanismus.html',
    'with': ['神道', 'War Mikao Usui Schamane?', 'Reiki und Runen'],
    'without': ['Hinterlasse eine Antwort', 'Catch Evolution', 'und gekennzeichnet mit'],
},
'http://love-hina.ch/news/0409.html': {
    'file': 'love-hina.ch.0409.html',
    'with': ['Kapitel 121 ist'],
    'without': ['Kommentare schreiben', '19:49'],
    'comments': ['Danke für dieses Kapitel'],
},
'http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html': {
    'file': 'cdu-fraktion-erfurt.de.waldorfschule.html',
    'with': ['Ein positives Signal gab', 'der steigenden Nachfrage gerecht zu werden.'],
    'without': ['Zurück zur Übersicht', 'Erhöhung für Zoo-Eintritt'],
},
'http://www.wehranlage-horka.de/veranstaltung/887/': {
    'file': 'wehranlage-horka.de.887.html',
    'with': ['Görlitzer Str. 45', 'Während Sie über den Markt schlendern', 'Konzert bei Kerzenschein'],
    'without': ['Infos zum Verein', 'nach oben', 'Datenschutzerklärung'],
},
'https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/': {
    'file': 'de.creativecommons.org.endlich.html',
    'with': ['das letzte Wort sein kann.'],
    'without': ['Ähnliche Beiträge', 'OERde14', 'Michael Blahm'],
    'comments': ['Das LG Köln hat einfach keine Ahnung'],
},
'https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/': {
    'file': 'piratenpartei-mv.de.grundeinkommen.html',
    'with': ['Unter diesem Motto findet am 14. September', 'Volksinitiative Schweiz zum Grundeinkommen.'], 
    'without': ['getaggt mit:', 'Was denkst du?'],
},
'https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/': {
    'file': 'spektrum.de.engelbart.html',
    'with': ['Zweitens wird der Genderstern', 'alldem leider – nichts.'], 
    'without': ['Originalbeitrag', 'Spektrum.de Newsletter', 'Beitragsbild'],
    'comments': ['Ich sperre nur Kommentare,'],
},
'https://www.sueddeutsche.de/kultur/genderdebatte-tief-in-der-sprache-lebt-die-alte-geschlechterordnung-fort-1.4003975': {
    'file': 'sueddeutsche.de.genderdebatte.html',
    'with': ['Es ist erstaunlich:', 'Damaris Nübling ist Professorin'], 
    'without': ['Der Fall Weinstein', 'Leser empfehlen'],
},
'https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html': {
    'file': 'rnz.de.witzel.html',
    'with': ['Für einen Roman', 'Auszeichnung der Branche.'], 
    'without': ['Ihre RNZ.', 'WHATSAPP'],
},
'https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg': {
    'file': 'austria.info.radfahren.html',
    'with': ['Salzburg liebt seine Radfahrer.', 'Puls einsaugen zu lassen.', 'Radfahren in der Fußgängerzone der Innenstadt ist erlaubt'], 
    'without': ['Das könnte Sie auch interessieren ...', 'So macht Radfahren sonst noch Spaß'],
},
'https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/': {
    'file': 'buchperlen.wordpress.com.html',
    'with': ['Dann sollten Sie erst recht', 'als saure Gürkchen entlarvte Ex-Boyfriends.'], 
    'without': ['US-Musiker Lou Reed'],
},
'https://www.fairkom.eu/about': {
    'file': 'fairkom.eu.about.html',
    'with': ['ein gemeinwohlorientiertes Partnerschaftsnetzwerk', 'Stimmberechtigung bei der Generalversammlung.'], 
    'without': ['Sicher, ökologisch und fair.', 'Gemeinwohlpunkten'],
},
'https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461': {
    'file': 'futurezone.at.lyft.html',
    'with': ['Einige Kunden des Fahrdienst-Vermittler Lyft', 'zeitweise rund vier Prozent.'], 
    'without': ['Allgemeine Nutzungsbedingungen', 'Waymo bittet Autohersteller um Geld'],  # 
},
'http://www.hundeverein-kreisunna.de/unserverein.html': {
    'file': 'hundeverein-kreisunna.de.html',
    'with': ['Beate und Norbert Olschewski', 'ein Familienmitglied und unser Freund.'], 
    'without': ['zurück zur Startseite'],
},
'https://viehbacher.com/de/steuerrecht': {
    'file': 'viehbacher.com.steuerrecht.html',
    'with': ['und wirtschaftlich orientierte Privatpersonen', 'rund um die Uhr.', 'Mensch im Mittelpunkt.'], 
    'without': ['Was sind Cookies?'],
},
'http://www.jovelstefan.de/2011/09/11/gefallt-mir/': {
    'file': 'jovelstefan.de.gefallt.html',
    'with': ['Manchmal überrascht einen', 'kein Meisterwerk war!'], 
    'without': ['Pingback von', 'Kommentare geschlossen'],
},
'https://www.stuttgart.de/item/show/132240/1': {
    'file': 'stuttgart.de.html',
    'with': ['Das Bohnenviertel entstand', 'sich herrlich entspannen.'], 
    'without': ['Nützliche Links', 'Mehr zum Thema'],
},
'https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/': {
    'file': 'modepilot.de.duschkopf.html',
    'with': ['Allerdings sieht es wie ein Dildo aus,', 'gibt Bescheid, ne?'], 
    'without': ['Ähnliche Beiträge', 'Deine E-Mail (bleibt natürlich unter uns)'],
},
'https://www.otto.de/twoforfashion/strohtasche/': {
    'file': 'otto.de.twoforfashion.html',
    'with': ['Ob rund oder kastenförmig, ob dezent oder auffällig', 'XX, Die Redaktion'], 
    'without': ['Kommentieren', 'Dienstag, 4. Juni 2019'],
},
'http://iloveponysmag.com/2018/05/24/barbour-coastal/': {
    'file': 'iloveponysmag.com.barbour.html',
    'with': ['Eine meiner besten Entscheidungen bisher:', 'Verlassenes Gewächshaus meets versteckter Deich', 'Der Hundestrand in Stein an der Ostsee'], 
    'without': ['Tags: Barbour,', 'Bitte (noch) mehr Bilder von Helle', 'Hinterlasse einen Kommentar'],
},
'https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/': {
    'file': 'moritz-meyer.net.vreni.html',
    'with': ['Das ist alles nicht gekennzeichnet, wie soll ich wissen', 'Instagramshops machen es Abmahnanwälten leicht', 'Ich bin der Ansicht, abwarten und Tee trinken.'],
    'without': ['Diese Geschichte teilen', 'Diese Website verwendet Akismet, um Spam zu reduzieren.', 'Ähnliche Beiträge'],
    'comments': ['Danke für dein Feedback. Auch zum Look meiner Seite.'],
},
'http://www.womencantalksports.com/top-10-women-talking-sports/': {
    'file': 'womencantalksports.com.top10.html',
    'with': ['3.Charlotte Jones Anderson', 'Keep Talking Sports!', ], 
    'without': ['Category: Blog Popular', 'Copyright Women Can Talk Sports.'],
},
'https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html': {
    'file': 'plentylife.blogspot.pamela-reif.html',
    'with': ['Schönheit kommt für Pamela von Innen und Außen', 'Die Workout Übungen kannte ich bereits'],
    'without': ['Links zu diesem Post', 'mehr über mich', 'Bitte beachte auch die Datenschutzerklärung von Google.'],
    'comments': ['Great post, I like your blog', 'Vielen Dank an den den Verlag'],
},
'https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html': {
    'file': 'luxuryhaven.co.hyatt.html',
    'with': ['Grounded in sustainable architecture and refined Vietnamese craftsmanship,', 'and Carmelo Resort', 'Dining and Drinking'],
    'without': ['Food Advertising by', 'A lovely note makes a beautiful day!', 'Reply'],
    'comments': ['OMG what a beautiful place to stay!'],
},
'https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/': {
    'file': 'luxuriousmagazine.com.polo.html',
    'with': ['Argentina, the birthplace of polo.', 'Simon Wittenberg travels to the Eternal City in Italy'], 
    'without': ['Luxury and lifestyle articles', 'Pinterest'],
},
'https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/': {
    'file': 'gruen-digital.de.jahrestagung.html',
    'with': ['Prof. Dr. Caja Thimm', 'zur Anmeldung.'], 
    'without': ['Next post', 'Aus den Ländern'],
},
'https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/': {
    'file': 'rechtambild.de.kochbuch.html',
    'with': ['Leitsätze des Gerichts', 'III. Die Revision der Beklagten'],
    'without': ['twittern', 'Ähnliche Beiträge', 'd.toelle[at]rechtambild.de'],
},
'http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html': {
    'file': 'internet-law.de.pseudonymen.html',
    'with': ['Wann Blogs einer Impressumspflicht unterliegen,'], 
    'without': ['Über mich', 'Gesetzes- und Rechtsprechungszitate werden automatisch', 'Comment by'],
    'comments': ['Mit Verlaub, ich halte das für groben Unsinn.'],
},
'https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html': {
    'file': 'telemedicus.info.rezension.html',
    'with': ['Aufbau und Inhalt', 'Verlag Dr. Otto Schmidt'], 
    'without': ['Anzeige:', 'Handbuch', 'Drucken', 'Ähnliche Artikel', 'Kommentar schreiben'],
},
'https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen': {
    'file': 'cnet.de.schutz.html',
    'with': ['Auch der Verweis auf ehrverletzende Bewertungen'], 
    'without': ['Anja Schmoll-Trautmann', 'Fanden Sie diesen Artikel nützlich?', 'Aktuell', 'Kommentar hinzufügen', 'Zu seinen Tätigkeitsfeldern zählen'],
},
'https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage': {
    'file': 'correctiv.org.zusage.html',
    'with': ['Vorweg: Die beteiligten AfD-Politiker', 'ist heute Abend um 21 Uhr auch im ZDF-Magazin Frontal'], 
    'without': ['Alle Artikel zu unseren Recherchen', 'Wir informieren Sie regelmäßig zum Thema Neue Rechte', 'Kommentar verfassen', 'weiterlesen'],
},
'https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845': {
    'file': 'sueddeutsche.de.flixtrain.html',
    'with': ['Bahn-Konkurrenten wie Flixbus fürchten durch den geplanten Deutschlandtakt', 'auch der Bus ein klimafreundliches Verkehrsmittel sei'], 
    'without': ['05:28 Uhr', 'ICE im S-Bahn-Takt', 'Diskussion zu diesem Artikel auf', 'Berater-Affäre bringt Bahnchef Lutz in Bedrängnis'],
},
'https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/': {
    'file': 'adac.de.kindersitze.html',
    'with': ['in punkto Sicherheit, Bedienung, Ergonomie', 'Elf Modelle sind empfehlenswert', 'Jané Koos i-Size', 'Grenzwert der Richtlinie 2014/79/EU', 'Besonders bei Babyschalen sollte geprüft werden'], 
    'without': ['23.10.2018', 'Rund ums Fahrzeug', 'Diesel-Umtauschprämien', 'Dieses Video wird über YouTube'],
},
'https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/': {
    'file': 'caktusgroup.com.django.html',
    'with': ['Was I losing my mind?', 'being cached after their first access.', 'Finding a Fix', 'from django.conf import settings', 'Clear the cache versions'], 
    'without': ['Mark Lavin', 'New Call-to-action', 'You might also like:', 'Get tips, see case studies'],
},
'https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/': {
    'file': 'computerbase.de.htc.html',
    'with': ['Vor knapp zwei Wochen', 'gibt es in der dazugehörigen Vorstellungs-News.'], 
    'without': ['Themen:', 'bis Januar 2009 Artikel für ComputerBase verfasst.', '71 Kommentare'],
},
'http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html': {
    'file': 'chineselyrics4u.com.zhineng.html',
    'with': ['就放心去吧', 'Repeat Chorus'], 
    'without': ['Posted by K A', 'Older post', 'Thank you for your support!', 'Follower'],
},
'https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/': {
    'file': 'basicthinking.de.tweets.html',
    'with': ['Frank Thelen, Investor', 'Meine Mutter ist jederzeit', 'Female founders must constantly consider', 'Thema des öffentlichen Interesses'],
    'without': ['Nach langjähriger Tätigkeit im Ausland', 'Mit Absendung des Formulars willige ich', 'Auch interessant' 'Kommentieren', 'Wir tun jeden Tag, was wir lieben.'],
    'comments': ['Schaut man ganz genau hin, ist der Habeck-Kommentar'],
},
'https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/': {
    'file': 'meedia.de.freenet.html',
    'with': ['Welche Werbeeinnahmen erwarten Sie hier langfristig?', 'wir haben keinerlei Pläne, das zu verändern.'],
    'without': ['Nachrichtenüberblick abonnieren', 'über alle aktuellen Entwicklungen auf dem Laufenden.', 'Schlagworte', 'Dauerzoff um drohenden UKW-Blackout'],
    'comments': ['Mobilcom Debitel has charged me for third party'],
},
'https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/': {
    'file': 'incurvy.de.wellness.html',
    'with': ['Zeit für Loslassen und Entspannung.', 'Erfrischende, abschwellende Augencreme Phyto Contour', 'Wie sieht dein Alltag aus?', 'Vielen Dank Anja für deine Tipps rund um Beauty'], 
    'without': ['Das Thema könnte dich auch interessieren:', 'Betreiberin von incurvy Plus Size', 'Wir verwenden Cookies'],
},
}
#'': {
#    'file': '',
#    'with': [], 
#    'without': [],
#},
#'http://exotic_tags': 'exotic_tags.html',
# overview page: result is None
# 'https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5': {
#    'file': 'chip.de.tests.html',
#    'with': [], 
#    'without': [],
#},


MOCK_PAGES = {
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
    result = extract(htmlstring, no_fallback=True, include_comments=False)
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


def run_trafilatura_justext(htmlstring):
    '''run trafilatura (without fallback) on content'''
    result = extract(htmlstring, no_fallback=False, include_comments=False)
    return result


def run_goose(htmlstring):
    '''try with the goose algorithm'''
    g = Goose()
    article = g.extract(raw_html=htmlstring)
    return article.cleaned_text


def run_readability(htmlstring):
    '''try with the Python3 port of readability.js'''
    doc = Document(htmlstring)
    return doc.summary()


def run_inscriptis(htmlstring):
    '''try with the inscriptis module'''
    text = get_text(htmlstring)
    return text


def run_html2text(htmlstring):
    '''try with the html2text module'''
    text = html2text.html2text(htmlstring)
    return text


def run_newspaper(htmlstring):
    '''try with the inscriptis module'''
    try:
        text = fulltext(htmlstring)
    except AttributeError:
        return ''
    return text


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
trafilatura_justext_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
goose_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
readability_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
inscriptis_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
newspaper_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
html2text_result = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}


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
    # html2text
    start = time.time()
    result = run_html2text(htmlstring)
    html2text_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    html2text_result['true positives'] += tp
    html2text_result['false positives'] += fp
    html2text_result['true negatives'] += tn
    html2text_result['false negatives'] += fn
    # inscriptis
    start = time.time()
    result = run_inscriptis(htmlstring)
    inscriptis_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    inscriptis_result['true positives'] += tp
    inscriptis_result['false positives'] += fp
    inscriptis_result['true negatives'] += tn
    inscriptis_result['false negatives'] += fn
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
    # trafilatura + justext
    start = time.time()
    result = run_trafilatura_justext(htmlstring)
    trafilatura_justext_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    trafilatura_justext_result['true positives'] += tp
    trafilatura_justext_result['false positives'] += fp
    trafilatura_justext_result['true negatives'] += tn
    trafilatura_justext_result['false negatives'] += fn
    # readability
    start = time.time()
    result = run_readability(htmlstring)
    readability_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    readability_result['true positives'] += tp
    readability_result['false positives'] += fp
    readability_result['true negatives'] += tn
    readability_result['false negatives'] += fn
    # goose
    start = time.time()
    result = run_goose(htmlstring)
    goose_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    goose_result['true positives'] += tp
    goose_result['false positives'] += fp
    goose_result['true negatives'] += tn
    goose_result['false negatives'] += fn
    # newspaper
    start = time.time()
    result = run_newspaper(htmlstring)
    newspaper_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    newspaper_result['true positives'] += tp
    newspaper_result['false positives'] += fp
    newspaper_result['true negatives'] += tn
    newspaper_result['false negatives'] += fn

print('number of documents:', len(EVAL_PAGES))
print('nothing')
print(nothing)
# print(calculate_f_score(nothing))
print('everything')
print(everything)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(everything)))
print('html2text')
print(html2text_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(html2text_result)))
print('inscriptis')
print(inscriptis_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(inscriptis_result)))
print('trafilatura')
print(trafilatura_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(trafilatura_result)))
print('justext')
print(justext_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(justext_result)))
print('trafilatura + justext')
print(trafilatura_justext_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(trafilatura_justext_result)))
print('readability')
print(readability_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(readability_result)))
print('goose')
print(goose_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(goose_result)))
print('newspaper')
print(newspaper_result)
print("precision: %.3f recall: %.3f f-score: %.3f" % (calculate_f_score(newspaper_result)))
