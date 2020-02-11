"""
Compare extraction results with other libraries of the same kind.
"""

# import logging
import os
import time

from lxml import etree, html

try:
    import cchardet as chardet
except ImportError:
    import chardet

import html2text
import justext
from boilerpy3 import extractors
from dragnet import extract_content #, extract_content_and_comments
from goose3 import Goose
from inscriptis import get_text
from jparser import PageModel
# from libextract.api import extract as lib_extract
from newspaper import fulltext
from newsplease import NewsPlease
from readability import Document
from trafilatura import extract
## add to tests?
# https://github.com/nikitautiu/learnhtml


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

boilerpipe_extractor = extractors.DefaultExtractor()  # ArticleExtractor DefaultExtractor LargestContentExtractor


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
'https://www.dw.com/en/uncork-the-mystery-of-germanys-fr%C3%BChburgunder/a-16863843': {
    'file': 'dw.com.uncork.html',
    'with': ['No grape variety invites as much intrigue', 'With just 0.9 hectares'],
    'without': ['Related Subjects', 'Audios and videos on the topic', 'But boozers in Berlin'],
},
'https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html': {
    'file': 'jolie.de.adele.html',
    'with': ['Adele feierte ausgelassen mit den Spice Girls', 'wie sich Adele weiterentwickelt.'],
    'without': ['Sommerzeit ist Urlaubszeit,', 'Lade weitere Inhalte'],
},
'https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx': {
    'file': 'speicherguide.de.schwierige.html',
    'with': ['Konflikte mag keiner.', 'Gespräche meistern können.'],
    'without': ['Weiterführender Link', 'Flexible Wege in die'],
},
'https://novalanalove.com/ear-candy/': {
    'file': 'novalanalove.com.ear-candy.html',
    'with': ['Earcuff: Zoeca', 'mit längeren Ohrringen (:', 'Kreole: Stella Hoops'],
    'without': ['Jetzt heißt es schnell sein:', 'Diese Website speichert Cookies', 'VON Sina Giebel'],
},
'http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/': {
    'file': 'franziska-elea.de.vuitton.html',
    'with': ['Zuerst dachte ich, ich könnte das', 'x Franzi', 'Flauschjacke: Bershka'],
    'without': ['Palm Springs Mini (links)', 'Diese Website verwendet Akismet', 'New York, New York'],
},
'https://www.gofeminin.de/abnehmen/wie-kann-ich-schnell-abnehmen-s1431651.html': {
    'file': 'gofeminin.de.abnehmen.html',
    'with': ['Crash-Diäten ziehen meist den Jojo-Effekt', 'Die Psyche spielt eine nicht unerhebliche Rolle', '2. Satt essen bei den Mahlzeiten'],
    'without': ['Sportskanone oder Sportmuffel', 'PINNEN', 'Bringt die Kilos zum Purzeln!'],
},
'https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html': {
    'file': 'brigitte.de.ikigai.html',
    'with': ['Glücks-Trend Konkurrenz', 'Praktiziere Dankbarkeit', 'dein Ikigai schon gefunden?', '14,90 Euro.'],
    'without': ['Neu in Liebe', 'Erfahre mehr', 'Erfahrung mit privater Arbeitsvermittlung?'],
},
'https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/': {
    'file': 'changelog.blog.zwischenbilanz.html',
    'with': ['Gibt es weitere Top-Maßnahmen für Multi-Channel?', 'Vielen Dank für das interessante Interview!'],
    'without': ['Annette Henkel', 'akzeptiere die Datenschutzbestimmungen', 'Diese Beiträge solltest du nicht verpassen'],
},
'https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/': {
    'file': 'threatpost.com.android.html',
    'with': ['These messages include links to the ransomware', 'using novel techniques to exfiltrate data.'],
    'without': ['Share this article:', 'Write a comment', 'Notify me when new comments are added.', 'uses Akismet to reduce spam.'],
},
'https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space': {
    'file': 'vice.com.amazon.html',
    'with': ['Brazil went dark.', 'the highest number of deforestation warnings.”'],
    'without': ['Tagged:', 'to the VICE newsletter.', 'Watch this next'],
},
'https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html': {
    'file': 'heise.de.lithium.html',
    'with': ['Die Ökobilanz von Elektroautos', 'Nur die Folie bleibt zurück'],
    'without': ['TR 7/2019', 'Forum zum Thema:', 'Highlights aus dem Heft:'],
},
'https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact': {
    'file': 'theverge.com.ios13.html',
    'with': ['Normally, video calls tend to', 'across both the eyes and nose.', 'Added ARKit explanation and tweet.'],
    'without': ['Singapore’s public health program', 'Command Line delivers daily updates'],
},
'https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/': {
    'file': 'crazy-julia.de.tipps.html',
    'with': ['in keinem Braut-Beauty-Programm fehlen darf?', 'nicht nur vor der Hochzeit ein absolutes Muss.', 'Gesundes, glänzendes Haar'],
    'without': ['Neue Wandbilder von Posterlounge', 'mit meinen Texten und mit meinen Gedanken.', 'Erforderliche Felder sind mit * markiert.'],
},
'https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis': {
    'file': 'brandenburg.de.homo-brandenburgensis.html',
    'with': ['Stilles Rackern, statt lautem Deklamieren.', 'Watt jibt’s n hier zu lachen?', 'Das Brandenbuch. Ein Land in Stichworten.'],
    'without': ['Bürgerbeteiligung', 'Anmelden', 'Foto: Timur', 'Schlagworte', 'Zeilenumbrüche und Absätze werden automatisch erzeugt.'],
},
'https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html': {
    'file': 'skateboardmsm.de.dormhagen.html',
    'with': ['Wakebeach 257', 'Be there or be square!', 'Hier geht’s zur Facebook Veranstaltung', 'Blue Tomato präsentiert die dritte'],
    'without': ['More from News', 'von Redaktion MSM', 'add yours.'],
},
'https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/': {
    'file': 'knowtechie.com.rally.html',
    'with': ['Rocket Pass 4 will begin at 10:00 a.m. PDT', 'Let us know down below in the comments', 'Holy shit, Mortal Kombat 11'],  # title: 'what to do with thousands of crates tho'
    'without': ['Related Topics', 'You can keep up with me on Twitter', 'Hit the track today with Mario Kart Tour'],
},
'https://boingboing.net/2013/07/19/hating-millennials-the-preju.html': {
    'file': 'boingboing.net.millenials.html',
    'with': ['Click through for the whole thing.', 'The generation we love to dump on'],
    'without': ['GET THE BOING BOING NEWSLETTER', 'happy mutants', 'Patti Smith and Stewart Copeland'],
},
'https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding': {
    'file': 'en.wikipedia.org.tsne.html',
    'with': ['Given a set of high-dimensional objects', 'Herein a heavy-tailed Student t-distribution'],
    'without': ['Categories:', 'Conditional random field'],
},
'https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/': {
    'file': 'mixed.de.vrodo.html',
    'with': ['Niedlicher Roboter-Spielkamerad: Anki Cozmo', 'Empfehlungen von Dennis:'],
    'without': ['Unterstütze unsere Arbeit', 'Deepfake-Hollywood', 'Avengers', 'Katzenschreck'],
},
'http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/': {
    'file': 'spreeblick.com.habeck.html',
    'with': ['Hunderttausende von jungen Paaren', 'wie flatterhaft das Mädl ist? :)'],
    'without': ['Malte Welding', 'YouTube und die Alten', 'Autokorrektur'],
},
'https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/': {
    'file': 'majkaswelt.com.fashion.html',
    'with': ['Rüschen und Volants.', 'ihr jedes Jahr tragen könnt?', 'mein Lieblingskleid vereint'],
    'without': ['Das könnte dich auch interessieren', 'Catherine Classic Lac 602'],
},
'https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/': {
    'file': 'erp-news.info.interview.html',
    'with': ['Einblicke in die Vision zukünftiger', 'Frage 4: Welche Rolle spielt Big Data', 'von The unbelievable Machine Company (*um)'],
    'without': ['Matthias Weber ist ERP-Experte mit langjähriger Berufserfahrung.', 'Die Top 5 digitalen Trends für den Mittelstand', ', leading edge,', 'Lesen Sie hier einen weiteren'],
},
'https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/': {
    'file': 'github.blog.spiceland.html',
    'with': ['Erin Spiceland is a Software Engineer for SpaceX.', 'make effective plans and goals for the future', 'looking forward to next?', 'Research Consultant at Adelard LLP'],
    'without': ['Related posts', 'Jeremy Epling', 'Missed the main event?', 'Privacy'],
},
'https://lady50plus.de/2019/06/19/sekre-mystery-bag/': {
    'file': 'lady50plus.de.sekre.html',
    'with': ['ist eine echte Luxushandtasche', 'Insgesamt 160 weibliche „Designerinnen“', 'Sei herzlich gegrüßt', 'Ein Mann alleine hätte niemals', 'in den Bann ziehen!'],
    'without': ['Erforderliche Felder sind mit', 'Benachrichtige mich', 'Reisen ist meine große Leidenschaft', 'Styling Tipps für Oktober'],
},
'https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer': {
    'file': 'sonntag-sachsen.de.emanuel.html',
    'with': ['Neuer Geschäftsführender Leiter', 'nach Leipzig wechseln.'],
    'without': ['Mehr zum Thema', 'Folgen Sie uns auf Facebook und Twitter', 'Aktuelle Ausgabe'],
},
'https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite': {
    'file': 'psl.eu.luniversite.html',
    'with': ['Le décret n°2019-1130 validant', 'restructurant à cet effet ».'],
    'without': [' utilise des cookies pour', 'En savoir plus', 'CNRS, Inserm, Inria.'],
},
'https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html': {
    'file': 'chip.de.beef.html',
    'with': ['Starke Hitze nur in der Mitte', 'ca. 35,7×29,4 cm', 'Wir sind im Steak-Himmel!'],
    'without': ['Samsung Galaxy S10 128GB', 'Für Links auf dieser Seite', 'Inga Buller ist Head of Social'],
},
'http://www.sauvonsluniversite.fr/spip.php?article8532': {
    'file': 'sauvonsluniversite.com.spip.html',
    'with': ['L’AG Éducation Île-de-France inter-degrés', 'Grève et mobilisation pour le climat', 'suivi.reformes.blanquer@gmail.com'],
    'without': ['Sauvons l’Université !', 'La semaine de SLU'],
},
'https://www.spiegel.de/spiegel/print/d-161500790.html': {
    'file': 'spiegel.de.albtraum.html',
    'with': ['Wie konnte es dazu kommen?', 'Die Geschichte beginnt am 26. Oktober', 'Es stützt seine Version.'],
    'without': ['und Vorteile sichern!', 'Verschickt', 'Die digitale Welt der Nachrichten.', 'Vervielfältigung nur mit Genehmigung'],
},
'https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/': {
    'file': 'lemire.me.json.html',
    'with': ['I use a Skylake processor with GNU GCC 8.3.', 'gsoc-2018', '0.091 GB/s', 'version 0.2 on vcpkg.'],
    'without': ['Leave a Reply', 'Science and Technology links', 'Proudly powered by WordPress'],
},
'https://www.zeit.de/mobilitaet/2020-01/zugverkehr-christian-lindner-hochgeschwindigkeitsstrecke-eu-kommission': {
    'file': 'zeit.de.zugverkehr.html',
    'with': ['36 Stunden.', 'Nationale Egoismen', 'Deutschland kaum beschleunigt.', 'geprägte Fehlentscheidung.', 'horrende Preise für miserablen Service bezahlen?'],
    'without': ['Durchgehende Tickets fehlen', 'Bitte melden Sie sich an, um zu kommentieren.'],
},
'https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020': {
    'file': 'franceculture.fr.idees.html',
    'with': ['Performativité', 'Les individus productifs communiquent', 'de nos espoirs et de nos désirs.'],
    'without': ['A la tribune je monterai', 'À découvrir', 'Le fil culture'],
},
'https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/': {
    'file': 'wikimediafoundation.org.turkey.html',
    'with': ['Bu yazının Türkçe’sini buradan okuyabilirsiniz', 'as further access is restored.'],
    'without': ['Read further in the pursuit of knowledge', 'Here’s what that means.', 'Stay up-to-date on our work.', 'Photo credits'],
},
'https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH': {
    'file': 'reuters.com.parasite.html',
    'with': ['Despite an unknown cast,', 'Additional reporting by'],
    'without': ['4 Min Read', 'The Thomson Reuters Trust Principles', 'Factbox: Key winners'],
},
'https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2': {
    'file': 'vancouversun.com.microsoft.html',
    'with': ['Microsoft Corp said on Thursday', 'It was not immediately clear if'],
    'without': ['Reuters files', 'turns CO2 into soap', 'I consent to receiving'],
    'comments': ['Postmedia is committed'],
},
'https://www.ahlen.de/start/aktuelles/aktuelle/information/nachricht/aus-ahlen/reparaturcafe-am-31-januar/': {
    'file': 'ahlen.de.reparaturcafe.html',
    'author': '',
    'title': 'Reparaturcafé am 31. Januar',
    'date': '2020-01-27',
    'description': 'Jede Menge Spaß bereitet es den ehrenamtlichen Experten im Reparaturcafé, wenn sie defekte Hausgeräte wieder flott bekommen. Die regelmäßigen Besucherinnen und Besucher wissen das schon lange. Gelegenheit zu einem Besuch im Reparaturcafé bietet sich am Freitag, 31. Januar, in der Zeit von 15.00 bis 18.00 Uhr in den Räumen des Gruppenergänzenden Dienstes des St. Vinzenz am Park (Kampstraße 13-15).',
    'categories': ['Soziales & Gesundheit'],
    'tags': [''],
    'with': ['Jede Menge Spaß bereitet es den', 'Das Projekt ist eine Kooperationsveranstaltung', 'althausa@stadt.ahlen.de'],
    'without': ['Stadtverwaltung Ahlen Rechnungseingang', 'Internetredaktion Stadt Ahlen', 'Allgemeine Sprechstunden der Verwaltung'],
    'comments': [''],
    'license': '',
    'region': 'DE',
},
'https://www.travanto.de/ferienhaus/lierfeld/40222/ferienhaus-feinen.php': {
    'file': 'travanto.de.ferienhaus-feinen.php',
    'author': '',
    'title': 'Ferienhaus Feinen',
    'date': '',
    'description': '',
    'categories': [''],
    'tags': [''],
    'with': ['Wir haben unser altes Bauernhaus zu einem', 'Das idyllische Eifeldörfchen Lierfeld liegt', 'Kinder unter 4 Jahren werden nicht als'],
    'without': ['Travanto Buchungshotline', 'tolle Gewinnspiele', ' TrustScore 4.2 580 Bewertungen'],
    'comments': [''],
    'license': '',
    'region': 'DE',
},
'https://rete-mirabile.net/notizen/15-jahre-rete-mirabile/': {
    'file': 'rete-mirabile.net.15jahre.html',
    'author': 'Andreas Kalt',
    'title': '15 Jahre rete-mirabile.net',
    'date': '2019-07-28',
    'description': 'Diesen Blog gibt es seit 15 Jahren – ein Rückblick.',
    'categories': ['Notizen'],
    'tags': ['reflexion', 'blogs', 'digitalisierung', 'inspiration', 'internet'],
    'with': ['Im Trubel des Alltags', 'Vor zehn Jahren war Twitter', 'Aktuell fallen mir wieder mehr Themen ein'],
    'without': ['Deine E-Mail-Adresse wird nicht veröffentlicht', 'Logo von Jonathas Mello', 'Gedanken über Lernen und Schule'],
    'comments': ['Vielen Dank für die netten Worte', 'Danke für Deine guten', 'Ich gehe also davon aus'],
    'license': 'CC BY-SA 4.0',
    'region': 'DE',
},
'https://shop.nmb-media.de/eBay-Template-Datenschutz-Google-Fonts-Fontawesome': {
    'file': 'nmb-media.de.ebay.html',
    'author': '',
    'title': 'Datenschutztechnische Anpassung der eBay-Verkaufsvorlagen',
    'date': '2018-06-22',
    'description': 'eBay-Auktionsvorlagen für JTL Wawi / Eazyauction, Magnalister und Afterbuy.',
    'categories': ['News'],
    'tags': [''],
    'with': ['Aus datenschutzrechtlichen Gründen wird', 'Aufgrund der derzeitigen, datenschutzrechtlichen', 'Die IP-Adressen werden'],
    'without': ['Die Beratung zu den von uns angebotenen', 'Fernwartung nach Absprache per AnyDesk', 'Bitte laden Sie sich über Ihr '],
    'comments': [''],
    'license': '',
    'region': 'DE',
},
'https://viertausendhertz.de/ddg48/': {
    'file': 'viertausendhertz.de.ddg48.html',
    'author': '',
    'title': 'Mit Musiker Voodoo Jürgens in Wien',
    'date': '2019-12-16',
    'description': '"Mit Christian Möller ist Musiker David Öllerer aka Voodoo Jürgens durch Wien spaziert – vom Friedhof, wo er selbst mal gearbeitet hat, bis in sein Stammcafé, Gulaschsuppe essen.',
    'categories': [''],
    'tags': [''],
    'with': ['Im Dialekt zu singen', 'Mit seinen Songs über Glücksspiel', 'Stammcafé, Gulaschsuppe essen'],
    'without': ['Foto: Ingo Pertramer', 'Mehr Episoden anzeigen', 'Mit dem Cartoonisten Tobias Vogel in Krefeld'],
    'comments': [''],
    'license': '',
    'region': 'DE',
},
'http://www.bibliothek2null.de/2014/05/18/alles-neue-mach-der-mai/': {
    'file': 'bibliothek2null.de.mai.html',
    'author': 'Patrick Danowski',
    'title': 'Alles Neue mach der Mai…',
    'date': '2014-05-18',
    'description': 'Innovative Ideen für Bibliotheken,  Freie Inhalte und Interessantes aus dem Web',
    'categories': ['Uncategorized'],
    'tags': ['Uncategorized'],
    'with': ['Nachdem ich mein Blog', 'Der Anfang ist gemacht', 'Ich hoffe euch gefällt der Relaunch.'],
    'without': ['Deine E-Mail-Adresse wird', 'bei Informationspraxis- ein neues', 'Permalink'],
    'comments': ['ich bin schon ganz gespannt'],
    'license': 'CC BY 2.0 DE',
    'region': 'DE',
},
'http://www.helge.at/2014/03/warum-wien-zu-blod-fur-eine-staufreie-mahu-ist/': {
    'file': 'helge.at.mahu.html',
    'author': 'Helge Fahrnberger',
    'title': 'Warum Wien zu blöd für eine staufreie Mahü ist',
    'date': '2014-03-05',
    'description': 'Die &#8220;Krone&#8221; zitiert heute meinen Tweet &#8220;Wien ist zu blöd für eine staufreie Mahü. Muss man so hinnehmen.&#8221; (Hier die Online-Version.) Warum ich glaube, dass Wien (beachte: nicht wie die Krone behauptet &#8220;alle Wiener&#8221;) zu blöd ist für eine staufreie Mariahilfer Straße (oder fast, falls die Abstimmung doch für die Verkehrsberuhigung ausgeht): 1. Die rot-grüne &hellip;',
    'categories': ['Politics'],
    'tags': [''],
    'with': ['Die “Krone” zitiert heute meinen', 'die rote Personalvertretung der Wiener Linien', 'Blöd sind also nicht die Wiener'],
    'without': ['Warum Michel Reimon nach Brüssel muss', "Helge Fahrnberger's personal pages", 'Provider information '],
    'comments': ['Es war ein wunderbarer Beschluss'],
    'license': '',
    'region': 'AT',
},
'http://www.nalas-loewenseiten.info/loewen-lexikon/?letter=M': {
    'file': 'nalas-loewenseiten.info.m.html',
    'author': '',
    'title': 'M wie Mähnenlöwe',
    'date': '',
    'description': 'Nalas LöwenseitenLöwisch gute Unterhaltung wünscht die Nala',
    'categories': ['Lexikon'],
    'tags': [''],
    'with': ['Nur die Löwenmännchen haben eine', 'Aber es gibt eben nicht nur diese tollen Schnuckllöwen', 'Und nicht nur dass, wie Peyton West'],
    'without': ['Nala Löwenkönigin', 'Prankentausch', 'Lexikon'],
    'comments': [''],
    'license': '',
    'region': '',
},
'https://blogoff.de/2015/11/12/i-htm/': {
    'file': 'blogoff.de.i-htm.html',
    'author': '',
    'title': '3 verrückte Orte in Berlin',
    'date': '2015-11-12',
    'description': '',
    'categories': [''],
    'tags': [''],
    'with': ['In Berlin lebe ich nun', 'Vielen Dank an die S-Bahn', 'Base Flying'],
    'without': ['I ♥ BLOG OFF!', 'Was passiert hier eigentlich noch?', 'powdered by wordpress'],
    'comments': [''], 
    'license': 'CC BY-NC-SA 2.0 DE',
    'region': 'DE',
},
'https://de.globalvoices.org/2019/04/30/ein-jahr-voller-proteste-nicaraguaner-wollen-nicht-mehr-nur-den-rucktritt-ortegas-sondern-einen-neuanfang/': {
    'file': 'de.globalvoices.org.nicaragua.html',
    'author': 'Elisa Marvena',
    'title': 'Ein Jahr voller Proteste: Nicaraguaner wollen nicht mehr nur den Rücktritt Ortegas, sondern einen Neuanfang',
    'date': '2019-04-30',
    'description': '[Wir müssen] Autoritarismus, Sexismus, Alleinherrschaft einzelner und andere Übel, die in die politische Kultur dieses Landes Einzug gehalten haben, beseitigen.',
    'categories': ['Lateinamerika', 'Nicaragua', 'Bürgermedien', 'Kriege & Konflikte', 'Meinungsfreiheit', 'Menschenrechte', 'Politik', 'Protest'],
    'tags': [''],
    'with': ['Seit dem Ausbruch der Massenproteste gegen', 'Laut der niedrigsten Schätzung', 'Ich sah, wie eine Freundin von der Universität'],
    'without': ['@globalvoices verdient einen Preis für die', 'Italiano', 'Name (Pflichtfeld)'],
    'comments': [''],
    'license': 'CC BY 3.0',
    'region': 'DE',
},
'http://www.heiko-adams.de/laufen-im-winter-von-baeh-zu-yeah-in-12-monaten/': {
    'file': 'heiko-adams.de.laufen.html',
    'author': 'Heiko',
    'title': 'Laufen im Winter: Von „bäh!“ zu „yeah!“ in 12 Monaten.',
    'date': '2019-02-10',
    'description': '',
    'categories': ['Privat', 'Sport'],
    'tags': ['dunkel', 'Dunkelheit', 'Laufen', 'Running', 'Training', 'Winter'],
    'with': ['Heute, 12 Monate später,', 'das gefällt mir 😉'],
    'without': ['Einfach laufen lassen', "Heiko's Activity"],
    'comments': [''],
    'license': '',
    'region': 'DE',
},
'https://www.wbf.admin.ch/wbf/de/home/dokumentation/nsb-news_list.msg-id-14093.html': {
    'file': 'wbf.admin.ch.14093.html',
    'author': '',
    'title': '',
    'date': '',
    'description': '',  # in HTML source
    'categories': [''],
    'tags': [''],
    'with': ['beim SP-Städtegipfel', 'Dies führt dazu, dass die Sozialpolitik', 'wie in der Nationalhymne,'],
    'without': ['Kommunikationsdienst', 'Letzte Änderung', 'Informiert bleiben'],
    'comments': [''],  # 0 or 3 segments
    'license': '',  # if CC-...
    'region': 'CH',  # if obvious: DE, CH, AT
},
'https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html': {
    'file': 'faz.net.streaming.html',
    'author': '',
    'title': '',
    'date': '2020-01-28',
    'description': '',  # in HTML source
    'categories': [''],
    'tags': [''],
    'with': ['„Die Liste der Künstler', 'nicht bloß um höhere Einkünfte', 'Der Wandel der Musikbranche'],
    'without': ['Etwa 100 deutsche Reisende', 'Abonnieren Sie unsere', 'Joe Kaeser deutet vage', 'Redakteur in der Wirtschaft.'],
    'comments': ['keinen Bock auf solche Buchhalter', 'Verklagt eure Labels', 'Zur Verdeutlichung ein Extrembeispiel:'],
    'license': '',  # if CC-...
    'region': 'DE',  # if obvious: DE, CH, AT
},
'https://www.toptal.com/python/top-10-mistakes-that-python-programmers-make': {
    'file': 'toptal.com.python.html',
    'author': '',
    'title': '',
    'date': '',
    'description': '',  # in HTML source
    'categories': [''],
    'tags': [''],
    'with': ['and code reuse.', 'bar is optional', 'What the $%#!&??', 'And you then tried to do', 'Familiarizing oneself with the key'],
    'without': ['Martin has worked as', 'delivered weekly.', 'MCMC Methods:'],
    'comments': ['for common mistake #6', 'This is a fairer comparison', 'I liked the article.'],
    'license': '',  # if CC-...
    'region': '',  # if obvious: DE, CH, AT
},
'https://www.reddit.com/r/Python/comments/1bbbwk/whats_your_opinion_on_what_to_include_in_init_py/': {
    'file': 'reddit.com.init.html',
    'author': '',
    'title': '',
    'date': '',
    'description': '',  # in HTML source
    'categories': [''],
    'tags': [''],
    'with': ['Considering a package', 'Import key functions', 'EDIT: Thanks a lot'],
    'without': ['news about the dynamic', 'All rights reserved', 'I see your minesweeper'],
    'comments': ['I do similar things.', 'from foo.bar import x, y, z', 'IMO it makes things'],
    'license': '',  # if CC-...
    'region': '',  # if obvious: DE, CH, AT
},
}
# overview page: result is None
# 'https://www.chip.de/tests/akkuschrauber-werkzeug-co,82197/5': {
#    'file': 'chip.de.tests.html',
#    'with': [],
#    'without': [],
#},


def load_document(filename):
    '''load mock page from samples'''
    mypath = os.path.join(TEST_DIR, 'cache', filename)
    if not os.path.isfile(mypath):
        mypath = os.path.join(TEST_DIR, 'eval', filename)
    try:
        with open(mypath, 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(mypath, 'rb') as inputf:
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
    '''try with the newspaper module'''
    try:
        text = fulltext(htmlstring)
    except AttributeError:
        return ''
    return text


def run_dragnet(htmlstring):
    '''try with the dragnet module'''
    content = extract_content(htmlstring)
    return content


def run_boilerpipe(htmlstring):
    '''try with the boilerpipe algorithm'''
    try:
        content = boilerpipe_extractor.get_content(htmlstring)
    except:
        content = ''
    return content


def run_newsplease(htmlstring):
   '''try with newsplease'''
   article = NewsPlease.from_html(htmlstring, url=None)
   return article.maintext


def run_jparser(htmlstring):
   '''try with jparser'''
   pm = PageModel(htmlstring)
   result = pm.extract()
   mylist = list()
   for x in result['content']:
       if x['type'] in ('text', 'html'):
           mylist.append(str(x['data']))
   return ' '.join(mylist)


#def run_libextract(htmlstring):
#    '''try with the libextract module'''
#    textlist = list()
#    for textnode in list(lib_extract(htmlstring)):
#        textlist.append(textnode.text_content())
#    textcontent = '\n'.join(textlist)
#    return contextcontenttent


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


def calculate_scores(mydict):
    '''output weighted result score'''
    tp, fn, fp, tn = mydict['true positives'], mydict['false negatives'], mydict['false positives'], mydict['true negatives']
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    fscore = (2*tp)/(2*tp + fp + fn)  # 2*((precision*recall)/(precision+recall))
    return precision, recall, accuracy, fscore


template_dict = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
everything, nothing, trafilatura_result, justext_result, trafilatura_justext_result, goose_result, readability_result, inscriptis_result, newspaper_result, html2text_result, dragnet_result, boilerpipe_result, newsplease_result, jparser_result = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
everything.update(template_dict)
nothing.update(template_dict)
trafilatura_result.update(template_dict)
justext_result.update(template_dict)
trafilatura_justext_result.update(template_dict)
goose_result.update(template_dict)
readability_result.update(template_dict)
inscriptis_result.update(template_dict)
newspaper_result.update(template_dict)
html2text_result.update(template_dict)
dragnet_result.update(template_dict)
boilerpipe_result.update(template_dict)
newsplease_result.update(template_dict)
jparser_result.update(template_dict)


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
    # dragnet
    start = time.time()
    result = run_dragnet(htmlstring)
    dragnet_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    dragnet_result['true positives'] += tp
    dragnet_result['false positives'] += fp
    dragnet_result['true negatives'] += tn
    dragnet_result['false negatives'] += fn
    # boilerpipe
    start = time.time()
    result = run_boilerpipe(htmlstring)
    boilerpipe_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    boilerpipe_result['true positives'] += tp
    boilerpipe_result['false positives'] += fp
    boilerpipe_result['true negatives'] += tn
    boilerpipe_result['false negatives'] += fn
    # newsplease
    start = time.time()
    result = run_newsplease(htmlstring)
    newsplease_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    newsplease_result['true positives'] += tp
    newsplease_result['false positives'] += fp
    newsplease_result['true negatives'] += tn
    newsplease_result['false negatives'] += fn
    # jparser
    start = time.time()
    result = run_jparser(htmlstring)
    jparser_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES, item)
    jparser_result['true positives'] += tp
    jparser_result['false positives'] += fp
    jparser_result['true negatives'] += tn
    jparser_result['false negatives'] += fn


print('number of documents:', len(EVAL_PAGES))
print('nothing')
print(nothing)
# print(calculate_f_score(nothing))
print('everything')
print(everything)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(everything)))
print('html2text')
print(html2text_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(html2text_result)))
print('inscriptis')
print(inscriptis_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(inscriptis_result)))
print('trafilatura')
print(trafilatura_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_result)))
print('justext')
print(justext_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(justext_result)))
print('trafilatura + justext')
print(trafilatura_justext_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_justext_result)))
print('readability')
print(readability_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(readability_result)))
print('goose')
print(goose_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(goose_result)))
print('newspaper')
print(newspaper_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(newspaper_result)))
print('dragnet')
print(dragnet_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(dragnet_result)))
print('boilerpipe')
print(boilerpipe_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(boilerpipe_result)))
print('newsplease')
print(newsplease_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(newsplease_result)))
print('jparser')
print(jparser_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(jparser_result)))
