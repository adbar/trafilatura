# pylint: disable=C0114,C0301,C0302
EVAL_PAGES = {
    "https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/": {
        "file": "die-partei.net.luebeck.html",
        "with": ["Die GEMA dreht völlig am Zeiger!", "http://www.openpetition.de"],
        "without": ["31. Mai", "Impressum", "Steuerdarling"],
    },
    "https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html": {
        "file": "bmjv.de.konsum.html",
        "with": [
            "Auch hier gilt der Grundsatz,",
            "Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol",
            "(Billigkeitskontrolle nach § 315 BGB)",
        ],
        "without": ["Impressum", "Weitere Informationen", "Transparenz bei Preisanpassungen", "Twitter"],
    },
    "http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/": {
        "file": "kulinariaathome.com.mandelplätzchen.html",
        "with": [
            "(+ 15 Minuten backen)",
            "200 g Zucker",
            "zu einem glatten Teig verarbeiten.",
            "Ein Backblech mit Backpapier auslegen.",
        ],
        "without": ["Sharen mit", "Creative Commons", "Trotz sorgfältiger inhaltlicher Kontrolle"],
    },
    "https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/": {
        "file": "denkanstoos.com.2012.html",
        "with": ["Moderator: Hass Chapman", "Two or three 10-15 min", "What type? Etc. (30 mins)"],
        "without": ["Dieser Eintrag wurde veröffentlicht", "Mit anderen Teillen", 'In "DenkanStoos-Treffen"'],
    },
    "https://www.demokratiewebstatt.at/thema/thema-umwelt-und-klima/woher-kommt-die-dicke-luft": {
        "file": "demokratiewebstatt.at.luft.html",
        "with": ["Eines der großen Probleme,", "Millionen Menschen fahren jeden Tag", "versteinerte Dinosaurierknochen."],
        "without": ["Clipdealer", "Teste dein Wissen", "Thema: Fußball"],
    },
    "http://www.toralin.de/schmierfett-reparierend-verschlei-y-910.html": {
        "file": "toralin.de.schmierfett.html",
        "with": ["Die Lebensdauer von Bauteilen erhöht sich beträchtlich.", "bis zu 50% Verschleiß.", "Li-Seifen/Mineralöl"],
        "without": [
            "Newsletter",
            "Wie bewerten Sie diesen Artikel?",
            "Meander 151",
            "Sie könnten auch an folgenden Artikeln interessiert sein",
        ],
    },
    "https://www.ebrosia.de/beringer-zinfandel-rose-stone-cellars-lieblich-suess": {
        "file": "ebrosia.de.zinfandel.html",
        "with": [
            "Das Bukett präsentiert sich",
            "Besonders gut passt er zu asiatischen Gerichten",
            "Details zum Artikel",
            "Dekantieren nicht notwendig",
        ],
        "without": [
            "Kunden kauften auch",
            "Gutschein sichern",
            "wurde erfolgreich hinzugefügt.",
            "Bitte geben Sie die Zahlenfolge",
        ],
    },
    "https://www.landwirt.com/Precision-Farming-Moderne-Sensortechnik-im-Kuhstall,,4229,,Bericht.html": {
        "file": "landwirt.com.sensortechnik.html",
        "with": ["b) Überwachung der somatischen Zellen", "Wiederkauverhalten und Kotkonsistenz.", "Köllitsch (D)"],
        "without": ["Anzeigentarife", "weiterempfehlen", "New Holland T6050", "Aktuelle Berichte aus dieser Kategorie"],
    },
    "http://schleifen.ucoz.de/blog/briefe/2010-10-26-18": {
        "file": "schleifen.ucoz.de.briefe.html",
        "with": ["Es war gesagt,", "Jedes Mädchen träumt von Justin", "Symbol auf dem Finger haben"],
        "without": ["3:59 PM", "Aufrufe:", "Kommentare insgesamt:"],
    },
    "http://www.rs-ingenieure.de/de/hochbau/leistungen/tragwerksplanung": {
        "file": "rs-ingenieure.de.tragwerksplanung.html",
        "with": ["Wir bearbeiten alle Leistungsbilder"],
        "without": ["Brückenbau"],
    },
    "http://www.simplyscience.ch/teens-liesnach-archiv/articles/wie-entsteht-erdoel.html": {
        "file": "simplyscience.ch.erdoel.html",
        "with": ["Erdöl bildet nach Millionen", "Plankton zersetzt sich", 'in unserem Artikel "Warum wird das Erdöl knapp?".'],
        "without": [
            "TebNad/Shutterstock.com",
            "Empfiehl dies deinen Freunden.",
            "Die Natur ist aus chemischen Elementen aufgebaut",
        ],
        "comments": ["Sehr cooles Thema!"],
    },
    "http://www.shingon-reiki.de/reiki-und-schamanismus/": {
        "file": "shingon-reiki.de.schamanismus.html",
        "with": ["神道", "War Mikao Usui Schamane?", "Reiki und Runen"],
        "without": ["Hinterlasse eine Antwort", "Catch Evolution", "und gekennzeichnet mit"],
    },
    "http://love-hina.ch/news/0409.html": {
        "file": "love-hina.ch.0409.html",
        "with": ["Kapitel 121 ist"],
        "without": ["Kommentare schreiben", "19:49"],
        "comments": ["Danke für dieses Kapitel"],
    },
    "http://www.cdu-fraktion-erfurt.de/inhalte/aktuelles/entwicklung-der-waldorfschule-ermoeglicht/index.html": {
        "file": "cdu-fraktion-erfurt.de.waldorfschule.html",
        "with": ["Ein positives Signal gab", "der steigenden Nachfrage gerecht zu werden."],
        "without": ["Zurück zur Übersicht", "Erhöhung für Zoo-Eintritt"],
    },
    "http://www.wehranlage-horka.de/veranstaltung/887/": {
        "file": "wehranlage-horka.de.887.html",
        "with": ["Görlitzer Str. 45", "Während Sie über den Markt schlendern", "Konzert bei Kerzenschein"],
        "without": ["Infos zum Verein", "nach oben", "Datenschutzerklärung"],
    },
    "https://de.creativecommons.org/index.php/2014/03/20/endlich-wird-es-spannend-die-nc-einschraenkung-nach-deutschem-recht/": {
        "file": "de.creativecommons.org.endlich.html",
        "with": ["das letzte Wort sein kann."],
        "without": ["Ähnliche Beiträge", "OERde14", "Michael Blahm"],
        "comments": ["Das LG Köln hat einfach keine Ahnung"],
    },
    "https://piratenpartei-mv.de/blog/2013/09/12/grundeinkommen-ist-ein-menschenrecht/": {
        "file": "piratenpartei-mv.de.grundeinkommen.html",
        "with": ["Unter diesem Motto findet am 14. September", "Volksinitiative Schweiz zum Grundeinkommen."],
        "without": ["getaggt mit:", "Was denkst du?"],
    },
    "https://scilogs.spektrum.de/engelbart-galaxis/die-ablehnung-der-gendersprache/": {
        "file": "spektrum.de.engelbart.html",
        "with": ["Zweitens wird der Genderstern", "alldem leider – nichts."],
        "without": ["Originalbeitrag", "Spektrum.de Newsletter", "Beitragsbild"],
        "comments": ["Ich sperre nur Kommentare,"],
    },
    "https://www.rnz.de/nachrichten_artikel,-zz-dpa-Schlaglichter-Frank-Witzel-erhaelt-Deutschen-Buchpreis-2015-_arid,133484.html": {
        "file": "rnz.de.witzel.html",
        "with": ["Für einen Roman", "Auszeichnung der Branche."],
        "without": ["Ihre RNZ.", "WHATSAPP"],
    },
    "https://www.austria.info/de/aktivitaten/radfahren/radfahren-in-der-weltstadt-salzburg": {
        "file": "austria.info.radfahren.html",
        "with": [
            "Salzburg liebt seine Radfahrer.",
            "Puls einsaugen zu lassen.",
            "Radfahren in der Fußgängerzone der Innenstadt ist erlaubt",
        ],
        "without": ["Das könnte Sie auch interessieren ...", "So macht Radfahren sonst noch Spaß"],
    },
    "https://buchperlen.wordpress.com/2013/10/20/leandra-lou-der-etwas-andere-modeblog-jetzt-auch-zwischen-buchdeckeln/": {
        "file": "buchperlen.wordpress.com.html",
        "with": ["Dann sollten Sie erst recht", "als saure Gürkchen entlarvte Ex-Boyfriends."],
        "without": ["US-Musiker Lou Reed"],
    },
    "https://www.fairkom.eu/about": {
        "file": "fairkom.eu.about.html",
        "with": ["ein gemeinwohlorientiertes Partnerschaftsnetzwerk", "Stimmberechtigung bei der Generalversammlung."],
        "without": ["Sicher, ökologisch und fair.", "Gemeinwohlpunkten"],
    },
    "https://futurezone.at/digital-life/uber-konkurrent-lyft-startet-mit-waymo-robotertaxis-in-usa/400487461": {
        "file": "futurezone.at.lyft.html",
        "with": ["Einige Kunden des Fahrdienst-Vermittler Lyft", "zeitweise rund vier Prozent."],
        "without": ["Allgemeine Nutzungsbedingungen", "Waymo bittet Autohersteller um Geld"],  #
    },
    "http://www.hundeverein-kreisunna.de/unserverein.html": {
        "file": "hundeverein-kreisunna.de.html",
        "with": ["Beate und Norbert Olschewski", "ein Familienmitglied und unser Freund."],
        "without": ["zurück zur Startseite"],
    },
    "https://viehbacher.com/de/steuerrecht": {
        "file": "viehbacher.com.steuerrecht.html",
        "with": ["und wirtschaftlich orientierte Privatpersonen", "rund um die Uhr.", "Mensch im Mittelpunkt."],
        "without": ["Was sind Cookies?"],
    },
    "http://www.jovelstefan.de/2011/09/11/gefallt-mir/": {
        "file": "jovelstefan.de.gefallt.html",
        "with": ["Manchmal überrascht einen", "kein Meisterwerk war!"],
        "without": ["Pingback von", "Kommentare geschlossen"],
    },
    "https://www.stuttgart.de/item/show/132240/1": {
        "file": "stuttgart.de.html",
        "with": ["Das Bohnenviertel entstand", "sich herrlich entspannen."],
        "without": ["Nützliche Links", "Mehr zum Thema"],
    },
    "https://www.modepilot.de/2019/05/21/geht-euch-auch-so-oder-auf-reisen-nie-ohne-meinen-duschkopf/": {
        "file": "modepilot.de.duschkopf.html",
        "with": ["Allerdings sieht es wie ein Dildo aus,", "gibt Bescheid, ne?"],
        "without": ["Ähnliche Beiträge", "Deine E-Mail (bleibt natürlich unter uns)"],
    },
    "https://www.otto.de/twoforfashion/strohtasche/": {
        "file": "otto.de.twoforfashion.html",
        "with": ["Ob rund oder kastenförmig, ob dezent oder auffällig", "XX, Die Redaktion"],
        "without": ["Kommentieren", "Dienstag, 4. Juni 2019"],
    },
    "http://iloveponysmag.com/2018/05/24/barbour-coastal/": {
        "file": "iloveponysmag.com.barbour.html",
        "with": [
            "Eine meiner besten Entscheidungen bisher:",
            "Verlassenes Gewächshaus meets versteckter Deich",
            "Der Hundestrand in Stein an der Ostsee",
        ],
        "without": ["Tags: Barbour,", "Bitte (noch) mehr Bilder von Helle", "Hinterlasse einen Kommentar"],
    },
    "https://moritz-meyer.net/blog/vreni-frost-instagram-abmahnung/": {
        "file": "moritz-meyer.net.vreni.html",
        "with": [
            "Das ist alles nicht gekennzeichnet, wie soll ich wissen",
            "Instagramshops machen es Abmahnanwälten leicht",
            "Ich bin der Ansicht, abwarten und Tee trinken.",
        ],
        "without": ["Diese Geschichte teilen", "Diese Website verwendet Akismet, um Spam zu reduzieren.", "Ähnliche Beiträge"],
        "comments": ["Danke für dein Feedback. Auch zum Look meiner Seite."],
    },
    "https://plentylife.blogspot.com/2017/05/strong-beautiful-pamela-reif-rezension.html": {
        "file": "plentylife.blogspot.pamela-reif.html",
        "with": ["Schönheit kommt für Pamela von Innen und Außen", "Die Workout Übungen kannte ich bereits"],
        "without": ["Links zu diesem Post", "mehr über mich", "Bitte beachte auch die Datenschutzerklärung von Google."],
        "comments": ["Great post, I like your blog", "Vielen Dank an den den Verlag"],
    },
    "https://www.luxuryhaven.co/2019/05/nam-nghi-phu-quoc-unbound-collection-by-hyatt-officially-opens.html": {
        "file": "luxuryhaven.co.hyatt.html",
        "with": [
            "Grounded in sustainable architecture and refined Vietnamese craftsmanship,",
            "and Carmelo Resort",
            "Dining and Drinking",
        ],
        "without": ["Food Advertising by", "A lovely note makes a beautiful day!", "Reply"],
        "comments": ["OMG what a beautiful place to stay!"],
    },
    "https://www.luxuriousmagazine.com/2019/06/royal-salute-polo-rome/": {
        "file": "luxuriousmagazine.com.polo.html",
        "with": ["Argentina, the birthplace of polo.", "Simon Wittenberg travels to the Eternal City in Italy"],
        "without": ["Luxury and lifestyle articles", "Pinterest"],
    },
    "https://www.gruen-digital.de/2015/01/digitalpolitisches-jahrestagung-2015-der-heinrich-boell-stiftung-baden-wuerttemberg/": {
        "file": "gruen-digital.de.jahrestagung.html",
        "with": ["Prof. Dr. Caja Thimm", "zur Anmeldung."],
        "without": ["Next post", "Aus den Ländern"],
    },
    "https://www.rechtambild.de/2011/10/bgh-marions-kochbuch-de/": {
        "file": "rechtambild.de.kochbuch.html",
        "with": ["Leitsätze des Gerichts", "III. Die Revision der Beklagten"],
        "without": ["twittern", "Ähnliche Beiträge", "d.toelle[at]rechtambild.de"],
    },
    "http://www.internet-law.de/2011/07/verstost-der-ausschluss-von-pseudonymen-bei-google-gegen-deutsches-recht.html": {
        "file": "internet-law.de.pseudonymen.html",
        "with": ["Wann Blogs einer Impressumspflicht unterliegen,"],
        "without": ["Über mich", "Gesetzes- und Rechtsprechungszitate werden automatisch", "Comment by"],
        "comments": ["Mit Verlaub, ich halte das für groben Unsinn."],
    },
    "https://www.telemedicus.info/article/2766-Rezension-Haerting-Internetrecht,-5.-Auflage-2014.html": {
        "file": "telemedicus.info.rezension.html",
        "with": ["Aufbau und Inhalt", "Verlag Dr. Otto Schmidt"],
        "without": ["Anzeige:", "Handbuch", "Drucken", "Ähnliche Artikel", "Kommentar schreiben"],
    },
    "https://www.cnet.de/88130484/so-koennen-internet-user-nach-dem-eugh-urteil-fuer-den-schutz-sensibler-daten-sorgen": {
        "file": "cnet.de.schutz.html",
        "with": ["liefert eine Einschätzung", "Auch der Verweis auf ehrverletzende Bewertungen", "Am 13. Mai 2014"],
        "without": [
            "Anja Schmoll-Trautmann",
            "Fanden Sie diesen Artikel nützlich?",
            "Aktuell",
            "Kommentar hinzufügen",
            "Zu seinen Tätigkeitsfeldern zählen",
        ],
    },
    "https://correctiv.org/aktuelles/neue-rechte/2019/05/14/wir-haben-bereits-die-zusage": {
        "file": "correctiv.org.zusage.html",
        "with": ["Vorweg: Die beteiligten AfD-Politiker", "ist heute Abend um 21 Uhr auch im ZDF-Magazin Frontal"],
        "without": [
            "Alle Artikel zu unseren Recherchen",
            "Wir informieren Sie regelmäßig zum Thema Neue Rechte",
            "Kommentar verfassen",
            "weiterlesen",
        ],
    },
    "https://www.sueddeutsche.de/wirtschaft/bahn-flixbus-flixtrain-deutschlandtakt-fernverkehr-1.4445845": {
        "file": "sueddeutsche.de.flixtrain.html",
        "with": [
            "Bahn-Konkurrenten wie Flixbus fürchten durch den geplanten Deutschlandtakt",
            "auch der Bus ein klimafreundliches Verkehrsmittel sei",
        ],
        "without": [
            "05:28 Uhr",
            "ICE im S-Bahn-Takt",
            "Diskussion zu diesem Artikel auf",
            "Berater-Affäre bringt Bahnchef Lutz in Bedrängnis",
        ],
    },
    "https://www.adac.de/rund-ums-fahrzeug/tests/kindersicherheit/kindersitztest-2018/": {
        "file": "adac.de.kindersitze.html",
        "with": [
            "in punkto Sicherheit, Bedienung, Ergonomie",
            "Elf Modelle sind empfehlenswert",
            "Jané Koos i-Size",
            "Grenzwert der Richtlinie 2014/79/EU",
            "Besonders bei Babyschalen sollte geprüft werden",
        ],
        "without": ["23.10.2018", "Rund ums Fahrzeug", "Diesel-Umtauschprämien", "Dieses Video wird über YouTube"],
    },
    "https://www.caktusgroup.com/blog/2015/06/08/testing-client-side-applications-django-post-mortem/": {
        "file": "caktusgroup.com.django.html",
        "with": [
            "Was I losing my mind?",
            "being cached after their first access.",
            "Finding a Fix",
            "from django.conf import settings",
            "Clear the cache versions",
        ],
        "without": ["Mark Lavin", "New Call-to-action", "You might also like:", "Get tips, see case studies"],
    },
    "https://www.computerbase.de/2007-06/htc-touch-bald-bei-o2-als-xda-nova/": {
        "file": "computerbase.de.htc.html",
        "with": ["Vor knapp zwei Wochen", "gibt es in der dazugehörigen Vorstellungs-News."],
        "without": ["Themen:", "bis Januar 2009 Artikel für ComputerBase verfasst.", "71 Kommentare"],
    },
    "http://www.chineselyrics4u.com/2011/07/zhi-neng-xiang-nian-ni-jam-hsiao-jing.html": {
        "file": "chineselyrics4u.com.zhineng.html",
        "with": ["就放心去吧", "Repeat Chorus"],
        "without": ["Posted by K A", "Older post", "Thank you for your support!", "Follower"],
    },
    "https://www.basicthinking.de/blog/2018/12/05/erfolgreiche-tweets-zutaten/": {
        "file": "basicthinking.de.tweets.html",
        "with": [
            "Frank Thelen, Investor",
            "Meine Mutter ist jederzeit",
            "Female founders must constantly consider",
            "Thema des öffentlichen Interesses",
        ],
        "without": [
            "Nach langjähriger Tätigkeit im Ausland",
            "Mit Absendung des Formulars willige ich",
            "Auch interessant",
            "Kommentieren",
            "Wir tun jeden Tag, was wir lieben.",
        ],
        "comments": ["Schaut man ganz genau hin, ist der Habeck-Kommentar"],
    },
    "https://meedia.de/2016/03/08/einstieg-ins-tv-geschaeft-wie-freenet-privatkunden-fuer-antennen-tv-in-hd-qualitaet-gewinnen-will/": {
        "file": "meedia.de.freenet.html",
        "with": [
            "Dadurch sollen Privatkunden",
            "Welche Werbeeinnahmen erwarten Sie hier langfristig?",
            "wir haben keinerlei Pläne, das zu verändern.",
        ],
        "without": [
            "Nachrichtenüberblick abonnieren",
            "über alle aktuellen Entwicklungen auf dem Laufenden.",
            "Schlagworte",
            "Dauerzoff um drohenden UKW-Blackout",
        ],
        "comments": ["Mobilcom Debitel has charged me for third party"],
    },
    "https://www.incurvy.de/trends-grosse-groessen/wellness-gesichtsbehandlung-plaisir-daromes/": {
        "file": "incurvy.de.wellness.html",
        "with": [
            "Zeit für Loslassen und Entspannung.",
            "Erfrischende, abschwellende Augencreme Phyto Contour",
            "Wie sieht dein Alltag aus?",
            "Vielen Dank Anja für deine Tipps rund um Beauty",
        ],
        "without": ["Das Thema könnte dich auch interessieren:", "Betreiberin von incurvy Plus Size", "Wir verwenden Cookies"],
    },
    "https://www.jolie.de/stars/adele-10-kilo-abgenommen-sie-zeigt-sich-schlanker-denn-je-200226.html": {
        "file": "jolie.de.adele.html",
        "with": ["Adele feierte ausgelassen mit den Spice Girls", "wie sich Adele weiterentwickelt."],
        "without": ["Sommerzeit ist Urlaubszeit,", "Lade weitere Inhalte"],
    },
    "https://www.speicherguide.de/digitalisierung/faktor-mensch/schwierige-gespraeche-so-gehts-24376.aspx": {
        "file": "speicherguide.de.schwierige.html",
        "with": ["Konflikte mag keiner.", "Gespräche meistern können."],
        "without": ["Weiterführender Link", "Flexible Wege in die"],
    },
    "https://novalanalove.com/ear-candy/": {
        "file": "novalanalove.com.ear-candy.html",
        "with": ["Earcuff: Zoeca", "mit längeren Ohrringen (:", "Kreole: Stella Hoops"],
        "without": ["Jetzt heißt es schnell sein:", "Diese Website speichert Cookies", "VON Sina Giebel"],
    },
    "http://www.franziska-elea.de/2019/02/10/das-louis-vuitton-missgeschick/": {
        "file": "franziska-elea.de.vuitton.html",
        "with": ["Zuerst dachte ich, ich könnte das", "x Franzi", "Flauschjacke: Bershka"],
        "without": ["Palm Springs Mini (links)", "Diese Website verwendet Akismet", "New York, New York"],
    },
    "https://www.brigitte.de/liebe/persoenlichkeit/ikigai-macht-dich-sofort-gluecklicher--10972896.html": {
        "file": "brigitte.de.ikigai.html",
        "with": ["Glücks-Trend Konkurrenz", "Praktiziere Dankbarkeit", "dein Ikigai schon gefunden?", "14,90 Euro."],
        "without": ["Neu in Liebe", "Erfahre mehr", "Erfahrung mit privater Arbeitsvermittlung?"],
    },
    "https://www.changelog.blog/zwischenbilanz-jan-kegelberg-ueber-tops-und-flops-bei-der-transformation-von-sportscheck/": {
        "file": "changelog.blog.zwischenbilanz.html",
        "with": ["Gibt es weitere Top-Maßnahmen für Multi-Channel?", "Vielen Dank für das interessante Interview!"],
        "without": ["Annette Henkel", "akzeptiere die Datenschutzbestimmungen", "Diese Beiträge solltest du nicht verpassen"],
    },
    "https://threatpost.com/android-ransomware-spreads-via-sex-simulation-game-links-on-reddit-sms/146774/": {
        "file": "threatpost.com.android.html",
        "with": ["These messages include links to the ransomware", "using novel techniques to exfiltrate data."],
        "without": [
            "Share this article:",
            "Write a comment",
            "Notify me when new comments are added.",
            "uses Akismet to reduce spam.",
        ],
    },
    "https://www.vice.com/en_uk/article/d3avvm/the-amazon-is-on-fire-and-the-smoke-can-be-seen-from-space": {
        "file": "vice.com.amazon.html",
        "with": ["Brazil went dark.", "the highest number of deforestation warnings.”"],
        "without": ["Tagged:", "to the VICE newsletter.", "Watch this next"],
    },
    "https://www.heise.de/newsticker/meldung/Lithium-aus-dem-Schredder-4451133.html": {
        "file": "heise.de.lithium.html",
        "with": ["Die Ökobilanz von Elektroautos", "Nur die Folie bleibt zurück"],
        "without": ["TR 7/2019", "Forum zum Thema:", "Highlights aus dem Heft:"],
    },
    "https://www.theverge.com/2019/7/3/20680681/ios-13-beta-3-facetime-attention-correction-eye-contact": {
        "file": "theverge.com.ios13.html",
        "with": ["Normally, video calls tend to", "across both the eyes and nose.", "Added ARKit explanation and tweet."],
        "without": ["Singapore’s public health program", "Command Line delivers daily updates"],
    },
    "https://crazy-julia.de/beauty-tipps-die-jede-braut-kennen-sollte/": {
        "file": "crazy-julia.de.tipps.html",
        "with": [
            "in keinem Braut-Beauty-Programm fehlen darf?",
            "nicht nur vor der Hochzeit ein absolutes Muss.",
            "Gesundes, glänzendes Haar",
        ],
        "without": [
            "Neue Wandbilder von Posterlounge",
            "mit meinen Texten und mit meinen Gedanken.",
            "Erforderliche Felder sind mit * markiert.",
        ],
    },
    "https://www.politische-bildung-brandenburg.de/themen/land-und-leute/homo-brandenburgensis": {
        "file": "brandenburg.de.homo-brandenburgensis.html",
        "with": [
            "Stilles Rackern, statt lautem Deklamieren.",
            "Watt jibt’s n hier zu lachen?",
            "Das Brandenbuch. Ein Land in Stichworten.",
        ],
        "without": [
            "Bürgerbeteiligung",
            "Anmelden",
            "Foto: Timur",
            "Schlagworte",
            "Zeilenumbrüche und Absätze werden automatisch erzeugt.",
        ],
    },
    "https://skateboardmsm.de/news/the-captains-quest-2017-contest-auf-schwimmender-miniramp-am-19-august-in-dormagen.html": {
        "file": "skateboardmsm.de.dormhagen.html",
        "with": [
            "Wakebeach 257",
            "Be there or be square!",
            "Hier geht’s zur Facebook Veranstaltung",
            "Blue Tomato präsentiert die dritte",
        ],
        "without": ["More from News", "von Redaktion MSM", "add yours."],
    },
    "https://knowtechie.com/rocket-pass-4-in-rocket-league-brings-with-it-a-new-rally-inspired-car/": {
        "file": "knowtechie.com.rally.html",
        "with": [
            "Rocket Pass 4 will begin at 10:00 a.m. PDT",
            "Let us know down below in the comments",
            "Holy shit, Mortal Kombat 11",
        ],  # title: 'what to do with thousands of crates tho'
        "without": ["Related Topics", "You can keep up with me on Twitter", "Hit the track today with Mario Kart Tour"],
    },
    "https://boingboing.net/2013/07/19/hating-millennials-the-preju.html": {
        "file": "boingboing.net.millenials.html",
        "with": ["Click through for the whole thing.", "The generation we love to dump on"],
        "without": ["GET THE BOING BOING NEWSLETTER", "happy mutants", "Patti Smith and Stewart Copeland"],
    },
    "https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding": {
        "file": "en.wikipedia.org.tsne.html",
        "with": ["Given a set of high-dimensional objects", "Herein a heavy-tailed Student t-distribution"],
        "without": ["Categories:", "Conditional random field"],
    },
    "https://mixed.de/vrodo-deals-vr-taugliches-notebook-fuer-83215-euro-99-cent-leihfilme-bei-amazon-psvr/": {
        "file": "mixed.de.vrodo.html",
        "with": ["Niedlicher Roboter-Spielkamerad: Anki Cozmo", "Empfehlungen von Dennis:"],
        "without": ["Unterstütze unsere Arbeit", "Deepfake-Hollywood", "Avengers", "Katzenschreck"],
    },
    "http://www.spreeblick.com/blog/2006/07/29/aus-aus-alles-vorbei-habeck-macht-die-stahnke/": {
        "file": "spreeblick.com.habeck.html",
        "with": ["Hunderttausende von jungen Paaren", "wie flatterhaft das Mädl ist? :)"],
        "without": ["Malte Welding", "YouTube und die Alten", "Autokorrektur"],
    },
    "https://majkaswelt.com/top-5-fashion-must-haves-2018-werbung/": {
        "file": "majkaswelt.com.fashion.html",
        "with": ["Rüschen und Volants.", "ihr jedes Jahr tragen könnt?", "mein Lieblingskleid vereint"],
        "without": ["Das könnte dich auch interessieren", "Catherine Classic Lac 602"],
    },
    "https://erp-news.info/erp-interview-mit-um-digitale-assistenten-und-kuenstliche-intelligenz-ki/": {
        "file": "erp-news.info.interview.html",
        "with": [
            "Einblicke in die Vision zukünftiger",
            "Frage 4: Welche Rolle spielt Big Data",
            "von The unbelievable Machine Company (*um)",
        ],
        "without": [
            "Matthias Weber ist ERP-Experte mit langjähriger Berufserfahrung.",
            "Die Top 5 digitalen Trends für den Mittelstand",
            "leading edge",
            "Lesen Sie hier einen weiteren",
        ],
    },
    "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/": {
        "file": "github.blog.spiceland.html",
        "with": [
            "Erin Spiceland is a Software Engineer for SpaceX.",
            "make effective plans and goals for the future",
            "looking forward to next?",
            "Research Consultant at Adelard LLP",
        ],
        "without": ["Related posts", "Jeremy Epling", "Missed the main event?", "Privacy"],
    },
    "https://lady50plus.de/2019/06/19/sekre-mystery-bag/": {
        "file": "lady50plus.de.sekre.html",
        "with": [
            "ist eine echte Luxushandtasche",
            "Insgesamt 160 weibliche „Designerinnen“",
            "Sei herzlich gegrüßt",
            "Ein Mann alleine hätte niemals",
            "in den Bann ziehen!",
        ],
        "without": [
            "Erforderliche Felder sind mit",
            "Benachrichtige mich",
            "Reisen ist meine große Leidenschaft",
            "Styling Tipps für Oktober",
        ],
    },
    "https://www.sonntag-sachsen.de/emanuel-scobel-wird-thomanerchor-geschaeftsfuehrer": {
        "file": "sonntag-sachsen.de.emanuel.html",
        "with": ["Neuer Geschäftsführender Leiter", "nach Leipzig wechseln."],
        "without": ["Mehr zum Thema", "Folgen Sie uns auf Facebook und Twitter", "Aktuelle Ausgabe"],
    },
    "https://www.psl.eu/actualites/luniversite-psl-quand-les-grandes-ecoles-font-universite": {
        "file": "psl.eu.luniversite.html",
        "with": ["Le décret n°2019-1130 validant", "restructurant à cet effet »."],
        "without": [" utilise des cookies pour", "En savoir plus", "CNRS, Inserm, Inria."],
    },
    "https://www.chip.de/test/Beef-Maker-von-Aldi-im-Test_154632771.html": {
        "file": "chip.de.beef.html",
        "with": ["Starke Hitze nur in der Mitte", "ca. 35,7×29,4 cm", "Wir sind im Steak-Himmel!"],
        "without": ["Samsung Galaxy S10 128GB", "Für Links auf dieser Seite", "Inga Buller ist Head of Social"],
    },
    "http://www.sauvonsluniversite.fr/spip.php?article8532": {
        "file": "sauvonsluniversite.com.spip.html",
        "with": [
            "L’AG Éducation Île-de-France inter-degrés",
            "Grève et mobilisation pour le climat",
            "suivi.reformes.blanquer@gmail.com",
        ],
        "without": ["Sauvons l’Université !", "La semaine de SLU"],
    },
    "https://www.spiegel.de/spiegel/print/d-161500790.html": {
        "file": "spiegel.de.albtraum.html",
        "with": ["Wie konnte es dazu kommen?", "Die Geschichte beginnt am 26. Oktober", "Es stützt seine Version."],
        "without": [
            "und Vorteile sichern!",
            "Verschickt",
            "Die digitale Welt der Nachrichten.",
            "Vervielfältigung nur mit Genehmigung",
        ],
    },
    "https://lemire.me/blog/2019/08/02/json-parsing-simdjson-vs-json-for-modern-c/": {
        "file": "lemire.me.json.html",
        "author": "Daniel Lemire",
        "title": "JSON parsing: simdjson vs. JSON for Modern C++",
        "date": "2019-08-02",
        "with": ["I use a Skylake processor with GNU GCC 8.3.", "gsoc-2018", "0.091 GB/s", "version 0.2 on vcpkg."],
        "without": ["Leave a Reply", "Science and Technology links", "Proudly powered by WordPress"],
    },
    "https://www.franceculture.fr/emissions/le-journal-des-idees/le-journal-des-idees-emission-du-mardi-14-janvier-2020": {
        "file": "franceculture.fr.idees.html",
        "with": ["Performativité", "Les individus productifs communiquent", "de nos espoirs et de nos désirs."],
        "without": ["A la tribune je monterai", "À découvrir", "Le fil culture"],
    },
    "https://vancouversun.com/technology/microsoft-moves-to-erase-its-carbon-footprint-from-the-atmosphere-in-climate-push/wcm/76e426d9-56de-40ad-9504-18d5101013d2": {
        "file": "vancouversun.com.microsoft.html",
        "with": ["Microsoft Corp said on Thursday", "It was not immediately clear if"],
        "without": ["Reuters files", "turns CO2 into soap", "I consent to receiving"],
        "comments": ["Postmedia is committed"],
    },
    "https://www.ahlen.de/start/aktuelles/aktuelle/information/nachricht/aus-ahlen/reparaturcafe-am-31-januar/": {
        "file": "ahlen.de.reparaturcafe.html",
        "author": "",
        "title": "Reparaturcafé am 31. Januar",
        "date": "2020-01-27",
        "description": "Jede Menge Spaß bereitet es den ehrenamtlichen Experten im Reparaturcafé, wenn sie defekte Hausgeräte wieder flott bekommen. Die regelmäßigen Besucherinnen und Besucher wissen das schon lange. Gelegenheit zu einem Besuch im Reparaturcafé bietet sich am Freitag, 31. Januar, in der Zeit von 15.00 bis 18.00 Uhr in den Räumen des Gruppenergänzenden Dienstes des St. Vinzenz am Park (Kampstraße 13-15).",
        "categories": ["Soziales & Gesundheit"],
        "tags": [],
        "with": [
            "Jede Menge Spaß bereitet es den",
            "Das Projekt ist eine Kooperationsveranstaltung",
            "althausa@stadt.ahlen.de",
        ],
        "without": [
            "Stadtverwaltung Ahlen Rechnungseingang",
            "Internetredaktion Stadt Ahlen",
            "Allgemeine Sprechstunden der Verwaltung",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.travanto.de/ferienhaus/lierfeld/40222/ferienhaus-feinen.php": {
        "file": "travanto.de.ferienhaus-feinen.html",
        "author": "",
        "title": "Ferienhaus Feinen",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Wir haben unser altes Bauernhaus zu einem",
            "Das idyllische Eifeldörfchen Lierfeld liegt",
            "Kinder unter 4 Jahren werden nicht als",
        ],
        "without": ["Travanto Buchungshotline", "tolle Gewinnspiele", " TrustScore 4.2 580 Bewertungen"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://rete-mirabile.net/notizen/15-jahre-rete-mirabile/": {
        "file": "rete-mirabile.net.15jahre.html",
        "author": "Andreas Kalt",
        "title": "15 Jahre rete-mirabile.net",
        "date": "2019-07-28",
        "description": "Diesen Blog gibt es seit 15 Jahren – ein Rückblick.",
        "categories": ["Notizen"],
        "tags": ["reflexion", "blogs", "digitalisierung", "inspiration", "internet"],
        "with": ["Im Trubel des Alltags", "Vor zehn Jahren war Twitter", "Aktuell fallen mir wieder mehr Themen ein"],
        "without": [
            "Deine E-Mail-Adresse wird nicht veröffentlicht",
            "Logo von Jonathas Mello",
            "Gedanken über Lernen und Schule",
        ],
        "comments": ["Vielen Dank für die netten Worte", "Danke für Deine guten", "Ich gehe also davon aus"],
        "license": "CC BY-SA 4.0",
        "region": "DE",
    },
    "https://shop.nmb-media.de/eBay-Template-Datenschutz-Google-Fonts-Fontawesome": {
        "file": "nmb-media.de.ebay.html",
        "author": "",
        "title": "Datenschutztechnische Anpassung der eBay-Verkaufsvorlagen",
        "date": "2018-06-22",
        "description": "eBay-Auktionsvorlagen für JTL Wawi / Eazyauction, Magnalister und Afterbuy.",
        "categories": ["News"],
        "tags": [],
        "with": [
            "Aus datenschutzrechtlichen Gründen wird",
            "Aufgrund der derzeitigen, datenschutzrechtlichen",
            "Die IP-Adressen werden",
        ],
        "without": [
            "Die Beratung zu den von uns angebotenen",
            "Fernwartung nach Absprache per AnyDesk",
            "Bitte laden Sie sich über Ihr ",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://viertausendhertz.de/ddg48/": {
        "file": "viertausendhertz.de.ddg48.html",
        "author": "",
        "title": "Mit Musiker Voodoo Jürgens in Wien",
        "date": "2019-12-16",
        "description": '"Mit Christian Möller ist Musiker David Öllerer aka Voodoo Jürgens durch Wien spaziert – vom Friedhof, wo er selbst mal gearbeitet hat, bis in sein Stammcafé, Gulaschsuppe essen.',
        "categories": [],
        "tags": [],
        "with": ["Im Dialekt zu singen", "Mit seinen Songs über Glücksspiel", "Stammcafé, Gulaschsuppe essen"],
        "without": ["Foto: Ingo Pertramer", "Mehr Episoden anzeigen", "Mit dem Cartoonisten Tobias Vogel in Krefeld"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://www.bibliothek2null.de/2014/05/18/alles-neue-mach-der-mai/": {
        "file": "bibliothek2null.de.mai.html",
        "author": "Patrick Danowski",
        "title": "Alles Neue mach der Mai…",
        "date": "2014-05-18",
        "description": "Innovative Ideen für Bibliotheken,  Freie Inhalte und Interessantes aus dem Web",
        "categories": ["Uncategorized"],
        "tags": ["Uncategorized"],
        "with": ["Nachdem ich mein Blog", "Der Anfang ist gemacht", "Ich hoffe euch gefällt der Relaunch."],
        "without": ["Deine E-Mail-Adresse wird", "bei Informationspraxis- ein neues", "Permalink"],
        "comments": ["ich bin schon ganz gespannt"],
        "license": "CC BY 2.0 DE",
        "region": "DE",
    },
    "http://www.helge.at/2014/03/warum-wien-zu-blod-fur-eine-staufreie-mahu-ist/": {
        "file": "helge.at.mahu.html",
        "author": "Helge Fahrnberger",
        "title": "Warum Wien zu blöd für eine staufreie Mahü ist",
        "date": "2014-03-05",
        "description": "Die &#8220;Krone&#8221; zitiert heute meinen Tweet &#8220;Wien ist zu blöd für eine staufreie Mahü. Muss man so hinnehmen.&#8221; (Hier die Online-Version.) Warum ich glaube, dass Wien (beachte: nicht wie die Krone behauptet &#8220;alle Wiener&#8221;) zu blöd ist für eine staufreie Mariahilfer Straße (oder fast, falls die Abstimmung doch für die Verkehrsberuhigung ausgeht): 1. Die rot-grüne &hellip;",
        "categories": ["Politics"],
        "tags": [],
        "with": [
            "Die “Krone” zitiert heute meinen",
            "die rote Personalvertretung der Wiener Linien",
            "Blöd sind also nicht die Wiener",
        ],
        "without": ["Warum Michel Reimon nach Brüssel muss", "Helge Fahrnberger's personal pages", "Provider information "],
        "comments": ["Es war ein wunderbarer Beschluss"],
        "license": "",
        "region": "AT",
    },
    "http://www.nalas-loewenseiten.info/loewen-lexikon/?letter=M": {
        "file": "nalas-loewenseiten.info.m.html",
        "author": "",
        "title": "M wie Mähnenlöwe",
        "date": "",
        "description": "Nalas LöwenseitenLöwisch gute Unterhaltung wünscht die Nala",
        "categories": ["Lexikon"],
        "tags": [],
        "with": [
            "Nur die Löwenmännchen haben eine",
            "Aber es gibt eben nicht nur diese tollen Schnuckllöwen",
            "Und nicht nur dass, wie Peyton West",
        ],
        "without": ["Nala Löwenkönigin", "Prankentausch", "Lexikon"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://blogoff.de/2015/11/12/i-htm/": {
        "file": "blogoff.de.i-htm.html",
        "author": "",
        "title": "3 verrückte Orte in Berlin",
        "date": "2015-11-12",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["In Berlin lebe ich nun", "Vielen Dank an die S-Bahn", "Base Flying"],
        "without": ["I ♥ BLOG OFF!", "Was passiert hier eigentlich noch?", "powdered by wordpress"],
        "comments": [],
        "license": "CC BY-NC-SA 2.0 DE",
        "region": "DE",
    },
    "https://de.globalvoices.org/2019/04/30/ein-jahr-voller-proteste-nicaraguaner-wollen-nicht-mehr-nur-den-rucktritt-ortegas-sondern-einen-neuanfang/": {
        "file": "de.globalvoices.org.nicaragua.html",
        "author": "Elisa Marvena",
        "title": "Ein Jahr voller Proteste: Nicaraguaner wollen nicht mehr nur den Rücktritt Ortegas, sondern einen Neuanfang",
        "date": "2019-04-30",
        "description": "[Wir müssen] Autoritarismus, Sexismus, Alleinherrschaft einzelner und andere Übel, die in die politische Kultur dieses Landes Einzug gehalten haben, beseitigen.",
        "categories": [
            "Lateinamerika",
            "Nicaragua",
            "Bürgermedien",
            "Kriege & Konflikte",
            "Meinungsfreiheit",
            "Menschenrechte",
            "Politik",
            "Protest",
        ],
        "tags": [],
        "with": [
            "Seit dem Ausbruch der Massenproteste gegen",
            "Laut der niedrigsten Schätzung",
            "Ich sah, wie eine Freundin von der Universität",
        ],
        "without": ["@globalvoices verdient einen Preis für die", "Italiano", "Name (Pflichtfeld)"],
        "comments": [],
        "license": "CC BY 3.0",
        "region": "DE",
    },
    "http://www.heiko-adams.de/laufen-im-winter-von-baeh-zu-yeah-in-12-monaten/": {
        "file": "heiko-adams.de.laufen.html",
        "author": "Heiko",
        "title": "Laufen im Winter: Von „bäh!“ zu „yeah!“ in 12 Monaten.",
        "date": "2019-02-10",
        "description": "",
        "categories": ["Privat", "Sport"],
        "tags": ["dunkel", "Dunkelheit", "Laufen", "Running", "Training", "Winter"],
        "with": ["Heute, 12 Monate später,", "das gefällt mir 😉"],
        "without": ["Einfach laufen lassen", "Heiko's Activity"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.wbf.admin.ch/wbf/de/home/dokumentation/nsb-news_list.msg-id-14093.html": {
        "file": "wbf.admin.ch.14093.html",
        "author": "",
        "title": "",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["beim SP-Städtegipfel", "Dies führt dazu, dass die Sozialpolitik", "wie in der Nationalhymne,"],
        "without": ["Kommunikationsdienst", "Letzte Änderung", "Informiert bleiben"],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html": {
        "file": "faz.net.streaming.html",
        "author": "Benjamin Fischer und Marcus Theurer",
        "title": "Nutzerbasierte Abrechnung: Musik-Stars fordern neues Streaming-Modell",
        "date": "2020-01-28",
        "description": "Die Abogebühr eines Nutzers soll nur noch unter den Künstlern verteilt werden, die er gehört hat, so das Ziel der Initiative. Dabei gehe es auch um „kulturelle Vielfalt“. Welche Chancen hat diese Forderung?",
        "categories": [],
        "tags": [],
        "with": ["„Die Liste der Künstler", "nicht bloß um höhere Einkünfte", "Der Wandel der Musikbranche"],
        "without": [
            "Etwa 100 deutsche Reisende",
            "Abonnieren Sie unsere",
            "Joe Kaeser deutet vage",
            "Redakteur in der Wirtschaft.",
        ],
        "comments": ["keinen Bock auf solche Buchhalter", "Verklagt eure Labels", "Zur Verdeutlichung ein Extrembeispiel:"],
        "license": "",
        "region": "DE",
    },
    "https://www.toptal.com/python/top-10-mistakes-that-python-programmers-make": {
        "file": "toptal.com.python.html",
        "author": "",
        "title": "",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "and code reuse.",
            "bar is optional",
            "What the $%#!&??",
            "And you then tried to do",
            "Familiarizing oneself with the key",
        ],
        "without": ["Martin has worked as", "delivered weekly.", "MCMC Methods:"],
        "comments": ["for common mistake #6", "This is a fairer comparison", "I liked the article."],
        "license": "",
        "region": "",
    },
    "https://www.reddit.com/r/Python/comments/1bbbwk/whats_your_opinion_on_what_to_include_in_init_py/": {
        "file": "reddit.com.init.html",
        "author": "",
        "title": "",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Considering a package", "Import key functions", "EDIT: Thanks a lot"],
        "without": ["news about the dynamic", "All rights reserved", "I see your minesweeper"],
        "comments": ["I do similar things.", "from foo.bar import x, y, z", "IMO it makes things"],
        "license": "",
        "region": "",
    },
    "http://wir-empfehlen.info/?p=3289": {
        "file": "wir-empfehlen.info.3289.html",
        "author": "Support Team",
        "title": "Truckwash A31",
        "date": "2020-01-03",
        "description": "Seit Anfang 2019 stehen wir mit vier großzügig angelegten Waschstraßen für die LKW Reinigung mit motiviertem Personal in Rhede direkt an der A31 zur Verfügung, um Sie von unserem guten Waschergebnis zu überzeugen. Für Spezialfahrzeuge (incl. Viehtransportern) steht sogar an 24/7 eine SB Waschstraße zur Verfügung. Truckwash A31 Ottostraße 1426899 Rhede /Ems Tel.: +49 4964 95816-120Fax: +49 4964 95816-29",
        "categories": [],
        "tags": [],
        "with": ["Seit Anfang 2019 stehen wir", "Ottostraße 14", " Für Spezialfahrzeuge (incl. Viehtransportern)"],
        "without": ["Deine E-Mail-Adresse wird", "Sei der Erste dem dies gefällt.", "Top Kunden Bewertungen"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.reisen-mit-dem-internet.de/europa/deutschland/niedersachsen/ostfriesland/emden-21416": {
        "file": "reisen-mit-dem-internet.de.emden-21416.html",
        "author": "",
        "title": "Emden",
        "date": "",
        "description": "Emden Sehenswürdigkeiten - lohnende Ziele und Locations, Kurzportraits, Fotos und Informationen, Lage Google Maps, Wikipedia Verweise, Weblinks,",
        "categories": ["Emden"],
        "tags": ["Best of Travel", "Fahrradtour", "Historischer Stadtkern", "Länder & Sitten", "Michael Müller Verlag"],
        "with": ["Emden ist vor allem in Deutschland", "Die Kunsthalle in Emden wurde 1986", "Erwachsene: 3 € (Preis 2019) "],
        "without": ["Quellen und Inspiration: u.a. wikipedia.org", "Infos zum Reiseziel"],
        "comments": ["© 2004 - 2020 Volker Pohl"],
        "license": "CC BY-SA 3.0",
        "region": "",
    },
    "https://nextkabinett.wordpress.com/2014/01/17/derek-jarman-%c2%b7-the-garden/": {
        "file": "nextkabinett.wordpress.com.garden.html",
        "author": "",
        "title": "Derek Jarman · The Garden",
        "date": "2014-01-17",
        "description": "The Garden · Derek Jarman (1990) A nearly wordless visual narrative intercuts two main stories and a couple of minor ones. A woman, perhaps the Madonna, brings forth her baby to a cro…",
        "categories": ["Allgemein"],
        "tags": ["The Garden", "Derek Jarman"],
        "with": ["The Garden · Derek Jarman (1990)", "A nearly wordless visual narrative", "Loose in this contemporary world"],
        "without": ["Büro der Social Secretary", "Kommentar verfassen", "@EwigeSommerzeit Danke für den Link"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://sprechblase.wordpress.com/2019/11/17/elektro-zapfsaeulen/": {
        "file": "sprechblase.wordpress.com.zapfsaeulen.html",
        "author": "Cem Basman",
        "title": "Elektro-Zapfsäulen.",
        "date": "2019-11-17",
        "description": "Ich würde ja in smarte und wirtschaftliche Elektro-Zapfsäulen investieren. Wundere mich, dass es sie noch nicht konkurenzfähig mit Drumrum und Service gibt. Ich bedanke mich für die Tipp-Provjon vo…",
        "categories": [],
        "tags": ["Elektro", "Micro-Series Entrepreneurs", "Zapfsäulen"],
        "with": ["Ich würde ja", "Drumrum und Service", "Ich bedanke mich"],
        "without": ["Life is not digital", "Bewerten:", "Micro-Series: Born Entrepreneurs"],
        "comments": [],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "",
    },
    "https://creeny.wordpress.com/2020/01/24/nebelsuppe-6/": {
        "file": "creeny.wordpress.com.nebelsuppe.html",
        "author": "Creeny",
        "title": "Nebelsuppe.",
        "date": "2020-01-24",
        "description": "1. Ich glaube, heute möchte ich mal nicht um halb neun auf der Couch einnicken :D . 2. Pommes esse ich am liebsten mit den Fingern. 3. Das Dschungelcamp bei RTL habe ich in diesem Jahr nicht geguck…",
        "categories": ["Schönes…", "Das Leben", "Blogprojekte"],
        "tags": [],
        "with": ["1. Ich glaube, heute möchte", "Glücksmomente finden sich", "leckeren Flammkuchen, morgen"],
        "without": ["Was ich liebe... ♥", "Wortspuren hinterlassen", "♥ Glücksmomente"],
        "comments": [],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "",
    },
    "https://nurmeinstandpunkt.wordpress.com/2020/01/23/blogposting-01-23-2020/": {
        "file": "nurmeinstandpunkt.wordpress.com.blogposting.html",
        "author": "Christian Spließ",
        "title": "Blogposting 01/23/2020",
        "date": "2020-01-23",
        "description": "Presseförderung: Studie zweifelt an Stütze vom Staat via Horizont Gewalt im Netz &#8211; Schuldzuweisung statt Opferschutz via netzpolitik.org Künstliche Intelligenz &#8211; EU erwägt Verbot von Ge…",
        "categories": ["Allgemeines"],
        "tags": [],
        "with": ["Presseförderung: Studie zweifelt an Stütze vom Staat", "via netzpolitik.org", "via t3n News"],
        "without": ["Hier könnte Ihre Meinung stehen", "Ein Fehler ist aufgetaucht", "Es heißt SOCIAL Media"],
        "comments": [],
        "license": "CC BY-NC-SA 2.0 DE",
        "region": "DE",
    },
    "https://flowfx.de/blog/copy-paste-from-tmux-to-system-clipboard/": {
        "file": "flowfx.de.tmux.html",
        "author": "Florian Posdziech",
        "title": "Copy & paste from tmux to system clipboard",
        "date": "2020-01-16",
        "description": "For the first time in many years I am using a Linux machine for my work. In general I am extremely pleased with the system I've set up. But of course, there are things that don't &quot;just work&quot;. Like... ",
        "categories": [],
        "tags": [],
        "with": ["or the first time in many years", "As usual, StackOverflow", "set-option -s set"],
        "without": ["Next post", "All content is licensed", "Powered by Nikola"],
        "comments": [],
        "license": "CC BY 4.0",
        "region": "",
    },
    "https://wiki.piratenpartei.de/HE:Kassel/Stammtisch": {
        "file": "wiki.piratenpartei.de.stammtisch.html",
        "author": "",
        "title": "HE:Kassel/Stammtisch",
        "date": "2020-01-29",
        "description": "",
        "categories": ["Stammtisch in Hessen"],
        "tags": [],
        "with": ["Der nächste Stammtisch", "Mittwoch des Monats", "Die Protokolle der Stammtische"],
        "without": ["Diese Seite wurde zuletzt", "Werkzeuge", "Benutzerkonto erstellen"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://gnadlib.wordpress.com/2020/01/05/scherenschnitt-3/": {
        "file": "gnadlib.wordpress.com.scherenschnitt.html",
        "author": "gnaddrig",
        "title": "Scherenschnitt (3)",
        "date": "2020-01-05",
        "description": "Die Stadt steht schwarz und schweiget&#8230; Angefangen hatte es mit",
        "categories": ["Canon Powershot S110", "Fotografie"],
        "tags": ["Abendhimmel", "Gegenlicht", "Silhouette"],
        "with": ["Die Stadt steht schwarz", "Für den von der Kamera", "besser geworden…"],
        "without": ["Auf gnaddrig ad libitum gibt", "Ob dieser Hinweis nötig", "Haftungsbeschränkung für externe Links"],
        "comments": ["Beide Bilder sind toll!", "ohne Kondensstreifen fehlt was", "Der helle „Stern“ müsste die Venus sein"],
        "license": "",
        "region": "",
    },
    "http://www.buero-hoppe.de/baumgutachten.htm": {
        "file": "buero-hoppe.de.baumgutachten.html",
        "author": "",
        "title": "Baumgutachten",
        "date": "2006-12-16",
        "description": "&Uuml;bersicht: Baumgutachten, Baumkataster, Baumbeschreibungen",
        "categories": [],
        "tags": [],
        "with": [
            "Die Erstellung von Baumgutachten",
            "Es gibt eine Vielzahl von Gründen",
            "Baumkataster eine sinnvolle Investition.",
        ],
        "without": ["Um unsere Webseite für Sie", "Leistungen und Informationen im", "Planungsbüro G. & L. Hoppe"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.spontis.de/schwarze-szene/liebe-leser-bitte-rutschen-sie-nicht-in-das-neue-jahrzehnt/": {
        "file": "spontis.de.jahrzehnt.html",
        "author": "Robert",
        "title": "Liebe Leser, bitte rutschen Sie nicht in das neue Jahrzehnt!",
        "date": "2019-12-31",
        "description": "Wieso eigentlich einen guten Rutsch wünschen? Ist das nicht gehässig? Spekuliert das nicht möglicherweise darauf, das sich der gemeine Grufti bei den",
        "categories": [],
        "tags": ["2019", "Jahreswechsel", "Sylvester"],
        "with": ["Wieso eigentlich einen guten", "Das Lithium-Ionen Akku", "Sie das neue Jahrzehnt"],
        "without": ["Wizard of Goth", "Nossi: Belgien: Porta Nigra", "Soziale Netzwerke"],
        "comments": ["Lieber Robert, danke", "Wie so oft, triffst", "Siegeszug der Computer"],
        "license": "CC BY-SA 3.0",
        "region": "DE",
    },
    "https://www.schneems.com/2018/10/09/pair-with-me-rubocop-cop-that-detects-duplicate-array-allocations/": {
        "file": "schneems.com.rubocop.html",
        "author": "",
        "title": "Pair With Me: Rubocop Cop that Detects Duplicate Array Allocations",
        "date": "2018-10-09",
        "description": "You might know rubocop as the linter that helps enforce your code styles, but did you know you can use it to make your code faster? In this post, we’ll look ...",
        "categories": [],
        "tags": [],
        "with": ["You might know rubocop", "You can use this code:", "While it might not"],
        "without": ["Join the hundreds of developers", "I maintain an internal-facing", "Today I have an unusual proposition"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://hackernoon.com/how-to-scrape-google-with-python-bo7d2tal": {
        "file": "hackernoon.com.scrape.html",
        "author": "",
        "title": "How To Scrape Google With Python",
        "date": "2019-12-29",
        "description": "Ever since Google Web Search API deprecation in 2011, I've been searching for an alternative. I need a way to get links from Google search into my Python script. So I made my own, and here is a quick guide on scraping Google searches with requests and Beautiful Soup.",
        "categories": [],
        "tags": [
            "Google Search",
            "Web Scraping",
            "Python",
            "Search Engine",
            "Datascraping",
            "Data Scraping",
            "Data Science",
            "Data",
        ],
        "with": ["There are also some caveats", "Ever since Google Web", "Making the request is"],
        "without": ["Hackernoon Newsletter curates", "Comments", "Creating Search Engine API"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.colours-of-the-soul.alhelm.net": {
        "file": "colours-of-the-soul.alhelm.net.html",
        "author": "",
        "title": "trnd-Projekt “G Data InternetSecurity 2009”",
        "date": "2009-02-18",
        "description": "",
        "categories": ["trnd-Projekte"],
        "tags": ["Antivirus", "Projekt", "Test", "trnd"],
        "with": ["Einen Paralel-Scan", "1 Projektfahrplan-Broschüre", "Aber es gibt noch den Sinn"],
        "without": ["ein Buch-Gewinn", "Dann würde ich mich darüber "],
        "comments": ["Dankeschön für die Blümchen", "Liebe Ines, Danke", "so langes Blogschweigen?"],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "DE",
    },
    "https://lernpfadprismen.wordpress.com/masse/masse-des-quaders/": {
        "file": "lernpfadprismen.wordpress.com.masse.html",
        "author": "",
        "title": "Masse des Quaders",
        "date": "2015-12-07",
        "description": "Die Masse eines Körpers berechnest du, indem du das Volumen (V) mit der Dichte (ρ) multiplizierst. Siehe Kapitel Masse! Bevor du die Beispiele löst, schau dir die Videos mit den Erklärungen an.   A…",
        "categories": [],
        "tags": [],
        "with": ["Die Masse eines Körpers", "Lösung: m = 210 g", "Vollständig durchgerechnete Lösung"],
        "without": ["Bloggen auf WordPress.com", "Dieser Lernpfad ist", "Didaktischer Kommentar"],
        "comments": [],
        "license": "CC BY-NC-ND 4.0",
        "region": "",
    },
    "https://grossefragen.wordpress.com/2019/03/13/wuerde-des-lebens-ein-projekt/": {
        "file": "grossefragen.wordpress.com.projekt.html",
        "author": "Michael Veeser-Dombrowski",
        "title": "Würde des Lebens – ein Projekt",
        "date": "2019-03-13",
        "description": "Dieses Thema eignet sich gut für hoch individualisiertes Lernen und die Unterrichtsmethode „bloggen“.  Um den Anspruch nicht zu hoch zu schrauben, gibt es  dazwischen vier Anregungen: Hinweise zu e…",
        "categories": [],
        "tags": [],
        "with": ["Dieses Thema eignet", "Dabei gelten ein paar wichtige", "=> Wie hast Du gelernt?"],
        "without": ["Unterrichtsideen und die Bilder", "für erfolgreiches Lernen", "142 Antworten zu"],
        "comments": ["Die meisten Flüchtlinge kamen", "Sind Todesstrafen moralisch vertretbar", "Wünschen zu gestalten"],
        "license": "CC BY 4.0",
        "region": "",
    },
    "https://2gewinnt.wordpress.com/uber-uns/": {
        "file": "2gewinnt.wordpress.com.uns.html",
        "author": "",
        "title": "Über uns",
        "date": "2012-06-30",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Künstlerischer Lebenslauf", "Finalist bei der ORF-Show", "100 Folgen von"],
        "without": ["Sei der Erste dem dies gefällt.", "Gefällt mir", "Gipfelpunkt der Geschmacklosigkeit"],
        "comments": ["Hey ihr beiden!"],
        "license": "",
        "region": "",
    },
    "https://knowledge-on-air.de/2019/12/17/koa039-live-vom-knowledgecamp-2019/": {
        "file": "knowledge-on-air.de.koa039.html",
        "author": "Simon Dückert",
        "title": "KOA039 Live vom KnowledgeCamp 2019",
        "date": "2019-12-17",
        "description": "",
        "categories": ["Podcast"],
        "tags": ["berlin", "gkc19"],
        "with": ["Auch auf dem KnowledgeCamp 2019", "vom Camp erzählen", "die über ihre Eindrücke"],
        "without": ["Scholarch der Cogneon", "Sei der Erste dem dies gefällt", "Dieser Eintrag wurde veröffentlicht"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://campino2k.de/2016/02/28/uberspace-und-lets-encrypt/": {
        "file": "campino2k.de.uberspace.html",
        "author": "Chris Jung",
        "title": "Uberspace und Let’s Encrypt",
        "date": "2016-02-28",
        "description": "",
        "categories": ["Internet", "Projekte"],
        "tags": ["HTTPS", "ssl", "Uberspace"],
        "with": ["Nachdem bei Uberspace jetzt", "Die Anpassung der entsprechenden", "bei Projekten mit WordPress"],
        "without": ["Hier schreibt Christian", "Das könnte Sie auch interessieren"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.coopbuddy.de/games/bee-simulator/": {
        "file": "coopbuddy.de.bee.html",
        "author": "",
        "title": "Bee Simulator",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Entdecke die großen Abenteuer", "Bee Simulator Mehrspieler", "Koop und Splitscreen-Modus"],
        "without": ["Dieses Kommentarformular steht", "Splitscreen Coop", "Wenn ja, auf welcher Plattform?"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://www.silvias.net/blog/wahlzensur-angriff-auf-universitaeten/": {
        "file": "silvias.net.wahlzensur.html",
        "author": "Silvia Jura",
        "title": "Wahlzensur: Angriff auf Universitäten",
        "date": "2018-10-26",
        "description": "",
        "categories": ["politics"],
        "tags": ["elenão", "fascismonobrasil", "wahlen2018"],
        "with": ["Am 25. Oktober gab es", "Der Oberste Wahlgerichtshof", "Até agora tiveram"],
        "without": ["alle inhalte @silviajura", "CAPTCHA Code", "Primavera feminista em Viena"],
        "comments": ["Dankeschön für die Blümchen", "Liebe Ines, Danke", "so langes Blogschweigen?"],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "DE",
    },
    "https://wolfsrebellen-netz.forumieren.com/t7-forums-regeln": {
        "file": "wolfsrebellen-netz.forumieren.com.regeln.html",
        "author": "lupa",
        "title": "Forums-Regeln",
        "date": "2013-10-26",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Wir pflegen hier ein sehr freundschaftliches", "Grafik, besonders der eigenen", "gez. Admin lupa"],
        "without": [
            "Einen Missbrauch melden",
            "Widerruf des Lebensversicherungsvertrags vor oder nach",
            "Sie sind nicht verbunden",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.alexander-klier.net/zeitenkompetenz/zeitphilosophie/": {
        "file": "alexander-klier.net.zeitphilosophie.html",
        "author": "Alexander Klier",
        "title": "Zeitphilosophie",
        "date": "2012-06-08",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Es ist nicht zu wenig Zeit", "Dieses tiefsitzende Kulturmuster", "Im Rahmen des Tutzinger"],
        "without": ["Gib Deine E-Mail-Adresse", "Diese Seite steht grundsätzlich", "Alexander bei MOOCs – Ein Selbstversuch"],
        "comments": [],
        "license": "CC-BY-SA",
        "region": "",
    },
    "http://www.villacc.de/ferienvilla/119/Villa-Galaxy": {
        "file": "villacc.de.galaxy.html",
        "author": "",
        "title": "Villa Galaxy",
        "date": "",
        "description": "Villa Galaxy  - Ein Luxus-Ferienhaus mit 4.5 Schlafzimmern und 3.5 Badezimmern in Florida. Gönnen Sie sich für Ihren Urlaub ein Ferienhaus mit privatem Pool unter der Sonne Floridas.",
        "categories": [],
        "tags": [],
        "with": ["In Cape Coral gibt", "Pool verwendet Salzelektrolyse", "Jede weitere Person: US $ 100,00"],
        "without": ["oder berechnen Sie die Kosten", "+49 8670 986823", "LVCC ist Ihr Partner für die"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.chorknaben-ulm.de/geschichte.html": {
        "file": "chorknaben-ulm.de.geschichte.html",
        "author": "",
        "title": "Chorgeschichte",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["1968 bis heute Knabenmusik", "Der Chor wird durch den 1978", "973 übernahm der damals"],
        "without": ["Seit 50 Jahren sind wir", "Leitung: Thomas Stang", "Impressum & Datenschutz"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://resonator-podcast.de/2019/res158-kathrin-goebel/": {
        "file": "resonator-podcast.de.res158.html",
        "author": "",
        "title": "RES158 Sternfusion am Teilchenbeschleuniger",
        "date": "2019-08-16",
        "description": "",
        "categories": [],
        "tags": ["Astronomie", "Astrophysik", "Sterne", "Sonnensystem", "GSI", "Beschleuniger", "Physik"],
        "with": ["Kathrin Göbel (Twitter) ist", "Veröffentlicht am 16.08.2019", "Und bitte entschuldigt den Helium-Fehler "],
        "without": ["Mit diesem Button kannst Du", "Der Resonator-Podcast von Holger", "Etwa alle zwei Wochen erscheint "],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://bunterepublik.wordpress.com/2017/06/12/keine-spiel-talstrasse-zur-bunten-republik-neustadt/": {
        "file": "bunterepublik.wordpress.com.talstrasse.html",
        "author": "gizzmo",
        "title": "Keine Spiel-Talstraße zur Bunten Republik Neustadt",
        "date": "2017-06-12",
        "description": "Zur Bunten Republik Neustadt 2017 wird es keine Kinder und Kulturinsel auf der Talstraße geben. Das für die Anmeldung zuständige Orgateam sah sich wegen den seit 2016 geltenden Konditionen und dem …",
        "categories": ["Aktuelles"],
        "tags": ["2017", "brn", "Inseln", "koordinieren", "Organisation", "Spiel-Talstraße", "Spielstraße", "Talstrasse"],
        "with": [
            "Zur Bunten Republik Neustadt 2017",
            "Zur Bunten Republik Neustadt 2017",
            "Zur Bunten Republik Neustadt 2017",
        ],
        "without": ["Abgelegt unter Aktuelles", "Der Inhalt dieser Seite steht", "Bloggen auf WordPress.com"],
        "comments": [],
        "license": "CC BY-SA 3.0 DE",
        "region": "",
    },
    "https://murdeltas.wordpress.com/2015/04/05/barcamp-graz-2015-politcamp-call-for-action/": {
        "file": "murdeltas.wordpress.com.politcamp.html",
        "author": "marc",
        "title": "Barcamp Graz 2015 – Politcamp Call for Action",
        "date": "2015-04-05",
        "description": "In nicht mehr ganz 2 Wochen ist es soweit: das Barcamp Graz 2015 steht vor der Tür &#8211; 17-19 April an der FH Joanneum! Es werden wieder interessierte und interessante Menschen zusammenkommen, d…",
        "categories": ["bunt gemischt", "freie kultur", "politik", "veranstaltung"],
        "tags": [],
        "with": ["Leute, die in Zukunft das Barcamp", "Ein Zeichen dieser Veränderung", "In nicht mehr ganz 2 Wochen"],
        "without": ["Ich bin ein linker Webterrorist", "Flattr this:", "Dieses Blog steht unter"],
        "comments": [],
        "license": "CC BY 3.0 AT",
        "region": "AT",
    },
    "https://herrpfleger.de/2019/10/new-balance-fuelcell-echo-bringt-speed/": {
        "file": "herrpfleger.de.fuelcell.html",
        "author": "Matthias",
        "title": "New Balance: FuelCell Echo bringt Speed",
        "date": "2019-10-01",
        "description": "Die FuelCell-Familie von New Balance nimmt mit dem FuelCell Echo ein neues schnelles und stylisches Mitglied in seine Produktfamilie auf. Bei der FuelCell-Technologie von New Balance handelt es sich&#8230;",
        "categories": ["Lifestyle", "Sport"],
        "tags": ["FuelCell", "Laufen", "Laufschuh", "New Balance", "Running"],
        "with": ["Die FuelCell-Familie", "Das Retro-Design ist auf", "Mehr Infos auch auf der"],
        "without": ["Medizinstudent, Papa, (ehemaliger)", "Über den Autor", "Schreib einen Kommentar"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://andreabottlinger.wordpress.com/2019/12/26/arent-we-all/": {
        "file": "andreabottlinger.wordpress.com.arent.html",
        "author": "Andrea",
        "title": "Aren’t we all …?",
        "date": "2019-12-26",
        "description": "Es wird Zeit, dass ich hier auch etwas dazu schreibe: Wir machen ein Spiel! Es heißt &#8222;Aren&#8217;t we all &#8230;?&#8220;, und es ist ein Visual Novel. Das heißt, man klickt sich durch Dialog…",
        "categories": ["Allgemein"],
        "tags": [],
        "with": ["Es wird Zeit, dass ich", "Und damit möchte ich auch", "Mitstreiter Bug gebastelt"],
        "without": ["Um neue Beiträge per E-Mail", "Einem Blogger gefällt dies", "Twitter hat nicht geantwortet"],
        "comments": [],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "",
    },
    "http://www.jan-grosser.de/art/385_xum1541_dateien_zwischen_linux.html": {
        "file": "jan-grosser.de.xum1541.html",
        "author": "",
        "title": "XUM1541: Dateien zwischen Linux und C64 austauschen",
        "date": "2016-01-31",
        "description": "Fertiger XUM1541-Adapter zum Anschluß eines Commodore Disketten-Laufwerks über USB Es gibt verschiedene Möglichkeiten, Dateien zwischen einem über 30",
        "categories": ["Hardware"],
        "tags": ["linux", "c64", "retro", "1541", "diskette"],
        "with": ["Es gibt verschiedene Möglichkeiten", "Die Hardware für den XUM1541", "Das Innenleben des Gehäuses"],
        "without": ["If not explicitly specified otherwise", "cat /dev/brain/ideas >> blog"],
        "comments": [],
        "license": "CC BY 2.0",
        "region": "DE",
    },
    "https://together.ch/de/karriere/events-messen/119-sprungbrett-event-schaffhausen": {
        "file": "together.ch.schaffhausen.html",
        "author": "",
        "title": "Sprungbrett-Event Schaffhausen",
        "date": "",
        "description": "Vom Industrieunternehmen bis hin zum Hightech Betrieb: In Schaffhausen sind Firmen mit Top Angeboten zu Hause. Weltkonzerne wie ABB, Garmin, Georg Fischer (GF),",
        "categories": [],
        "tags": [],
        "with": ["für eine erfolgreiche Zukunft!", "In einer lockeren Atmosphäre", "Anreise"],
        "without": ["Abonniere unseren Newsletter", "Partner für Studium", "Für Hochschulen"],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "http://www.hr-innovation.org/hr-innovation-einer-enterprise-2-0/": {
        "file": "hr-innovation.org.enterprise.html",
        "author": "",
        "title": "Enterprise 2.0",
        "date": "",
        "description": "HR Innovation in einer Enterprise 2.0 – Herausforderungen und Chancen der Personalabteilungen HR wird zukünftig nur auf Augenhöhe wahrgenommen, wenn es Innovationen fördert und selbst innovativ wird. Clayton M. Christensen (US-amerikanischer Wirtschaftswissenschaftler; Forschungsschwerpunkt: Innovation in Unternehmen; Veröffentlichung: The Innovator’s Dilemma (1997)) zeigt in seinen Untersuchungen, warum großartige Unternehmen im Wettbewerb um Innovationen versagen, obwohl sie &hellip;",
        "categories": [],
        "tags": [],
        "with": ["Clayton M. Christensen", "You can’t solve a problem", "Nur zu selten tritt"],
        "without": ["Copyright © 2020", "Geben Sie Ihre E-Mail", "Initiative zur Entwicklung"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://aktion-hummelschutz.de/biologie/tote-hummeln-unter-linden/": {
        "file": "aktion-hummelschutz.de.hummeln.html",
        "author": "",
        "title": "Tote Hummeln unter Linden",
        "date": "2017-08-09",
        "description": "Warum findet man im Sommer so viele tote Hummeln? Lösung: Die Insekten&hellip; Continue reading &ldquo;Tote Hummeln unter Linden&rdquo;&hellip;",
        "categories": ["Biologie & Wissenschaft"],
        "tags": [],
        "with": ["Normalerweise leben Hummeln", "Das Sterben tritt zur Blütezeit", "Baal T, Denke B, Mühlen"],
        "without": ["War der Artikel nützlich?", "Holen Sie sich meinen", "Möchten Sie den Artikel teilen?"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.pix-bavaria.de/": {
        "file": "pix-bavaria.de.html",
        "author": "",
        "title": "pix-bavaria",
        "date": "",
        "description": "Startseite",
        "categories": [],
        "tags": [],
        "with": ["Alle Fotos sind in Auflösungen", "in der Web-Galerie von", "Jede andere Art der Bildnutzung"],
        "without": ["Erstellt mit Piwigo", "Kontakt zu pix-bavaria"],
        "comments": [],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "DE",
    },
    "http://www.singapur-reiseinfo.de/Reise-ABC/reise-abc.html": {
        "file": "singapur-reiseinfo.de.abc.html",
        "author": "",
        "title": "Reise ABC für Singapur",
        "date": "",
        "description": "Reise ABC Singapur mit Tipps zur Reisevorbereitung und günstigen Reiseangeboten",
        "categories": [],
        "tags": [],
        "with": ["Reiseinformationen durch das", "Einfuhrverbot: Waffen. Munition", "SARS kann bei Wiederauftreten"],
        "without": ["Über 45.000 Ferienhäuser", "Die folgenden Hotel Links"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://www.einfachspanien.de/malaga-die-quirlige-metropole-in-andalusien.html": {
        "file": "einfachspanien.de.malaga.html",
        "author": "",
        "title": "Malaga, die quirlige Metropole in Andalusien",
        "date": "2011-11-22",
        "description": "Spanien hat als Reiseland eine Menge zu bieten. Ob nun die Inselgruppen der Balearen oder auch Kanaren, so gut wie",
        "categories": ["Allgemein"],
        "tags": [],
        "with": ["Spanien hat als Reiseland", "Wer Malaga nicht nur", "Einfluss auf die Freundlichkeit"],
        "without": ["Keine Kommentare for", "Wussten Sie schon...?", "Warning: Creating default object"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://anwaltniemeyer.de/index.html": {
        "file": "anwaltniemeyer.de.index.html",
        "author": "",
        "title": "Willkommen!",
        "date": "",
        "description": "Rechtsanwalt Jens-Christof Niemeyer ist im Internetrecht/IT-Recht, Zivil- und Familienrecht sowie Verkehrsrecht bundesweit tätig.",
        "categories": [],
        "tags": [],
        "with": ["Ich bin Jens-Christof", "Ich freue mich", "und mittelständischen Unternehmen"],
        "without": ["Fachanwalt für IT-Recht", "9, 32130 Enger", "Service"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.vinosytapas.de/wein/herkunft/spanien/d_o_ca_-rioja/": {
        "file": "vinosytapas.de.rioja.html",
        "author": "",
        "title": "D.O.Ca. Rioja, Spanien",
        "date": "2020-02-11",
        "description": "Alle Weine aus D.O.Ca. Rioja, Spanien,",
        "categories": [],
        "tags": [],
        "with": ["Die Bestimmungen der D.O.Ca.", "Für die Qualitätsstufen der Weine", "Mindestlagerzeit Rotwein"],
        "without": [
            "Es werden die Weine 1 bis 10 von insgesamt 19 angezeigt!",
            "Ihr Warenkorb ist leer",
            "Patanegra-Schinken aus ",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://prof-pc.de/": {
        "file": "prof-pc.de.html",
        "author": "Benni",
        "title": "Time to say goodbye.",
        "date": "2017-09-10",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Liebe_r Besucher_in", "Doch seitdem ist viel Zeit", "Thanks for All the Fish"],
        "without": ["Datenschutzerklärung"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://mobilsicher.de/aktuelles/apple-kippt-verschluesselungsplaene-fuer-icloud": {
        "file": "mobilsicher.de.icloud.html",
        "author": "Miriam Ruhenstroth",
        "title": "Apple kippt Verschlüsselungspläne für iCloud",
        "date": "2020-01-23",
        "description": "Apple hat seine Pläne aufgegeben, Backup-Daten in der iCloud so zu verschlüsseln, dass selbst Apple sie nicht mehr lesen könnte.",
        "categories": ["News"],
        "tags": [],
        "with": ["Medienberichten zufolge hat", "Anders sieht es bei den Daten aus", "Was dabei erstaunlich wenig Beachtung"],
        "without": ["Wie Apple welche Daten", "30.01.2020 Wieso Updates?", "Weitere Artikel"],
        "comments": [],
        "license": "CC BY-ND 3.0 DE",
        "region": "DE",
    },
    "http://www.maescot.de/kleine-schafskunde/": {
        "file": "maescot.de.schafskunde.html",
        "author": "Jonathan Krase",
        "title": "Kleine Schafskunde",
        "date": "",
        "description": "Mäscot Schaf, Standardausführung, weiß: Das Exemplar an Schaf, das sich in Massen auf der großen, grünen Wiese herumtreibt. Ganz nach dem Schafklischee, sind sie alle ein bisschen beschränkt, ängstlich und naiv.",
        "categories": [],
        "tags": [],
        "with": ["Schaf, Standardausführung, weiß", "Bei diesem arroganten Schafweibchen", "Eine Intellektuelle, die"],
        "without": ["Der Webcomic mit den niedlichen Schafen", "© 2009-2012 Jonathan Krase", "…und anderem Web 2.0 Gedöns."],
        "comments": [],
        "license": "CC BY-NC-ND 3.0",
        "region": "DE",
    },
    "https://www.lavazza.de/de/kaffee/gemahlener-kaffee/qualita-oro-250-g.html": {
        "file": "lavazza.de.qualita.html",
        "author": "",
        "title": "Qualità Oro - Perfect Symphony, 250g Dose",
        "date": "",
        "description": "Probieren Sie Lavazza Qualità Oro, die Lavazza-Mischung für alle, die jeden Tag einen guten Kaffee genießen möchten. Finden Sie es auf der Lavazza-Website.",
        "categories": [],
        "tags": [],
        "with": [
            "Qualità Oro war die erste Lavazza-Mischung",
            "Jede Mischung wird meisterhaft zusammengestellt",
            "Fruchtige und florale Noten",
        ],
        "without": ["Die Lieferung ist für Sie kostenlos", "Bitte teilen Sie uns Ihre Erfahrungen", "Heute empfehlen wir"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://gnaur.wordpress.com/2013/06/14/die-moglichkeit-nichts-zu-tun-ist-auch-eine-moglichkeit/": {
        "file": "gnaur.wordpress.com.moglichkeit.html",
        "author": "",
        "title": "Die Möglichkeit nichts zu tun ist auch eine Möglichkeit",
        "date": "2013-06-14",
        "description": "&#8222;Ich weiß ich bin betrunken und sollte das vielleicht nicht sagen&#8230;&#8220; &#8211; &#8222;Dann sag es nicht&#8220; &#8211; &#8222;Ok.&#8220;",
        "categories": ["Spezifisch"],
        "tags": [],
        "with": ["„Ich weiß ich bin", "– „Ok.“", "sollte das vielleich"],
        "without": ["Kommentar verfassen", "Die Inhalte dieser Website sind", "Kategorien"],
        "comments": [],
        "license": "CC BY-NC-ND 2.0 DE",
        "region": "",
    },
    "http://www.seelenradio.de/nummer-zwei-leo/": {
        "file": "seelenradio.de.leo.html",
        "author": "",
        "title": "Nummer zwei: Leo",
        "date": "2015-08-03",
        "description": "",
        "categories": ["ziemlich privat"],
        "tags": [],
        "with": ["Es ist schon einige Zeit", "=)", "So sah es aus"],
        "without": ["seelenradio is powered by", "Say your words", "No Response so far"],
        "comments": [],
        "license": "CC BY-NC-SA 2.5 CN",
        "region": "DE",
    },
    "https://www.rheinruhronline.de/essen/essen2/essenwestviertel/essenwestviertel.htm": {
        "file": "rheinruhronline.de.essenwestviertel.html",
        "author": "",
        "title": "Essen-Westviertel",
        "date": "",
        "description": "Das Westviertel ist ein Stadtteil von Essen. Es liegt in unmittelbarer N&auml;he zum Stadtkern und bildet zusammen mit dem S&uuml;dviertel, dem Nordviertel, dem Ostviertel, dem S&uuml;dostviertel und dem Stadtk...",
        "categories": [],
        "tags": [],
        "with": ["Essen-Westviertel Ehemaliges Press- und", "geringe Wohnbebauung auf", "Colosseum Theater Essen"],
        "without": ["- Anzeige-", "Nützliche Apps und Services"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://www.hertha-blog.de/der-lange-und-die-alte-dame.html": {
        "file": "hertha-blog.de.dame.html",
        "author": "Daniel",
        "title": "Der Lange und die alte Dame",
        "date": "2017-07-23",
        "description": "In diesem Sommer war Michael Preetz ganz vorne mit dabei. Kaum hatte die Liga auch offiziell ihren Meister gekürt, präsentierte der Manager des Berliner",
        "categories": ["Hertha BSC"],
        "tags": ["Michael Preetz"],
        "with": ["In diesem Sommer war Michael Preetz", "Zeit als Spieler noch", "die Entscheidung für Dardai"],
        "without": [
            "Drei Berliner kommentieren ihre Erlebniss",
            "“Hertha? Ist das dein Ernst?”",
            "Beliebte Beiträge zum Thema:",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://www.echte-demokratie-jetzt.de/blog/": {
        "file": "echte-demokratie-jetzt.de.blog.html",
        "author": "uriebe",
        "title": "Liebe Menschen Europas",
        "date": "2014-01-13",
        "description": "",
        "categories": ["Allgemein"],
        "tags": [],
        "with": ["Liebe Menschen Europas", "Dieses Werk bzw. Inhalt", "Αγαπητέ λαέ της Ευρώπης"],
        "without": ["von anderen", "Du hörst es oft.", "Eine Filmempfehlung für die"],
        "comments": [],
        "license": "CC BY-NC-ND 3.0",
        "region": "DE",
    },
    "https://gizmeo.eu/makrophotos-von-insekten/": {
        "file": "gizmeo.eu.insekten.html",
        "author": "c1ph4",
        "title": "Makrophotos von Insekten",
        "date": "2020-01-22",
        "description": "",
        "categories": ["Artwork", "Handy & Smartphone", "Photo"],
        "tags": ["insekten", "makrophotos"],
        "with": ["Alle seine Photos entstanden", "Eine Ameise in einer Bar!", "Echt schön bzw. bitte"],
        "without": ["Relevantes aus dem gizmeo.eu-Archiv:", "keine Ahnung mehr wie es...", "© 2010-2020 gizmeo.eu"],
        "comments": [],
        "license": "CC BY-SA 3.0 DE",
        "region": "",
    },
    "https://alexanderlasch.wordpress.com/2019/11/14/was-das-christkind-und-native-americans-gemeinsam-haben-oder-warum-wir-sprachgeschichte-brauchen/": {
        "file": "alexanderlasch.wordpress.com.sprachgeschichte.html",
        "author": "Alexander Lasch",
        "title": "Was das Christkind und Native Americans gemeinsam haben (oder warum wir Sprachgeschichte brauchen)",
        "date": "2019-11-14",
        "description": "An dieser und anderer Stelle habe ich vor kurzem das Projekt #DigitalHerrnhut aufgerissen – das ist auf den ersten Blick ein Thema für Religionslinguistik und Sprachgeschichte und ohne besonderen G…",
        "categories": ["Forschung", "Projekte", "Sprachpunkt"],
        "tags": ["Digital", "Herrnhut", "Sprache und Religion", "Sprachgeschichte"],
        "with": ["Wenn man sich heutzutage", "An dieser und anderer Stelle", "Genau dieses Bild ruft die AfD"],
        "without": ["Es gibt noch keine Kommentare.", "Das setzt das Verständnis voraus", "Alle Artikel und Inhalte"],
        "comments": [],
        "license": "CC BY-SA 4.0",
        "region": "",
    },
    "https://www.pamelaandersonfoundation.org/news/2018/12/4/yellow-vests-and-i": {
        "file": "pamelaandersonfoundation.org.yellow.html",
        "author": "Pamela Anderson",
        "title": "Yellow Vests and I",
        "date": "2018-12-04",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["I am glad that the media", "Lots of media see Yellow Vests", "Moralising about burned"],
        "without": ["John Bitove, Chair Priszm Brandz", "January 2020", "Oct 9, 2019"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.dbjr.de/artikel/bundespraesident-wuerdigte-das-ehrenamtliche-engagement/": {
        "file": "dbjr.de.bundespraesident.html",
        "author": "",
        "title": "Bundespräsident würdigte das ehrenamtliche Engagement",
        "date": "2020-01-23",
        "description": "",
        "categories": ["Jugendverbände", "Ehrenamt"],
        "tags": [],
        "with": ["Steinmeier lädt jedes Jahr", "Zum Empfang kamen", "Er bat darum"],
        "without": ["10178 Berlin", "Themen: Ehrenamt Jugendverbände", "Datenschutz"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://achtundvierzig.hypotheses.org/822": {
        "file": "achtundvierzig.hypotheses.org.822.html",
        "author": "karstenruppert",
        "title": "Tagung: Institutionen revolutionärer Macht in den europäischen Revolutionen der ersten Hälfte des 19. Jahrhunderts (26. und 27. 2. 2015, Eichstätt)",
        "date": "2015-01-28",
        "description": "Das DFG-Projekt „Edition der Akten der Provisorischen Zentralgewalt“ veranstaltet am 26. und 27. Februar 2015 im Bischöflichen Seminar Eichstätt die Tagung „Institutionen revolutionärer Macht in den europäischen Revolutionen der ersten Hälfte des 19. Jahrhunderts“. Auf der Tagung werden die exekutiven Institutionen der Revolutionen in der Hochzeit der europäischen Umwälzungen behandelt. Neben dem Prototyp, dem Wohlfahrtsausschuss &hellip; Tagung: Institutionen revolutionärer Macht in den europäischen Revolutionen der ersten Hälfte des 19. Jahrhunderts (26. und 27. 2. 2015, Eichstätt) weiterlesen &rarr;",
        "categories": ["Artikel", "Unsere Forschung", "Veranstaltungen"],
        "tags": ["Institutionen revolutionärer Macht", "Provisorische Zentralgewalt", "Regierungen", "Tagung"],
        "with": ["Das DFG-Projekt „Edition der Akten", "Kulturgeschichte des Politischen", "eine zeitliche Konzentration"],
        "without": [
            "Vorheriger Beitrag",
            "Deine E-Mail-Adresse wird nicht veröffentlicht.",
            "Diese Website verwendet Akismet",
        ],
        "comments": [],
        "license": "CC BY 3.0",
        "region": "",
    },
    "http://bayrische-bembel.de/bbr/modules/news/article.php?storyid=504": {
        "file": "bayrische-bembel.de.504.html",
        "author": "Cooper",
        "title": "Eintracht Frankfurt stellt Weichen für die Zukunft",
        "date": "2015-08-25",
        "description": "",
        "categories": ["Eintracht Presse"],
        "tags": [],
        "with": [
            "Axel Hellmann übernimmt die",
            "Der Vorsitzende des Aufsichtsrat Wolfgang",
            "Saisonende bei Heribert Bruchhagen.",
        ],
        "without": ["Hier geht es zur neuen Vorstandsstruktur", "Nur für Bembel-Mitglieder", "Besucher sind online"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://ethify.org/content/vegetarier-zu-sein-bedarf-trend-oder-eigene-entscheidung": {
        "file": "ethify.org.vegetarier.html",
        "author": "Margarita Koreneva",
        "title": "Vegetarier zu sein. Bedarf, Trend oder eigene Entscheidung?",
        "date": "2019-07-07",
        "description": "",
        "categories": [],
        "tags": ["Markt", "Selbstbestimmung"],
        "with": ["Vegetarier zu sein. Bedarf, Trend", "In Österreich sind momentan", "vor 5 Jahren fast keine"],
        "without": ["Wachstum im Wandel", "Mit unserem Newsletter", "communities 2010 - 2020"],
        "comments": [],
        "license": "CC BY-SA 4.0",
        "region": "",
    },
    "https://disfunctions.de/tutorials/podcasts-in-plex-einbinden/": {
        "file": "disfunctions.de.podcasts.html",
        "author": "Fabian",
        "title": "Podcasts in Plex einbinden",
        "date": "2014-05-06",
        "description": "",
        "categories": ["debianforum", "Linux", "Tutorials", "Ubuntu", "ubuntuusers.de"],
        "tags": [],
        "with": ["Ich benutze jetzt seit längerem", "filename=$1", "DOWNLOAD_DIRECTORY"],
        "without": [
            "Erstellt am Dienstag 6. Mai 2014",
            "Das Blog der gnadenlosen Fehlfunktionen!",
            "Design von Andreas Viklund",
        ],
        "comments": [],
        "license": "CC BY-SA 3.0 DE",
        "region": "DE",
    },
    "https://von-der-see.de/design/": {
        "file": "von-der-see.de.design.html",
        "author": "",
        "title": "Design",
        "date": "",
        "description": "Profitiere von jahrelanger Erfahrung, fundierter Fachkenntnis und großer Expertise im Bereich Design der Agentur VON DER SEE. Wir helfen wirklich weiter.",
        "categories": [],
        "tags": [],
        "with": ["Ein professionelles und seriös", "Design geht aber auch weit", "zahlreiche Bereiche zuverlässig ab"],
        "without": ["Wenn Sie uns per Kontaktformular Anfragen", "Der Upstalsboom-Weg", "Interessantes aus unserem"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://archiv.krimiblog.de/?p=2895": {
        "file": "archiv.krimiblog.de.2895.html",
        "author": "Krimiblogger",
        "title": "Das vermutlich schwulste Musikvideo der Welt",
        "date": "2009-08-06",
        "description": "",
        "categories": ["Aus dem Alltag", "Bilderberg", "Schöne Töne"],
        "tags": ["Christopher Dallman", "Joshua Pohja", "Kevin R. Thomspon", "Musik", "schwul"],
        "with": ["Okay, hat wieder nichts mit", "Ergänzung 2: Glaubt man", "Ergänzung 1: Den Text des Songs"],
        "without": ["Leider sind keine Kommentare möglich.", "Rasterfahndung", "Dies ist das Archiv von krimiblog.de"],
        "comments": ["Hamburg feiert CSD. Vielleicht"],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "DE",
    },
    "https://journal.3960.org/posts/2019-12-22-firefox-weniger-werbung-mehr-speed-unter-android/": {
        "file": "journal.3960.org.firefox.html",
        "author": "Frank Boës",
        "title": "Firefox – Weniger Werbung, mehr Speed unter Android",
        "date": "2019-12-22",
        "description": "Werbung nervt. Tracking nervt. Nerven nervt. Und gerade mobil habe ich eigentlich keine Zeit, meine geringe Download-Rate mit dem Herunterladen von hässlichen…",
        "categories": [" Programmierung"],
        "tags": ["Für Tumblr", "Geckobar", "Review", "Technologie", "Webdevelop", "Adblocker"],
        "with": [
            "Werbung nervt. Tracking nervt. Nerven nervt.",
            "Von seinem Vorgänger unterscheidet",
            "nicht von mir benutzter Dienst",
        ],
        "without": [
            "Zurück zur Übersichtsseite",
            "Merkwürdige Erlebnisse, spontane Einfälle",
            'Artikel mit dem Tag "Für Tumblr"',
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://beyssonmanagement.com/2014/07/15/was-ist-innovation/": {
        "file": "beyssonmanagement.com.innovation.html",
        "author": "Guido Beyß",
        "title": "Was ist Innovation?",
        "date": "2014-07-15",
        "description": "Am 14. Juni 2005 hielt Steve Jobs eine vielbeachtete Rede vor den Absolventen der Stanford University. Den Zuhörern erzählte er drei Geschichten, die für sein Leben wichtig waren. “The first story …",
        "categories": ["Innovation"],
        "tags": ["David Brier", "Innovation", "Rafa Galeano", "Steve Jobs"],
        "with": [
            "Am 14. Juni 2005 hielt Steve Jobs",
            "David Brier, international anerkannter",
            "Ein hilfreicher kleiner Film",
        ],
        "without": [
            "Bitte geben Sie Ihre E-Mail-Adresse ein",
            "Dieser Eintrag wurde veröffentlicht in",
            "Kommentar verfassen",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://damianduchamps.wordpress.com/2019/08/03/office-365-hbdi-die-dritte/": {
        "file": "damianduchamps.wordpress.com.hbdi.html",
        "author": "damianduchamps",
        "title": "Office 365 – HBDI – die Dritte",
        "date": "2019-08-03",
        "description": "Es bleibt weiterhin spannend, was die Zulässigkeit einer Nutzung von Office 365 durch Schulen angeht. Nachdem der Hessische Beauftragte für Datenschutz und Informationsfreiheit am 09.07.2019 zunäch…",
        "categories": [],
        "tags": ["Datenschutz", "Office 365", "Schule"],
        "with": ["Es bleibt weiterhin spannend", "Auch Schulen, die nicht unter 1", "Wie letzteres umzusetzen ist, dafür"],
        "without": ["Erstelle eine kostenlose Website oder Blog", "Um neue Beiträge per E-Mail zu", "Kommentar verfassen"],
        "comments": [
            "Vielen Dank für alle die guten Beiträge",
            "bestehenden Probleme zu bereinigen",
            "dies auch thematisiert werden sollte.",
        ],
        "license": "CC BY 3.0 DE",
        "region": "",
    },
    "https://sladisworld.wordpress.com/2019/12/10/was-wurde-eigentlich-aus-six-sigma/": {
        "file": "sladisworld.wordpress.com.sigma.html",
        "author": "freeman1984",
        "title": "Was wurde eigentlich aus Six Sigma?",
        "date": "2019-12-10",
        "description": "Qualität war bei Führungskräften mal groß in Mode. Wie es dazu kam, was der Hype bewirkte und welche Nebenwirkungen er hatte, erläutert der Management-Kenner Alfred Kieser. Interview: Jens Bergmann…",
        "categories": ["Uncategorized"],
        "tags": [],
        "with": ["Herr Kieser, ältere Menschen erinnern sich", "Was war der zweite Grund?", "Man muss das nüchtern sehen"],
        "without": ["Enter your email address to follow", "Bloggen auf WordPress.com.", "…through the looking glass…"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.haenselblatt.com/chinese-money-plant-info": {
        "file": "haenselblatt.com.chinese.html",
        "author": "",
        "title": "Chinese Money Plant Info: Erfahren Sie, wie man eine Pilea-Pflanze anbaut",
        "date": "",
        "description": "Die chinesische Geldpflanze ist eine schöne, einzigartige und einfach zu züchtende Zimmerpflanze.  Langsam zu vermehren und erst seit kurzem weltweit bekannt, ist es das größte Hindernis für den Anbau dieser Pflanze, einen zu finden.  Erfahren Sie mehr über die Pflanze und ihre Pflege hier.",
        "categories": ["Zimmerpflanzen"],
        "tags": [],
        "with": [
            "Was ist eine chinesische Geldanlage?",
            "Pilea Pflanzenpflege ist relativ minimal",
            "Langsam zu vermehren und erst",
        ],
        "without": [
            "Spinat kann mit einer Reihe von Krankheiten, vor allem",
            "Ich bin ein billiger Gärtner.",
            "Haben Sie schon einmal darüber nachgedacht",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.regiolanda.de/content/149-filmbuero-goettingen": {
        "file": "regiolanda.de.filmbuero.html",
        "author": "Sven Schreivogel",
        "title": "Filmbüro Göttingen",
        "date": "",
        "description": "Filmbüro Göttingen",
        "categories": [],
        "tags": [],
        "with": [
            "Göttingen war in den 1950er Jahren",
            "Bedeutend für den Standort waren neben Ateliergesellschaf",
            "die Schließung des Instituts für den Wissenschaftlichen Film",
        ],
        "without": ["An der Aue 1", " Warenkorb", "2018 Regiolanda "],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.piratenpartei-marburg.de/2019/09/21/wir-unterstuetzen-fridays-for-future/": {
        "file": "piratenpartei-marburg.de.fridays.html",
        "author": "flerche",
        "title": "Wir unterstützen Fridays for Future",
        "date": "2019-09-21",
        "description": "Diese Seite war gestern nicht erreichbar, und wir waren auf der Alle-fürs-Klima-Demo in Marburg präsent. Es war eine großartige Veranstaltung mit ca. 8000&hellip;",
        "categories": [],
        "tags": ["#nichtMeinErbe", "#AlleFuersKlima"],
        "with": [
            "Die Ignoranz, mit der die Dringlichkeit tiefgreifender Änderungen",
            "Diese Seite war gestern nicht erreichbar",
            "Die Ignoranz, mit der die Dringlichkeit",
        ],
        "without": ["Klarmachen zum Ändern!", "Von allein wird es nicht besser!", "Copyright © 2020 Piratenpartei"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.piratenpartei.at/volksbegehren-zum-bedingungslosen-grundeinkommen-bge/": {
        "file": "piratenpartei.at.grundeinkommen.html",
        "author": "Harald Bauer",
        "title": "Volksbegehren zum Bedingungslosen Grundeinkommen (BGE)!",
        "date": "2019-11-17",
        "description": "Aktuell liegt beim Innenministerium ein Volksbegehren für ein Bedingungsloses Grundeinkommen in der Höhe von 1200 € für alle österreichischen",
        "categories": ["Blogposts", "News", "Slider", "Uncategorized"],
        "tags": ["Bedingungsloses Grundeinkommen", "BGE", "Österreich", "Piraten", "Piratenpartei", "ppat", "Volksbegehren"],
        "with": [
            "Aktuell liegt beim Innenministerium ein Volksbegehren",
            "Jetzt wäre der richtige Zeitpunkt",
            "Durch die aktuelle wirtschaftliche Hochlage ",
        ],
        "without": ["Please reload CAPTCHA.", "Theme based on the great work", "Getaggt mit"],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.dobszay.ch/2016-04-15/was-ist-der-unterschied-zwischen-privaten-und-staatlichen-geheimdiensten/": {
        "file": "dobszay.ch.geheimdiensten.html",
        "author": "LD",
        "title": "Was ist der Unterschied zwischen privaten und staatlichen Geheimdiensten?",
        "date": "2016-04-15",
        "description": "",
        "categories": [],
        "tags": [
            "Datenschutz und Sicherheit",
            "Web/Internet",
            "Apple",
            "Facebook",
            "Geheimdienste",
            "Google",
            "Microsoft",
            "Samsung",
            "Twitter",
            "Überwachung",
        ],
        "with": [
            "Die massenmediale Berichterstattung",
            "Seit vor allem das FBI Druck auf die Anbieter macht",
            "„Bellende Hunde beissen nicht“ ",
        ],
        "without": ["Stichwort-Wolke", "einige Rechte vorbehalten", "Neueste Beiträge"],
        "comments": [],
        "license": "CC BY-SA 2.5 CH",
        "region": "CH",
    },
    "https://www.unsere-zeitung.at/2020/02/02/ist-die-inklusion-im-kapitalismus-umsetzbar/": {
        "file": "unsere-zeitung.at.inklusion.html",
        "author": "Alexander Roll",
        "title": "Ist die Inklusion im Kapitalismus umsetzbar?",
        "date": "2020-02-02",
        "description": "Der Mensch braucht soziale Verbindungen. Die heutige Gesellschaft ist jedoch geprägt von Isolierung und Vereinsamung von Teilen der Gesellschaft.",
        "categories": [],
        "tags": ["Inklusion", "Kapitalismus"],
        "with": [
            "Soziales Netzwerk, Sozialraumorientierung, Inklusion",
            "Hohe Bedeutung von sozialen",
            "Menschen mit Behinderung, ist im Bereich",
        ],
        "without": [
            "Abonniere unseren Newsletter",
            "Alle Kooperationspartner von Unsere Zeitung auf einem Blick",
            "Verein „Unsere Zeitung – Die Demokratische.“",
        ],
        "comments": ["Wenns nur der Kapitalismus alleine wäre …"],
        "license": "",
        "region": "AT",
    },
    "http://www.sprechwaisen.com/sw082-82-gruende-zum-weiter-hoeren/": {
        "file": "sprechwaisen.com.sw082.html",
        "author": "Realiberry",  # unterschrieben als Heiko
        "title": "SW082 – 82 Gründe zum weiter hören",
        "date": "2019-07-21",
        "description": "Ingo hat ja gesagt, er habe diesen Text nicht geschrieben. Dennoch steht das jetzt da. Als wäre das geplant gewesen. Aber wozu? Nur damit jetzt Petra einen Text verfasst über dem Ingos Name steht u…",
        "categories": [],
        "tags": [],
        "with": ["Ingo hat ja gesagt", "Oder damit Petra", "Äußert Vermutungen"],
        "without": ["Deine E-Mail-Adresse", "Der geheimnisvolle Button", "This entry was posted "],
        "comments": [
            "Schöne Folge. Hab mich gefreut.",
            "da haste wohl rescht wa?",
            "Trotzdem mal wieder eine sehr kurzweilige",
        ],
        "license": "",
        "region": "",
    },
    "https://www.unterwegsinberlin.de/radtouren-berlin/radtour-durch-friedrichsfelde-karlshorst-und-schoeneweide/": {
        "file": "unterwegsinberlin.de.friedrichsfelde.html",
        "author": "Tine",
        "title": "Radtour durch Friedrichsfelde, Karlshorst und Schöneweide",
        "date": "2020-02-02",
        "description": "Spoiler-Alarm: Meine neue Lieblings-Radtour in Berlin. Viele Jahre war ja die Müggelsee-Runde tatsächlich meine Lieblings-Radtour, das hat sich nun aber geändert.",
        "categories": ["Radtouren Berlin"],
        "tags": ["berlin", "fahrradtour", "friedrichsfelde", "karlshorst", "lichtenberg", "radtour", "schöneweide"],
        "with": ["Meine neue Lieblings-Radtour", "ca. 80 m links", "um das Gelände herum"],
        "without": ["Klicken Sie auf den unteren", "Keine Lust alleine zu", "Kein Fahrrad zur Hand?"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.strafprozess.ch/rasende-polizisten/": {
        "file": "strafprozess.ch.polizisten.html",
        "author": "",
        "title": "Rasende Polizisten",
        "date": "2020-02-04",
        "description": "Auch Polizisten im Dienst können den Rasertatbestand (Art. 90 Abs. 3 und 4 SVG) erfüllen, wenn sie mitten in der Nacht mit über 120 km/h durch ein Wohngebiet (signalisierte Höchstgeschwindigkeit: 50 km/h) jagen. Das Bundesgericht kassiert ein Urteil des Kantonsgerichts GE (BGer 6B_1224/2019 vom 24.01.2020, Fünferbesetzung), das den fehlbaren Polizeibeamten nur wegen Art. 90 Abs. &hellip;",
        "categories": ["Bundesgericht", "BGer", "SVG", "Vorsatz"],
        "tags": ["StGB 12", "SVG 100", "SVG 90"],
        "with": ["Auch Polizisten im Dienst", "Das Bundesgericht kassiert", "signalisierte Höchstgeschwindigkeit"],
        "without": ["Ege/Heimgartner/Niggli (Hrsg.)", "Drucken etc.", "10. Dreiländerforum in Bregenz"],
        "comments": [],
        "license": "CC BY 4.0",
        "region": "CH",
    },
    "https://www.rent-a-salesman.eu/den-vertrieb-auslagern-anders-als-andere-oder-gut-zu-wissen": {
        "file": "rent-a-salesman.eu.auslagern.html",
        "author": "Bernhard Sgoda",
        "title": "Gut zu Wissen",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Einen Vertriebsmitarbeiter ohne", "Wir wollen auch Provisionen", "Keine Excel-Sheets - sondern"],
        "without": ["RENT A SALESMAN®", "Blog - Tag Cloud"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://wolfgangschmale.eu/abgebrochene-forschung-eine-neue-studie-von-heinz-duchhardt/": {
        "file": "wolfgangschmale.eu.duchhardt.html",
        "author": "Wolfgang Schmale",
        "title": "„Abgebrochene Forschung“ – Eine neue Studie von Heinz Duchhardt",
        "date": "2020-02-10",
        "description": "Heinz Duchhardt hat in seiner neuesten Studie ein heikles Thema aufgegriffen. Es geht um zweite Bände in der Geschichtswissenschaft, die nie erschienen sind.",
        "categories": [],
        "tags": [
            "Abgebrochene Forschung",
            "Georg von Below",
            "Gerhard Ritter",
            "Geschichtswissenschaft",
            "Heinz Duchhardt",
            "Martin Göhring",
            "Rudolf Smend",
        ],
        "with": [
            "[1] Wer im Wissenschaftsbetrieb würde",
            "Band zwei alsbald folgen zu lassen",
            "[8] Historiker oder Geschichte als Fach",
        ],
        "without": ["Wenn Sie diesen Blogeintrag kommentieren", "Diese Website verwendet Akismet", "Neueste Kommentare"],
        "comments": ["Danke für die schöne Zusammenfassung!"],
        "license": "",
        "region": "",
    },
    "https://netzfueralle.blog.rosalux.de/2019/10/30/netzpolitik-als-us-wahlkampfthema/": {
        "file": "netzfueralle.blog.rosalux.de.netzpolitik.html",
        "author": "",
        "title": "Netzpolitik als US-Wahlkampfthema",
        "date": "2019-10-30",
        "description": "",
        "categories": ["FOSS", "Überwachung", "Wem gehört das Netz", "Wie das Internet Politik verändert"],
        "tags": ["Eigentum", "Facebook", "Open Source"],
        "with": ["Radikal-reformistischer Vorschlag", "I am a capitalist. Come on", "Was die Problemwahrnehmung angeht"],
        "without": [
            "Vorstudie zur Menüerweiterung durch FOSS-Produkte bei der RLS",
            "Smarte Worte",
            "Netz für Alle bei Facebook",
        ],
        "comments": [],
        "license": "CC BY-NC-SA 3.0 DE",
        "region": "DE",
    },
    "http://www.creativecommons.ch/wie-funktionierts/": {
        "file": "creativecommons.ch.wie.html",
        "author": "",
        "title": "",
        "date": "2014-03-17",
        "description": "Creative Commons Team Switzerland",
        "categories": [],
        "tags": [],
        "with": ["Sie können selber bestimmen", "Die Bedeutungen der Lizenzen", "Der durchgestrichene Dollar bedeutet"],
        "without": ["Sofern nicht anders ausgewiesen", "Designed by Elegant Themes"],
        "comments": [],
        "license": "CC BY 4.0",
        "region": "CH",
    },
    "https://arsnova.thm.de/blog/frag-jetzt/": {
        "file": "arsnova.thm.de.frag.html",
        "author": "Klaus Quibeldey-Cirkel",
        "title": "»frag.jetzt«",
        "date": "2019-06-28",
        "description": "ARSnova is a novel approach to Audience Response Systems (ARS), hence its Latin name. ARSnova is Open Source and offered as Software-as-a-Service free of charge.",
        "categories": ["Blog"],
        "tags": ["Blog"],
        "with": ["live moderierbar", "einen Workshop an", "im Hörsaal Fragen"],
        "without": ["ARSnova-Workshop an der Uni Wien", "wird nicht veröffentlicht", "Technische Hochschule Mittelhessen"],
        "comments": [],
        "license": "CC BY-SA 4.0",
        "region": "DE",
    },
    "https://www.anchor.ch/gesellschaft/ein-tag-aus-dem-leben-eines-taugenichts-oder-die-leute-von-sri-lanka/": {
        "file": "anchor.ch.lanka.html",
        "author": "Peter Addor",
        "title": "Ein Tag aus dem Leben eines Taugenichts oder die Leute von Sri Lanka",
        "date": "2019-12-22",
        "description": "Es ist sechs Uhr früh und noch stockdunkel. Vom nahen Kloster dringen die monotonen Gebetsgesänge der buddhistischen Priester in meine Ohren. Für mich ist es die reinste Kakophonie. Und bestimmt ko…",
        "categories": ["Gesellschaft", "Länder", "Menschen", "Sri Lanka"],
        "tags": ["Alltag", "Religionen", "Sri Lanka", "Tiere"],
        "with": [
            "Es ist sechs Uhr früh und noch stockdunkel",
            "führen diese improvisierten Tüten aus Schülernotizen.",
            "Kumara kennt mich recht gut",
        ],
        "without": [
            "Deine E-Mail-Adresse wird nicht veröffentlicht",
            "Blog via E-Mail abonnieren",
            "Peter Addor ist Mathematiker, Systemdenke",
        ],
        "comments": ["wunderbarer Text, Danke!", "Danke Peter für den interessanten Bericht!", "lieber Martin"],
        "license": "CC BY-NC 4.0",
        "region": "CH",
    },
    "https://www.ejwue.de/aktuell/news/faire-lieferketten/": {
        "file": "ejwue.de.lieferketten.html",
        "author": "Eberhard Fuhr",
        "title": "Faire Lieferketten",
        "date": "2020-02-05",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Deshalb lädt der EJW-Weltdienst zusammen",
            "Das Evangelische Jugendwerk in Württemberg",
            "koordiniert, fördert und gestaltet",
        ],
        "without": ["Haeberlinstraße 1-3", "Kontaktieren Sie uns gerne auch direkt", "kalte Welt herein leuchten"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://pinup-fashion.de/korsetts-shops-designer-online-kaufen/": {
        "file": "pinup-fashion.de.korsetts.html",
        "author": "",
        "title": "Korsetts – Shops, Designer, online kaufen",
        "date": "",  # 2011/12
        "description": "Korsetts sind für Pin Up Girls so etwas wie Wasser für Delphine: Ohne geht es nur ganz kurz. Egal ob man es nun als klassisches Vintage Dessous trägt oder ein auffälliges Burlesque Outfit daraus zaubert: Die Teile sind einfach nur sexy und sehr talentiert. Eine schmale Taille &hellip; Weiterlesen &rarr;",
        "categories": [],
        "tags": [],
        "with": [
            "Korsetts sind für Pin Up Girls so etwas wie Wasser",
            "och was macht den Unterschied beim Korsettkauf",
            "Wem Shapewear ab sofort nicht edel",
        ],
        "without": [
            "Wer einen Rockabilly Shop oder einen",
            "Auf Pinup-Fashion findet man tolle Mode",
            "Viel Spaß beim Stöbern",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://thebigbone.wordpress.com/2017/04/13/die-ueberforderung-durch-ueberangebote/": {
        "file": "thebigbone.wordpress.com.ueberforderung.html",
        "author": "www.koffergepackt.com",
        "title": "Die Überforderung durch Überangebote",
        "date": "2017-04-13",
        "description": "Überangebot überfordert uns immer mehr Bist du auch schon mal die Regale im Supermarkt abgelaufen und hast dich gewundert über die acht Meter H-Milch-Regale und die gefühlten 300 Packungen Müsli. O…",
        "categories": ["Allgemein", "Essen und Trinken", "Gesellschaft", "Kommentare", "Lifestyle"],
        "tags": [
            "Überangebot",
            "Überforderung",
            "überfordert",
            "Burnout",
            "Entschleunigung",
            "Entschleunigung im Alltag",
            "gesellschaft",
            "ich kann mich nicht entscheiden",
            "Kommunikationsmittel",
            "psychologie",
            "richtige Entscheidungen treffen",
            "richtige Wahl treffen",
            "soziale medien",
            "Supermarkt",
        ],
        "with": [
            "Bist du auch schon mal die Regale im Supermarkt",
            "Wir sind die Opfer einer Gesellschaft",
            "Die Beschleunigung im Privaten liegt",
        ],
        "without": ["Gib deine E-Mail-Adresse ein", "Kommentare zu", "Ähnliche Beiträge"],
        "comments": ["So wahr!", "Toller Text – spannendes Thema"],
        "license": "",
        "region": "",
    },
    "https://ritinardo.wordpress.com/2017/11/26/bundesregierung-2017-btw17-groko/": {
        "file": "ritinardo.wordpress.com.btw17.html",
        "author": "tlow",
        "title": "Bundesregierung 2017 #btw17 #groko",
        "date": "2017-11-26",
        "description": "t Wenn man so hört und liest, was nach den Bundestagswahlen so geschrieben wurde und wird. Und wenn auch nach den Sondierungen und ggf. vor einer Neuauflage der großen Koalition, finde ich diese Di…",
        "categories": [],
        "tags": ["btw17", "Bundestagswahl"],
        "with": ["Wenn man so hört und liest", "Deutschland ist ein Land", "SPD und FDP haben dieses mal vieles"],
        "without": [
            "Erstelle eine kostenlose Website oder Blog",
            "Teilen Sie dies mit:",
            "Fall #Amani, was passiert denn da? #aboutyouawards",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://ohneq.de/ohneq/johannes/": {
        "file": "ohneq.de.johannes.html",
        "author": "Johannes Wolf",
        "title": "Johannes",
        "date": "",
        "description": "Hi! Mein Name ist Johannes aka ohneQ. Mir macht es sehr viel Spaß, Podcasts zu produzieren. Meine Freunde und ich stecken viel Liebe und Geld in die Herstellung dieser Podcasts. Wir freuen uns, die In",
        "categories": [],
        "tags": [],
        "with": [
            "Mein Name ist Johannes aka ohneQ",
            "teile unsere Beiträge auf Facebook oder Twitter",
            "wenn Dir unsere Podcasts gefallen",
        ],
        "without": ["(c) Johannes Wolf", "Neueste Beiträge", "Akte Aurora"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://shabka.org/about-us/": {
        "file": "shabka.org.about.html",
        "author": "",
        "title": "The strategic Think & Do Tank",
        "date": "2018-06-07",
        "description": "The strategic Think &amp; Do Tank Foreign, security and development policy &amp; analyses. Crisis management and civil society engagement. All in one network. Where do we originate from? Shabka was founded in 2013 as a publication network focused on the Arab world by young journalists and academics. One of its early major projects, a book &hellip;  About Us Read More &raquo;",
        "categories": [],
        "tags": [],
        "with": [
            "The Future Strategists Hub 2018 was Shabka’s",
            "on several levels as well as supra-instutional",
            "One of the book project’s key",
        ],
        "without": ["© Shabka 2019", "Contact"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.parallels.com/products/desktop/": {
        "file": "parallels.com.desktop.html",
        "author": "",
        "title": "Parallels Desktop 15 for Mac",
        "date": "2020-02-03",
        "description": "The #1 choice of Mac® users to Run Windows on Mac without Rebooting! Easy to Get Started. Instant Download. Try Free Today!",
        "categories": [],
        "tags": [],
        "with": ["Quickly move files, apps and more", "#1 choice of Mac Users", "Visual Studio plug-In"],
        "without": ["© 1999-2020 Parallels", "Parallels Mac Management for SCCM"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.qualisys.eu/gefahrstoff-service": {
        "file": "qualisys.eu.gefahrstoff.html",
        "author": "",
        "title": "Gefahrstoffmanagement für Hersteller, Importeure und Alleinvertreter",
        "date": "2019-12-19",
        "description": "Datenrecherche und aktuelle Sicherheitsdatenblätter. Optimiertes Gefahrstoffmanagement. Verbesserte Marktfähigkeit Ihrer Produkte.",
        "categories": [],
        "tags": [],
        "with": [
            "Qualisys ist spezialisiert auf die Optimierung des Gefahrstoffmanagements",
            "SUMDAT Desktop im Format eines Sicherheitsdatenblattes",
            "Das Qualisys Gefahrstoff-Backoffice erfüllt alle Anforderungen",
        ],
        "without": ["D-40764 Langenfeld", "Kontakt"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.xinhuanet.com/local/2020-02/19/c_1125597921.htm": {
        "file": "xinhuanet.com.c_1125597921.html",
        "author": "焦鹏",
        "title": "武汉的声音：有英勇的你，才有英雄的城！",
        "date": "2020-02-19",
        "description": "武汉的声音：有英勇的你，才有英雄的城！\n---越是到疫情防控最为吃劲的时候，越是需要汇聚信心与力量。武汉“封城”27天后，湖北以外地区新冠肺炎每日确诊病例迎来15连降，湖北神农架林区确诊病例全部治愈。疫情虽在持续，但希望就在继续努力之中。正是有了英勇的你们，才有这座英雄的城！",
        "categories": [],
        "tags": [],
        "with": ["2月17日", "能过关。", "萧海川"],
        "without": ["纠错", "关注新华网", "半月谈"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.banyuetan.org/jmcs/detail/20200102/1000200033136171577956287380194268_1.html": {
        "file": "banyuetan.org.1000200033136171577956287380194268_1.html",
        "author": "孔德明",
        "title": "益阳：“数字”是优长",
        "date": "2020-01-02",
        "description": "益阳近3年连续举办智慧乡村互联网大会，赋能农业无土栽培、立体种植、智能调控、四季生产……在益阳一个智慧农业园区里，作为益阳智慧医疗的组成部分。",
        "categories": [],
        "tags": [],
        "with": ["高度认可……", "发现社会", "姚劲波说。"],
        "without": ["热门推荐", "理论应该", "杂志图书订阅"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://baike.baidu.com/item/%E8%94%A1%E5%81%A5%E9%9B%85": {
        "file": "baike.baidu.com.tanya.html",
        "author": "",
        "title": "蔡健雅_百度百科",
        "date": "2020-02-14",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["1975年1月28日出生", "独立制作", "2000年在新加坡"],
        "without": ["原木渣男", "网友印象", "百科词"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.lastampa.it/cronaca/2020/02/19/news/temperature-in-calo-in-tutta-italia-attesa-neve-sull-appennino-1.38487954": {
        "file": "lastampa.it.temperature.html",
        "author": "",
        "title": "Perturbazione polare al Centro e al Sud. Il Nord, scavalcato, mantiene temperature alte",
        "date": "2020-02-19",
        "description": "Piogge, temporali e nevicate previste per oggi nelle regioni centrali e meridionali. Interessate Marche, Abruzzo, Molise, Umbria e Lazio. Neve sull’Appennino sopra i 1400 metri. Il bel tempo tornerà in poche ore",
        "categories": ["Cronaca"],
        "tags": ["meteo", "neve", "caldo"],
        "with": ["tornerà in poche ore", "sopra i 1400 metri.", "specialmente in Galles."],
        "without": ["La grande sete", "Argomenti", "Ultima modifica"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://elpais.com/elpais/2020/02/18/ciencia/1582045946_459487.html": {
        "file": "elpais.com.ciencia.html",
        "author": "Nuño Domínguez",
        "title": "¿Ha llegado realmente la Antártida a los 20 grados?",
        "date": "2020-02-19",
        "description": "Los científicos cuestionan el reciente récord de temperatura y advierten de que lo más importante es la tendencia gradual al calentamiento que afecta al continente desde hace 60 años",
        "categories": ["Ciencia"],
        "tags": [
            "Hielo",
            "Aemet",
            "Antártida",
            "Altas temperaturas",
            "Calor",
            "Temperaturas",
            "Calentamiento global",
            "Cambio climático",
            "Meteorología",
            "Problemas ambientales",
        ],
        "with": ["Que en la Antártida se registren", "Este mediodía la Base", "y pasará a ser verde"],
        "without": ["Puede escribirnos", "Un grupo de pingüinos", "El portal de empleo InfoJobs"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.latimes.com/politics/story/2020-02-19/mike-bloomberg-democratic-debate-history": {
        "file": "latimes.com.bloomberg.html",
        "author": "Evan Halper",
        "title": "As his first debate nears, Bloomberg is having to answer about his past",
        "date": "2020-02-19",
        "description": "Bloomberg&#x27;s debate debut on Wednesday comes as he faces intensifying questions about past statements and acts that critics say demeaned women and minorities and contradict Democratic values.",
        "categories": [],
        "tags": ["Campaign 2020"],
        "with": ["a lot of explaining.", "His opponents don’t lack for material to use.", "floating above the fray"],
        "without": [
            "The latest news, analysis and insights",
            "writes about a broad range",
            "California loosens its individual mandate",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.uusisuomi.fi/uutiset/sanna-marin-tapasi-angela-merkelin-myos-saksa-haluaa-pitaa-kiinni-maataloustuista-meidan-nakemyksiamme-suurimpana-nettomaksajana-ei-ole-otettu-riittavasti-huomioon/b29c11d3-9590-4045-8e2c-a568f9f24617": {
        "file": "uusisuomi.fi.angela.html",
        "author": "Tapio Nurminen",
        "title": "Sanna Marin tapasi Angela Merkelin: Myös Saksa haluaa pitää kiinni maataloustuista - ”Meidän näkemyksiämme suurimpana nettomaksajana ei ole otettu riittävästi huomioon”",
        "date": "2019-02-19",
        "description": "",
        "categories": [],
        "tags": ["Politiikka", "EU"],
        "with": ["ehdistötilaisuudessa Berliinissä.", "Merkel korosti.", "Charles Michels"],
        "without": [
            "Kuva: ALEXANDER BECHER",
            "Brexit kasvattaa maksuja",
            "uudesta maahanmuuttolaista",
            "hiilineutraaliuteen ilman vippaskonsteja",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://yle.fi/uutiset/3-11212601": {
        "file": "yle.fi.3-11212601.html",
        "author": "Markus Mäki",
        "title": "Leudot talvet tekevät meistä väsyneempiä – näillä keinoilla torjut kaamosoireita",
        "date": "2019-02-19",
        "description": "Vuodenaikojen vaihtuminen vaikuttaa mielialaan ja käyttäytymiseen lähes kaikilla suomalaisilla.",
        "categories": ["Kotimaa"],
        "tags": [],
        "with": ["Vuodenaikojen vaihtuminen", "Ilmastonmuutos vaikuttaa terveyteen", "tuntuakin raskaalta."],
        "without": ["Korkeasaaren karhut", "Saat Ylen parhaat", "Wuhanilainen"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.tofugu.com/travel/dezuka-suisan/": {
        "file": "tofugu.com.dezuka-suisan.html",
        "author": "Kanae Nakamine",
        "title": "Dezuka Suisan: Deep-Fried Fish Cakes, Hot and Fresh",
        "date": "2020-02-04",
        "description": "Visit 出塚水産 (Dezuka Suisan), a local kamaboko fish cake factory/store in Monbetsu, Hokkaido and enjoy all the unique kinds of deep-fried fish cakes, hot and fresh",
        "categories": ["travel"],
        "tags": ["Hokkaido prefecture", "food", "fish cakes", "Monbestu", "travel"],
        "with": ["We picked out a couple of", "While they were cooking", "and everything was tasty.", "+81 158-23-2012"],
        "without": ["Abashiri Prison Museum", "885 words", "View larger map"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://blog.gaijinpot.com/tweet-of-the-week-67-dealing-with-chikan/": {
        "file": "blog.gaijinpot.com.chikan.html",
        "author": "Amelie Marie Nishizawa",
        "title": "Tweet of the Week #67: Dealing With Chikan",
        "date": "2020-02-08",
        "description": "Follow these steps shared on Twitter to safely apprehend a train groper in Japan.",
        "categories": [],
        "tags": ["Study Japanese", "Tweet of the Week"],
        "with": ["fear of causing a fuss in public", "確保する。", "help apprehend the culprit.", "@keizi666"],
        "without": ["Vegan food is notoriously hard", " 5 min read", "Student Placement Service"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://madame.lefigaro.fr/bien-etre/problemes-dintestin-quoi-manger-pour-aller-bien-110417-130897": {
        "file": "madame.lefigaro.fr.dintestin.html",
        "author": "Ophélie Ostermann",
        "title": "Les clés pour donner les bonnes bactéries à son intestin et aller bien",
        "date": "2017-04-12",
        "description": "Pour aller bien «en haut», commençons par aller bien «en bas». Mode d&#039;emploi pour prendre soin de son ventre et faire du bien à son «second cerveau».",
        "categories": [],
        "tags": ["Santé", "alimentation", "Ventre plat", "conseils"],
        "with": [
            "Car oui, avec ses 200 millions de neurones",
            "Travailler son stress",
            "riches en prébiotiques et en probiotiques.",
        ],
        "without": ["À lire aussi", "dîne tard chez soi", "Remportez le soin Time-Filler", "veuillez vous connecter"],
        "comments": ["quel enfumage !"],
        "license": "",
        "region": "",
    },
    "https://www.bondyblog.fr/societe/a-paris-8-un-peu-de-tension-beaucoup-d-actions/": {
        "file": "bondyblog.fr.paris-8.html",
        "author": "Kab Niang",
        "title": "A Paris-8, un peu de tension, beaucoup d’actions",
        "date": "2020-02-17",
        "description": "A l’université Paris-8 de Saint-Denis, des centaines d’étudiants, enseignants et personnels sont en grève depuis plusieurs semaines pour protester contre les projets de réformes du gouvernement. Ils espèrent faire franchir un nouveau cap à leur mobilisation à compter du 5 mars.",
        "categories": ["Société"],
        "tags": ["grève", "lutte", "mouvement social", "paris 8", "Saint-Denis", "université"],
        "with": [
            "Une grève reconductible à partir du 5 mars",
            "Marie-Pierre ne fait plus de cours",
            "Solidaires Étudiant-e-s Saint-Denis",
        ],
        "without": ["Candidatures ouvertes pour le Prix", "Intervenant à l’atelier", "Le piquet de grève dans le hall"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.assabah.com.tn/article/164913/%D8%A7%D9%84%D9%86%D8%A7%D8%B4%D8%B7-%D8%A7%D9%84%D8%AD%D9%82%D9%88%D9%82%D9%8A-%D8%A7%D9%84%D8%B3%D9%88%D8%AF%D8%A7%D9%86%D9%8A-%D8%AE%D8%A7%D9%84%D8%AF-%D8%B9%D8%A8%D8%AF-%D8%A7%D9%84%D9%83%D8%B1%D9%8A%D9%85-%D9%85%D8%A7%D8%B3%D8%A7-%D9%84%D9%80%C2%AB%D8%A7%D9%84%D8%B5%D8%A8%D8%A7%D8%AD%C2%BB-%D9%83%D9%84-%D8%A7%D9%84%D8%B4%D8%B1%D9%88%D8%B7-%D9%85%D8%AA%D9%88%D9%81%D8%B1%D8%A9-%D9%84%D8%AB%D9%88%D8%B1%D8%A9": {
        "file": "assabah.com.tn.article.html",
        "author": "",
        "title": "الناشط الحقوقي السوداني خالد عبد الكريم ماسا لـ«الصباح»:  كل الشروط متوفرة لثورة سودانية ولا حاجة لنستورد شيئا",
        "date": "",
        "description": "حوار: آسيا العتروس مالذي يحدث في السودان؟ والى أين يتجه البلد الذي يقوده الرئيس عمر البشير منذ ثلاثين عاما؟ وماذا عن الوعود الرسمية بالاصلاحات السياسية وضمان الحريات؟ ما هي أفاق التحركات الشعبية المست",
        "categories": [],
        "tags": [],
        "with": ["منذ بدء", "كل المجالات", "وماذا عن حقيقة"],
        "without": ["كورونا يقتل", "غائم جزئيا", "إضافة تعليق جديد"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://lapresse.tn/48915/parite-hommes-femmes-en-tunisie-au-dessous-de-la-moyenne-mondiale/": {
        "file": "lapresse.tn.parite.html",
        "author": "Chokri GHARBI",
        "title": "Parité hommes-femmes en Tunisie : Au-dessous de la moyenne mondiale",
        "date": "2020-02-18",
        "description": "",
        "categories": ["Société"],
        "tags": ["femme", "homme", "parité"],
        "with": ["Malgré les acquis législatifs", "Des actions à entreprendre", "assurer l’égalité des chances"],
        "without": ["Après une mise en quarantaine", "des moments dans le parcours historique", "partiellement nuageux"],
        "comments": ["La parité je veux bien"],
        "license": "",
        "region": "",
    },
    "https://www.ledevoir.com/politique/montreal/573258/la-fin-des-trottinettes-en-libre-service-a-montreal": {
        "file": "ledevoir.com.trottinettes.html",
        "author": "Jeanne Corriveau",
        "title": "La fin des trottinettes en libre-service à Montréal",
        "date": "2020-02-19",
        "description": "L’administration Plante justifie sa décision par le taux élevé de délinquance chez les utilisateurs.",
        "categories": [],
        "tags": ["Valérie Plante", "trottinette", "trottinette électrique"],
        "with": ["En raison du taux élevé de délinquance", "D’autres détails suivront."],
        "without": ["La GRC doit partir", "des 4 articles gratuits", "Du lundi au samedi"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://taz.de/Siemens-und-die-Kohlemine-Adani/!5655255/": {
        "file": "taz.de.siemens.html",
        "author": "Ingo Arzt",
        "title": "Kaeser verarscht Neubauer",
        "date": "2020-01-13",
        "description": ">Siemens-Chef Joe Kaeser hat die Klimaaktivistin Luisa Neubauer über den Tisch gezogen. In der Logik des Konzerns lohnt sich das.",
        "categories": ["Öko"],
        "tags": ["Siemens", "Luisa Neubauer", "Joe Kaeser", "Australien"],
        "with": [
            "Ein paar Konsument*innen mögen",
            "Einige von ihnen, etwa Axa",
            "ei potenziellen Kund*innen aus der fossilen Industrie",
        ],
        "without": [
            "Hinter jedem Klick auf taz.de",
            "Schreibt seit 2008 für die taz",
            "Bitte registrieren Sie sich und halten Sie sich",
        ],
        "comments": [
            "Inhaltlich ist der Artikel super",
            " Neubauers Job ist nicht Kaeser quasi",
            "folgenden Artikel interessant, ob man jetzt die Ernsthaftigkeit",
        ],
        "license": "",
        "region": "DE",
    },
    "https://fivethirtyeight.com/features/the-2020-endorsement-race-is-getting-interesting/": {
        "file": "fivethirtyeight.com.endorsement.html",
        "author": "Perry Bacon Jr.",
        "title": "The 2020 Endorsement Race Is Getting Interesting",
        "date": "2020-01-28",
        "description": "If you’ve been following endorsements of the 2020 Democratic primary field, the biggest thing that stands out is the lack of them, as my colleague Geoffrey Skel&#8230;",
        "categories": ["2020 Election"],
        "tags": [
            "2020 Election",
            "2020 Democratic Primary",
            "Bernie Sanders",
            "Joe Biden",
            "Elizabeth Warren",
            "Iowa Caucus",
            "Pete Buttigieg",
            "Iowa",
            "New Hampshire",
            "New Hampshire Primary",
            "Amy Klobuchar",
            "The Endorsement Primary",
        ],
        "with": [
            "If you’ve been following endorsements",
            "fter all, Biden and Sanders lead in national polls",
            "Perhaps these endorsements are capturing",
        ],
        "without": ["Perry Bacon Jr. is a senior writer for FiveThirtyEight.", "Filed under", "About Nielsen Measurement"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.wired.com/story/ai-great-things-burn-planet/": {
        "file": "wired.com.burn.html",
        "author": "Will Knight",
        "title": "AI Can Do Great Things—if It Doesn't Burn the Planet",
        "date": "2020-01-21",
        "description": "",
        "categories": ["business"],
        "tags": ["artificial intelligence", "machine learning", "OpenAI", "Energy", "Climate Change"],
        "with": [
            "Last month, researchers at OpenAI in San Francisco revealed",
            "As more companies across more industries begin",
            "including the energy needed to build it",
        ],
        "without": [
            "One algorithm that lets a robot manipulate a Rubik",
            "The latest on artificial intelligence, from machine learning to computer vision and more",
            "writer for WIRED, covering artificial intelligence",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.parcoabruzzo.it/dettaglio.php?id=58354": {
        "file": "parcoabruzzo.it.58354.html",
        "author": "",
        "title": "ORSO MARSICANO: 2019 UN ANNO DA RECORD",
        "date": "2020-01-14",
        "description": "ORSO MARSICANO: 2019 UN ANNO DA RECORD (Notizia del 14 Gennaio 2020)",
        "categories": [],
        "tags": [],
        "with": ["Il risultato è molto positivo", "naturali di regolazione numerica", "In questo contesto è chiaro"],
        "without": ["Grafico conta femmine con", "Tel. 0863/91131 - Fax 0863/912132", "Autore di Parks.it"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.timesofisrael.com/state-of-washington-swears-in-first-native-american-jewish-supreme-court-justice/": {
        "file": "timesofisrael.com.washington.html",
        "author": "Emily Burack",
        "title": "State of Washington swears in first Native American-Jewish Supreme Court justice",
        "date": "2020-01-08",
        "description": "Governor says naming of &#039;exceptional&#039; Raquel Montoya-Lewis is historic, but he called on her &#039;because she&#039;s the best for the job&#039;",
        "categories": [],
        "tags": [
            "Jewish Times",
            "Jewish Supreme Court Justices",
            "Supreme Court",
            "judges",
            "female judges",
            "US courts",
            "Jewish women",
            "Native Americans",
        ],
        "with": [
            "Governor Jay Inslee appointed Montoya-Lewis",
            "I was raised to remember that I come",
            "At the ceremony, there was an invocation from",
        ],
        "without": ["Get The Times of Israel", "For as little as $6 a month", "Already a member? Sign in to stop seeing this"],
        "comments": [
            "Congratulations to the Lady",
            "I'd like to add my Mazel Tov",
            "of irrelevant information, personal bias and",
        ],
        "license": "",
        "region": "",
    },
    "https://www.scmp.com/comment/opinion/article/3046526/taiwanese-president-tsai-ing-wens-political-playbook-should-be": {
        "file": "scmp.com.playbook.html",
        "author": "Alice Wu",
        "title": "Taiwanese President Tsai Ing-wen’s political playbook should be essential reading for Hong Kong leader Carrie Lam",
        "date": "2020-01-20",
        "description": "While both Tsai and Lam faced a challenging year, the Taiwanese leader shrewdly capitalised on the crisis in Hong Kong to claim herself a massive election win.",
        "categories": [],
        "tags": [
            "Carrie Lam",
            "Legislative Council of Hong Kong",
            "Taiwan",
            "Taiwan elections 2020",
            "Tsai Ing-wen",
            "Hong Kong protests",
            "Hong Kong extradition bill",
            "5050",
        ],
        "with": ["almost insulting to Hongkongers", "a sign she was working hard for the", "using political shrewdness"],
        "without": [
            "Alice Wu fell down the rabbit hole",
            "Lam staying on as chief executive",
            "Tsai says Beijing must face",
            "By registering, you agree to",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://deleuze.enacademic.com/104/micropolitics": {
        "file": "deleuze.enacademic.com.micropolitics.html",
        "author": "Kenneth Surin",
        "title": "micropolitics",
        "date": "",  # 2010
        "description": "by Kenneth Surin   Deleuze and Guattari oppose micropolitics to the politics of molarisation. Where the molar (or arborescent , to use their equivalent term) designates structures and principles that are based on rigid stratifications or&amp;#8230",
        "categories": [],
        "tags": [],
        "with": ["The orchestration of desire", "Deleuze and Guattari oppose", "into itself the ﬂows"],
        "without": ["noun The use of formal", "is professor emeritus of", "Merleau-Ponty, Maurice"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://juliasleseblog.blogspot.com/2018/08/irland-roadtrip.html": {
        "file": "juliasleseblog.blogspot.com.irland.html",
        "author": "Julia Fahrngruber",
        "title": "Irland Roadtrip",
        "date": "2018-08-02",
        "description": "",
        "categories": [],
        "tags": ["OffTopic", "Reiseberichte", "Urlaub"],
        "with": ["meine zweite große Leidenschaft", "findet ihr darin sogar", "bei Fragen helfe ich gerne"],
        "without": ["Gepostet vor", "Kommentar schreiben als", "Julias Lesewelt "],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://literaturgefluester.wordpress.com/2019/01/01/ins-neue-jahr-4/": {
        "file": "literaturgefluester.wordpress.com.jahr.html",
        "author": "jancak",
        "title": "Ins neue Jahr",
        "date": "2019-01-01",
        "description": "Weihnachten und Silvester habe ich diesmal wieder in Harland bei St. Pölten verbracht. Zehn lange Tage, denn wir sind am Samstag den 22. Dezember sehr früh dorthin gefahren, nachdem ich den Freitag…",
        "categories": ["Alltagsgeplauder", "Büchergeschichten", "Gesellschaftspolitik", "Schreibbericht"],
        "tags": ["Neujahrswünsche"],
        "with": ["Weihnachten und Silvester habe", "wahrscheinlich am Mittwoch, wenn", "in der ersten Jännerwoche"],
        "without": ["Einem Blogger gefällt dies.", "Teilen Sie dies mit:", "This site uses Akismet to reduce spam"],
        "comments": ["Deinen letzten Absatz kann ich nur", "Ebenfalls alles Gute"],
        "license": "",
        "region": "",
    },
    "https://abookshelffullofsunshine.blogspot.com/2013/10/news-viertes-eigenes-blog-interview.html": {
        "file": "abookshelffullofsunshine.blogspot.com.interview.html",
        "author": "",
        "title": "(News) Viertes eigenes Blog-Interview: Dieses Mal mit Anne Lück",
        "date": "2013-10-05",
        "description": "Ein Interview mit Anne Lück",
        "categories": [],
        "tags": ["Anne", "Der Weg des Unsterblichen", "Endless Life", "Interview", "Lück", "News"],
        "with": [
            'Vor einiger Zeit durfte ich "Endless Life"',
            "Am 4. Oktober kommt dein",
            "Freiraum für seine eigenen Gedanken",
        ],
        "without": ["Angelfall – Tage der Dunkelheit", "Kommentare:", "Ihr seid die Besten!"],
        "comments": ["ein wirklich tolles Interview", "Ja, die bekannten Verlage"],
        "license": "",
        "region": "",
    },
    "https://www.derpapierplanet.de/2015/06/through-booking-glass-juni-genre.html": {
        "file": "derpapierplanet.de.juni.html",
        "author": "",
        "title": "Through the Booking Glass: Juni & Genre-Vorstellung",
        "date": "2015-06-05",
        "description": "",
        "categories": [],
        "tags": ["genres", "through the booking glass"],
        "with": ["Jeder darf mit machen", "als wirklich ausgiebig Fantasy", "einem schon gewisse Bilder"],
        "without": ["Du möchtest gerne bei Through", "dir abgeschickten Kommentar akzeptierst", "Teilnehmende Blogs:"],
        "comments": ["Interessanter Post!", "Übrigens höre ich gerade deine Playlists", "Bin schon gespannt wie"],
        "license": "DE",
        "region": "",
    },
    "https://weinlachgummis.blogspot.com/2017/09/rezi-love-is-war-sehnsucht-von-r-k.html": {
        "file": "weinlachgummis.blogspot.com.rezi.html",
        "author": "Weinlachgummi",
        "title": "[Rezi] Love is War - Sehnsucht von R. K. Lilley",
        "date": "2017-09-09",
        "description": "",
        "categories": [],
        "tags": ["2017", "4Weingummis", "Buchrezensionen", "Erotik", "fesselnd", "Heyne", "Missbrauch", "Reihe"],
        "with": ["Wir fühlten uns vereint", "Aber wieso aus Liebe Krieg", "Ich habe das Buch regelrecht verschlugen"],
        "without": ["Ich freue mich über eure Kommentare", "Danke für eure Kommentare^^", "Info zur Bewertung"],
        "comments": ["schön, dass dir das"],
        "license": "",
        "region": "",
    },
    "https://happyface313.com/2018/03/07/im-test-plantur-39-color-braun-phyto-coffein-shampoo-und-pflege-spulung/": {
        "file": "happyface313.com.plantur.html",
        "author": "happyface313",
        "title": "Im Test: Plantur 39 Color Braun Phyto-Coffein-Shampoo und Pflege-Spülung",
        "date": "2018-03-07",
        "description": "Als ich neulich eine Anfrage erhielt ein Plantur Farbshampoo samt Spülung zu testen, war ich ein wenig skeptisch. Meine Kopfhaut ist super empfindlich und deshalb bin ich sehr heikel was Shampoos angeht. Deshalb färbe ich meine Haare auch nicht so oft, wie ich es eigentlich müsste.",
        "categories": ["Allgemein", "Beauty"],
        "tags": ["Braun", "Color-Shampoo", "Haare färben", "Haarfarbe", "Pflegespülung"],
        "with": [
            "Als ich neulich eine Anfrage erhielt",
            "Shampoo und Spülung werden in einer dunkelbrauen",
            "und meine Haare sahen gesund",
        ],
        "without": ["Teilen mit:", "Follow Blog via Email", "Vollständiges Profil anzeigen"],
        "comments": ["Du hast sehr schönes Haar", "Schön, dass Du Pflegeprodukte", "die Farbe von Shampoo und"],
        "license": "",
        "region": "",
    },
    "https://www.sheego.de/magazin/coole-tipps/magic-cleaning/": {
        "file": "sheego.de.cleaning.html",
        "author": "",
        "title": "Die besten Tricks von Marie Kondo für Kleiderschrank & Co.",
        "date": "",
        "description": "Magic Cleaning | sheego ♥ Magazin",
        "categories": [],
        "tags": [],
        "with": ["Sie ist die Königin des Aufräumens", "sie kommen ganz zum Schluss", "Was gibt mir ein gutes Gefühl"],
        "without": ["15 %* Newsletter Gutschein", "Ich bin damit einverstanden", "Coole Tipps|Magic Cleaning"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.limespace.de/2019/10/22/professionell-entloeten-so-machen-sie-alte-elektrogeraete-wieder-einsatzbereit/": {
        "file": "limespace.de.entloeten.html",
        "author": "Limespacer",
        "title": "Professionell entlöten – so machen Sie alte Elektrogeräte wieder einsatzbereit",
        "date": "2019-10-22",
        "description": "",
        "categories": [],
        "tags": ["Bauteile", "Löten", "Reparieren"],
        "with": ["Haushaltsgeräte, die verrücktspielen", "das Verzinnen der Pins", "Entlötstation und einigen Handgriffen"],
        "without": ["Diese Website verwendet Akismet", "Das könnte Dich auch interessieren …", "Werbepause"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://chadim.net/text-planung/der-schreibstil": {
        "file": "chadim.net.schreibstil.html",
        "author": "",
        "title": "Schreiben Sie Informationen für Ihre Zielgruppe",
        "date": "",
        "description": "Ihre Website mit chadim.net - Webdesign. Optimale Lösungen und perfekte Umsetzung für Ihren Webauftritt oder Ihr Redesign. Kompetent und preisgünstig.",
        "categories": [],
        "tags": [],
        "with": ["Beim Schreiben Ihrer Texte", "Fremd- und Modewörtern", "an Ihren Lesern vorbeischreiben"],
        "without": ["Angemeldet bleiben", '... weiter zu "die Wortwahl"', "Aktuelle Seite:"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://frau-sabienes.de/konsumsparen-fazit/": {
        "file": "frau-sabienes.de.konsumsparen.html",
        "author": "Frau Sabienes",
        "title": "Mein Motto Konsumsparen: Fazit, Erkenntnisse und meine Pläne für 2020",
        "date": "2020-02-17",
        "description": "",
        "categories": ["Allgemein"],
        "tags": ["geld", "minimalismus", "sparen"],
        "with": ["Das Jahr 2019 stand", "Ich werde also weiterhin meinen Konsum einschränken", "Ich bin gerade am Überlegen"],
        "without": ["Inzwischen ganze 60", "Hier bin ich auch noch unterwegs", "Vorschau auf den nächsten Artikel"],
        "comments": [
            "ganz interessant Deine Erfahrungen",
            "die Preise für einen Aperol Sprizz",
            "Lieben Dank für die Auflistung",
        ],
        "license": "",
        "region": "DE",
    },
    "http://lexikon.huettenhilfe.de/obst/banane.html": {
        "file": "lexikon.huettenhilfe.de.banane.html",
        "author": "",
        "title": "Banane, Bananen, Banana (Musa spp. paradisica)",
        "date": "2011-07-25",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Bananen verderben - wie es bestimmt jeder schon erlebt hat",
            'Die "Große Obstbanane" und ihre Sorten',
            "Wie die Banane nach Europa kam",
        ],
        "without": ["2006 - 2012 huettenhilfe.de", "Nüsse und Kerne", "und vieles mehr rund um die Küche"],
        "comments": [],
        "license": "CC BY-NC-SA 2.0 DE",
        "region": "DE",
    },
    "https://www.guenter-pilger.de/mailaktion.htm": {
        "file": "guenter-pilger.de.mailaktion.html",
        "author": "Günter Pilger",
        "title": "Mail-Aktion an den Deutschen Bundestag",
        "date": "",
        "description": "Mailaktion an den Bundestag. Frage an die Abgeordneten zur erneuten Halbierung des Sparerfreibetrages und die Antworten dazu",
        "categories": [],
        "tags": [],
        "with": [
            "ich protestiere gegen die erneute",
            'Geantwortet haben nur "Die Linken"',
            "in denen Sie die Bürger zur privaten",
        ],
        "without": ["Rentenpolitik | Blog | Mailaktion Bundestag | Alles klar?", "Startseite", "Partnerseiten"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://de.happycoffee.org/collections/shop/products/happy-coffee-sidamo-bio-kaffeebohnen": {
        "file": "de.happycoffee.org.sidamo.html",
        "author": "",
        "title": "Happy Coffee SIDAMO Bio Bohnen",
        "date": "2019-03-02",
        "description": "HINWEIS: Neues Design im Feb. 2020. Mehr erfahren.  Aroma Rote Beeren, Zitrusnoten, süßlich, kräftig-würzig Stärke Säure Herkunft  Kooperative Sidama Coffee Farmers Cooperative Union SCFCU, Sidamo (Äthiopien) Prozess Handgepflückt, gewaschen, sonnengetrocknet Varietät einheimische Varietäten Bio-zertifiziert | Kontroll",
        "categories": [],
        "tags": [],
        "with": [
            "Rote Beeren, Zitrusnoten, süßlich",
            "Handgepflückt, gewaschen, sonnengetrocknet",
            "Alle Kaffees von Happy Coffee sind bio-zertifiziert",
        ],
        "without": ["Jetzt mit 10% Dauerrabatt", "Unsere Kaffees", "Frisch gerösteter Kaffee nach Hause geliefert"],
        "comments": [
            "Ich kann die Meinung von Dieter nicht nachvollziehen",
            "Der Geschmack war kaum von Tchibo",
            "Der Kaffe duftet herrlich",
        ],
        "license": "",
        "region": "",
    },
    "https://www.spektrum.de/wissen/laesst-sich-die-coronavirus-ausbreitung-in-deutschland-kontrollieren/1700384": {
        "file": "spektrum.de.coronavirus.html",
        "author": "Lars Fischer und Alina Schadwinkel",
        "title": "Lässt sich die Coronavirus-Ausbreitung in Deutschland kontrollieren?",
        "date": "2020-02-26",
        "description": "In Baden-Württemberg und NRW gibt es erstmals Covid-19-Fälle. Wie Behörden die Ausbreitung verhindern wollen und wie man sich schützen kann, ein FAQ.",
        "categories": [],
        "tags": [],
        "with": [
            "In Baden-Württemberg und NRW",
            "Ein Problem: So viele Berichte und Nachrichten",
            "Viele Menschen haben nur eine leichte",
        ],
        "without": ["Wenn Sie inhaltliche Anmerkungen zu", "Bleiben Sie auf dem Laufenden", "Lesedauer ca. 6"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.talent.ch/?p=5031": {
        "file": "talent.ch.5031.html",
        "author": "revamp-it Webteam",
        "title": "Protokoll der Vorstandssitzung vom 10. Oktober 2019",
        "date": "2019-12-26",
        "description": "Zeit und Ort: 15.00 - 16.45 bei revamp-it, Röschibachstr. 24-26, 8037 Zürich Teilnehmende Vorstandsmitglieder: Daniel Sieber, Hans Leuenberger, Johannes Mahler",
        "categories": [],
        "tags": [],
        "with": [
            "Abnahme Protokoll der letzten Vorstandssitzung",
            "Johannes schickt seinen Entwurf für einen",
            "Daniel sucht nach Möglichkeiten",
        ],
        "without": [
            "Möchtest du TALENT einfach nur",
            "Oder du überweisst deine Spende",
            "Es gibt derzeit keine bevorstehenden Veranstaltungen.",
        ],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://www.pronats.de/informationen/kindheit-und-arbeit/kinder-und-arbeit/": {
        "file": "pronats.de.arbeit.html",
        "author": "",
        "title": "Kinder und Arbeit",
        "date": "2016-12-30",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Nicht die Arbeit ist für die", "Wir bestehen deshalb darauf", "Einmal begleiteten wir eine"],
        "without": [
            "Als NATs bezeichnen sich die",
            "Texte auf dieser Webseite stehen unter einer",
            "ProNATs - Verein zur Unterstützung arbeitender",
        ],
        "comments": [],
        "license": "CC BY-ND 3.0",
        "region": "DE",
    },
    "https://www.tafelblog.de/welches-europa-wir-wollen/": {
        "file": "tafelblog.de.europa.html",
        "author": "Herr_Rein",
        "title": "„Welches Europa wir wollen“",
        "date": "2019-06-11",
        "description": "",
        "categories": ["politisches"],
        "tags": ["Demokratie", "EU", "Wahlen"],
        "with": [
            "Knapp zwei Tage vor der Europawahl",
            "Die Ergebnisse der Bülow-Wahl",
            "bei uns viele Stimmen hinzugewinnen",
        ],  # 3' segments
        "without": ["Schreibe einen Kommentar", "Aachen 1933 – 1945", "Meinen Namen, E-Mail"],
        "comments": [],
        "license": "CC BY-NC 3.0 DE",
        "region": "DE",
    },
    "http://columbus-entdeckt.de/ski-fahren-auf-den-spuren-des-trolls/": {
        "file": "columbus-entdeckt.de.trolls.html",
        "author": "",
        "title": "Ski-Fahren auf den Spuren des Trolls",
        "date": "2020-01-05",
        "description": "Island lockt auch im Winter: Abfahrten über unberührte Hänge. Und noch keine Spur vom Massenskitourismus. Siglufjörður im Norden Islands ist das Zentrum des isländischen Ski-Tourismus. Die Troll-Ha…",
        "categories": [],
        "tags": [],
        "with": ["Island lockt auch im Winter", "Das größte in Akureyri hat fünf Lifte", "und auf den Spuren des Trolls"],
        "without": ["Die besten Reisegeschichten"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.geburtstagsecke.de/ideen": {
        "file": "geburtstagsecke.de.ideen.html",
        "author": "",
        "title": "Ideen für den Kindergeburtstag",
        "date": "",
        "description": "Geburtstagsecke.de gibt die eine Menge Ideen für den Kindergeburtstag. Egal ob Kleinkinder oder Teenager, bei uns findest du viele Anregungen.",
        "categories": [],
        "tags": [],
        "with": [
            "Die richtigen Ideen für den",
            "Daher ist es sinnvoll das Kind in die Planung",
            "Ihr solltet aber auf jeden Fall",
        ],
        "without": ["© 2019 geburtstagsecke.de", "Geburtstage für Erwachsene planen und feiern", "Beliebte Tags"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.advents-shopping.de/die-weihnachtsmarkt-saison-beginnt-so-finden-sie-die-besten-weihnachtsmaerkte-in-ihrer-naehe.html": {
        "file": "advents-shopping.de.weihnachtsmaerkte.html",
        "author": "",
        "title": "Die Weihnachtsmarkt-Saison beginnt! So finden Sie die besten Weihnachtsmärkte in Ihrer Nähe",
        "date": "2014-11-02",
        "description": "P&uuml;nktlich mit dem Beginn der Weihnachtsmarkt-Saison in Deutschland wurde der Weihnachtsmarkt-Finder, eine kostenlose Webapplikation, mit der Sie ganz einfach...",
        "categories": [],
        "tags": ["Weihnachtsmarkt"],
        "with": ["Pünktlich mit dem Beginn der", "Ein neues Layout stellt sicher", "ein kostenlose Webapplikation"],
        "without": [
            "Ihr weihnachtlicher Kurzurlaub",
            "Advents-Shopping.de nimmt Sie mit in die",
            "o finden Sie die besten Weihnachtsmärkte",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://bloghaus.hypotheses.org/2320": {
        "file": "bloghaus.hypotheses.org.2320.html",
        "author": "Ulrike Stockhausen",
        "title": "Einen Twitterfeed in das Blog einbinden – so geht’s!",
        "date": "2019-09-26",
        "description": "Aktualisiert am 19.02.2020 Um Sichtbarkeit und Leserschaft auf einem Wissenschaftsblog zu generieren, empfiehlt sich der Einsatz eines Twitteraccount, über den Artikel geteilt und ein Austausch mit der Community angestoßen werden kann. In diesem Blogbeitrag zeigen wir, wie man den eigenen  Twitterfeed direkt und datenschutzkonform in ein Blog einbetten kann. So sehen Leserinnen und Leser auf &hellip; Einen Twitterfeed in das Blog einbinden – so geht’s! weiterlesen &rarr;",
        "categories": [],
        "tags": ["Datenschutz", "Twitter"],
        "with": [
            "Um Sichtbarkeit und Leserschaft",
            "In diesem Blogbeitrag zeigen wir",
            "Und so sieht das bei uns im Redaktionsblog aus",
        ],
        "without": ["Ein Blog präsentiert von Hypotheses", "Dieses Blog gibt Hilfestellung", "Bloghaus in anderen Sprachen"],
        "comments": [],
        "license": "CC BY 3.0",
        "region": "",
    },
    "http://www.der-erfolg-gibt-recht.de/rezepte/rinderleber-geschnetzeltes-mit-apfel-und-zwiebel.htm": {
        "file": "der-erfolg-gibt-recht.de.rinderleber.html",
        "author": "Rezepte von Mutti",
        "title": "Rinderleber-Geschnetzeltes mit Apfel und Zwiebel",
        "date": "2010-12-08",
        "description": "So schön winterlich ist es wie schon lange nicht mehr. Da bringt es richtig Laune, mal wieder was ganz besonders",
        "categories": [],
        "tags": ["Apfel", "Leber", "Rinderfonds", "Rinderleber", "Rotwein", "Zwiebel"],
        "with": ["So schön winterlich ist es wie", "Und wie (fast) immer bei uns", "Dazu gab es bei uns selbst gemachten"],
        "without": ["© Liebe geht durch den Magen", "Holen Sie sich Ihre „Kostprobe“", "Be Sociable, Share!"],
        "comments": ["Eine interessante Art Leber zuzubereiten", "Das sieht lecker aus", "Gelingt am besten in einer mit"],
        "license": "",
        "region": "DE",
    },
    "https://www.trainingline-english.de/am-telefon-1/einzeltraining/": {
        "file": "trainingline-english.de.einzeltraining.html",
        "author": "",
        "title": "Einzeltraining",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Beim Englischtraining am Telefon", "Das Englischtraining am Telefon", "Und mit jedem Satz wächst"],
        "without": ["51467 Bergisch Gladbach", "...und fast unbemerkt", "+49 (0)2202 -2809436"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://tell-review.de/unstillbares-heimweh/": {
        "file": "tell-review.de.heimweh.html",
        "author": "Frank Hahn",
        "title": "Unstillbares Heimweh",
        "date": "2019-09-18",
        "description": "In seinem Essay „Lob der Melancholie“ erkundet László Földényi ein paradoxes Gefühl zwischen Traurigkeit und Transzendenz.",
        "categories": ["Aktuell", "Rezension", "Sachbuch"],
        "tags": ["Melancholie"],
        "with": [
            "In seinem Essay „Lob der Melancholie“",
            "Schon in seiner ersten Studie Melancholie",
            "in immer wiederkehrender Bezugspunkt",
        ],
        "without": ["Gefällt Ihnen, was Sie sehen?", "Benachrichtige mich über nachfolgende", "Freier Autor in Berlin"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://it-for-kids.org/blog/191211_variables/": {
        "file": "it-for-kids.org.variables.html",
        "author": "Amelie Loevenich",
        "title": "Variablen und ihr Zuhause",
        "date": "2019-12-11",
        "description": "Wie war das nochmal mit den Variablen? Hier ein Auszug aus unseren Lehrmaterialien!           Variablen sind kein Problem für dich? Dann schau doch mal, ob du unser Puzzle lösen kannst!",
        "categories": [],
        "tags": [],
        "with": [
            "Wie war das nochmal mit den Variablen",
            "Variablen sind kein Problem für dich?",
            "Auszug aus unseren Lehrmaterialien",
        ],
        "without": ["Copyright © 2020 IT4Kids", "Impressum"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://papaganda.org/2016/04/02/minions-mit-schablonen-malen-mit-malerrolle-und-bunten-farben/": {
        "file": "papaganda.org.minions.html",
        "author": "Floyd",
        "title": "Minions mit Schablonen malen – mit Malerrolle und bunten Farben",
        "date": "2016-04-02",
        "description": "Die Kinder lieben Minions. An einem regnerischen Wochenende malen Kind 1 und ich mit Schablonen Minions auf Holz. Für das Kinderzimmer.",
        "categories": ["DIY (Do it Yourself)"],
        "tags": ["Bild", "Farbe", "Holz", "Kind 1", "Minions", "Schablonen", "Stencil"],
        "with": ["Wochenende. Regen. Mist.", "Im Baumarkt des Misstrauens", "Papa, geh mal auf Google"],
        "without": ["Das Internet behauptet", "2 Kommentare", "Zu faul zu tippen?"],
        "comments": ["Großartig! Das gefällt mir richtig gut!", "Schön Yvonne, dass es dir gefällt"],
        "license": "",
        "region": "",
    },
    "http://marktplatz.die-besserwisser.org/alles-hat-seine-zeit/": {
        "file": "marktplatz.die-besserwisser.org.zeit.html",
        "author": "",
        "title": "Alles hat seine Zeit…",
        "date": "2017-04-05",
        "description": "...und die Zeit mit der Genossenschaft besserwisser geht nun zu Ende. Sie war für uns spannend, energiegeladen und voller wunderbarer Begegnungen. Nun ist es",
        "categories": ["Allgemein", "news"],
        "tags": [],
        "with": ["Sie war für uns spannend", "Für einige der Mitglieder", "Begeisterung ist ansteckend"],
        "without": ["Vorheriger Artikel", "Marktplatz für ein gutes Leben", "Leitfaden für den bio-regionalen Einkauf"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.doschu.com/2020/02/solopreneur-social-media-linkedin/": {
        "file": "doschu.com.solopreneur.html",
        "author": "Doris Schuppe",
        "title": "Solopreneur Social Media: LinkedIn",
        "date": "2020-02-14",
        "description": "Friederike Gonzalez zeigt, wie wirksam ein gut positioniertes Profil im Social Network LinkedIn zur Darstellung und Wahrnehmung der fachlichen Expertise ist",
        "categories": ["Social Media"],
        "tags": ["B2B", "Best Practice", "Interview", "LinkedIn", "Selbständige", "Solopreneure"],
        "with": [
            "Einblicke und Impulse aus der Praxis",
            "Was ist zu beachten um sich im Business",
            "Ohne diesen Blog, welcher",
        ],
        "without": ["Like it? Share it!", "Hinterlassen Sie einen Kommentar", "Let’s Talk @ Social Web"],
        "comments": [],
        "license": "CC BY-NC-ND 3.0 DE",
        "region": "DE",
    },
    "https://blog.teufel.de/musik-und-sport-so-steigern-songs-deine-leistung/": {
        "file": "blog.teufel.de.leistung.html",
        "author": "Teufel Blog Redaktion",
        "title": "Musik und Sport: So steigern Songs deine Leistung",
        "date": "2020-02-13",
        "description": "Musik und Sport gehören für dich einfach zusammen? Wir erklären dir, wie und warum deine Lieblingssongs deine Leistungsfähigkeit steigern können.",
        "categories": [],
        "tags": ["Audio-Ratgeber", "Entertainment", "Sport", "sportkopfhörer"],
        "with": [
            "Wenn das Lieblingslied im Radio",
            "Hier stellen wir dir einige spannende Fakten dazu vor",
            "Playlists, die dich zum Schwitzen bringen",
        ],
        "without": [
            "Alles über Lautsprecher, Heimkino",
            "In diesem Blog schreiben Teufel-Kollegen",
            "Newsletter abonnieren und 10€",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.whiskyverkostung.com/termine-whisky-tastings-januar-mai-2020-halle-saale/5805": {
        "file": "whiskyverkostung.com.halle.html",
        "author": "",
        "title": "Termine Whisky Tastings Januar – Mai 2020 Halle/Saale und Dessau",
        "date": "2019-11-27",
        "description": "Auch im Jahr 2020 wird es wieder Termine für Whisky-, Rum- und Ginverkostungen geben. Die ersten Termine stehen bereits fest, weitere werden in den nächsten Tagen und Wochen dazu kommen.   Februar 2020   Termin: 21.02.2020, 19 Uhr       	Ort: Ort: Rosi`s Bar ...",
        "categories": ["Allgemein", "Region Halle - Leipzig", "Tastings & Events", "Veranstaltungskalender"],
        "tags": [],
        "with": ["Auch im Jahr 2020 wird", "Termin: 29.02.2020, 19 Uhr", "Whikies aus verschiedenen Regionen Schottlands "],
        "without": ["Info & Anmeldungen", "Copyright © 2020 by: whiskyverkostung.com", "Der Beitrag wurde am Mittwoch"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://zahlenzauberin.wordpress.com/2012/08/22/was-zum-horen-in-den-ferien/": {
        "file": "zahlenzauberin.wordpress.com.ferien.html",
        "author": "zahlenzauberin",
        "title": "Was zum hören in den Ferien",
        "date": "2010-08-22",
        "description": "Dank Kabelanschluss kann ich, auch in Sachsen ,Bayern 2  hören. Da läuft gerade ein spannendes nah dran zum Thema: Freude, Falle, Frust: Der Mutterliebe zarte Sorgen Raben- versus Gluckenmütter &amp;#8…",
        "categories": ["Archiv", "Feminismus", "Mama"],
        "tags": [],
        "with": ["Dank Kabelanschluss kann ich", "der auch nur 20 Minuten dauert.", "Liebe zum Kind?"],
        "without": ["Teilen Sie dies mit:", "Ähnliche Beiträge", "Abgelegt unter:"],
        "comments": [],
        "license": "CC BY-NC-SA 3.0",
        "region": "",
    },
    "https://www.deutschlandfunk.de/die-zukunft-der-arbeit-wir-dekorieren-auf-der-titanic-die.911.de.html?dram:article_id=385022": {
        "file": "deutschlandfunk.de.titanic.html",
        "author": ["Richard David Precht", "Karin Fischer"],
        "title": "„Wir dekorieren auf der Titanic die Liegestühle um“",
        "date": "2017-05-01",
        "description": "Die Digitalisierung der Arbeitswelt werde Millionen Arbeitsplätze kosten, auch in Deutschland. Eine Herausforderung, der sich die Gesellschaft noch nicht einmal ansatzweise gestellt habe, sagte der Publizist und Philosoph Richard David Precht im DLF. Auch in Zukunft würden Menschen noch arbeiten, aber vielleicht nicht mehr für Geld.",
        "categories": [],
        "tags": [],
        "with": [
            "Die Digitalisierung der Arbeitswelt werde Millionen Arbeitsplätze kosten, auch in Deutschland.",
            "Das Problem ist dabei nicht das selbstfahrende",
            "Also ich glaube, wenn man sich",
        ],
        "without": ["Entdecken Sie den Deutschlandfunk", "Deutschlandradio © 2009-2020", "Mehr zum Thema"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://1hundetagebuch.wordpress.com/2019/10/31/nach-viel-zu-langer-zeit-mal-wieder/": {
        "file": "1hundetagebuch.wordpress.com.langer.html",
        "author": "Donald Townsend",
        "title": "Nach viel zu langer Zeit mal wieder",
        "date": "2019-10-31",
        "description": "Ich könnte glatt ein schlechtes Gewissen bekommen, wenn ich sehe, wie lange es her ist, dass ich das letzte Mal hier über meine Hunde geschrieben habe. Es gab Zeiten, da habe ich mehrmals die Woche…",
        "categories": ["Tagebuch"],
        "tags": ["amiga", "dogs", "floppy", "Hunde", "Hundeleben", "Mesty"],
        "with": [
            "Ich könnte glatt ein schlechtes Gewissen",
            "So muss Mesty jetzt Pillen nehmen",
            "Vielleicht muss man die Dosis des",
        ],
        "without": ["Share this:", "Kommentar verfassen", "Ein Blog über die Abenteue"],
        "comments": [],
        "license": "CC BY 3.0",
        "region": "",
    },
    "http://www.steinhau.com/steinhau/wordpress/einmal-zahlen-alles-lesen/": {
        "file": "steinhau.com.zahlen.html",
        "author": "HENRY STEINHAU",
        "title": "Einmal zahlen, alles lesen",
        "date": "2019-11-13",
        "description": "",
        "categories": ["Aktuell"],
        "tags": ["digitalabo", "flatrate", "Journalismus", "paywal", "Verlage"],
        "with": [
            "Hinweis: Der nachfolgende Artikel mitsamt der telefonisch",
            "Der Ruf nach einer Flatrate",
            "sowohl in der Browser-Version als auch in der App",
            "Zugang zu einer Zielgruppe ermöglicht",
        ],
        "without": [
            "Schreibe einen Kommentar",
            "Deine E-Mail-Adresse wird nicht",
            "um Spam zu reduzieren",
            "Alle Rechte beim Autoren",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.pointofsail-kiel.de/artikel/ben-wilson-surf.html": {
        "file": "pointofsail-kiel.de.wilson.html",
        "author": "",
        "title": "Ben Wilson Surf",
        "date": "2019-06-20",
        "description": "So manch einer der eingefleischten Waverider kennt sie schon, die kompromisslos auf Waveriding ...",
        "categories": [],
        "tags": [],
        "with": ["So manch einer der eingefleischten", "We are 100% committed to", "Our search for perfection never ends"],
        "without": ["Bei uns wirst du frei nach dem Motto", "Folge uns auch in den sozialen", "Kontakt"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://feuerwehrtaucher-oldenburg.de/bootsdienst/ausbildung.html": {
        "file": "feuerwehrtaucher-oldenburg.de.ausbildung.html",
        "author": "",
        "title": "Bootsdienst Ausbildung",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Die Bootsführerausbildung in der Feuerwehr",
            "Wichtig ist die Fähigkeit, eine",
            "Auch das slippen der Boote an",
        ],
        "without": ["Rettungsschwimmen"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://bummfilm.de/page/index.php?scroll=%DCber": {
        "file": "bummfilm.de.über.html",
        "author": "",
        "title": "Über uns",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Die bumm film GmbH bietet", "und wurde im Laufe der Zeit", "Web und Live-Entertainment"],
        "without": ["Kontakt", "Leistungen", "Lightbox2 © Lokesh Dhakar"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://denkmalpraxismoderne.de/studentendorf-schlachtensee-berlin/": {
        "file": "denkmalpraxismoderne.de.studentendorf.html",
        "author": "",
        "title": "Studentendorf Schlachtensee Berlin",
        "date": "",
        "description": "Ein Beitrag auf DenkmalPraxisModerne, Schlagwort(e): Berlin.",
        "categories": [],
        "tags": [],
        "with": [
            "Freie Universität Berlin, Land Berlin",
            "Erster Bauabschnitt: 21 ein- bis dreigeschossige",
            "Erstellung eines Parkpflegewerks von Uwe",
        ],
        "without": ["Wüstenrot Stiftung", "Kanzlerbungalow Bonn", "Alle Sanierungsbeispiele"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.gv-bayern.de/standard/artikel/der-genossenschaftsverband-bayern-im-portraet-775": {
        "file": "gv-bayern.de.portraet.html",
        "author": "",
        "title": "Der Genossenschaftsverband Bayern im Porträt",
        "date": "",
        "description": "Der Genossenschaftsverband Bayern (GVB) vertritt die Interessen der genossenschaftlichen Unternehmen im Freistaat.",
        "categories": [],
        "tags": [],
        "with": [
            "Der Genossenschaftsverband Bayern (GVB) vertritt",
            "Wir sind der gesetzliche Prüfungsverband",
            "unserer Mitglieder und verschaffen ihnen so Gehör",
        ],
        "without": ["Meldungen", "Meist gelesene Beiträge", "Historischer Verein"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.interscenar.io/politik/eindruecke/was-wir-ueber-uns-nicht-hoeren-wollen": {
        "file": "interscenar.io.hoeren.html",
        "author": "Gàbor Muniér",
        "title": "Was wir über uns nicht hören wollen",
        "date": "2019-03-03",
        "description": "Merkel: Warum alles gut ist wie&#039;s ist | Falscher Aktionismus ist schlimmer als Keiner",
        "categories": ["Politik", "Eindrücke", "Inland"],
        "tags": ["Merkel", "Vorwurfspolitik", "Kanzlerin", "Sündenbock"],
        "with": [
            "Viele ahnen es eigentlich schon, aber keiner",
            "So wie wir heute mit zwischenmenschlichen",
            "Und jetzt lassen Sie doch mal",
        ],
        "without": [
            "Den Artikel mit anderen teilen/diskutieren:",
            "hier bin ich eigentlich nur zufällig",
            "Theater- und Filmschauspielerin aus 2 Welten",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://mediaarchitecture.de/jens-weber/": {
        "file": "mediaarchitecture.de.weber.html",
        "author": "",
        "title": "Jens Weber",
        "date": "",
        "description": "Ausgew&auml;hlte Arbeiten von Jens Weber und Andreas Wolter aus den Bereichen MediaArchitecture, Interaction Design, Physical Computing und interaktive Architektur.",
        "categories": [],
        "tags": [],
        "with": [
            "1997 Medientechnik-Studium",
            "Umsetzung von über 70 kommerziellen Multimediaprojekten",
            "Nominierung Deutscher Multimedia Award",
        ],
        "without": ["Alle Inhalte unterliegen", "Projekte"],
        "comments": [],
        "license": "CC BY-NC-SA 2.0 DE",
        "region": "DE",
    },
    "https://www.deviante-pfade.de/unbefriedigt/": {
        "file": "deviante-pfade.de.unbefriedigt.html",
        "author": "Aureliana",
        "title": "Unbefriedigt",
        "date": "2020-01-08",
        "description": "Unbefriedigt-sein kann sich ziemlich doof anfühlen. Wir erläutern, wie man oder frau am besten damit umgeht und was die Laune wieder hebt.",
        "categories": ["Gefühle"],
        "tags": ["kein sex", "strategien", "umgang", "unbefriedigt"],
        "with": [
            "Wir alle haben Bedürfnisse. Mal mehr",
            "Die Situationen, in denen man unbefriedigt",
            "Ich denke, dass bei mir auch durch den neu",
        ],
        "without": [
            "Rückblick auf das Blog-Jahr 2019",
            "Durch die weitere Nutzung der Seite",
            "Orgasmuskontrolle und Sexentzug",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://seglerblog.stössenseer.de/haltet-unsere-gewaesser-sauber/": {
        "file": "seglerblog.stössenseer.de.sauber.html",
        "author": "",
        "title": "»Haltet unsere Gewässer sauber!«",
        "date": "2020-02-23",
        "description": "Und noch mal was mit Wasser: »Haltet unsere Gewässer sauber!« Der Plakatwettbewerb für Kinder findet in 2020 bereits zum 6. Mal statt. Kinder zwischen 6 und 12 Jahren sind aufgerufen, sich am Wettbewerb zu mit ihren bunten und kreativen Ideen zu beteiligen. Gestalte ein Plakat unter dem Motto: »Haltet unsere&hellip;",
        "categories": ["Infos"],
        "tags": ["Berlin", "Gewässer", "Plakatwettbewerb", "sauber"],
        "with": ["Der Plakatwettbewerb für Kinder", "Gestalte ein Plakat unter dem", "an die Berliner*innen"],
        "without": ["Finde im SeglerBlog!", "Verwandte Beiträge", "Schreibe einen Kommentar"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.ihrwebprofi.at/2011/09/17/publikumsvoting-beim-wiener-content-award-gestartet/": {
        "file": "ihrwebprofi.at.publikumsvoting.html",
        "author": "",
        "title": "Publikumsvoting beim Wiener Content Award gestartet",
        "date": "2011-09-17",
        "description": "Beim ContentAward.at, der vom ZIT — Technologieagentur der Stadt Wien zur Förderung der Wiener Content- und Medienszene durchgeführt wird, ...",
        "categories": ["News", "open3"],
        "tags": [],
        "with": [
            "Beim ContentAward.at, der",
            "Die „Toilet Map Vienna„, die erste App",
            "Das Online-Voting läuft von 14. September",
        ],
        "without": ["Kommentar hinzufügen", "Kategorie: News, open3", "Derzeit noch keine Kommentare"],
        "comments": [],
        "license": "CC BY-SA 3.0 AT",
        "region": "AT",
    },
    "https://mitternachtskabinett.wordpress.com/2016/06/19/geister-spuk-gentrifizierung/": {
        "file": "mitternachtskabinett.wordpress.com.gentrifizierung.html",
        "author": "",
        "title": "Geister, Spuk & Gentrifizierung (#5)",
        "date": "2016-06-19",
        "description": "MP3-DOWNLOAD (01:00 h)",
        "categories": ["Gesellschaft & Kultur"],
        "tags": ["Frankenstein", "Geister", "Spuk"],
        "with": [
            "Unser heutiger Gast berichtet von",
            "Wie wirkt sich die Gentrifizierung",
            "Als Monster der Woche besprechen",
        ],
        "without": ["Gib deine E-Mail-Adresse ein", "Ähnliche Beiträge", "Kommentar verfassen"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.aussengedanken.de/streit-ums-feuerholz/": {
        "file": "aussengedanken.de.feuerholz.html",
        "author": "Von Roland Brockmann und Sebastian Drescher",
        "title": "Streit ums Feuerholz",
        "date": "2017-02-13",
        "description": "MIGRATION &#8211; Probleme zwischen Einheimischen und Flüchtlingen sind auch in Afrika ein Thema &#8211; wie Kenia mit der Herausforderung umgeht Von Roland Brockmann und Sebastian Drescher",
        "categories": [
            "Afrika",
            "Entwicklungshilfe",
            "Kenia",
            "Länder",
            "Media",
            "Migration",
            "Flucht & Vertreibung",
            "Themen",
            "Videos",
        ],
        "tags": ["Flüchtlinge, Migration"],
        "with": [
            "Nur eine kurze Sandpiste",
            "Und nicht nur sie. Einige Hundert Kilometer",
            "Immerhin 1,6 Millionen Euro Hilfsgelder",
        ],
        "without": ["Schreibe einen Kommentar", "Lars Bauer (links im Bild) und Jens", "Unterstützen Sie uns"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://1337kultur.de/2020/folge-70-star-trek-picard/": {
        "file": "1337kultur.de.picard.html",
        "author": "",
        "title": "Folge 70: Star Trek: Picard",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Thema dieser Folge ist", "fünften Episode der", "Wir werden spoilern"],
        "without": [
            "Leet-Kultur – Kultur aus der Nerdperspektive",
            "Hohe Qualität Livestream in hoher Qualität (128 kbit/s)",
            "Lizenz des Podcasts",
        ],
        "comments": ["Vielen, vielen Dank für die tolle", "Logbuch: Nachtrag, die"],
        "license": "CC BY-SA 3.0 DE",
        "region": "DE",
    },
    "https://insubordinant.wordpress.com/2015/08/11/need-for-speed/": {
        "file": "insubordinant.wordpress.com.speed.html",
        "author": "",
        "title": "Need for Speed",
        "date": "2015-08-11",
        "description": "Der kleine Junge bremst abrupt vor mir ab: &#8222;Ich soll dir von Gerhard sagen, er hätte dein Mädel auf dem Hof.&#8220; Ich schaue ihm verwundert hinterher wie er den Flur der Kita entlang rennt,…",
        "categories": ["Everything but the kitchen sink", "Ivy vs. the world principle", "What a wonderful world"],
        "tags": ["Bandit GSF 600", "Gone Wild Mistress", "Survive unscathed", "Woman loves man"],
        "with": [
            "Der kleine Junge bremst abrupt vor mir",
            "Kein Kerl ist das wert, Kleines",
            "dem kleinen Polo so viel Gas wie er gerade",
        ],
        "without": ["5 Bloggern gefällt das.", "Gedanken zu “Need for Speed”", "Veröffentlicht in:"],
        "comments": [
            "Das ist ein wirklich gut geschriebener Text.",
            "wusste gar nicht dass du sowas auch",
            "eine richtige karre zickt nicht ",
        ],
        "license": "CC BY-NC-SA",
        "region": "",
    },
    "http://rueda.wikidot.com/enchufla": {
        "file": "rueda.wikidot.com.enchufla.html",
        "author": "",
        "title": "Enchufla Figuren",
        "date": "2008-03-23",
        "description": "",
        "categories": [],
        "tags": ["cubanito", "enchufla", "lacucaracha", "switch"],
        "with": [
            "Platzwechsel, langsam erklärt",
            "Start, wenn man rechts auf rechts ist",
            "zieht die Folgende den Führenden an der Hüfte zurück",
        ],
        "without": [
            "Unless otherwise stated, the content of this page",
            "Other interesting sites",
            "Ansagen nach Grundschritt",
        ],
        "comments": [],
        "license": "CC BY-SA 3.0",
        "region": "",
    },
    "http://www.klaenge-des-verschweigens.de/film/geschichte/": {
        "file": "klaenge-des-verschweigens.de.geschichte.html",
        "author": "Klaus Stanjek",
        "title": "Klänge des Verschweigens",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Das „schwarze Schaf“ unserer Familie",
            "Durch das Aufblättern eines Familiengeheimnisses",
            "Wobei Musik fundamental beteiligt wird",
        ],
        "without": ["Unterstütze das Projekt:", "Ein detektivisches Dokumentarprojekt", "Gefördert durch:"],
        "comments": [],
        "license": "CC BY-NC-SA 3.0",
        "region": "DE",
    },
    "https://trails.de/mountainbikeregion/ischgl/": {
        "file": "trails.de.ischgl.html",
        "author": "Ralf Glaser",
        "title": "Ischgl",
        "date": "",
        "description": "Ischgl hat sich im Sommer vor allem als Freeride Revier einen Namen gemacht. Das Ski Resort im Paznaun punktet mit einer guten Seilbahn Infrastruktur und alpinen Trails. Nach dem Motto Mountainbike als Funsport ist hier der Freerider König – in Ischgl findet er das perfekte Verhältnis aus viel bergab zu wenig bergauf!",
        "categories": [],
        "tags": [],
        "with": [
            "Ischgl hat sich im Sommer vor allem als Freeride Revier",
            "Wer MTB am liebsten bergab betreibt ist in Ischgl in seinem Element",
            "heißer Tipp für die warmen Monate",
        ],
        "without": ["Bike Hotels", "Webdesign und alle Inhalte"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://changenow.de/andre-loibl/": {
        "file": "changenow.de.loibl.html",
        "author": "André Loibl",
        "title": "",
        "date": "",
        "description": "André Loibl ​Der beliebteste Mindset-Coach mit Freude und Sönnchen reinlassen- Für Dein stabiles und großartiges Business, das Menschen bewegt und einen echten Unterschied in der Welt macht -Hey, André hier! :-)Du willst mich besser kennen lernen? Prima! Fangen wir mit den grundlegenden Fragen an:Wofür stehe ich?",
        "categories": [],
        "tags": [],
        "with": ["1. Freude und Leichtigkeit.", "Ich habe ein kurzes Video gemacht", "offen und neugierig sind"],
        "without": ["Weiter", "Hier kostenlos anmelden", "KANGA PROJECT"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://zulang.wordpress.com/2015/12/12/3-jahre-legalisierte-genitalverstuemmelung/": {
        "file": "zulang.wordpress.com.genitalverstuemmelung.html",
        "author": "HansG",
        "title": "3 Jahre legalisierte Genitalverstümmelung",
        "date": "2015-12-12",
        "description": "Gemeint ist natürlich das, was im Allgemeinen unter dem Euphemismus Beschneidung bekannt ist. Es handelt sich schon alleine deshalb um einen Euphemismus, da bei der Zirkumzision nicht einfach nur e…",
        "categories": ["Männer", "Recht"],
        "tags": ["Beschneidung", "Genitalverstümmelung"],
        "with": [
            "Einen ausführlichen Einstieg",
            "Befürworter der Beschneidung bagatellisieren",
            "Dem lässt sich kaum etwas hinzufügen",
        ],
        "without": ["Die Kommentarfunktion ist geschlossen", "Share this:", "Ähnliche Beiträge"],
        "comments": [
            "Das stimmt überhaupt nicht",
            "Am häufigsten werden in Deutschland Beschneidungen von muslimischen Eltern",
            "Je nach islamischer Rechtsschule wird die Beschneidung allerdings nicht einheitlich",
        ],
        "license": "",
        "region": "",
    },
    "https://surfguard.wordpress.com/2016/11/01/ich-las-sah-hoerte-medien-im-oktober-2016/": {
        "file": "surfguard.wordpress.com.medien.html",
        "author": "surfguard",
        "title": "Ich las, sah, hörte: Medien im Oktober 2016",
        "date": "2016-11-01",
        "description": "TV/Serie/DVD Amanda Knox Ich habe den Fall Amanda Knox und die Prozesse gegen sie, Raffaele Sollecito und Rudy Guede seinerzeit natürlich wahrgenommen, aber nicht besonders aufmerksam verfolgt. Die…",
        "categories": [],
        "tags": [],
        "with": [
            "Rudy Guede seinerzeit natürlich wahrgenommen",
            "Muss man gesehen haben. Augenöffnend.",
            "Eine neue Platte von Wilco also",
        ],
        "without": ["Diesen Artikel teilen:", "Ähnliche Beiträge", "Schreibe einen Kommentar: "],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://litradio.net/die-autorin-nora-bossong-im-gespraech-ueber-ihren-roman-schutzzone/": {
        "file": "litradio.net.bossong.html",
        "author": "Nicole Collignon",
        "title": "Die Autorin Nora Bossong im Gespräch über ihren Roman “Schutzzone”",
        "date": "2020-02-22",
        "description": "",
        "categories": [],
        "tags": [
            "Gespräch",
            "Ham.Lit",
            "HAM.LIT 2020",
            "Interview",
            "Literatur",
            "Nora Bossong",
            "Politik",
            "Schutzzone",
            "Audio",
        ],
        "with": [
            "Nora Bossong erzählt von der Arbeit",
            "ihre eigene Rolle als UN-Beauftragte",
            "Positionierung und Hoffnung in der Desillusion.",
        ],
        "without": ["LANGE NACHT JUNGER LITERATUR UND MUSIK", "Sharen mit:", "Ähnliche Beiträge"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.japantimes.co.jp/news/2020/02/18/national/crime-legal/6000-surgical-masks-stolen/": {
        "file": "japantimes.co.jp.surgical.html",
        "author": "JIJI",
        "title": "Losing face: 6,000 surgical masks stolen from Kobe hospital",
        "date": "2020-02-18",
        "description": "A total of 6,000 surgical masks have been lost at a hospital in Kobe, it was learned Tuesday. The Hyogo Prefectural Police is investigating the incident as",
        "categories": [],
        "tags": [],
        "with": [
            "The incident has occurred at a time when Japan is seeing a shortage of face masks",
            "Four of the 12 boxes of masks were gone",
            "KOBE – A total of 6,000 surgical masks",
        ],
        "without": ["Do masks offer protection from new coronavirus? It depends", "Mail the editor", "RELATED STORIES"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.hearya.com/2006/12/04/hit-paraders-top-100-metal-vocalists-of-all-time/": {
        "file": "hearya.com.metal.html",
        "author": "OZ",
        "title": "Hit Parader’s Top 100 Metal Vocalists of All Time",
        "date": "2006-12-04",
        "description": "I&#8217;m not much of a metal guy these days, but I dabbled in high school. I heard about this list on the radio this morning and had to look it up. It&#8217;s bound for controversy. Freddy Mercury at #6? Scott [&hellip;]",
        "categories": [],
        "tags": [],
        "with": ["100. Ray Gillen", "Keith Caputo, Life of Agony", "I’m not much of a metal guy these days, but I dabbled"],
        "without": ["Leave a Comment", "Recent Comments", "Blogroll"],
        "comments": [
            "Really, no Shagrath?",
            "Ok,so you put Dani Filth,the ”Ripper” and other few screamers",
            "Where’s Max Cavalera??",
        ],
        "license": "",
        "region": "",
    },
    "http://thenervousbreakdown.com/tanderson/2011/07/the-loneliest-woman-in-the-world-an-appreciation-of-hearts-alone/": {
        "file": "thenervousbreakdown.com.loneliest.html",
        "author": "Tim Anderson",
        "title": "The Loneliest Woman in the World: An Appreciation of Heart’s “Alone”",
        "date": "2011-07-11",
        "description": "Tim Anderson thinks the best way to appreciate Heart&#8217;s 1987 operatic chartbuster is while sitting in a darkened living room turning on and off the lamp.",
        "categories": [],
        "tags": ["ann wilson", "drama", "eighties", "heart", "loneliness", "Music", "nancy wilson", "power ballads", "Rock"],
        "with": [
            "Fans of Heart, the rawk band",
            "I stayed, because Ann was really about to deliver",
            "And of course they did get through it.",
        ],
        "without": [
            "Leave a Reply",
            "responses to “The Loneliest Woman in",
            "TIM ANDERSON has done many amazing things in his short life.",
        ],
        "comments": [
            "“How can you not hear Ann Wilson when she’s singing at you?!”",
            "The Wilson sisters are goddesses.",
            "Fischer and the original bass player it was",
        ],
        "license": "",
        "region": "",
    },
    "https://www.cbsnews.com/news/2020-presidential-election-south-carolina-black-voters-democrats-joe-biden/": {
        "file": "cbsnews.com.carolina.html",
        "author": "",
        "title": "Black voters in South Carolina are crucial for Democratic candidates",
        "date": "2020-02-24",
        "description": "One group of now mostly senior citizen organizers, known as The Reckoning Crew, is backing Joe Biden.",
        "categories": [],
        "tags": [],
        "with": [
            "The stakes are high for all of the candidates ahead of Tuesday",
            "At a family fun run in the state",
            "Asked why she called the group the Reckoning Crew,",
        ],
        "without": ["© 2020 CBS Interactive Inc. All Rights Reserved.", "Email", "Black voters in S.C. on the 2020 Democrats"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://pagesix.com/2020/02/24/former-wh-press-secretary-dee-dee-myers-exits-warner-bros-role/": {
        "file": "pagesix.com.myers.html",
        "author": "Ian Mohr",
        "title": "Former WH press secretary Dee Dee Myers exits Warner Bros. role",
        "date": "2020-02-24",
        "description": "Myers, a Bill Clinton staffer, said “I’m going to take some time to figure out what’s next. I don’t have any set ideas.",
        "categories": [],
        "tags": ["bill clinton", "warner bros."],
        "with": [
            "Dee Dee Myers — a White House press secretary for Bill Clinton",
            "“I’m going to take some time to figure out what’s next",
            "Her last day is April 1",
        ],
        "without": ["Getty Images", "Filed under", "Most Popular This Week"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://tonedeaf.thebrag.com/record-of-the-week-luboku-pale-blue-dot-lift-off/": {
        "file": "tonedeaf.thebrag.com.luboku.html",
        "author": "Poppy Reid",
        "title": "Record of The Week: Luboku, ‘Pale Blue Dot / Lift Off’",
        "date": "2020-02-21",
        "description": "It&#039;s no coincidence that the 30 year anniversary of the day NASA’s Voyager 1 space probe took a picture of Earth was the same day Luboku released his new",
        "categories": [],
        "tags": [],
        "with": [
            "It’s no coincidence that the 30 year anniversary of the da",
            "Still need convincing on why it’s our top record this week?",
            "From its hypnotic synths to its brooding melodies, Luboku takes",
        ],
        "without": [
            "Grimes releases her new album Miss Anthropocene",
            "Grimes has released her fifth album",
            "Discover our latest editorial picks",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://it-learner.de/wenn-das-netzwerk-unter-windows-10-sehr-langsam-ist-koennte-das-abschalten-der-autotuning-funktion-abhilfe-schaffen/": {
        "file": "it-learner.de.autotuning.html",
        "author": "Markus Elsberger",
        "title": "Wenn das Netzwerk unter Windows 10 sehr langsam ist, könnte das Abschalten der Autotuning Funktion Abhilfe schaffen.",
        "date": "2019-05-16",
        "description": "Wenn das Netzwerk unter Windows 10 sehr langsam ist, könnte das mit der Autotuning Funktion zusammen hängen. So kann man dies prüfen!",
        "categories": ["Netzwerk", "Windows"],
        "tags": ["Cmd", "Installation", "Netzwerk", "Windows"],
        "with": [
            "Mit Windows Vista wurde damals die sogenannte Autotuning Funktion",
            "netsh interface tcp set global autotuninglevel=normal",
            "Jedoch gibt es anscheinend Probleme mit älteren Routern",
        ],
        "without": ["Hole dir jetzt das kostenlose Ebook.", "2 Kommentare", "Zappen ... Rätsel : entdeckt"],
        "comments": ["Wenn ich den o.g. syntax eingebe", "Vorab habe ich eine cmd als Administrator geöffnet"],
        "license": "",
        "region": "",
    },
    "https://de.induux.com/4press/energiezaehler-m-bus-mod-bus-ethernet-mid-3999/": {
        "file": "de.induux.com.energiezaehler.html",
        "author": "",
        "title": "Neue Energiezähler mit M-Bus, Mod-Bus, Ethernet und MID",
        "date": "2018-04-20",
        "description": "Lovato Elctric erweitert sein umfangreiches Produktprogramm im Bereich E-Managemnt jetzt mit Geräte die für den deutschen Markt besonders interessant sind.",
        "categories": [],
        "tags": [],
        "with": [
            "Lovato Elctric erweitert sein umfangreiches Produktprogramm im Bereich E-Managemnt jetzt mit Geräte die für den deutschen Markt besonders interessant sind.",
            "0,5s Genauigkeitsklasse",
            "Nennversorgungsspannung: 380...415VAC (L-L)",
        ],
        "without": ["Angebote Lovato Electric", "Die internationale Industrie-Plattform", "Karriere"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://aoc.media/opinion/2019/12/09/pour-le-neoliberalisme-la-retraite-est-un-archaisme/": {
        "file": "aoc.media.archaisme.html",
        "author": "Barbara Stiegler",
        "title": "Pour le néolibéralisme, la retraite est un archaïsme",
        "date": "2019-12-10",
        "description": "Pour le néolibéralisme, la retraite ne peut être qu’un archaïsme, une sorte de déviance inadaptée, qui nous fait prendre du retard dans la compétition mondiale, et dont l’État lui-même doit programmer la disparition progressive. L’affrontement qui se met en place ces jours-ci dépasse donc les questions techniques de « réforme systémique » ou d’« ajustement paramétrique » dont nous parle le jargon des experts. Il oppose, bien plus profondément, deux visions incompatibles de l’avenir du vivant et de nos rythmes de vie.",
        "categories": [],
        "tags": [],
        "with": [
            "Pour le néolibéralisme, la retraite",
            "les grandes grèves de 1995 furent",
            "Pour réaliser ce programme, il impose",
        ],
        "without": ["Pour lire la suite", "Pour accéder en illimité", "Pour rester informé inscrivez-vous à la newsletter"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "http://www.regards.fr/politique/article/deux-ans-et-demi-en-macronie-9-mises-en-examen-10-enquetes-en-cours-et-2": {
        "file": "regards.fr.enquetes.html",
        "author": "Loïc Le Clerc",
        "title": "Deux ans et demi en Macronie : une condamnation, dix mises en examen et six enquêtes en cours",
        "date": "2018-09-30",
        "description": "On vous aurait bien fait un top 10 des macronistes confront&#233;s &#224; la justice, mais ils sont d&#233;j&#224; 20. Article mis &#224; jour le 7 janvier 2020. S&#039;il (...)",
        "categories": ["Accueil"],
        "tags": ["La République en marche", "Justice", "Emmanuel Macron"],
        "with": ["seule promesse du candidat Macron, la", "Le 6 août 2019, le député", "Anticor a porté plainte pour"],
        "without": ["Qui êtes-vous ?", "Pour créer des paragraphes, laissez simplement des lignes vides.", "Vos réactions"],
        "comments": [
            "Articles très bien faits et qui nous montre",
            ".iL faut etre sensible pour etre intéligent",
            "Rien de neuf donc....",
        ],
        "license": "",
        "region": "",
    },
    "https://newrepublic.com/article/155970/collapse-neoliberalism": {
        "file": "newrepublic.com.neoliberalism.html",
        "author": "Ganesh Sitaraman",
        "title": "The Collapse of Neoliberalism",
        "date": "2019-12-23",
        "description": "The long-dominant ideology brought us forever wars, the Great Recession, and extreme inequality. Good riddance.",
        "categories": [],
        "tags": [],
        "with": [
            "With the 2008 financial crash and the Great Recession",
            "Start with the economy. Over the course",
            "The central question of our time",
        ],
        "without": ["Ganesh Sitaraman is a professor at Vanderbilt Law School", "Read More", "Most Popular"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.tdg.ch/suisse/berne-interdit-chlorothalonil/story/18348200": {
        "file": "tdg.ch.chlorothalonil.html",
        "author": "",
        "title": "Berne interdit désormais le chlorothalonil",
        "date": "2019-12-12",
        "description": "L'Office fédéral de l'agriculture a décidé de retirer l'autorisation de mise en circulation des produits contenant ce fongicide avec effet immédiat.",
        "categories": [],
        "tags": [],
        "with": [
            "Le chlorothalonil sera interdit",
            "Le chlorothalonil est une substance active utilisée",
            "Les Suisses pourraient également se prononcer sur",
        ],
        "without": [
            "Avez-vous apprécié cet article?",
            "Plus de sujets",
            "Le canton de Berne veut interdire le chlorothalonil ",
        ],
        "comments": ["Un effet immédiat pour un effet long terme du poison"],
        "license": "",
        "region": "",
    },
    "https://www.gala.fr/l_actu/news_de_stars/jean-paul-delevoye-monsieur-retraites-du-gouvernement-jacques-chirac-lui-donnait-un-surnom-peu-flatteur_439447": {
        "file": "gala.fr.surnom.html",
        "author": "Marie Merlet",
        "title": "Jean-Paul Delevoye, monsieur retraites du gouvernement : Jacques Chirac lui donnait un surnom peu flatteur",
        "date": "2019-12-09",
        "description": "Chargé de porter la réforme des retraites, Jean-Paul Delevoye a su gagner la confiance d'Emmanuel Macron. Ancien chiraquien nommé ministre, il n'ét...",
        "categories": [],
        "tags": ["Gala politique", "président de la republique", "Homme politique"],
        "with": [
            "Chargé de porter la réforme des retraites",
            "Chirac le surnommaitle Grand Con, parce",
            "un dirigeant de LREM dans un portrait",
        ],
        "without": ["Crédits photos : Bestimage", "Articles les plus lus", "L'actu"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.chip.de/downloads/BestCrypt_13003274.html": {
        "file": "chip.de.bestcrypt.html",
        "author": "",
        "title": "BestCrypt",
        "date": "",
        "description": "BestCrypt  9.04 Englisch: BestCrypt erstellt virtuelle Laufwerke, deren Inhalt zusätzlich verschlüsselt wird.",
        "categories": [],
        "tags": [],
        "with": [
            "kann verschlüsselte, virtuelle Laufwerke anlegen",
            "Der integrierte Anti-Keylogger und",
            "Homepage des Herstellers nachlesen",
        ],
        "without": [
            "BestCrypt : Alternative Downloads",
            "UNSERE SHOPPING-GUTSCHEINE",
            " Für Links auf dieser Seite erhält CHIP",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.elle.de/plateau-sneaker-trend": {
        "file": "elle.de.sneaker.html",
        "author": "Alexa von Heyden",
        "title": "Sneaker-Trend: Plateau-Sohlen sorgen für ein neues Hochgefühl",
        "date": "2019-06-19",
        "description": "Alexander McQueen bis Adidas: Für den Sommer 2019 setzen die einflußreichsten Labels auf Plateau-Sneaker. Mehr über den Trend auf ELLE.de!",
        "categories": ["Home", "Fashion", "Trends & Styling"],
        "tags": [],
        "with": [
            "am meisten getragenen Lieblingsteilen in deiner Garderobe",
            "Die Lösung für diese modische Herausforderung liegt in der",
            "So geht die Tendenz nach Dad Sneaker und Ugly Sneaker",
        ],
        "without": ["Net Sustain: Die neue Plattform von", "Zum Shop", "Affiliatelink"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.management-circle.de/blog/remote-support-mit-smart-glasses/": {
        "file": "management-circle.de.glasses.html",
        "author": "Isabella Beyer",
        "title": "Remote Support mit Smart Glasses – AR-Kundenservice der Zukunft?",
        "date": "2019-07-25",
        "description": "Erfahren Sie in diesem Blog-Artikel, welche Vorteile Remote Support mit Smart Glasses in Verbindung mit Augmented Reality für Unternehmen haben kann?",
        "categories": ["Blogartikel", "Digitalisierung"],
        "tags": ["Augmented Reality", "Kundenservice", "Remote Support", "Smart Glasses"],
        "with": [
            "Wie Sie sehen bietet der Remote Support mit Smart Glasses",
            "Die Arbeit der Mitarbeiter im Karosseriebau vor Ort wird durch Smart Glasses",
            "In der Industrie wird der Remote Support mit Smart Glasses immer beliebter",
        ],
        "without": [
            "Als Content Marketing Managerin betreue ich",
            "Diese neuen Entwicklungen sollten Sie kennen",
            "In unserem Seminar „Augmented Reality“ erarbeiten Sie anhand verschiedener Experience",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.it-finanzmagazin.de/creditshelf-kooperiert-mit-finleap-und-plant-akquisition-der-valendo-gmbh-90871/": {
        "file": "it-finanzmagazin.de.creditshelf.html",
        "author": "John v. Berenberg-Consbruch",
        "title": "creditshelf kooperiert mit finleap und plant Akquisition der Valendo GmbH",
        "date": "2019-06-20",
        "description": "Die geplante Kooperation von creditshelf mit finleap stützt alle drei...",
        "categories": ["FINTECH"],
        "tags": [],
        "with": [
            "Die geplante Kooperation von creditshelf mit finleap",
            "Beide Parteien streben den Abschluss des Erwerbs der Valendo",
            "creditshelf eröffnet die geplante Akquisition der Valendo GmbH",
        ],
        "without": ["Jede Woche neu:", "(Noch keine Bewertungen)", "Auch interessant"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://abenteuer-astronomie.de/astrofoto-community/plejaden-m45-2/": {
        "file": "abenteuer-astronomie.de.plejaden.html",
        "author": "Helmut Rubik",
        "title": "Plejaden, M45",
        "date": "2019-09-17",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Nun nicht im Staub, sondern mit ausgeprägten Sternstrahlen",
            "Art der Aufnahme: Digitalfoto",
            "Kasberg im Frankenland",
        ],
        "without": [
            "Hinterlasse jetzt einen Kommentar",
            "Sie wollen Deep-Sky-Objekte am Himmel",
            "Abenteuer Astronomie war eine Zeitschrift",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.neos.eu/wir-sind-neos": {
        "file": "neos.eu.wir.html",
        "author": "",
        "title": "Wir sind NEOS",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Wir NEOS stehen seit 2012 für ein Neues Österreich",
            "Seit dem Bestehen von NEOS mussten wir ein paar Verluste",
            "Demokratie braucht Parteien, die transparent",
        ],
        "without": ["Erfahre mehr", "Ich stimme der elektronischen Verarbeitung", "Folge uns"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/": {
        "file": "blog.wordpress.com.diverse.html",
        "author": "Andrea Middleton",
        "title": "Want to See a More Diverse WordPress Contributor Community? So Do We.",
        "sitename": "The WordPress.com Blog",
        "date": "2019-06-19",
        "description": "More diverse speakers at WordCamps means a more diverse community contributing to WordPress — and that results in better software for everyone.",
        "categories": [],
        "tags": [],
        "with": ["Why WordCamps?", "which makes WordPress better for more people.", "Get in touch with Jill"],
        "without": ["Missing out on the latest", "Opens in new window", "Jill Binder, speaking at a WordCamp"],
        "comments": ["Thank you.", "Amazing!!!", "Wow,"],
        "license": "",
        "region": "",
    },
    "https://creativecommons.org/about/": {
        "file": "creativecommons.org.html",
        "author": "",
        "title": "What we do - Creative Commons",
        "sitename": "Creative Commons",
        "date": "2016-05-22",
        "description": 'What is Creative Commons? Creative Commons helps you legally share your knowledge and creativity to build a more equitable, accessible, and innovative world. We unlock the full potential of the internet to drive a new era of development, growth and productivity. With a network of staff, board, and affiliates around the world, Creative Commons provides … Read More "What we do"',
        "categories": [],
        "tags": [],
        "with": ["With a network of", "Our work is to build", "Our work spans a variety"],
        "without": ["Connect with Creative Commons", "Honoring Our Friend", "In this section"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.creativecommons.at/faircoin-hackathon": {
        "file": "creativecommons.at.faircoin.html",
        "author": "rasos",
        "title": "FairCoin hackathon beim Sommercamp",
        "sitename": "",
        "date": "2017-07-24",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["Wir waren massgeblich", "link is external"],
        "without": ["Publikationen in Forschung", "Vorheriges", "Nach fast zwei Jahren Arbeit"],
        "comments": [],
        "license": "CC-BY",
        "region": "AT",
    },
    "https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/": {
        "file": "netzpolitik.org.abmahnungen.html",
        "author": "Markus Reuter",
        "title": "Die Cider Connection: Abmahnungen gegen Nutzer von Creative-Commons-Bildern",
        "sitename": "netzpolitik.org",
        "date": "2016-06-23",
        "description": "Seit Dezember 2015 verschickt eine Cider Connection zahlreiche Abmahnungen wegen fehlerhafter Creative-Commons-Referenzierungen. Wir haben recherchiert und legen jetzt das Netzwerk der Abmahner offen.",
        "categories": [],
        "tags": [],
        "with": [
            "Seit Dezember 2015",
            "VSGE",
            "Dazu muss das überholte Urheberrecht",
            "Dieser Artikel baut auf einer gemeinsamen Recherche",
        ],
        "without": [
            "23.06.2016",
            "Zum Vergrößern auf das Bild",
            "Markus Reuter beschäftigt sich",
            "Ist Videoüberwachung beim Zahnarzt",
            "Wir sind spendenfinanziert.",
        ],
        "comments": ["News vom 31.10.2018", "Hallo zusammen,", "Selbstverständlich darf man den Namen"],
        "license": "CC-BY-NC-SA",
        "region": "",
    },
    "https://www.befifty.de/home/2017/7/12/unter-uns-montauk": {
        "file": "befifty.montauk.html",
        "author": "Beate Finken",
        "title": "Das vielleicht schönste Ende der Welt: Montauk",
        "sitename": "BeFifty",
        "date": "2017-07-12",
        "description": "Ein Strand, ist ein Strand, ist ein Strand Ein Strand, ist ein Strand, ist ein Strand. Von wegen! In Italien ist alles wohl organisiert, Handtuch an Handtuch oder Liegestuhl an Liegestuhl. In der Karibik liegt man unter Palmen im Sand und in Marbella dominieren Beton und eine kerzengerade Promenade",
        "categories": ["Travel", "Amerika"],
        "tags": ["Long Island", "Montauk", "New York", "Hamptons"],
        "with": ["Im kurzen BeFifty Video", "Und hier einige Impressionen", "bodenständig und stilsicher"],
        "without": ["Um Ihnen ein besseres Nutzererlebnis", "auf Linie gebracht", "Tumblr"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.soundofscience.fr/1927": {
        "file": "soundofscience.fr.1927.html",
        "author": "Martin Clavey",
        "title": "Une candidature collective à la présidence du HCERES",
        "sitename": "The Sound Of Science",
        "date": "2020-01-20",
        "description": "En réaction à la candidature du conseiller recherche d&#039;Emmanuel Macron, Thierry Coulhon, à la présidence du Haut Conseil de l&#039;évaluation de la recherche et de l&#039;enseignement supérieur (HCERES) annoncée récemment, plus de 2500 chercheur·eus·e·s annoncent faire acte de candidature collectivement à la tête de l&#039;autorité administrative indépendante chargée de l&#039;évaluation de l’enseignement supérie ...",
        "categories": ["Politique scientifique française"],
        "tags": ["évaluation", "HCERES"],
        "with": ["En réaction à la candidature", "Une cible,", "Sans recherche autonome,"],
        "without": ["Image illustrative", "Votre adresse de messagerie", "Le montage du CNRS"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.theguardian.com/education/2020/jan/20/thousands-of-uk-academics-treated-as-second-class-citizens": {
        "file": "theguardian.com.academics.html",
        "author": "Richard Adams",
        "title": "Thousands of UK academics 'treated as second-class citizens'",
        "sitename": "the Guardian",
        "date": "2020-01-20",
        "description": "Report claims higher education institutions have created pool of low-paid staff for teaching and research",
        "categories": ["Higher education"],
        "tags": ["Academics", "Lecturers' pay", "Gig economy", "Students", "Trade unions", "Office for Students", "news"],
        "with": ["It calls on the", "But a spokesperson for"],  # , 'Report claims higher education institutions'
        "without": ["Available for everyone, funded by readers", "Make a contribution", "Striking members of the UCU"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://phys.org/news/2019-10-flint-flake-tool-partially-birch.html": {
        "file": "phys.org.tool.html",
        "author": "Bob Yirka",
        "title": "Flint flake tool partially covered by birch tar adds to evidence of Neanderthal complex thinkin",
        "sitename": "",
        "date": "2019-10-22",
        "description": "A team of researchers affiliated with several institutions in The Netherlands has found evidence in small a cutting tool of Neanderthals using birch tar. In their paper published in Proceedings of the National Academy of Sciences, the group describes the tool and what it revealed about Neanderthal technology.",
        "categories": ["Archaeology", "Fossils"],
        "tags": [],
        "with": ["Prior work has turned up", "the North Sea for most of its existence"],
        "without": ["Explore further", "Feedback to editors", "the very first glue"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://laviedesidees.fr/L-evaluation-et-les-listes-de.html": {
        "file": "laviedesidees.fr.evaluation.html",
        "author": "Florence Audier",
        "title": "L’évaluation et les listes de revues",
        "sitename": "La Vie des idées",
        "date": "2009-09-15",
        "description": "L&#039;&#233;valuation, et la place qu&#039;y occupe la bibliom&#233;trie, sont au c&#339;ur des d&#233;bats actuels. Les enjeux sont majeurs : seront dot&#233;es en cr&#233;dits les universit&#233;s consid&#233;rant la bibliom&#233;trie comme l&#039;indicateur supr&#234;me de l&#039;activit&#233; et de la qualit&#233; de la recherche. Or, comme le montre Florence Audier, les Fran&#231;ais ont d&#233;sign&#233; comme cible d&#039;excellence des revues auxquelles ils n&#039;acc&#232;dent pas, sauf r&#233;seaux particuliers. Voir en annexe : Place des fran&#231;ais et des europ&#233;ens parmi les &#171; publiants &#187; des revues d&#233;pouill&#233;es dans (...) ",  # description.startswith("L'évaluation, et la place")
        "categories": ["Essai", "Économie"],
        "tags": ["université", "indicateurs", "recherche", "évaluation"],
        "with": ["Depuis longtemps,", "Retour sur les revues de rang", "Quelques réflexions"],
        "without": [
            "enquêtes à propos des pratiques de publication",
            "Si vous souhaitez critiquer ou développer cet article",
            "Télécharger au format EPUB",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://gregoryszorc.com/blog/2020/01/13/mercurial%27s-journey-to-and-reflections-on-python-3/": {
        "file": "gregoryszorc.com.python3.html",
        "author": "Gregory Szorc",
        "title": "Mercurial's Journey to and Reflections on Python 3",
        "sitename": "gregoryszorc",
        "date": "2020-01-13",
        "description": "Description of the experience of making Mercurial work with Python 3",
        "categories": ["Python", "Programming"],
        "tags": [],
        "with": ["This effort began in earnest", "Within a few months,", "Python had a wildly successful past"],
        "without": ["View the discussion thread.", "January 13"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.pluralsight.com/tech-blog/managing-python-environments/": {
        "file": "pluralsight.com.python.html",
        "author": "John Walk",
        "title": "Managing Python Environments",
        "sitename": "Pluralsight",
        "date": "2020-01-10",
        "description": "ros and cons of available tools for python setup",
        "categories": ["practices"],
        "tags": ["python", "docker", "getting started"],
        "with": ["self-contained = deployable", "<config files>"],
        "without": ["21 minutes", "Tags:"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/": {
        "file": "stackoverflow.com.rust.html",
        "author": "Jake Goulding",
        "title": "What is Rust and why is it so popular?",
        "sitename": "Stack Overflow",
        "date": "2020-01-20",
        "description": "Description of the Programming Language Rust",
        "categories": ["Rust", "Programming"],
        "tags": ["Bulletin", "Code for a Living", "Stackoverflow"],
        "with": ["Rust has been", "Going beyond technical points"],
        "without": ["Jake is the co-founder", "What inspires someone", "Discover and share internal knowledge"],
        "comments": ["Thanks for all you do"],
        "license": "",
        "region": "",
    },
    "https://www.theplanetarypress.com/2020/01/management-of-intact-forestlands-by-indigenous-peoples-key-to-protecting-climate/": {
        "file": "theplanetarypress.com.forestlands.html",
        "author": "Julie Mollins",
        "title": "Management of Intact Forestlands by Indigenous Peoples Key to Protecting Climate",
        "sitename": "The Planetary Press",
        "date": "2020-01-19",
        "description": "Advantages of Management of Intact Forestlands by Indigenous Peoples for the Climate",
        "categories": ["Indigenous People", "Environment"],
        "tags": [],
        "with": ["The U.N.-backed principle", "Overall, these landscapes"],
        "without": [
            "Management of Intact Forestlands by Indigenous Peoples Key to Protecting Climate",
            "China has announced a new plan",
            "TPP highlights sustainable solutions",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://wikimediafoundation.org/news/2020/01/15/access-to-wikipedia-restored-in-turkey-after-more-than-two-and-a-half-years/": {
        "file": "wikimediafoundation.org.turkey.html",
        "author": "Wikimedia Foundation",
        "title": "Access to Wikipedia restored in Turkey after more than two and a half years",
        "sitename": "Wikimedia Foundation",
        "date": "2020-01-15",
        "description": "Report about the restored accessibility of Wikipedia in Turkey",
        "categories": ["Politics", "Turkey", "Wikipedia"],
        "tags": [],
        "with": ["19th birthday", "Bu yazının Türkçe’sini buradan okuyabilirsiniz", "We will keep this statement updated"],
        "without": [
            "Read further in the pursuit of knowledge",
            "what that means.",
            "Stay up-to-date on our work.",
            "Photo credits",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.reuters.com/article/us-awards-sag/parasite-scores-upset-at-sag-awards-boosting-oscar-chances-idUSKBN1ZI0EH": {
        "file": "reuters.com.parasite.html",
        "author": "Jill Serjeant",
        "title": "'Parasite' scores historic upset at SAG awards, boosting Oscar chances",
        "sitename": "Reuters",
        "date": "2020-01-19",
        "description": "“Parasite,” the Korean language social satire about the wealth gap in South Korea, was the first film in a foreign language to win the top prize of best cast ensemble in the 26 year-history of the SAG awards.",
        "categories": ["Parasite", "SAG awards", "Cinema"],
        "tags": [],
        "with": ["cementing their roles", "Despite an unknown cast,", "Additional reporting by"],
        "without": ["Related Coverage", "4 Min Read", "The Thomson Reuters Trust Principles", "Factbox: Key winners"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.nationalgeographic.co.uk/environment-and-conservation/2020/01/ravenous-wild-goats-ruled-island-over-century-now-its-being": {
        "file": "nationalgeographic.co.uk.goats.html",
        "author": "Michael Hingston",
        "title": "Ravenous wild goats ruled this island for over a century. Now, it's being reborn.",
        "sitename": "National Geographic",
        "date": "2020-01-06",
        "description": "The rocky island of Redonda, once stripped of its flora and fauna by invasive species, makes an astonishingly quick comeback. What’s the secret to its recovery?",
        "categories": ["Goats", "Environment", "Redonda"],
        "tags": [],
        "with": ["an imposing piece", "Once the goats and rats", "But they don’t know the work"],
        "without": ["Photograph by", "Find More Information", "What it’s like to live"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.nature.com/articles/d41586-019-02790-3": {
        "file": "nature.com.telescope.html",
        "author": "Elizabeth Gibney",
        "title": "Gigantic Chinese telescope opens to astronomers worldwide",
        "sitename": "Nature",
        "date": "2019-09-24",
        "description": "FAST has superior sensitivity to detect cosmic phenomena, including fast radio bursts and pulsars.",
        "categories": ["Astronomy", "Telescope", "China"],
        "tags": [],
        "with": ["Since testing began", "Eye in the sky", "Li hopes that"],
        "without": ["You are using a browser version", "PDF version", "Latest on:", "I agree my information will be"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.salon.com/2020/01/10/despite-everything-u-s-emissions-dipped-in-2019_partner/": {
        "file": "salon.com.emissions.html",
        "author": "Nathanael Johnson",
        "title": "Despite everything, U.S. emissions dipped in 2019",
        "sitename": "Salon",
        "date": "2020-01-10",
        "description": "Coal has been in a slow-motion death spiral over the past ten years",
        "categories": ["Coal", "Emmisions", "Climate"],
        "tags": [],
        "with": ["This post originally", "The same can’t be", "Cleaning up the electrical grid"],
        "without": ["Credit:", "Advertisement:", "Reproduction of material from any"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20160526181643/http://ordnungsrausch.com/orga-life-das-leben-organisieren/": {
        "file": "archive.ordnungsrausch.com.orga-life.html",
        "author": "",
        "title": "{orga your life} – das Leben organisieren ",
        "date": "",
        "description": "Neben meinen Beiträgen zur Zeitplanung seht ihr hier auch übersichtlich alles zum Thema Finanzen organisieren und Selbstmanagement.",
        "categories": ["{orga your life}"],
        "tags": [],
        "with": ["Wenn der Tag mal wieder zu wenige Stunden hat"],
        "without": ["#19 Kuchen im Glas", "2016 Ordnungsrausch", "Suche"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://weselpower.wordpress.com/2009/12/23/monstergesprche-1/": {
        "file": "weselpower.wordpress.com.monstergesprche.html",
        "author": "Rolf Tschochohei",
        "title": "Monstergespräche #1",
        "date": "2009-12-23",
        "description": "M:Wer rutscht als n&auml;chstes aus auf dem Glatteis? Ich: Ich wette,dass du als n&auml;chstes ausr&#8230;aah. ..paff. ..aua. M: Gewonnen!",
        "categories": ["meins"],
        "tags": ["Monster", "winter"],
        "with": ["M:Wer rutscht als nächstes aus auf dem Glatteis?"],
        "without": ["Teilen Sie dies mit:", "Bloggern gefällt das.", "Ähnliche Beiträge", " Kommentare sind geschlossen. "],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://bigdata.ypart.eu/page/Digitale_Datenerhebung_und_verwertung_als_Herausforderung_f%C3%BCr_Medienbildung_und_Gesellschaft.html": {
        "file": "bigdata.ypart.eu.datenerhebung.html",
        "author": "",
        "title": "Digitale Datenerhebung und -verwertung als Herausforderung für Medienbildung und Gesellschaft",
        "date": "",
        "description": "Ein medienpädagogisches Diskussionspapier zu Big Data und Data Analytics",
        "categories": [],
        "tags": [],
        "with": [
            "Das vorliegende Papier wurde für die Gesellschaft für Medienpädagogik",
            "Für Nutzende digitaler Dienste ist es derzeit nahezu unmöglich zu erkennen",
            "Das Digitale ist zur globalen Infrastruktur geworden.",
        ],
        "without": ["Diese Plattform wird betrieben vom", "In Kooperation mit", "Follow us on Twitter"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20131110121040/http://www.peptalks.de/haben-sich-mozarts-eltern-wegen-seiner-schulnoten-gesorgt/": {
        "file": "archive.peptalks.de.schulnoten.html",
        "author": "Günter W. Kienitz",
        "title": "Haben sich Mozarts Eltern je wegen seiner Schulnoten gesorgt?",
        "date": "2013-04-04",
        "description": "Was meinen Sie: haben sie? Haben sich die Eltern von Wolfgang Amadeus Mozart jemals Sorgen wegen der Schulnoten ihres &quot;Wolferls&quot; gemacht? Ich kann Ihnen versichern, das war nie der Fall. Wie ich mi...",
        "categories": ["Bildung", "Homeschooling", "Schule"],
        "tags": [
            "bildung",
            "Eltern",
            "Hausschule",
            "Homeschooling",
            "Lehranstalt",
            "Lernen",
            "Musik",
            "Schule",
            "Schülereltern",
            "schulnoten",
            "Schulpflicht",
            "Wolfgang Amadeus Mozart",
            "Wunderkind",
        ],
        "with": ["Was meinen Sie", "Anfang 1762 nach München und anschließend", "Er lebte still und unscheinbar"],
        "without": [
            "Dichter und Denker zu Schule und Bildung",
            "Sie möchten gerne automatisch über jeden",
            "Trage deine Daten unten ein",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://web.archive.org/web/20190717140047/http://www.modabot.de/paris-haute-couture-ss14-serkan-cura": {
        "file": "archive.modabot.de.serkan.html",
        "author": "Barbara Russ",
        "title": "Paris Haute Couture SS14: Serkan Cura",
        "date": "2014-01-27",
        "description": "Haute Couture ist die Krone der Mode-Schöpfung - und Serkan Cura ist ein würdiger Nachfolger der alten Meister seiner Zunft.",
        "categories": ["Event", "Fashion"],
        "tags": ["Haute Couture", "Paris", "Serkan Cura", "SS14"],
        "with": ["die diesmal leider keine Präsentation", "Die dabei entstehenden Silhouetten"],
        "without": ["to see what your friends like", "Bild via"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.welt.de/regionales/hamburg/article202159566/Verhaertete-Fronten-nach-Tumulten-bei-Luckes-Vorlesung.html": {
        "file": "d90b19386e2b48559082547016cbe5ec.html",
        "author": "dpa/lno",
        "title": "Verhärtete Fronten nach Tumulten bei Luckes Vorlesung",
        "date": "2019-10-19",
        "description": "Hamburg (dpa/lno) &#8211; Trotz eines Gespräches zwischen AfD-Mitbegründer Bernd Lucke und der Studierendenvertretung AStA der Universität Hamburg bleiben die Fronten verhärtet. Der AStA (Allgemeiner Studierendenausschuss) verkläre die Vorfälle, sagte Lucke am Samstag der Deutschen Presse-Agentur in Hamburg. Der AStA entziehe sich seiner Verantwortung, indem er in grotesker Weise die Opfer zu Tätern mache, kritisierte Lucke weiter. Ein Gespräch nur mit ... Mehr lesen",
        "categories": ["Hamburg"],
        "tags": [],
        "with": [
            "Der AStA (Allgemeiner Studierendenausschuss) verkläre die Vorfälle",
            "betonte, nicht zu den Störungen im Hörsaal aufgerufen zu haben",
            "hieß es anschließend.",
        ],
        "without": ["Lesedauer: 3 Minuten", "Vom Oma-Schoßhund zurück zum Trend-Hund", "Newsticker"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.hessenschau.de/kultur/buchmesse/buecher-autoren/die-minze-als-mutmacher--deniz-yuecels-bericht-aus-dem-tuerkischen-knast,deniz-yuecel-buchmesse-agentterrorist-100.html": {
        "file": "d76cf81a74fa4633bd19d7060f5c05ee.html",
        "author": "hessenschau.de/bb",
        "title": "Die Minze als Mutmacher – Deniz Yücels Bericht aus dem türkischen Knast",
        "date": "2019-10-19",
        "description": "Deniz Yücel saß im türkischen Gefängnis – im Auftrag der Öffentlichkeit, wie er bei seiner Buchvorstellung auf der Buchmesse in Frankfurt sagt. Der Flörsheimer berichtet über angstvolle Momente, Erdogans Copyright und die besondere Kraft der Minze. ",
        "categories": ["Kultur"],
        "tags": ["Bücher", "Frankfurter Buchmesse 2019", "Literatur", "Medien"],
        "with": [
            "Gefängnis – im Auftrag der Öffentlichkeit",
            "diese triste Umgebung schlug Deniz Yücel aufs Gemüt",
            "Verfasst mithilfe von Tomatensoße und einer Plastikgabel",
        ],
        "without": ["Navigation der Marken des Hessischen Rundfunks", "Weitere Informationen ", "Frankfurter Buchmesse 2019"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.tag24.de/nachrichten/rostow-russland-fuenf-kinder-und-zwei-erwachsene-sterben-bei-schrecklichem-wohnhausbrand-1255262": {
        "file": "d76bb5cda4cd4621a04c1b166d6cad9f.html",
        "author": "",
        "title": "Fünf Kleinkinder und zwei Erwachsene sterben bei schrecklichem Wohnhausbrand",
        "date": "2019-10-19",
        "description": "Fünf kleine Kinder, unter ihnen ein Baby, sterben zusammen mit zwei Erwachsenen bei einem Brand in Russland.",
        "categories": ["Feuerwehreinsätze"],
        "tags": [],
        "with": [
            "als sich das Feuer im Treppenhaus ausbreitete",
            "Dachgeschoss brannte vollkommen aus.",
            "ob der Brand wegen eines defekten Elektrogerätes",
        ],
        "without": ["Letzter Auftritt bei", "FAMILIENDRAMA: MUTTER", "Wir bei WhatsApp"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.grazia-magazin.de/beauty/lange-haare-dank-dieser-lebensmittel-wachsen-sie-viel-schneller-43980.html": {
        "file": "d73e0fa055834b2dbb2036ba27d46597.html",
        "author": "Isabella.DiBiase",
        "title": "Lange Haare: Dank dieser Lebensmittel wachsen sie viel schneller",
        "date": "2019-10-19",
        "description": '"Wusstet ihr, dass ihr mit der richtigen Ernährung das Wachstum eurer Haare beschleunigen könnt? Mit diesen Lebensmitteln bekommt ihr im Handumdrehen eine lange Löwenmähne...',
        "categories": [],
        "tags": ["Lange Haare", "Haare", "Lebensmittel"],
        "with": [
            "Haare beschleunigen könnt?",
            "sowie Kalzium, Eisen, Zink und Biotin enthalten",
            "Für Rapunzelhaare sorgt übrigens auch",
        ],
        "without": ["Weitere Themen", "Richtig frühstücken", "Hinweis ausblenden", "Klambt Style-Verlag GmbH & Co. KG"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.monsterdealz.de/user-deals/deals/gratisartikel-kostenlos/rewe-produkttest-10-000-produkttester-fuer-leibniz-keksn-cream-milk-oder-choco": {
        "file": "d71bfdce9dd246c9a6ee6d08c8b39e4c.html",
        "author": "HansEhrlich",
        "title": "*Ab Montag* 10000 Produkttester für Leibniz Keks’n Cream Milk oder Choco *REWE Produkttest*",
        "date": "2019-10-17",
        "description": "&quot;Außen knusprig, innen cremig&quot; So beschreibt Leibniz ihr neues Produkt &quot;Keks´n Cream&quot;. Das beste kommt jetzt: Beim Rewe Produkttest der nächsten Woche",
        "categories": [],
        "tags": ["Gratisartikel & Kostenlos"],
        "with": ["„Außen knusprig, innen cremig“", "Das beste kommt jetzt:", "Euer HansEhrlich"],
        "without": [
            "Kostenlos zum Newsletter anmelden",
            "GRATIS-Jahresabo abstauben",
            "Top-Vergleiche",
            "Noch nicht angemeldet?",
        ],
        "comments": ["Prospekt next week", "unserem Markt waren aber keine mehr da", "ich gerne mit, klingt leck"],
        "license": "",
        "region": "DE",
    },
    "https://www.stern.de/politik/ausland/niederlage-fuer-johnson--parlament-vertagt-votum-ueber-brexit-deal-8961728.html?utm_campaign=alle&utm_medium=rss-feed&utm_source=standard": {
        "file": "d70fab3adde74d5fb63552855c981395.html",
        "author": "dsw / DPA",
        "title": "Unterhaus vertagt Votum über Brexit-Deal - es drohen Chaos-Tage",
        "date": "2019-10-19",
        "description": "Der Premierminister muss eine Verlängerung der Brexit-Frist beantragen. Kann er sein Versprechen einhalten, das Land am 31. Oktober aus der EU zu ...",
        "categories": ["Politik"],
        "tags": ["Boris Johnson", "EU", "Premierminister", "Niederlage", "Abstimmung", "EU-Gipfel", "Brüssel"],
        "with": [
            "Der Premierminister muss eine Verlängerung",
            "empfindliche Niederlage zugefügt.",
            "mit knapper Mehrheit in einem Referendum für den Austritt",
        ],
        "without": ["Themen in diesem Artikel", "Video", "Drucken"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.computerbild.de/artikel/cb-News-Freizeit-Bundesliga-Dortmund-Moenchengladbach-live-sehen-24356155.html": {
        "file": "d60caba9d12c467b9708ec8981cad8aa.html",
        "author": "	Dennis Kochinky",
        "title": "Bundesliga: Dortmund - Gladbach live sehen!",
        "date": "2019-10-19",
        "description": "Am 8. Spieltag der Bundesliga treffen Borussia Dortmund und Borussia Mönchengladbach aufeinander. So sehen Sie das Spiel live im TV und im Stream.",
        "categories": [],
        "tags": [],
        "with": [
            "So sehen Sie das Spiel live",
            "dennoch ist die Gladbacher Verletztenliste weiterhin lang",
            "» Zum Angebot: Borussia Dortmund",
            "Tipp: Die Sport-App",
        ],
        "without": [
            "Kein Bild, kein Ton und trotzdem bestens informiert",
            " Sehen Sie die Highlights der europäischen Top-Ligen",
            "Gefällt Ihnen dieser Artikel?",
            "Aktuelle Testberichte von Hard- und Software",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.express.de/duesseldorf/duesseldorf-tote-tauben-im-iss-dome-gefunden----peta--erstattet-strafanzeige-33335766": {
        "file": "d57cfadc540842ebb09971e28df123ec.html",
        "author": "Dieter Sieckmeyer",
        "title": "Düsseldorf ISS Dome: Peta erstattet Anzeige wegen toten Tauben ",
        "date": "2019-10-19",
        "description": "Immer wieder werden am ISS Dome tote Tauben gefunden. Viele verenden qualvoll in den Netzen, die unter dem Dach der Halle angebracht wurden.",
        "categories": ["Düsseldorf"],
        "tags": [],
        "with": [
            "Viele verenden qualvoll in den Netzen",
            "Das soll das Problem lösen",
            "em städtischen Veterinäramt umgesetzt.",
        ],
        "without": [
            "zwischen türkischer und kurdischer Mannschaft",
            "URL zum Kopieren",
            "Inhalt teilen",
            "Sei der/die Erste deiner Freunde",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.ln-online.de/Lokales/Luebeck/Luebeck-So-war-die-Auktion-fuer-St.-Johannes-in-Kuecknitz": {
        "file": "d51e75d9e53a472bb7708191899aa6b4.html",
        "author": "Cosima Künzel",
        "title": "So lief die Auktion der Schätzchen von St. Johannes",
        "date": "2019-10-19",
        "description": "Stühle, Leuchten und ein Abendmahl aus Gips. Im Kücknitzer Kirchen-Forum wurden Dachboden-Schätze der Kirche St. Johannes versteigert. Für die Neugestaltung des Gotteshauses kam viel Geld zusammen.",
        "categories": [],
        "tags": [],
        "with": [
            "wurden Dachboden-Schätze der Kirche St. Johannes versteigert",
            "Kirchenvorsteher Niels Sönnichsen hat alle Schätze",
            "Gemälde werden hoch gehandelt",
        ],
        "without": ["Newsletter abonnieren", "Die Kultkneipe schließt: Jutta's Eck", "Weitere LN+ Artikel"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://appen.com/blog/artificial-intelligence-and-machine-learning-industry-news-ai-in-patient-care-and-operations-ai-as-a-preventive-tool-and-how-major-hospitals-are-already-using-ai/": {
        "file": "d44c5ef50718437984dca47627dee96b.html",
        "author": "Joe S.",
        "title": "Artificial Intelligence and Machine Learning Industry News: AI in Patient Care and Operations, AI as a Preventive Tool, and How Major Hospitals are Already Using AI",
        "date": "2019-10-18",
        "description": "With the integration of AI into the work of both medical professionals and hospital systems, expect to see dramatic changes in both patient health outcomes and in the operational efficiency of hospitals. ",
        "categories": ["Blog Home AI", "Machine Learning"],
        "tags": ["AI", "Artificial Intelligence", "Industry News Roundup", "machine learning", "Video"],
        "with": [
            "Follow us to stay up to date on industry trends.",
            "How Major Hospitals are Already Using AI",
            "With predictive analytics,",
        ],
        "without": ["Trending Posts", "Subscribe to email updates", "Receive our monthly newsletter"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.mactechnews.de/forum/discussion/kein-App-Store-mehr-ueber-Mobile-Daten-mit-iOS-13--338679.html.html": {
        "file": "d43f330cbaf74e92b9aec85e937cb904.html",
        "author": "macbacchi",
        "title": "kein App Store mehr über Mobile Daten mit iOS 13 ?",
        "date": "2019-09-28",
        "description": "Immer aktuelle Apple-News, Tipps, Tricks und Testberichte rund um Mac, iPhone, iPad und Co.",
        "categories": ["iPhone"],
        "tags": [],
        "with": ["one 11 und xs und ipads sind keinen zugriff mehr auf den appstore", "und bevor wieder die übliche häme"],
        "without": [
            "Kommentieren",
            "Sie müssen sich einloggen, um sich an einer Diskussion beteiligen zu können.",
            "wo immer es sinnvoll erscheint. Sie unterstützen",
        ],
        "comments": [
            "ntr mobilen Daten auf den App Store zugreifen",
            "erst kürzlich hier im Forum?",
            "Ist aber nicht von Dauer.",
        ],
        "license": "",
        "region": "DE",
    },
    "https://www.nzz.ch/international/der-nervenkrieg-um-den-brexit-geht-in-die-naechste-runde-ld.1516516": {
        "file": "d42c68f1b0f4408b81cf8f00bbe1a631.html",
        "author": "Markus M. Haefliger, London, Beat Bumbacher",
        "title": "Der Nervenkrieg um den Brexit geht in die nächste Runde",
        "date": "2019-10-19",
        "description": "Das britische Unterhaus hat die Entscheidung über das neue EU-Austrittsabkommen verschoben und Premierminister Boris Johnson damit eine weitere Niederlage zugefügt. Wie vom Gesetz verlangt, ersucht die britische Regierung die EU nun um eine Verschiebung des für 31. Oktober geplanten EU-Austritts",
        "categories": [],
        "tags": [],
        "with": [
            "eine Brexit-Verschiebung bei der EU beantragt",
            "über den EU-Austritt Grossbritanniens gebracht. Eine Mehrheit ",
            "Dies könnte aus ihrer Sicht als Ersatz für den Grundsatzentscheid vom Samstag herhalten",
        ],
        "without": [
            "Niederlage für Boris Johnson – Britische Regierung will Brexit-Verschiebung beantragen",
            "Wagen Sie den anderen Blick mit unlimitiertem Zugang zur digitalen NZZ",
            "Haben Sie schon ein Benutzerkonto?",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.gamestar.de/videos/der-landwirtschafts-simulator-19-wird-ein-jahr-nach-release-groesser-trailer-stellt-platinum-edition-vor,99770.html": {
        "file": "d041d20a0bc04fdf8cef73f750f20bf6.html",
        "author": "",
        "title": "Der Landwirtschafts-Simulator 19 wird ein Jahr nach Release größer - Trailer stellt Platinum Edition vor",
        "date": "2019-10-19",
        "description": 'Am 22. Oktober 2019 erscheint die Platinum Edition des Landwirtschaft-Simulator 2019 mit einer Menge neuen Content auf Windows PCs, Mac, Xbox One und..." ',
        "categories": [],
        "tags": [
            "Spiele-Trailer",
            "Landwirtschafts-Simulator 19",
            "Video",
            "Trailer",
            "PC",
            "PlayStation 4",
            "Xbox One",
            "PlayStation",
            "Xbox",
        ],
        "with": [
            "auf Windows PCs, Mac, Xbox One und PS4. Der Trailer gibt euch einen kurzen Überblick zu den zusätzlichen Inhalten.",
            "als eigenständiges Spiel und wird zudem",
        ],
        "without": ["Kommentare", "alle anzeigen", "Nur angemeldete Benutzer können kommentieren und bewerten.", "Steam"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.tichyseinblick.de/kolumnen/spahns-spitzwege/no-peace-for-our-time-pence-syrien-und-die-tuerkei/": {
        "file": "d32ad974a4b04657bb6e4d91852bd52d.html",
        "author": "Tomas Spahn",
        "title": "No Peace for Our Time – Pence, Syrien und die Türkei",
        "date": "2019-10-18",
        "description": "Peace for our time“ war 1938 der Auftakt zur bisher größten Katastrophe, die die Menschheit sich selbst geschaffen hat. Hoffen wir inständig, dass das aktuelle US-Appeasement nicht eines Tages ähnlich beurteilt werden muss.",
        "categories": [],
        "tags": [],
        "with": [
            "war 1938 der Auftakt zur bisher größten",
            "Frieden in unserer Zeit?",
            "Außer Kuscheleinheiten nichts gewesen.",
        ],
        "without": [
            "Täglich schreiben unabhängige",
            "Unterstützen Sie diese Form",
            "Türkei: Der euroamerikanische Abschied aus der Weltpolitik",
        ],
        "comments": [],  # new comments online!!
        "license": "",
        "region": "DE",
    },
    "https://www.mopo.de/sport/hsv/fuer-den-hsv-in-der-oberliga--jansen-kaempft-um-trochowskis-comeback-33334622": {
        "file": "d27eb719099b43639104995806e07d00.html",
        "author": "Simon Braasch",
        "title": "Ex-Nationalspieler in der Oberliga: Marcell Jansen kämpft um Piotr Trochowskis HSV-Comeback ",
        "date": "2019-10-19",
        "description": "Läuft Piotr Trochowski künftig wieder für den HSV auf? Seit dieser Woche trainiert der 35-Jährige bei der dritten Mannschaft des Vereins mit, könnte schon bald in der Oberliga Hamburg zum Einsatz kommen. Dann würde der HSV auf gleich zwei Ex-Nationalspieler zurückgreifen können – denn Marcell Jansen (33) ist bereits fester Bestandteil des Teams. Nun hofft „Cello“, dass Trochowski es ihm nachmacht, sagte der MOPO: „Ich werde sehr stark auf ihn einreden, damit er auch wirklich bei uns ...",
        "categories": ["Sport"],
        "tags": [],
        "with": [
            "künftig wieder für den HSV auf? ",
            "Es bringt riesigen Spaß, die Liga hat sehr viel Tradition",
            "Oberliga ist keine Pillepalle-Liga",
        ],
        "without": ["haben einen guten Draht.", "4 Tsd. Abonnenten", "Kommentieren Sie hier", "URL zum Kopieren", "Messenger"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.nachrichten.at/meine-welt/gesundheit/was-bringen-alternative-therapien-bei-krebs;art114,3177663": {
        "file": "0b96fc66e2c94f45a1b923ec9a31fcf2.html",
        "author": "Claudia Riedler",
        "title": 'Was bringen "alternative" Therapien bei Krebs?',
        "date": "2019-10-19",
        "description": "Krebskongress in Linz über Schul- und Komplementärmedizin.",
        "categories": ["Gesundheit"],
        "tags": [],
        "with": [
            "Darüber diskutieren Experten seit gestern",
            "Wer sollte also die Komplementärmedizin anbieten?",
            "www.selbertun.at",
        ],
        "without": [
            "Leiterin Redaktion Leben",
            "Die OÖNachrichten nehmen den Schutz Ihrer Privatsphäre sehr ernst.",
            "3:1 - Vorwärts Steyr half der SV Ried ",
        ],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.ardmediathek.de/swr/player/Y3JpZDovL3N3ci5kZS9hZXgvbzExNjIyMjY/nahrungsergaenzungsmittel-das-dubiose-geschaeft-mit-der-hoffnung": {
        "file": "0b4609a864eb4fa0bbcb2b395f6be9eb.html",
        "author": "SWR Fernsehen",
        "title": "betrifft: ...: Nahrungsergänzungsmittel - Das dubiose Geschäft mit der Hoffnung | Video der Sendung vom 16.10.2019 18:15 Uhr (16.1.2019)",
        "date": "2019-10-16",
        "description": "Nahrungsergänzungsmittel - Das dubiose Geschäft mit der Hoffnung | Video | Dubiose Händler versprechen Hilfe bei Schlafstörungen, Gelenkschmerzen, erhöhten Cholesterinwerten oder sogar Krebs. &quot;betrifft&quot; beleuchtet, wie es Gesetzeslücken ermöglichen, dass sogar gefährliche Nahrungsergänzungsmittel völlig unkontrolliert auf den Markt gelangen.",
        "categories": [],
        "tags": [],
        "with": ["Dubiose Händler versprechen Hilfe bei Schlafstörungen"],
        "without": ["Navigation schliessen", "Mehr aus der Sendung", "Unfallbetrüger"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://jungefreiheit.de/debatte/kommentar/2019/kaisers-royaler-wochenrueckblick-31/": {
        "file": "0b66696af800472190a76b26faa845d4.html",
        "author": "Boris T. Kaiser",
        "title": "Kaisers royaler Wochenrückblick",
        "date": "2019-10-19",
        "description": "Während Mesut Özil mit Deutschland abrechnet, geben die Auseinandersetzungen zwischen Kurden und Türken in deutschen Straßen einen Vorgeschmack auf die Zukunft. In Essen mußte ein Diskogast seine Kreuzkette verbergen. Der Türsteher wollte es so. <i>Boris T. Kaiser blickt zurück.",
        "categories": [],
        "tags": [],
        "with": ["Im Interview mit dem Sportportal", "Ist Özil ein verkappter Feingeist?", "nicht für einen Rosenkranz hält."],
        "without": [
            "Der nächste Beitrag",
            "Die Kommentarfunktion wird 2 Tage nach Veröffentlichungsdatum des Beitrages geschlossen.",
            "Meistkommentiert",
        ],
        "comments": ["wichtig ist lebenswichtig, Christen sind böse und die Räume der Frankfurter Buchmesse sind frei"],
        "license": "",
        "region": "DE",
    },
    "https://telebasel.ch/2019/10/19/junge-lenker-schrotten-corvette-und-audi-in-einer-nacht/?channel=105100": {
        "file": "0afd671fc2b64f3caa83a91537e8d343.html",
        "author": "telebasel",
        "title": "Junge Lenker schrotten Corvette und Audi in einer Nacht",
        "date": "2019-10-19",
        "description": "Am Freitagabend krachte ein 19-jähriger Neulenker in Lenzburg in eine Leitplanke. Am Auto und an der Leitplanke entstand ein Sachschaden von 80&#039;000 Franken.",
        "categories": [],
        "tags": [],
        "with": [
            "In der Nacht auf Samstag haben zwei junge Lenker",
            "Ein Neulenker ist in der Nacht auf Samstag um 23:50",
            "Schweizer schrottet Corvette",
        ],
        "without": ["1 Kommentar", "Mehr aus dem Channel", "Fruchtiger Pinot Grigio zu Saiblingsfilet mit Buttermilch-Dashi"],
        "comments": ["Und ich (A) LOCHmuss"],
        "license": "",
        "region": "CH",
    },
    "https://www.dealdoktor.de/user-deals/deals/gutscheine-deals/jacobs-gold-instant-kaffee-2-glaeser-fuer-480-e/": {
        "file": "0ac0531f1f0543f4a3f68159e5fd1875.html",
        "author": "MikeNils",
        "title": "Jacobs Gold Instant Kaffee 2 Gläser für 4,80 €",
        "date": "2019-10-18",
        "description": "Im Aktionszeitraum gleichzeitig zwei Gläser Jacobs Gold instant 200g bei Edeka kaufen. Bei einsendung des Kassenbons und ausgefüllten",
        "categories": [],
        "tags": [],
        "with": [
            "Bei einsendung des Kassenbons",
            "4. 6 € Gutschein für den Einkauf bei Edeka erhalten.",
            "Einsendeschluss: 03.11.2019 (Poststempel)",
        ],
        "without": [
            "Deal abgelaufen? Jetzt melden!",
            "Kostenlos zum Newsletter anmelden und",
            "Du musst angemeldet sein, um einen Kommentar abzugeben.",
        ],
        "comments": [
            "Der 10 Euro Gutschein Deal vor 3 Wochen über Rewe war lukrativer",
            "Hast recht, gerade erst gesehen.",
            "Der Link geht zu EDEKA-Nordbayern",
        ],
        "license": "",
        "region": "DE",
    },
    "https://www.tagblatt.ch/kultur/mit-allen-wassern-gewaschen-ld.1161246": {
        "file": "0a29620f9c4347758c146ed06dab6f3e.html",
        "author": "Bettina Kugler",
        "title": "Tanz in der St. Galler Lokremise: Mit allen Wassern gewaschen",
        "date": "2019-10-19",
        "description": "Die Tanzkompanie des Theaters St.Gallen öffnet mit &quot;Rain&quot;, Kinsun Chans erster choreografischer Arbeit als neuer Tanzchef, traumleicht und bildstark Assoziationsräume.",
        "categories": [],
        "tags": [],
        "with": [
            "Nirgends und überall ist das Gedicht,",
            "Rund 75 Minuten lang spürt man den",
            "die Kunst, das Leben auf sich herabregnen zu lassen.",
        ],
        "without": ["Ein Kippmoment in", "Abonnemente", "Online Inserat aufgeben"],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://www.watson.ch/leben/drinks/453207266-sazerac-alles-ueber-den-cocktail-klassiker-aus-new-orleans": {
        "file": "0a24692a9ea846c1819bd6a5f92a8874.html",
        "author": "Oliver Baroni",
        "title": "Sazerac - alles über den Cocktail-Klassiker aus New Orleans",
        "date": "2019-10-19",
        "description": "Und weiter geht's mit einer neuen Folge von watson's Cocktail Classics mit Baroni! Heute ein Klassiker mit Schweizer Einschlag.",
        "categories": [],
        "tags": [],
        "with": [
            "wo man in Zürich",
            "1-2 Spritzer Peychaud",
            "Aber eigentlich kommt es für den Privatgebrauch",
            "mit Schweizer Einschlag",
            "Storming the Sazerac",
        ],
        "without": [
            "auf Twitter",
            "Nachtmodus ein",
            "Warum Trump jetzt Syrien um die Ohren fliegt",
            "Shot Happens",
            "Geht man auf die Anfänge",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://wien.orf.at/stories/3017954/": {
        "file": "0a6291ebbce449b3b04256b43c73e39d.html",
        "author": "red, wien.ORF.at/Agenturen",
        "title": "Lotte Tobisch ist tot",
        "date": "2019-10-19",
        "description": "Die Opernball-Grande-Dame und Burgschauspielerin Lotte Tobisch ist Samstagfrüh im Alter von 93 Jahren gestorben. Die Wienerin prägte unter anderem 16 turbulente Jahre lang den Opernball als Organisatorin.",
        "categories": [],
        "tags": [],
        "with": [
            "Die Opernball-Grande-Dame und Burgschauspielerin Lotte Tobisch",
            "Zahlreiche Auszeichnungen",
            "Auch bei der jüngsten Wahl",
        ],
        "without": [
            "ORF2 zeigt in memoriam",
            "die Funktionalität dieser Website zu gewährleisten",
            "Aktuell in wien",
            "Viele Freunde, Verwandte und Fans haben sich",
            "Georg Hochmuth",
        ],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.investmentwatchblog.com/biggest-money-laundering-scheme-in-history-uncovered-in-ukraine/": {
        "file": "0a3108e507c54157a95fe7a1338f5e9c.html",
        "author": "IWB",
        "title": "Biggest money laundering scheme in history uncovered in Ukraine",
        "date": "2019-10-19",
        "description": "",
        "categories": [],
        "tags": ["biggest", "history", "laundering", "money", "scheme", "ukraine", "uncovered"],
        "with": [
            "Jewish oligarchs Igor Kolomoisky and",
            "The Chairwoman of Ukraine’s Central Bank",
            "Now as to those missing IMF billions, ",
        ],
        "without": [
            "Privacy & Cookies: This site uses",
            "If you’re running an ad-blocker",
            "Don't have time to read every single post",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://neunzehn72.de/imac-5k-lightroom-performance-geloest-danke-an-die-community/": {
        "file": "0a962f6bcd5649f7a7e6effa338df80d.html",
        "author": "Paddy",
        "title": "iMac 5K Lightroom Performance gelöst – Danke an die Community",
        "date": "2019-04-19",
        "description": "Ich freue mich wie ein kleines Kind. Nachdem ich in meinem letzten VLog die Performance von Lightroom auf meinem neuen iMac Pro beklagt hatte, bekam ich von drei Lesern einen sehr hilfreichen Tipp.",
        "categories": ["Mac"],
        "tags": ["iMac", "lightroom", "performance"],
        "with": ["Ich freue mich wie ein kleines Kind.", "Jetzt rennt der iMac Pro wie Hulle", "Auflösung der 5K-Displays"],
        "without": [
            "Ich mag jede Art von Fotografie",
            "Leave a Comment! ",
            "Ja, ich möchte den wöchentlichen Newsletter bekommen",
        ],
        "comments": [
            "Ein kurzer Tipp noch von mir, man braucht kein Switchres X",
            "Freuen weil man Lightroom performant",
            "Gruss aus der Schweiz",
        ],
        "license": "",
        "region": "DE",
    },
    "https://www.zeit.de/2019/43/klimaschutz-banken-unternehmen-fracking-oelfoerderung-fossile-brennstoffe": {
        "file": "0a12df42d1764095989ab078ee0f940b.html",
        "author": "Heike Buchter",
        "title": "Bohren, bis es heiß wird",
        "date": "2019-10-16",
        "description": "Weltweit finanzieren Banken und Investoren Unternehmungen, die dem Klima schaden.",
        "categories": [],
        "tags": [],
        "with": [
            "Weltweit finanzieren Banken und Investoren Unternehmungen",
            "wollten damit vor zwei Wochen die Verbindung zwischen der Wall Street",
            "JPMorgan Chase",
        ],
        "without": ["Bundesstaat Pennsylvania", "Wählen Sie Ihren Zugang und lesen Sie weiter:", "Cookies & Tracking"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.zugreiseblog.de/db-lounge-zutritt-sparpreis/": {
        "file": "0a4a8ab61c054192b1ec70cc3570cf45.html",
        "author": "David",
        "title": "DB Lounge: Kein Zugang mehr mit Sparpreis-Ticket",
        "date": "2019-10-18",
        "description": "Die Bahn ändert die Zutrittsbestimmungen zur DB Lounge: Fahrgäste mit einem Sparpreis der ersten Klasse müssen künftig draußen bleiben.",
        "categories": [],
        "tags": ["bahn", "deutschland"],
        "with": [
            "Die Deutsche Bahn streicht den Zutritt zu ihrer DB Lounge",
            "Die Deutsche Bahn ändert zum Fahrplanwechsel",
            "Neues gastronomisches Konzept",
        ],
        "without": [
            "Das könnte Dich auch interessieren",
            "Sder Gründer des Zugreiseblog",
            "Erfahre zudem,",
            "Mit meinem kostenlosen Newsletter verpasst",
        ],
        "comments": [
            "Mir ist auch schon aufgefallen, dass es speziell in München",
            "Glückwunsch an den Autor",
            "Warum will man das abschaffen ?",
        ],
        "license": "",
        "region": "DE",
    },
    "https://www.ndr.de/nachrichten/info/16-Coronavirus-Update-Wir-brauchen-Abkuerzungen-bei-der-Impfstoffzulassung,podcastcoronavirus140.html": {
        "file": "ndr.de.podcastcoronavirus140.html",
        "author": "",
        "title": "(16) Coronavirus-Update: Brauchen Abkürzungen bei der Impfstoffzulassung",
        "date": "2020-03-18",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Das ist die zweithöchste von vier Stufen",
            "Die zentralen Fragen der Folge im Überblick",
            "Was sagt Professor Drosten dazu?",
            "Aus China.",
            "On-Off-Mechanismus",
            "Gerne. Bis morgen.",
        ],
        "without": [
            "Regelmäßig beantwortet Virus-Forscher",
            "Dieses Skript als PDF herunterladen",
            "Themen: Kritik aus dem Internet",
            "Was Sie zum Coronavirus wissen müssen",
            "Drucken",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://verfassungsblog.de/expertinnen-in-der-krise/": {
        "file": "verfassungsblog.de.expertinnen.html",
        "author": "Heiko Sauer",
        "title": "Expert*innen in der Krise",
        "date": "2020-04-09",
        "description": "",
        "categories": [],
        "tags": ["Coronavirus", "Rechtswissenschaft"],
        "with": [
            "Die verfassungsrechtswissenschaftliche Begleitung",
            "Selbstgewissheit abrüsten",
            "eine besondere Vorbildfunktion.",
        ],
        "without": [
            "is a Professor of Public",
            "I know that I may withdraw my consent",
            "If you enjoyed reading this post",
            "VerfBlog",
            "Comments under pseudonym are allowed",
            "European constitutional space and beyond.",
        ],
        "comments": ["Ich fürchte, das überzeugt mich nicht.", "Binnennormierung innerhalb", "etwas sauer aufgestoßen sind."],
        "license": "CC BY-NC-ND",
        "region": "DE",
    },
    "https://www.lecker.de/schneewittchen-kuchen-mit-mini-marshmallows-77975.html": {
        "file": "lecker.de.schneewittchen.html",
        "author": "",
        "title": "Schneewittchen-Kuchen mit Mini-Marshmallows",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [
            "vegetarisch",
            "Kuchen & Gebäck",
            "süß",
            "fruchtig",
            "Desserts & Backen",
            "einfach",
            "LECKER-Sonderheft 1/2019",
        ],
        "with": [
            "Mini-Marshmallows getoppt wird",
            "Vanillepuddingpulver",
            "Frischhaltefolie",
            "300 Minuten Wartezeit",
            "Zum Servieren Kuchen vorsichtig",
            "390 kcal",
        ],
        "without": ["Pin it", "Versenden", "Gebratener Blumenkohlsalat"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.chefkoch.de/rezepte/607331160490733/Mandarinen-Schmand-Kuchen.html": {
        "file": "chefkoch.de.mandarinen.html",
        "author": "jesusfreak",
        "title": "Mandarinen-Schmand-Kuchen",
        "date": "2006-10-10",
        "description": "",
        "categories": [],
        "tags": ["Backen", "Vegetarisch", "Kuchen", "Frucht", "Gluten", "Lactose"],
        "with": [
            "der cremigste Kuchen",
            "Für den Mürbeteig:",
            "Margarine oder Butter",
            "Mandarine(n), je ca.",
            "Koch-/Backzeit ca.",
            "Für eine 26er Springform.",
        ],
        "without": ["Für dieses Rezept gibt es noch", "Lactose", "Tipp falls bei euch"],
        "comments": ["Hallo zusammen, könnte ich", "LG steinchen71", "ja natürlich."],
        "license": "",
        "region": "",
    },
    "https://www.oetker.de/rezepte/r/bienenstich-muffins": {
        "file": "oetker.de.bienenstich.html",
        "author": "",
        "title": "Bienenstich-Muffins",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Saftig-weiche Muffins aus Hefeteig",
            "für das Rezept Bienenstich-Muffins",
            "Dr. Oetker Vanillin-Zucker",
            "Belag:",
            "Heißluft etwa 180 °C",
            "ein großes Brett legen.",
        ],
        "without": ["Merken", "Verwendete Dr. Oetker Produkte", "(24 Rezepte)"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://backen.de/rezept/maulwurfkuchen-mit-erdbeeren": {
        "file": "backen.de.maulwurfkuchen.html",
        "author": "",
        "title": "Maulwurfkuchen mit Erdbeeren",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "für 12 Stück",
            "z.B. Dr. Oetker Gelatine fix (15 g)",
            "Für dieses Rezept benötigst",
            "Teigschaber",
            "und schneide sie in kleine Würfel.",
        ],
        "without": ["Bild anzeigen", "Schreib du doch einen", "Neugierig geworden?"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.backenmachtgluecklich.de/rezepte/saftiger-zitronenkuchen-vom-blech.html": {
        "file": "backenmachtgluecklich.de.zitronenkuchen.html",
        "author": "Kathrin",
        "title": "Saftiger Zitronenkuchen vom Blech: einfach köstlich!",
        "date": "2020-02-17",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "einen echten Klassiker aus der Backstube.",
            "Sobald der Kuchen gebacken",
            "Diesen Beitrag habe ich 2017",
            "6 mittelgroße Eier",
            "Rührteig auf dem Blech verteilen",
            "Du möchtest Zutaten ersetzen?",
        ],
        "without": ["Pinnen", "Rezept drucken", "Zudem erhältst du jede Woche", "Hallo, ich bin Foodbloggerin"],
        "comments": [
            "Danke schonmals für die Antwort",
            "Du solltest 1-2 Eigelb weg lassen",
            "Puh,eine ganz normale Blechgröße",
        ],
        "license": "",
        "region": "",
    },
    "https://www.mz-web.de/dessau-rosslau/hingucker-beim-flugplatzfest-zweite-f13-kurz-vor-der-zulassung-33328852": {
        "file": "0af99c85f22b451a93a75bbf99ac412e.html",
        "author": "Thomas Steinberg",
        "title": "Hingucker beim Flugplatzfest in Dessau: Zweite F13 kurz vor der Zulassung",
        "date": "2019-10-19",
        "description": '"Vor eineinhalb Jahren war das von Hugo Junkers entwickelte erste Ganzmetallflugzeug der Welt der Hingucker beim Flugplatzfest in Dessau.',
        "categories": [],
        "tags": [],
        "with": [
            "entstanden ist er am Flughafen Dübendorf nahe Zürich.",
            "Zugleich habe man das Fahrwerk verbessert.",
            "dann auch die vierte Maschine gebaut und zugelassen werden.",
        ],
        "without": [
            "MZ Dessau-Roßlau bei Facebook",
            "polinturner suchen Meister: Stelldichein der deutschen Hoffnungen in Dessau",
            "zu die einwandfreie Funktion der Webse",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.rundschau-online.de/region/rhein-berg/bergischgladbach/pflaster-desaster-gladbacher-fussgaengerzone-in-schlechtem-zustand-33335514": {
        "file": "0b5db24739704283849ca3ed20ce09d4.html",
        "author": "Claus Boelen-Theile",
        "title": "Bergisch Gladbach: die Stadt verklagt die Baufirma wegen schlechter Pflastersteine",
        "date": "2019-10-19",
        "description": "Diese Flaniermeile ähnelt einer übergroßen Stolperfalle. Dabei ist das Pflaster der Gladbacher Fußgängerzone erst sechs Jahre alt.",
        "categories": [],
        "tags": [],
        "with": [
            "An manchen Stellen wirkt das Straßenpflaster deutlich in die Jahre gekommen.",
            "„Wir hätten es auch lieber anders, aber das Ver",
            "Auf den Zeitrahmen des Verfahrens habe die Stadt allerdings keinen Einfluss.",
        ],
        "without": [
            "Weitere interessante News",
            "Aktuelle Artikel",
            "damit die Stadt in einem Gerichtsverfahren Indizien vorlegen",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.finanztip.de/betriebliche-altersvorsorge/": {
        "file": "finanztip.de.altersvorsorge.html",
        "author": "Sara Zinnecker ",
        "title": "Mit Hilfe des Chefs für die Rente sparen",
        "date": "2020-02-05",
        "description": "Betriebliche Altersvorsorge sichert eine Zusatzrente im Alter. Das Modell lohnt besonders, wenn der Chef mit einzahlt.",
        "categories": [],
        "tags": [],
        "with": [
            "20,2 Mio.",
            "Altersvorsorge (bAV) versteht man den Aufbau einer Zusatzrente über den Arbeitgeber.",
            "vor allem vor der Frage: Lohnt sich das für",
            "erläutern wir diese genauer.",
            "So viel spart ein Durchschnittsverdiener",
            "Im Beispiel verliert der Durchschnittsverdiener durch die Entgeltumwandlung",
        ],
        "without": [
            "Weitere Themen",
            "Geld erhalten wir, wenn Sie di",
            "Aktuelle Ausgabe des Newsletters",
            "Unser Tipp: Bleiben Sie zum Thema",
            "05. Februar 2020 ",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.smava.de/privatkredit/privatkredit-zinsen/": {
        "file": "smava.de.privatkredit.html",
        "author": "",
        "title": "Wie hoch sind die Zinsen für einen Privatkredit? ",
        "date": "",
        "description": "Die Höhe der Zinsen für Ihren Privatkredit bestimmt, wie viel Geld Sie insgesamt zurückzahlen müssen. Tipps zur Berechnung finden Sie hier!",
        "categories": [],
        "tags": [],
        "with": [
            "und wie die Berechnung Ihrer Privatkredit-Zinsen erfolgt, erfahren Sie hier.",
            "286,35 €",
            "ein unbefristetes Arbeitsverhältnis sowie Vermögenswerte bzw. Sicherheiten",
            "Änderung der Zinshöhe bei Privatkrediten",
            "Wie wird die Höhe der fälligen Zinsen für meinen Privatkredit bestimmt?",
            "Gilt die vereinbarte Zinsbindung für die gesamte Kreditlaufzeit,",
        ],
        "without": [
            "Erhalten Sie kostenlos aktuelle Kredit-News und Informationen zu Sonderzins-Aktionen",
            "Kostenlose Beratung",
            "zum Kreditvergleich",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.finanzcheck.de/autokredit/leasing-oder-finanzierung/": {
        "file": "finanzcheck.de.finanzierung.html",
        "author": "",
        "title": "Leasing oder Finanzierung – was lohnt sich mehr?",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Im Vergleich zum Leasing gehört bei der Finanzierung das Fahrzeug am Ende dem Halter",
            "auch die Leasingraten senken, indem die Kunden eine Anzahlung leisten.",
            "Leasingverträge erstrecken sich meist",
            "Effektiver Jahreszins: 3,9 Prozent",
            "höheres Verschleißrisiko aufgrund einer längeren Nutzungsdauer",
        ],
        "without": ["Gemeinsam finden wir Ihren passenden Kredit!", "0,00% fester Sollzins", "3737 Bewertungen"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.vergleich.de/auto-leasen-finanzieren-oder-kaufen.html": {
        "file": "vergleich.de.leasen.html",
        "author": "",
        "title": "Auto leasen, finanzieren oder kaufen – was ist günstiger?",
        "date": "",
        "description": "Das neue Auto leasen, finanzieren oder kaufen? Viele Wege führen zum eigenen Auto. Wir zeigen, ob sich Barkauf, Leasing oder eine Finanzierung für Sie lohnt",
        "categories": [],
        "tags": [],
        "with": [
            "welche Vor- und Nachteile es dabei gibt.",
            "Vorteile bei der Finanzierung über einen Autokredit:",
            "Kratzer und Beulen kommen Sie teuer zu stehen.",
        ],
        "without": ["Zahnzusatzversicherung Vergleich", "So hoch sind die Kreditzinsen 2020", "Können wir helfen?"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.focus.de/auto/experten/auto-leasen-oder-kaufen-fuer-wen-lohnt-sich-was_id_9209161.html": {
        "file": "focus.de.leasen.html",
        "author": "Robin Tschöpe",
        "title": "Auto leasen oder kaufen: Für wen lohnt sich was?",
        "date": "2018-07-06",
        "description": "Leasen, finanzieren oder kaufen? Wer ein neues Auto will, hat mehrere Möglichkeiten. Jede bringt ihr Vor- und Nachteile mit. FOCUS-Online-Experte Robin Tschöpe hat sie verglichen.",
        "categories": [],
        "tags": [],
        "with": [
            "FOCUS-Online-Experte Robin Tschöpe hat sie verglichen.",
            "Mit einem Schlag ist d",
            "Wer es gerne flexibel mag",
        ],
        "without": ["Bitte loggen Sie sich vor dem Kommentieren ein", "„Experten“ abonnieren", "Persönlicher Newsletter"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.comparis.ch/leasing/info/autofinanzierung": {
        "file": "comparis.ch.autofinanzierung.html",
        "author": "",
        "title": "Finanzierung Ihres Autos",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Eine häufig gestellte Frage: Leasing oder Autokredit?",
            "Total Differenz (Ersparnis beim Leasing)",
            "Welche Art der Autofinanzierung ideal ist",
        ],
        "without": [
            "Immer aktuell informiert über Sparmöglichkeiten sowie Experten-Tipps",
            "8003 Zürich",
            "Mit der Anmeldung stimme ich der Bearbeitung",
        ],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://www.verivox.de/kredit/leasing-oder-finanzierung/": {
        "file": "verivox.de.finanzierung.html",
        "author": "",
        "title": "Leasing oder Finanzierung? Jetzt Angebote berechnen!",
        "date": "",
        "description": "Leasing oder Finanzierung? Die Verivox-Tarifexperten zeigen, ob Sie Ihr Auto leasen oder kaufen sollten – mit Rechnern, Beispielen, Vor- und Nachteilen.",
        "categories": [],
        "tags": [],
        "with": [
            "In diesem Ratgeber finden Sie Rechenbeis",
            "kann als Barzahler auftreten und einen Rabatt aushandeln.",
            "Die Drei-Wege-, Ballon- bzw. Vario-Finanzierung",
        ],
        "without": [
            "sachlich und geduldig",
            "Der Verivox-Newsletter",
            "in den Bereichen Energie, Telekommunikation, Versicherungen",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://fincompare.de/firmenwagen-leasing-oder-finanzierung": {
        "file": "fincompare.de.firmenwagen.html",
        "author": "Martin Junker",
        "title": "Firmenwagen: Leasing oder Finanzierung?",
        "date": "2019-10-07",
        "description": "Leasen oder Finanzieren eines Firmenwagens - Erfahren Sie die Besonderheiten sowie die Vor- und Nachteile ✔ für Ihr Unternehmen!",
        "categories": [],
        "tags": [],
        "with": [
            "In diesem Artikel stellen wir die wichtigsten Punkte und vor allem die steuerlichen Aspekte",
            "ist die Höhe der Monatsraten dementsprechend niedriger als beim Kilometerleasing.",
            "Kann nicht steuerlich geltend gemacht werden",
        ],
        "without": [
            "Umsatzsteuererstattung bei Leasing und Mietkauf?",
            "Nutzen Sie FinCompare als Wettbewerbsvorteil",
            "vielfältige Suchoptionen, Transparenz, Übersichtlichkeit",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.giromatch.com/online-kredit/1000-euro-kredit": {
        "file": "giromatch.com.kredit.html",
        "author": "",
        "title": "1000 Euro Kredit",
        "date": "",
        "description": "1000 Euro Kredit von GIROMATCH ✓ Günstig & unkompliziert ✓ Auszahlung direkt aufs Konto ✓ 100% Unverbindlich ➤ Jetzt 1000 Euro Kredit sichern ",
        "categories": [],
        "tags": [],
        "with": [
            "Fragen Sie noch heute den Kredit an und Sie haben bestenfalls morgen",
            "Grundeinkommen bzw. keine Überschuldung",
            "mit Expressüberweisung auch als Blitzkredit auszahlbar.",
        ],
        "without": ["info@giromatch.com", "Ausgewählte Kreditprodukte", "Bewerten Sie dieses Produkt"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.financescout24.de/kredit/autokredit": {
        "file": "financescout24.de.autokredit.html",
        "author": "",
        "title": "Jetzt günstigen Autokredit finden",
        "date": "",
        "description": "Jeder zweite Neuwagen wird mit Hilfe eines Kredits gekauft. Vergleichen Sie Jetzt bequem online, unverbindlich und schufa-neutral günstige Autokredite.",
        "categories": [],
        "tags": [],
        "with": [
            "Diese bringt weitere Kosten mit sich.",
            "hat der Finanzierer größere Chancen auf eine Vergütung ohne Abschläge",
            "Wieso sind Autobank-Kredite trotz niedriger Zinsen oft teurer?",
        ],
        "without": ["Die Nr. 1 rund um Immobilien", "© Copyright 2000", "Aktuelle News"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://web.archive.org/web/20140226054445/http://www.time4talks.com/2013/08/07/weitere-digitalisierung-der-schweizer-kinos/": {
        "file": "archive.org.time4talks.com.kinos.html",
        "author": "R. R.",
        "title": "Weitere Digitalisierung der Schweizer Kinos",
        "date": "2013-08-07",
        "description": "Digitalisierung der Schweizer Kinos",
        "categories": [],
        "tags": [],
        "with": [
            "Die Umstellung auf Hightech-Beamer hat nämlich kein Kinosterben verursacht",
            "Das BAK will mit diesen Beiträgen die Digitalisierung",
            "Auf 270 Leinwänden sind auch 3-D-Filme zu sehen.",
        ],
        "without": ["Bisher keine Kommentare", "(erforderlich)", "Nutzen Sie unsere Tools"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20181206101316/https://swap-stop.org/de/filmswap/zusammenarbeit-shuji-walter-april-2018-i/": {
        "file": "archive.org.swap-stop.org.shuji.html",
        "author": " Walter von Aachen",
        "title": "Zusammenarbeit Shuji ./. Walter April 2018 I",
        "date": "2018-04-11",
        "description": "Standorte: Shuji: Japan. Walter: Deutschland. Filmmaterial: Fuji X-TRA 400. Kameras: Shuji: Widelux. Walter: PENTAX Z-1 p. Belichtungsfolge: Shuji. Walter.",
        "categories": ["Filmswap", "Shuji-Walter"],
        "tags": [
            " Deutschland",
            "Doppelbelichtung",
            "Filmswap",
            "Fujifilm X-TRA 400",
            "Japan",
            "PENTAX Z-1p",
            "Shuji",
            "Walter",
            "zusammenarbeit",
        ],
        "with": ["Fuji X-TRA 400.", "Walter: PENTAX Z-1", "Belichtungsfolge"],
        "without": ["Wird geladen", "Teilen mit:", "(c) 2016"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20160401095740/http://www.welpenkaufen24.de/": {
        "file": "archive.org.welpenkaufen24.de.html",
        "author": "",
        "title": "Welpen kaufen – Tipps zu jeder Hunderasse",
        "date": "",
        "description": "Blog zum Thema Welpen-Kaufen. Tipps zum Welpenkauf in jeder Hunderasse. Augen auf beim Welpen-Kauf!",
        "categories": [],
        "tags": [],
        "with": [
            "dass Bekannte bei unseriösen Züchtern",
            "Beschimpfungen akzeptiere ich aber nicht unter den Kommentaren.",
            "möchte ich in diesem Blog den ein oder",
        ],
        "without": ["Hunderassen", "Welcher Hund passt zu mir?", "Erforderliche Felder sind markiert"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://web.archive.org/web/20160330101229/http://muffinrezept.net/muffin-grundrezept": {
        "file": "archive.org.muffinrezept.net.grundrezept.html",
        "author": "",
        "title": "Muffin Grundrezept",
        "date": "",
        "description": "",
        "categories": ["Grundrezept", "Rezepte"],
        "tags": [],
        "with": [
            "Ob Schokostückchen, Kokosraspeln, Kakaopulver, Erdbeeren, Kirschen oder anderes Obst",
            "bei 180 Grad auf mittlerer Schiene",
            "15 – 30 Min",
        ],
        "without": ["Fluffige Himbeermuffins", "Kommentieren", "Bildquellen"],
        "comments": [
            "Warum 2mal Zucker ?:-)",
            "man auch Lebensmittelfarbe hinzufügen?",
            "Könnt ihr mir sagen, ob die Silikonform daran schuld war?",
        ],
        "license": "CC-BY-SA",
        "region": "",
    },
    "https://web.archive.org/web/20160218174457/http://bewegliche-lettern.de/2010/05/literatur-und-animated-typography/": {
        "file": "archive.org.bewegliche-lettern.de.typography.html",
        "author": "",
        "title": "Literatur und Animated Typography",
        "date": "2010-05-19",
        "description": "bewegliche lettern ist das private blog von Thomas Rohde über Literatur und die Buchindustrie im Medienwandel.",
        "categories": ["Lesenswert", "Literatur", "Medienwandel"],
        "tags": ["Animated", "Typography", "iPad", "Vook"],
        "with": [
            "Ich schlage darin vor, in der Remix-Kunst der Animated Typography ein Beispiel dafür zu sehen",
            "und der Literatur vielleicht besonders gerechte",
        ],
        "without": [
            "Lesenswert: Interview über Google Editions in Deutschland",
            "Comments are closed.",
            "Alle redaktionellen Eigenbeiträge",
        ],
        "comments": [],
        "license": "CC BY-NC-SA 3.0 DE",
        "region": "",
    },
    "https://web.archive.org/web/20150721045344/http://rent-a-pastor.com/2015/05/18/neue-hochzeitslokation-in-roedermark-hessen-geheimtipp/": {
        "file": "archive.org.rent-a-pastor.com.hochzeitslokation.html",
        "author": "Samuel Diekmann",
        "title": " Neue Hochzeitslokation in Rödermark/ Hessen – Geheimtipp",
        "date": "",
        "description": "Blog über freie und kirchliche Trauungen, Hochzeiten und Eheschließungen. Alles rund ums Heiraten, Hochzeitsfeiern, Rituale und Zeremonien.",
        "categories": [],
        "tags": [],
        "with": [
            "am Parkhotel vorbei gefahren und habe über das weiträumige Gelände gestaunt",
            "auch einen unglaublichen 5000 m2 Park mit See und Springbrunnen",
            "Redner in der Region findest Du",
        ],
        "without": ["Kommentar verfassen", "Melden Sie sich für unseren Newsletter an", "Di-Fr 10-18:00 Uhr. "],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20171008220355/http://juergenheitmann.com/essays/2017/01/aggression-fotografie/": {
        "file": "archive.org.juergenheitmann.com.aggression.html",
        "author": "Jürgen Heitmann",
        "title": "Aggression Fotografie",
        "date": "2017-01-26",
        "description": "Fotografie ein Akt der Aggression? Fotos schießen, Schnappschuss, Fotoshooting ... Das geschossene Foto als Trophäe. Das klingt schon recht aggressiv, nach jage…",
        "categories": [],
        "tags": ["aggression", "kontemplativ"],
        "with": [
            '"To photograph people is to violate them"',
            "in vergangenen Kulturen und unserer aktuellen Gesellschaft (70er Jahre)",
            "welche alternativen Ausdrücke die empfangenden Haltung",
        ],
        "without": ["View all essays by tag", "#kontemplativ", "Mindfulness und kontemplative Fotografie"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20080731095558/http://www.dimido.de/2008/07/29/was-ist-virales-marketing/": {
        "file": "archive.org.dimido.de.marketing.html",
        "author": "Martin Weber",
        "title": "Was ist Virales Marketing?",
        "date": "",
        "description": "Was ist Virales Marketing?",
        "categories": [],
        "tags": [],
        "with": [
            "Marketing halten, habe aber keine Lust dazu, dies zu machen",
            "was unter Virales Marketing zu verstehen ist und wie wir unbewusst dadurch beeinflusst werden",
            "von Virales Marketing, habe ich festgestellt.",
        ],
        "without": [
            "besserwisser: Stecker ziehen für ne neue IP bringt nix.",
            "übernimmt Cherry Corporation",
            " E-Mail (wird benötigt und nicht veröffentlicht)",
        ],
        "comments": [],
        "license": "CC BY-NC-SA 2.0 DE",
        "region": "DE",
    },
    "https://web.archive.org/web/20140109030403/http://nesselsetzer.wordpress.com/2013/12/09/rebloggt-von-gnaddrig-ad-libitum-antipoden-die-wahrheit/": {
        "file": "archive.org.nesselsetzer.wordpress.com.antipoden.html",
        "author": "Nesselsetzer",
        "title": "Rebloggt von gnaddrig ad libitum: Antipoden: Die Wahrheit",
        "date": "2013-12-09",
        "description": "Gnaddrigs erstaunliche Betrachtungsweise und die Entwicklung einer Theorie zu einer offensichtlich aus dem Nichts aufgetauchten Schuhsohle soll heute als lehrreiches Stück und Vorbild für die Entwi...",
        "categories": ["Just For Fun", "Rebloggt"],
        "tags": ["Antipoden", "Hirngespinst", "Kasparei", "Theorie", "Weltwissen"],
        "with": [
            "Gnaddrigs erstaunliche Betrachtungsweise und die Entwicklung einer Theorie",
            "ob auf der anderen Seite der Erde überhaupt Menschen leben können.",
            "musste so sein, weil wir hier ja nachweislich mit den Füßen nach unten und dem Kopf nach oben herumlaufen",
        ],
        "without": ["Die dümmste aller Verschwörungstheorien: Chemtrails", "Gefällt mir", "Ähnliche Beiträge"],
        "comments": ["Schöne Einleitung", " Ich verbringe meine Tage normalerweise nicht damit, auf die", "Same here"],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20150206075900/http://www.steinzeitwissen.de/artefakttypen/werkzeuge-des-neandertalers-und-des-modernen-menschen": {
        "file": "archive.org.steinzeitwissen.de.werkzeuge.html",
        "author": "",
        "title": "Werkzeuge des Neandertalers und des Modernen Menschen",
        "date": "",
        "description": "Werkzeuge des Neandertalers und des Modernen Menschen",
        "categories": [],
        "tags": [],
        "with": [
            "erk­zeug­ty­pen und ihre Lauf­zei­ten be­han­delt.",
            "uge und sah sich of­fen­bar nicht ver­an­lasst, die Kern­werk­zeuge zu übernehmen.",
            "m Alt­pa­läo­li­thi­kum bis in die Neu­zeit, Tü­bin­gen 2012, Kerns Ver­lag, S. 426",
        ],
        "without": ["Proudly powered by WordPress.", "Überblick + Schülerhilfe", "Artikel Mittelpaläolithikum"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://web.archive.org/web/20160820205919/http://www.medialepfade.de/2016/01/medienpaedagogin-in-muenchen-gesucht/": {
        "file": "archive.org.medialepfade.de.medienpaedagogin.html",
        "author": "Danilo Dietsch",
        "title": "MedienpädagogIn in München gesucht",
        "date": "2016-01-15",
        "description": "Wir suchen eine MedienpädagogIn in München in Teilzeitanstellung (60%) “medialepfade.de – Agentur für Medienbildung” ist eine Agentur im Bereich der Medienbildung und Medienpädagogik. Zu unseren Aktivitäten gehören die Konzeption und Durchführung von Aktionen, Projekten und Fortbildungen in den Bereichen Mobiles Lernen, Web-Video, Online-Journalismus, sowie ePartizipation, Games und Open Education. Unser inhaltlicher Schwerpunkt liegt auf der …",
        "categories": [],
        "tags": [],
        "with": [
            "Web-Video, Online-Journalismus, sowie ePartizipation, Games und Open Education. Unser inhaltlicher Schwerpun",
            "Professionalität und Souveränität im Umgang mit Partnern und Förderern",
            "ngabe des möglichen Eintrittstermins bis zum 01. Februar 2016 an",
        ],
        "without": [
            "lauffähiges Wifi, angetrieben durch ein Fahrrad, um zum Umweltschutz zu animieren @jhacktost https://t.co/8elCKJjm3o",
            "Blog-Themen:",
            "Möchten Sie unseren Newsletter erhalten?",
        ],
        "comments": [],
        "license": "CC BY-SA 3.0 DE",
        "region": "DE",
    },
    "https://www.piratenpartei-hessen.de/blog/2020/03/31/solidaritaet-nachbarschaftshilfe/": {
        "file": "piratenpartei-hessen.de.nachbarschaftshilfe.html",
        "author": "Martina Scharmann",
        "title": "Solidarität = Nachbarschaftshilfe",
        "date": "2020-03-31",
        "description": "Piraten rufen zur Einhaltung der Corona-Schutzmaßnahmen und gegenseitiger Solidarität auf! Die Corona-Pandemie breitet sich aus. Ungeachtet der zahlreichen inzwischen eingeleiteten Maßnahmen steigt die&hellip;",
        "categories": [],
        "tags": ["Corona", "Covid-19", "Covid19", "Hilfe", "Piraten", "Piratenpartei", "RKI", "Robert-Koch-Institut"],
        "with": [
            "anbieten und ihren Beitrag leisten,",
            "Wohle der Allgemeinheit riskieren. Auch die zahlreichen privaten Initiativen",
            "ng der Corona-Schutzmaßnahmen und gegenseitiger Solidarität auf",
        ],
        "without": ["0 Piratenpartei Hes", "Bundesschiedsgericht", "vKV Kassel Stadt-Land-Web"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://gormulus.wordpress.com/2012/12/11/das-wird-man-ja-wohl-noch-sagen-durfen/": {
        "file": "gormulus.wordpress.com.durfen.html",
        "author": "",
        "title": "„Das wird man ja wohl noch sagen dürfen!“",
        "date": "2012-12-11",
        "description": "Dieser Artikel folgt auf einen betont sachlich gehaltenen Beitrag über die Diskussionsunkultur beim Thema israelisch-palästinensischer Konflikt. Der @tarzun würde sagen, dass wir mal wieder reden m…",
        "categories": ["Inland", "Politik", "Rant"],
        "tags": ["Antisemitismus"],
        "with": [
            "leicht beratungsresistent erscheint.",
            "Ein regelrechter Hammer ist dann die Gleichsetzung von Gaza mit einem KZ.",
            "sobald ihre abstruse Gedankenwelt etwas näher beleuchtet wird",
        ],
        "without": ["Mielke 2.0", "icken des JMStV gewidmet.", "Updates!"],
        "comments": [
            "ie gemeint sind. Vielmehr soll jede kritische Stimme der Politik im Nahen und Mittleren Osten zum Schweig",
            "mir einen offen Brief mit Unterschriftenliste gewuenscht.",
            "offenem Antisemitismus zu garnieren und das ganze Paket unter dem Deckmäntelchen der Mei",
        ],
        "license": "",
        "region": "CC BY-NC-SA 3.0 DE",
    },
    "http://diy-expeditions.com/expeditionen-planen/expeditionen-in-uebersee/": {
        "file": "diy-expeditions.com.uebersee.html",
        "author": "",
        "title": "Expeditionen in Übersee",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Wir gehen gerne mit Ihnen Ihr Expeditionskonzept durch.",
            "Falls Sie sich für ein vorgeschlagenes Reise-Paket der auf unserer News-Seite vertretenen Tour-Veranstalter entscheiden",
            "Sie bezahlen Ihren Guide, Transport, Unterkunft etc. vor Ort und direkt bei Ihrem von uns vermittelten Kontakt.",
        ],
        "without": ["Fahrzeug samt Fahrer", "Neuigkeiten aus unseren Destinationen", "y-expeditions.com. All rights reserved"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://kleinegruenemonster.wordpress.com/2016/01/01/ein-entspannter-start-ins-neue-jahr-2016-be-happy/": {
        "file": "kleinegruenemonster.wordpress.com.start.html",
        "author": "KleineGrüneMonster",
        "title": "Ein entspannter Start ins neue Jahr 2016 – be happy! Alles andere kann warten…",
        "date": "2016-01-01",
        "description": "Das Wichtigste zuerst: Euch allen ein wunderschönes, neues Jahr 2016, voller Glück, Freude und Schabernack :) Ein neues Jahr beginnt. Auch wenn jedem Morgen ein Neuanfang innewohnt, so hat für mich…",
        "categories": ["Empfehlung", "Plattformen", "Schöne Dinge"],
        "tags": ["Entspannung", "Glück", "Neues Jahr", "Rituale, Wellness"],
        "with": [
            "geht es um Themen wie Entspannung, Meditation und Wellness, aber auch Essen, Leben und Fitness.",
            "Man zieht Bilanz. Was hat das vergangene Jahr gebracht?",
            "Wer, verdammt noch mal, hat die 40 Stunden Arbeitswoche erfunden?",
        ],
        "without": [
            "r unter Namensnennung bzw. Linksetzung. Danke.",
            "Benachrichtigungen über neue Beiträge zu",
            " Verwendung, Vervielfältigung und Weitergabe der Inhalte",
        ],
        "comments": [
            "Man denkt immer, es ist nicht viel passiert, aber wenn man es genau nimmt, dann tut sich doch immer einiges"
        ],
        "license": "CC BY-NC 3.0 DE",
        "region": "",
    },
    "https://www.markeich.de/kontakt/impressum-werbeagentur-soltau/": {
        "file": "markeich.de.impressum.html",
        "author": "",
        "title": "Impressum",
        "date": "",
        "description": "Impressum der Werbeagentur MARKE ICH in Soltau im Heidekreis. ",
        "categories": [],
        "tags": [],
        "with": [
            "ngaben gemäß § 5 TMG",
            "bieter oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft. Rechtsw",
            "rtlich für den Inhalt nach § 55 Abs. 2 RStV",
        ],
        "without": ["Auszeichnungen", "© 2020 Agentur MARKE ICH", "Es gilt die Datenschutzerklärung."],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://www.schlosswirtjuval.it/hof-geschichte/": {
        "file": "schlosswirtjuval.it.geschichte.html",
        "author": "",
        "title": "Zur Geschichte des „Oberortlhofs“",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Leider war dies nicht von langer Dauer, denn bereits 1581",
            "Den Möglichkeiten des Kommunikationszeitalters setzt er sein Unterwegssein",
            "alle 6 bis 14-jährigen Kinder der Juvaler Höfe zum Unterricht",
        ],
        "without": [
            "Messner Mountain Museum Juval",
            "+39 389 1976362 info@schlosswirtjuval.it",
            "Weingut & Hofbrennerei Unterortl",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.digitale-exzellenz.de/ki-china-teil-2-wie-das-fernost-facebook-das-gesundheitswesen-revolutioniert/": {
        "file": "digitale-exzellenz.de.gesundheitswesen.html",
        "author": "Yirou Chen",
        "title": "KI @ China (Teil 2): Wie das Fernost-Facebook das Gesundheitswesen revolutioniert",
        "date": "2018-10-24",
        "description": "Tencent will das Gesundheitssystem Chinas mithilfe von KI revolutionieren und investiert massiv in die medizinische Versorgung.",
        "categories": ["Healthcare"],
        "tags": ["China", "Gesundheitswesen", "INSURANCE_HEALTH_SOCIAL", "KI", "Tencent"],
        "with": [
            "Nach einem Einblick in zwei künstlich intelligente Sicherheitsprojekt",
            "Chinas medizinische Versorgung ist, salopp gesagt, verbesserungswürdig: wenig ",
            "Weitere genutzte Quellen in englischer und chinesischer Sprache:",
        ],
        "without": ["Empfohlene Beiträge", "Schreibe einen Kommentar ", "Process Mining und Verhaltensvielfalt miteinander"],
        "comments": [],
        "license": "DE",
        "region": "",
    },
    "https://www.mdr.de/thueringen/corona-lockerung-autohaeuser-werkstatten-100.html": {
        "file": "mdr.de.autohaeuser.html",
        "author": "MDR THÜRINGEN/ls",
        "title": "Autohäuser rechnen mit langsamem Anlaufen des Geschäfts",
        "date": "2020-04-20",
        "description": "Autohändler in Thüringen dürfen ihre Verkaufsräume wieder öffnen. Mit einem großen Ansturm rechnen sie angesichts der andauernden Corona-Krise jedoch nicht.",
        "categories": ["Thüringen"],
        "tags": [],
        "with": [
            "Geschäftes. Helmut Peter von der gleichnamigen Autohaus-Gruppe sagte MDR THÜRINGEN am Mo",
            "ann. Nach Informationen von MDR THÜRINGEN hatte ein VW-Händler in Erfurt bis Montagmorgen nicht gewusst, dass er wieder Kunden im Autohaus beraten darf. Ein BMW-Händler in Weimar erklärte, auch in d",
            "am Montag, die Händler seien froh, dass sie wieder die Verkaufsräume öffnen dürften. Allerdings se",
        ],
        "without": [
            "Weitere Informationen zum Coronavirus in Thüringen:",
            "Mehr aus Thüringen",
            "Der Mitteldeutsche Rundfunk ist Mitglied der ARD.",
        ],
        "comments": ["Daran, dass die Autohändler so ziemlich als erst"],
        "license": "",
        "region": "DE",
    },
    "https://pythonspeed.com/articles/pipenv-docker/": {
        "file": "pythonspeed.com.docker.html",
        "author": "Itamar Turner-Trauring",
        "title": "Faster Docker builds with pipenv, poetry, or pip-tools",
        "date": "2020-06-04",
        "description": "Installing dependencies separately from your code allows you to take advantage of Docker&rsquo;s layer caching. Here&rsquo;s how to do it with pipenv, poetry, or pip-tools.",
        "categories": [],
        "tags": [],
        "with": [
            "CMD flask run exampleapp:app",
            "The takeaway",
            "Install dependencies separately and earlier in your Dockerfile to ensure faster builds.",
        ],
        "without": [
            "Learn how to build fast, production-ready Docker images—read the rest of ",
            "You need to stay competitive in the job market—but there",
            "Next: Elegantly activating a virtualenv in a Dockerfile",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.bbc.com/news/world-us-canada-52241221": {
        "file": "bbc.com.52241221.html",
        "author": "",
        "title": "Coronavirus: New York ramps up mass burials amid outbreak",
        "date": "2020-04-10",
        "description": "Drone footage shows coffins stacked in a pit in the city, as the state logs more cases than any country.",
        "categories": ["Coronavirus pandemic"],
        "tags": ["New York", "Coronavirus pandemic", "United States"],
        "with": [
            "ried in a mass grave in New York City, as the death toll from the coronavirus continues to rise.",
            "The daily rise in coronavirus deaths announced",
            "unemployment claims had topped",
        ],
        "without": [
            "Can we answer your question on the coronavirus?",
            "Four out of five jobs affected by virus globally",
            "Top Stories",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.handelsblatt.com/politik/international/grenzschliessungen-report-von-der-deutsch-franzoesischen-grenze-der-partner-wird-zum-fremden/25776812.html": {
        "file": "handelsblatt.com.grenzschliessungen.html",
        "author": "Thomas Hanke",
        "title": "Deutschland, Frankreich und die Rückkehr der Ressentiments",
        "date": "2020-04-27",
        "description": "Frankreich,Deutschland,Luxemburg,Coronakrise,Grenzschließungen,Ressentiments,Außenpolitik mit Land,ZF,Innenministerium,Ford,Deutschlandradio,En Marche!,CDU,TAZ,Christophe Arend,Helmut Kohl,Emmanuel Macron,Jean-Yves Le Drian,Andreas Jung,Armin Laschet",
        "categories": [],
        "tags": [],
        "with": [
            "Wenn Helmut Kohl emotional wu",
            "en darf und vor allen Dingen nicht zwischen Deutschland und Frankreich.“",
            "an der Grenze zu Frankreich ",
        ],
        "without": ["Jetzt weiterlesen", "Serviceangebote", "aktivieren"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.pcgamer.com/through-the-darkest-of-times-review/": {
        "file": "pcgamer.com.darkest.html",
        "author": "Luke Kemp",
        "title": "Through the Darkest of Times review",
        "date": "2020-02-11",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            'your grip on the concept further, by saying little more than "go s',
            "Developer Paintbucket Games",
            "A superbly crafted game that serves as storyteller, teacher, and concerned friend.",
        ],
        "without": ["PC Gamer Newsletter", "C Gamer is supported by its audience. When you buy throu", "Also on PC Gamer"],
        "comments": [
            "Down-votes are allowed again? Oh jolly.",
            "n stopped. China buying PPE from countries all over the planet and selling it back at a huge ma",
            "hard enough which is very disappointing. This could have been a great opportunity to show ",
        ],
        "license": "",
        "region": "",
    },
    "https://www.thelocal.se/20200428/meet-the-swede-who-tattooed-a-state-epidemiologists-face-on-his-arm": {
        "file": "thelocal.se.tattooed.html",
        "author": "AFP/The Local",
        "title": "Meet the Swede who tattooed a state epidemiologist's face on his arm",
        "date": "2020-04-28",
        "description": "Whether you&#039;re for or against Sweden&#039;s softer approach to coronavirus lockdowns, there is no denying state epidemiologist Anders Tegnell has become a household name in the country during the crisis.",
        "categories": [],
        "tags": ["tattoo", "covid-19"],
        "with": [
            "epidemiologist Anders Tegnell has become a household name",
            "to get the tattoo after Tastas advertised the design",
            "Asked about the tattoo last week by newspaper GP",
        ],
        "without": ["to leave a comment", "Advertisement", "The latest news about the coronavirus outbreak"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://uepo.de/2020/04/26/digitales-woerterbuch-der-deutschen-sprache-redaktion-erstellt-glossar-zur-corona-pandemie/": {
        "file": "uepo.de.glossar.html",
        "author": "BBAW",
        "title": "Digitales Wörterbuch der deutschen Sprache: Redaktion erstellt Glossar zur Corona-Pandemie",
        "date": "2020-04-26",
        "description": "Digitales+W%C3%B6rterbuch+der+deutschen+Sprache%3A+Redaktion+erstellt+Glossar+zur+Corona-Pandemie",
        "categories": ["Deutsche Sprache"],
        "tags": [],
        "with": [
            "Weiterführender Link",
            "randenburgischen Akademie der Wissenschaften (BBAW) die in Presse und Medien bereits sichtb",
            "c) [Militär] Strategie für den geordneten Abzug eines Truppenkontingents aus dem Auslandseinsatz",
        ],
        "without": [
            "Twitter-Kurznachrichten",
            "Mehr zum Thema auf UEPO.de",
            "Das Übersetzerportal UEPO.de ist seit 2001 die Tagesschau der Übersetzungsbranche im ",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.bdzv.de/nachrichten-und-service/presse/pressemitteilungen/artikel/detail/olafur-eliasson-gestaltet-titelseite-fuer-die-deutschen-zeitungen/": {
        "file": "bdzv.de.eliasson.html",
        "author": "",
        "title": "Olafur Eliasson gestaltet Titelseite für die deutschen Zeitungen",
        "date": "2020-04-24",
        "description": "Bundesweite Kunstaktion zum Internationalen Tag der Pressefreiheit am 3. Mai",
        "categories": ["Pressemitteilungen"],
        "tags": ["Pressefreiheit"],
        "with": [
            "esichts der Corona-Krise und ihrer Folgen für die Gesellschaft ist das Thema ",
            "effpunkt von Journalist, Text und Leser fokussiert. Das Werk entstan",
            "rall auf der Welt das Recht haben muss, frei und ohne Angst berichten zu können.",
        ],
        "without": ["zurück", "nach oben", "English"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://bumsbutzener-gumpfen.blogspot.com/2020/04/tach-auch.html": {
        "file": "bumsbutzener-gumpfen.blogspot.com.tach-auch.html",
        "author": "der Michel",
        "title": "Tach auch!",
        "date": "2020-04-28",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Ich hätte zwar das ein oder andere Mal noch Lust gehabt, den ein oder ande",
            "weck verfolgt, Kranke zu heilen und Brunnen zu bauen.",
            "Oder, um es mit Reinhard Mey zu sagen:",
        ],
        "without": ["Dieses Blog durchsuchen", "Eingestellt von der Michel", "Nachdem ProSieben mit seinem Auktionshaus"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.tagesschau.de/investigativ/ndr/rheinmetall-datenleck-101.html": {
        "file": "tagesschau.de.rheinmetall.html",
        "author": ["Volkmar Kabisch", "Jan Lukas Strozyk", "Benedikt Strunz", "NDR"],
        "title": "Daten von Rheinmetall gehackt",
        "date": "2020-04-28",
        "description": "Der Rüstungskonzern Rheinmetall ist nach <em>NDR</em>-Recherchen von einem Datenleck betroffen: Mehr als 1000 interne Unterlagen kursieren im Netz, auch zu Panzerfahrzeugen. Neben dem Image-Schaden droht dem Konzern ein Bußgeld.",
        "categories": [],
        "tags": [],
        "with": [
            "h NDR-Recherchen von einem Datenleck betroffen: Mehr als 1000 interne Unterlagen kursiere",
            "Der Datensatz liegt dem NDR vor.",
            "Rheinmetall stellt in den damals betroffenen Fabriken Bauteile für die Autoindustrie her.",
        ],
        "without": ["Darstellung", "Rundfunkanstalten", "Tagesschau Investigativ"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.neues-deutschland.de/artikel/1136087.mietenstreik-in-den-usa-einfach-kein-geld-mehr-um-die-miete-zu-zahlen.html": {
        "file": "neues-deutschland.de.mietenstreik.html",
        "author": "Moritz Wichmann",
        "title": "»Einfach kein Geld mehr, um die Miete zu zahlen«",
        "date": "2020-04-29",
        "description": "Ab dem 1. Mai könnte es in den USA Mietstreiks geben - wenige explizit erklärte, womögliche viele unausgesprochene. Aktivisten fordern einen Mietenstopp in der Coronakrise. Sie warnen vor der Verzweiflung vieler neuer Corona-Arbeitsloser.",
        "categories": ["Politik"],
        "tags": ["Arbeitslosigkeit", "Coronakrise", "Mieten", "Mietenpolitik", "Mietenwahnsinn", "USA"],
        "with": [
            "In den Vereinigten Staaten trommeln Aktivisten für einen Mietenstopp in der Coronakrise und warnen Vermieter",
            "gigen Mietergewerkschaft Autonomous Tenant Union (ATU) aus Chicago sagt auch",
            "wie Oakland oder Seattle und auch in Philadelphia haben Aktivisten",
        ],
        "without": [
            "Hat Ihnen dieser Artikel gefallen? Dann teilen Sie ihn doch mit anderen",
            "ptstadtregion, die sich aus der Verbreitung des Coronavirus ergeben.",
            "Früher war mehr Lametta.",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://blog.amp.dev/2020/04/07/people-behind-the-code-the-axios-ascent/": {
        "file": "blog.amp.dev.axios.html",
        "author": "Alex Durán",
        "title": "People behind the code: The Axios ascent",
        "date": "2020-04-07",
        "description": "Digital media company Axios has stepped onto the scene with a quick, smart, audience-first experience. Sound familiar? Fast, audience-first and efficient – talk about mission alignment. Maris…",
        "categories": [],
        "tags": [],
        "with": [
            "shift to AMP-first. We invited the duo for a chat to discover how a beta test in 2019 escalated",
            "Were there any challenges you had to overcome?",
            "color in your pencil case, you start drawing a lot quicker instead of worrying about shades",
        ],
        "without": [
            "Your email address will not be published.",
            "iscussions, and advanced tutorials straight to your inbox with the AMP newsletter.",
            "All rights reserved. The OpenJS Foundation",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.fr.de/politik/kim-jong-un-nordkorea-bilder-diktator-donald-trump-zr-13680734.html": {
        "file": "fr.de.nordkorea.html",
        "author": "FR mit dpa",
        "title": "Kim Jong Un: Der Diktator ist zurück - Donald Trump ist „glücklich“",
        "date": "2020-05-04",
        "description": "Kim Jong Un taucht nach Wochen wieder auf. Die Bilder, die das beweisen sollen, erfreuen Donald Trump. Er sendet Gr&#252;&#223;e nach Nordkorea.",
        "categories": ["Politik"],
        "tags": ["Nordkorea", "Donald Trump", "Kim Jong Un"],
        "with": [
            "Er sendet Grüße nach Nordkorea.",
            "wenn auch nur in der demilitarisierten Zone im Grenzgebiet und nur für ein paar Schritte.",
            "runggelenk operierte worden und deshalb wochenlang verschwunden gewesen sei",
        ],
        "without": ["Das könnte Sie auch interessieren", "Abo-Service", "Mehr zum Thema"],
        "comments": [
            "keit gesehen wurde? Man sollte sich an dem Personenkult, der in Nordkorea um diesen Mann betrieben wird, nicht auch noch beteiligen.",
            "tiker die Zähne ausbeißen. Vergessen Sie es. Im Fernen Osten haben d",
            "dhismus ist mehr Körperfülle - weshalb auch immer - mit mehr Autorität behaftet.",
        ],
        "license": "",
        "region": "DE",
    },
    "https://www.tagesspiegel.de/wirtschaft/abstandsregeln-und-fieberkontrollen-wie-firmen-ihre-beschaeftigten-vor-dem-coronavirus-schuetzen/25784520.html": {
        "file": "tagesspiegel.de.abstandsregeln.html",
        "author": "Marie Rövekamp",
        "title": "Wie Firmen ihre Beschäftigten vor dem Coronavirus schützen",
        "date": "2020-04-29",
        "description": "Damit Mitarbeiter gesund bleiben, müssen sich Unternehmen einiges einfallen lassen. Die Ideen reichen vom Spuckschutz bis zur Kontrolle der Körpertemperatur.",
        "categories": ["Wirtschaft"],
        "tags": ["Coronavirus"],
        "with": [
            "Die Ideen reichen vom Spuckschutz bis zur Kontrolle d",
            "Heil mahnte: Besorgt ausreichend Seife und Desinfektionsmittel!",
            "Das Liefergeschäft mit Hotels, das die Hälfte des Umsatzes ausmachte, ist weggebrochen",
        ],
        "without": ["Diskutieren Sie mit!", "Meistdiskutiert", "Login"],
        "comments": ["erfahren zu sein. Ich habe es bei Bayer Berlin in Anwendung erlebt - vollkommen unkompliziert. "],
        "license": "",
        "region": "DE",
    },
    "https://www.die-tagespost.de/leben/glauben-wissen/Warum-wir-jetzt-Demut-brauchen;art4886,207643": {
        "file": "die-tagespost.de.Demut.html",
        "author": "Christoph von Ritter",
        "title": "Warum wir jetzt Demut brauchen",
        "date": "2020-04-24",
        "description": "Viele der zur Abwehr des Virus SARS-CoV-2 ergriffenen könnten am Ende mehr Schäden anrichten, als das Virus selbst, fürchtet der Autor, der selbst Arzt ist. Ein Debattenbeitrag.",
        "categories": ["Glaube & Wissen"],
        "tags": [],
        "with": [
            "sondern auch politische Maßnahmen, wie die zur Bekämpfung einer Pandemie",
            "In der Tat: Der moderne, säkulare Mensch scheint weder Feigheit noch Schwäche zu kennen.",
            "nwirkungen unserer Maßnahmen angesichts der SARS-CoV-2 Pandemie in den Blick zu nehmen",
        ],
        "without": ["Weitere Artikel", "Ihre Meinung zu diesem Thema", "Triage: Ein medizinethisches Dilemma"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.furche.at/gesellschaft/achtsam-durch-die-krise-2497954": {
        "file": "furche.at.achtsam.html",
        "author": "Ursula Baatz ",
        "title": "Achtsam durch die Krise ",
        "date": "2020-03-18",
        "description": "Die „Ökonomie der Aufmerksamkeit“ ist ein Motor der Industriegesellschaft. Aber in Krisensituationen erweist sich Aufmerksamkeit als zusätzlicher Stressfaktor. Das Konzept der Achtsamkeit kann hier helfen.",
        "categories": ["Gesellschaft"],
        "tags": [],
        "with": [
            "gen genährt wird. Und lebensbedrohlich ist es – jedenfalls statistisch gesehen, und da die Statistik nichts darüb",
            "n, verwechseln Achtsamkeit mit Aufmerksamkeit.",
            "Achtsamkeit zu üben, kann man im",
        ],
        "without": ["Im FURCHE-Navigator weiterlesen", "FURCHE-Newsletter", "itreisen und neue Perspektiven"],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.cicero.de/innenpolitik/corona-pandemie-es-kommt-auch-darauf-an-wie-die-menschen-sterben": {
        "file": "cicero.de.pandemie.html",
        "author": "MORITZ GATHMANN",
        "title": "„Es kommt auch darauf an, wie die Menschen sterben“",
        "date": "2020-04-21",
        "description": "Müssen Infizierte unbedingt ins Krankenhaus? Der Palliativmediziner Gian Domenico Borasio erklärt, warum viele Covid-Patienten im Pflegeheim bessere Überlebenschancen haben - und warum die Anzahl der Todesfälle bei der Frage, wie wir die Krise bewältigen, nicht das einzige Kriterium sein kann.",
        "categories": ["Innenpolitik"],
        "tags": ["Corona-Pandemie"],
        "with": [
            "Intensivbehandlung geht oder palliativ behandelt wird, ist ja die Patientenverfügung.",
            "Wurde eine unnötige Einweisung ins Krankenhaus verhindert?",
            "bei der Frage, wie wir die Krise bewältigen, nicht das einzige Kriterium sein kann",
        ],
        "without": ["Cicero Newsletter", "Moritz Gathmann leitet", "Sie sind leider nicht angemeldet"],
        "comments": [
            "-Krise hat man u.a. nämlich einen dafür wichtigen Aktivposten sozusagen ausgeschaltet i",
            "rachtend. Unsere Kultur hat vergessen, dass der Tod zum Lebe",
            "iger Artikel. Solche Gedanken und Konsequenzen, d",
        ],
        "license": "",
        "region": "DE",
    },
    "https://legrandcontinent.eu/fr/2020/03/02/francois-heran/": {
        "file": "legrandcontinent.eu.heran.html",
        "author": "Uriel Gadessaud",
        "title": "« Il y a, d’abord, le poids de la géographie ». Sur les migrations avec François Héran ",
        "date": "2020-03-02",
        "description": "Alors qu’Erdogan ouvre les frontières turques et que la Méditerranée est encore une fois la scène d&#039;images insupportables, nous publions une conversation avec François Héran, l&#039;un des principaux spécialistes des migrations en Europe, titulaire de la Chaire migrations et sociétés du Collège de France.",
        "categories": ["Entretiens"],
        "tags": ["Méditerranée"],
        "with": [
            "certes beaucoup de migrants, mais c’est un flux massif continu.",
            "il faut avoir déjà les ressources, savoir déjà",
            "la justice spatiale est un des objectifs de l’Union, alors Dublin n’est pas acceptable",
        ],
        "without": ["Pour approfondir", "concepts liés à l", "Coronavirus, un témoignage du front"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.bundespraesident.de/SharedDocs/Reden/DE/Johannes-Rau/Reden/2003/03/20030331_Rede2.html": {
        "file": "bundespraesident.de.20030331.html",
        "author": "Johannes Rau",
        "title": "Rede von Bundespräsident Johannes Rau beim Föderalismuskonvent der deutschen Landesparlamente",
        "date": "2003-03-31",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "m Juni 1948 unternahm ein Berater des amerikanischen Militärgouverneurs Clay eine Rundreise durc",
            " vielleicht am schönsten mit einem Kirchenlied des Grafen Zinzendorf sagen:",
            "994 errechnet, dass nur sechzehn von 120 Gesetzgebungsvorhaben gestaltende ",
        ],
        "without": ["Diese Seite", "© 2020 Bundespräsidialamt", "Lebenslauf"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://wiki.python.org/moin/BeginnersGuide/Download": {
        "file": "wiki.python.org.Download.html",
        "author": "MatsWichmann",
        "title": "Downloading Python",
        "date": "2019-11-10",
        "description": "",
        "categories": ["Beginners Guide"],
        "tags": [],
        "with": [
            "hey are available via the yellow download buttons on that page. ",
            "Before you start, you will need Python on your computer.",
            "general download page",
        ],
        "without": ["Unable to edit the page? See the FrontPage for instructions.", "Attachments", "Login"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.pcmag.com/news/next-gen-hamr-platters-promise-80tb-hard-drives": {
        "file": "pcmag.com.platters.html",
        "author": "Matthew Humphries",
        "title": "Next-Gen HAMR Platters Promise 80TB Hard Drives",
        "date": "2020-02-07",
        "description": "We&#039;re about to get 20 terabyte hard drives, but the path looks clear to scale up to 80TB.",
        "categories": ["Storage"],
        "tags": [],
        "with": [
            "but the path looks clear to scale up to 80TB.",
            "hat means an 80TB hard drive is theoretically possible.",
            "per square inch. Based on to",
        ],
        "without": [
            "nd a Masters in Computer Games Development from Abertay University.",
            "Read the latest from Matthew Humphries",
            "Honest, Objective Reviews",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.rutgers.edu/news/new-robot-does-superior-job-sampling-blood": {
        "file": "rutgers.edu.robot.html",
        "author": "Todd Bates",
        "title": "New Robot Does Superior Job Sampling Blood",
        "date": "2020-02-05",
        "description": "n the future, robots could take blood samples, benefiting patients and healthcare workers alike.",
        "categories": ["Research & Innovation"],
        "tags": [],
        "with": [
            "First clinical trial of an automated blood drawing and testing device",
            "nefiting patients and healthcare workers alike.",
            "from this study will be used to enhance artificial intelligence in the robot to improve its performance.",
        ],
        "without": ["You May Also Like", "University Operating Status", "ng. The university has move"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.acpjournals.org/doi/10.7326/M19-3075": {
        "file": "acpjournals.org.3075.html",
        "author": ["Michael L. Anderson, PhD", "Carlos Dobkin, PhD", "Devon Gorry, PhD"],
        "title": "The Effect of Influenza Vaccination for the Elderly on Hospitalization and Mortality",
        "date": "2020-04-07",
        "description": "",
        "categories": [],
        "tags": [
            "Pulmonary diseases",
            "Epidemiology",
            "Seasons",
            "Pneumonia",
            "Vaccines",
            "Research design",
            "Surveys",
            "Morbidity",
            "Information storage and retrieval",
            "Birth",
            "Medical services",
            "Elderly",
            "Observational studies",
            "Statistical data",
            "Hospitalizations",
            "Sexual identity",
            "General practitioners",
            "Immune response",
            "Death rates",
            "Age groups",
        ],
        "with": [
            "cination reduces hospitalizations and mortality among elderly persons. Acc",
            "ged 55 to 75 years residing in the study area during 2000 to 2014.",
            "Primary Funding Source:",
        ],
        "without": ["ACP Journals home", "Institutions / Libraries / Agencies", "2020 American College of"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://blog.mondediplo.net/turpitude-et-architecture": {
        "file": "blog.mondediplo.net.turpitude.html",
        "author": "Didier Roy",
        "title": "Turpitude et architecture",
        "date": "2018-06-21",
        "description": " L&#039;un des &#233;crivains sud-cor&#233;ens les plus c&#233;l&#232;bres, Hwang Sok-yong, est un homme heureux. Inscrit, avec beaucoup d&#039;autres intellectuels, sur une liste (...) ",
        "categories": ["Planète Asie"],
        "tags": ["Asie Censure", "Littérature", "Corée du Sud", "Corée du Nord"],
        "with": [
            "sation des rapports intercoréens, il voit à 75 ans le rapprochement se réaliser",
            "malgré tout l’amitié et l’entraide occupent une grande place",
            "hitecte de ressentir des moments de nostalgie en repensa",
        ],
        "without": [
            "arrête, on réfléchit",
            "des clefs du monde contemporain. Depuis le début du XXIe siècle, le",
            "engagent que leurs auteurs.",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.zdnet.de/88298335/facebook-wehrt-sich-gegen-maas-gesetz": {
        "file": "zdnet.de.facebook.html",
        "author": "Stefan Beiersmann ",
        "title": "Facebook wehrt sich gegen Maas-Gesetz",
        "date": "2017-05-29",
        "description": "Es bezeichnet den Entwurf des Netzwerkdurchsetzungsgesetzes als ungeeignet. Stattdessen sieht Facebook den Kampf gegen Hass-Postings und Fake News als öffentliche Aufgabe an. Es wehrt sich auch gegen einen deutschen Alleingang und fordert eine europäische Lösung.",
        "categories": ["Regulierung"],
        "tags": ["Facebook", "Politik", "Soziale Netze", "Zensur"],
        "with": [
            "esjustizminister Heiko Maas geäußert, per Gesetz „Compliance-Regeln für Soziale Netzwerke“ e",
            "acebook zusätzliche Kosten von 530 Millionen Euro pro Jahr zukommen, für „realistisch“.",
            "nste anbieten. Während beispielsweise die Leugnung des Holocaust hierzulande unter Str",
        ],
        "without": [
            "Whitepaper",
            "Bericht: Apple kündigt zur WWDC 13,3-Zoll-MacBook und 24-Zoll-iMac mit ARM-Prozessoren an",
            "erden Sie die Corona Warn-App der Bundesregierung verwenden?",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.infocomcgt.fr/caisse-de-solidarite-financiere/": {
        "file": "infocomcgt.fr.caisse.html",
        "author": "",
        "title": "Caisse de solidarité financière",
        "date": "",
        "description": "Faire un don : En ligneEnvoyer un chèque ou faire un virement    Site internet de la #CaisseDeGreve : caisse-solidarite.fr&hellip;",
        "categories": [],
        "tags": [],
        "with": ["ou tout autre régression sociale", "1 545 500 EUROS", "Reportage JT 13 heures de France 2"],  # 3 segments
        "without": [
            "On n’est pas de la chair à patron",
            "Votre adresse e-mail ne sera pas publiée",
            "Contactez vos représentants",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.ok-magazin.de/people/real-life/horror-fund-instagram-star-24-einbetoniert-62276.html": {
        "file": "ok-magazin.de.einbetoniert.html",
        "author": "Ulrike",
        "title": "Horror-Fund! Instagram-Star (†24) einbetoniert",
        "date": "2019-10-18",
        "description": "https://www.ok-magazin.de/sites/default/files/styles/facebook/public/media/gallery/2019/10/18/esmeralda-1.jpg?itok=ufNX8thk",
        "categories": ["Tod"],
        "tags": [],
        "with": [
            "Die Ermittler gehen davon aus, dass der drogensüchtige Mann",
            "das alles wäre nur ein Traum, es tut mir so leid.",
            "Kaum zu fassen, dass diese Story wirklich passiert ist:",
        ],  # 3 segments
        "without": ["TikTok-Star begeht", "Real Life", "Themen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.zdf.de/sport/us-sport-corona-100.html": {
        "file": "zdf.de.corona.html",
        "author": "Andreas Kürten",
        "title": "US-Sport in Zeiten von Corona",
        "date": "2020-04-04",
        "description": "US-Sport in Zeiten von Corona - ZDFmediathek",
        "categories": ["Sport"],
        "tags": [],
        "with": [
            "New York ist das Epizentrum der Corona-Pandemie",
            " Auch der Sport ist zum Stillstand",
            "Die Anteilnahme in den Top-Ligen ist groß. Wie es ",
        ],  # 3 segments
        "without": ["Video verfügbar bis 28.02.2021", "Auch interessant", "ZDF Unternehmen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.fluter.de/corona-big-data-suedkorea-vorbild-fuer-deutschland": {
        "file": "fluter.de.vorbild.html",
        "author": "Julia Lauter",
        "title": "„Es bricht eine andere Zeit der Datennutzung an“",
        "date": "2020-03-31",
        "description": "Mit Big Data Corona bekämpfen: zu schön, um wahr zu sein? Medienwissenschaftler Felix Stalder schätzt ein, ob Deutschland dem Beispiel Südkorea folgen soll",
        "categories": ["Corona"],
        "tags": ["Corona", "Datenschutz", "Internet", "Daten"],
        "with": [
            "Felix Stalder: Zu wissen, mit wem Corona-Patienten",
            "gleichzeitig Dutzende, vielleicht sogar Hunderte Nutzer eingewählt.",
            "möglich zu machen. In jedem Fall bricht eine ander",
        ],  # 3 segments
        "without": ["Titelbild:", "Auch interessant", "Dieser Text wurde veröffentlicht"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "CC-BY-NC-ND-4.0-DE",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://geschichtedergegenwart.ch/mit-foucault-die-pandemie-verstehen/": {
        "file": "geschichtedergegenwart.ch.foucault.html",
        "author": "Philipp Sarasin",
        "title": "Mit Foucault die Pandemie verstehen?",
        "date": "2020-03-25",
        "description": "Geschichte der Gegenwart",
        "categories": ["Geschichten der Gegenwart"],
        "tags": ["Biopolitik", "Corona", "Foucault", "Gesellschaft", "Gouvernementalität", "Infektion", "Lepra", "Pest"],
        "with": [
            "„Über­le­bens“ aller demo­kra­ti­schen Hinder­nisse und können endlich",
            "Daher sei das „Verhältnis zu sich selbst“, wie Foucault",
            "einge­führt, um das Auftau­chen neuer poli­ti­scher Ziele und Stra­te­gien in",
        ],  # 3 segments
        "without": [
            "Die Versu­chungen des Abso­lu­tismus.",
            "Sinn ohne Wort. Vom „Volks­thum“ und anderen „Thum­heiten“",
            "lehrt Geschichte der Neu­zeit",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.giga.de/downloads/google-chrome/tipps/google-chrome-exportieren-alle-daten-sichern-und-nichts-mehr-verlieren/": {
        "file": "giga.de.chrome.html",
        "author": "Marco Kratzenberg",
        "title": "Google Chrome exportieren und alles sichern",
        "date": "2017-12-01",
        "description": "Wenn ihr alle Daten und Einstellungen aus Google Chrome exportieren wollt, müsst ihr nicht auf Hilfsprogramme zurückgreifen. Der Browser bringt..",
        "categories": ["Software & Apps"],
        "tags": [],
        "with": [
            "Es gibt zwei Methoden, mit denen ihr Google Chrome",
            "Google Chrome speichert alle benutzerrelevanten Daten,",
            "funktioniert - in eingeschränktem Maße - natürlich auch auf",
        ],  # 3 segments
        "without": [
            "Für Links auf dieser Seite erhält GIGA",
            "oder blauer Unterstreichung gekennzeichnete. Mehr Infos.",
            "Alle Rechte vorbehalten.",
        ],  # 3 segments
        "comments": [
            "Und wie macht man das auf Andriod",
            "das Orwell recht behält und der Datenüberwachungskrake",
            "Deine so krass wertvollen Passwörter für Online Foren und",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.antary.de/2017/06/29/wireshark-besuchte-urls-anzeigen-http-und-https/": {
        "file": "antary.de.wireshark.html",
        "author": "Tobi",
        "title": "Wireshark: Besuchte URLs anzeigen (HTTP und HTTPS)",
        "date": "2017-06-29",
        "description": "",
        "categories": ["Internet", "Software & Apps", "Tutorials"],
        "tags": [],
        "with": [
            "Wireshark möglich ist, alle aufgerufenen",
            "Paketmitschnitt und eine aktuelle Version von Wireshark voraus. Beim",
            "angezeigt werden, was meiner Meinung nach komfortabler ist.",
        ],  # 3 segments
        "without": [
            "Mit der Nutzung dieses Formulars erklärst du dich mit der Speicherung",
            "Über ein Geschenk von meine",
            "mich über nachfolgende Kommentare per E-Mail.",
        ],  # 3 segments
        "comments": ["umindest einigermaßen dem Thema nähern :)", "Aufruf dafür aussehen muss."],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dalloz-actualite.fr/node/libre-cours-raoult-nazis-et-moi": {
        "file": "dalloz-actualite.fr.raoult.html",
        "author": "Matthieu Hy",
        "title": "Libre cours : Raoult, les nazis et moi",
        "date": "2020-05-07",
        "description": "Le contenu de ce champ sera maintenu privé et ne sera pas affiché publiquement.",
        "categories": ["Avocat"],
        "tags": [],
        "with": [
            "C’est la guerre. Et pourtant",
            "Vive le professeur Raoult !",
            "Que les magistrats sachent qu’ils peuvent com",
        ],  # 3 segments
        "without": ["Votre commentaire ", "otre adresse e-m", "otre no"],  # 3 segments
        "comments": ["En ce temps de confinement, Ceyss", "Le confinement chauffe les esprits"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://www.pocketpc.ch/windows-phone-7-allgemein/122760-microsoft-beginnt-auslieferung-vorbereitungsupdate-34.html": {
        "file": "pocketpc.ch.auslieferung.html",
        "author": "",
        "title": "Microsoft beginnt mit der Auslieferung des Vorbereitungsupdate!",
        "date": "2011-03-03",
        "description": "Soeben wurde auf dem Windows Phone Blog bekannt gegeben, dass Microsoft mit der auslieferung des Updates beginnt. Ihr solltet in den nächsten Stunden Automatisch per Pop-up darüber Informiert werden.",
        "categories": [],
        "tags": [],
        "with": [
            "as war noch nicht das Update, sondern nur",
            "s auf Gerät, Telefon oder Ha",
            "hat keine 5 Minuten gedauert, warum denn bei einigen",
        ],  # 3 segments
        "without": [
            "Gewinnspiel: Das neue Quizdue",
            "[Apple Pay] und eure Erfahrun",
            "Review: InLine BT-POCKET falt",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://strangemachines.io/articles/performant-python": {
        "file": "strangemachines.io.performant.html",
        "author": "Jacopo Cascioli",
        "title": "Performant Python",
        "date": "2019-12-03",
        "description": "A look at how to write performant Python code in simple ways and how much each improvement is effective.",
        "categories": ["articles"],
        "tags": [],
        "with": [
            "There are many ways to improve Python",
            "complicated, there are a number of ways ",
            "Map and filter are sometimes faster",
        ],  # 3 segments
        "without": ["Challenges", "hello@strangemachines.io", "06 December 2019"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://wordsmith.org/words/maudlin.html": {
        "file": "wordsmith.org.maudlin.html",
        "author": "Anu Garg",
        "title": "maudlin ",
        "date": "2009-04-07",
        "description": "",
        "categories": ["words"],
        "tags": [],
        "with": [
            "adjective: Overly sentimental",
            "derived after a town on the Sea ",
            "Jeannette Layne-Clark; Minister on Stage; Daily Nation ",
        ],  # 3 segments
        "without": [
            "spread the magic of words to readers everywhere",
            "“A word in the head is worth two in the book.”",
            "“A trawl through the site’s archive yields all kinds of delights.”",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://businessjargons.com/leadership-styles.html": {
        "file": "businessjargons.com.leadership.html",
        "author": "",
        "title": "Leadership Styles",
        "date": "2016-02-08",
        "description": "Definition: The Leadership Styles are the behavioral patterns that a leader adopt to influence the behavior of his followers, i.e. the way he gives directions to his subordinates and motivates them to",
        "categories": ["Business"],
        "tags": [],
        "with": [
            "the way he gives directions to his subordinates and ",
            "The leadership styles can either be classified on",
            "adopts to influence the behavior of his subordinates.",
        ],  # 3 segments
        "without": ["Effective Communication", "International Marketing", "Communication Process"],  # 3 segments
        "comments": [
            "well detailed article. More knowledge",
            "I haven’t come across a more succinct",
            "very informative I have learnt a lot",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.mesopinions.com/petition/art-culture/mutilation-choeur-radio-france-unique-choeur/76519": {
        "file": "mesopinions.com.mutilation.html",
        "author": "Les Membres du Choeur de Radio France",
        "title": "Non à la mutilation du choeur de Radio France, Unique Choeur professionnel à vocation Symphonique en France",
        "date": "",
        "description": "Arts et culture - Signez la pétition : Non à la mutilation du choeur de Radio France, Unique Choeur professionnel à vocation Symphonique en France",
        "categories": [],
        "tags": [],
        "with": [
            "National de France et du Philharmonique de Radio France.",
            "bien des promesses non tenues par des directions successives",
            "vide de toute ambition artistique et culturelle.",
        ],  # 3 segments
        "without": ["Notre communauté", "Espace presse", "Réussir votre mobilisation"],  # 3 segments
        "comments": [
            "un fleuron du patrimoine artistique et culturel français",
            "L'art c'est les hommes...humains !",
            "Arrêtez la casse du service public !",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.linkedin.com/pulse/ich-war-am-wochenende-auf-einer-hochzeit-im-wendland-inga-hoeltmann": {
        "file": "linkedin.com.hoeltmann.html",
        "author": "Inga Hoeltmann",
        "title": "Ich war am Wochenende auf einer Hochzeit im Wendland.",
        "date": "2019-08-19",
        "description": "Das Wendland ist eine schöne, aber sehr ländliche Region in einem (nord)östlichen Zipfel von Niedersachsen, der nach Sachsen-Anhalt reinragt, etwa eine Zugstunde von Hamburg. Ich bin von Berlin mit dem Zug durch Brandenburg nach Salzwedel in Sachsen-Anhalt gefahren und habe mich dort abholen lassen.",
        "categories": [],
        "tags": ["NeueArbeit", "Digitalisierung "],
        "with": [
            "Das Wendland ist eine schöne, aber sehr ländliche",
            "hinnehmen als sei es nicht zu ändern. Beschämend.",
            "Konzepte abseits der urbanen Räume in",
        ],  # 3 segments
        "without": ["Einstellungen für Nichtmitglieder", "Nutzervereinbarung", "Markenrichtlinine"],  # 3 segments
        "comments": [
            "Meine Antworten sin, laut LinkedIn,",
            "sondern häufig an den fehlenden Baggern.",
            "Die gibt es bereits zuhauf ohne gute Connectivity.",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.wolfgangmichal.de/2017/06/07/publizistische-sorgfaltspflicht-statt-netzwerkdurchsetzungsgesetz/": {
        "file": "wolfgangmichal.de.sorgfaltspflicht.html",
        "author": "Wolfgang Michal",
        "title": "Publizistische Sorgfaltspflicht statt Netzwerkdurchsetzungsgesetz",
        "date": "2017-06-07",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "Die Repräsentanten der Republik sind nervös. ",
            "verkaufen, muss jedes Unternehmen in die Bredouille bringen.",
            "EU-Urheberrechts-Richtlinie sogar bindend vorgeschrieben werden.",
        ],  # 3 segments
        "without": [
            "verteidigt sie ihre Linie gegen die Zumutungen der Moderne.",
            "verhindert, sondern zu Geld gemacht werden.",
            "den Rechtspopulisten mehr nützen als schaden.",
        ],  # 3 segments
        "comments": [
            "Sehr schön zusammengefasst bzw. heraus gearbeitet.",
            "Soziodemographische Untersuchungen?",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.zooroyal.de/trixie-natura-kleintierstall-mit-freilaufgehege": {
        "file": "zooroyal.de.trixie.html",
        "author": "",
        "title": "Trixie Natura Kleintierstall mit Freilaufgehege",
        "date": "",
        "description": "Kaninchenstall mit integriertem Freigehege im Unterbau. Aus stabilem Kiefernholz gefertigt mit herausziehbarem, kunststoffbeschichtetem Boden.",
        "categories": ["kleintier"],
        "tags": [],
        "with": [
            "stabilem Kiefernholz gefertigt mit herausziehbarem, kunststoffbeschichtetem Boden.",
            "Der Natura Stall lässt sich von oben sowie von vorne öffnen ",
            "verschließbare Bodenluke mit Kunststoffbeschichtung",
        ],  # 3 segments
        "without": [
            "Kleintierheim",
            "dass ZooRoyal mir per E-Mail an mich gerichtete Werbung",
            "Trixie Kleintierfutter",
        ],  # 3 segments
        "comments": [
            "Danke dem Team von zoo royale.",
            "und preisleistungsverhaltniss ist auch o.k",
            "Unsere Meerschweinchen fühlen sich sehr wohl darin",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.lopinion.fr/edition/economie/glyphosate-radiographie-d-intoxication-collective-186859": {
        "file": "lopinion.fr.glyphosate.html",
        "author": "Emmanuelle Ducros",
        "title": "Glyphosate: radiographie d’une intoxication collective",
        "date": "2019-05-15",
        "description": "A chaque civilisation, ses d\u00e9mons. La n\u00f4tre a le sien&thinsp;: le glyphosate. Comment cet herbicide en est-il venu \u00e0 incarner le mal aux yeux de...",
        "categories": ["Economie"],
        "tags": [],
        "with": [
            "La firme Bayer, propriétaire",
            "Jackpot pour Monsanto qui vend à la fois les semences",
            "puisque le champ des recherches est infini...",
        ],  # 3 segments
        "without": ["Mentions légales", "Conditions générales de vente", "Charte des commentaires"],  # 3 segments
        "comments": [
            "Sauf sur une forme rarissime de lymphome.",
            "de prouver la nocivité, autre que végétale",
            "suffisant. Notre société est redevenue religieuse.",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://www.tagesanzeiger.ch/wie-umweltzerstoerung-neue-epidemien-beguenstigt-633956751547": {
        "file": "tagesanzeiger.ch.umweltzerstoerung.html",
        "author": "Christoph von Eichhorn",
        "title": "Wie Umweltzerstörung neue Epidemien begünstigt",
        "date": "2020-04-11",
        "description": "Sars-CoV-2 stammt von einem Tier. Allein in Fledermäusen und Flughunden existieren mehr als 3000 Coronaviren. Ist ihr Lebensraum zerstört, rücken sie näher an den Menschen - und eine Übertragung wird wahrscheinlicher.",
        "categories": ["Wissen"],
        "tags": [],
        "with": [
            "Dichter Rauch hing im Herbst des Jahres 1997",
            "es kann auch von Mensch zu Mensch weitergegeben werden.",
            "Im Wesentlichen geht es da aber um Fragen der Wirtschaft und",
        ],  # 3 segments
        "without": ["Aktualisiert:", "03.04.2020", "All Rights Reserved"],  # 3 segments
        "comments": [
            "Jetzt werden wir den Preis bezahlen für stetigen Wachstum",
            "Verhütungsmitteln (rein technische Massnahmen) mit ",
            "Was nicht unbedingt schlecht ist - sonst würde die Menschheit wohl",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.freitag.de/autoren/benjamin-immanuel-hoff/heute-schon-an-morgen-denken": {
        "file": "freitag.de.morgen.html",
        "author": "Benjamin-Immanuel Hoff",
        "title": "Heute schon an morgen denken ",
        "date": "2020-04-17",
        "description": "Die Thüringer Kultur kommt schrittweise aus der Corona-Zwangspause. Notwendig sind wirksame Hilfen, neues Denken und verlässliche Politik, die aufbaut statt zu kürzen.",
        "categories": [],
        "tags": [
            "solo-selbständige",
            "künstlersozialkasse",
            "theater",
            "freie szene",
            "krise",
            "kulturwirtschaft",
            "gewerkschaft",
            "archive",
            "medien",
            "bibliotheken",
            "museen",
            "rundfunkbeitrag",
            "kreativwirtschaft",
            "städte und gemeinden",
            "orchester",
            "kunst",
            "kultur",
        ],
        "with": [
            "Kommunen, die Länder und der Bund einschneidende",
            "Durch die Beschränkungen des öffentlichen Lebens wurde erreicht",
            "Kultur mit dem gemeinwirtschaftlichen Gedanken des Genossenschaftswesens verbinden",
        ],  # 3 segments
        "without": [
            "© der Freitag Mediengesellschaft mbH & Co. KG",
            "Beitrag gibt die Meinung des Autors wieder, nicht notwendigerweise die der Redaktion des Freitag.",
            "Beitrag handelt es sich um ein Blog aus der Freitag-Community",
        ],  # 3 segments
        "comments": ["Nun ... erst gestern wurde dem Zuschauer "],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.stylegart.de/naturkosmetik-doch-gesuender/": {
        "file": "stylegart.de.naturkosmetik.html",
        "author": "Ramona",
        "title": "Naturkosmetik – die gesündere Alternative?",
        "date": "2019-04-10",
        "description": "Naturkosmetik- Auflistung Pro und Kontra- was verbirgt sich wirklich hinter den Produkten und welche Inhaltsstoffe sind hier nicht vorhanden!",
        "categories": ["Fashion Trends 2019"],
        "tags": ["Kosmetika", "Natur", "Naturkosmetik", "Produkktttest"],
        "with": [
            "Wer meine Instastorys fleißig verfolgt, der weiß, dass ich",
            "Tuben und Tiegel mit natürlichen Verpackungen, meist mit Blütenprints umrankt versprechen ",
            "Dr. Scheller und Lavera, die natürliche Kosmetika zu fairen Preisen anbieten!",
        ],  # 3 segments
        "without": ["Was dich erwartet", "Datenschutzerklärung", "Vorher-Nachher"],  # 3 segments
        "comments": [
            "Ich verwende sehr viel Naturkosmetik, denn wir haben",
            "Vielen Dank für deinen Kommentar… ja. das sagt meine Mutter auch immer zu mir",
            "Hey, ich würde nie sagen, dass Natur- oder konventionelle Kosmetik",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "http://fouryears.eu/2019/10/21/interning-of-small-integers-in-python/": {
        "file": "fouryears.eu.interning.html",
        "author": "Konstantin",
        "title": "Interning of Small Integers in Python",
        "date": "2019-10-21",
        "description": "Preparing the consequences",
        "categories": [],
        "tags": ["Computer science", "Fun", "Hacks", "Programming", "Python"],
        "with": [
            "Note that depending on the version of Python the value of the integer",
            "lovely example, illustrating the way Python",
            "(addr, ctypes.",
        ],  # 3 segments
        "without": [
            'Best western clearfield pa on Skype "removed" messages',
            "6 Regularization Techniques for Deep Learning",
            "Konstantin on ROC Area-Under-the-Curve Explained",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "EU",  # if obvious: DE, CH, AT
    },
    "https://www.axios.com/newsletters/axios-future-7120a6cf-cf67-4e01-9f15-f73f114e8d27.html": {
        "file": "axios.com.future.html",
        "author": "Bryan Walsh",
        "title": "Axios Future",
        "date": "2019-01-18",
        "description": "",
        "categories": ["newsletters"],
        "tags": [],
        "with": [
            "A new breed of intelligent video surveillance is being installed",
            'good kid, m.A.A.d city," the 5th song starts 19 ',
            "to school districts and universities, in addition to banks",
        ],  # 3 segments
        "without": ["Axios newsletters", "Online tracking choices", "Axios podcasts"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.nytimes.com/2020/08/16/business/california-blackouts.html": {
        "file": "nytimes.com.blackouts.html",
        "author": "Ivan Penn",
        "title": "Rolling Blackouts in California Have Power Experts Stumped",
        "date": "2020-08-16",
        "description": "Managers of the electric system argue that a lack of power prompted the decision to enact blackouts, though demand this weekend fell short of the state’s peak years.",
        "categories": ["Business"],
        "tags": [],
        "with": [
            "As temperatures began to rise in California on",
            "“If there’s really a problem and not just the ISO",
            "In particular, California ISO said two natural gas power",
        ],  # 3 segments
        "without": [
            "Her Husband Abused Her. But Getting a Divorce Was",
            "Chris Rock Tried to Warn Us",
            "Opinion: Which Party Represents the Racial Future?",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://californiaglobe.com/section-2/amazon-liable-for-defective-third-party-products-rules-ca-appelate-court/": {
        "file": "californiaglobe.com.amazon.html",
        "author": "Evan Symon",
        "title": "Amazon Liable for Defective Third-Party Products Rules CA Appellate Court",
        "date": "2020-08-14",
        "description": "On Thursday, California’s 4th District Court of Appeal in Santa Ana found that Amazon.com can now be held liable for injury for selling defective products",
        "categories": ["COM"],
        "tags": [
            "Amazon",
            "Amazon Bolger case",
            "Amazon liability lawsuit",
            "Amazon retailer",
            "Amazon service provider",
            "Amazon third party seller liability lawsuit",
            "Amazon third-party sellers",
            "Amazon.com",
            "Angela Bolger",
            "California Amazon liability appeal",
            "California superior court amazon ruling, California’s 4th District Court of Appeal",
            "Lenoge Technology",
            "Superior Court",
        ],
        "with": [
            "The ruling has grouped Amazon with other retailers who",
            "provided by Lenoge for its product listing.",
            "case to a higher court in the near future.",
        ],  # 3 segments
        "without": ["Get a weekly summary of California Globe stories:", "Follow Us", "Leave a Reply"],  # 3 segments
        "comments": [
            "Nail them to the wall. amazon is bad",
            "together like Ebay, but also offer to",
            "to groups that are determined to tear down society.",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.sciencesetavenir.fr/sante/covid-19-et-infox-comment-une-rumeur-devient-realite_147359": {
        "file": "sciencesetavenir.fr.rumeur.html",
        "author": "Nicolas Gutierrez C.",
        "title": "Covid-19 et infox : comment une rumeur devient réalité",
        "date": "2020-09-14",
        "description": "oici ce que l’on peut apprendre du voyage de l’une d’entre elles : la dangerosité de l’ibuprofène chez les patients de Covid-19.",
        "categories": ["Santé"],
        "tags": ["COVID-19", "Coronavirus", "Ibuprofène", "Fake news", "Coronavirus en France", "Espagne"],
        "with": [
            "Aussi contagieuses que le virus ?",
            "contagieux (et potentiellement dangereux) que le SARS-CoV-2.",
            "popularité du sujet a explosé suite à ce",
        ],  # 3 segments
        "without": ["L’essentiel santé", "A découvrir sur Challenges", "En images"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://www.siegfried-marcus-berufsschule.at/kraftfahrzeugtechnik/lehrberufe-kft-2/": {
        "file": "siegfried-marcus-berufsschule.at.kft.html",
        "author": "",
        "title": "Lehrberufe KFT",
        "date": "",
        "description": "Hier finden Sie unsere Lehrberufe zum Lehrgang Kraftfahrzeugtechnik (KFT) - Siegfried Marcus Berufsschule",
        "categories": ["kraftfahrzeugtechnik"],
        "tags": [],
        "with": ["Lehrstoffinhalte", "3. Klasse", "Module"],  # 3 segments
        "without": [
            "Direktor: OSR Dipl.-Päd. Markus Fuchs",
            "Verein der Freunde für berufsbegleitende Aus- und ",
            "Obmann: OSR Markus Fuchs",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.minusl.de/produkt_kategorien/joghurt/": {
        "file": "minusl.de.joghurt.html",
        "author": "",
        "title": "Unsere MinusL Joghurts",
        "date": "",
        "description": "Sie lieben Joghurt mit frischen Früchten, einen leckeren Fruchtjoghurt oder Joghurt nach griechischer Art? Dann entdecken Sie unsere Joghurtvielfalt!",
        "categories": [],
        "tags": [],
        "with": [
            "wohl, denn MinusL bringt Genuss in mein Leben.",
            "generell die Zutatenliste einer Verpackung beachten. Allergene Zutaten ",
            "Sie lieben Joghurt mit frischen Früchten un",
        ],  # 3 segments
        "without": ["Senden", "ZURÜCK", "MinusL Athentikos"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://sass-ag.de": {
        "file": "sass-ag.de.index.html",
        "author": "",
        "title": "Drucker und Druckausgabe-Lösungen vom Experten!",
        "date": "",
        "description": "Drucker, Etiketten, TTF-Folien, Auto-ID, Zubehör &amp; mehr vom Experten ✓Top Service ✓große Auswahl ✓langjährige Erfahrung ▶ Jetzt anfragen!",
        "categories": [],
        "tags": [],
        "with": [
            "Wir beraten herstellerunabhängig und planen immer objektiv",
            "Kaufen Sie bei uns preiswerte Etiketten in Ihrem",
            "Wir bieten professionelle Drucksysteme für alle Anwendungsbereiche; ganz",
        ],  # 3 segments
        "without": ["Produkte & Leistungen", "Zentrale Gilching", "Störungen:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20130217080612/http://tv-orange.de/2012/08/future-of-hope-island-befreit-sich-von-den-bankstern-der-film/": {
        "file": "archive.org.tv-orange.de.future.html",
        "author": "oradmin",
        "title": "FUTURE of HOPE – Island befreit sich von den Bankstern – der Film",
        "date": "2012-08-02",
        "description": "ISLAND befreit sich von der Macht der Finanzoligarchie und geht seinen eigenen Weg. Dieser Film wird bislang von den Kontinental-Europäischen Medien so gu...",
        "categories": [],
        "tags": [
            "Banken",
            "Bankster",
            "Bilderberger",
            "demokratie",
            "direkte Demokratie",
            "Eurokrise",
            "Fianzoligarchie",
            "finanzadel",
            "Finanzkrise",
            "Free Iceland",
            "FUTUREofHOPE",
            "Island",
            "Selbstbestimmt",
            "Volksentscheid",
        ],
        "with": [
            "Dieser Film wird bislang von den Kontinental-Europäischen Medien",
            "Ein Beispiel von Selbstzensur, symptomatisch für die Haltung gefälliger",
            "Außerdem verbreitet sich über Facebook die Information über",
        ],  # 3 segments
        "without": [
            "Hiesige Medien schwören die Bevölkerung auf Gedeih",
            "In den von den Banken verursachten Immobilienblasen und unsauberen",
            "Wir haben Gutwettermacher, Medienmacher, Meinungsmacher, Schlechtwettermacher, Schuhmacher",
        ],  # 3 segments
        "comments": ["Zum Trailer des Filmes geht es hier"],  # 0 or 3 segments
        "license": "DE",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20120216182711/http://www.stol.it/Artikel/Politik-im-Ueberblick/Politik/Verfassungsgericht-Berlusconis-Sex-Prozess-geht-weiter": {
        "file": "archive.org.stol.it.berlusconi.html",
        "author": "APA/AP",
        "title": "Verfassungsgericht: Berlusconis Sex-Prozess geht weiter",
        "date": "2012-02-14",
        "description": "taeglich aktuelle Suedtirol-Nachrichten aus Chronik, Politik, Sport, Wirtschaft, Kultur, Events. Lokale Wetter- und Service-Meldungen sowie Dolomiten-Online.",
        "categories": ["Politik"],
        "tags": [],
        "with": [
            "Das Verfassungsgericht in Rom verwarf am Dienstag einen Antrag",
            "Das Argument hatten die Mailänder Staatsanwälte „lächerlich“ genannt.",
            "Das laufende Verfahren gegen den im November als",
        ],  # 3 segments
        "without": ["IT 00853870210", "Hier können Sie den Artikel bewerten", "On-Tour Fotos"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://blog.leichtathletik-ostalbkreis.de/2007/05/20/ergebnisse-rm-schuelerinnen-a-aalen-unterkochen-1952007/": {
        "file": "leichtathletik-ostalbkreis.de.1952007.html",
        "author": "Marc Scheloske",
        "title": "Ergebnisse: RM Schülerinnen A, Aalen-Unterkochen, 19.5.2007",
        "date": "2007-05-20",
        "description": "",
        "categories": [],
        "tags": [],
        "with": ["1. und Regionalmeister 2007", "Schlumberger, Lea 1993;", "LG Staufen"],  # 3 segments
        "without": ["LA-Kreis Ulm/Alb-Donau", "LA-Kreis Göppingen", "LAC Essingen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://next2games.de/previews,id1085,0,anno_1800_beta.html": {
        "file": "next2games.de.anno.html",
        "author": "Lars",
        "title": "Anno 1800 Beta ",
        "date": "",
        "description": "Mit Anno 1800 veröffentlichen Blue Byte und Ubisoft im April den mittlerweile siebten (Haupt-)Ableger der beliebten Aufbaustrategie-Reihe. Im Zuge des ...",
        "categories": [],
        "tags": [],
        "with": [
            "zu entdecken, was Anno 1800 noch in petto hält.",
            "Neben dem Startgebiet in einer klimatisch eher gemäßigten",
            "Wie in jedem Titel der mittlerweile über 20 Jahre",
        ],  # 3 segments
        "without": ["n2g media network", "CMS: Apexx by Stylemotion", "Diese Website nutzt Cookies"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "http://www.exlibris-deg.de/2019/10/24/balsamo-stella-guido/": {
        "file": "exlibris-deg.de.balsamo.html",
        "author": "",
        "title": "Balsamo Stella, Guido (I)",
        "date": "",
        "description": "Werkliste Guido Balsamo Stella",
        "categories": [],
        "tags": [],
        "with": [
            "M. Akt mit Axt einen Baum fällend; Rem",
            "Adler nach Klippe, nach links blickend, Schooner im",
            "Exlibrissammlung PALMIRANI, Remo: Guido Balsamo Stella",
        ],  # 3 segments
        "without": ["Winkler, Eduard", "Rechtliches", "German"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://foren.myoos.de/viewtopic.php?f=4&t=167&sid=58428beaa14598c2e02d93ad5c773e4d": {
        "file": "foren.myoos.de.html",
        "author": "r23",
        "title": "Was ist Freie Software",
        "date": "2009-01-21",
        "description": "Was ist Freie Software und warum ist sie wichtig? von Georg C. F. Greve Freie Software ist Software, die ohne Ansicht der Person vier Freiheiten garantiert: Die Freiheit der unbegrenzten Nutzung zu jedem Zweck, die Freiheit des Studiums und der Modif..",
        "categories": [],
        "tags": [],
        "with": [
            "Freie Software ist Software, die ohne Ansicht der Person",
            "http://www.gnu.org/philosophy/free-sw.de.html",
            "Software (OSS) ein und entwickeln einen Praxisleitfaden.",
        ],  # 3 segments
        "without": ["Forum Software", "Alle Zeiten sind UTC+02:00", "Mitglieder in diesem Forum:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "http://www.mueritzurlauber.de/blockhaus-typ-3/": {
        "file": "mueritzurlauber.de.blockhaus.html",
        "author": "",
        "title": "Blockhaus 3",
        "date": "",
        "description": "Günstiges Blockhaus in Ludorf an der Müritz für bis zu 6 Personen",
        "categories": [],
        "tags": [],
        "with": [
            "Das helle und liebevoll eingerichtete Blockhaus 1 hat",
            "Buchung ab 3 Nächte oder nach Absprache.",
            "über die freien Termine oder nehmen einfach Kontakt zu uns auf.",
        ],  # 3 segments
        "without": ["info@mueritzurlauber.de", "039931 51438", "Datenschutzerklärung"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "http://harddecor.at/work/denkmaler-neuem-licht/": {
        "file": "harddecor.at.denkmaler.html",
        "author": "",
        "title": "Denkmäler in neuem Licht.",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "CONDITIONING. of Atmospheres in Architecture",
            "Denkmalpflegerinnen, Politikerinnen und der interessierten Öffentlichkeit fördern.",
            "Thema Planen und Bauen in historisch wertvoller Umgebung",
        ],  # 3 segments
        "without": ["Best of 2016.", "Gegen Leerstand und Wertminderung.", "Mission Statement"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20130307194448/the-pain.net/2008/05/silkroad-roc-mountain-quests-und-npcs.html": {
        "file": "archive.org.the-pain.net.silkroad.html",
        "author": "ThE_PaiN",
        "title": "Silkroad Roc Mountain Quests und NPC’s",
        "date": "2008-05-26",
        "description": "Hier findet ihr alle Informationen zu den Quests des Roc Mountain in Silkroad Online. Selbstverständlich ist auch eine NPC Map vorhanden!",
        "categories": ["Guides", "Silkroad", "Tipps & Tricks", "Tutorials"],
        "tags": ["infos", "legend 3", "Silkroad"],
        "with": [
            "Ich wurde von vielen Leuten darum gebeten zum neuen",
            "man kann ja nicht alles wissen",
            "Bringe eine Nachricht über den vermissten Sohn zu",
        ],  # 3 segments
        "without": [
            "Silkroad Online und alle damit in Verbindung stehenden Logos",
            "2007 - 2013",
            "Alle anderen Warenzeichen oder",
        ],  # 3 segments
        "comments": [
            "Servus ich wollte dich bitten ob ich diesen",
            "gegeben, aber bei der vorraussetzung von Rahid",
            "joymax, weil es nicht deine sachen sind !",
        ],  # 0 or 3 segments
        "license": "CC BY-SA 3.0 DE",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://mywakenews.wordpress.com/2016/07/09/nwo-psyop-unitedwestrike-radio-marathon/": {
        "file": "mywakenews.wordpress.com.psyop.html",
        "author": "mywakenews",
        "title": "NWO – PSYOP UNITEDWESTRIKE Radio-Marathon",
        "date": "2016-06-09",
        "description": "Abb.: Collage aus Internetbild und Wake News Die Aufzeichnung dieser Veranstaltung als Video: Den meisten Menschen auf dieser Erde ist nicht bewusst, dass wir in einer grossen Simulation leben, gen…",
        "categories": ["Uncategorized"],
        "tags": [
            "Abzocke",
            "Bankster",
            "Bürgerkrieg",
            "Bilderberger",
            "Dallas",
            "Detlev",
            "Deutschland",
            "DIMs",
            "EU-Faschismus",
            "EURO-CRASH",
            "falsche Flagge Terror",
            "Freiheit",
            "Geheimgesellschaften",
            "Globalisten",
            "Grossfinanz",
            "Illuminati",
            "International Strike",
            "Internationaler Streik",
            "Korruption",
            "Matrix",
            "Menschenrechte",
            "Neue Welt Ordnung",
            "NWO",
            "Obama",
            "PSYOP",
            "Regierung",
            "Schweiz",
            "Terror",
            "Tyrannei",
            "unitedwestrike",
            "USA",
            "Wake News Radio",
            "Wake News TV",
            "Weltelite",
            "Weltkrieg III",
            "ziviles Ungehorsam",
        ],
        "with": [
            "diesen Bastarden diese Worte einvernehmlicher Verkehr in den Mund???",
            "Kritische Betrachter haben bereits sehr viele Indizien zusammengetragen",
            "und unsere Wahrnehmung gefangen gehalten, manipuliert und gesteuert",
        ],  # 3 segments
        "without": [
            "For all who want to wake up!",
            "Erstelle eine kostenlose Website oder Blog – auf WordPress.com",
            "Meine persönlichen Informationen nicht verkaufen",
        ],  # 3 segments
        "comments": ["Hat dies auf meinfreundhawey.com rebloggt."],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://uniqz.de/produkte/katzendecke-zweilagig-mit-namen-und-main-coon/": {
        "file": "uniqz.de.katzendecke.html",
        "author": "Petra Ruland",
        "title": "Katzendecke, zweilagig mit Namen und Main Coon",
        "date": "",
        "description": "Mit Namen bestickte Geschenkideen zur Taufe, Geburt, Hochzeit, Abitur | Ringkissen, Babykissen, Babydecken, Hundedecken, fotorealistisch gestickte Rassehunde,",
        "categories": [],
        "tags": [],
        "with": [
            "Lieferzeit: 15 - 21 Tag(e)",
            "Hochwertige Hunde- oder Katzendecke in besonders kuscheliger",
            "Main Coon-Stickerei",
        ],  # 3 segments
        "without": ["Das Kleingedruckte", "Informationen", "Copyright / Rechte"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.oekonomenstimme.org/artikel/2015/01/eine-realistische-interpretation-des-keynes-hicks-multiplikators/": {
        "file": "oekonomenstimme.org.keynes.html",
        "author": "Georg Quaas",
        "title": "Eine realistische Interpretation des Keynes-Hicks-Multiplikators",
        "date": "2015-01-21",
        "description": "",
        "categories": [],
        "tags": ["Multiplikator", "Selbstfinanzierung"],
        "with": [
            "In seinem Beitrag von 5. Januar 2015 erörtert Wolfgang",
            "Wirtschaftsdienst, 92. Jahrgang, Heft 10, Oktober 2012",
            "Erfasst werden. Dabei steht T für den technologischen Fortschritt",
        ],  # 3 segments
        "without": [
            "Die paradigmatische Struktur der Makroökonomik",
            "um Kommentare zu schreiben",
            "Faktor Arbeit im Sinkflug",
        ],  # 3 segments
        "comments": [
            "Sie fliesst nur in die Taschen der Haushalte, die damit nichts anzufangen wissen.",
            "bitte darum, die anderen Themen woanders, beispielsweise in einem eigenen",
            "Multiplikators – aber der Theorie, die sich darum herumrankt, aufzudecken. ",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://leukefeld-handball.de/dago-leukefeld-wird-botschafter-des-sports-der-ifzw-impulsstiftung/": {
        "file": "leukefeld-handball.de.leukefeld.html",
        "author": "",
        "title": "Dago Leukefeld wird „Botschafter des Sports“ der ifzw impulsstiftung",
        "date": "",
        "description": "Die ifzw impulsstiftung und Dago Leukefeld besiegeln ihre gute Zusammenarbeit und richten sich für die Zukunft aus: Dago Leukefeld wird „Botschafter des Sports“ der ifzw impulsstiftung. 2012 hat sich die ifzw impulsstiftung zur Unterstützung im Bereich Sport den ehemaligen Frauen National? und langjähriger Bundesligatrainer, Dago Leukefeld, nach Zwickau geholt. Als einer der besten Trainer Deutschlands,Weiterlesen",
        "categories": [],
        "tags": [],
        "with": [
            "Die ifzw impulsstiftung und Dago Leukefeld besiegeln ihre gute",
            "mit Ihm und auf spannende Projekte im Vereinssport“, so Mechthild Aßmann.",
            "in die beteiligten Vereine beigetreten sind. Für uns ein tolles Ergebnis.",
        ],  # 3 segments
        "without": ["© 2017 Dago Leukefeld Handball", "Lieferzeit: 9-12 Tage", "Hier geht es zu den"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.propellets.at/soziale-energie": {
        "file": "propellets.at.energie.html",
        "author": "",
        "title": "Soziale Energie",
        "date": "",
        "description": "Besonders f&uuml;r Haushalte mit geringem Einkommen stellen steigende Energiekosten ein gro&szlig;es Problem dar. G&uuml;nstige und regionale Brennstoffe k&ouml;nnen im Kampf gegen Energiearmut helfen.",
        "categories": [],
        "tags": [],
        "with": [
            "Besonders für Haushalte mit geringem Einkommen stellen steigende",
            "Ziel der vorliegenden Studie war es, zu klären ob",
            "hohen Anfangsinvestition von rund 2700 € schwer erschwinglich.",
        ],  # 3 segments
        "without": ["Newsletter", "teilen", "Alles über den Verein"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://chabermu.wordpress.com/2015/09/02/windows-expertenwissen-per-update-spioniert-microsoft-nun-auch-windows-7-8-und-8-1-aus-microsoft-privacy-windows10-chabermu/": {
        "file": "chabermu.wordpress.com.expertenwissen.html",
        "author": "C.Habermueller",
        "title": "[Windows Expertenwissen] Per Update spioniert Microsoft nun auch Windows 7, 8 und 8.1 aus // #Microsoft #Privacy #Windows10 @chabermu",
        "date": "2015-09-02",
        "description": "Die Sammelwut der Benutzerdaten von Windows 10 reicht Microsoft (Börsenwert an Nasdaq: 334,48 Milliarden US-Dollar, Stand: 1. Sep 2015) immer noch nicht – Nun hat es der Softwarekonzern auch auf di…",
        "categories": [],
        "tags": ["Microsoft", "Privacy", "Windows10", "@chabermu"],
        "with": [
            "Nun hat es der Softwarekonzern auch auf die Nutzerdaten",
            "Klicken Sie die betroffenen, optionalen Windows-Updates",
            "Wann jedoch Microsoft diese Abhilfe gegen seine Abhör-Updates blockiert",
        ],  # 3 segments
        "without": ["© since 2010", "News vom Computerarchiv München", "Gib deine E-Mail-Adresse ein"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20110106023242/http://dzs-clan.de/index.php?site=news_comments&newsID=111": {
        "file": "archive.org.dzs-clan.de.html",
        "author": "Bo2man",
        "title": "Die Events der letzten Zeit",
        "date": "2010-12-29",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "In dieser News möchten wir euch über das Geschehen",
            "Diese Nachrichten könnt ihr auch auf unserer Homepage in unserer Twitter-Box lesen.",
            "Aller Voraussicht nach wird dieses auf der kommenden",
        ],  # 3 segments
        "without": [
            "Hi, ihr habt das falsche Statment von mir",
            "sein um Kommentare zu schreiben!",
            "© 2010 by dzs",
        ],  # 3 segments
        "comments": ["ich werde wohl auch auf die Mega Lan kommen"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "http://sibenlab.blogspot.com/2018/06/sibenlab-privacy-policy.html": {
        "file": "sibenlab.blogspot.com.privacy.html",
        "author": "Unknown",
        "title": "SibenLab privacy policy ",
        "date": "2018-06-05",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "This privacy policy has been compiled to",
            "If at any time you would like to",
            "visiting the Google Ad and Content Network privacy",
        ],  # 3 segments
        "without": ["Thème Simple. Fourni par", "Inscription à", "Publier un commentaire"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://hellogiggles.com/beauty/dead-skin-cells-build-up/": {
        "file": "hellogiggles.com.skin.html",
        "author": "Jessica DeFino ",
        "title": "Wait, are dead skin cells actually a good thing?",
        "date": "2020-03-12",
        "description": "Put down the exfoliating acid. According to dermatologists, dead skin cells actually do *so* much more than we give them credit for.",
        "categories": ["Beauty"],
        "tags": [],
        "with": [
            "Admit it: Ever since the first rough, grainy glob",
            "exfoliating acids, you kind of owe them an apology.",
            "Desquamation can only take place when the skin is functioning",
        ],  # 3 segments
        "without": [
            "adhere to in the morning and at night.",
            "two makeup artists to get their top tips on how to extend",
            "spots caused by melasma, sun damage, or pigmentation",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://link.springer.com/article/10.1007/s11926-017-0626-z": {
        "file": "link.springer.com.1007.html",
        "author": "Marwan H. Adwan",
        "title": "Drug Reaction with Eosinophilia and Systemic Symptoms (DRESS) Syndrome and the Rheumatologist",
        "date": "2017-01-30",
        "description": "The purpose of the review is to summarise the various drugs used in rheumatology practice implicated in the causation of DRESS syndrome. The most commonly reported drugs are allopurinol, sulfasalazine and minocycline, which pose a very high risk for DRESS syndrome development, followed by strontium ranelate and dapsone. Other, less commonly reported, drugs include leflunomide, hydroxychloroquine, non-steroidal anti-inflammatory drugs, febuxostat, bosentan and solcitinib. Reaction to some drugs is strongly associated with certain HLA alleles, which may be used to screen patients at risk of serious toxicity. DRESS syndrome is a serious reaction to many drugs used in rheumatic diseases, with a potentially fatal outcome and needs to be considered in any patient started on these medications who presents with a rash, fever and eosinophilia, sometimes with internal organ involvement.",
        "categories": [],
        "tags": [
            "DRESS syndrome",
            "Eosinophilia",
            "Hypersensitivity",
            "Toxicity",
            "Idiosynchratic",
            "Allopurinol",
            "Minocycline",
            "Sulfasalazine",
        ],
        "with": [
            "The purpose of the review is to summarise",
            "The most commonly reported drugs are allopurinol",
            "Kirchhof MG, Wong A, Dutz JP. Cyclosporine treatment",
        ],  # 3 segments
        "without": [
            "Immediate online access to all issues from 2019.",
            "© 2020 Springer Nature Switzerland AG",
            "Instant access to the full article PDF.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.royalroad.com/fiction/34798/melas/chapter/535107/chapter-1-prologue-murdered": {
        "file": "royalroad.com.melas.html",
        "author": "delta201",
        "title": "Chapter 1: Prologue - Murdered",
        "date": "2020-08-06",
        "description": " &#xA;When I woke up, there was nothing.&#xA;A pure white empty space that seemed to stretch for all eternity was all that I saw; an expansive blank canvas filled (...)",
        "categories": [],
        "tags": [],
        "with": [
            "When I woke up, there was nothing.",
            "If it was limited to my birth, I",
            "Make me the most powerful spellcaster, or whatever",
        ],  # 3 segments
        "without": [
            "Royal Road® is the home of web novels",
            "Royal Road® © 2013-2020, background by",
            "advertising fees by advertising and linking to amazon.com.",
        ],  # 3 segments
        "comments": [
            "Nice chapter! I had Melas in my PTR list",
            " the entity is an incompetent with a quick trucker finger.",
            "Her mother is wearing a purple pointed hat, something",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://harpers.org/a-letter-on-justice-and-open-debate/": {
        "file": "harpers.org.justice.html",
        "author": "",
        "title": "A Letter on Justice and Open Debate",
        "date": "2020-07-07",
        "description": "July 7, 2020 The below letter will be appearing in the Letters section of the magazine’s October issue. We welcome responses at letters@harpers.org Our cultural institutions are facing a moment of trial. Powerful protests for racial and social justice are leading to overdue demands for police reform, along with wider calls for greater equality and [&hellip;]",
        "categories": [],
        "tags": [],
        "with": [
            "Our cultural institutions are facing a moment of trial",
            "expect the public or the state to defend it for us.",
            "The free exchange of information and ideas, the",
        ],  # 3 segments
        "without": ["Do Not Sell My Personal Information", "Privacy Policy ", "Customer Care"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://nymag.com/intelligencer/2020/05/polarization-republicans-democracy-ezra-klein-book-review.html": {
        "file": "nymag.com.polarization.html",
        "author": "Eric Levitz",
        "title": "The GOP Is the Problem. Is ‘Human Identity Politics’ the Solution?",
        "date": "2020-05-16",
        "description": "Ezra Klein’s new book on polarization alerts liberals and conservatives to their species’ unifying affinity for identity-based divisiveness.",
        "categories": ["Intelligencer"],
        "tags": [
            "partisan polarization",
            "political science",
            "books",
            "politics",
            "conservatism",
            "the republican party",
            "ezra klein",
        ],
        "with": [
            "Which is to say, why was a solipsistic reality",
            "of its contradictions. As African-Americans migrated North in",
            "truth that our own identities are preventing",
        ],  # 3 segments
        "without": [
            "This site is protected by reCAPTCHA and the Googl",
            "Daily news about the politics, business, and technolog",
            "© 2020 Vox Media, LLC. All rights reserved.",
        ],  # 3 segments
        "comments": [
            "I wrote Klein off as intolerably naive a",
            "bombers of the grand old pedophile criminal gang.",
            "Trump supporters believe Trump when he says",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "http://www.netbits.us/docs/stunnel_rsync.html": {
        "file": "netbits.us.stunnel_rsync.html",
        "author": "",
        "title": "Rsync + Stunnel 4.x",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "documentation examples rely heavily on tcp-wrappers and Stunnel",
            "cd to the directory containing the tarball",
            "cert = /etc/stunnel/langly_stunnel_cert.pem",
        ],  # 3 segments
        "without": ["Last Modified:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "US",  # if obvious: DE, CH, AT
    },
    "https://emacspeak.blogspot.com/2019/10/meta-programming-in-emacs-using.html": {
        "file": "emacspeak.blogspot.com.meta.html",
        "author": "T. V. Raman ",
        "title": "Meta-Programming In Emacs Using Defadvice",
        "date": "2019-10-16",
        "description": "Here is where I plan to Blog Emacspeak tricks and introduce new features as I implement them.",
        "categories": [],
        "tags": [],
        "with": [
            "Decorators in Python enable you to modify",
            "entitled Beautiful Code, OReilly.",
            "Speak line moved to after next-line and",
        ],  # 3 segments
        "without": ["Followers (7) ", "View my complete profile", "Simple theme. Powered by"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.politico.com/news/2019/12/30/mark-meadows-retirement-elect-wife-friend-090838": {
        "file": "politico.com.retirement.html",
        "author": "ALLY MUTNICK",
        "title": "Mark Meadows accused of timing retirement to help elect wife’s friend",
        "date": "2019-12-30",
        "description": "Republicans in Western North Carolina are grumbling about his last-minute announcement, which boxed out a number of elected officials.",
        "categories": [],
        "tags": [],
        "with": [
            "shock retirement — revealed just 30 hours before the",
            "though he faces another stiff primary challenge next year.",
            "“I don’t expect anyone to hand me anything.",
        ],  # 3 segments
        "without": ["Credit Card Payments", "Notice to California Residents", "Terms of Service"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://security.googleblog.com/2020/05/enhanced-safe-browsing-protection-now.html": {
        "file": "security.googleblog.com.protection.html",
        "author": ["Nathan Parker", "Varun Khaneja", "Eric Mill", "Kiran C Nair"],
        "title": "Enhanced Safe Browsing Protection now available in Chrome ",
        "date": "2020-05-19",
        "description": "Posted by Nathan Parker, Varun Khaneja, Eric Mill and Kiran C Nair - Chrome Safe Browsing team   Over the past few years we’ve seen threats ...",
        "categories": [],
        "tags": [
            "android",
            "android security",
            "android tr",
            "app security",
            "big data",
            "biometrics",
            "blackhat",
            "chrome",
            "chrome security",
            "federated learning",
            "Gboard",
            "google play",
            "google play protect",
            " pha family highlights",
            "privacy",
            "Security",
            "spyware",
            "targeted spyware",
            "vulnerabilities",
        ],
        "with": [
            "ve seen threats on the web becoming increasingly sophisticated",
            "This protocol is designed so that Google cannot",
            "billions of users are incredibly diverse, with",
        ],  # 3 segments
        "without": [
            "Give us feedback in our",
            "Google Privacy Terms ",
            "insights from Google on security and safety on the Internet",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.wevolver.com/article/3dprinting.gets.a.turbo.boost.from.um.technology": {
        "file": "wevolver.com.3dprinting.html",
        "author": "James Lynch from University of Michigan",
        "title": "3D-printing gets a turbo boost from U-M technology",
        "date": "2020-02-20",
        "description": "",
        "categories": [],
        "tags": ["3D Printing", "machine learning vehicles"],
        "with": [
            "The algorithm allows printers to deliver high-quality results",
            "Chinedum Okwudire",
            "vibration-induced error compensation of a 3D printer",
        ],  # 3 segments
        "without": [
            "Search for articles and topics",
            "Create smart machines.",
            "We reach millions of professional engineers",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www3.nhk.or.jp/news/easy/k10011959621000/k10011959621000.html": {
        "file": "nhk.or.jp.k100.html",
        "author": "",
        "title": "子どもへの体罰を禁止する法律ができる ",
        "date": "2019-06-24",
        "description": "子どもへの虐待をなくすための法律ができて、親が子どもを教育するために、たたいたり蹴ったりする体罰を禁止することになりました。最近、親に虐待...",
        "categories": [],
        "tags": [],
        "with": [
            "子どもへの虐待をなくすための法律ができて、親が子どもを教育するために、",
            "法律では虐待をした親に専門家が子どもの育て方を",
            "虐待したときに叱っていただけだと言う親がいます。新しい法律では",
        ],  # 3 segments
        "without": [
            "※下に線があることばは辞書の説明を見ることができます。 ",
            "く転載することを禁じます。このページは受信料で制作しています。",
            "Copyright NHK (Japan Broadcasting Corporation).",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.unocero.com/smartphones/marcas-mala-gestion-apps-segundo-plano-android/": {
        "file": "unocero.com.marcas.html",
        "author": "Alberto Ávila",
        "title": "Estas son las marcas que más dificultan el trabajo de tus aplicaciones en Android",
        "date": "2019-08-27",
        "description": "Aunque muchas veces crees que el problema de tus aplicaciones es culpa del desarrollador, en realidad podría ser culpa del fabricante.",
        "categories": ["Smartphones"],
        "tags": [],
        "with": [
            "pues al hacer esto se gastaba mucha",
            "El problema es que a pesar de que",
            "convierten en una desventaja para la experiencia de uso.",
        ],  # 3 segments
        "without": [
            "y te enviaremos un correo diario con lo",
            "Derechos Reservados. unocero es una",
            "Modo Nocturno",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://thepointsguy.com/news/alaska-airlines-oneworld-membership-new-date/": {
        "file": "thepointsguy.com.alaska.html",
        "author": "Edward Russell",
        "title": "Alaska Airlines sets new date for full Oneworld membership",
        "date": "2020-10-13",
        "description": "Alaska Airlines has a new date for when it will be a full fledged member of the Oneworld alliance: March 31, 2021.",
        "categories": [],
        "tags": [],
        "with": [
            "has a new date for when it will be a full fledged member of the Oneworld",
            "at its Seattle/Tacoma International Airport (SEA) base in 2019.",
            "hat it launched in 2020, according to Cirium",
        ],  # 3 segments
        "without": [
            "This post contains references to products from one or more",
            "Bonus value is an estimated value calculated by",
            "responsibility to ensure all posts and/or questions are answered.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.medicalnewstoday.com/articles/318674": {
        "file": "medicalnewstoday.com.318674.html",
        "author": "Ana Sandoiu",
        "title": "How does the brain turn unconscious information into conscious thought?",
        "date": "2017-07-27",
        "description": "New research investigates the neurobiological timing of the so-called a-ha! moment that occurs we have come up with the solution to a complex problem.",
        "categories": [],
        "tags": ["Biology / Biochemistry", "Neurology / Neuroscience", "Psychology / Psychiatry"],
        "with": [
            "Many of us have noticed that we seem to get our",
            "But the exact moment at which information becomes",
            " that the brain goes through to complete a",
        ],  # 3 segments
        "without": [
            "myths, and reveal tips for improving brain functioning.",
            "to such placement, do not provide the information.",
            "© 2004-2020 Healthline Media UK Ltd, Brighton",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.mdavis.xyz/supermarket/": {
        "file": "mdavis.xyz.supermarket.html",
        "author": "Matthew Davis",
        "title": "A Stallman-esque short story about the future of offline tracking and the right to buy",
        "date": "2019-01-11",
        "description": "A Stallman-esque short story about the future of offline tracking and the right to buy",
        "categories": [],
        "tags": [],
        "with": [
            "The cameras recognise me as soon as I",
            "afternoon snack on way home from work",
            " FoodCorp to feed ourselves, FoodCorp feeds on us",
        ],  # 3 segments
        "without": ["11 Jan 2019", "Photo by ev on Unsplash", "find more by Matthew Davis"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.economist.com/open-future/2018/06/18/why-collaborative-thinking-beats-individual-smarts": {
        "file": "economist.com.thinking.html",
        "author": "",
        "title": "Why collaborative thinking beats individual smarts",
        "date": "2018-06-18",
        "description": 'An interview with Thomas Malone, author of “Superminds”, together with an extract from the book"',
        "categories": ["Open Future"],
        "tags": [],
        "with": [
            "about the role that the proportion of men and women in",
            "You might call this a measure of a person",
            "Can groups be intelligent in the same way individuals",
        ],  # 3 segments
        "without": [
            "Sign up to our free daily newsletter",
            "Published since September 1843 to take part in",
            "Jun 18th 2018",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://diem25.org/the-eus-green-deal-isnt-enough-save-from-climate-catastrophe/": {
        "file": "diem25.org.climate.html",
        "author": "Giovanni Gaggero",
        "title": "The EU’s Green Deal isn’t enough to save us from climate catastrophe",
        "date": "2020-12-12",
        "description": "The substantial inertia of governments on the climate crisis clearly showcases the political crisis of the European Union.",
        "categories": [],
        "tags": [
            "eu",
            "european commission",
            "European Union",
            "Green New Deal",
            "Green New Deal for Europe",
            "Ursula von der Leyen",
        ],
        "with": [
            "Due to the rise of movements dedicated to addressing",
            "The Green New Deal for Europe is the most",
            "To answer this question, the starting point should",
        ],  # 3 segments
        "without": [
            "Democracy in Europe Movement 2025",
            "Do you want to be informed of DiEM25",
            "empower workers on an unprecedented scale.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.theatlantic.com/ideas/archive/2020/08/californias-disasters-are-a-warning-climate-change-is-here/615610/": {
        "file": "theatlantic.com.disasters.html",
        "author": "Leah C. Stokes",
        "title": "How Can We Plan for the Future in California?",
        "date": "2020-08-23",
        "description": "The state’s heat waves, blackouts, and fires—amid a pandemic—offer a warning of our fossil-fuel future.",
        "categories": ["Ideas"],
        "tags": [],
        "with": [
            "When I moved to California five years ago",
            "Yet some people refuse to acknowledge that climate change",
            "happening in California has a name: climate change",
        ],  # 3 segments
        "without": [
            "We want to hear what you think about this article.",
            "Some were blasted by critics, some flopped at the",
            "Subscribe and support 162 years of independent journalism",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.bettycrocker.com/recipes/easy-pineapple-upside-down-cake/c4d3321d-fad9-41cb-8f29-8d91a4279b07": {
        "file": "bettycrocker.com.pineapple.html",
        "author": "",
        "title": "Easy Pineapple Upside-Down Cake",
        "date": "2019-06-13",
        "description": "This classic cake boasts all the fruity, gooey, caramel-y goodness that’s made it a favorite for generations—plus a secret shortcut so you can make it in a snap. With Betty Crocker™ Super Moist™ yellow cake mix, you can have this impressive dessert prepped for the oven in just 15 minutes. Bake, flip and bring it to the table to add a sweet and colorful flourish to any party!&quot;",
        "categories": ["recipes"],
        "tags": [],
        "with": [
            "pineapple slices in juice, drained, juice reserved",
            "Serve with sweetened whipped cream or an 8-oz",
            "warm or cool. Store covered in refrigerator.",
        ],  # 3 segments
        "without": [
            "© 2020 ®/TM General Mills All Rights Reserved",
            "Get kitchen tested recipes, meal ideas and more – straight to your inbox",
            "Most Recent Collections",
        ],  # 3 segments
        "comments": [
            "My son loved it. Super easy and came out perfect.",
            "Where can I find a cake recipe from scratch that works",
            "Easy directions. my family is so excited that",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://cybercook.com.br/receitas/doces/biscoitos-doces/receita-de-sequilho-com-chocolate-amargo-124300": {
        "file": "cybercook.com.br.sequilho.html",
        "author": "",
        "title": "Sequilho com Chocolate Amargo",
        "date": "",
        "description": "Já experimentou essa deliciosa receita de Sequilho com Chocolate Amargo? Na CyberCook você encontra essa e outras receitas. Saiba mais!",
        "categories": [
            "Biscoitos doces",
            "Amido de milho",
            "Chocolate",
            "Farinha de trigo",
            "Manteiga",
            "Ovo",
            "Açúcar",
            "Fermento químico em pó",
        ],
        "tags": [],
        "with": [
            "Todos os ingredientes",
            "Composição nutricional da receita",
            "Deixe secar em uma folha de papel",
        ],  # 3 segments
        "without": [
            "Geladinho de Leite em Pó e",
            "Siga o CyberCook",
            "Conheça os iogurtes proteicos e inclua-os na sua alimentação!",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BR",  # if obvious: DE, CH, AT
    },
    "https://eatsmarter.de/rezepte/vanille-hafer-porridge-mit-leinsamen-und-apfel": {
        "file": "eatsmarter.de.porridge.html",
        "author": "Iris Lange-Fricke",
        "title": "Vanille-Hafer-Porridge mit Leinsamen und Apfel",
        "date": "",
        "description": "Das Vanille-Hafer-Porridge mit Leinsamen und Apfel von EAT SMARTER sorgt für einen guten Start in den Tag.",
        "categories": [],
        "tags": [
            "Frühstück",
            "Ballaststoffreich",
            "Clean Eating",
            "Clean Eating Frühstück",
            "Porridge",
            "Süßes Frühstück",
            "Vegan",
            "Vegetarisch",
        ],
        "with": [
            "Haferdrink mit Haferflocken, Vanille und Zimt, Leinsamen",
            "Nüsse trocken in einer Pfanne anrösten. Äpfel waschen",
            "Hafer ist reich an Ballaststoffen und Calcium. Insbesondere der Quellstoff",
        ],  # 3 segments
        "without": [
            "und Beauty. Erfahren Sie hier alles über die Kooperation.",
            "Eine runde Sache also, wie Sie in dieser Warenkunde erfahren! ",
            "Diätrezepte unter 400 Kcal",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://eatwhattonight.com/2020/09/vegan-styled-char-kway-teow-stir-fry-flat-rice-noodles/": {
        "file": "eatwhattonight.com.stir.html",
        "author": "",
        "title": "Vegan Styled Char Kway Teow (Stir Fry Flat Rice Noodles)",
        "date": "2020-09-28",
        "description": "Once in a while, I liked to go vegan ! And making it a point to do it once or twice in a month if I can. And this time with a vegan styled char kway teow. It was quite delicious though even without the eggs, meat or pork lard. [&hellip;]",
        "categories": [],
        "tags": [],
        "with": [
            "Once in a while, I liked to go vegan",
            "With 2 tbsp oil left in the wok",
            "120g kway teow (flat rice noodles)⁣",
        ],  # 3 segments
        "without": ["I am Joyce from Sunny Singapore", "Enter your keywords", "Print Recipe"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://uk.trustpilot.com/reviews/581cf1892ae760087cadbf17": {
        "file": "uk.trustpilot.com.reviews.html",
        "author": "Mrs H Pyke",
        "title": "Gousto has changed my life....",
        "date": "2016-11-04",
        "description": "Gousto has changed my life....",
        "categories": [],
        "tags": [],
        "with": ["Gousto has changed my life", "What a fantastic idea!"],  # 3 segments
        "without": ["4 Nov 2016", "Useful", "reviews"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.hassanchef.com/2020/09/bhindi-masala-okra-stir-fry.html": {
        "file": "hassanchef.com.bhindi.html",
        "author": "Mobasir hassan",
        "title": "Bhindi masala (okra stir fry)",
        "date": "2020-09-15",
        "description": "Bhindi masala is a popular north Indian main course veg recipe made with bhindi (okra), tomato, onion and some spices. It can be made as dhaba style.",
        "categories": [],
        "tags": ["Veg recipes"],
        "with": [
            "Tandoori roti, Naan and paratha are also served with this masala.",
            "You can many popular dishes with bhindi like",
            "My wife only use red chilli powder",
        ],  # 3 segments
        "without": ["Copyright © Hassanchef 2020", "Post a Comment", "You might like"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.kochbar.de/tipp/1918/Tomaten-richtig-schneiden.html": {
        "file": "kochbar.de.schneiden.html",
        "author": "Marianne1",
        "title": "Tomaten richtig schneiden",
        "date": "2020-09-20",
        "description": "Der perfekte Tomaten richtig schneiden-Tipp mit Bild und einfacher Schritt-für-Schritt-Anleitung",
        "categories": [],
        "tags": [],
        "with": [
            "Ihr kennt es sicher auch!",
            "aber ohne Strunk sieht es auch schöner aus.",
            "haften am Fruchtfleisch und und können nicht",
        ],  # 3 segments
        "without": [
            "Tipp favorisieren",
            'Um den Tipp "Tomaten richtig schneiden" kommentieren',
            "Die besten TIPPS",
        ],  # 3 segments
        "comments": [
            "da ich meine Tomaten zum Anrichten schon lange",
            "Dankeschön emari ♥ Sehr gerne...und ja",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.mindmegette.hu/levagott-ujj-vajas-kekszek-halloweenra-59841/": {
        "file": "mindmegette.hu.levagott.html",
        "author": "",
        "title": "Ettől kitör a frász! Így készíts levágott ujj kekszeket Halloweenra",
        "date": "",
        "description": "Léteznek olyan ünnepek, melyeknek nem igazán vannak magyar érdekeltségű hagyományai, ám mégis beszivárogtak a köztudatba. Én például kimondottan utálom például a Valentin napot, aminek szerintem semmi értelme nincs, de az ellenkezőjére is van példa. Ilyen az angolszász gyökerekkel bíró Halloween, amit minden évben várok, és persze készülök is rá. ",
        "categories": [],
        "tags": ["házisáfrány", "halloween", "Levágott ujj", "desszert", "süti", "halloweeni süti", "Déri Szilvi", "recept"],
        "with": [
            "Szeretem, hogy a közelgő téli hónapokat",
            "Ezen az éjszakán nagy bulikat szerveznek, ahol",
            "azonnal, vagy tároljuk őket jól záródó dobozban",
        ],  # 3 segments
        "without": ["Ezek is érdekelhetnek", "Receptek karfiollal", "Friss receptjeink"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "HU",  # if obvious: DE, CH, AT
    },
    "https://www.tine.no/presserom/nyhetsarkiv/nff-tine-fotballskole-viktig-for-barneidretten-gjennom-pandemien": {
        "file": "tine.no.fotballskole.html",
        "author": "",
        "title": "NFF: TINE Fotballskole viktig for barneidretten gjennom pandemien",
        "date": "2020-10-07",
        "description": "En annerledes sesong med TINE Fotballskole nærmer seg slutten. Norges Fotballforbund (NFF) har vært bekymret for et stort frafall i barnefotballen i løpet av koronaperioden, og derfor er det ekstra gledelig å se at nærmere 55 000 fotballglade barn har deltatt på over 350 fotballskoler rundt om i hele Norge, ifølge ferske tall.",
        "categories": [],
        "tags": [],
        "with": [
            "En annerledes sesong med TINE Fotballskole nærmer seg",
            "TINE Fotballskole er en fantastisk og veldig",
            "TINE være med å bidra, avslutter Syversen.",
        ],  # 3 segments
        "without": ["113 Kalbakken, 0902 Oslo", "dine og tar i mot kommentarer og forslag.", "7. oktober 2020"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "NO",  # if obvious: DE, CH, AT
    },
    "https://www.vegolosi.it/news/climate-clock/": {
        "file": "vegolosi.it.climate.html",
        "author": "",
        "title": "ll Climate Clock ha iniziato a scorrere: sette anni è il tempo che ci rimane per agire ",
        "date": "2020-09-30",
        "description": "A New York il Metronome si trasforma in un gigantesco orologio che fa il countdown dell&#039;emergenza climatica e ricorda al mondo l&#039;urgenza di agire per ridurre rapidamente le emissioni",
        "categories": [],
        "tags": [],
        "with": [
            "Ce lo ripetono continuamente gli esperti che",
            "Ma se la nostra specie vuole sopravvivere",
            "A New York il Metronome si trasforma in un",
        ],  # 3 segments
        "without": ["Per saperne di più", "Guide di base", "Frutta e verdura di stagione"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "IT",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20200808063632/https://www.przepisy.pl/przepis/pierogi-z-dynia-w-sosie-szalwiowym": {
        "file": "archive.org.przepisy.pl.pierogi.html",
        "author": "przepisy.pl ",
        "title": "Pierogi z dynią w sosie szałwiowym",
        "date": "",
        "description": "Zobacz, jak przygotować sprawdzony przepis na Pierogi z dynią w sosie szałwiowym. Wydrukuj lub pobierz PDF z przepisem.",
        "categories": [],
        "tags": [
            "ciasto na pierogi",
            "Kuchnia Polska",
            "cebula",
            "JAJKA",
            "DYNIA",
            "PIEROGI",
            "FRISCO",
            "orzechy włoskie",
            "z orzechami",
        ],
        "with": [
            "ugotowane pierogi, chwilę wymieszaj i natychmiast podawaj.",
            "Przyprawa w Mini kostkach Smażona cebula",
            "Przygotowanie krok po kroku",
        ],  # 3 segments
        "without": [
            "Słodkie i soczyste owoce, które mogą być",
            "się do niego warzywa, sery, mięso, zioła. Skorzystaj z",
            "To naprawdę pyszne danie – przekonaj się?",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PL",  # if obvious: DE, CH, AT
    },
    "https://journals.univie.ac.at/index.php/wdr/about/submissions": {
        "file": "journals.univie.ac.at.submissions.html",
        "author": "",
        "title": "Checkliste für Beitragseinreichungen ",
        "date": "",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "müssen Sie registriert und eingeloggt sein.",
            "Soweit möglich, wurden den Literaturangaben",
            "Betonungen kursiv",
            "Internetquellen",
            "wird in Kürze bereitgestellt.",
        ],  # 3 segments
        "without": ["Beitragseinreichung", "Aktuelle Ausgabe", "Suchen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://flawlessfood.co.uk/olive-herb-focaccia-bread/": {
        "file": "flawlessfood.co.uk.olive.html",
        "author": "Kay",
        "title": "Olive & Herb Focaccia Bread",
        "date": "2020-04-12",
        "description": "Oven-baked Italian Olive &amp; Herb Focaccia Bread with fantastic flavours of olive oil, garlic, sundried tomato, olives and herbs a great side or starter",
        "categories": [],
        "tags": [
            "Focaccia",
            "Focaccia Bread",
            "Garlic Focaccia",
            "Italian Focaccia Bread",
            "Olive Bread",
            "Sundried tomato and garlic Focaccia bread",
        ],
        "with": [
            "Oven-baked Italian Olive & Herb Focaccia",
            "oil mixture for dipping the focaccia bread into.",
            "Carbohydrates: 31g",
        ],  # 3 segments
        "without": [
            "email address will not be published. Required fields",
            "We occasionally get sponsored by products, we",
            "We publish new recipes weekly, so keep",
        ],  # 3 segments
        "comments": [
            "Yum how delicious! Love the special touch of",
            "Great to hear Jenny!",
            "It is a great bread, hope you get",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://sportowefakty.wp.pl/zuzel/relacja/110331/fogo-unia-leszno-rm-solar-falubaz-zielona-gora": {
        "file": "sportowefakty.wp.pl.falubaz.html",
        "author": "",
        "title": "RM Solar Falubaz Zielona Góra",
        "date": "",
        "description": "Zobacz relację live z wydarzenia Fogo Unia Leszno - RM Solar Falubaz Zielona Góra – 57 : 33, 28.09.2020, Żużel, PGE Ekstraliga. Wyniki online, komentarze, informacje.",
        "categories": [],
        "tags": [],
        "with": [
            "Znów lepszy moment startowy miejscowych, lecz",
            "W Lesznie zaczął mocno padać deszcz.",
            "Stadion im. Alfreda Smoczyka w Lesznie",
        ],  # 3 segments
        "without": ["© 1995-2020 Grupa WP", "Polskie gwiazdy", "Zobacz również"],  # 3 segments
        "comments": [
            "W rundzie zasadniczej zespół z Zielonej Góry zaskoczy",
            "pierwszym meczu w tej parze półfinałowe",
            "Wylosowano I zestaw startowy.",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.healthline.com/nutrition/ways-to-measure-body-fat": {
        "file": "healthline.com.fat.html",
        "author": "Grant Tinsley",
        "title": "The 10 Best Ways to Measure Your Body Fat Percentage",
        "date": "2018-04-29",
        "description": "Focusing on body fat percentage instead of weight is much more useful to track fat loss progress. Here are the 10 best ways to measure your body fat percentage.",
        "categories": ["Nutrition"],
        "tags": [],
        "with": [
            "It can be frustrating to step on the scale",
            "Skinfold measurements have been used to estimate",
            "Some methods, such as skinfold measurements, circumference",
        ],  # 3 segments
        "without": [
            "to improve your health or lose weight, ",
            "© 2005-2020 Healthline Media a Red Ventures",
            "Filter out the noise and nurture your inbox",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.realsimple.com/home-organizing/gardening/outdoor/hydrangea-care": {
        "file": "realsimple.com.hydrangea.html",
        "author": "Sarah Yang",
        "title": "How to Care for Hydrangeas to Get the Most Beautiful Blooms on the Block",
        "date": "2019-05-06",
        "description": "It&#x27;s not too late to start a garden this year. Here are the best fall plants, including beautiful hydrangea, to grow right now.",
        "categories": [],
        "tags": ["Real Simple", "Home Organizing", "Gardening", "Outdoor Gardening"],
        "with": [
            "Hydrangeas may be just about everywhere",
            "Make sure that the bottom of your container has holes",
            "1. Choose the Right Pot",
        ],  # 3 segments
        "without": [
            "choosing your hydrangeas at the store, look for",
            "Fall is the time of year when root",
            "Sarah Yang",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://thepostpartumparty.com/how-to-set-up-a-baby-nursery-in-a-small-space": {
        "file": "thepostpartumparty.com.nursery.html",
        "author": "Amy Motroni",
        "title": "20 Clever Small Nursery Ideas When You’re Tight On Space + Free Printable",
        "date": "2019-07-24",
        "description": "Set up your baby nursery in a small space. With these simple small nursery ideas, you can set up a functional nursery, even if you&#039;re tight on space.",
        "categories": [],
        "tags": [],
        "with": [
            "Pick products that can serve multiple purposes",
            "Sometimes space is in the eye of the beholder",
            "the idea of where to put everything can",
        ],  # 3 segments
        "without": [
            "must-haves, and so much more.",
            "Notify me of follow-up comments by email.",
            "The Postpartum Party does not offer medical advice",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.instyle.com/beauty/wigs-for-black-women-cancer": {
        "file": "instyle.com.cancer.html",
        "author": "Kayla Greaves",
        "title": "Black Women Battling Breast Cancer Deserve More Wig Options, According to Coils to Locs Founder Dianne Austin",
        "date": "2020-10-13",
        "description": "Dianne Austin is the co-founder of Coils to Locs, a company that creates medical wigs for Black women battling cancer that match the texture of their natural hair. ",
        "categories": ["Beauty"],
        "tags": [],
        "with": [
            "decided to ditch her relaxer and transition back",
            "to see themselves provides privacy and dignity.",
            "All women, regardless of hair type, should",
        ],  # 3 segments
        "without": [
            "Scroll Down For the Next Article",
            "A lot of the royal families had these",
            "On the other hand, Black doo-wop girl",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.dailymail.co.uk/news/article-8772683/Chef-Jamie-Oliver-joins-Mail-Sundays-war-toxic-food.html": {
        "file": "dailymail.co.uk.food.html",
        "author": "Glen Owen And Brendan Carlin For The Mail On Sunday",
        "title": "Jamie's war on toxic US food: Chef and fitness guru Joe Wicks lead plea to Boris Johnson to block sub-standard products from flooding into the UK under post-Brexit trade deals",
        "date": "2020-09-26",
        "description": "The move comes as International Trade Secretary Liz Truss faces growing Parliamentary pressure to bolster protections against poor quality foreign food.",
        "categories": [],
        "tags": [],
        "with": [
            "A powerful alliance of chefs, celebrities and charities",
            " would also help secure the goal set out so",
            "Even George Eustice, the current Environment Secretary",
        ],  # 3 segments
        "without": [
            "As many as a million young people",
            "The letter also argues that 'the British public",
            "As things stand the Government is telling Tory MP",
        ],  # 3 segments
        "comments": [
            "Cont) Some Chefs in Britain cannot even COOK MEAT PROPERLY",
            "vegetarian animals, as in the EU! No BSE in the US!",
            "If we want distinctively British standards and regulation",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://www.independent.co.uk/news/uk/politics/coronavirus-false-reporting-contact-fine-penalty-b671230.html": {
        "file": "independent.co.uk.penalty.html",
        "author": "Andrew Woodcock",
        "title": "Coronavirus: £1,000 fine for falsely reporting a contact to force them to self-isolate",
        "date": "2020-09-28",
        "description": "Pubs and bars face penalties for playing loud music or allowing singing and dancing ",
        "categories": [],
        "tags": ["pubs", "regulations", "Coronavirus"],
        "with": [
            "Anyone falsely naming an antagonist as a coronavirus contact",
            "But it is understood that the ban on giving",
            "New fines for failure to self-isolate, starting",
        ],  # 3 segments
        "without": [
            "Code of conduct and complaints",
            "Share your thoughts and debate the big issues",
            "Popular videos",
        ],  # 3 segments
        "comments": [
            "Is this fake news?  I cannot",
            "Rather than trying to force people to isolate",
            "At least we don&amp;#x27;t have to go to prayers?",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://stardewvalleywiki.com/Penny": {
        "file": "stardewvalleywiki.com.penny.html",
        "author": "",
        "title": "Penny",
        "date": "2020-10-25",
        "description": "Penny is a villager who lives in Pelican Town. She's one of the twelve characters available to marry. Her trailer is just east of the center of town, west of the river.",
        "categories": ["Marriage candidates"],
        "tags": [],
        "with": [
            "Penny lives with her mom, Pam, in a little trailer by",
            "Penny is a villager who lives in Pelican Town",
            "A fermented beverage made from honey.",
        ],  # 3 segments
        "without": ["Content is available under", "Privacy policy", "Admin noticeboard"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "CC BY-NC-SA 3.0",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://statisticsglobe.com/change-font-size-of-ggplot2-plot-in-r-axis-text-main-title-legend": {
        "file": "statisticsglobe.com.ggplot2.html",
        "author": "oachim Schork",
        "title": "Change Font Size of ggplot2 Plot in R (5 Examples) | Axis Text, Main Title & Legend",
        "date": "",
        "description": "How to modify font sizes of ggplot2 graphics in R - 5 programming examples - Change font size of axes, main title &amp; legend - Reproducible R code",
        "categories": [],
        "tags": [],
        "with": [
            "explain how to increase and decrease the text",
            "y = Probability",
            "If you have any further questions, please",
        ],  # 3 segments
        "without": [
            "Get regular updates on the latest tutorials",
            "On this website, I provide statistics tutorials",
            "Related Tutorials",
        ],  # 3 segments
        "comments": ["I posted on your youtube channel a question", "Very helpful."],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.tomshardware.com/uk/news/where-and-how-to-buy-rtx-3080-3090-3070": {
        "file": "tomshardware.com.rtx.html",
        "author": "Michelle Ehrhardt",
        "title": "Where and How to Buy an RTX 3080, 3090 or 3070 ",
        "date": "2020-11-02",
        "description": "The RTX 3000 series is finally here, which is why we’ve compiled a guide to get your hands on an RTX 3000 card before they sell out.",
        "categories": [],
        "tags": [],
        "with": [
            "RTX 3000 series graphics cards are finally",
            "also some aftermarket RTX 3080 cards up on",
            "RTX 3080 and RTX 3090 cards are",
        ],  # 3 segments
        "without": ["No spam, we promise.", "More about...", "When you purchase through links on our site"],  # 3 segments
        "comments": [
            "How to buy: be a bot, otherwise, you",
            "As predicted by many reviewers and journalists",
            "As predicted by many reviewers and journalists",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.corkbeo.ie/news/local-news/level-3-live-cork-ireland-19056312": {
        "file": "corkbeo.ie.level.html",
        "author": "Gavin O'Callaghan",
        "title": "Level 3 LIVE from Cork as Ireland adapts to incoming coronavirus restrictions",
        "date": "2020-10-06",
        "description": "The country avoided Level 5 last night, but NPHET have warned it may be down the line",
        "categories": [],
        "tags": [],
        "with": [
            "Tonight at midnight Cork will be moved into Level 3",
            "So we thought that this is not the",
            "Taoiseach Micheal Martin confirmed this evening that",
        ],  # 3 segments
        "without": [
            "Never miss the latest news by signing",
            "Corrections and Clarifications",
            "The latest update for the Irish abroad",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "IE",  # if obvious: DE, CH, AT
    },
    "https://www.nationalrail.co.uk/service_disruptions/245738.aspx": {
        "file": "nationalrail.co.uk.disruptions.html",
        "author": "",
        "title": "Rail Replacement Services Travel Advice",
        "date": "",
        "description": "The gateway to Britain&#39;s National Rail network. A portal into UK rail travel including train company information and promotions; train times; fares enquiries; ticket purchase and train running information.",
        "categories": [],
        "tags": ["Coronavirus", "Facebook", "Twitter", "Museums"],
        "with": [
            "Customers with disabilities will be asked about the best",
            "only on longer journeys over 60 minutes",
            "LNER are able to carry foldable wheelchairs as",
        ],  # 3 segments
        "without": ["About this site", "Rail Replacement", "You are here"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://www.chocolate.com/view/woman-sees-a-car-stop-for-pregnant-beggar-this-is-what-she-finds-when-she-follows/&page=2": {
        "file": "chocolate.com.pregnant.html",
        "author": "Cara Stiles",
        "title": "Woman Sees a Car Stop for Pregnant Beggar, This is What She Finds When She Follows ",
        "date": "2020-04-13",
        "description": "Woman Sees a Car Stop for Pregnant Beggar, This is What She Finds When She Follows - A Mysterious Woman She couldn't take her eyes off the woman. Could it be true? Was she trying to fool her all along? So many thoughts were racing through her head. Maybe she was just being lured. But, maybe she was also in danger. . But, when the beggar agreed to sit into that car, she knew that something was wrong. She decided to go after her and find out the truth. But, little did she know that she'd discover a web of lies.",
        "categories": [],
        "tags": [],
        "with": [
            "Could it be true? Was she trying",
            "working to catch those who run operations",
            "she was lucky enough to receive a",
        ],  # 3 segments
        "without": ["CHOCOLATE.COM2020", "Terms Of Service", "DMCA"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.thelist.com/214894/when-you-take-a-multivitamin-every-day-this-is-what-happens-to-your-body/": {
        "file": "thelist.com.multivitamin.html",
        "author": "Cat Lafuente",
        "title": "When you take a multivitamin every day, this is what happens to your body",
        "date": "2020-06-12",
        "description": "Do you take a multivitamin every day? It certainly seems like a rational way to give yourself an extra boost, whether it&#039;s to amp up your immunity or increase your energy levels. But just what happens to your body if you start taking a multivitamin daily? Here&#039;s what you need to know.",
        "categories": [],
        "tags": [],
        "with": [
            "Do you take a multivitamin every day?",
            "sleeping for seven to nine hours a night",
            "help steel yourself against any nutritional fallout.",
        ],  # 3 segments
        "without": [
            "If you take turmeric every day, you might",
            "retro-hipster chic (so 2010!) to your bathroom.",
            "everyone has different nutritional needs, and she",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.sports.fr/direct-foot/50918/177512/lorient-olympique-lyonnais.html": {
        "file": "sports.fr.lorient.html",
        "author": "",
        "title": "Match en direct",
        "date": "",
        "description": "Toute l'actualité sportive : football, basket, nba, rugby, tennis...",
        "categories": [],
        "tags": [],
        "with": [
            "terminé au Moustoir ! Lorient a tenu",
            "Le coup de pied de coin ne donne rien.",
            "se cherchent en ce début de match.",
        ],  # 3 segments
        "without": ["Ligue des Champions de la CAF", "Europa League", "Tous les sports"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://pawszilla.com/pop-culture/celebrities/fans-expressed-fears-celine-dions-appearance-savagely-responded/21/": {
        "file": "pawszilla.com.celine.html",
        "author": "Staff Writer",
        "title": "Fans Expressed Fears Over Céline Dion’s Major Weight Loss – Then The Star Confirmed The Real Cause",
        "date": "",
        "description": "When Céline Dion became the victim of trolling and body-shaming, she responded in surprising style. Even though Céline Dion is a multi-million-selling pop icon, people have occasionally chosen to focus more on her body than her considerable professional accomplishments. Recently, for instance, fans of the “My Heart Will Go On” songstress took to her Instagram&hellip;",
        "categories": [],
        "tags": [],
        "with": [
            "Even though Céline Dion is a multi-million-selling",
            "So this led to the star coming clean to her critics in spectacular fashion.",
            "Her most iconic looks of the 1990s",
        ],  # 3 segments
        "without": ["Getty Images", "Staff Writer", "Battery Media Group"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.foxyfolksy.com/chocolate-buttercream-frosting-without-powdered-sugar-ermine-icing/": {
        "file": "foxyfolksy.com.buttercream.html",
        "author": "Bebs",
        "title": "Chocolate Buttercream Frosting without Powdered Sugar (Ermine Icing)",
        "date": "2018-01-28",
        "description": "Try this Chocolate Buttercream Frosting. No powdered sugar needed. It is so light and fluffy and smoother than the classic American Buttercream Frosting. It is a bit more work but definitely easier than Swiss Meringue Frosting. It is easily the best buttercream frosting I&#039;ve tried.",
        "categories": ["Cake Recipes"],
        "tags": [],
        "with": [
            "Try this Chocolate Buttercream Frosting. No powdered sugar",
            "Combine and sift together the flour, sugar, salt",
            "work but definitely easier than Swiss Meringue Frosting",
        ],  # 3 segments
        "without": [
            "Send me email every new post.",
            "Receive new posts directly delivered to your inbox",
            "miss a post. Get updates directly to your inbox ",
        ],  # 3 segments
        "comments": [
            "not as sweet as the American version",
            "Amazing! Just sweet enough, silky smooth texture",
            "Hi Fiona, glad this recipe was able",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://mydailymagazine.com/get-in-the-spooky-spirit-with-these-halloween-workouts/": {
        "file": "mydailymagazine.com.halloween.html",
        "author": "Ariel H",
        "title": "Get in the Spooky Spirit With These Halloween Workouts",
        "date": "2020-10-26",
        "description": "Get in the Spooky Spirit With These Halloween Workouts - My Daily Magazine - Art, Design, DIY, Fashion and Beauty !",
        "categories": [],
        "tags": ["halloween", "Halloween workout"],
        "with": [
            "Believe it or not, Halloween is just days",
            "Kelsey Ellis, is perfect for you. The workout",
            "12 reps of each exercise with one to",
        ],  # 3 segments
        "without": [
            "Terms & Conditions",
            "Find Beauty in Imperfection with Public Holiday",
            "Hot Buttered Rum Cocktail All Season Long",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://youhadmeatgardening.com/lemon-tree-from-seed": {
        "file": "youhadmeatgardening.com.lemon.html",
        "author": "Florina Ionescu",
        "title": "How to Grow a Lemon Tree from Seed | Step-by-Step Guide",
        "date": "",
        "description": "Learn how to grow a lemon tree from seed with this step-by-step guide on germinating and planting lemon seeds from store-bought lemons!",
        "categories": [],
        "tags": [],
        "with": [
            "Now you know how to grow lemon trees",
            "for planting lemon seeds has a pH between",
            "Place the seeds about one inch apart on a paper",
        ],  # 3 segments
        "without": [
            "Your email address will not be published",
            "We can help you grow the indoor",
            "apartment gardening. Learn how to stop killing",
        ],  # 3 segments
        "comments": [
            "I have grown a lemon tree from seed",
            "Hello Tarina! Thank you for contacting us",
            "inches tall but they are doing well",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.standard.co.uk/news/uk/turkey-poland-caribbean-islands-added-to-uk-quarantine-list-a4561256.html": {
        "file": "standard.co.uk.caribbean.html",
        "author": "Daniel O'Mahony",
        "title": "Turkey, Poland and three Caribbean islands added to UK quarantine list",
        "date": "2020-10-01",
        "description": "Penalties for those who refuse to self-isolate are to be increased to a maximum of £10,000 for repeat offenders",
        "categories": [],
        "tags": [
            "Turkey",
            "Poland",
            "Caribbean",
            "Quarantine",
            "Coronavirus",
            "covid-19",
            "Travel",
            "Grant Shapps",
            "air bridges",
        ],
        "with": [
            "Penalties for those who refuse to self-isolate are",
            "Travellers arriving in the UK from those places after",
            "to defend what the Government is doing",
        ],  # 3 segments
        "without": ["There are no comments yet", "This is London Magazine", "Be part of the conversation"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://ext.theperspective.com/items-we-never-knew-we-wanted/1/": {
        "file": "ext.theperspective.com.items.html",
        "author": "Adi Tzlil",
        "title": "Items We Never Knew We Wanted",
        "date": "2020-09-21",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "dawn of the internet brought about a lot",
            "to turn any laundry day into a blast",
            "This item is perfect for those of",
        ],  # 3 segments
        "without": ["All Rights Reserved", "The Perspective Challenge", "DMCA"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.popsugar.co.uk/smart-living/Cheap-Homemade-Halloween-Costumes-42432483/amp": {
        "file": "popsugar.co.uk.halloween.html",
        "author": "Emily Co",
        "title": "90+ Costumes For Adults to DIY on the Cheap This Halloween",
        "date": "2020-10-30",
        "description": "Cheap and easy DIY costumes are all that matter this Halloween, and we are here to tell you that you can consider your 2020 costume complete thanks to these",
        "categories": [],
        "tags": ["Budget Tips", "DIY Costumes", "DIY", "Halloween"],
        "with": [
            "thanks to these genius ideas. This year",
            "With a bowler hat, a set of false lashes",
            "Long hair or not, you can still pull",
        ],  # 3 segments
        "without": ["Send You Push Notifications.", "POPSUGAR Would Like To ", "Want More?"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://harrypotter.fandom.com/wiki/Water-Making_Spell": {
        "file": "harrypotter.fandom.com.spell.html",
        "author": "",
        "title": "Water-Making Spell",
        "date": "",
        "description": "The Water-Making Spell2 (Aguamenti) was a charm that conjured a jet of clean, drinkable water from the tip of the caster&#039;s wand. This spell, in addition to being a charm, can also be classified as conjuration, an advanced form of Transfiguration. 1 History 2 Effects 3 Known uses 4 Known...",
        "categories": [
            "Articles with information from Wonderbook: Book of Spells",
            "Articles with information from Harry Potter and the Half-Blood Prince",
            "Articles with information from Harry Potter and the Deathly Hallows",
            "Articles with information from Harry Potter and the Goblet of Fire",
            "Articles with information from Harry Potter and the Order of the Phoenix",
            "Articles with information from Harry Potter: Hogwarts Mystery",
            "Articles with information from Harry Potter: Puzzles &amp; Spells",
            "Articles with information from Harry Potter: Wizards Unite Articles with information from Pottermore",
            "Articles with information from Wizarding World",
            "Spells",
            "Charms",
            "Conjurations",
            "Crystal Cave",
            "Spells with a light",
            "Spells with Incantations of Latin Origin",
            "Transfiguration Spells",
            "Water",
            "Water-based magic",
        ],
        "tags": [],
        "with": [
            '"The Water-Making Spell conjures clean, drinkable water from',
            "A jet of water flew out of the umbrella tip",
            "Hermione used this charm to extinguish his burning eyebrows",
        ],  # 3 segments
        "without": [
            "Take your favorite fandoms with you and never miss a beat.",
            "What is your opinion on people becoming obsessed with Draco?",
            "Harry Potter Wiki is a FANDOM Movies Community.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.msn.com/en-gb/news/uknews/uk-university-student-halls-too-full-to-be-safe-experts-warn/ar-BB19DUqK": {
        "file": "msn.com.university.html",
        "author": "Anna Fazackerley",
        "title": "UK university student halls too full to be safe, experts warn ",
        "date": "2020-10-02",
        "description": "As increasing numbers of UK universities wrestle with Covid-19 outbreaks, experts are warning that student halls are too full to be safe.&amp;nbsp;",
        "categories": [],
        "tags": [],
        "with": [
            "s increasing numbers of UK universities wrestle with",
            "seven days. In Northern Ireland, call your GP.",
            "Some UK universities, including Cambridge, Imperial College London",
        ],  # 3 segments
        "without": [
            "powered by Microsoft News",
            "Sign in",
            "Commenting is not currently available, but don’t worry",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UK",  # if obvious: DE, CH, AT
    },
    "https://klubjagiellonski.pl/2021/04/22/nowa-zelandia-platny-urlop-dla-rodzicow-poronionego-dziecka-jak-to-wyglada-w-polsce/": {
        "file": "Nowa Zelandia_ płatny urlop dla rodziców poronionego dziecka. Jak to wygląda w Polsce_ — Klub Jagielloński.html",
        "with": ["Trzy dni", "w życie w kwietniu.", "Ustawa Holidays"],
        "without": ["korzystamy z cookies.", "Czytasz właśnie nowy", "Twój email"],
    },
    "https://liberte.pl/koncesjonowana-opozycja/": {
        "file": "Koncesjonowana opozycja -Leszek Jażdżewski - Liberté!.html",
        "with": ["Pakt lewicy z PiS", "Podsumujmy. Lewica", "na salonach władzy."],
        "without": ["Fundusz Odbudowy, lewica, PiS", "Inne artykuły autora", "Polityka prywatności"],
    },
    "https://www.dwutygodnik.com/artykul/9491-winda-w-chmurach.html": {
        "file": "Winda w chmurach _ Obyczaje _ Dwutygodnik _ Dwutygodnik.html",
        "with": ["Ludzie ci", "Aleksandra Zbroja przedstawia się", "Mireczka, i bez niego."],
        "without": ["11 minut czytania", "Historyczka nowoczesnej kultury polskiej", "IWONA KURZ"],
    },
    "https://publica.pl/teksty/rafalska-finowie-odkrywaja-wino-68379.html": {
        "file": "Finowie odkrywają wino _ Res Publica Nowa.html",
        "with": ["Nie mogąc konkurować", "W Finlandii obowiązuje", "koncepcję „zero waste”"],
        "without": ["marca 2021", "Rozmowa z dr nauk", "Wino lepsze od"],
    },
    "https://spidersweb.pl/2021/05/windows-10-flash.html": {
        "file": "Windows 10 od lipca przestanie obsługiwać Adobe Flash.html",
        "with": ["W październiku na", "wspomniane cyberbezpieczeństwo.", "nigdy go nie obsługiwały."],
        "without": ["do dyskusji", "Używamy informacji zapisanych", "UDOSTĘPNIJ"],
    },
    "https://www.polityka.pl/tygodnikpolityka/swiat/2116825,1,krolowa-elzbieta-wyplywa-w-swiat-sygnal-dla-chin-i-rosji.read": {
        "file": "„Królowa Elżbieta” wypływa w świat. Sygnał dla Chin i Rosji - Polityka.pl.html",
        "with": ["Pierwszy rejs HMS", "Bandera podąża za handlem", "zaważyła na jego trasie."],
        "without": ["Czytaj też", "Były dowódca wojsk USA", "starszy analityk"],
    },
    "https://www.rp.pl/Polityka/305049888-Unijne-fundusze-coraz-blizej-Sejm-zaglosowal-za.html": {
        "file": "Unijne fundusze coraz bliżej. Sejm zagłosował _za_ - Polityka - rp.pl.html",
        "with": ["To jest moment fundamentalny", "Ciężar dyskusji przeniesie", "Na lepszą konkurencyjność gospodarki"],
        "without": ["Licencja na publikację", "Reklama", "Dowiedz się więcej", "Rafał Guz", "Publikacja:"],
    },
    "https://forsal.pl/gospodarka/pkb/artykuly/8150873,ile-jest-warta-godzina-pracy.html": {
        "file": "Ile jest warta godzina pracy_ W tych krajach praca popłaca - Forsal.pl.html",
        "with": ["Portal Statista powołuje", "54,4 dolara.", "Oto kraje, w"],
        "without": ["ShutterStock", "Ten tekst przeczytasz", "Źródło:"],
    },
    "https://wiadomosci.dziennik.pl/polityka/artykuly/8156148,dezubekizacja-trybunal-konstytucyjny-wyrok-termin.html": {
        "file": "Dezubekizacja – reaktywacja. Czyli daty mają znaczenie - Dziennik.pl.html",
        "with": ["Historia dezubekizacji przed", "12 maja. Tego", "Skarżący powołali się"],
        "without": ["Trybunał Konstytucyjny", "CZYTAJ WIĘCEJ W", "Materiał chroniony prawem"],
    },
    "https://dorzeczy.pl/ekonomia/183131/eurostat-polska-z-najnizszym-bezrobociem-w-calej-ue.html": {
        "file": "Eurostat_ Polska z najniższym bezrobociem w całej UE.html",
        "with": ["Wyrównana sezonowo stopa", "Holandia (3,5 proc.).", "najniższa w UE – podał Eurostat."],
        "without": ["Praca w magazynie", "Źródło:", "NAJNOWSZE"],
    },
    "https://www.portalspozywczy.pl/handel/wiadomosci/eurocash-rusza-z-innowacyjna-platforma-handlu,198264.html": {
        "file": "Eurocash rusza z Innowacyjną Platformą Handlu - Handel dystrybucja.html",
        "with": ["Jest to zintegrowany system", "kasowy IPH POS.", "dostęp do IPH za 1 zł."],
        "without": ["Szukasz lokalu handlowego", "Materiał chroniony prawem", "więcej informacji:"],
    },
    "https://wiadomosci.gazeta.pl/wiadomosci/7,114883,27025667,ziemniaki-na-szostej-surowka-na-dziesiatej-jak-pomoc-zeby.html#s=BoxMMt2": {
        "file": "_Ziemniaki na szóstej, surówka na dziesiątej_. Jak pomagać, żeby nie zaszkodzić_ [PORADNIK W PIGUŁCE].html",
        "with": ["pomóc osobie niewidomej", "Osoby niewidome, słabowidzące:", "może wypaść z wózka."],
        "without": ["Agencja Gazeta", "cocopanda.pl", "Komentarze"],
    },
    "https://www.radiomaryja.pl/informacje/sprzeciw-wobec-atakow-na-fundacje-lux-veritatis/": {
        "file": "Sprzeciw wobec ataków na Fundację Lux Veritatis – RadioMaryja.pl.html",
        "with": ["Watchdog wytoczył", "Nie możemy pozwolić na", "nękania Fundacji Lux Veritatis"],
        "without": ["więcej]", "drukuj", "RIRM"],
    },
    "https://www.wsieciprawdy.pl/sieci-ipn-czyli-element-infrastruktury-krytycznej-pnews-4715.html": {
        "file": "„Sieci”_ IPN, czyli element infrastruktury krytycznej Tygodnik Sieci.html",
        "with": ["Zadania Instytutu Pamięci", "co zechcą - czytamy.", "łamach nowego wydania"],
        "without": ["opublikowano:", "Zobacz także", "Zapraszamy też do subskrypcji"],
    },
    "https://wpolityce.pl/gospodarka/549052-jest-zgoda-pe-na-umowe-handlowa-miedzy-ue-a-londynem": {
        "file": "Jest zgoda PE na umowę handlową między UE a Londynem.html",
        "with": ["Zgoda PE jest", "i otwiera nową erę", "„historycznym błędem”"],
        "without": ["opublikowano", "aja/PAP", "Czekamy na Wasze"],
    },
    "https://www.osw.waw.pl/pl/publikacje/analizy/2021-04-20/rosyjskie-zamachy-w-czechach-kontekst-krajowy-implikacje-perspektywy": {
        "file": "Rosyjskie zamachy w Czechach – kontekst krajowy, implikacje, perspektywy.html",
        "with": ["17 kwietnia na konferencji", "Informacja o noszącym", "Media czeskie i brytyjskie"],
        "without": ["DO WYSŁUCHANIA W SERWISIE", "Mateusz Seroka", "Publikacje"],
    },
    "https://www.wirtualnemedia.pl/artykul/maciej-krzysztoszek-rzecznik-prasowy-amica-menedzer-komunikacji-zewnetrznej": {
        "file": "Maciej Krzysztoszek rzecznik prasowy Amica menedżer komunikacji zewnętrznej.html",
        "with": ["w dziale marketingu.", "Mickiewicza w Poznaniu.", "i komunikacją wewnętrzną."],
        "without": ["Zmiany personalne", "polecamy", "Podziel się"],
    },
    "https://menway.interia.pl/historia/news-angus-barbieri-nie-jadl-przez-382-dni,nId,5222535": {
        "file": "Angus Barbieri. Nie jadł przez 382 dni - Menway w INTERIA.PL.html",
        "with": ["Angus pochodził ze", "nie dłuższy niż 40 dni.", "Początkowo Barbieri znajdował", "cukru oraz mleka."],
        "without": ["domena publiczna", "Opuszczony Dom", " Poniedziałek"],
    },
    "https://energetyka24.com/rosjanie-sugeruja-natychmiastowe-odciecie-polski-od-gazu": {
        "file": "Rosjanie sugerują natychmiastowe odcięcie Polski od gazu - Energetyka24.html",
        "with": ["Rosjanie twierdzą, że z", "Danię do Polski.", "konkluduje finobzor.ru."],
        "without": ["ZOBACZ TAKŻE", "Reklama", "Prosimy o zaznaczenie", "Czyżewski"],
    },
    "https://villagersandheroes.com/forums/threads/patchnotes-4-47-4-tagundnachtgleiche-bugfix-build.3976/": {
        "file": "villagersandheroes.com.forums.patchnotes.html",
        "author": "Tiberius",
        "title": "Patchnotes 4.47.4 - Tagundnachtgleiche Bugfix Build",
        "date": "2020-09-18",
        "description": "Patch Notes 4.47.4",
        "categories": [],
        "tags": [],
        "with": [
            "Die Farbe der Spawn-Ankündigungen wurde geändert auf orange",
            "erhöhen, zum Schaden aber nur begrenzt beitragen, entsteht.",
            "Was jeder von Euch daraus nun für Konsequenzen zieht in Eventzonen",
        ],  # 3 segments
        "without": [
            "Forum software by XenForo® © 2010-2019 XenForo Ltd.",
            " Terms and rules",
            " Privacy policy",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://plantcaretoday.com/how-to-grow-and-care-for-bougainvillea.html": {
        "file": "plantcaretoday.com.bougainvillea.html",
        "author": "",
        "title": "How To Grow and Care For Bougainvillea",
        "date": "",
        "description": "Bougainvillea care has become more important with the popularity of this plant. A colorful patio or deck addition, We share growing and care info.",
        "categories": ["Vines"],
        "tags": [],
        "with": [
            "I need some help with Bougainvillea care and watering",
            "In the United States, the peak blooms are typically",
            "Hardiest species, with somewhat furry foliage and red-purple",
        ],  # 3 segments
        "without": [
            "Plantcaretoday.com is a participant in the Amazon Services",
            "Plant Care Newsletter",
            "Tips On Getting Rid Of Caterpillars On Roses",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://anarc.at/blog/2020-10-18-cdpath-replacement/": {
        "file": "anarc.at.cdpath.html",
        "author": "",
        "title": "CDPATH replacements",
        "date": "2020-10-18",
        "description": "",
        "categories": ["Blog"],
        "tags": ["debian-planet", "emacs", "python-planet", "review", "shell"],
        "with": [
            " I figured I might as well bite the",
            "Those projects can be used to track files",
            "this list through a command or the menu",
        ],  # 3 segments
        "without": ["Contact", "Copyleft © 2002-2016 The Anarcat", " Powered by"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "CC-BY-SA",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://economictimes.indiatimes.com/tech/hardware/the-iphone-se-is-in-india-heres-all-we-know/not-a-flagship/slideshow/76280131.cms": {
        "file": "economictimes.indiatimes.com.slideshow.html",
        "author": "ET Online",
        "title": "The iPhone SE is in India, here's all we know",
        "date": "2020-06-09",
        "description": "The latest iPhone from Apple is not what you would expect - a successor to the 2016 SE - it is designed to look like the iPhone 8 from 2017, but is a massive upgrade on it.Image credit: www.apple.com/in/ ​Not a flagship",
        "categories": [],
        "tags": [],
        "with": [
            "The latest iPhone from Apple is not what",
            "All of this - coupled with better cameras - comes",
            "But, the iPhone SE fits in so much more",
        ],  # 3 segments
        "without": [
            "Apple has just updated the 13-inch MacBook Pro",
            "for a smoother typing experience, according to Apple.",
            "production and sales but new models are still being ",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "http://www.jobsnhire.com/articles/35030/20160214/need-know-cvs-health.htm": {
        "file": "jobsnhire.com.health.html",
        "author": "Jose de la Cruz",
        "title": "Better Health For America: What You Need To Know About CVS Health",
        "date": "2016-02-14",
        "description": "CVS Health is all about helping people who are treading a path to better health. Basically, this business entity is a pharmacy innovation company with a clear goal of providing the best in health care to its customers.",
        "categories": [],
        "tags": ["CVS Health", "CVS Pharmacy", "Healthcare", "CVS Health Platinum Whitening Kit"],
        "with": [
            "is all about helping people who are treading",
            "CVS Health also helps those diagnosed with complex",
            "17.6 percent to $2.7 billion. It seems CVS Health is really",
        ],  # 3 segments
        "without": [
            "Get the Most Popular Jobs&Hire Stories in a Weekly Newsletter",
            " acceptance of our Terms and Conditions of Use and Privacy Policy. ",
            "t Career Options, Job Titles and Descriptions",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://football.ua/germany/311510-podolski-zavershil-kareru-v-sbornojj.html": {
        "file": "football.ua.podolski.html",
        "author": "",
        "title": "Подольски завершил карьеру в сборной",
        "date": "2016-08-15",
        "description": "Ветеран сборной Германии Лукаш Подольски принял решение прекратить выступления за Бундестим.",
        "categories": [],
        "tags": [],
        "with": [
            "летний Лукаш Подольски – третий по количеству матчей за сборную",
            "Экс-игрок Арсенала и Баварии попал в заявку",
            "Решение далось мне очень тяжело. Сборная всегда была",
        ],  # 3 segments
        "without": [
            '© 2006-2019 ООО "ВИДАВНИЦТВО УКРАЇНСЬКИЙ МЕДІА ДІМ". Все права защищены.',
            "Политика в сфере конфиденциальности и персональных данных",
            "Германия. Новости",
        ],  # 3 segments
        "comments": [
            "Польди этот тот человек,который в сборной играл лучше чем в клубах ",
            '"Я прошел путь от двухлетнего поляка до чемпиона мира в этой футболке',
            "Ждал пока Тимощук со сборной уйдет)",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "UA",  # if obvious: DE, CH, AT
    },
    "https://ukbdnews.com/2020/08/23646/": {
        "file": "ukbdnews.com.23646.html",
        "author": "",
        "title": "এমপির ভাইকে নিজ বাড়ির সামনেই কুপিয়ে হত্যা",
        "date": "2020-08-29",
        "description": "কুষ্টিয়া-১ (দৌলতপুর) আসনের সংসদ সদস্য (এমপি) অ্যাডভোকেট আ ক ম বিস্তারিত",
        "categories": [],
        "tags": [],
        "with": ["কুষ্টিয়া-১ (দৌলতপুর) আসনের সংসদ সদস্য (এমপি) অ্যাডভোকেট", "আজ শনিবার (২৯ আগস্ট) সকাল সাড়ে ৭টার"],
        "without": ["করোনায় আরও ৩২ জনের মৃত্যু, নতুন শনাক্ত ২১৩১", "ইভ্যালির সিইও রাসেলের", " আগস্ট ২৯"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20120611024252/http://www.he.xinhuanet.com/news/2012-06/04/content_25340717.htm": {
        "file": "archive.org.he.xinhuanet.com.25340717.html",
        "author": "",
        "title": "话剧《约定无期限》河北各市巡演结束 ",
        "date": "2012-06-04",
        "description": "",
        "categories": [],
        "tags": [],
        "with": [
            "一个约定，信守15年，感人至深；一段真情，延续15年",
            "秦皇岛、承德、张家口等10个设区市演出(此前已在保定市演出多场)，引起强烈反响。",
            "如今，向河北农大果树93(01)班毕业生群体学习的热潮正在全省各地深入开展。廊坊以巡演为",
        ],  # 3 segments
        "without": ["copyright (c) 2000", "ICP证010042号", "河北探索农村劳动力就地就近转移培训"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://redtri.com/best-jokes-for-kids/slide/1": {
        "file": "redtri.com.jokes.html",
        "author": "Amber Guetebier  Shares",
        "title": "Here Comes the Pun: 265 Hilarious Jokes for Kids",
        "date": "2020-11-03",
        "description": "Encourage your kids to get punny with these kid-approved quips that require little to no explanation from parents. Whether it&#039;s a joke a day for the kids, lunchbox jokes for every day or clean jokes to tell to kids,  just don&#039;t be surprised when the comedy sketch goes beyond today! Scroll down for silly jokes and corny jokes, many of which have been sent to us by kid-readers (like you!).",
        "categories": [],
        "tags": [],
        "with": [
            "37. What did one volcano say to the other?",
            " You look for fresh prints.",
            "Kids are natural comedians so why not encourage",
        ],  # 3 segments
        "without": ["more stories you may have missed", "COMPANY INFO", "AS SEEN IN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.fifplay.com/fifa-21-game-settings/": {
        "file": "fifplay.com.settings.html",
        "author": "",
        "title": "FIFA 21 Game Settings",
        "date": "",
        "description": "FIFA 21 Game Settings guide and instructions.",
        "categories": [],
        "tags": [],
        "with": [
            "You are able to customise and adjust the settings",
            "Your Default Game Lanaguage",
            "By setting this to Default, attributes are",
            "CPU GAMEPLAY CUSTOMISATION",
        ],  # 3 segments
        "without": ["FIFA 21 Camera Settings", "Post Your Comments", "Shortcuts"],  # 3 segments
        "comments": ["Please i want you to teach me how to start"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.duengebehoerde-niedersachsen.de/duengebehoerde/news/38853_Sperrfristende_01._Februar_-_Rechtliche_Hinweise_zur_N-D%C3%BCngung": {
        "file": "duengebehoerde-niedersachsen.de-Sperrfristen.html",
        "author": "Jelko Djuren und Jutta Klaukien",
        "title": "Sperrfristende 01. Februar - Rechtliche Hinweise zur N-Düngung",
        "date": "",
        "with": [
            "und damit auch mit Wirtschaftsdünger",
            ". Die Regelung gilt für Grünland und",
            "Aufgrund EU-Vorgaben wurde die Auslegung",
        ],  # 3 segments
        "without": [
            "überschwemmte Böden: Düngung verboten",
            "Mehr zum Thema",
            "Frost: Der Boden muss am Tag des Aufbringens völlig",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.careelite.de/flaechenverbrauch-fuer-fleisch/": {
        "file": "careelite.de-flaechenverbrauch.html",
        "author": "Christoph Schulz",
        "title": "Flächenverbrauch für Fleisch – Warum wir ohne Tierprodukte nur 1/4 aller Ackerflächen bräuchten",
        "date": "2022-01-21",
        "with": [
            "Du willst mehr über den Flächenverbrauch für Fleisch,",
            "dessen Entwicklung vermitteln:",
            "Eine bemerkenswerte Statistik macht besonders",
        ],  # 3 segments
        "without": ["Quellenangaben:", "richtig! Die Aufmerksamkeit", "NEUESTE BEITRÄGE."],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bund-naturschutz.de/pressemitteilungen/habeck-besuch-in-muenchen-windkraft-in-bayern-kann-nur-ohne-10-h-in-fahrt-gebracht-werden": {
        "file": "bund-naturschutz.de-habeck.html",
        "author": "",
        "title": "HABECK IN MÜNCHEN - WINDKRAFT IN BAYERN GEHT NUR OHNE 10H",
        "date": "2022-01-20",
        "with": [
            "dass das Gespräch zwischen",
            "Wir appellieren an die Ampelkoalition, dies",
            "Bekämpfung der Klimakrise verlieren",
        ],  # 3 segments
        "without": ["Downloads", "Energiewende: BN stellt fünf Kernforderungen", "Foto: Christof Stache"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bfn.de/pressemitteilungen/allervielfalt-verden-bringt-natur-die-aller-zurueck": {
        "file": "bfn.de-verden.html",
        "author": "",
        "title": "„AllerVielfalt Verden“ bringt Natur an die Aller zurück",
        "date": "2022-01-13",
        "with": [
            "5,1 Millionen Euro für die erste Förderphase",
            "Interessen von Landwirtschaft und",
            "einer gemeinsamen Initiative von",
        ],  # 3 segments
        "without": [
            "Weiterführende Informationen",
            "Das Projektgebiet an der Aller",
            "Bundesprogramm „Blaues Band Deutschland“",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.lbv.de/news/details/lebenszeichen-von-bavaria-nach-zwei-monaten-funkstille/": {
        "file": "lbv.de-Bavaria.html",
        "author": "",
        "title": "Lebenszeichen von Bavaria nach zwei Monaten Funkstille",
        "date": "2022-01-21",
        "with": ["November ausgefallener Sender", "Ladestand von drei Prozent", "der GPS-Daten im Gästebuch"],  # 3 segments
        "without": ["Online-Fangemeinde war beunruhig", "zum Naturschutz in Bayern", "LBV-HOCHSCHULGRUPPEN:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.waldwissen.net/de/lernen-und-vermitteln/der-hollaenderholzhandel": {
        "file": "waldwiesen.net-holländerholzhandel.html",
        "author": "Joachim Hamberger",
        "title": "Der Holländerholzhandel",
        "date": "2022-01-21",
        "with": [
            "Heute längst vergessen, war der Holzhandel",
            "Vom 17. bis ins 19. Jahrhundert war der Begriff ",
            "Drittländer eintreffen. Auch der russische",
        ],  # 3 segments
        "without": [
            "Originalartikel",
            "Lernen und Vermitteln",
            "Wissenstransfer, Öffentlichkeitsarbeit, Waldpädagogik",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://neubau.wsl.ch/de/index.html": {
        "file": "wsl.ch-neubeau.html",
        "author": "",
        "title": "Projektwettbewerb Neubau Werkstattgebäude WSL Birmensdorf",
        "date": "2022-01-17",
        "with": ["in der Grundlagenforschung tätig und stellt"],  # 3 segments
        "without": ["Schachbrett"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE/CH",  # if obvious: DE, CH, AT
    },
    "https://www.eawag.ch/de/news-agenda/news-plattform/news/auf-das-erste-elektron-kommt-es-an/": {
        "file": "eawag.ch-elektron.html",
        "author": "Andri Bryner",
        "title": "Auf das erste Elektron kommt es an",
        "date": "2022-01-12",
        "with": [
            "Reduktionsraten schwanken stark",
            "Meret Aeppli, die Erstautorin der Studie",
            "Die Studie beschreibt nur einen kleinen",
        ],  # 3 segments
        "without": [
            "Kontakt an ETHZ",
            "Rund um Wurzeln, die Sauerstoff in den Boden bringen, lagert sich",
            "Originalpublikation",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.slf.ch/de/lawinenbulletin-und-schneesituation/wochen-und-winterberichte/2021/22/wochenbericht-14-20-januar-2022.html": {
        "file": "slf.ch-lawinensituation.html",
        "author": "",
        "title": "Schwache Profile – günstige Lawinensituation",
        "date": "2022-01-14",
        "with": [
            "dieser Satz fand sich mehrfach in",
            "In den Alpen zeigte sich dies mit wiederholt",
            "Diese führte zu einer deutlichen Abkühlung",
        ],  # 3 segments
        "without": [
            "Die grösste Lawine dieser Berichtsperiode",
            "Oberflächenreif in einem Nordhang",
            "Lawinenbulletins dieser Zeitperiode im Überblick.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.vogelwarte.ch/de/vogelwarte/news/avinews/dezember-2021/zielartenfoerderung-im-lichten-wald-dank-aktionsplan": {
        "file": "vogelwarte.ch-aktionsplan.html",
        "author": "",
        "title": "Zielartenförderung im lichten Wald dank Aktionsplan",
        "date": "",
        "with": [
            "mikroklimatische Bedingungen in der Strauch",
            "BAFU, einen Aktionsplan «Zielartenförderung",
            " Lebensraumförderung mit der spezifischen Artenförderung",
        ],  # 3 segments
        "without": [
            "und der Hirschkäfer (Lucanus cervus)",
            "beinhaltet auch die lichten Wälder, welche",
            "Kastanienselven beispielsweise",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "xhttps://www.zoo-berlin.de/de/aktuelles/alle-news/artikel/der-turm-der-wuensche": {
        "file": "zoo-berlin.de-turm.html",
        "author": "",
        "title": "Der Turm der Wünsche",
        "date": "2022-01-21",
        "with": [
            "Zukünftig wird man bei der Ein- oder Ausfahrt",
            "mehr über ihren Lebensraum im ",
            " pearlman Erlebnisarchitektur geplant.",
        ],  # 3 segments
        "without": ["Zurück zur Übersicht", "PRESSE-MITTEILUNG", "Jetzt Newsletter abonnieren"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.selbstversorger.de/eier-legen-huehner/": {
        "file": "selbstversorger.de-Huhn.html",
        "author": "",
        "title": "Ab wann legen und wie lange legen Hühner Eier",
        "date": "",
        "with": [
            "Mit Sicherheit kennen Sie das Sprichwort: “Ich wollt’ ich",
            "Ab wann legen Hühner Eier?",
            "Die jeweilige Hühnerrasse spielt in Bezug",
        ],  # 3 segments
        "without": [
            "Atme tief durch bevor du Michaela",
            "20 Zeichen, dass ein Herzinfarkt",
            "Mann schenkt seiner Freundin eine",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.wochenblatt.com/landwirtschaft/agrarpolitik/heinen-esser-offen-fuer-existenzgruendungspraemie-12810183.html": {
        "file": "wochenblatt.com-Heinen-Essen.html",
        "author": "Patrick Otte",
        "title": "Heinen-Esser offen für Existenzgründungsprämie",
        "date": "2022-02-21",
        "with": [
            "Die Jugendverbände der Landwirtschaft in",
            "Die Jugendverbände der Landwirtschaft in",
            "besprach sie Fragen zur erwartenden",
        ],  # 3 segments
        "without": ["Vertreterinnen und Vertreter der", "Jugendverbände fordern", "Die Jugendverbände der"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://oekolandbau.de/service/nachrichten/detailansicht/tag-des-zweinutzungshuhns-am-22-januar/": {
        "file": "oekolaundbau.de-zweinutzungshuhns.html",
        "author": "",
        "title": "Tag des Zweinutzungshuhns am 22. Januar",
        "date": "2022-01-21",
        "with": [
            "einem echten Zweinutzungstier? Die Ökotierzucht",
            "wurden. Hier in Deutschland",
            "halten inzwischen ÖTZ-Tiere",
        ],  # 3 segments
        "without": ["Thema auf Oekolandbau.de", "Alternativen zum Kükentöten", "Foto: ÖTZ"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dlg.org/de/landwirtschaft/presse/aktuell#!/news/dlg-hat-wilhelm-rimpau-preis-ausgeschrieben": {
        "file": "dlg.org-Preis.html",
        "author": "",
        "title": "DLG hat „Wilhelm-Rimpau-Preis“ ausgeschrieben",
        "date": "2022-01-20",
        "with": [
            "Auszeichnung für innovative und praxisnahe",
            "Fakultät deutschsprachiger Universitäten",
            "nächsten DLG-Feldtage, die",
        ],  # 3 segments
        "without": ["Fotoarchiv", "Servicebereich Kommunikation", "14.72 KB"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.zamg.ac.at/cms/de/klima/news/histalp/histalp-oesterreich-jahresbericht-2021": {
        "file": "zamg.ac.at-Jahresbericht.html",
        "author": "",
        "title": "HISTALP Österreich Jahresbericht 2021",
        "date": "2022-01-21",
        "with": [
            "zurückreichen und besonderen",
            "Messwerte der Gegenwart mit",
            "nternationale Klimadatensammlung",
        ],  # 3 segments
        "without": ["Die ZAMG ist eine", "Auskunft über vergangenes", "Berechnung der erwartbaren"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.handwerksblatt.de/themen-specials/coronaschutz-im-betrieb/2g-3g-was-gilt-beim-friseurbesuch": {
        "file": "handwerksblatt.de-Friseurbesuch.html",
        "author": "Kirsten Freund",
        "title": "3G, 2G oder 2G Plus: Was gilt jetzt beim Friseurbesuch?",
        "date": "2022-01-01",
        "with": [
            "Corona und die neue Omikron-Variante",
            "Besuch beim Friseur oder der Kosmetikerin",
            "bis einschließlich 15 Jahren brauchen",
        ],  # 3 segments
        "without": ["Alle Angaben ohne Gewähr", "Quelle: Landesregierung", "DHB jetzt auch digital!"],  # 3 segments
        "comments": [
            "Servus, Bayern hat eine Hospitalisierungsrate",
            "Sehr geehrte Frau Singer",
            "Frisörbesuch mit 3G möglich?",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.deutsche-handwerks-zeitung.de/eigentumsvorbehalt-das-sollten-kaeufer-und-verkaeufer-wissen-168384/": {
        "file": "deutsche-handwerkszeitung.de-eigentumsvorbehalt.html",
        "author": "Tobias Kuske",
        "title": "Eigentumsvorbehalt: Das sollten Käufer und Verkäufer wissen",
        "date": "2022-01-21",
        "with": [
            "übergibt der Verkäufer dem Käufer die",
            "der Käufer dem Verkäufer zu, das Eigentum",
            "Lieferungen beglichen wurden. Ein",
        ],  # 3 segments
        "without": [
            "Sie werktäglich, was erfolgreiche",
            "Stapel mit Mauerziegeln: Wenn ein",
            "WEITERE BEITRÄGE ZU",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.handwerk-magazin.de/cyber-angriffe-20-prozent-vom-it-budget-in-die-it-sicherheit-stecken-250901/": {
        "file": "handwerk-magazin.de-Angriffe.html",
        "author": "Irmela Schwab",
        "title": "Cyber-Angriffe: 20 Prozent vom IT-Budget in die IT-Sicherheit stecken!",
        "date": "2022-01-21",
        "with": [
            "Erpressungsmethoden wie Ransomeware fest.“",
            "gesichtet, das sind durchschnittlich",
            "weshalb das Update noch nicht umgesetzt wurde",
        ],  # 3 segments
        "without": [
            "Steuern Sie Ihren Kundendienst",
            "Mission Mittelstand - digitales",
            "Cyber-Attacken nehmen weiter zu.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.zdh.de/presse/veroeffentlichungen/pressemitteilungen/kfw-foerderungsstopp-ist-klimapolitisch-fatales-signal/": {
        "file": "zdh.de-foerderungsstopp.html",
        "author": "",
        "title": "KfW-Förderungsstopp ist klimapolitisch fatales Signal",
        "date": "2022-01-25",
        "with": [
            "und nicht akzeptabel ist, dass",
            " Bundesregierung aufgefordert, verlässliche",
            "CO2-Minderungs- und Klimaschutzziele so wichtig",
        ],  # 3 segments
        "without": ["Schlagworte", "Foto: unsplash/Bill Mead", "Energiewende"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.selbst.de/wurmkiste-39572.html": {
        "file": "selbst.de-wurmkiste.html",
        "author": "",
        "title": "Wurmkiste selber bauen",
        "date": "2022-01-22",
        "with": [
            "kompostieren. In einer Wurmkiste",
            "foetida Kartoffelschalen oder Kaffeesatz",
            "Nachdem der Abfall in der obersten",
        ],  # 3 segments
        "without": ["Selbst.de empfiehlt", "Mehr zum Thema", "Einfach"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.werkzeugforum.de/heizjacken-von-bosch/": {
        "file": "werkzeugforum.de-heizjacke.html",
        "author": "",
        "title": "Heizjacken von Bosch",
        "date": "2022-01-26",
        "with": [
            "Profis binnen drei Minuten auf „Betriebstemperatur“",
            "gebückter Haltung effizient gewärmt. Die Jacke",
            "jeweils in den Unisex-Größen",
        ],  # 3 segments
        "without": ["Mauerschlitze fräsen", "Eine Antwort schreiben", "Ausbildungsvergütung: Was"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.holzwerken.net/blog/dominik-ricker/perfekte-schnitte-nach-riss-an-der-kreissaege": {
        "file": "holzwerken.net-Kreissaege.html",
        "author": "Dominik Ricker",
        "title": "Perfekte Schnitte nach Riss an der Kreissaege",
        "date": "2022-01-21",
        "with": [
            "Schnitten. Doch es geht auch einfacher...",
            "Ein schmales Reststück wird am Parallelanschlag",
            "Bei dünneren Plattenwerkstoffen",
        ],  # 3 segments
        "without": [
            "Das könnte Sie auch interessieren!",
            "Nodus-Knoten, Besteckschrank",
            "Sie sind aktuell nicht eingeloggt.",
        ],  # 3 segments
        "comments": [
            "Du bist der Beste!",
            "super Idee. Hatte auch schon des",
            "Danke Dominik, dieser Tipp",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://selbermachen.de/garten/gartenhaus-selber-bauen/wohngewaechshaus-selber-bauen": {
        "file": "selbermachen.de-wohngewaechshaus.html",
        "author": "",
        "title": "Wohngewächshaus selber bauen",
        "date": "2022-01-15",
        "with": [
            "feuchteres Klima, als in unseren",
            "Konstruiert nach dem Prinzip der thermischen",
            "Die Traufenprofile werden mit Hilfe",
        ],  # 3 segments
        "without": ["Mehr lesen über:", "Fahrradunterstand selber", "Hochbeet selber bauen -"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.mein-schoener-garten.de/news/3-profi-tipps-rund-um-die-topinambur-ernte-48412": {
        "file": "mein-schoener-garten.de-topinabur.html",
        "author": "Kathrin Hofmeister",
        "title": "Topinambur ernten: 3 Profi-Tipps",
        "date": "2022-01-26",
        "with": [
            "Winter Gemüse frisch aus dem Garten",
            "Pflanze sind nahrhaft, ballaststoffreich und",
            "Der Boden ist gefroren. Dagegen hilft",
        ],  # 3 segments
        "without": ["Empfehlungen aus dem", "Verwandte Artikel", "Rüben: Schätze aus dem Untergrund"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.haus.de/bauen/vorsatzschalung-33656": {
        "file": "haus.de-Vorsatzschallung.html",
        "author": "André Borbe",
        "title": "Was ist eine Vorsatzschalung und was bringt sie?",
        "date": "2022-01-25",
        "with": [
            "vor allem in der Trockenbauweise",
            "Zwischen den beiden Elementen",
            "Schallschutz sorgen. Bei der direkt befestigten",
        ],  # 3 segments
        "without": [
            "HÄUFIG GESTELLTE FRAGEN",
            "Wirkt eine Vorsatzschalung als Dampfbremse?",
            "Schallschutz sowie die Wärmeisolierung.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.gartenjournal.net/zaubernuss-im-winter": {
        "file": "gartenjournal.net-Zaubernuss.html",
        "author": "Ursula Eggers",
        "title": "Wie pflege ich meine Zaubernuss im Winter?",
        "date": "",
        "with": [
            "filigrane Blüten mit bis zu 4 cm",
            "bevor der Wurzelballen austrocknet",
            "keine besondere Winterpflege nötig",
        ],  # 3 segments
        "without": ["Hier weiterlesen", "Wie groß wird die", "Lesen Sie auch"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.houzz.de/magazin/best-of-houzz-2022-das-sind-die-beliebtesten-projekte-auf-houzz-stsetivw-vs~157401545": {
        "file": "houzz.de-Projekte.html",
        "author": "Houzz Deutschland",
        "title": "Best of Houzz 2022: Das sind die beliebtesten Projekte auf Houzz",
        "date": "2022-01.26",
        "with": ["Projekte, die bei den Millionen", "zu den Projekten, die", "Auszügen hat es der Community"],  # 3 segments
        "without": [
            "Verraten Sie gerne in den Kommentaren:",
            "Ähnliche Artikel lesen",
            "Nutzer mochten auch folgende",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.homify.de/diy/20546/wie-man-eine-runde-tischdecke-in-nur-7-schritten-herstellt": {
        "file": "homify.de-Tischdecke.html",
        "author": "Robert Stitz",
        "title": "Wie man eine runde Tischdecke in nur 7 Schritten herstellt",
        "date": "2022-01-10",
        "with": [
            "Unabhängig von Größe und Stil kannst du",
            "den Durchmesser (das ist das Maß,",
            "wie du eine runde Tischdecke",
        ],  # 3 segments
        "without": ["Kommentare", "Die Seedball Manufaktur", "Ernährungsworkshop"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bauemotion.de/magazin/schneeraeumpflicht-das-sollten-sie-wissen/15002914/": {
        "file": "bauemotion.de-schneereampflicht.html",
        "author": "",
        "title": "Schneeräumpflicht: Das sollten Sie wissen",
        "date": "",
        "with": [
            "Hausbesitzer sind gesetzlich dazu",
            "Wenn sich ein Passant auf einem",
            "Fitnesstraining an der frischen Luft.",
        ],  # 3 segments
        "without": [
            "Meist gelesene Artikel",
            "Schneeräumpflicht - was man darüber",
            "Dieser Artikel wird Ihnen präsentiert",
        ],  # 3 segments
        "comments": [
            "Vielen Dank, sehr informative Tipps!",
            "das ist eigentlich ganz einfach.",
            "Schneebeseitigung beginnt, um",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://hausinfo.ch/de/wohnen/wohnen-leben/angenehmes-raumklima/kondenswasser.html": {
        "file": "hausinfo.ch-kondenswasser.html",
        "author": "hausinfo",
        "title": "Kondenswasser am Fenster verhindern",
        "date": "2021-12-15",
        "with": [
            "Fenstern nicht durch überstellte Fensterbänke",
            "Dies schlägt sich aber in",
            "Luftfeuchtigkeit im Raum sorgen",
        ],  # 3 segments
        "without": ["Kondenswasser an den Fensterrändern", "Angenehmes Raumklima", "Gesund wohnen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.outdoor-magazin.com/outdoor-szene/vanlife-in-schweden/": {
        "file": "outdoor-magazin.com-vanlife.html",
        "author": "",
        "title": "Skandinavien im Wohnmobil erleben",
        "date": "2022-01-06",
        "with": ["Der Traum vieler Vanlife- und", "Teilnehmern gilt die 2G-Regel", "Schweden unzählige legale"],  # 3 segments
        "without": ["Das Wasser aus Bächen und Flüssen", "Die Alstadt Stockholms", "Weitere Tourentipps"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.alpin.de/sicher-am-berg/skitouren/51490/artikel_quantum-free-asolo-factory-130-das-beste-aus-der-touring-und-der-freeride-welt-vereint.html": {
        "file": "alpin.de-freeride.html",
        "author": "",
        "title": "Quantum Free Asolo Factory 130: Das Beste aus der Touring- und der Freeride-Welt vereint",
        "date": "2022-01-21",
        "with": ["Spitzenklasse, der das Beste", "Die zweiteilige X Dual", "Der exklusive IF Touring"],  # 3 segments
        "without": ["Quantum Free Asolo Factory 130:", "Besonders komfortable Innenschuhe", "Thema Skitouren:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bike-magazin.de/mtb_news/szene_news/strava-update-poi-bei-routen": {
        "file": "bike-magazin.de-strava.html",
        "author": "Stefan Loibl",
        "title": "Strava-Karten ab sofort mit mehr Infos",
        "date": "2022-01-26",
        "with": [
            "Mitte Januar 2022 hat Strava ein",
            "Durch die Kombination der Datenbank",
            "Unterwegs kann man spontan",
        ],  # 3 segments
        "without": [
            "Ob Supermarkt, Pumptrack oder",
            "Lesen Sie das BIKE Magazin",
            "Empfehlungen aus der Redaktion",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.mtb-news.de/news/reifen-tubeless-montieren/": {
        "file": "mtb-news.de-tubeless.html",
        "author": "Stefanus Stahl",
        "title": "MTB-Reifen auf Tubeless umrüsten Schritt für Schritt: so einfach montierst du Tubeless-Reifen",
        "date": "2022-01-26",
        "with": [
            "gemacht! Schlauchlose Reifen",
            "Dieser muss luftdicht abschliessen",
            "Systeme bieten eine höhere",
        ],  # 3 segments
        "without": ["Mehr zum Thema", "120 Kommentare", "Best of Test: Die besten Bikes 2022"],  # 3 segments
        "comments": [
            "und nachhaltiger als mit CO2-Patronen.",
            "und nachhaltiger als mit CO2-Patronen.",
            "und nachhaltiger als mit CO2-Patronen.",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tour-magazin.de/profisport/news/nach-unfall-auf-intensivstation-bernal-kaempft-um-karriere/a51346.html": {
        "file": "tour-magazin.de-unfall.html",
        "author": "",
        "title": "Nach Unfall auf Intensivstation: Bernal kämpft um Karriere",
        "date": "2022-01-25",
        "with": [
            "Sieger der Tour de France",
            "Twitter und reihte sich damit",
            "Der Unfall erinnert an den schweren",
        ],  # 3 segments
        "without": ["Das könnte Sie auch interessieren", "Branchen News", "Egan Bernal verlängert bis"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.gipfelbuch.ch/outdoornews/detail/id/718": {
        "file": "gipfelbuch.ch-hochaufloesung.html",
        "author": "",
        "title": "HOCHAUFLÖSENDE SCHNEEKARTEN AUF GIPFELBUCH.CH",
        "date": "2022-01-14",
        "with": [
            "Um einen ersten Eindruck zu erhalten",
            "hilft uns in den Satellitendaten",
            " Zusammengefasst berücksichtigen wir in",
        ],  # 3 segments
        "without": [
            "Abbildung: Vergleich auf dem Aletschgletscher",
            "FRAGEN AN DEN AUTOR",
            "Farblich codierte Schneehöhendarstellung",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.baechli-bergsport.ch/Blog/Einblick-in-die-Praxis-und-Theorie-von-Lawinen-De-9-9-9-9-1.htm": {
        "file": "baechli-bergsport.ch-lawinen.html",
        "author": "Janic Cathomen",
        "title": "EINBLICK IN DIE PRAXIS UND THEORIE VON LAWINEN",
        "date": "2021-12-01",
        "with": [
            "wir bestens vorbereitet sind,",
            "Knie in die Hüfte bis in den",
            "langsam sein und im Nachhinein",
        ],  # 3 segments
        "without": [
            "Abbildung 4: klassische Schwachschicht.",
            "TEILE DIESEN BEITRAG AUF",
            "Vorgehensweise für grosse Ereignisse",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.lacrux.com/klettern/mammut-nimmt-adam-ondra-unter-vertrag/": {
        "file": "lacrux.com-mammut.html",
        "author": "Redaktion",
        "title": "Mammut nimmt Adam Ondra unter Vertrag",
        "date": "2022-01-25",
        "with": [
            "Im von Adam Ondra veröffentlichten Video",
            "Black Diamond bald den Rücken zu und wechselt",
            "kurze Sequenzen aneinandergereiht",
        ],  # 3 segments
        "without": ["Gefällt dir unser Klettermagazin?", "Das ist die deutsche", "Wetter Chironico"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.sac-cas.ch/de/umwelt/schneesport-mit-ruecksicht-auf-wildtiere-35334/": {
        "file": "sac-cas.ch-schneesport.html",
        "author": "",
        "title": "Schneesport mit Rücksicht auf Wildtiere Verhaltenstipps für einen naturverträglichen Schneesport",
        "date": "2022-01-25",
        "with": [
            " du schon einmal durch Tiefschnee gestapft bist",
            "Beachte Wildruhezonen und Wildschutzgebiete:",
            "sowie die Übernachtung gehören",
        ],  # 3 segments
        "without": ["Verwandte Links", "Skitour im (Voll)Mondschein", "Alpentiere im Winter - Tiertafeln"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.bergsteigen.com/produkte/skibergestiegen-schnell-und-leicht-mit-den-camp-neuheiten/": {
        "file": "bergsteigen.com-skibergsteigen.html",
        "author": "",
        "title": "SKIBERGSTEIGEN: SCHNELL UND LEICHT MIT DEN C.A.M.P. - NEUHEITEN",
        "date": "2022-01-14",
        "with": [
            "Fixer Aluminiumstock",
            "ambitionierte Skibergsteiger, die",
            " X-Press-Hauptskihalter mit innovativem",
        ],  # 3 segments
        "without": ["KOMMENTARE", "KOMMENDE TERMINE", "One Love – Babsi Zangerl und Jacopo Larcher"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://mluk.brandenburg.de/mluk/de/aktuelles/presseinformationen/detail/~02-01-2022-land-zahlte-rund-1-4-millionen-euro-erlegungspraemie-fuer-wildschweine-im-jagdjahr-202020#": {
        "file": "mluk.brandenburg.de-erlegungspermie.html",
        "author": "",
        "title": "Land zahlte rund 1,4 Millionen Euro Erlegungsprämie für Wildschweine im Jagdjahr 2020/2021",
        "date": "2022-01-02",
        "with": [
            "Rückblickend wurde die allgemeine Erlegungsprämie",
            "Schwarzwild lag sowohl die Zahl",
            "Auszahlung der Bachenprämie müssen bis zum 30. April",
        ],  # 3 segments
        "without": [
            "Informationen zur ASP und zur Bachenprämie",
            "Weiterführende Informationen",
            "Weiterführende Informationen",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.jagderleben.de/news/waldwege-unrechtsmaessig-gesperrt-polizei-ermittelt-wegen-noetigung-713266": {
        "file": "jagdleben.de-waldwege.html",
        "author": "Kathrin Führes",
        "title": "Waldwege unrechtsmäßig gesperrt: Polizei ermittelt wegen Nötigung",
        "date": "2022-01-26",
        "with": ["Landwirte und Eigentümer werden so", "Hinweise unter der"],  # 3 segments
        "without": ["Wer die Äste immer wieder auf", "Kommentieren Sie", "angegriffen: Polizei"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.jaegermagazin.de/jagd-aktuell/news-fuer-jaeger/suedtirol-woelfe-toeten-hund-und-bedrohen-besitzer/": {
        "file": "jaegermagazin.de-südtirol.html",
        "author": "Jon Nitz",
        "title": "Südtirol: Wölfe töten Hund und bedrohen Besitzer",
        "date": "2022-01-24",
        "with": [
            "Woche ereignete sich in Südtirol eine",
            "Folgaria gemacht haben. Der",
            "Als sich die Wölfe immer noch",
        ],  # 3 segments
        "without": ["Hundemeute oder Solojäger?", "Nutria bejagen und verwerten", "Neuentdeckung: Die wahren"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://wildundhund.de/bonn-un-konvention-veroeffentlicht-empfehlungen-zur-vogelgrippe-und-zum-umgang-mit-wildvoegeln/": {
        "file": "wildundhund.de-bonn.html",
        "author": "",
        "title": "Bonn: UN-Konvention veröffentlicht Empfehlungen zur Vogelgrippe und zum Umgang mit Wildvögeln",
        "date": "2022-01-26",
        "with": [
            "Arbeitsgruppe zur Vogelgrippe und zu",
            "Die CMS stellt fest, dass",
            "ungefährlichen Vogelgrippe festzustellen.",
        ],  # 3 segments
        "without": ["Russland: Erstmalige Infektion", "VERWANDTE ARTIKEL", "NOCH MEHR WILD UND HUND"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://djz.de/amoklauf-in-heidelberg-rufe-nach-schneller-aufklaerung/": {
        "file": "djz.de-amoklauf.html",
        "author": "",
        "title": "AMOKLAUF IN HEIDELBERG: RUFE NACH SCHNELLER AUFKLÄRUNG",
        "date": "2022-01-25",
        "with": [
            "einer Meldung von heute.",
            "FWR fordere eine schnelle und umfassende",
            "und Europa verhindern.",
        ],  # 3 segments
        "without": [
            "DJV-Verbandsbericht veröffentlicht",
            "Vorheriger Artikel",
            "Immer mehr Wildschweine in Köln",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.jagdverband.de/wir-sind-tief-erschuettert": {
        "file": "jagdverband.de-erschuettert.html",
        "author": "",
        "title": '"Wir sind tief erschüttert"',
        "date": "2022-01-25",
        "with": ["und schnelle Aufklärung", "niemals anonym erworben", "Schätzung von Experten."],  # 3 segments
        "without": ["Wer wir sind und was wir tun", "(Quelle: Fleischmann/Unsplash/DJV)", "Unsere Akademie"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://schweizerjaeger.ch/aktuell/vogeldesjahres2021.html": {
        "file": "schweizerjaeger.ch-steinkauz.html",
        "author": "",
        "title": "Der Steinkauz ist der Vogel des Jahres 2021",
        "date": "2022-01-04",
        "with": ["Botschafter für eine Ökologische", "Mittelland und Jura in fast", "aber auch Hecken und"],  # 3 segments
        "without": [
            "WEITERE INTERESSANTE INFORMATIONEN",
            "Wildtiere & Lebensräume im Wandel der Zeit",
            "Vogel des Jahres 2022: Feldlerche",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.jagd-oesterreich.at/2021/12/14/noe-jagdverband-auf-natur-wildtier-beduerfnisse-achten/": {
        "file": "jagdoesterreich.at-Parkplätze.html",
        "author": "",
        "title": "NÖ Jagdverband appelliert, Wege freizuhalten, vorgesehene Parkplätze zu nützen und grundsätzliche Regeln in der Natur einzuhalten, um Wildtiere zu schonen",
        "date": "2021-12-14",
        "with": [
            "Ruhe, Äsung und Deckung.",
            "Immer auf (Forst-)Straßen oder",
            "Parkverbote missachten und auf Forst-",
        ],  # 3 segments
        "without": ["Ähnliche Beiträge", "NÖ Jagdverband: Auf Natur", "FOLGEN SIE UNS:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://taucher.net/diveinside-boot_tulln_2022_abgesagt-kaz8693": {
        "file": "taucher.net-tauchmesse.html",
        "author": "",
        "title": "Österreichs Tauchmesse in Tulln abgesagt",
        "date": "2022-01-24",
        "with": [
            "Wassersportler in Österreich und",
            "Optimismus und damit die Vorfreude",
            "Sobald weitere Informationen vorliegen",
        ],  # 3 segments
        "without": ["Letzte Artikel", "Norwegen: Orcas und Buckelwale auf Jagd", "Kategorie: News"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.blinker.de/angelmethoden/angeln-allgemein/news/fishing-masters-show-in-rostock-findet-naechstes-jahr-statt/": {
        "file": "blinker.de-Rostock.html",
        "author": "",
        "title": "Fishing Masters Show in Rostock im Mai 2022",
        "date": "2022-01-11",
        "with": [
            "IGA Park alles ums Angeln drehen.",
            "coronabedingten Verschiebungen steht",
            "frischem Räucherfisch und vielen",
        ],  # 3 segments
        "without": ["Das könnte Sie auch interessieren", "Bild: Jahr Media", "Wir erstellen Ihr"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.zoll.de/SharedDocs/Fachmeldungen/Aktuelle-Einzelmeldungen/2021/vst_verkuendung_tabaksteuermodernisierungsgesetz.html": {
        "file": "zoll.de-Tabaksteuer.html",
        "author": "",
        "title": "Verkündung des Tabaksteuermodernisierungsgesetzes",
        "date": "2021-10-18",
        "with": ["für Substitute für Tabakwaren.", "1. Januar 2023", "Beteiligte, die erstmals"],  # 3 segments
        "without": ["(Fachthemen)", "Wie gefällt Ihnen unsere", "Weitere Informationen", "PDF"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://de.motor1.com/news/545242/bmw-3er-touring-2022-erwischt/": {
        "file": "motor1.de-erwischt.html",
        "author": "Adrian Padeanu",
        "title": "BMW 3er Touring Facelift (2022) zum ersten Mal erwischt",
        "date": "2021-11-03",
        "with": ["eine der beliebtesten", "3er-Facelifts mit den", "werden, die auf der in China,"],  # 3 segments
        "without": ["Die besten Leasing-Deals", "Ein Service von", "Fiat 500 Leasing für 55 Euro"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.autozeitung.de/adblue-diesel-tanken-ratgeber-180301.html": {
        "file": "autozeitung.de-adblue.html",
        "author": "",
        "title": "So wird Adblue richtig angewendet",
        "date": "2021-11-02",
        "with": [
            "Tankstellen: Wo kann man Adblue kaufen?",
            "AdBlue-Tank einfrieren?",
            "Diesel dürfen seitdem statt",
        ],  # 3 segments
        "without": ["Beliebte Marken", "So kommt die", "Hefte testen und 35"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.automobilwoche.de/article/20211103/AGENTURMELDUNGEN/311039909/1276/krach-vor-der-vw-betriebsversammlung-es-knirscht-zwischen-diess-und-aufsichtsraeten": {
        "file": "automobilwoche.de-VW-Betriebsversammlung.html",
        "author": "",
        "title": "Krach vor der VW-Betriebsversammlung:Es knirscht zwischen Diess und Aufsichtsräten ",
        "date": "2021-11-03",
        "with": ["bei VW mehren sich", "VW-Chef Herbert Diess:", "Haussegen hängt schief"],  # 3 segments
        "without": ["Starker Rückgang im Oktober:", "Die neuesten Aufzeichnungen", "Jobs in der Autobranche"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.autohaus.de/nachrichten/autohersteller/skoda-der-lange-weg-zum-strom-2980654": {
        "file": "autohaus.de-skode.html",
        "author": "Peter Maahn",
        "title": "Skoda: Der lange Weg zum Strom",
        "date": "2021-11-03",
        "with": ["immerhin auf Platz drei", "Fuhrparks greifen zu", "Das neue Top-Modell"],  # 3 segments
        "without": ["Skoda: Der lange Weg zum Strom", "Familien-Lösung", "Fahrbericht BMW"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://auto-presse.de/autonews.php?newsid=6486285": {
        "file": "auto-presse.de-minisuv.html",
        "author": "",
        "title": "Japanisches Mini-SUV auf dem Vormarsch",
        "date": "2021-11-05",
        "with": ["wenige Wochen nach", "1,5-Liter-Hybridantrieb", "Mit dem demnächst"],  # 3 segments
        "without": ["Top Meldungen", "Mazda fertigt flexibler", "für dynamische Fortbewegung"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.autonews.ch/?p=31228": {
        "file": "autonews.ch-Tesla.html",
        "author": "",
        "title": "Plant Tesla eine zweite Fabrik in China?",
        "date": "2021-11-05",
        "with": ["wieder Gerüchte zu Tesla", "Gunsten von Qingdao", "aber sicher eine vierte Gigafactory"],  # 3 segments
        "without": ["Volltext-Suche:", "Fahrbericht Ioniq 5 von Hyundai", "Crossback – charmant und mit"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://auto-wirtschaft.ch/news/8950-fur-die-freiheit-auf-radern-campinglosungen-von-sortimo-am-caravan-salon": {
        "file": "auto-wirtschaft.ch-camping.html",
        "author": "",
        "title": "Für die Freiheit auf Rädern – Campinglösungen von Sortimo am Caravan Salon",
        "date": "2021-11-04",
        "with": ["An fünf Messetagen", "Mit dem EQV stand", "Thule-Markise sowie"],  # 3 segments
        "without": ["Sinus 2021: Kinder und", "Immer informiert bleiben", "SHAB-Abfrage"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://auto-motor.at/Hyundai/Tests/Hyundai-Santa-Fe-Plug-in-Test.html": {
        "file": "auto-motor.at-hyundaitest.html",
        "author": "auto-motor.at Redaktion",
        "title": "Hyundai Santa Fe Luxury Line 1,6 T-GDI Plug-in 4WD im Test",
        "date": "2021-11-04",
        "with": ["Santa Fe ist weit", "Ausstattung Sicherheit: 1", "CO2 Ausstoß pro km in"],  # 3 segments
        "without": ["Die neuesten Meldungen", "Der neue SL ist erstmals", "Test verraten wir"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://auto.oe24.at/thema/vw-chef-diess-warnt-vor-tesla-und-golf-aus-china/497533355": {
        "file": "auto.oe24.at-golfchina.html",
        "author": "",
        "title": 'VW-Chef warnt vor Tesla und "Golf aus China"',
        "date": "2021-11-05",
        "with": ["Stammsitz Wolfsburg zu einem", "wieder zum Aushängeschild", "Warnung vor Tesla"],  # 3 segments
        "without": ["Auto kostenlos bewerten", "Mehr Videos", "des ET7 in Europa an."],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://motor.at/zweirad/seat-mo-125-der-elektroroller-im-test/401755605": {
        "file": "motor.at-elektroroller.html",
        "author": "Michael Andrusio",
        "title": "Seat Mo 125: Was kann der Elektroroller mit dem Akku-Trolley?",
        "date": "2021-11-01",
        "with": ["Der (Elektro-)Roller versteht", "Mo 125 auf 95 km/h", "man noch die Förderung"],  # 3 segments
        "without": ["Kommentare gepostet", "motor.at, and", "Bild: Werk/CHRISTIAN HOUDEK"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://bos-fahrzeuge.info/news/Die-Haubenfahrzeuge-der-Nachkriegszeit-Teil-49-223": {
        "file": "bos-fahrzeuge.info-haubenfahrzeuge.html",
        "author": "Klausmartin Friedrich",
        "title": "Die Haubenfahrzeuge der Nachkriegszeit - Teil 49 – Büssing-NAG (Baujahre 1931 – 1945)",
        "date": "2021-11-02",
        "with": ["seine Fahrzeuge fuhren", "und Soldatenräte das Werk", "Trittstufe aus über"],  # 3 segments
        "without": ["Störung bei der Suchfunktion", "Florian Neunkircher...", "von der Feuerlöschpolizei"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.cducsu.de/themen/wirtschaft-und-energie-verkehr-bildung-und-forschung/gruener-wasserstoff-das-schluesselelement-der-energiewende": {
        "file": "cducsu.de-wasserstoff.html",
        "author": "",
        "title": "Grüner Wasserstoff – das Schlüsselelement der Energiewende",
        "date": "2021-11-02",
        "with": ["Mark Helfrich über das gewaltige", "Aktuell befinden wir", "Deutschland einen erheblichen"],  # 3 segments
        "without": ["Biokerosin, Verpackungen", "Quelle: Foto Steven", "Transfer in die Praxis."],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.spdfraktion.de/themen/aydan-oezoguz-vizepraesidentin": {
        "file": "spdfraktion.de-Vizepräsidentin.html",
        "author": "",
        "title": "Aydan Özoğuz wird Vizepräsidentin",
        "date": "2021-10-26",
        "with": [
            "ist zur stellvertretenden Präsidentin",
            "und arbeitete als wissenschaftliche",
            "türkischen Wurzeln am",
        ],  # 3 segments
        "without": ["Arbeitsgruppen", "Bei Fragen und Anregungen", "Foto: DBT/Stella"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.gruene-bundestag.de/themen/klimaschutz/cop26-in-glasgow": {
        "file": "gruene-bundestag.de-COP26.html",
        "author": "",
        "title": "COP26 in Glasgow",
        "date": "2021-11-03",
        "with": ["Es ist höchste Zeit", "Versprechen, ab 2020 jährlich", "Die Initiative der britischen"],  # 3 segments
        "without": ["Andrew Milligan", "Mehr Klimaschutz", "1,5 Grad-Pfad zu kommen."],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.fdpbt.de/beendigung-epidemischen-lage-nationaler-tragweite": {
        "file": "fdpbt.de-epidemischenLage.html",
        "author": "",
        "title": "Beendigung der epidemischen Lage von nationaler Tragweite",
        "date": "2021-10-27",
        "with": ["Lage von nationaler Tragweite", "erste Fraktion gewesen", "Das Konzeptpapier"],  # 3 segments
        "without": ["Mit unserem Newsletter", "Artikel", "Twitter"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.linksfraktion.de/themen/nachrichten/detail/abzocke-wird-als-klimaschutz-verkauft/": {
        "file": "linksfraktion.de-Abzocke.html",
        "author": "Deutschlandfunk",  # nicht sicher
        "title": "»Abzocke wird als Klimaschutz verkauft«",
        "date": "2021-11-02",
        "with": ["der Linken-Vorsitzende", "Aber was wir im Moment", "Unternehmen durch immer"],  # 3 segments
        "without": ["Kein Recht auf Faulheit", "Im Wortlaut von Katja", "Pressemitteilung von"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bund.net/bund-tipps/detail-tipps/tip/unser-tipp-im-november-das-hermelin/": {
        "file": "bund.net-hermlin.html",
        "author": "",
        "title": "Unser Tipp im November: Das Hermelin",
        "date": "2021-11-01",
        "with": ["Beobachtungstipp", "Paarungszeit der Hermeline", "Hermelin ist weit verbreitet"],  # 3 segments
        "without": ["Newsletter erhalten", "iStock.com", "Unser Tipp im Oktober:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.rosalux.de/news/id/45292/wir-waren-fast-40-tage-in-quarantaene?cHash=39ac749d120d127296ab076c203053d3": {
        "file": "rosalux.de-quarantaene.html",
        "author": "Nikolai Huke",
        "title": "«Wir waren fast 40 Tage in Quarantäne» ",
        "date": "2021-10-30",
        "with": ["Wir waren fast 40 Tage in Quarantäne", "Wo sind Sie in die", "Es war nach dem"],  # 3 segments
        "without": ["zum Thema", "Teilen:", "zählt für sie nicht"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.freiheit.org/de/holocaust-ueberlebende-margot-friedlaender-wird-100-jahre": {
        "file": "freiheit.org-überlebende.html",
        "author": "",
        "title": "Holocaust-Überlebende Margot Friedländer wird 100 Jahre",
        "date": "2021-11-05",
        "with": ["Gespräch mit Sabine", "Herzlichen Glückwunsch.", "Als eine der letzten"],  # 3 segments
        "without": ["Meist gelesen", "„Die Eskalation geht", "Die Sorge unter der jüdischen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.hss.de/news/detail/grosse-aufgaben-fuer-die-neue-regierung-news8123/": {
        "file": "hss.de-Regierung.html",
        "author": "Uta Staschewski",
        "title": "Große Aufgaben für die neue Regierung",
        "date": "2021-11-03",
        "with": ["Najla Bouden ist die", "Tunesier landesweit die", "tunesische Bevölkerung durchaus in einer"],  # 3 segments
        "without": ["Naher Osten, Nordafrika", "Bourguiba, Tunis.", "Ahmed Zarrouki, Avenue Hbib"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.kas.de/de/laenderberichte/detail/-/content/kommunalwahlen-in-nordmazedonien": {
        "file": "kas.de-nordmazedonien.html",
        "author": "Daniel Braun, Davor Pasoski",
        "title": "Kommunalwahlen in Nordmazedonien",
        "date": "2021-11-05",
        "with": ["Die Lokalwahlen endeten", "Der Hauptstadt Skopje wird", "Zaev erklärt seinen Rücktritt"],  # 3 segments
        "without": ["Über diese Reihe", "Die Auslandsmitarbeiter vor Ort", "Erdrutschsieg der"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bundesfeuerwehrverband.at/2021/10/20/zentrum-am-berg-offiziell-eroeffnet/": {
        "file": "bundesfeuerwehrverband.at-eröffnet.html",
        "author": "",
        "title": "„Zentrum am Berg“ offiziell eröffnet",
        "date": "2021-10-20",
        "with": ["Mit mehr als vier", "Heinz Faßmann ging auf die", "Würdigung der ÖBFV-Kooperation"],  # 3 segments
        "without": ["Landesverbände", "Aktuelles aus dem ÖBFV", "E-LBD Krugfahrt verstorben"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.berliner-feuerwehr.de/aktuelles/nachrichten/feuerwehr-und-katastrophenschutz-ehrenzeichen-verliehen-3896/": {
        "file": "berliner-feuerwehr.de-Ehrenzeichen.html",
        "author": "",
        "title": "Feuerwehr- und Katastrophenschutz-Ehrenzeichen verliehen",
        "date": "2021-11-05",
        "with": [
            "Ehrenzeichen der Stufe 1",
            "Landesbranddirektor Dr. Karsten Homrighausen",
            "Kameradinnen und Kameraden erhielten",
        ],  # 3 segments
        "without": ["Kameradinnen und Kameraden erhielten", "„Red levens“ - Leben retten", "Zum Seitenanfang"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.thw.de/SharedDocs/Meldungen/DE/Meldungen/national/2021/10/meldung_01_miniserie_frauen_im_thw/meldung_001_startseite_miniserie_frauen_im_thw.html": {
        "file": "thw.de-frauen.html",
        "author": "",
        "title": "Frauen im THW: Vergangenheit, Gegenwart und Zukunft",
        "date": "2021-10-11",
        "with": [
            "heute für Frauen ist und wie",
            "nahezu allen Gesellschaften und Kulturen",
            "„Cool, ‘ne Frau in",
        ],  # 3 segments
        "without": ["Mehr zum Ereignis", "Das THW in Ihrer", "Alle Termine"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.drk.de/presse/pressemitteilungen/meldung/drk-immer-mehr-menschen-wegen-klimawandel-auf-hilfe-angewiesen/": {
        "file": "drk.de-Glasgow.html",
        "author": "",
        "title": "UN-Klimakonferenz in Glasgow - DRK: Immer mehr Menschen wegen Klimawandel auf Hilfe angewiesen",
        "date": "2021-10-28",
        "with": [
            " Hitzewellen ausgesetzt gewesen",
            "Zudem betreibt das DRK",
            "Klimawandel als globale Bedrohung",
        ],  # 3 segments
        "without": ["Jede kleine Spende", "Beitrag teilen", "Diese Seite:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.malteser.de/newsdetails/news/hilfsorganisationen-fordern-von-kuenftiger-bundesregierung-investitionsoffensive-im-bevoelkerungsschutz-1.html": {
        "file": "malteser.de-Bevölkerungsschutz.html",
        "author": "",
        "title": "Hilfsorganisationen fordern von künftiger Bundesregierung Investitionsoffensive im Bevölkerungsschutz",
        "date": "2021-11-04",
        "with": ["in den Bevölkerungsschutz", "behördlichen Strukturen und unter", "Achtung Redaktion:"],  # 3 segments
        "without": ["Zurück zu allen Meldungen", "Foto: Galli/Malteser", "Jetzt helfen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.caritas.de/presse/pressemeldungen-dcv/eva-welskop-deffaa-zur-neuen-caritas-praesidentin-gewaehlt-7fc83ad4-6508-4c79-adba-8a0fee82a677": {
        "file": "caritas.de-Präsidentin.html",
        "author": "Pressestelle des Deutschen Caritasverbandes",
        "title": "Eva Welskop-Deffaa zur neuen Caritas-Präsidentin gewählt",
        "date": "2021-10-13",
        "with": [
            "Digitale Agenda des Verbande",
            "„Die Türen der Kirche von innen aufstoßen“",
            "18 Jahren als Caritas-Präsident",
        ],  # 3 segments
        "without": ["Pressesprecherin des", "Berliner Büro – Pressestelle", "DCV / Oppitz"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bundespolizei.de/Web/DE/04Aktuelles/01Meldungen/2021/10/staendige_aktualisierung_migrationslage.html;jsessionid=51A21717FEF5DF385B5C87C9E5FABD92.2_cid324": {
        "file": "bundespolizei.de-Belarus.html",
        "author": "",
        "title": "Illegale Migration aus Belarus über Polen nach Deutschland: Bereits 9.087 Feststellungen durch die Bundespolizei im laufenden Jahr",
        "date": "2021-11-10",
        "with": ["Die deutsch-polnische Grenze", "Bei Personen, die unerlaubt", "Lesen Sie dazu auch die"],  # 3 segments
        "without": ["Illegale Migration aus Belarus über", "Seite drucken", "So erreichen Sie uns:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://weisser-ring.de/media-news/meldungen/29-10-2021": {
        "file": "weisser-ring.de-Erfolgsgechichte.html",
        "author": "",
        "title": "Erfolgsgeschichte: Zehn Jahre „Tag des Einbruchschutzes“ ",
        "date": "2021-10-29",
        "with": [
            "bundesweiten Einbruchschutzkampagne K-EINBRUCH",
            "seit 2015 kontinuierlich",
            "Wenn Sie Ihr Haus verlassen",
        ],  # 3 segments
        "without": ["Foto: www.k-einbruch.de", "Zurück zur Übersicht", "Startseite"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.diakonie.de/pressemeldungen/vorstellung-der-studie-lebensgefuehl-corona": {
        "file": "diakonie.de-Lebensgefühl.html",
        "author": "",
        "title": "Vorstellung der Studie „Lebensgefühl Corona“",
        "date": "2021-11-10",
        "with": ["Lebensgefühl der Menschen", "ist eine Studie der Evangelischen", "Online-Pressekonferenz"],  # 3 segments
        "without": ["Kathrin Klinkusch", "Hermann Bredehorst", "und Berufe bei der Diakonie"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.jugend-forscht.de/presse/pressemitteilungen/archiv/neuartige-feuerloeschtechnik-alternative-grillkohle-und-redox-flow-technologie-mint-talente-praesentieren-innovative-ideen.html": {
        "file": "jugend-forscht.de-Feuerlöschtechnik.html",
        "author": "",
        "title": "Neuartige Feuerlöschtechnik, alternative Grillkohle und Redox-Flow-Technologie – MINT-Talente präsentieren innovative Ideen",
        "date": "2021-11-02",
        "with": [
            "Preisträger von Deutschlands bekanntestem",
            "Kern-Brennstoff“ ist eine",
            "Geschäftsführender Vorstand",
        ],  # 3 segments
        "without": ["Folge uns", "Video: Mehrwert eines Jugend", "Projektdatenbank"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.awo.org/menschenrechte-achten": {
        "file": "awo.org-Menschenrechte.html",
        "author": "",
        "title": "Menschenrechte achten",
        "date": "2021-11-10",
        "with": ["Gesundheitsversorgung gewähren und", "Geflüchtete brauchen einen", "Dies gelingt durch einen"],  # 3 segments
        "without": ["Aktionstag Suchtberatung.", "Suchtberatung wirkt", "Klassismus in"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tierschutzpartei.de/eine-private-wildvogelauffang-und-auswilderungsstation/": {
        "file": "tierschutzpartei.de-wildvogelauffang.html",
        "author": "",
        "title": "Eine private Wildvogelauffang- und Auswilderungsstation",
        "date": "2021-11-08",
        "with": [
            "Dortmund-Dorstfeld jedoch anders sein",
            "Ewald Ferlemann und sein",
            "Sebastian Everding stellt nach",
        ],  # 3 segments
        "without": ["8. November 2021", "Wildvogelstation Ferlemann in", "Aktuelle Wahlen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.achgut.com/artikel/bericht_zur_coronalage_vom_22.04.2020_worauf_wartet_die_politik": {
        "file": "achgut.com-coronalage.html",
        "author": "Gunter Frank",
        "title": "Bericht zur Coronalage vom 22.04.2020 – worauf wartet die Politik?",
        "date": "2020-04-22",
        "with": [
            "Noch nicht offiziell ist die Zahl",
            "Wie schwer ist die Krankheit",
            "Wahlumfrage, Wahlprognose",
        ],  # 3 segments
        "without": [
            "Sie lesen gern Achgut.com?",
            "schnell & einfach einen Boot-Stick",
            "Sensationelles Urteil für Dieselfahrer",
        ],  # 3 segments
        "comments": ["Toten noch bei 2500, mit", "den wir einer Regierung", "wie wir ohne Maske ab Montag"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tvtoday.de/entertainment/kino-news/will-smith-gestoertes-verhaeltnis-zu-sohn-trey-205331.html": {
        "file": "tvtoday.de-willsmith.html",
        "author": "",
        "title": "Will Smith",
        "date": "",
        "with": ["ältesten Spross im Alter von gerade", "Immer wieder posten", "hat der Familienvater"],  # 3 segments
        "without": ["Das könnte Sie auch", "Kinoprogramm-Suche", "Judy Eddy/WENN.com"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.gelbe-liste.de/produkte/Chininum-salicylicum-D4-DHU-Tabletten_433873": {
        "file": "gelbe-liste.de-chininum.html",
        "author": "Redaktion Gelbe Liste Pharmindex",
        "title": "Chininum salicylicum D4 DHU Tabletten",
        "date": "",
        "with": ["Gebrauchsinformation", "Keine Basisinformation zu diesem", "Hersteller bereitgestellt"],  # 3 segments
        "without": ["Mit der Identa-Suche", "bei Eisenmangel", "Zusatzinfos für"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/italiensicherheit/211322": {
        "file": "auswaertiges-amt.de-Italien.html",
        "author": "",
        "title": "Italien: Reise- und Sicherheitshinweise",
        "date": "2021-11-12",  # letzter Stand
        "with": [
            "kann weiterhin zu Einschränkungen",
            "Beachten Sie die ausführlichen",
            "Besonderheiten in den Regionen",
        ],  # 3 segments
        "without": ["Schlagworte", "Reisewarnungen anlässlich", "Gesellschaftsgruppen. Das Sendeformat"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.swr.de/sport/mehr-sport/volleyball/mtv-stuttgart/stuttgart-ohne-rivers-im-finale-100.html": {
        "file": "swr.de-volleyball.html",
        "author": "Julius Richter ",
        "title": "Hiobsbotschaft für Allianz MTV Stuttgart: Top-Angreiferin Krystal Rivers fällt aus",
        "date": "2021-04-21",
        "with": ['"Was genau sie hat', "Lena Große Scharmann übernimmt", "letzten beiden Finalspielen"],  # 3 segments
        "without": ["Die meistgelesenen Artikel", "Gelten neue Regeln", "Corona-Alarmstufe"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "http://www.finanztreff.de/realtimenews/influencer-und-trading-apps-die-jungen-entdecken-die-boerse/24437626": {
        "file": "finanztreff.de-Influencer.html",
        "author": "David Hutzler",
        "title": "Influencer und Trading Apps: Die Jungen entdecken die Börse",
        "date": "2021-04-28",
        "with": [
            "informieren sich bei Instagram",
            "ausschließlich Einzelaktien ins Depot.",
            "Die Kanäle heißen «Aktien mit Kopf»",
        ],  # 3 segments
        "without": ["Krypto-Hot-Stock mit 60%", "MIDDAY BRIEFING - Unternehmen", "Weitere Nachrichten"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.rtl.de/cms/bericht-bund-und-laender-wollen-lockdown-verlaengern-um-weitere-vier-wochen-4723862.html ": {
        "file": "rtl.de-lockdown.html",
        "author": "",
        "title": "Medienbericht: Bund und Länder planen Lockdown-Verlängerung",
        "date": "2021-03-20",
        "with": [
            "bringt die ganze Impfstrategie",
            'Wie der "Business Insider" unter',
            "TVNOW-DOKU: Das Impfdilemma",
        ],  # 3 segments
        "without": ["Stefan Boness", "Zahlen explodieren - Politik pennt?!", "Wohnen & Haushalt Gutscheine"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tonight.de/unterhaltung/promis/daniela-buechner-danni-und-ennesto-monte-trennen-sich-arschloch_114240.html": {
        "file": "tonight.de-Arschloch.html",
        "author": "Steven Salentin ",
        "title": "„Arschloch“: Danni Büchner und Ennesto Monté trennen sich",
        "date": "2021-03-16",
        "with": [
            "gescheitert“, schrieb der 46-Jährige.",
            "einem halben Jahr",
            "Danni Büchner hat derweil ihren",
        ],  # 3 segments
        "without": ["Foto: Instagram", "Wegen Corona:", "Promis"],  # 3 segments #dort gab es kaum was
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dw.com/fr/la-perte-des-terres-fertiles-et-les-%C3%A9l%C3%A9phants-en-guin%C3%A9e-conakry/a-6533123": {
        "file": "dw.com-elephants.html",
        "author": "Kossivi Tiassou",
        "title": "La perte des terres fertiles et les éléphants en Guinée-Conakry",
        "date": "2011-05-23",
        "with": ["24 milliards de tonnes", "développement, IRD à Dakar.", "d'une étude menée"],  # 3 segments
        "without": ["et vidéos sur le sujet", "terres fertiles et les éléphants en Guinée-Conakry", "Permalien"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://france.attac.org/actus-et-medias/dans-les-medias/article/les-privatisations-sont-au-profit-d-interets-prives-financiers-des": {
        "file": "france.attc.org-privatisations.html",
        "author": "Attac France",
        "title": "« Les privatisations sont au profit d’intérêts privés, financiers, des multinationales et au détriment des salariés et des usagers »",
        "date": "2019-06-13",
        "with": ["Aurélie Trouvé, porte-parole", "partagé pour empêcher", " pour parler du"],  # 3 segments
        "without": ["Dans la même rubrique", "Je fais un don à Attac", "Abandon du projet"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://www.katzen-forum.net/threads/jede-nacht-verliert-pepe-soviel-dreck-aus-dem-fell.230143/": {
        "file": "katzen-forum.net-Pepe.html",
        "author": "Pepemaus",
        "title": "Jede Nacht verliert Pepe soviel Dreck aus dem Fell",
        "date": "2018-09-27",
        "with": ["auf seiner beigefarbenen", '(Vor allem die "Bettelmänner", wenn', "schon seit 5 Uhr draußen"],  # 3 segments
        "without": ["das wirklich Katzenflöhe!?", "Ähnliche Themen", "Katzen Forum"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.arteradio.com/son/61661515/la_voix_des_nuls": {
        "file": "arteradio.com-nuls.html",
        "author": "",
        "title": "La voix des nuls",
        "date": "2019-05-23",
        "with": ["revendication prend chaque", 'jour par les "gilets', "spécialiste du sujet."],  # 3 segments
        "without": ["Vous aimerez aussi", "Tous nos derniers podcasts", "de messagerie est uniquement"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "http://www.womencantalksports.com/top-10-women-talking-sports/": {
        "file": "womencantalksports.com-top10.html",
        "author": "",
        "title": "Top 10 Women Talking Sports",
        "date": "2014-01-22",
        "with": ["begin a series highlighting", "5. Kristi Dosh", "I really love what"],  # 3 segments
        "without": ["Submit your sports", "Twitter Talk", "So Much Math in Football?"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "US",  # if obvious: DE, CH, AT
    },
    "https://mitundvoneinander.wordpress.com/2008/12/31/ratschlage-geben/": {
        "file": "mitundvoneinander.com-Frühling.html",
        "author": "mitundvoneinander",
        "title": "Ratschläge geben",
        "date": "2008-12-31",
        "with": ["PDF:"],
        "without": ["Teilen Sie dies mit", "Gib das erste", "Dezember"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.aclu.org/blog/juvenile-justice/school-prison-pipeline/county-criminalized-students-bad-grades-until-now": {
        "file": "aclu.org-grades.html",
        "author": "Sarah Hinger",
        "Sylvia Torres-Guilléntitle": "This County Criminalized Students for Bad Grades – Until Now",
        "date": "2019-07-25",
        "with": ["criminal justice system.", "more than a decade", "many areas of juvenile"],  # 3 segments
        "without": ["Fight for everyone's rights", "RELATED STORIES", "of Our Students"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "US",  # if obvious: DE, CH, AT
    },
    "https://francais.radio.cz/le-ministre-de-la-sante-surpris-sans-masque-au-restaurant-8698000": {
        "file": "francais.radio.cz-ministre.html",
        "author": "Anna Kubišta",
        "title": "Le ministre de la Santé sommé de démissionner",
        "date": "2020-10-23",
        "with": ["savoir qu'il lui cherchait", "Andrej Babiš a également", "de la Santé avait"],  # 3 segments
        "without": ["ARTICLES CORRESPONDANTS", "Pour faire face à l’épidémie", "Roman Prymula, photo:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CZ",  # if obvious: DE, CH, AT
    },
    "https://www.nestle-family.com/en/recipes/roasted-chicken-oriental-rice": {
        "file": "nestle-family-com-chicken.html",
        "author": "",
        "title": "Roasted Chicken with Oriental Rice",
        "date": "",
        "with": ["1 large or 1200 g whole", "1 tablespoon ground", "cups or 1125 ml of"],  # 3 segments
        "without": ["NEW AND EXCITING SIMILAR", "Like recipe?", "basket and deliver to you"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://edition.cnn.com/2021/03/08/uk/meghan-harry-oprah-interview-recap-scli-gbr-intl/index.html": {
        "file": "edition.cnn.com-royal.html",
        "author": "Rob Picheta",
        "title": "The royal split, racism and family struggles: 11 things we learned from Harry and Meghan's explosive interview",
        "date": "2021-03-14",
        "with": ["The duchess has hinted", "broach the topic", "Harry also criticized"],  # 3 segments
        "without": ["baby's skin color", "PAID CONTENT", "Berlin: Eine Senior-Dating"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "US",  # if obvious: DE, CH, AT
    },
    "https://web.archive.org/web/20070228213001/http://www.alternatives-economiques.fr/site/hs72_003_35heures.html": {
        "file": "archive.org-travaillent.html",
        "author": "Denis Clerc",
        "title": "Les Français travaillent-ils trop peu ?",
        "date": "",
        "with": ["autres travaillent moins", "350 000 emplois créés", "âge effectif de"],  # 3 segments
        "without": ["Le marché du travail est-il trop", "Hors-série n° 72", "L’état de l’économie"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "FR",  # if obvious: DE, CH, AT
    },
    "https://www.ekd.de/andacht-zur-friedensdekade-in-der-kaiser-wilhelm-69810.htm": {
        "file": "ekd.de-Friedensdekade.html",
        "author": "",
        "title": "Andacht zur Friedensdekade in der Kaiser-Wilhelm-Gedächtniskirche, 11. November 2021, 18 Uhr",
        "date": "2021-11-11",
        "with": ["Bevollmächtigter des", "mit euch und Friede", "unerschrocken und furchtlos"],  # 3 segments
        "without": ["SCHWERPUNKTE DER EKD", "Sie suchen Fakten", "Deswegen haben wir"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.ekiba.de/detail/nachricht-seite/id/35204-trauern-digital-am-ewigkeitssonntag/?default=true": {
        "file": "ekiba.de-trauer.html",
        "author": "Alexandra Weber",
        "title": "Trauern digital am Ewigkeitssonntag",
        "date": "2021-12-12",
        "with": ["Gottesdiensten ihrer Gemeinden", "Namen von Verstorbenen", " und dazu laden wir herzlich ein"],  # 3 segments
        "without": [
            "Kirchengemeinde braucht klares Ziel“",
            "Erlebnisraum Kirche",
            "weitere Veranstaltungen ...",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.ekhn.de/aktuell/detailmagazin/news/ekd-papier-fordert-reform-der-pflegefinanzierung.html": {
        "file": "ekhn.de-Pflegefinanzierung.html",
        "author": "",
        "title": "Pflegefinanzierung: Papier der Evangelischen Kirche in Deutschland fordert Reform",
        "date": "2021-11-12",
        "with": ["soziale Ordnung anhand", "Bewährungstest des Sozialstaates", "besser bewältigt werden"],  # 3 segments
        "without": ["zu diesem Thema", "Pflege: Diakonie und", "Gewalt"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.ekbo.de/themen/detail/nachricht/bischofswort.html": {
        "file": "ekbo.de-Bischofs.html",
        "author": "",
        "title": "Wort des Bischofs: Gottesdienst als Identitätsmarker und Wesensmerkmal",
        "date": "2021-11-11",
        "with": ["zur Eröffnung der Schloßkirche", "Bei der Erweiterung", "„Wir sind Kirche mit Geflüchteten"],  # 3 segments
        "without": ["Ähnliche Nachrichten", "Livestream der Synode", "Wort des Bischofs zur Herbstsynode"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://kath.net/news/76785": {
        "file": "kath.net-Menschensohn.html",
        "author": "",
        "title": "Der Tag, an dem sich der Menschensohn offenbart",
        "date": "2021-11-12",
        "with": ["da sammeln sich auch", "hauptsächlich der orthodoxen", "Die scheinbare Verherrlichung"],  # 3 segments
        "without": ["(Weihe-)Alter", "Bistum Hildesheim: Das", "meist-diskutiert"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.piratenpartei.de/2021/11/12/patrick-breyer-haugen-anhoerung-entlarvt-den-unwillen-der-eu-das-digitale-zeitalter-in-die-eigene-hand-zu-nehmen/": {
        "file": "piratenpatei.de-Entlarvt.html",
        "author": "",
        "title": "Patrick Breyer: Haugen-Anhörung entlarvt den Unwillen der EU, das digitale Zeitalter in die eigene Hand zu nehmen",
        "date": "2021-11-12",
        "with": [
            "„Haugen warnt, dass Facebooks",
            "Die Anhörung der Facebook-Whistleblowerin",
            "profitgetriebenen Konzernen anzuvertrauen",
        ],  # 3 segments
        "without": ["Schreibe einen Kommentar", "Meinen Namen, meine E-Mail-Adresse", "Topthemen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://evang.at/lockdown-gottesdienste-bleiben-unter-strengen-auflagen-moeglich/": {
        "file": "evang.at-lockdown.html",
        "author": "",
        "title": "Lockdown: Gottesdienste bleiben unter strengen Auflagen möglich",
        "date": "2021-11-19",
        "with": [
            "in Pfarrgemeinden sollen als",
            "seien alle Presbyterien dringend",
            "Mit Verweis auf den Lockdown",
        ],  # 3 segments
        "without": ["Foto: ccnull/Marco", "Aus dem Evangelium", "theologiebedürftig"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.katholisch.at/aktuelles/136290/alleinerziehende-kinderbetreuung-flaechendeckend-ausbauen": {
        "file": "katholisch.at-alleinerziehende.html",
        "author": "kathpress",
        "title": "Alleinerziehende: Kinderbetreuung flächendeckend ausbauen",
        "date": "2021-11-19",
        "with": [
            "anlässlich des internationalen",
            "kostengünstigen, niederschwelligen und",
            "Die Plattform für Alleinerziehende",
        ],  # 3 segments
        "without": ["Einkommens sein", "wie etwa Caritas-Lerncafés", "Symposium des Akademikerverbands"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.evref.ch/oekumene-trifft-diplomatie-aussenminister-cassis-und-kardinalstaatssekretaer-parolin-besuchen-synode-der-eks/": {
        "file": "evref.ch-ökumene.html",
        "author": "",
        "title": "Ökumene trifft Diplomatie: Aussenminister Cassis und Kardinalstaatssekretär Parolin besuchen Synode der EKS",
        "date": "2021-11-08",
        "with": [
            "In ihren Grusswörtern",
            "Cassis auf die parlamentarische",
            "Präsidentin Rita Famos überreichte",
        ],  # 3 segments
        "without": ["Stefan Wermuth", "Aktuelles", "Bilder des Treffens"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.livenet.ch/themen/gesellschaft/ethik/ethik/398805-von_sprachregeln_genderpolitik_und_ganz_normalem_deutsch.html": {
        "file": "livenet.ch-sprache.html",
        "author": "Fritz Imhof",
        "title": "Von Sprachregeln, Gender-Politik und «ganz normalem Deutsch»",
        "date": "2021-11-19",
        "with": ["dem Jakobsweg geschrieben!", "die Journalistin, ob es", "über Gender-Politik finden"],  # 3 segments
        "without": ["The Edge wurde 60", "Dienstag 30.11.2021 in Baden", "von Livenet in der"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.domradio.de/themen/laien/2021-11-19/reformstau-loesen-irme-stetter-karp-ist-neue-zdk-praesidentin": {
        "file": "domradio.de-Reformstau.html",
        "author": "",
        "title": "Irme Stetter-Karp ist neue ZdK-Präsidentin",
        "date": "2021-11-19",
        "with": ["votierten 41 Delegierte.", "Für Reformen kämpfen", "Stil des ZdK-Präsidiums."],  # 3 segments
        "without": ["Logo des Zdk", "Nach oben", "Zentralkomitee der"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.kirche-und-leben.de/artikel/muensters-caritas-chef-kessmann-ist-gegen-impfpflicht-in-der-pflege": {
        "file": "kirche-und-leben.de-Münster.html",
        "author": "",
        "title": "Münsters Caritas-Chef Kessmann ist gegen Impfpflicht in der Pflege",
        "date": "2021-11-19",
        "with": ["Die Impfpflicht für die Pflege", "Impfquoten mit zwischen", "komme es trotz hohen"],  # 3 segments
        "without": ["Die Ignoranz der", "können entscheiden", "auf Corona-Tests vor"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://ditib.de/detail1.php?id=765&lang=de": {
        "file": "ditb.de-Propheten.html",
        "author": "Kazım TÜRKMEN",
        "title": "Die Nacht der Geburt unseres Propheten sei gesegnet!",
        "date": "2021-10-16",
        "with": ["Mit seinen durch die Schwüre", "Süden und vom Osten", "Knappheit, sowie in Zeiten"],  # 3 segments
        "without": ["Nachrichten und Pressemeldungen", "Botschaft", "Twittern"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://islamische-zeitung.de/bundespraesident-sieht-radikalisierung-bei-querdenkern-und-corona-leugnern/": {
        "file": "islamische-zeitung.de-Bundespräsident.html",
        "author": "",
        "title": "Bundespräsident sieht „Radikalisierung“ bei Querdenkern und Corona-Leugnern",
        "date": "2021-11-19",
        "with": [
            "eigenen Worten eine „zunehmende",
            "Bundeskriminalamts im „föderalen Sicherheitsgefüge“",
            "Verbindungen in weite Teile",
        ],  # 3 segments
        "without": [
            "Schreibe einen Kommentar",
            "Anzeige: Mehr lesen mit dem IZ+ Abo",
            "Corona & die Folgen, Debatte",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.fisch-hitparade.de/magazine/alkohol-auf-dem-boot/": {
        "file": "fisch-hitparade.de-alkohhol.html",
        "author": "",
        "title": "Alkohol auf dem Boot",
        "date": "2022-01-07",
        "with": [
            "sodass man dazu geneigt ist,",
            "und der Führer des Wasserfahrzeugs",
            "zwischen 0,5 und 1,09 werden als Ordnungswidrigkeiten",
        ],  # 3 segments
        "without": ["Alkohol beim Angeln – Diskussion im Forum", "Jetzt teilen!", "Video: Achtung Kontrolle"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://anglerboard.de/ams/raubfisch-rute-im-test-die-iaconelli-spinning-rod.434/": {
        "file": "anglerboard.de-rute.html",
        "author": "Catch more fish",
        "title": "Raubfisch-Rute im Test: die Iaconelli Spinning Rod",
        "date": "2022-01-21",
        "with": [
            'Classic-Gewinner Mike "IKE" Iaconelli',
            "ist für jeden Spinnangler hier die",
            "Zuerst ging es für mich aufs Boot, um",
        ],  # 3 segments
        "without": [
            "Kategorie Catch more fish",
            "Pulse Realistic Softbaits - wie echt!",
            "Diesen Artikel teilen",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://fischundfang.de/radical-pop-ups-und-dips/": {
        "file": "fischundfang.de-pop-ups.html",
        "author": "",
        "title": "Radical Pop-Ups und Dips",
        "date": "2022-01-28",
        "with": [
            "Kein Wunder – die Murmeln gibt",
            "mit denen die Köder nochmal",
            "Pop-Ups haben sich mittlerweile",
        ],  # 3 segments
        "without": [
            'Radical Dips: "Bloody Chicken", "Smashed Fish',
            "Matzes Zander Scheuche",
            "mit Jörg Strehlow",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://fischerhuette.hejfish.com/anglertalk-mit-stephan-hoeferer/": {
        "file": "hejfish.com-stephan.html",
        "author": "",
        "title": "Anglertalk mit Stephan Höferer",
        "date": "2022-01-07",
        "with": [
            "Zudem produziere er eigenständige",
            "gibt es keine Angelpause im Jahr",
            "Ich liebe meine Brandenburger Gewässer in ihrer",
        ],  # 3 segments
        "without": ["Schreibe einen Kommentar", "Das könnte dich auch interessieren:", "Anglertalk mit"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://angelmagazin.de/fische-schmerzen/": {
        "file": "angelmagazin.de-schmerzen.html",
        "author": "Christoph Hein",
        "title": "Können Fische Schmerzen spüren / empfinden?",
        "date": "2022-01-12",
        "with": [
            "anatomischen Voraussetzungen für ein Schmerzempfinden",
            "Fähigkeiten, d. h. sie können Umweltinformationen",
            "Situation zum Bewusstsein beitragen.",
        ],  # 3 segments
        "without": ["Über den Autor", "zusätzlich noch einen Kaffee ", "Angeln in Magdeburg"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.petri-heil.ch/de/bielerseewinterhechte--1026": {
        "file": "petri-heil-ch-hechte.html",
        "author": "Ivan Valetny",
        "title": "Bielersee-Winterhechte",
        "date": "2022-01-26",
        "with": [
            "unterschätzter Zielfisch in der Schweiz",
            "kalten Jahreszeit im Revier",
            "kräftezehrend hochgedrillt werden",
        ],  # 3 segments
        "without": ["Keine Kommentare", "Faszination Bass", "Unterwasser Angriff"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://mannschaft.com/benjamin-naessler-liebe-kennt-keine-pause-gegen-homophobie-in-katar/": {
        "file": "mannschaft.com-katar.html",
        "author": "Newsdesk",
        "title": "Benjamin Näßler: «Liebe kennt keine Pause – gegen Homophobie in Katar»",
        "date": "2022-01-28",
        "with": [
            "Petition heisst es: «Im Winter 2022",
            "US-Bürger eine sechsmonatige Haftstrafe",
            "Organisatoren zu verteidigen und die Bühne",
        ],  # 3 segments
        "without": ["VIELLEICHT AUCH", "Hans und Kosh", "Coming-outs 2021"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://gay.ch/news/vatikan-eltern-sollen-queere-kinder-unterstuetzen-sagt-der-papst": {
        "file": "gay.ch-papst.html",
        "author": "Dominique",
        "title": "VATIKAN: Eltern sollen queere Kinder unterstützen, sagt der Papst",
        "date": "2022-01-28",
        "with": [
            "Obwohl sich gerade viele Gläubige",
            "sorgte Papst Franzikus nun",
            "Der Zickzack-Kurs der Katholischen",
        ],  # 3 segments
        "without": ["Weitere Artikel zum Thema:", "VATIKAN: Papst fordert", "SCHWEIZ/ DEUTSCHLAND:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.lsvd.de/de/ct/6520-Erste-Zusagen-fuer-Aufnahmen-von-ueber-80-LSBTI-aus-Afghanistan": {
        "file": "lsvd.de-afghanistan.html",
        "author": "",
        "title": "ERSTE ZUSAGEN FÜR AUFNAHMEN VON ÜBER 80 LSBTI AUS AFGHANISTAN",
        "date": "2022-01-20",
        "with": [
            "Wir begrüßen die mehr als 80 Aufnahmezusagen",
            "vom Auswärtigen Amt bei der Familienzusammenführung",
            "Situation verschiedener Personengruppen",
        ],  # 3 segments
        "without": [
            "Pressesprecher*in Markus Ulrich",
            "zuständiges Vorstandsmitglied",
            "Der Lesben- und Schwulenverband (LSVD) ist",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.siegessaeule.de/magazin/p%C3%A4dophilie-als-politisches-machtinstrument/": {
        "file": "siegessaeule.de-Machtinstrument.html",
        "author": "Paula Balov",
        "title": "Pädophilie als politisches Machtinstrument",
        "date": "2022-01-28",
        "with": [
            "Dabei gab es dort keine Befürwortung",
            "wie etwa die QAnon-Erzählung",
            "Wir haben auch heute noch keinen Weg",
        ],  # 3 segments
        "without": ["Peter Rehberg: „Schwule glauben, sich", "KULTUR", "Bild: Stefan Müller"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.l-mag.de/news-1010/holocaust-gedenktag-lesbische-erinnerungskultur-mit-stolpersteinverlegung.html?L=422": {
        "file": "l-mag.de-Holocaust-Gedenken.html",
        "author": "Claudia Lindner",
        "title": "Holocaust-Gedenktag: Lesbische Erinnerungskultur mit Stolpersteinverlegung",
        "date": "2022-01-27",
        "with": [
            "Deutschland waren queere Opfer",
            "Mit der Wahl von Dr. Hertha Kraus",
            "international an der Integration von",
        ],  # 3 segments
        "without": ["Weiterlesen:", "Die aktuelle Ausgabe der L-MAG", " von den Wirtschaftsweibern"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.maenner.media/gesellschaft/community/interview-mit-rainer-teuber-outinchurch/": {
        "file": "maenner.media-church.html",
        "author": "Michael Rädel, Redaktion",
        "title": "Interview mit Rainer Teuber – #OutInChurch",
        "date": "2022-01-24",
        "with": [
            "den Besucherservice. Er ist schwul",
            "Was müsste sich in den Bistümern",
            "Über das Rogate-Kloster: Eine",
        ],  # 3 segments
        "without": [
            "HuK (Homosexuelle und Kirche)",
            "Der Einsatz für die Menschenrechte ist",
            "Kostenloser Download:",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.regenbogenportal.de/aktuelles/08112021-online-fachtag-zum-intersex-day-of-remembrance": {
        "file": "regenbogenportal.de-intersex.html",
        "author": "",
        "title": "Online-Fachtag zum Intersex Day of Remembrance",
        "date": "2021-11-08",
        "with": [
            "digitale Veranstaltung zum Thema",
            "Für inter* Personen ist es wichtig",
            "Familie, Senioren, Frauen und Jugend",
        ],  # 3 segments
        "without": [
            "Newsletter abonnieren",
            "Online-Fachtag zum Intersex",
            "Anlaufstellen, Fachveranstaltungen und Materialien",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.falstaff.de/nd/burgenland-best-of-ruster-ausbruch-dac/": {
        "file": "falstaff.de-burgenland.html",
        "author": "",
        "title": "Burgenland: Best of Ruster Ausbruch DAC",
        "date": "2022-01-28",
        "with": [
            "Jahr 2020 ist dieses Juwel aus",
            "Die sanften Hänge des Ruster Hügellands",
            "Ruster Ausbruch DAC",
        ],  # 3 segments
        "without": ["Mehr zum Thema", "ERSCHIENEN IN", "Rust am Westufer des"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.silkes-weinkeller.de/weinblatt-magazin/wein-dekantieren/": {
        "file": "silkes-weinkeller.de-dekantieren.html",
        "author": "",
        "title": "Wein dekantieren: Alles Wissenswerte rund um einen besonderen Schritt",
        "date": "2021-10-14",
        "with": ["Während die Trennung vom Depot", "Die meisten Gefäße bestehen", " Potenzial, den Genuss"],  # 3 segments
        "without": ["Wein zum Spargel:", "Schreibe einen Kommentar", "Inhaltsverzeichnis"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.deutscheweine.de/aktuelles/meldungen/details/news/detail/News/rieslingbirthday-posts-gewinnen/": {
        "file": "deutscheweine.de-riesling.html",
        "author": "",
        "title": "#RieslingBirthday Posts gewinnen",
        "date": "2022-01-27",
        "with": [
            'Es gibt zahlreiche "erste" Erwähnungen',
            "zeigen die Verwandtschaft mit Wildreben",
            "Instagram-Posts mit dem hashtag",
        ],  # 3 segments
        "without": ["MELDUNGEN AUS DEM DWI", "Downloadbereich", "UNSERE APP DEUTSCHE WEINE IM APPSTORE"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.meininger.de/wein/erzeuger/lvmh-mit-ordentlichem-wachstum": {
        "file": "meininger.de-wachstum.html",
        "author": "",
        "title": "LVMH mit ordentlichem Wachstum",
        "date": "2022-01-28",
        "with": [
            "meldet für 2021 einen Umsatz von 64,2",
            "Wichtige Brands sind etwa die Champagnermarken",
            "Joint Venture Cheval des Andes",
        ],  # 3 segments
        "without": [
            "Unsere neue Rubrik. Zum Auftakt fragen",
            "Italien-Fans alles, was das Herz begehrt",
            "Sektkellerei am",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.weinkenner.de/st-magdalener-rotweine-mit-eleganz-und-charakter/": {
        "file": "weinkenner.de-st.magdalener.html",
        "author": "Jossi Loibl",
        "title": "St. Magdalener: Rotweine mit Eleganz und Charakter",
        "date": "2022-01-27",
        "with": [
            "Italiens, neben Barolo und Barbaresco",
            "St. Magdalener überzeugen mit zarter Frucht",
            "ernatschwein, der vom Gambero",
        ],  # 3 segments
        "without": [
            "Über den Autor",
            "Südtiroler Weissweine die Geschichte schrieben",
            "Das ideale Universal-Weinglas",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.alacarte.at/reisen/der-historische-purzelbaum-20215/": {
        "file": "alacarte.at-purzelbaum.html",
        "author": "Christian Seiler",
        "title": "Der historische Purzelbaum",
        "date": "2021-11-25",
        "with": [
            "Leipzig war, widerfuhr mir etwas Merkwürdiges",
            "Menschen umfassende Saal bis auf",
            "anderswo kennengelernt hatte, und",
        ],  # 3 segments
        "without": ["Milchbar Pinguin", "In Auerbachs Keller tafelten Faust und Mephisto", "SHARE"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.umweltbundesamt.de/themen/eu-taxonomie-atomkraft-erdgas-sind-nicht-nachhaltig": {
        "file": "umweltbundesamt.de-atomkraft.html",
        "author": "",
        "title": "EU-Taxonomie: Atomkraft und Erdgas sind nicht nachhaltig",
        "date": "2022-01-25",
        "with": [
            "Entwurf der Europäischen Kommission für einen",
            "denn die Entsorgung",
            "Energien auszubauen und Technologien",
        ],  # 3 segments
        "without": [
            "Die Auswertung der Stimmen beansprucht einige Zeit.",
            "Quelle: jorisvo / Fotolia.com",
            "Greenwashing",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bmwi.de/Redaktion/DE/Meldung/2022/20220124-foerderung-fur-energieeffiziente-gebaude-durch-kfw.html": {
        "file": "bmwi.de-neubau.html",
        "author": "",
        "title": "Förderung für energieeffiziente Gebäude der KfW vorläufig gestoppt - Bundesregierung ordnet Förderung und gesetzliche Standards für Neubau neu",
        "date": "2022-01-24",
        "with": [
            " EH55 Neubauförderung hat",
            "wieder aufgenommen, sobald",
            "Über die Zukunft der Neubauförderung",
        ],  # 3 segments
        "without": ["Verwandte Themen", "Europäische und internationale Energiepolitik", "MEDIENRAUM"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bafa.de/SharedDocs/Kurzmeldungen/DE/Energie/Mineraloel/2021_11_mineraloelinfo.html;jsessionid=B01BDCE4530EF0FB9BD52A2652C1F167.2_cid390": {
        "file": "bafa.de-mineraloelabsatz.html",
        "author": "",
        "title": "MineralölINFO November 2021 (Mineralölabsatz)",
        "date": "2022-01-27",
        "with": ["Deutschland im aktuellen Zeitraum", "32,23", "die Einfuhr von Rohöl"],
        "without": ["Mineralölstatistik", "Diese Seite", "27.01.2022"],
        "comments": [],  # 0 or 3 segments
        "license": "CC-BY-ND",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bmas.de/DE/Service/Presse/Meldungen/2022/aenderung-der-anforderungen-an-impf-und-genesenennachweisen.html": {
        "file": "bmas.de-anforderungen.html",
        "author": "",
        "title": "Änderung der Anforderungen an Impf- und Genesenen­­nachweise",
        "date": "2022-01-26",
        "with": [
            "Das Robert-Koch-Institut (RKI) wurde beauftragt",
            "Anforderungen an 3G-Nachweise ggf.",
            'wieder den Status "vollständig geimpft"',
        ],  # 3 segments
        "without": [
            "FAQs Betrieblicher Infektionsschutz",
            "Fragen zum Thema Betrieblicher Infektionsschutz.",
            "NACH OBEN",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bmfsfj.de/bmfsfj/aktuelles/alle-meldungen/bundeskabinett-legt-schwerpunkte-der-praesidentschaft-fest-192440": {
        "file": "bmfsfj.de-praesidentschaft.html",
        "author": "",
        "title": "Bundeskabinett legt Schwerpunkte der Präsidentschaft fest",
        "date": "2022-01-21",
        "with": [
            "Gruppe der Sieben verständigt",
            "Am 1. Januar hat Deutschland turnusgemäß",
            "ein starkes Miteinander.",
        ],  # 3 segments
        "without": [
            "G7 Germany 2022: Informationen zur",
            "Internationales und Europa",
            "Bundesregierung/Steffen Kugler",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.bfs.de/SharedDocs/Pressemitteilungen/BfS/DE/2022/001.html": {
        "file": "bfs.de-radon.html",
        "author": "",
        "title": "Radon im Boden: Neue Karte gibt Orientierung",
        "date": "2022-01-25",
        "with": [
            "richtet sich an alle, die sich über die Radon-Situation",
            "darüber hinaus bereits vorhandene Messdaten",
            "nur mit einer Radon-Messung im Boden",
        ],  # 3 segments
        "without": [
            "Was ist Radon?",
            "Radon in der Boden-Luft in Deutschland",
            "Wie bewerten Sie diesen Artikel?",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bsi.bund.de/DE/Service-Navi/Presse/Pressemitteilungen/Presse2022/220128_Forschungsprojek-KI-Auto_BSI-ZF.html": {
        "file": "bsi.de-ki.html",
        "author": "",
        "title": "Sicherheits-Check für Künstliche Intelligenz in Autos: BSI und ZF starten Projekt mit TÜViT",
        "date": "2022-01-28",
        "with": [
            "orteile von KI-Systemen in der Mobilität",
            "Anforderungen, Methoden und Werkzeuge",
            "KI-Systemen in Autos nach allgemein",
        ],  # 3 segments
        "without": ["Verbraucherinnen und Verbraucher", "IT-SICHERHEITSVORFALL", "FOLGEN SIE UNS"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bmel.de/DE/themen/laendliche-regionen/zukunftsforum2022.html;jsessionid=ED5DD5866BE5A5FAA71D389A9C6A5802.live922": {
        "file": "bmel.de-zukunftsforum.html",
        "author": "",
        "title": "15. Zukunftsforum Ländliche Entwicklung",
        "date": "2022-01-26",
        "with": [
            "Bürgerschaftliches Engagement und Ehrenamt",
            "Zwei Tage wurde darüber diskutiert,",
            "Ehrenamtliche in ländlichen Regionen.",
        ],  # 3 segments
        "without": [
            "Gestalten, anstatt zu spalten: Ehrenamtliche",
            "Kommission Gleichwertige",
            "Rückblick: Das 14. Zukunftsforum Ländliche",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bka.de/DE/Presse/Listenseite_Pressemitteilungen/2022/Presse2022/220126_PM_Telegram.html": {
        "file": "bka.de-messengerdienste.html",
        "author": "",
        "title": "Messengerdienste sind kein rechtsfreier Raum",
        "date": "2022-01-26",
        "with": [
            "entwickelt sich nach Einschätzung der",
            "BKA gemeinsam mit den Landeskriminalämtern",
            "Corona-Pandemie hat dazu beigetragen",
        ],  # 3 segments
        "without": [
            "Pressemitteilung als PDF",
            "Haben Sie das Gesuchte nicht",
            "Neue Taskforce des Bundeskriminalamtes",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bundesrat.de/SharedDocs/texte/22/20220127-weremember-gedenkstunde-kranzniederlegung.html;jsessionid=FD52ED97F4C3551B332D2AA670DAE45C.1_cid382": {
        "file": "bundesrat.de-erinnerungen.html",
        "author": "",
        "title": "Erinnerung an die Opfer der NS-Verbrechen",
        "date": "2022-01-27",
        "with": [
            "wurde als Siebenjährige von Stuttgart",
            "Neben der gastgebenden Bundestagspräsidentin",
            "als Zeichen des Gedenkens an die Opfer",
        ],  # 3 segments
        "without": [
            "Presse- und Informationsamt der Bundesregierung | Jesco Denzel",
            " Bundesrat | Frank Bräuer",
            "Ist dieser Beitrag hilfreich?",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bmz.de/de/aktuelles/aktuelle-meldungen/schulze-deutschland-an-der-der-seite-wfp-im-kampf-gegen-hunger-103026": {
        "file": "bmz.de-schulze.html",
        "author": "",
        "title": "Schulze: Deutsch­land steht fest an der Seite des Welt­ernährungs­programms im Einsatz gegen Hunger in der Welt",
        "date": "2022-01-25",
        "with": ["tragen auch der Klima­wandel", "Fast fünf Millionen Menschen", "Alleine im letzten Jahr"],  # 3 segments
        "without": ["Sonderinitiative EINEWELT", "SDG 2: Kein Hunger", "Siehe auch"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.mein-haustier.de/hund/eat-small/": {
        "file": "mein-haustier.de-hund.html",
        "author": "",
        "title": "20% Rabatt auf EAT SMALL",
        "date": "2022-01-28",
        "with": [
            "Nachhaltigkeit ist heutzutage ein wichtiges Thema",
            "Ressourcen benötigen, sind sie",
            "Alleinfutter für alle etwas ruhigeren Hunde",
        ],  # 3 segments
        "without": ["Energy Snack", "Ähnliche Artikel", "WALD Nassfutter"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tierwelt.ch/news/natur-umwelt/immer-mehr-modemarken-werden-pelzfrei-so-erkennen-sie-echtpelz-im-laden": {
        "file": "tierwelt.ch-plez.html",
        "author": "Jil Schuller",
        "title": "Immer mehr Modemarken werden pelzfrei – so erkennen Sie Echtpelz im Laden",
        "date": "2022-02-02",
        "with": [
            "Waschbären oder Hunde unter schlechten",
            "Fell aus einer Zucht oder gezieltem Wildfang",
            "Sind die Haarspitzen sichtbar",
        ],  # 3 segments
        "without": [
            "übergeben worden ist.",
            "Pelzdeklarationskontrolleure haben im vergangenen",
            "Die aktuelle Ausgabe",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.martinruetter.com/service/aktuelles/aktuelles/schneefloeckchen-weissroeckchen-mit-hund-im-winter/": {
        "file": "martinruetter.com-Winter.html",
        "author": "",
        "title": "Schneeflöckchen, Weißröckchen… – mit Hund im Winter",
        "date": "2022-01-27",
        "with": [
            "Spaziergang in geschlossener Schneedecke",
            "Müssen Hunde im Winter auch Schneeschuhe",
            "Wichtig bei allen Trainingsstunden",
        ],  # 3 segments
        "without": ["Martin Rütter DOGS", "Umgang mit dem", "HUNDESCHULEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://tierschutz-berlin.de/aktuelles/tierschutzverein-ruft-zu-boellerverzicht-auf/": {
        "file": "tierschutz-berlin.de-boellerverzicht.html",
        "author": "",
        "title": "Tierschutzverein ruft zu Böllerverzicht auf",
        "date": "2021-12-29",
        "with": [
            "Vorstandsvorsitzende Eva Rönspieß.",
            "ihre Lieblinge möglichst gut gegen",
            "Silvesternacht gerade in Stadtrandbezirken",
        ],  # 3 segments
        "without": ["Tierschutzverein für Berlin und Umgebung", "Bank für Sozialwirtschaft", "Hausvaterweg 39"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.haustiermagazin.com/kaufratgeber-vergleich-bestes-elektronisches-katzenspielzeug/": {
        "file": "haustiermagazin.com-katzenspielzeug.html",
        "author": "Steffi",
        "title": "Kaufratgeber: elektronisches Katzenspielzeug – sorgt ganz automatisch für Abwechslung",
        "date": "2022-02-01",
        "with": [
            "haben uns deshalb verschiedene elektrische",
            "Welches Spiel zu deiner Mieze passt",
            "elektrisches Katzenspielzeug bereits",
        ],  # 3 segments
        "without": [
            "TIPPS, HILFE UND SCHNÄPPCHEN",
            "Bei den Verlinkungen handelt es sich um",
            "drei Kater und aktuell zwei portugiesische",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.eurosport.de/olympia/olympia-2022-in-peking/2022/olympia-2022-zweiter-coronafall-deutschen-team-aufregung-thomas-weikert-vorganger-attackiert_sto8749554/story.shtml": {
        "file": "eurosport.de-corona.html",
        "author": "Eurosport",
        "title": "OLYMPIA 2022: ZWEITER CORONAFALL IM DEUTSCHEN TEAM SORGT FÜR AUFREGUNG - WEIKERT VON HÖRMANN ATTACKIERT",
        "date": "2022-02-02",
        "with": [
            "Alfons Hörmann seinen Nachfolger Thomas",
            "die Defensive. Kurz vor der Eröffnungsfeier",
            "Athlet oder Betreuer, sitzt symptomfrei mit einem",
        ],  # 3 segments
        "without": ["LETZTE NEWS", 'DOLL "BEIM ERSTEN MAL LOCKERER"', "NÄCHSTES DEUTSCHES TEAMMITGLIED"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.laola1.at/de/red/fussball/bundesliga/news/rapids-barisic-geschlaucht---dann-hau--ich-mein-handy-zam-/": {
        "file": "laola1.at-barisic.html",
        "author": "Alexander Karper",
        "title": 'Barisic: "Dann hau\' ich mein Handy zam"',
        "date": "2022-02-02",
        "with": [
            "Business wird immer schnelllebiger",
            "Kampfmannschaft gekommen sind, die aus unserer Akademie",
            "Die Corona-Pandemie sorgt nicht nur für sportliche",
        ],  # 3 segments
        "without": [
            "Status quo: Das passiert noch beim SK Rapid",
            "Action! Anna Gasser im Olympia-Interview",
            'WAC: "Handschrift von Dutt verinnerlicht"',
        ],  # 3 segments
        "comments": [
            "Wieviele Rapid Artikel kommen heute",
            "Schaust mal wie viele Reaktionen es",
            "Hauptsachen schwurbeln - oder?",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.sportnews.bz/artikel/wintersport/wintersport-mix/peking-sucht-den-superstar-7-moegliche-gesichter": {
        "file": "sportnews.bz-peking.html",
        "author": "det/dpa",
        "title": "Peking sucht den Superstar: 7 mögliche Gesichter",
        "date": "2022-02-02",
        "with": [
            "bereits zur jüngsten Slalom-Olympiasiegerin",
            "Gu gilt als Musterschülerin, sie ist Stanford",
            "bisher allerdings nicht optimal gelaufen",
        ],  # 3 segments
        "without": ["AFP / MARCO BERTORELLO", "So viel verdienen Lkw-Fahrer in Berlin", "Tausende Hausbesitzer"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.munich2022.com/de/europas-topathleten-fit-fur-munchen-2022": {
        "file": "munich2022.com-topathleten.html",
        "author": "",
        "title": "EUROPAS TOPATHLETEN FIT FÜR MÜNCHEN 2022",
        "date": "2022-01-31",
        "with": [
            "Weltjahresbestleistung von 6,02 m",
            "dass ich viel Selbstvertrauen habe,",
            "dass ich viel Selbstvertrauen habe,",
        ],  # 3 segments
        "without": ["Getty Images", "Externer Inhalt", "Tags"],  # 3 segments #nicht mehr als zwei gefunden
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.golfpost.de/golf-im-tv-777789172/": {
        "file": "golfpost.de-premiere.html",
        "author": "",
        "title": "Golf im TV: Klassiker auf der PGA Tour, Premiere beim Desert Swing",
        "date": "2022-01-31",
        "with": [
            "Nach zuvor zwei Rolex-Series-Events",
            "Kalifornien, die DP World Tour",
            "Deutsche um Max Kieffer, Matti Schmid",
        ],  # 3 segments
        "without": [
            "Jetzt für Golf-Lotse Top-News anmelden",
            "News rund um PGA Tour",
            "Überblick. (Foto: Getty)",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.golf.de/i7484_1.html": {
        "file": "golf.de-augusta.html",
        "author": "Daniel Dillenburg",
        "title": "Elder: Aus dem Ghetto nach Augusta",
        "date": "2022-02-01",
        "with": [
            "Weg dorthin war für den in Dallas geborenen",
            "Blickt man auf Elders Werdegang",
            "Zocker und Wettliebhaber arbeitete",
        ],  # 3 segments
        "without": ["Nicklaus – Mann der großen Worte", "Mehr zum Thema", "Augusta National/Getty Images"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.motorsport-total.com/formel-1/news/nach-erstem-f1-test-2022-alfa-romeo-plant-spaeten-launch-des-c42-22020203": {
        "file": "motorsport-total.com-romeo.html",
        "author": "Juliane Ziegengeist",
        "title": "Nach erstem F1-Test 2022: Alfa Romeo plant späten Launch des C42",
        "date": "2022-02-02",
        "with": [
            "Team bestätigte am Mittwoch, dass sein neues Auto",
            "25. Februar auf dem Circuit de Barcelona-Catalunya",
            "Giovinazzi und werden versuchen",
        ],  # 3 segments
        "without": [
            "Was kostet eine Solaranlage",
            "Lada Niva Monster: Russlands",
            "auf dem Formel-1-Auto für 2022",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.motorsport-magazin.com/formel1/news-275350-formel-1-fahrercheck-alphatauri-das-koennen-pierre-gasly-yuki-tsunoda-f1-2022/": {
        "file": "motorsport-magazin.com-alphatauri.html",
        "author": "Markus Steinrisser",
        "title": "Formel-1-Fahrercheck - AlphaTauri: Das können Gasly & Tsunoda",
        "date": "2022-02-02",
        "with": [
            "beginnt das Jahr mit einem Fahrer-Formcheck",
            "Fehltritte ein, die hin und wieder auch große Konsequenzen haben.",
            "zeigt, ist, dass er gelegentlich Gefahr",
        ],  # 3 segments
        "without": ["Formel 1 - Pierre Gasly", "mischt Top-Teams", "Motorsport-Magazin.com Redakteur"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.autosprint.ch/de/classic/histo-monte-pistenstopp-in-rheinfelden/": {
        "file": "autosprint.ch-pistenstopp.html",
        "author": "Redaktion",
        "title": "Histo-Monte: Pistenstopp in Rheinfelden",
        "date": "2022-01-31",
        "with": [
            "Histo-Monte stehen gut. Die",
            "gesperrte historische Stadtbrücke benutzten",
            "früherer Veranstaltungen zur Verfügung",
        ],  # 3 segments
        "without": ["Beiträge zum Thema", "Respekt vor dem", "Erinnerung an den"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.eishockeynews.de/aktuell/artikel/2022/02/01/zweimal-kuusela-im-powerplay-und-ein-konter-muenchen-verliert-bei-tappara-tampere-mit-0-3-und-verpasst-das-chl-endspiel/c90d406b-2b41-4e98-b9cd-4aa661e512b2.html": {
        "file": "eishockeynews.de-halbfinale.html",
        "author": "Stefan Wasmer",
        "title": "Das Halbfinale der Champions Hockey League am Dienstag",
        "date": "2022-02-01",
        "with": [
            "Tappara ging dabei bereits nach rund",
            "sowie die bessere Struktur. So",
            "Saison 2021/22 und damit den Nachfolger",
        ],  # 3 segments
        "without": [
            "DAS KÖNNTE SIE AUCH INTERESSIEREN",
            "Wenn du Zeit am Computer",
            "Schwenningen, Landshut oder",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.skispringen.com/marita-kramer-verpasst-olympische-spiele-in-peking/": {
        "file": "skispringen.com-verpasst.html",
        "author": "Luis Holuch",
        "title": '"Pure Leere": Marita Kramer verpasst Olympische Spiele in Peking',
        "date": "2022-02-01",
        "with": [
            "Spiele in Peking werden ohne die große Top",
            "Ich habe so viel Energieund Zeit investiert",
            "die Einzel-Entscheidung auf",
        ],  # 3 segments
        "without": ["Über Luis Holuch", "Ryoyu Kobayashi gewinnt die 70.", "NATIONENCUP 2021/2022"],  # 3 segments
        "comments": [
            "der WM haben sie genau vor Ihr verkürzt",
            "Du bist dann erst 24/25 und kannst Olympiasiegerin",
            "werden folgen, egal von welcher",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://berkutschi.com/de/front/news/10759-marius-lindvik-gewinnt-in-willingen": {
        "file": "berkutschi.com-willingen.html",
        "author": "",
        "title": "Marius Lindvik gewinnt in Willingen",
        "date": "2022-01-31",
        "with": [
            "und dem Slowenen Cene Prevc durch",
            "zu den Top-Favoriten auf Olympisches",
            "Olympischen Spiele am",
        ],  # 3 segments
        "without": ["Wettkampfdaten", "Weltcup Herren", "Weitester Sprung"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.handball-world.news/o.red.r/news-1-1-1-139353.html": {
        "file": "handball-word.news-nationalspiel.html",
        "author": "",
        "title": '"Mehr Variabilität im Angriff": HSV Hamburg verpflichtet niederländischen Nationalspieler',
        "date": "2022-02-02",
        "with": ["Jahre zum Handball Sport", "Lippe und die SG Flensburg-Handewitt", "Erinnerungen an Hamburg"],  # 3 segments
        "without": ["Eine Tasse davon", "nimmt...", '"Waren vier'],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.handball.ch/de/news/2022/cup-vorschau-beim-bsv-stans-freut-man-sich-auf-ein-bruderduell-und-viele-fans/": {
        "file": "handball.ch-bruderduell.html",
        "author": "",
        "title": "CUP-VORSCHAU: BEIM BSV STANS FREUT MAN SICH AUF EIN BRUDERDUELL UND VIELE FANS",
        "date": "2022-02-02",
        "with": [
            "Ich glaube fest daran, dass wir die Halle füllen",
            "spezielle Affiche. Mit Daniel",
            "mit Spannung erwarteten Viertelfinals HSC",
        ],  # 3 segments
        "without": ["Gemeinsam den Verein", "DAS KÖNNTE DICH", "HSC Kreuzlingen in die"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.liquimoly-hbl.de/de/n/news/2--liga/2021-22/transfers/tsv-bayer-dormagen/neuer-cheftrainer-fuer-dormagen--matthias-flohr-uebernimmt-ab-sommer-2022/": {
        "file": "liquimoly-hbl.de-cheftrainer.html",
        "author": "",
        "title": "NEUER CHEFTRAINER FÜR DORMAGEN: MATTHIAS FLOHR ÜBERNIMMT AB SOMMER 2022",
        "date": "2022-01-31",
        "with": [
            "mit einer bestens motivierten Mannschaft den",
            "Haases breitem Netzwerk. Auch heimische",
            "aber ich habe ein gutes Gefühl",
        ],  # 3 segments
        "without": ["Verwandte Themen", "Coburg", "#diewiesel"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dhb.de/de/redaktionsbaum/nationalteams/a-frauen/erneuter-verzicht-auf-regionallehrgang-/": {
        "file": "www.dhb.de-regionallehrgang.html",
        "author": "",
        "title": "ERNEUTER VERZICHT AUF REGIONALLEHRGANG",
        "date": "2022-02-02",
        "with": [
            "im März beginnen. Teil der Maßnahme",
            "HBF und Liga können die freigewordenen",
            "Nationalmannschaft im März mit",
        ],  # 3 segments
        "without": ["NEWS", "Foto: Sascha Klahn", "A-FRAUEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.rhein-neckar-loewen.de/kleiner-vorverkauf-fuer-liga-heimspiele-gestartet-920981": {
        "file": "rhein-neckar-loewen.de-vorverkauf.html",
        "author": "",
        "title": "„Kleiner“ Vorverkauf für Liga-Heimspiele gestartet",
        "date": "2022-02-02",
        "with": [
            "können die Rhein-Neckar Löwen lediglich",
            "12. Februar, 20.30 Uhr treffen die Löwen",
            "sollte sich die erlaubte Zuschauer-Kapazität",
        ],  # 3 segments
        "without": ["Wenn du per E-Mail über Aktuelles aus", "Alle News anzeigen", "Veröffentlichung"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.hvw-online.org/aktuell/detail/news/zuschauerrueckkehr-bei-den-proficlubs-der-region": {
        "file": "hvw-online.org-zuschauer.html",
        "author": "",
        "title": "Zuschauerrückkehr bei den Proficlubs der Region",
        "date": "2022-02-02",
        "with": [
            "Heimspiele keine Tickets zu erwerben.",
            "Göppingen und den TVB Stuttgart geht",
            "Beachtung der 2G+-Regelung",
        ],  # 3 segments
        "without": ["Schriftgröße", "Impressum", "Fritz-Walter-Weg"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.biathlonworld.com/de/news": {
        "file": "biathlonword.com-chinesisch.html",
        "author": "",
        "title": "PEKING 2022 – EINE GROSSE CHANCE FÜR DEN CHINESISCHEN BIATHLONSPOR",
        "date": "2022-02-02",
        "with": [
            "kam die chinesische Damenstaffel viermal",
            "BMW IBU Weltcupgesamtwertung",
            "und eine solide Basis für die Weiterentwicklung",
        ],  # 3 segments
        "without": ["BEIJING 2022 - CHINA STORY", "ABONNIERE UNSEREN NEWSLETTER", "OLYMPISCHE WINTERSPIELE"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.biathlon-antholz.it/de/newsroom/23-01-2022-dorothea-wierer-darf-beim-antholz-abschluss-noch-jubeln/17-378.html": {
        "file": "biathlon-antholz.it-jubeln.html",
        "author": "",
        "title": "DOROTHEA WIERER DARF BEIM ANTHOLZ-ABSCHLUSS NOCH JUBELN",
        "date": "2022-01-23",
        "with": [
            "beim letzten Weltcuprennen schlug",
            "Biathlon-Tross pausiert jetzt knapp",
            "die trotz Corona, gut verlaufen",
        ],  # 3 segments
        "without": ["ZURÜCK ZUR LISTE", "MIT FREUNDEN TEILEN", "DAS KÖNNTE SIE AUCH"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "IT",  # if obvious: DE, CH, AT
    },
    "https://www.leichtathletik.de/news/news/detail/76066-erfurt-maximilian-thorwirth-ueberrascht-auf-1500-meter-distanz": {
        "file": "leichtathletik.de-erfurt.html",
        "author": "Sandra Arm",
        "title": "Erfurt: Maximilian Thorwirth überrascht auf 1.500 Meter-Distanz",
        "date": "2022-02-01",
        "with": [
            "mit zwei Topzeiten ihre gute Form",
            "hätte ich mit dieser Zeit nicht gerechnet.",
            "Karlsruhe kam Imke Onnen (Hannover 96)",
        ],  # 3 segments
        "without": ["Bildergalerie", "WEITERE NEWS", "Trauer um Henning von Papen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.leichtathletik-berlin.de/pressemitteilungen_reader/norddeutschland-sucht-seine-meister.html": {
        "file": "leichtathletik-berlin.de-norddeutschland.html",
        "author": "",
        "title": "Norddeutschland findet seine Meister",
        "date": "2022-01-31",
        "with": [
            "Goldrausch auf den 1500 Metern",
            "Altersklasse souverän auf den 60m",
            "den 2. Platz erreichen.",
        ],  # 3 segments
        "without": ["Gisele Wender", "Sponsoren", "Pressemitteilungen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.flvw.de/news/detail/joana-herrmann-fliegt-bei-den-flvw-hallenmeisterschaften-ueber-178-meter/": {
        "file": "flvw.de-hallenmeisterschaften.html",
        "author": "",
        "title": "JOANA HERRMANN FLIEGT BEI DEN FLVW-HALLENMEISTERSCHAFTEN ÜBER 1,78 METER",
        "date": "",
        "with": [
            "Eine Woche nach seinem Titelgewinn",
            "Sekunden bedeutet für sie eine",
            "dreimal vergeblich an 1,80 Meter",
        ],  # 3 segments
        "without": ["Themenrelevante Nachrichten", "Dreisprung auf 13,93 Meter", "im Kugelstoßen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.boxen.de/news/viviane-obenauf-staatsanwaltschaft-hat-beweise-vorgelegt-70501": {
        "file": "boxen.de-staatsanwaltschaft.html",
        "author": "reineckefuchs",
        "title": "Viviane Obenauf – Staatsanwaltschaft hat Beweise vorgelegt",
        "date": "2022-02-02",
        "with": [
            "Das wurde abgelehnt, weil die Beweislage",
            "Chevrolet Camaro zur Tatzeit vor dem Apartment",
            "Tatzeit zuhause gewesen zu sein",
        ],  # 3 segments
        "without": [
            "Ähnliche Beiträge",
            "Tyson Fury vs Dillian Whyte wird von",
            "Trevor Bryan siegt über Jonathan Guidry",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.boxen1.com/morgen-abend-chris-eubank-jr-mit-ring-rueckkehr-gegen-liam-williams-60586/": {
        "file": "boxen1.com-ring-rückkehr.html",
        "author": "Patrick Czerny",
        "title": "Morgen Abend: Chris Eubank Jr. mit Ring-Rückkehr gegen Liam Williams!",
        "date": "2022-02-04",
        "with": [
            "Wochenende wieder in den Ring. Der",
            "„Gegen mich wird er den Schlussgong",
            "Monaten offizieller Pflichtherausforderer.",
        ],  # 3 segments
        "without": ["BOXEN1-Award: Das sind Boxer, Boxerin,", "Promoter des Jahres 2021", "Chris Eubank Jr."],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.spox.com/de/sport/olympia/2202/Artikel/zwei-corona-faelle-olympische-spiele-peking-eric-frenzel-terence-weber.html": {
        "file": "spox.com-corona-fealle.html",
        "author": "",
        "title": "Olympia 2022 - Zwei weitere Corona-Fälle! Kombinierer Eric Frenzel und Terence Weber betroffen",
        "date": "2022-02-04",
        "with": [
            "Kombinierer waren am Tag zuvor in China",
            "besten sieben Athleten des Gesamtweltcups",
            "November im finnischen Ruka den ersten Weltcupsieg",
        ],  # 3 segments
        "without": [
            "Die Nordischen Kombinierer Terence Weber",
            "Gegen Peking: Tibeter protestieren vor IOC-Hauptquartier",
            "Olympia 2022 - Nordische Kombination:",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tennisnet.com/news/diese-ymers-zwei-ueberraschungen-an-einem-tag": {
        "file": "tennisnet.com-ueberraschungen.html",
        "author": "",
        "title": "Diese Ymers! Zwei Überraschungen an einem Tag!",
        "date": "2022-02-04",
        "with": [
            "Montpellier für zwei Überraschungen gesorgt",
            "Drei-Kronen-Team wieder einmal Gesprächsthema",
            "Mann am Start, der nach seinem frühen",
        ],  # 3 segments
        "without": [
            "Hier das Einzel-Tableau in Pune",
            "ATP: Aufschlag-Hüne Milos Raonic fällt",
            "Berlin: GEERS sucht 700",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.tennismagazin.de/news/zverev-zieht-ins-viertelfinale-von-montpellier-ein/": {
        "file": "tennismagazin.de-viertelfinale.html",
        "author": "Redaktion",
        "title": "Zverev zieht ins Viertelfinale von Montpellier ein",
        "date": "2022-02-04",
        "with": [
            "besaß der mit einer Wildcard ausgestattete",
            "Niederlage gegen Jonathan Erlich/Edouard",
            "Achtelfinal-Aus gegen Denis Shapovalov",
        ],  # 3 segments
        "without": [
            "Alexander Zverev steht im Viertelfinale des ATP-Turniers",
            "AUCH AUF TENNISMAGAZIN.DE",
            "Ein Kommentar von tennis",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.btv.de/de/spielbetrieb/news/auf-den-spuren-von-rafael-nadal.html": {
        "file": "btv.de-spuren.html",
        "author": "JUERGEN HASENKOPF",
        "title": "AUF DEN SPUREN VON RAFAEL NADAL",
        "date": "2022-02-03",
        "with": [
            "Februar 2022 in der TennisBase Oberhaching",
            "und diesmal sogar in der dritthöchsten",
            "findet am kommenden Wochenende",
        ],  # 3 segments
        "without": ["Weitere Infos unter www.itfjuniors.de.", "Liam Gavrielides", "PARTNER"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.oetv.at/news/artikel/d/erfolgreiches-masters-debuet-fuer-taucher-2.html": {
        "file": "oetv.at-taucher.html",
        "author": "Michael Mäser",
        "title": "Erfolgreiches Masters-Debüt für Taucher",
        "date": "2022-02-02",
        "with": [
            "Rollstuhlclub ENJO Vorarlberg erneut",
            "Nachwuchssportler ging es dabei bereits einige Tage",
            "Im Match Tiebreak hatten die Engländer",
        ],  # 3 segments
        "without": [
            "Top Themen der Redaktion",
            "Weltspitze der Junioren angekommen. (Foto: Privat)",
            "feierte indes in der vergangenen Woche internationale",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dtb-tennis.de/Tennis-International/Davis-Cup/News-Features/Davis-Cup-Qualifiers-Kohlmann-nominiert-zwei-Neulinge": {
        "file": "dtb-tennis.de-nominiert.html",
        "author": "DEUTSCHER TENNIS BUND",
        "title": "Davis Cup-Qualifiers: Kohlmann nominiert zwei Neulinge",
        "date": "2022-02-04",
        "with": [
            "Michael Kohlmann hat die Mannschaft für die Davis Cup-Qualifiers",
            "Dass auch Kevin Krawietz und Tim Pütz mit ihrer makellosen",
            "Gespielt werden Dreisatz-Matches mit",
        ],  # 3 segments
        "without": [
            "Kohlmann: „Als nächstes gewinnen wir den Davis Cup“",
            "ZURÜCK NACH OBEN ",
            "DTB nominiert Porsche Nachwuchsteams für 2022",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dsv.de/synchronschwimmen/aktuelles-synchronschwimmen/lesen/?tx_ttnews%5Btt_news%5D=5793&cHash=36febeba61a32f5c94f98d8f59efb32e": {
        "file": "dsv.de-synchronschwimmen.html",
        "author": "",
        "title": "LEVELPÄSSE FÜR DAS SYNCHRONSCHWIMMEN KÖNNEN AB SOFORT BESTELLT WERDEN",
        "date": "2022-02-01",
        "with": [
            "also, dass die filigranen Meerestiere als",
            "Die Kosten für den Levelpass belaufen",
            "dokumentiert. „So haben die Kinder auch etwas",
        ],  # 3 segments
        "without": ["UNSERE PARTNER - SYNCHRONSCHWIMMEN", "KOMMENDE EVENTS", "TERMINE / AUSSCHREIBUNGEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://swim.de/training/lagen-pyramide-mit-ga2/": {
        "file": "swim.de-ga2.html",
        "author": "Jule Radeck",
        "title": "Lagen-Pyramide mit GA2",
        "date": "2022-02-03",
        "with": [
            "Wählen Sie Übungen, bei denen Sie sich",
            "vierten Stufe dürfen Sie entscheiden,",
            "Hälfte der Teilstrecke in",
        ],  # 3 segments
        "without": [
            "studierte Sportwissenschaften, bevor",
            "Starker Serienauftakt in der",
            "Wenn du auf den Abo-Button klickst, verpasst",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://schwimmverband.at/news-artikel tx_news_pi1%5Baction%5D=detail&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Bnews%5D=2236&cHash=892ac1491204c09aa3b2f080298e0218": {
        "file": "schimmverband.at-weltmeisterschaft.html",
        "author": "",
        "title": "FINA Weltmeisterschaften VERSCHOBEN",
        "date": "2022-02-01",
        "with": [
            "Wochen kolportiert wurde, ist",
            "verschoben werden müssen.",
            "Möglichkeiten für Wettkämpfe auf höchstem",
        ],  # 3 segments
        "without": ["Zurück", "logo", "powered by"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dtb.de/weitere-nachrichten/nachrichten/artikel/massnahmen-umgesetzt-und-kulturwandel-angestossen": {
        "file": "dtb.de-kulturwandel.html",
        "author": "",
        "title": "Erste Maßnahmen umgesetzt und Kulturwandel angestoßen",
        "date": "2022-02-03",
        "with": [
            "Verantwortlichen Zeit, eine erste Bilanz zu ziehen",
            "Präventions- und Interventionskonzept zum Schutz",
            "die Ergebnisse aus verschiedenen Perspektiven",
        ],  # 3 segments
        "without": [
            "Weiterführende Links",
            "Kultur- und Strukturwandel im DTB – ein Zwischenfazit",
            "Weitere Informationen hierzu gibt es in Kürze auf der Website des",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.st-georg.de/news/mehr-sport/pferdesport-definitiv-bei-olympia-2028-dabei/": {
        "file": "st-georg.de-olympia.html",
        "author": "Dominique Wehrmann",
        "title": "Pferdesport definitiv bei Olympia 2028 dabei",
        "date": "2022-02-04",
        "with": [
            "Dezember kam die Meldung, dass Reiten",
            "Sportarten dort zu sehen sein werden. Reiten ist",
            "für die Umwelt und die Frage, ob der Sport",
        ],  # 3 segments
        "without": ["Tschüss, Bauchfett!", "(FEI/Christophe Taniere)", "OLYMPISCHE SPIELE"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.reiterrevue.de/ausbildung-und-praxis/fuetterung/heulage-besser-als-ihr-ruf-12842649.html": {
        "file": "reiterrevue.de-heulage.html",
        "author": "Sarah Schnieder",
        "title": "Heulage: Besser als ihr Ruf?",
        "date": "2022-02-03",
        "with": [
            "Pferdefutter einen weniger guten Ruf.",
            ",die die Heulage haltbar machen, die natürli",
            "„atmen“ und gammelt schnell.",
        ],  # 3 segments
        "without": ["Heu ist die Grundlage einer", "und Schimmelpilze. Was Sie bei", "DAS PERFEKTE DINNER"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.pferderevue.at/aktuelles/ausbildung/2022/schluss-mit-poltern--vier-uebungen-fuer-einen-geschmeidigen-sitz.html": {
        "file": "pferderevue.at-übung.html",
        "author": "Pamela Sladky",
        "title": "Schluss mit Poltern: Vier Übungen für einen geschmeidigen Sitz im Trab",
        "date": "2022-01-27",
        "with": [
            "poltert’s bei Ihnen beim Aussitzen?",
            "Pferde selbst in den schwierigsten",
            "Kursen im In- und Ausland gemacht hat. Dieses",
        ],  # 3 segments
        "without": [
            "Große Beckenkreise (links) stabiliseren,",
            "Bei der Beckenkippung nach hinten sinkt der Brustkorb ein",
            "Das Buch & der Online-Lehrgang zum",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.pferd-aktuell.de/news/aktuelle-meldungen/zucht/stellungnahme-der-fn-zum-hlp-pilotjahr-2022": {
        "file": "pferd-aktuell.de-stellungnahmen.html",
        "author": "Uta Helkenberg",
        "title": "Stellungnahme der FN zum HLP-Pilotjahr 2022",
        "date": "2022-02-04",
        "with": [
            "Bereits seit Jahren haben sich die Zuchtverbände",
            "Pferde altersgemäß stattfindet und im Einklang",
            "Veranlagungsprüfung von Hengsten der deutschen",
        ],  # 3 segments
        "without": [
            "zurück zur vorherigen Seite",
            "HLP: Zuchtverbände planen 2022 als Pilotjahr",
            "TSF Dalera BB: Tänzerin im",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.natuerlich-jagd.de/allgemein/neue-djv-online-seminare/": {
        "file": "natuerliche-jagd.de-seminar.html",
        "author": "",
        "title": "Neue DJV-Online-Seminare",
        "date": "2022-02-03",
        "with": [
            "Umgang mit den sozialen Medien sowie",
            "Wie müssen Texte und Fotos dafür",
            "tätige Presseobleute aus den",
        ],  # 3 segments
        "without": [
            "Quelle: Deutscher Jagdverband (DJV)",
            "Neue DJV-Online-Seminare starten im März",
            "Folgen Sie uns",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.eurailpress.de/nachrichten/unternehmen-maerkte/detail/news/hafen-goeteborg-umschlag-auf-rekordniveau.html": {
        "file": "eurailpress.de-rekordniveau.html",
        "author": "",
        "title": "Hafen Göteborg: Umschlag auf Rekordniveau",
        "date": "2022-02-04",
        "with": [
            "Bahnshuttles zurückzuführen, die den Hafen",
            "Der Hafen rechnet wegen des Ausbaus des",
            "unter anderem auf die Einführung",
        ],  # 3 segments
        "without": ["Redaktion Eurailpress", "Artikel", "Unternehmen & Märkte"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://aerobuzz.de/militar/cae-bildet-kuenftig-luftwaffen-piloten-in-bremen-aus/": {
        "file": "aerobuzz.de-bremen.html",
        "author": "BOB FISCHER",
        "title": "CAE bildet künftig Luftwaffen-Piloten in Bremen aus",
        "date": "2022-02-04",
        "with": [
            "GmbH hat sich bei der Ausschreibung",
            "Bremen am Flughafen ein neues Trainingszentrum",
            "Industriepartner die Flugzeuge und die",
        ],  # 3 segments
        "without": [
            "Schon gelesen?",
            "Die CAE GmbH wird Nachwuchspiloten",
            "Luftwaffe hat mit dem Training auf den H145 von NHV begonnen",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.feuerwehrverband.de/dfv-auf-der-vorbereitungstagung-der-interkulturellen-woche/": {
        "file": "feuerwehrverband.de-vorbereitungstagung.html",
        "author": "",
        "title": "DFV auf der Vorbereitungstagung der Interkulturellen Woche",
        "date": "2022-02-04",
        "with": [
            "bundesweite Vorbereitungstagung der Interkulturellen",
            "Faktor 112",
            "Die eigentliche Interkulturelle Woche",
        ],  # 3 segments
        "without": ["DFV-Experte Carsten Schneider", "Nach Anmeldung geht mir eine E-Mail", "Beitrag teilen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.erzbistum-koeln.de/presse_und_medien/magazin/Blasius-Segen-Schutz-vor-Halskrankheiten/": {
        "file": "erzbstbstum-koeln.de-halskrankheiten.html",
        "author": "",
        "title": "Blasius-Segen: Schutz vor Halskrankheiten",
        "date": "2022-01-26",
        "with": [
            "der bekanntesten Legende soll",
            "ab dem Vorabend des Gedenktages des hl. Blasius",
            "Gott Mensch geworden ist, will uns",
        ],  # 3 segments
        "without": [
            "Radiobeitrag zum Blasius-Segen",
            "Der Valentinstag am 14. Februar ist der",
            "Live-Übertragungen der Hl.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bundeskanzleramt.gv.at/bundeskanzleramt/nachrichten-der-bundesregierung/2022/02/bundesministerin-raab-mit-Laendern-und-unternehmen-frauen-und-familienfreundliche-rahmenbedingungen-gestalten.html": {
        "file": "bundeskanzleramt.gv.at-bundesminsterin.html",
        "author": "",
        "title": "Bundesministerin Raab: Mit Ländern und Unternehmen frauen- und familienfreundliche Rahmenbedingungen gestalten",
        "date": "2022-02-01",
        "with": [
            "damit Mütter selbstverständlich",
            "bei der Vereinbarkeit von Beruf",
            '"dass wir einen großen Gap bei den',
        ],  # 3 segments
        "without": ["Nachrichten", "Datenschutzinformation", "Direkt zu"],
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",  # if obvious: DE, CH, AT
    },
    "https://www.be.ch/de/start/dienstleistungen/medien/medienmitteilungen.html?newsID=c3aa546f-24d3-4b47-9c0c-59db58b2f725": {
        "file": "be.ch-impfen.html",
        "author": "",
        "title": "Impfen und Boostern ist bis Ende Februar noch überall möglich",
        "date": "2022-02-08",
        "with": [
            "daher die zusätzlich aufgebauten Impforte",
            "schwere Krankheitsverläufe zu schützen.",
            "eine Kartenansicht umgestellt werden.",
        ],  # 3 segments
        "without": ["Seite teilen", "Inhalt", "Zurück zur Übersicht"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CH",  # if obvious: DE, CH, AT
    },
    "https://www.mix1.de/music/leslie-clio/brave-new-woman/": {
        "file": "mix1.de-clio.html",
        "author": "",
        "title": "Leslie Clio",
        "date": "2022-02-04",
        "with": [
            "Zuvor hatte die Sängerin und Songschreiberin",
            "Clio präsentiert das Album",
            "bisherigen Karriere geschrieben.",
        ],  # 3 segments
        "without": [
            "amazon Tipp: Nutzen Sie die Musik",
            "Tracklist / Infos",
            "Sie möchten wöchtliche Produktvorstellungen?",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.spoe.at/2022/02/04/automatische-mieterhoehung-verhindern/": {
        "file": "spoe.at-mieterhöhung.html",
        "author": "",
        "title": "Rendi-Wagner will automatische Mieterhöhung verhindern",
        "date": "2022-02-04",
        "with": [
            "April zusätzlich aufgrund einer",
            "das sind pro Jahr über 500 Euro an Mehrkosten",
            "Wohnverhältnisse sollen als Ausnahme",
        ],  # 3 segments
        "without": ["Wohnen", "nicht noch zusätzlich", "Preise für das tägliche"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.gitarrebass.de/dm-native-advert/gitarre-bass-02-2022/": {
        "file": "gitarrebass.de-dieneue.html",
        "author": "Redaktion",
        "title": "Gitarre & Bass 02/2022",
        "date": "2022-02-24",
        "with": [
            "Und hat einen neuen Signature-Amp",
            "hat sich Matthias Mineur mit ihm",
            "Vintage-Fender-Telecaster,",
        ],  # 3 segments
        "without": ["Alles Gute zum neuen Jahr", "Schreibe einen Kommentar", "AKTUELLE AUSGABE"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.peta.de/neuigkeiten/veterinaeraemter-2021/": {
        "file": "peta.de-veterinärämter.html",
        "author": "PETA-Team",
        "title": "Die Top 5 und die Flop 5 der deutschen Veterinärämter 2021",
        "date": "2022-02-08",
        "with": [
            "für die Überwachung und den",
            "immer die gesamte Behörde",
            "Unterschreiben Sie unsere Petition",
        ],  # 3 segments
        "without": ["1. Kreisveterinäramt", "VERWANDTE ARTIKEL", "Alle Blogbeiträge zu unseren"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.onmeda.de/krankheiten/coronavirus/paxlovid-id212627/": {
        "file": "omeda.de-paxlovid.html",
        "author": "Brit Weirich",
        "title": "Paxlovid: Grünes Licht für neues Corona-Medikament",
        "date": "2022-01-28",
        "with": [
            "durch das Coronavirus. Erfahren Sie",
            "Präparat namens Molnupiravir brachte",
            "Menschen mit einem erhöhten Risiko",
        ],  # 3 segments
        "without": ["Dieser Text entspricht den", "Covid-19 oder Grippe?", "Tschüss, Bauchfett! Hilfe"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.macwelt.de/ratgeber/iPhone-14-Warum-sich-das-Warten-wirklich-lohnt-11153570.html": {
        "file": "macwelt.de-warten.html",
        "author": "Dennis Steimels",
        "title": "iPhone 14: Warum sich das Warten wirklich lohnt",
        "date": "2022-02-04",
        "with": [
            "Unternehmen auf Features, die wir durchaus",
            "Frontkamera setzen, wie der Experte Ross Young",
            "Eine Periskop-Kamera findet sich bereits",
        ],  # 3 segments
        "without": [
            "Shopping24 Angebot",
            "Eine kleine runde Aussparung für die Facetime-Kamera",
            "Eine kleine runde Aussparung",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.dhz-online.de/de/news/detail/artikel/schwangere-zu-mehr-bewegung-motivieren/": {
        "file": "dhz-online.de-bewegung.html",
        "author": "",
        "title": "Schwangere zu mehr Bewegung motivieren",
        "date": "2022-02-07",
        "with": [
            "schlussfolgern aus ihren Daten, dass körperliche",
            "Schwangerschaft sollte geschärft werden.",
            "durchgeführt wurden waren Bummeln",
        ],  # 3 segments
        "without": [
            "Weitere Meldungen aus",
            "Alle Meldungen der Rubrik",
            "Sylter Hebammen-Notruf wieder erreichbar",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://guten-tach.de/dgb-brueckensperrung-belegt-die-versaeumnisse-der-letzten-jahre/": {
        "file": "guten-tach.de-sperrung.html",
        "author": "Redaktion",
        "title": "DGB: Brückensperrung belegt die Versäumnisse der letzten Jahre",
        "date": "2022-02-08",
        "with": [
            "einhergehenden katastrophalen Auswirkungen",
            "Ihre gemeinsame Aussage lautet:",
            "so die DGB-Vertreter. Auch",
        ],  # 3 segments
        "without": ["HINTERLASSEN SIE EINE ANTWORT", "NOCH MEHR NEWS", "Ingo Degenhardt (DGB Südwestfalen)"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.gdp.de/gdp/gdp.nsf/id/DE_GdP-Vize-Klemmer-Mangelnde-Wertschaetzung-fuer-die-Beschaeftigten-des-oeD?open&ccm=000": {
        "file": "gdp.de-Wertschätzung.html",
        "author": "",
        "title": "GdP-Vize Klemmer: Mangelnde Wertschätzung für die Beschäftigten des öD",
        "date": "2021-10-29",
        "with": ["Potsdam die bisherige Sprachlosigkeit", "Verhandlungsort wollen am", "5 Prozent, mindestens"],  # 3 segments
        "without": ["GdP Länder & Bezirke", "GdP App 2.0", "Foto: GdP/Hagen Immel"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.amnesty.de/allgemein/pressemitteilung/autonome-waffensysteme-gefahr-menschenrechte": {
        "file": "amnesty.de-waffensysteme.html",
        "author": "",
        "title": "Global: Autonome Waffensysteme dürfen nicht über Leben und Tod entscheiden",
        "date": "2021-11-02",
        "with": [
            "die globale Kampagne",
            "wird zu verheerenden Verstößen",
            "nationalen Nichtregierungsorganisationen",
        ],  # 3 segments
        "without": ["Wir respektieren deine Privatsphäre", "Aktuell", "Getty Images"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.for-me-online.de/familie/kinder/tochter-pubertaet": {
        "file": "for-me-online.de-pubertät.html",
        "author": "",
        "title": "Wie spreche ich mit meiner Tochter über ihre Pubertät?",
        "date": "2022-02-17",
        "with": ["Dann ist sie wohl in der Pubertät!", "bei Problemen auch an andere", "Du wirst manchmal sehr"],  # 3 segments
        "without": ["Mehr Inspiration", "Jetzt registrieren", "erhalten Sie exklusive"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.lidl.de/c/nachhaltigkeit-im-onlineshop/s10009344": {
        "file": "lidl.de-nachhaltigkeit.html",
        "author": "",
        "title": "Nachhaltigkeit im Onlineshop",
        "date": "",
        "with": [
            "Wegfall des Lieferscheins und der",
            "geben wir an unsere Kartonagelieferanten weiter.",
            "unserer Kundschaft zukünftig die",
        ],  # 3 segments
        "without": [
            "ZUR NACHHALTIGKEIT IM ONLINESHOP",
            "SCHRITT FÜR SCHRITT ANLEITUNG",
            "Ich habe als Gast bestellt",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.nestle-marktplatz.de/mitmachen/produkttests": {
        "file": "nestle-marktplatz.de-produkttest.html",
        "author": "",
        "title": "Jetzt Produkttester werden - so einfach geht's",
        "date": "",
        "with": [
            "können Sie die Einstellung ganz",
            "auf Foren und Blogs, teilen Sie",
            "Wir zählen auf Ihre Meinung",
        ],  # 3 segments
        "without": ["Aktuelle Produkttests", "NESQUIK Trinkfertig", "Wie läuft ein Produkttest ab"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.theinsidersnet.com/de-de/campaigns/info/55887/welladryhairspraysmf2202.htm": {
        "file": "theinsidersnet.com-wellaflex.html",
        "author": "",
        "title": "Wellaflex – Schnell aufgefrischtes Haar in jeder Situation mit dem 10-in-1 Trockenshampoo",
        "date": "",
        "with": [
            "Dann haben wir genau das richtige für Dich!",
            "Du möchtet Deinen Look nach",
            "Dose kräftig schütteln. Sprühkopf",
        ],  # 3 segments
        "without": ["Start", "das Influencer-Marketingnetzwerk", "eine Kampagne mit uns"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.arbeitsagentur.de/news/arbeitsmarkt-2022": {
        "file": "arbeitsagentur.de-arbeitsmarkt.html",
        "author": "",
        "title": "Arbeitslosenquote & Arbeitslosenzahlen 2022",
        "date": "2022-02-01",
        "with": [
            "sagte der Vorstand Regionen der Bundesagentur",
            "Beschäftigung nahm saisonbereinigt von Oktober",
            "Anzeigen wurde vom 1. bis einschließlich",
        ],  # 3 segments
        "without": [
            "Auf der Seite Aktuelle Meldungen 2021",
            "auf der Seite Entwicklung des",
            "Arbeitsmarkts in den Vorjahren lesen",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.iwrpressedienst.de/energie-themen/pm-7663-iwes-und-nordex-group-intensivieren-zusammenarbeit-bei-netzintegration-von-windenergieanlagen": {
        "file": "iwr.de.IWRpressedienst.Nordex.html",
        "author": "Nordex SE",
        "title": "IWES und Nordex Group intensivieren Zusammenarbeit bei Netzintegration von Windenergieanlagen",
        "date": "2022-11-22",
        "with": [
            "Gemeinsam entwickelter Versuchsstand",
            "Michael Franke, Vice President",
            "Die Nordex Group im Profil",
        ],  # 3 segments
        "without": ["Telefon:", "Online-Pressemappe", "- alle Pressemitteilungen der"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.bmbf.de/bmbf/de/forschung/energiewende-und-nachhaltiges-wirtschaften/energiewende-und-nachhaltiges-wirtschaften_node.html": {
        "file": "bmbf.de.energiewende.html",
        "author": "",
        "title": "Energiewende, Mobilität und nachhaltiges Wirtschaften",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Ländliche Regionen schrumpfen",
            "Die Bundesregierung investiert",
            "mit vielfältigen Forschungsprojekten",
        ],  # 3 segments
        "without": ["Thinkstock", "Chancen für eine biobasierte", "Folgen Sie uns"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.zfk.de/energie/waerme/waermepumpenmarkt-waechst-um-42-prozent-gegenueber-dem-vorjahr": {
        "file": "zfk.de.waermepumpen.html",
        "author": "",
        "title": "Wärmepumpenmarkt wächst um 42 Prozent gegenüber dem Vorjahr",
        "date": "2022-12-06",
        "with": ["Wärmepumpen boomen", "Trotz schwieriger", "Gas rückläufig"],  # 3 segments
        "without": ["Mehr zum Thema", "ZfK.de > Energie > Wärme", "AGB Impressum Datenschutz"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://internetchemie.info/news/2021/jan21/heliumkerne-in-zinn-atomen-entdeckt.php": {
        "file": "internetchemie.info.Heliumkerne.html",
        "author": "",
        "title": "Heliumkerne in Zinn-Atomen entdeckt",
        "date": "2021-01-17",
        "with": ["Darmstadt - Januar 2021", "Im Detail:", "Die von Tanaka et al"],  # 3 segments
        "without": ["Zusatzinformationen:", "About", "Aktualisiert am"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.enbw.com/unternehmen/presse/buergerbeteiligung-fuer-den-windpark-steinheim-startet.html": {
        "file": "enwb.com.windpark.steinheim.html",
        "author": "EnBW Energie Baden-Württemberg AG",
        "title": "Umweltfreundliche Geldanlage: Bürgerbeteiligung am Windpark Steinheim",
        "date": "2022-12-06",
        "with": ["Steinheim, Nordrhein-Westfalen/Stuttgart", "Mit der Bürgerbeteiligung", "Über die digitale"],  # 3 segments
        "without": [
            "Die EnBW Energie Baden-Württemberg AG ist:",
            "Das könnte Sie auch interessieren",
            "Zurück zum Newsroom",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.oekologisch-bauen.info/haustechnik/elektro-fotovoltaik/initiative-energieeffizienz/": {
        "file": "oekologisch-bauen.info.energieeffizienz.html",
        "author": "Oekologisch-bauen",
        "title": "Kostenloser Stromcheck für private Haushalte",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Mit der Initiative EnergieEffizienz",
            "Der Stromcheck",
            "Weitere Informationen rund um das Thema",
        ],  # 3 segments
        "without": ["RATGEBER FIRMEN NEWS FORUM", "KURZ NOTIERT", "Impressum"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://orsted.de/gruene-energie/gruener-wasserstoff/potenzial": {
        "file": "orsted.de.gruener-Wasserstoff.html",
        "author": "Ørsted",
        "title": "Das Potenzial von grünem Wasserstoff",
        "date": "",  # YYYY-MM-DD
        "with": ["Das „erneuerbare Molekül“:", "Wasserstoff als Energieträger", "E-Fuels als Lösung"],  # 3 segments
        "without": ["Folgen Sie uns auf", "Ørsted glaubt an eine Welt", "Home"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.offshore-stiftung.de/offshore-windenergie": {
        "file": "offshore-stiftung.de.offshore-windenergie.html",
        "author": "Offshore-Stiftung ",
        "title": "OFFSHORE-WINDENERGIE SAUBERER STROM VOM MEER",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Windparks in Nord- und Ostsee",
            "EXTREME BEDINGUNGEN AUF SEE",
            "OFFSHORE-WINDENERGIE ALS BUNDESWEITER JOBMOTOR",
        ],  # 3 segments
        "without": ["VERANSTALTUNGEN", "PROJEKTE", "BLEIBEN SIE INFORMIERT"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://battery-news.de/index.php/2022/12/06/ultium-cells-erhoeht-gigafactory-kapazitaet-in-tennessee/": {
        "file": "battery-news.de.ultium-cells.html",
        "author": "Die Redaktion von Battery News",
        "title": "Ultium Cells erhöht Gigafactory-Kapazität in Tennessee",
        "date": "2022-12-06",
        "with": [
            "Ultium Cells investiert",
            "Weitere US-Zellprojekte im Aufbau",
            "Gesamtvolumen über 130 Gigawattstunden",
        ],  # 3 segments
        "without": ["Artikel teilen", "SUCHE", "NEUESTE BEITRÄGE"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.techfieber.de/green/2022/12/06/energiesparen-bei-cern-teilchenbeschleuniger-macht-winterpause/ ": {
        "file": "greentech.live.energiesparen bei cern.html",
        "author": "Greentech.LIVE Redaktion",
        "title": "Energiesparen bei Cern: Teilchenbeschleuniger macht Winterpause",
        "date": "2022-12-06",
        "with": ["Um Strom zu sparen", "Einschränkung ist «verschmerzbar»", "Sparen durch Wartung"],  # 3 segments
        "without": ["Greentech.LIVE c/o Innoport RT", "Name *", "Kontakt & Impressum"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.forstpraxis.de/pilotprojekt-heizen-mit-pellets-aus-laub-so-funktioniert-es-21677": {
        "file": "forstpraxis.de.palletsauslaub.html",
        "author": "Amelie Siekmann",
        "title": "Pilotprojekt Heizen mit Pellets aus Laub: So funktioniert es",
        "date": "2022-12-04",
        "with": [
            "In Reichenbach in der Lausitz",
            "Ein Antrag für Fördermittel ist gestellt",
            "„Man kann diese Pellets genauso",
        ],  # 3 segments
        "without": ["AUCH INTERESSANT", "FORST&TECHNIK", "KLEINANZEIGEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.chemietechnik.de/sicherheit-umwelt/covestro-startet-neue-forschungsgruppe-fuer-biotechnologie-843.html": {
        "file": "chemietechnik.de.forschungsgruppe fuer biotechnologie.html",
        "author": "Jona Göbelbecker",
        "title": "Covestro startet neue Biotechnologie-Forschungsgruppe",
        "date": "2022-12-01",
        "with": [
            "Der Kunststoff-Hersteller Covestro will",
            "Neues Labor in Leverkusen eingerichtet",
            "Auch HDMA mithilfe von Biotechnologie produziert",
        ],  # 3 segments
        "without": ["Auch interessant", "Diskutieren Sie mit", "Aktuellste Beiträge"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.unendlich-viel-energie.de/themen/strom/umfrage-zur-strompreisbremse-oekostromkundinnen-besonders-sensibel-fuers-stromsparen": {
        "file": "unendlich-viel-energie-strompreisbremse.html",
        "author": "Dr. Tim Loppe",
        "title": "Umfrage zur Strompreisbremse: Ökostromkund*innen besonders sensibel fürs Stromsparen",
        "date": "2022-11-22",
        "with": [
            "Düsseldorf, 22. November 2022 -",
            "„Die große Mehrheit der Bevölkerung",
            "Das Marktforschungsunternehmen YouGov",
        ],  # 3 segments
        "without": ["Diesen Artikel teilen", "Newsletter November", "Suche"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.solarserver.de/2022/12/01/groesstes-solarthermisches-kraftwerk-der-welt-entsteht-in-dubai/ ": {
        "file": "Solarserver.de.solarthermisches kraftwerk dubai.html",
        "author": "SolarServer",
        "title": "Größtes solarthermisches Kraftwerk der Welt entsteht in Dubai",
        "date": "2022-12-01",
        "with": [
            "Shanghai Electric baut",
            "Die PV-Module mit insgesamt 250",
            "Für das Projekt werden etwa 560.000 Tonnen",
        ],  # 3 segments
        "without": ["Solarserver Newsletter", "Solarserver Stellenmarkt", "teilen twittern E-Mail"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.iass-potsdam.de/de/forschungsbereich/energiewende-und-gesellschaftlicher-wandel ": {
        "file": "iass-potsdam.de.energiewende.html",
        "author": "Dr. Rainer Quitzow",
        "title": "Energiewende und gesellschaftlicher Wandel",
        "date": "",  # YYYY-MM-DD
        "with": ["Die Dekarbonisierung der Energieversorgung", "Vision", "Mission"],  # 3 segments
        "without": ["FORSCHUNGSGRUPPEN", "Weitere Beiträge anzeigen", "NEWSLETTER"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.zvei.org/presse-medien/pressebereich/messstellenbetriebsgesetz-endlich-klarheit-geschaffen ": {
        "file": "zvei.org.messestellenbetriebsgesetz.html",
        "author": "Zvei",
        "title": "Messstellenbetriebsgesetz: Endlich Klarheit geschaffen",
        "date": "2022-12-02",
        "with": ["Wolfgang Weber, Vorsitzender", "Insbesondere ist hervorzuheben", "Der Entwurf kommt dennoch"],  # 3 segments
        "without": ["Weiterführende Informationen", "Folgen Sie uns", "Zurück zur Übersicht"],  # 3 segments
        "comments": [],  # 0 or 3 segments
    },
    "https://www.energiezukunft.eu/erneuerbare-energien/biomasse/bundesregierung-drosselt-bioenergie-branche-protestiert/": {
        "file": "energiezukunft.eu.bioenergie.html",
        "author": "",
        "title": "Bundesregierung drosselt Bioenergie, Branche protestiert",
        "date": "2022-11-29",
        "with": [
            "Am vergangenen Freitag",
            "Die Abschöpfung von Erlösen",
            " Die Bioenergieverbände im Hauptstadtbüro",
        ],  # 3 segments
        "without": ["Mehr zum Thema", "TOP-THEMEN", "Magazine"],  # 3 segments
        "comments": ["Ich bin schon vor Wochen", "Entweder ist es die Unfähigkeit", "Ein Tip: Es sollten"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.erneuerbareenergien.de/technologie/offshore-wind/usa-kalifornien-verpachtet-seeboden-zur-entwicklung-von-floating-offshore-windfarmen.": {
        "file": "erneuerbareenergien.de.seeboden.html",
        "author": "Tilman Weber",
        "title": "Kalifornien verpachtet Seeboden zur Entwicklung von Floating-Offshore-Windfarmen",
        "date": "2022-12-10",
        "with": ["Bei den siegreichen Bietern", "Wo die Windfarmentwickler", "Außer in den Vereinigten Staaten"],  # 3 segments
        "without": ["Autoren:", "Tags", "ANMELDUNG UND REGISTRIERUNG"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.wind-energie.de/presse/pressemitteilungen/detail/endlich-mehr-beschleunigung-wagen/": {
        "file": "wind-energie.de.beschleunigung.html",
        "author": "",
        "title": "Endlich mehr Beschleunigung wagen!",
        "date": "2022-12-08",
        "with": [
            "Innerhalb ihres ersten Jahres hat",
            "Eine Erhebung der Fachagentur Windenergie an Land",
            "Zu weiteren Komplikationen trägt",
        ],  # 3 segments
        "without": ["Ihr Ansprechpartner für Pressefragen", "Tel.:", "EUREF-Campus 16"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.dvfg.de/presse/pressemeldung/2022/11/29/verbrauchertipp-an-oder-aus-so-heizen-sie-waehrend-des-weihnachtsurlaubs-effizient": {
        "file": "dvg.de.weihnachtsurlaub.html",
        "author": "",
        "title": "An oder aus? So heizen Sie während des Weihnachtsurlaubs effizient",
        "date": "2022-29-11",
        "with": [
            "Weihnachten ist Reisezeit",
            "Thermostate runterdrehen,",
            " Smarten Thermostaten die Steuerung überlassen",
        ],  # 3 segments
        "without": ["zurück zur Listenansicht", " 2022 Deutscher Verband Flüssiggas e.V.", "Kontakt"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.cleanthinking.de/oranger-wasserstoff-erdkruste/": {
        "file": "cleanthinking.de.oranger-wasserstoff.html",
        "author": "Martin Jendrischik",
        "title": "Oranger Wasserstoff: Der Traum vom erneuerbaren Gas aus der Erdkruste",
        "date": "2022-12-12",
        "with": [
            "Französische Forscher wollen",
            "Grüner Wasserstoff und seine erneuerbaren",
            "Oranger Wasserstoff aus der Erdkruste:",
        ],  # 3 segments
        "without": ["HINTERLASSE EINE ANTWORT", "Diese Website verwendet Akismet", "Buch-Tipp:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://reset.org/du-wirst-nicht-glauben-wie-viel-co2-clickbait-websites-produzieren/": {
        "file": "reset.org.clickbait.html",
        "author": "Mark Newton",
        "title": "Du wirst nicht glauben, wie viel CO2 Clickbait-Websites produzieren!",
        "date": "2022-12-12",
        "with": [
            "Schlagzeilen wie die dieses Artikels",
            "Die Studie von Ebiquity und Scope3 legt",
            "Im Gegensatz dazu lag der CO2PM für",
        ],  # 3 segments
        "without": ["MARKIERT MIT", "DAS KÖNNTE DICH AUCH INTERESSIEREN", "MEIST GELESEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://mpimet.mpg.de/kommunikation/aktuelles/single-news/neuer-blick-auf-das-blue-marble-foto-icon-simuliert-das-gekoppelte-klimasystem-mit-1-km-aufloesung.": {
        "file": "mpimet.de.klimasystem.html",
        "author": "",
        "title": "Neuer Blick auf das „Blue Marble“-Foto: ICON simuliert das gekoppelte Klimasystem mit 1 km-Auflösung",
        "date": "2022-12-07",
        "with": [
            "Die frühen 1970er Jahre werden oft",
            "Während wir über die Ursprünge",
            "Die Daten werden mithilfe von NVIDIA",
        ],  # 3 segments
        "without": ["Weitere Informationen:", "Kontakt:", "MPI Website /Kommunikation /Aktuelles /Single News"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.recyclingmagazin.de/2022/12/12/europas-erste-lithium-rueckgewinnungsanlage-in-nrw/": {
        "file": "recyclingmagazin.de.lithium.html",
        "author": "",
        "title": "Europas erste Lithium-Rückgewinnungsanlage in NRW",
        "date": "2022-12-12",
        "with": [
            "Die Anlage mit einem geplanten",
            "Seit etwa 8 Jahren",
            "Accurec wird mit der HydroLiC-Technologie",
        ],  # 3 segments
        "without": ["TEILEN", "VERWANDTE ARTIKEL", "Letzte Meldungen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.helmholtz-klima.de/aktuelles/kein-kipppunkt-zugunsten-des-klimaschutzes": {
        "file": "helmholtz-klima.de.kipppunkt.html",
        "author": "Christian Mihatsch",
        "title": "Kein Kipppunkt zugunsten des Klimaschutzes",
        "date": "",  # YYYY-MM-DD
        "with": ["„Die multilaterale Diplomatie", "Der Fonds hat", "Christoph Bals von der Umweltorganisation"],  # 3 segments
        "without": ["MEHR ZUM THEMA", "NEWSLETTERANMELDUNG", "AUF DEM LAUFENDEN BLEIBEN!"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.baumev.de/News/10365/TransformationslaborErnhrung.html": {
        "file": "baumev.de.Transformationslabor.html",
        "author": "Jan Koch",
        "title": "TRANSFORMATIONSLABOR ERNÄHRUNG",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Die Ernährungswirtschaft birgt",
            "Ausschlaggebend für die Initiative",
            "Im Fokus des Projekts steht die Frage",
        ],  # 3 segments
        "without": ["Kontakt:", "Ansprechpartnerin zum", "KLIMANEUTRALITÄT VON UNTERNEHMEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://daheim-solar.de/lexikon/batteriespeicher/": {
        "file": "daheim-solar.de.batteriespeicher.html",
        "author": "Daheim Solar",
        "title": "Batteriespeicher",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Der am häufigsten für Solarbatterien",
            "Dies ist vor allem im stationären Betrieb",
            "Lithium-Ionen-Akkumulatoren werden",
        ],  # 3 segments
        "without": ["Zurück zum Lexikon", "Zu allen Beiträgen", "Kontakt"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.dvgw.de/blog/gas/welche-heizung-ist-klimafreundlich-und-zukunftstauglich": {
        "file": "dvgw.de.heizug.html",
        "author": "",
        "title": "Welche Heizung ist klimafreundlich und zukunftstauglich?",
        "date": "2021-11-19",
        "with": [
            "In den Heizungen unserer",
            "Von den verschiedenen Heizsystemen im Haus",
            "Dazu kommt, dass nicht jedes Gebäude für",
        ],  # 3 segments
        "without": ["Weitere Informationen", "Ansprechpartner", "Bleiben Sie auf dem Laufenden"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://fluessiggas.de/aktuelles/dimethylether/": {
        "file": "fluessiggas.de.dimethylether.html",
        "author": "Fluessiggas.de",
        "title": "DIMETHYLETHER: ALTERNATIVE FÜR DAS HEIZEN DER ZUKUNFT",
        "date": "2022-10-24",
        "with": [
            "Die Nachfrage nach erneuerbaren Energien",
            "Verbraucher in Deutschland können bereits",
            "Die Aussicht, dass erneuerbarer Dimethylether",
        ],  # 3 segments
        "without": ["Verwandte Themenbereiche", "Highlights aus dem Bereich:", "Beitrag teilen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.energieverbraucher.de/de/preise__312/NewsDetail__18725/.": {
        "file": "energieverbraucher.de.energie.html",
        "author": "Leonora Holling",
        "title": "Energiepreiskrise: Entlastungen und Rechte auf einen Blick",
        "date": "2022-11-21",
        "with": [
            "(21. November 2022) Energieverbraucher erhalten",
            "Zwei weitere Umlagen treffen Verbraucher",
            "Auf Grundlage von § 3 der Allgemeinen Bedingungen",
        ],  # 3 segments
        "without": ["weitere Inhalte zu »Preise«", "MITGLIED WERDEN", "ÜBER UNS"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.sonnenenergie.de//index.php?id=30&no_cache=1&tx_ttnews%5Btt_news%5D=477": {
        "file": "sonnenernergie.de.Windrebell.html",
        "author": "Götz Warnke",
        "title": "Der WindRebell",
        "date": "",  # YYYY-MM-DD
        "with": [
            "MIT KLEINWINDKRAFT ZU MEHR AUTARKIE:",
            "Ebenso wichtig wie die großräumige",
            "Ob eine Kleinwindenergieanlage",
        ],  # 3 segments
        "without": ["Von:", "Meist gesucht:", "Copyright 2018 - "],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://vorangedacht.de/umwelt-und-klima/ueber-kohleausstieg-kernkraftwerke-und-erneuerbare-energien/": {
        "file": "vorangedacht.de.kohleausstieg.html",
        "author": "",
        "title": "Über Kohleausstieg, Kernkraftwerke und Erneuerbare Energien",
        "date": "2022-10-13",
        "with": [
            "Bundeswirtschaftsminister Habeck kündigte",
            "Erneuerbare Energien sind volatil",
            "Eine überwältigende Mehrzahl der Klimaschützer",
        ],  # 3 segments
        "without": ["Mehr zum Thema:", "Zum Newsletter anmelden", "Gründe für Atomkraftwerke"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.verbaende.com/news/pressemitteilung/das-aendert-sich-im-jahr-2023-die-wichtigsten-aenderungen-fuer-verbraucherinnen-im-ueberblick-151642/": {
        "file": "verbaende.com.2023.html",
        "author": "VZS",
        "title": "Das ändert sich im Jahr 2023: Die wichtigsten Änderungen für Verbraucher*innen im Überblick",
        "date": "2022-12-12",
        "with": [
            "(Leipzig) - Von Preisbremsen",
            "Private Solaranlagen:",
            "Mehrwegpflicht fürs Essen zum Mitnehmen:",
        ],  # 3 segments
        "without": ["Weitere Pressemitteilungen dieses Verbands", "Folgen Sie uns", "NEWS TEILEN:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.agrarheute.com/energie/heizen-abfallholz-erfindung-funktioniert-601129": {
        "file": "agrarheute.com.abfallholz.html",
        "author": "Amelie Siekmann",
        "title": "Heizen mit Abfallholz: Mit dieser Erfindung funktioniert es",
        "date": "2022-12-11",
        "with": ["Auch dünne Äste,", "Zunächst steckt er die", "Die Hydraulikpresse im Inneren"],  # 3 segments
        "without": ["Mehr zum Thema", "Hier ist Ihre Meinung gefragt", "Wir informieren Sie täglich"],  # 3 segments
        "comments": ["Moin vom Fjord", "Zum andern ist", "Gerne Nachfragen"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.proplanta.de/agrar-nachrichten/energie/bayern-fordert-hoehere-erloesobergrenzen-fuer-bioenergie_article1670823962.html": {
        "file": "proplanta.de.erloesobergrenze.html",
        "author": "",
        "title": "Bayern fordert höhere Erlösobergrenzen für Bioenergie",
        "date": "2022-12-12",
        "with": [
            "Wie der Ressortchef am Dienstag ",
            "Unterdessen pochte die Leiterin",
            "Derweil würde die vorgeschlagene",
        ],  # 3 segments
        "without": ["Weitere Artikel zum Thema", "Kommentierte Artikel", "Mehr zum Thema"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.heizung.de/waermepumpe/wissen/eignet-sich-eine-waermepumpe-im-altbau.html": {
        "file": "heizung.de.waermepumpen.html",
        "author": "Alexander Rosenkranz",
        "title": "Eignet sich eine Wärmepumpe im Altbau?",
        "date": "2022-03-09",
        "with": [
            "Wärmepumpenheizungen setzen",
            "Wärmepumpenanlagen gelten als",
            "Erreichen lässt sich eine niedrige Vorlauftemperatur",
        ],  # 3 segments
        "without": ["Mehr zu Wärmepumpe", "Neueste Artikel", "Heizung.de Top Themen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.chemie.de/news/1178836/empa-spin-off-revolutioniert-die-messung-von-treibhausgasen-und-luftschadstoffen.html": {
        "file": "chemie.de.spin-off.html",
        "author": "Empa",
        "title": "Empa-Spin-off revolutioniert die Messung von Treibhausgasen und Luftschadstoffen",
        "date": "2022-12-12",  #
        "with": [
            "Das im Februar 2018 als Spin-off der Empa ",
            "Die von Hundt und Aseev",
            "Und im Oktober verlieh Innosuisse",
        ],  # 3 segments
        "without": [
            "Fakten, Hintergründe, Dossiers",
            "Start-ups",
            "Empa (Eidgenössische Materialprüfungs- und Forschungsanstalt)",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.scinexx.de/news/energie/ammoniak-spaltung-durch-leds-statt-hitze/": {
        "file": "scinexx.com.ammoniak.html",
        "author": "Nadja Podbregar",
        "title": "Ammoniak-Spaltung durch LEDs statt Hitze",
        "date": "2022-11-28",
        "with": [
            "Wegbereiter zu „grünem“ Wasserstoff?",
            "Eine günstigere Alternative",
            "„Dies ist der erste Bericht in der Fachliteratur,",
        ],  # 3 segments
        "without": ["Zurück zur Startseite", "Das könnte Sie auch interessieren", "In den Schlagzeilen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.ingenieur.de/technik/fachbereiche/energie/kernfusion-kann-die-energiequelle-der-sterne-energieprobleme-aus-der-welt-schaffen/": {
        "file": "ingenieur.de.kernfusion.html",
        "author": "Alexandra Illina",
        "title": "Kernfusion: Kann „die Energiequelle der Sterne“ Energieprobleme aus der Welt schaffen?",
        "date": "2022-12-12",
        "with": [
            "Überall auf der Welt forscht man",
            "Das NIF-Team hat",
            "Kleiner Schritt zu einer grünen Energiequelle",
        ],  # 3 segments
        "without": ["THEMEN IM ARTIKEL", "TOP 5 ENERGIE", "12.12.2022, 08:30 Uhr"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.greenpeace.de/engagieren/nachhaltiger-leben": {
        "file": "greenpeace.de.nachhaltigleben.html",
        "author": "Greenpeace",
        "title": "Nachhaltig leben",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Jede:r Deutsche kauft im Schnitt ",
            "Für vier große industriell-genutzten Materialströme",
            "Als Gesellschaft können wir die Verantwortung",
        ],  # 3 segments
        "without": ["PETITION", "Mehr zu Klima und Konsum", "Zum Weiterlesen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.topagrar.com/energie/news/schnee-belastet-module-10558804.html": {
        "file": "topagrar.com.schnee.solat.html",
        "author": "Hinrich Neumann",
        "title": "Schnee belastet Solarmodule - Warum nur Profis zum Entfernen ran sollten",
        "date": "2022-12-10",
        "with": ["Eine Schneedecke auf der", "Das Gewicht belastet", "Verschiedene Experten warnen "],  # 3 segments
        "without": ["DIE REDAKTION EMPFIEHLT", "Meistgelesene Artikel", "Meistdiskutierte Artikel"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://mitvergnuegen.com/2022/ausflug-herbst-um-berlin/": {
        "file": "mitvergnuegen.de.herbst.html",
        "author": "Marina Beuerle",
        "title": "11 schöne Ausflugsziele für den Herbst rund um Berlin",
        "date": "",  # YYYY-MM-DD
        "with": ["Zugegeben, wir", "Am Werbellinsee gibt", "Raus aus den Klamotten und rein"],  # 3 segments
        "without": ["DIESE ARTIKEL KÖNNTEN DICH INTERESSIEREN", "ZURÜCK ZUR STARTSEITE", "Kategorien"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://goodnight.at/magazin/kultur/3017-konzert-highlights-im-november-2022": {
        "file": "goodnight.at.konzert.html",
        "author": "Johanna Kropfitsch",
        "title": "Konzert-Highlights im November 2022",
        "date": "2022-11-02",
        "with": ["Mit dem im August 2022", "Seit 2012 bringen Kraftklub", "Ein bisschen Old-School Hip-Hop,"],  # 3 segments
        "without": ["Beliebteste Artikel", "Facebook", "Mediadaten"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "AT",
    },
    "https://www.thisisjanewayne.com/news/2022/09/14/von-bauchgeburten-und-falschen-gefuehlen-im-richtigen-sein/": {
        "file": "thisisjanewayne.com.bauch.html",
        "author": "Nike Jane",
        "title": "Warum ich lieber „Bauchgeburt“ statt Kaiserschnitt sage.",
        "date": "2022-09-14",
        "with": ["„Geht los!“, schrie", "Benötigen Sie psychologische", "Während der Französischen Revolution"],  # 3 segments
        "without": ["TAGS:", "Mehr von", "11 KOMMENTARE"],  # 3 segments
        "comments": ["Hab Rotz und", " Ich finde es komisch, dass", "Tolle Worte."],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://frolleinherr.com/thoughts/kolumne-lost-aber-immer-noch-da/ ": {
        "file": "frolleinherr.com.lost.html",
        "author": "Karoline Herr",
        "title": "SUNDAY THOUGHTS: EIN WENIG LOST, ABER IMMER NOCH DA!",
        "date": "2022-11-20",
        "with": ["Einige sehr aufmerksame", "Es ist so: Mein", "An dieser Stelle sei gesagt:"],  # 3 segments
        "without": ["11 Antworten zu", "Impressum", "Schon gelesen?"],  # 3 segments
        "comments": [
            "danke für deine Ehrlichkeit!",
            "Ich bin so froh,",
            "selten hat mich ein Kommentar so gefreut",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.amazedmag.de/white-passing-oder-mein-leben-irgendwo-dazwischen/": {
        "file": "amazedmag.de.meinleben.html",
        "author": "Fatima",
        "title": "White Passing oder (m)ein Leben irgendwo dazwischen",
        "date": "2022-12-06",
        "with": [
            "Ich wollte diesen Text schon",
            "Heute sehe ich das anders.",
            "„Da wo du herkommst, bin ich zu weiß",
        ],  # 3 segments
        "without": ["Sharing is caring", "Ähnliche Artikel", "ABOUT"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.refinery29.com/de-de/single-weihnachten-fragen": {
        "file": "refinery29.com.single.html",
        "author": "SADHBH O'SULLIVAN, ELISABETH KOCHAN",
        "title": "Ich habe es satt, an Weihnachten gefragt zu werden, wieso ich Single bin",
        "date": "2022-12-12",
        "with": [
            "„Meine letzte ernste Beziehung ging ",
            "Wenn dir Leute Fragen zum Dating",
            "Während der Feiertage gibt es zahlreiche",
        ],  # 3 segments
        "without": ["Lust auf mehr?", "The Conversation", "More from Relationships"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://rosa-mag.de/sheila-atim-the-woman-king-zeigt-weibliche-staerke-in-all-ihren-facetten/": {
        "file": "rosa-mag.de.womanking.html",
        "author": "Celia Parbey",
        "title": "Sheila Atim: „The Woman King zeigt weibliche Stärke in all ihren Facetten“",
        "date": "2022-10-06",
        "with": [
            "Gerade ist der Hollywood Blockbuster",
            "Atim: The Woman King zeigt weibliche Stärke",
            "Die Stunt-Szenen im Film sind",
        ],  # 3 segments
        "without": ["Unterstütze RosaMag ", "Wähle deine Mitgliedschaft", "RELATED POSTS"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://theoriginalcopy.de/editors-letter-baby/": {
        "file": "theoriginalcopy.de.baby.html",
        "author": "Swantje Bernsmann",
        "title": "Editor’s Letter: bye OC Baby, hi Bernsi Baby!",
        "date": "2022-08-11",
        "with": ["Lange habe ich diesen", "Während ich diese Wort", "Bis dahin halte ich Euch auf Instagram "],  # 3 segments
        "without": ["Teilen", "Schreibe einen Kommentar", "Copyright 2022"],  # 3 segments
        "comments": ["Dir und Timo alles Gute", "Hach Swantje.", "Wow so toll geschrieben!"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.galore.de/kultur/artikel/30-11-buch-der-woche-nikole-hannah-jones-hrsg-o-1619": {
        "file": "galore.de.buch.html",
        "author": "Marina Mucha",
        "title": "30.11. | Buch der Woche",
        "date": "2022-11-30",
        "with": ["Was als Sonderausgabe der", "Die fundierten wie komplexen", "Nikole Hannah-Jones (Hrsg.)"],  # 3 segments
        "without": ["Abo", "Facebook", "Interviews"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://beige.de/artikel/reisen-travel-provence-suedfrankreich-tipps": {
        "file": "beige.de.suedfrankreich.html",
        "author": "Marie Jaster",
        "title": "Provence Travel Guide",
        "date": "2022-11-07",
        "with": ["Die Provence kann etwas,", "Als wir uns spontan entschieden,", "Dementsprechend haben wir"],  # 3 segments
        "without": ["Die Karte zum Abspeichern:", "Newsletter", "Datenschutz"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.urania.de/die-freiheit-der-planung": {
        "file": "urania.de.freiheit.html",
        "author": "Reiner Nagel",
        "title": "Die Freiheit der Planung",
        "date": "2022-25-10",
        "with": [
            "Was haben fahrerlose Autos und Pakete ",
            "Öffentliche Räume sind",
            "Städtebau ist planungsrechtlich die Art",
        ],  # 3 segments
        "without": ["Diese Seite teilen", "Blog", "Cookie-Einstellungen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.wmn.de/health/body-fitness/staendig-muede-an-diesen-krankheiten-koennte-es-liegen-id459844": {
        "file": "wmn.de.krankheit.html",
        "author": "Nadja Demel",
        "title": "",
        "date": "2022-12-13",
        "with": [
            "Leidest du an ständiger Müdigkeit",
            "Ständige Müdigkeit kann belastend sein",
            "um eine Diagnose zu bekommen,",
        ],  # 3 segments
        "without": ["Markiert:", "Kontakt", "BODY & FITNESS"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.gofeminin.de/horoskop/liebeshoroskop-januar-2023-s4055611.html": {
        "file": "gofeminin.de.horoskop.html",
        "author": "Sonia Mevißen",
        "title": "Liebeshoroskop Januar 2023: Das sagen die Sterne über euer Liebesglück",
        "date": "2023-01-01",
        "with": ["Zeit für große Gefühle?", "Im Januar sind Sie verträumt", "Doch nicht nur im Bett klappt es"],  # 3 segments
        "without": ["Folge uns überall!", "wir haben viele spannende Themen", "Auch lesen:"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.fitforfun.de/news/studie-zeigt-zwei-beliebte-lebensmittel-koennen-gegen-soziale-aengste-helfen-531297.html": {
        "file": "fitforfun.de.sozialeaengste.html",
        "author": "Mathilda Trausch",
        "title": "Studie zeigt: Zwei beliebte Lebensmittel können gegen soziale Ängste helfen",
        "date": "2022-12-26",  # YYYY-MM-DD
        "with": [
            "Schon länger ist bekannt:",
            "Da der Darm und die Psyche eng",
            "Fermantation ist die chemische Umwandlung",
        ],  # 3 segments
        "without": ["Quellen ausblenden", "Top-Themen bei FIT FOR FUN", "Meistgelesen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.womenshealth.de/abnehmen/weihnachten-nicht-zunehmen/": {
        "file": "womenshealth.de.weihnachten.html",
        "author": "Tina Klostermeier",
        "title": "Weihnachten nicht zunehmen: 10 Tipps für ein schlankes Fest",
        "date": "2022-12-15",  # YYYY-MM-DD
        "with": [
            "Durchschnittlich ein Kilo mehr",
            "In der Folge testeten die",
            "Normalerweise ist es nicht ratsam",
        ],  # 3 segments
        "without": ["Meist gelesen", "Abnehmen", "Zur Startseite"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.madymorrison.com/yoga/energy-rising": {
        "file": "madymorrsion.com.energy.html",
        "author": "Mady",
        "title": "Energy Rising – 33 Tage Yoga Challenge",
        "date": "2022-04-03",  # YYYY-MM-DD
        "with": [
            "Der Frühling steht bevor,",
            "Für die Energy Rising – Challenge nutzen wir",
            "Nun wünsch ich dir aber ganz viel Spaß",
        ],  # 3 segments
        "without": ["YOU MAY ALSO LIKE", "YOGA", "FOOD"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.emotion.de/psychologie-partnerschaft/persoenlichkeit/selfcare-fuer-faule-99-wege-dein-selbstbewusstsein-aufzupaeppeln": {
        "file": "emotion.de.selfcare.html",
        "author": "Emotion",
        "title": "Tut so gut: 99 Wege, heute Selfcare zu betreiben",
        "date": "2022-12-23",  # YYYY-MM-DD
        "with": [
            "Jeden Morgen eine stundenlange Beauty-Routine",
            '"Ich nehme mir regelmäßig Zeit und Ruhe',
            "Dir selbst Blumen",
        ],  # 3 segments
        "without": ["Mehr Themen:", "BELIEBTE THEMEN ENTDECKEN", "ÜBER"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://greator.com/innere-zufriedenheit/": {
        "file": "greator.com.innerezufriedenheit.html",
        "author": "Greator",
        "title": "Glück kommt von innen: Wie du deine innere Zufriedenheit steigern kannst",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Innere Zufriedenheit ist ein wichtiger Faktor ",
            "10 Tipps für innere Zufriedenheit:",
            "Fazit",
        ],  # 3 segments
        "without": ["Themen", "Greator Newsletter", "Artikel gefallen? Vergiss nicht zu teilen!"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.impulse.de/recht-steuern/rechtsratgeber/kind-krank/7297147.html": {
        "file": "impulse.de.eltern.html",
        "author": "Julia Müller",
        "title": "Was Arbeitgeber über die Rechte von Eltern wissen müssen",
        "date": "2022-12-28",  # YYYY-MM-DD
        "with": [
            "Wie viele Tage im Jahr dürfen Mitarbeiter",
            "Gibt es dabei eine Altersgrenze für die Kinder?",
            "Man kann den Anspruch auf Kinderkrankentage",
        ],  # 3 segments
        "without": [
            "TERMINE FÜR UNTERNEHMER",
            "2023 nichts mehr versäumen!",
            "Das könnte Sie auch interessieren",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.fem.com/beauty-lifestyle/warum-wir-anfangen-muessen-mehr-ueber-gehaelter-zu-sprechen": {
        "file": "fem.com.gehaelter.html",
        "author": "",
        "title": "Warum wir anfangen müssen, mehr über Gehälter zu sprechen",
        "date": "2019-01-17",  # YYYY-MM-DD
        "with": [
            "Es ist schon sehr deutsch,",
            "Offenheit gegen ungleiche Gehälter",
            "Weil Chefs das natürlich gar",
        ],  # 3 segments
        "without": ["MEHR ZUM THEMA JOB UND KARRIERE", "INSTAGRAM", "AM HÄUFIGSTEN GELESEN"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.business-punk.com/2022/12/netflix-and-dont-chill-netflix-nimmt-fitness-reihe-ins-programm-auf/": {
        "file": "business-punk.com.fitness.html",
        "author": "Business Punk Redaktion",
        "title": "Netflix and DON’T chill: Netflix nimmt Fitness-Reihe ins Programm auf",
        "date": "2022-12-22",  # YYYY-MM-DD
        "with": ["Insgesamt werde es über 30", "In der ersten Staffel", "Die Kollaboration ist"],  # 3 segments
        "without": ["BUSINESS PUNK NEWSLETTER", "Blick ins Heft", "Mediadaten"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.7mind.de/magazin/so-lernen-wir-grenzen-zu-setzen": {
        "file": "7mind.de.grenzen.html",
        "author": "Daniela Obers",
        "title": "So lernen wir Grenzen zu setzten",
        "date": "",  # YYYY-MM-DD
        "with": ["Sie sind das Fundament der", "So erkennst du", "Übung, Übung, Übung"],  # 3 segments
        "without": ["Das könnte dich auch interessieren", "Unsere Inhalte", "Einloggen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.brandeins.de/magazine/brand-eins-wirtschaftsmagazin/2023/keine-panik/unser-wahres-ich": {
        "file": "brandeins.de.wahresIch.html",
        "author": "Brand eins",
        "title": "Unser wahres Ich",
        "date": "",  # YYYY-MM-DD
        "with": ["brand eins: „Im Grunde gut“", "Sie wollen ein populäres", "Ist das Ihr ultimatives"],  # 3 segments
        "without": ["Ausgabe kaufen", "Rechtliches", "Über uns"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.arbeit-und-arbeitsrecht.de/news/verjaehrung-von-urlaubsanspruechen.html": {
        "file": "arbeit-und-arbeitsrecht.de.urlaub.html",
        "author": "",
        "title": "Verjährung von Urlaubsansprüchen",
        "date": "2022-12-20",  # YYYY-MM-DD
        "with": ["Der Beklagte beschäftigte", "Der Senat hat damit die", "Pressemitteilung Nr. 48/22"],  # 3 segments
        "without": ["Jetzt zum kostenlosen Newsletter anmelden", "Recherche im Archiv", "Redaktions-Newsletter"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://erfolg-magazin.de/mit-der-richtigen-konfliktkultur-zum-erfolg/": {
        "file": "erfolg-magazin.de.konfliktkultur.html",
        "author": "Redaktion",
        "title": "Mit der richtigen Konfliktkultur zum Erfolg",
        "date": "2022-12-19",  # YYYY-MM-DD
        "with": ["Unternehmen setzen alles", "Unser ganzes Leben geht es", "Und was am wichtigsten ist: "],  # 3 segments
        "without": [
            "Will Smith: Selbsthilfebücher als Teil seines Erfolgsgeheimnisses",
            "Impressum",
            "»Wir brauchen Leute, die Entscheidungen treffen«",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.humanresourcesmanager.de/future-of-work/gender-diversity-revolution-im-reallabor-women-digit-praxislaboratorien-atruvia/": {
        "file": "humanresourcesmanager.de.diversity.html",
        "author": "Jörg Staff",
        "title": "Gender-Diversity: Revolution im Reallabor",
        "date": "2022-12-15",  # YYYY-MM-DD
        "with": ["Bulgarien hat uns einiges voraus,", "In Praxislabs die Zukunft", "Agilität wirkt."],  # 3 segments
        "without": ["Weitere Beiträge aus der Kolumne:", "Unser Newsletter", "Verwandte Artikel"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.strive-magazine.de/post/das-dating-dilemma-erfolgreicher-frauen": {
        "file": "strive-magazin.de.dating.html",
        "author": "Bianca Praetorius",
        "title": "Das Dating-Dilemma erfolgreicher Frauen",
        "date": "2022-10-02",  # YYYY-MM-DD
        "with": [
            "Je erfolgreicher, klüger, smarter",
            "Oha, steile These, Frau Praetorius!",
            "Für jene, die damit ein ",
        ],  # 3 segments
        "without": ["Ähnliche Beiträge", "Kiosk finden", "Log In"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://nwx.new-work.se/themenwelten/gesellschaft/umfrage-zur-digitalisierung-am-arbeitsplatz-mitbestimmung-und-vertrauen-reduziert-digitalen-stress": {
        "file": "nwx.new-work.se.digitaler-stress.html",
        "author": "nwx",
        "title": "Vertrauen und Mitbestimmung helfen gegen digitalen Stress",
        "date": "2022-12-26",  # YYYY-MM-DD
        "with": [
            "Die Potenziale der Digitalisierung",
            "„Corona hatte einen regelrechten",
            "*Mit der repräsentativen Befragung",
        ],  # 3 segments
        "without": ["Weitere aktuelle Themen aus der Arbeitswelt", "Schwerpunkte", "Magazin"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.bewusster-leben.de/hope/": {
        "file": "bewusster-leben.de.hope.html",
        "author": "Claudia Duwe",
        "title": "Hope!",
        "date": "",  # YYYY-MM-DD
        "with": ["Ein grauer Wintermorgen ", "Dem Wunder die Hand reichen", "In ihrem Buch „Krafttiere"],  # 3 segments
        "without": ["Diesen Artikel teilen", "Weitere Beiträge", "Startseite"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://wirtschaftspsychologie-aktuell.de/magazin/fuehrung/staerkenorientierte-fuehrung ": {
        "file": "wirtschaftspsychologie-aktuell.de.starken.html",
        "author": "Christian Thiele",
        "title": "Warum Sie die Stärken Ihrer Mitarbeitenden stärken sollten",
        "date": "2022-12-07",  # YYYY-MM-DD
        "with": [
            "Stärkenorientierte Führung",
            "Rund zwei Millionen Stellen",
            "Positive Leadership lässt sich s",
        ],  # 3 segments
        "without": [
            "Zum Weiterlesen:",
            "Shared, Plural oder Dual Leadership:",
            "2022 Deutscher Psychologen Verlag GmbH",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.courage-online.de/erfinderinnen-ann-kiessling-und-ihre-forschung-im-kampf-gegen-das-hiv-virus/": {
        "file": "courgage-online.de.HIV.html",
        "author": "Matthias Lauerer",
        "title": "Erfinderinnen: Ann Kiessling und ihre Forschung im Kampf gegen das HIV-Virus",
        "date": "2022-12-25",  # YYYY-MM-DD
        "with": ["Ann Kiessling hat viele wichtige", "Tausende von Texten zum Thema", "IVF vor über"],  # 3 segments
        "without": [
            "Dir hat der Artikel gefallen? Jetzt teilen...",
            "Das eigene Limit infrage stellen",
            "Noch mehr Infos für dich",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.she-works.de/aktuelles/5-inspirierende-frauen-aus-der-sportwelt/2022/12/29/ ": {
        "file": "she-works.de.sport.html",
        "author": "she works",
        "title": "5 inspirierende Frauen aus der Sportwelt",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Die amerikanische Profi-Surferin",
            "Wenn wir schon beim Snowboarden",
            "Diese Legende und Powerfrau darf wohl",
        ],  # 3 segments
        "without": ["Schlagwörter", "E-Magazin", "SHE!"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.coaching-magazin.de/konzepte/transgenerationales-coaching": {
        "file": "coaching-magazin.de.transgenerationales-coaching.html",
        "author": "Julia Kern",
        "title": "Transgenerationales Coaching",
        "date": "",  # YYYY-MM-DD
        "with": ["Wer bin ich wirklich?", "Der Einfluss der Vererbung", "Entwicklungsreise"],  # 3 segments
        "without": ["Themen:", "Dieser Artikel gefällt Ihnen?", "Haben Sie Fragen zum Coaching-Magazin?"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.hrjournal.de/fuenf-hr-trends-2023/": {
        "file": "hrjournal.de.trends.html",
        "author": "Arne Sjöström",
        "title": "Fünf HR-Trends 2023",
        "date": "2022-12-30",  # YYYY-MM-DD
        "with": [
            "Auch wenn Mitarbeitende Zuschüsse",
            "Doch sollten Arbeitgeber nicht selbstgefällig",
            "Unternehmen, ganz gleich welcher",
        ],  # 3 segments
        "without": [
            "Lesen Sie auch die folgenden Beiträge:",
            "Zur Person",
            "Die Zusammenarbeit und Führung von Teams",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.ad-magazin.de/artikel/wellness-hotels": {
        "file": "ad-magazin.de.wellness.html",
        "author": "Fiona Bornhöft und Mariam Hofbeck",
        "title": "Diese Wellness-Hotels versprechen einen traumhaften Kurzurlaub",
        "date": "2023-01-01",  # YYYY-MM-DD
        "with": [
            "Diese Wellness-Hotels sind genau richtig",
            "Ein Infinity-Pool, ein Onsen-Pool,",
            "Zwei Jahre lang restaurierte Elisabeth",
        ],  # 3 segments
        "without": ["Ob Chalet, Öko-Resort oder", "Tropische Reiseziele:", "Mehr von AD"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.journelles.de/gift-guide-westwing-22/": {
        "file": "journelles.de.westwing.html",
        "author": "Jessie",
        "title": "Mein cosy Home Gift Guide bei Westwing Collection",
        "date": "2022-12-16",  # YYYY-MM-DD
        "with": ["Geschenke für die Liebsten aussuchen,", "Buchstützen:", "All diese schönen Produkte und"],  # 3 segments
        "without": ["Tags:", "Anzeige, enthält Affiliate Links", "Das ist Liebe in deinem Posteingang:"],  # 3 segments
        "comments": ["Lena", "Die Buchstützen", "Liebe Grüße"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.herzundblut.com/blog-1/kebbqe4kcwbrx62pr60i7gkd6mvlf7": {
        "file": "herzundblut.com.Besuch.html",
        "author": "Herz und Blut",
        "title": "Zu Besuch bei Véronique Lacaze",
        "date": "2022-11-1",  # YYYY-MM-DD
        "with": [
            "In einer wunderschönen Penthousewohnung",
            "Durch kulturelle Ausflüge,",
            "Wie feiert es sich auf eurer 360",
        ],  # 3 segments
        "without": [
            "Share",
            "Tags Homestory, Interior design, Berlin",
            "Everything i like..People, Photography, Interior",
        ],  # 3 segments
        "comments": ["Lisa", "Sehr schöne", "Ist der Hersteller"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.couchstyle.de/living/homestory/vintage-flair-mit-sehr-viel-gruen--1597": {
        "file": "couchstyle.de.vintage.html",
        "author": "fri.juli",
        "title": "Vintage-Flair mit viel Grün",
        "date": "2022-09-23",  # YYYY-MM-DD
        "with": ["Vintage trifft Urban Jungle", "Am alten Küchentisch", "Der Barschrank aus den 50er Jahre"],  # 3 segments
        "without": ["Entdecke weitere Homestorys", "Community", "Abo"],  # 3 segments
        "comments": ["Mayakoenigin", "Wunderschön, aber", "grünen Daumen"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.urlaubsarchitektur.de/de/das-glashaus-in-der-uckermark/ ": {
        "file": "urlaubsarchitektur.de.glashaus.html",
        "author": "",
        "title": "Das Glashaus in der Uckermark",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Mit dem Glashaus hat der dänische Architekt",
            "Das Zusammenspiel aus Holz, Glas, poliertem Estrich",
            "Die Fernwärme kommt aus",
        ],  # 3 segments
        "without": ["Übersichtakarte", "Lesezeichen hinzufügen", "weiterlesen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://iconmagazine.de/story/interview-mit-sharon-stone/": {
        "file": "iconmagazine.de.sharonstone.html",
        "author": "Sven Michaelsen",
        "title": "Davor und Danach",
        "date": "",  # YYYY-MM-DD
        "with": ["Es gibt Ereignisse, die", "In welchem seelischen Zustand", "Ich war zehn Jahre lang"],  # 3 segments
        "without": ["INTERVIEW SVEN MICHAELSEN", "Kontakt", "Impressum"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.baumeister.de/sportzentrum-kerenzerberg-filzbach/": {
        "file": "baumeister.de.sportzentrum.html",
        "author": "Arian Schlichenmayer",
        "title": "Sportzentrum Kerenzberg in Filzbach erweitert",
        "date": "2022-12-21",  # YYYY-MM-DD
        "with": [
            "Am Südufer des Walensees",
            "Das Sportzentrum erhielt auch",
            "Im Bestand liegt der Schwerpunkt",
        ],  # 3 segments
        "without": [
            "Nicht aus den Siebzigern",
            "NAPURS MUSEUM OF ETHNOGRAPHY BUDAPEST, FOTO: PALKÓ GYÖRGY - ",
            "Napur Marcel Ferencz Kultur",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.decohome.de/farbe-des-jahres-2023-viva-magenta/": {
        "file": "decohome.de.magenta.html",
        "author": "Katharina Volkwein",
        "title": "Viva Magenta: „Eine unkonventionelle Farbe für eine unkonventionelle Zeit“",
        "date": "",  # YYYY-MM-DD
        "with": [
            "Als „Faust im Samthandschuh“ ",
            "Pulsierend, mutig, fröhlich,",
            "Ob nun als Akzent oder All-over Look",
        ],  # 3 segments
        "without": [
            " Wie finde ich das richtige Möbel?",
            "Marsala, Terrakotta, Ochsenblut, Curry und Co",
            "Hat das Sammel-Gen von ihrem Opa geerbt",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.familie.de/kleinkind/montessori-spielzeug-13-paedagogisch-wertvolle-ideen-fuer-babys-und-kleinkinder/": {
        "file": "familie.de.montessori.html",
        "author": "Gesine Engels-Krone",
        "title": "Montessori-Spielzeug: 13 pädagogisch wertvolle Ideen für Babys und Kleinkinder",
        "date": "2023-01-02",  # YYYY-MM-DD
        "with": ["Es ist schön, bunt, unkaputtbar.", "Montessori Spielzeug fördert", "#3 Nanchen-Pupen"],  # 3 segments
        "without": ["Du willst nichts mehr verpassen?", "Lies auch", "Teste dich"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://heavenlynnhealthy.de/lieblingslabel-faire-swimwear-von-mymarini-interview-mit-gruenderin-mareen-burk/": {
        "file": "heavenlynnhealthy.de.mareenburk.html",
        "author": "heavenlynnhealthy",
        "title": "Lieblingslabel: Faire Swimwear von MYMARINI + Interview mit Gründerin Mareen Burk",
        "date": "2022-06-15",  # YYYY-MM-DD
        "with": [
            "Dies ist vielleicht ein Food Blog, ",
            "Meine Gründergeschichte",
            "Wir bei MYMARINI gehen von daher aus einer",
        ],  # 3 segments
        "without": ["Kategorie:", "Folge mir", "Hallo!"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://fogsmagazin.com/outdoor-bekleidung/": {
        "file": "fogsmagazin.com.outdoor.html",
        "author": "Jennifer Koutni",
        "title": "Schnee-Vergnügen ohne Fussabdruck",
        "date": "2022-12-29",  # YYYY-MM-DD
        "with": [
            "Egal, ob man ein Outdoor-Fan",
            "Dass Outdoor-Bekleidung immer leistungsfähiger wird",
            "Pflegen und Reparieren",
        ],  # 3 segments
        "without": [
            "Schlagworte:",
            "Immer mehr Schmucklabels setzen auf faire Produktionsbedingungen",
            "Alles über nachhaltige Wanderschuhe",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.infobae.com/america/mundo/2022/05/03/el-nobel-de-la-paz-ruso-dmitry-muratov-advirtio-que-el-regimen-de-vladimir-putin-podria-utilizar-armas-nucleares-en-ucrania/": {
        "file": "infobae.com-ucrania.html",
        "author": "",
        "title": "El Nobel de la Paz ruso, Dmitry Muratov, advirtió que el régimen de Vladimir Putin podría utilizar armas nucleares en Ucrania",
        "date": "2022-05-03",
        "with": [
            "El periodista sostuvo que eso supondría “el fin",
            "advirtiendo que eso supondría“",
            "un poder absoluto y sin restricciones”.",
        ],  # 3 segments
        "without": [
            "TEMAS RELACIONADOS",
            "Muratov, tras el ataque sufrido a principios",
            "Premio Nobel de la Paz (REUTERS/Denis Balibouse)",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.eltiempo.com/colombia/medellin/elecciones-2022-candidatos-presidenciales-en-la-universidad-eafit-669594": {
        "file": "eltiempo.com-candidatos.html",
        "author": "MEDELLÍN",
        "title": "Candidatos se enfrentaron a las preguntas de estudiantes",
        "date": "2022-05-04",
        "with": [
            "enmarcado en 6 ejes temáticos relacionados",
            "que se llama Neobanco con un billón",
            "colectivamente, de acabar con este sistema",
        ],  # 3 segments
        "without": ["Necesitamos una renovación", "llenó de empresas de webcam", "noticias para ti"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "",  # if obvious: DE, CH, AT
    },
    "https://www.clarin.com/politica/tension-alberto-fernandez-cristina-kirchner-escalo-maximo-nivel_0_h7svjXlK9z.html": {
        "file": "clarin.com-albertofernandez.html",
        "author": "Federico Mayol",
        "title": "La interna oficial Aumenta la ofensiva K sobre Alberto Fernández: Cristina Kirchner puso en duda la legitimidad de su gestión",
        "date": "2022-05-03",
        "with": [
            "embestida que sumó por estas horas",
            "La Cámpora en declaraciones radiales",
            "cuenta administrada por su",
        ],  # 3 segments
        "without": ["Mirá también", "Cristina Kirchner y Alberto Fernández,", "Lo que tenés que saber hoy"],  # 3 segments
        "comments": [
            "altura de los acontecimientos se puede",
            "peleitas?!!!...cuando gobiernan?",
            "Con mucho respeto esa cara señora",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "ARG",  # if obvious: DE, CH, AT
    },
    "https://www.lanacion.com.ar/politica/jugada-del-oficialismo-para-evitar-que-jxc-avance-con-la-boleta-unica-en-diputados-nid03052022/": {
        "file": "lanacion.com.ar-jugada.html",
        "author": "",
        "title": "Jugada del oficialismo para evitar que JxC avance con la boleta única en Diputados",
        "date": "2022-05-03",
        "with": [
            "elecciones nacionales. Lo hizo por medio",
            "la infección por el",
            "función de esta comisión no es tratar la ley",
        ],  # 3 segments
        "without": ["una causa por cohecho", "a una sesión para", "Sergio Massa, el presidente"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "ARG",  # if obvious: DE, CH, AT
    },
    "https://www.ambito.com/politica/paritarias/al-rojo-gremios-la-alimentacion-marcan-inflacion-53-abril-y-amenazan-paro-n5431248": {
        "file": "ambito.com-paritarias.html",
        "author": "Mariano Martín",
        "title": "Paritarias al rojo: gremios de la alimentación marcan inflación de 5,3% en abril y amenazan con paro",
        "date": "2022-05-04",
        "with": [
            "sindicato irá hoy a una audiencia",
            "cerró en 52,7% y en base",
            "Se trata de un informe interno que",
        ],  # 3 segments
        "without": ["Temas", "Suscribite a nuestro", "Informate más"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "ARG",  # if obvious: DE, CH, AT
    },
    "https://www.pagina12.com.ar/419327-la-corte-suprema-no-imparte-justicia-sino-injusticia": {
        "file": "pagina12.com.ar-suprema.html",
        "author": "Luciana Bertoia",
        "title": '"La Corte Suprema no imparte justicia sino injusticia"',
        "date": "2022-05-04",
        "with": [
            "Organismos de derechos",
            "entendió como un desafío a los poderes",
            "desactivada durante el gobierno de Mauricio",
        ],  # 3 segments
        "without": ["INGRESAR", "Imagen: Télam", "Corte Suprema"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "ARG",  # if obvious: DE, CH, AT
    },
    "https://www.losandes.com.ar/sociedad/el-ano-de-las-evaluaciones-las-escuelas-de-mendoza-tendran-tres-relevamientos-de-calidad-educativa/": {
        "file": "losandes.com-mendoza.html",
        "author": "Verónica De Vita",
        "title": "El año de las evaluaciones: las escuelas de Mendoza tendrán tres relevamientos de calidad educativa",
        "date": "2022-05-04",
        "with": [
            "escuelas mendocinas. El gobierno",
            "que se realizará en mayo,",
            "Evaluación Internacional de Alumnos de",
        ],  # 3 segments
        "without": [
            "TEMAS RELACIONADOS",
            "El mendocino que suma su ayuda",
            "Los exámenes PISA en Mendoza se realizarán",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "ARG",  # if obvious: DE, CH, AT
    },
    "https://24ora.com/minister-president-presente-ne-trashion-fashion-show-di-international-school/": {
        "file": "24ora.com-internationalschol.html",
        "author": "",
        "title": "MINISTER-PRESIDENT PRESENTE N’E “TRASHION FASHION SHOW” DI INTERNATIONAL SCHOOL",
        "date": "2022-05-03",
        "with": [
            "studiantenan a presenta trahenan traha",
            "fatal pa e animalnan. Tambe",
            "amor pa nos planeta.",
        ],  # 3 segments
        "without": [
            "MAS FOR DI E AUTOR",
            "MINISTERIO DI HUSTICIA NO LO TOLERA NINGUN ACTO",
            "AFECTA ARUBA TAMBE",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "ABW",  # if obvious: DE, CH, AT
    },
    "https://eldeber.com.bo/santa-cruz/investigador-chileno-asegura-que-no-publico-todo-su-material-el-90-de-los-autos-robados-estan-en-pos_276757": {
        "file": "eldeber.com.bo-autos.html",
        "author": "Ariel Melgar Cabrera",
        "title": 'Investigador chileno asegura que no publicó todo su material: "El 90% de los autos robados están en posesión de autoridades bolivianas"',
        "date": "2022-05-03",
        "with": [
            "coronel Raúl Cabezas Pantoja,",
            "recuperación de la vagoneta. Comentó",
            "devolver los vehículos.",
        ],  # 3 segments
        "without": ["Recomendado para ti", "ESCUCHA ESTA NOTA AQUÍ", "TE PUEDE INTERESAR"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BOL",  # if obvious: DE, CH, AT
    },
    "https://www.paginasiete.bo/seguridad/2022/5/3/policia-anuncia-coordinacion-con-carabineros-para-investigar-otros-casos-de-robo-de-vehiculos-330199.html": {
        "file": "paginasiete.bo-carabineros.html",
        "author": "Redacción Diario Pagina Siete",
        "title": "Policía anuncia coordinación con Carabineros para investigar otros casos de robo de vehículos",
        "date": "",
        "with": [
            "coordinación con Carabineros de Chile para",
            "Tribunal Supremo Disciplinario, teniente",
            "por el director nacional de Diprove”.",
        ],  # 3 segments
        "without": ["OTRAS NOTICIAS", "Investigan muerte de un", "SEGURIDAD"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BOL",  # if obvious: DE, CH, AT
    },
    "https://www.lostiempos.com/actualidad/pais/20220503/juicio-caso-golpe-ii-entra-recta-final-sentencia-podria-dictarse-este": {
        "file": "lostiempos.com-juicio.html",
        "author": "Jeanine Áñez",
        "title": "Juicio por el caso golpe II entra en la recta final; sentencia podría dictarse este miércoles",
        "date": "2022-05-03",
        "with": [
            "La audiencia que podría ser decisiva",
            "de Sentencia Anticorrupción de La Paz fijó",
            "condena de tres años de cárcel",
        ],  # 3 segments
        "without": [
            "Valora esta noticia",
            "sentencia y presenta recurso al TCP",
            "abogados en el juicio por el caso “golpe”.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BOL",  # if obvious: DE, CH, AT
    },
    "https://www.correiobraziliense.com.br/politica/2022/05/5005250-de-novo-em-busca-da-tregua-institucional.html": {
        "file": "correiobraziliense.com.br-poderes.html",
        "author": "Luana Patriolino",
        "Raphael Felicetitle": "Pacheco e Fux tentam uma trégua institucional entre os Poderes",
        "date": "2022-05-04",
        "with": [
            "do Senado, Rodrigo Pacheco (PSD-MG)",
            "o Supremo Tribunal Federal",
            "Com o mesmo repertório das manifestações",
        ],  # 3 segments
        "without": ["(crédito: Minervino Júnior", "urgência para barrar", "Pela Web"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BRA",  # if obvious: DE, CH, AT
    },
    "https://www.brasil247.com/regionais/brasilia/militares-enviaram-88-questoes-ao-tse-sobre-eleicoes-e-urnas-eletronicas": {
        "file": "brasil247.com-militares.html",
        "author": "",
        "title": "Militares enviaram 88 questões ao TSE sobre eleições e urnas eletrônicas",
        "date": "2022-05-04",
        "with": [
            "supostos riscos e fragilidades",
            "votação ainda era em cédula de papel",
            "levantadas apesar de os órgãos",
        ],  # 3 segments
        "without": ["MAIS POPULAR", "(Foto: ABr)", "Fique por dentro do 247"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BRA",  # if obvious: DE, CH, AT
    },
    "https://www.gazetadopovo.com.br/republica/o-que-pacheco-pretende-acenos-ao-stf-e-propor-limites-ao-indulto-presidencial/": {
        "file": "gazetadopovo.com.br-pacheco.html",
        "author": "Rodolfo Costa.",
        "title": "O que Pacheco pretende ao fazer acenos ao STF e propor limites ao indulto presidencial",
        "date": "2022-05-03",
        "with": [
            "e nas faixas de manifestantes",
            "Esplanada dos Ministérios como",
            "dos Poderes, não só com manifestações",
        ],  # 3 segments
        "without": ["VEJA TAMBÉM:", "indulto em outras ações", "a batalha dos palanques em São Paulo"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BRA",  # if obvious: DE, CH, AT
    },
    "https://www.correio24horas.com.br/noticia/nid/lider-do-grupo-de-sequestradores-que-tinha-pms-foi-morto-em-confronto-policial/": {
        "file": "correio24horas.com.br-PMS.html",
        "author": "Bruno Wendel",
        "title": "Líder do grupo de sequestradores que tinha PMs foi morto em confronto policial",
        "date": "2022-05-04",
        "with": ["mediante sequestro, e que", "lotados na Rondesp Atlântico", "Ele também era investigado"],  # 3 segments
        "without": [
            "Em tempos de coronavírus e desinformação",
            "(Foto: Tony Silva/Ascom-PC)",
            "Polícia faz operação de combate a",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BRA",  # if obvious: DE, CH, AT
    },
    "https://www.campograndenews.com.br/cidades/interior/adolescente-encontrada-morta-em-vala-estava-gravida-de-3-meses-confirma-irma": {
        "file": "campograndenews.com.br-adolescente.html",
        "author": "Adriano Fernandes",
        "title": "Adolescente encontrada morta em vala estava grávida de 3 meses, confirma irmã",
        "date": "2022-05-03",
        "with": ["intrigante. Conforme a irmã", "no momento em que a menina teria", "Luana na mesma noite do"],  # 3 segments
        "without": ["VEJA TAMBÉM", "Adolescente morta na", "Nos siga no"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "BRA",  # if obvious: DE, CH, AT
    },
    "https://www.caymancompass.com/2022/05/04/prison-official-anyone-could-escape-from-northward/": {
        "file": "caymancompass.com-prison.html",
        "author": "James Whittaker",
        "title": "Prison official: ‘Anyone’ could escape from Northward",
        "date": "2022-05-04",
        "with": [
            "The evidence was given in support of a decision",
            "provided by the most dangerous and high risk offenders.”",
            "added that the prison estate was not considered",
        ],  # 3 segments
        "without": [
            "The prison official’s affidavit highlights security",
            "You have 4 free articles left this month",
            "Previous article",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CYM",  # if obvious: DE, CH, AT
    },
    "https://www.biobiochile.cl/noticias/nacional/region-de-los-rios/2022/05/04/gremios-de-los-camioneros-no-descartan-nueva-movilizacion-realizaran-consulta-nacional.shtml": {
        "file": "biobiochile.cl-gremios.html",
        "author": "Alberto González",
        "title": "Gremios de los camioneros no descartan nueva movilización: realizarán consulta nacional",
        "date": "2022-05-04",
        "with": [
            "En este contexto, la tarde",
            "consulta que se hará este jueves",
            "suma protección a la infraestructura",
        ],  # 3 segments
        "without": ['"A ver si se atreve a viajar":', "visto ahora", "Hector Andrade"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.latercera.com/politica/noticia/la-agenda-con-que-interior-busca-contener-la-crisis-de-seguridad-y-el-dilema-del-oficialismo/DHCHJTT5TNETPCHCIYLXWMQOBA/": {
        "file": "latercera.com-laagenda.html",
        "author": "Isabel Caro, Rocío Latorre, José Miguel Wilson",
        "title": "La agenda con que Interior busca contener la crisis de seguridad y el dilema del oficialismo",
        "date": "2022-05-04",
        "with": [
            "La estrategia contempla, entre otras acciones,",
            "efundidos “sobre fortalecimiento de la persecución",
            "Yáñez. Y agregó: “Nosotros permanentemente estamos evaluando a las autoridades",
        ],  # 3 segments
        "without": [
            "Más sobre La Tercera AM",
            "de terrenos adquiridos por celebridades",
            "$636 millones del cambio de mando?",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.cooperativa.cl/noticias/pais/presidente-boric/presidente-boric-vuelve-a-su-casa-magallanes-este-miercoles-realiza-su/2022-05-04/074527.html": {
        "file": "cooperativa.cl-presidente.html",
        "author": "",
        "title": "Presidente Boric vuelve a su casa, Magallanes: Este miércoles realiza su segunda visita a regiones",
        "date": "2022-05-04",
        "with": [
            "Punta Arenas, con las autoridades",
            'territorio amigo", al que representó durante dos',
            "Arenas, Boric se desplazará a Puerto",
        ],  # 3 segments
        "without": ["Suscríbete a nuestro newsletter", "Este sitio está protegido por", "Foto: ATON"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.lacuarta.com/espectaculos/noticia/va-y-agarra-las-llaves-de-su-cartera-destapan-pelea-a-grito-pelado-entre-loreto-aravena-y-pancha-merino-en-pasillos-de-canal-13/I7QCHL6HAZCBBIROIOUNHFGB5I/": {
        "file": "lacuarta.com-loretoaravena.html",
        "author": "Juan Carlos Muñoz C.",
        "title": "“Va y agarra las llaves de su cartera…”: destapan pelea a “grito pelado” entre Loreto Aravena y Pancha Merino en pasillos de Canal 13",
        "date": "2022-05-04",
        "with": [
            "protagonizó Loreto Aravena y Pancha",
            "hasta el camarín del Bienvenidos.",
            "alegando que le ocupan el estacionamiento”",
        ],  # 3 segments
        "without": ["COMPARTIR NOTA", "TEMAS RELACIONADOS", "Stella a Francisca en Pobre Novio"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.elmostrador.cl/destacado/2022/05/04/las-trabas-del-congreso-discusion-parlamentaria-sobre-normas-de-una-nueva-constitucion-podria-tardar-decadas/": {
        "file": "elmostrador.cl-congreso.html",
        "author": "Raúl Espina",
        "title": "Las trabas del Congreso: discusión parlamentaria sobre normas de una nueva Constitución podría tardar décadas",
        "date": "2022-05-04",
        "with": [
            "en el caso de que la opción Apruebo se imponga",
            "Lo cierto es que, para que las nuevas",
            "constituidos, y en particular los partidos",
        ],  # 3 segments
        "without": ["Nueva Constitución", "Comprensión del Derecho", "Directora Ejecutiva de Fundación"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.24horas.cl/politica/presidente-boric-inicia-gira-por-magallanes-este-miercoles-5287894": {
        "file": "24horas.cl-segundo.html",
        "author": "Agencia EFE",
        "title": "Segundo viaje oficial fuera de Santiago: Presidente Boric inicia gira por Magallanes este miércoles",
        "date": "2022-05-04",
        "with": [
            "joven jefe del Estado, al que apenas se",
            "mundial, arrastrada por la guerra en Europa",
            'Armada por el "Mes del Mar", retomar el pulso',
        ],  # 3 segments
        "without": ["condonación progresiva del CAE", "Kiss se presentó por", "MÁS SEÑALES EN VIVO"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.publimetro.cl/noticias/2022/05/04/ministra-de-la-mujer-por-berrios-que-la-justicia-penal-investigue-no-la-canonica/": {
        "file": "publimetro.cl-ministra.html",
        "author": "Rodrigo Mejías",
        "title": "Ministra de la Mujer por Berrios: “Que la justicia penal investigue, no la canónica”",
        "date": "2022-05-04",
        "with": [
            "a la denuncia que recae en contra",
            "en declaraciones a T13 Noche.",
            "mayor celeridad posible”, añadió.",
        ],  # 3 segments
        "without": ["Síguenos en", "LO ÚLTIMO", "“Nos pilló de sorpresa”"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "CHL",  # if obvious: DE, CH, AT
    },
    "https://www.elespectador.com/judicial/asi-seran-los-tres-macrocasos-que-abrira-la-jep/": {
        "file": "elespectador.com-orion.html",
        "author": "Felipe Morales Sierra",
        "title": "Operación Orión, tomas guerrilleras de pueblos y más hechos que investigará la JEP",
        "date": "2022-05-06",
        "with": [
            "contra la naturaleza serán parte de las investigaciones",
            "El 09, en las violencias que sufrieron los pueblos étnicos",
            "macrocaso, pero se apartó de exigencias más duras",
        ],  # 3 segments
        "without": [
            "Desvinculan al general (r) Leonardo Barrero",
            "Le puede interesar",
            "Mejor calidad de vida con gas natural",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "COL",  # if obvious: DE, CH, AT
    },
    "https://www.elcolombiano.com/antioquia/polemica-por-buses-de-la-alcaldia-en-casa-de-gustavo-petro-en-la-floresta-EN17385450": {
        "file": "elcolumbiano.com-alcaldia.html",
        "author": "JACOBO BETANCUR PELÁEZ",
        "title": "¿Buses de la Alcaldía al servicio de Petro?",
        "date": "2022-05-06",
        "with": [
            "encenderse esta semana, justo",
            "que el pasado 30 de abril los vehículos",
            "una de las cuotas de Quintero en el Pacto Histórico",
        ],  # 3 segments
        "without": [
            "CONTEXTO DE LA NOTICIA",
            "ENLACES PATROCINADOS",
            "Porque entre varios ojos vemos más, queremos construir",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "COL",  # if obvious: DE, CH, AT
    },
    "https://www.minuto30.com/policia-hace-presencia-en-la-sierra/1331134/": {
        "file": "minuto30-lasierra.html",
        "author": "Juliet Jimenez",
        "title": "La Policía dice que todo ‘tranqui’ en La Sierra, reforzaron los uniformados en el sector",
        "date": "2022-05-05",
        "with": [
            "Tras el anuncio del Paro armado por parte",
            "El Coronel, aseguró que con ayudas",
            "del día a día, no solamente con las patrullas",
        ],  # 3 segments
        "without": [
            "Imágenes capturadas de video",
            "CONTENIDO PATROCINADO",
            "se elevan un 583 % en el primer trimestre",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "COL",  # if obvious: DE, CH, AT
    },
    "https://www.kaieteurnewsonline.com/2022/05/06/essequibo-hunter-found-dead-with-gunshot-wounds/": {
        "file": "kaieteurnewsonline.com-essequibo.html",
        "author": "",
        "title": "Essequibo hunter found dead with gunshot wounds",
        "date": "2022-05-06",
        "with": ["they had heard when", "Ramdehol had told them to", "was removed and taken to Suddie"],  # 3 segments
        "without": [
            "Guyanese killed",
            "Coalition Govt ‘short-changed’ judiciary in 2018",
            "Club 40overs cricket...",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "GUY",  # if obvious: DE, CH, AT
    },
    "https://www.ultimahora.com/tribunal-apelacion-confirma-la-ejecucion-la-condena-la-secretaria-vip-n2999922.html": {
        "file": "ultimahora.com-apelacion.html",
        "author": "",
        "title": "Tribunal de Apelación confirma la ejecución de la condena a la secretaria vip",
        "date": "2022-05-05",
        "with": [
            "la Corte Suprema de Justicia,",
            "el pedido y esto fue apelado por la defensa",
            "de honorarios a 23 meses con la suspensión",
        ],  # 3 segments
        "without": ["Asunción: Tras ola", " marihuana que", "Dejá tu comentario"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PRY",  # if obvious: DE, CH, AT
    },
    "https://www.hoy.com.py/nacionales/daran-bendicion-a-vehiculos-este-sabado": {
        "file": "hoy.com-daran.html",
        "author": "",
        "title": "Darán bendición a vehículos este sábado",
        "date": "2022-05-06",
        "with": [
            "a ocasión también para entregar una",
            "cuidado que se debe tener con respecto a la",
            "Hermanos Franciscanos Capuchinos realizarán",
        ],  # 3 segments
        "without": ["Etiquetas:", "La bendición se realizará mañana. Foto: LN", "Bebé muere electrocutado al"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PRY",  # if obvious: DE, CH, AT
    },
    "https://elcomercio.pe/politica/justicia/kenji-fujimori-juicio-contra-excongresista-por-presunta-compra-de-votos-continuara-el-18-de-mayo-pedro-pablo-kuczynski-ppk-fiscalia-rmmn-noticia/": {
        "file": "elcomercio.pe-kenjifujimori.html",
        "author": "",
        "title": "Kenji Fujimori: juicio por presunta compra de votos continuará el 18 de mayo",
        "date": "2022-05-07",
        "with": [
            "de oficio (Milton Hinojoza y Luis Loyola)",
            "demostrarían que los acusados habrían",
            "PPK y Kenji Fujimori por",
        ],  # 3 segments
        "without": [
            "VIDEO RECOMENDADO",
            "Fiscalía de la Nación abre investigación",
            "Este juicio comprende también a",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PER",  # if obvious: DE, CH, AT
    },
    "https://larepublica.pe/datos-lr/respuestas/2022/05/02/cronograma-minedu-2022-cuando-seran-las-vacaciones-escolares-atmp/": {
        "file": "larepublica.pe-minedu.html",
        "author": "",
        "title": "¿Cuándo serán las primeras vacaciones escolares del 2022, según el cronograma del Minedu?",
        "date": "2022-05-08",
        "with": [
            "y semipresencial el último 28 de marzo",
            "a fin de mejorar las estadísticas vinculadas al avance",
            "compartir alimentos ni utensilios.",
        ],  # 3 segments
        "without": [
            "Quiniela de HOY, sábado 7 de mayo: resultados",
            "Son tres los periodos de vacaciones durante",
            "PUEDES VER: ¿Qué es la Sunedu,",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PER",  # if obvious: DE, CH, AT
    },
    "https://trome.pe/espectaculos/dia-de-la-madre-trome-celebro-con-las-mamitas-de-chollywood-magaly-medina-janet-barboza-noticia/": {
        "file": "trome.pe-chollywood.html",
        "author": "Carla Chevez",
        "title": "Día de la Madre: Trome celebró con las mamitas de Chollywood",
        "date": "2022-05-08",
        "with": [
            "porque siempre fui muy estudiosa,",
            "descubriría, pues no iba así nomás a mi",
            "culpé a mi hermano, pero finalmente",
        ],  # 3 segments
        "without": [
            "Silvia Núñez del Arco: “Jaime",
            "y origen de su apodo",
            "contó la historia de un flan, que se comió en su infancia.",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PER",  # if obvious: DE, CH, AT
    },
    "https://libero.pe/futbol-internacional/2022/05/06/manchester-united-vs-brighton-en-vivo-via-star-plus-fox-sports-sky-sports-espn-2-premier-league-2022-cristiano-ronaldo-56304": {
        "file": "libero.pe-ronaldo.html",
        "author": "Edilson La Rosa",
        "title": "Cristiano Ronaldo lo sufre: Brighton goleó 4-0 a Manchester United y lo alejó de la Champions",
        "date": "2022-05-07",
        "with": [
            "cinco del Arsenal. Eso sí, la desventaja",
            "Así fue el gol de Moisés Caicedo que",
            "siendo una tarea muy difícil, los dirigidos",
        ],  # 3 segments #schwierig zu erkennen, was zum Text gehört und was nicht
        "without": [
            "Barcelona: el día que Ter Stegen",
            "Brighton goleó al Manchester United por",
            "Manchester United vs. Brighton, en vivo: minuto",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PER",  # if obvious: DE, CH, AT
    },
    "https://elperuano.pe/noticia/152832-logran-evacuar-a-otros-50-civiles": {
        "file": "elperuanoa.pe-logran.html",
        "author": "2022-05-07",
        "title": "Logran evacuar a otros 50 civiles",
        "date": "",
        "with": [
            "niños y ancianos”, informó la",
            "se iniciaron el fin de semana pasado y",
            "el cese el fuego, por lo",
        ],  # 3 segments
        "without": [
            "Algunos se acuerdan de su madre",
            "(05:45) Senamhi: DANA “Bernardo”",
            "Ser madre en el Perú",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PER",  # if obvious: DE, CH, AT
    },
    "https://www.elnuevodia.com/noticias/politica/notas/lider-de-la-organizacion-mujeres-populares-denuncia-intentos-del-ppd-de-silenciarla/": {
        "file": "elnuevodia.com-mujeres.html",
        "author": "Gloria Ruiz Kuilan",
        "title": "Líder de la organización Mujeres Populares denuncia intentos del PPD de silenciarla",
        "date": "2022-05-11",
        "with": [
            "José Luis Dalmau relacionadas al aborto",
            "posturas públicas en contra de la",
            "que se han practicado un aborto.",
        ],  # 3 segments
        "without": [
            "José Luis Dalmau indica que el",
            "Carlos Delgado Altieri",
            "Ada Álvarez Conde anticipó que renunciará",
        ],  # 3 segments
        "comments": [
            "exactamente lo que diga Manuel",
            "Dalmau será el sepulturero.¿Por",
            "de Rafael Hernández y su hijo al defender",
        ],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "PRI",  # if obvious: DE, CH, AT
    },
    "https://www.elpais.com.uy/informacion/sociedad/gobierno-acusa-montecon-aliarse-sindicato-fomentar-conflicto-portuario.html": {
        "file": "elpais.com.uy-gobierno.html",
        "author": "E. BARRENECHE / J. I. DA SILVA",
        "title": "Gobierno acusa a Montecon de aliarse con el sindicato y fomentar conflicto portuario",
        "date": "2022-05-11",
        "with": [
            "ahora enviaría a 125 trabajadores",
            "previstos para fin de mes. Horas más tarde",
            "causó a la firma que dirige la pérdida de dos",
        ],  # 3 segments
        "without": [
            "Por último, se ofreció que la ANP tome en cuenta",
            "LAS MÁS VISTAS",
            "Puerto de Montevideo. Foto: Archivo",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "URY",  # if obvious: DE, CH, AT
    },
    "https://ladiaria.com.uy/ambiente/articulo/2022/5/productor-fumigo-con-glifosato-predio-lindero-a-escuela-rural-ubicada-dentro-del-area-protegida-paso-centurion-y-sierra-de-rios/": {
        "file": "ladiaria.com.uy-productor.html",
        "author": "Camila Méndez en Territorio",
        "title": "Productor fumigó con glifosato predio lindero a escuela rural ubicada dentro del área protegida Paso Centurión y Sierra de Ríos",
        "date": "2022-05-11",
        "with": [
            "consideran “excesivo” su tamaño.",
            " Ministerio de Ganadería, Agricultura y Pesca, autoridad",
            "en las zonas rurales lo que pasa muchas veces es que no",
        ],  # 3 segments
        "without": [
            "Comentar este artículo",
            "La asociación civil de rescate y",
            "Predio fumigado lindero a escuela dentro",
        ],  # 3 segments
        "comments": ["conversaciones saludables y constructivas"],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "URY",  # if obvious: DE, CH, AT
    },
    "https://viconsortium.com/vi-crime/virgin-islands-vessel-returning-to-puerto-rico-from-st-thomas-with-475-pounds-of-cocaine-intercepted-by-federal-agents-cbp-says": {
        "file": "viconsortium.com-cocaine.html",
        "author": "",
        "title": "Vessel Returning to Puerto Rico From St. Thomas With 475 Pounds of Cocaine Intercepted by Federal Agents, CBP Says",
        "date": "2022-05-10",
        "with": [
            "U.S. Customs and Border Protection",
            "AMO agents requested assistance from a Puerto",
            "awareness in the air and maritime environments,”",
        ],  # 3 segments
        "without": [
            "phone with the VI Consortium app.",
            "AMO found Sunday 475 pounds of cocaine",
            "By U.S. CUSTOMS AND BORDER PROTECTION",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "VIR",  # if obvious: DE, CH, AT
    },
    "https://www.elnacional.com/venezuela/carta-abierta-un-nuevo-espacio-donde-el-nacional-recibira-las-denuncias-de-sus-lectores/": {
        "file": "elenacional.com-carta.html",
        "author": "Williams Perdomo",
        "title": "Carta abierta, un nuevo espacio donde El Nacional recibirá las denuncias de sus lectores",
        "date": "2022-05-11",
        "with": [
            "«Queremos contar las historias desde",
            "gente, crear vínculos y sobre todo",
            "voz del venezolano», resaltó Makriniotis.",
        ],  # 3 segments
        "without": ["El Nacional recibirá cartas", "MINUTO A MINUTO", "desapariciones forzadas en Brasil"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "VEN",  # if obvious: DE, CH, AT
    },
    "https://www.eluniversal.com/internacional/125703/senador-republicano-califica-a-biden-de-incapacitado": {
        "file": "eluniversal.com-senador.html",
        "author": "",
        "title": 'Senador republicano califica a Biden de "incapacitado"',
        "date": "2022-05-11",
        "with": [
            "y confundido. No sabe dónde está la mitad del tiempo.",
            "en alusión a la marca Make America",
            "sobre la declaración de Scott, Biden sonrió y dijo",
        ],  # 3 segments
        "without": [
            "Siguenos en Telegram, Instagram, Facebook y Twitter",
            "Lluvias en Colombia dejan 47 fallecidos",
            "Emmanuel presentará en",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "VEN",  # if obvious: DE, CH, AT
    },
    "https://ultimasnoticias.com.ve/noticias/mundo/ucrania-interrumpe-paso-de-gas-ruso-a-europa-por-su-territorio/": {
        "file": "ultimasnoticias.com.ve-ucraina.html",
        "author": "VÍCTOR CASTELLANOS",
        "title": "Ucrania interrumpe paso de gas ruso a Europa por su territorio",
        "date": "2022-05-10",
        "with": [
            "por «causas de fuerza mayor», arguyendo",
            "Emmanuel Macron dijo que la entrada",
            "ucraniana es muy consciente de ello",
        ],  # 3 segments
        "without": [
            "Deja un comentario",
            "causan más hambre en el mundo",
            "Ucrania interrumpe paso de gas ruso a Europa por su territorio",
        ],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "VEN",  # if obvious: DE, CH, AT
    },
    "https://dawo-dresden.de/2023/10/30/drei-haselnuesse-fuer-aschenbroedel-jetzt-tickets-sichern-fuer-winterausstellung/": {
        "file": "dawo-dresden.de-Winterausstellung.html",
        "author": "Carola Pönisch",
        "title": "Drei Haselnüsse für Aschenbrödel: Jetzt Tickets sichern für Winterausstellung",
        "date": "2023-10-30",
        "description": "Die Winterausstellung „Drei Haselnüsse für Aschenbrödel“ zum tschechisch-deutschen Märchenkultfilm öffnet am 22. November 2023 auf Schloss Moritzburg. ",
        "categories": ["KULTUR"],
        "tags": [],
        "with": [
            "Genau 50 Jahre ist es her",
            "das der Film im Januar 1973 in Moritzburg",
            "in den Kulissen der Filmstudios Babelsberg",
        ],
        "without": ["Mehr Nachrichten aus Dresden", "Noch mehr lokale Fundstücke", "MEHR AUSFLUGSTIPPS"],
        "comments": [
            "Die Ausstellung besuchen und gleichzeitig in Moritzburg",
            "ein bisschen wandern gehen das wäre doch schön",
            "wir kommen gerne",
        ],
        "license": "",
        "region": "DE",
    },
    "https://de.cointelegraph.com/news/cme-second-largest-bitcoin-futures-exchange-open-interest-surges": {
        "file": "de.cointelegraph.com-CME.html",
        "author": "PRASHANT JHA",
        "title": "CME nun zweitgrößte Bitcoin (BTC)-Futures-Börse: Open Interest steigt sehr stark",
        "date": "2023-10-31",
        "description": "Der Anstieg des Open Interest bei den Bitcoin-Futures der CME hat der regulierten Derivateplattform einen Marktanteil von 25 Prozent gesichert. ",
        "categories": [],
        "tags": ["Bitcoin", "Kryptowährungen", "Wirtschaft", "Akzeptanz", "Bitcoin-Futures", "CME", "Futures"],
        "with": ["Die Chicago Mercantile Exchange (CME)", "eine regulierte Derivatbörse", "liegt nun in Bezug auf das Open"],
        "without": ["AUCH INTERESSANT", "CT EMPFIEHLT", "WERBEN SIE BEI UNS"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://der-farang.com/de/pages/frei-erfunden-grab-bote-fliegt-nach-singapur": {
        "file": "der-farang.com-Grab-Bote.html",
        "author": "Björn Jahner",
        "title": "Frei erfunden: Grab-Bote fliegt nach Singapur",
        "date": "2023-10-31",
        "description": "BANGKOK: Ein TikTok-Video, in dem behauptet wird, dass ein Grab-Lieferbote nach Singapur fliegt, um Hühnerreis für seinen Kunden in Thailand zu kaufen, ist frei erfunden, sagte ein Grab-Sprecher am Montag (30. Oktober 2023). ",
        "categories": ["BANGKOK"],
        "tags": [],
        "with": [
            "das inzwischen mehr als",
            "drei Millionen Aufrufe verzeichnet",
            "ist ein thailändischer Grab-Lieferfahrer zu sehen",
        ],
        "without": [
            "Lesen Sie auch",
            "Die Regierung braucht einen Notfallplan: Pita",
            "Than On beantragt Thai-ID-Card und Reisepass",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://de.starsinsider.com/gesundheit/588409/this-is-what-happens-to-your-brain-and-body-when-you-get-scared": {
        "file": "de.starsinsider.com-Angst.html",
        "author": "",
        "title": "Das passiert mit Ihrem Gehirn und Körper, wenn Sie Angst haben",
        "date": "2023-10-30",
        "description": "Die Wissenschaft der Angst verstehen ",
        "categories": ["GESUNDHEIT"],
        "tags": [],
        "with": [
            "Angst ist ein unausweichlicher Bestandteil",
            "der menschlichen Erfahrung",
            "Obwohl sie in der Regel als eine unerwünschte Emotion",
        ],
        "without": ["MEIST GELESEN", "FÜR DICH EMPFOHLEN", "Wie gefährlich ist Scharlach?"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://deutsche-wirtschafts-nachrichten.de/706332/industriestrompreis-kein-ende-der-debatte?src=live": {
        "file": "deutsche-wirtschafts-nachrichten.de-Industriestrompreis.html",
        "author": "",
        "title": "Habeck, BDI und Gewerkschaft dringen auf raschen Industrie-Strompreis",
        "date": "2023-10-31",
        "description": "Die Ampel streitet über einen subventionierten Strompreis. Industrie- und Gewerkschaftsvertreter fordern endlich Klarheit. ",
        "categories": [],
        "tags": ["Industrie", "Deutschland", "Energie-Krise"],
        "with": [
            "Bundeswirtschaftsminister Robert Habeck",
            " die Industrie und die Gewerkschaft IG Metall",
            "dringen auf ein schnelles Ja für einen verbilligten Strompreis",
        ],
        "without": [
            "Experte: Energiepreise werden weiter steigen",
            "Standort Deutschland – zu großes Geschäftsrisiko?",
            "Unverbindliches aus dem Hause Habeck",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://dietagespresse.com/halloween-bizarrer-horrorclown-versetzt-oesterreich-in-angst-und-schrecken/": {
        "file": "dietagespresse.com-halloween.html",
        "author": "",
        "title": "Halloween: Bizarrer Horrorclown versetzt Österreich in Angst und Schrecken",
        "date": "2023-10-31",
        "description": "Halloween lockt offenbar die bizarrsten Gestalten aus ihren Löchern. Die Polizei warnt aktuell vor einem Horrorclown, der das ganze Land in Angst und Schrecken versetzt. Er droht, Kindern die Süßigkeiten wegzunehmen. Zielfahnder vermuten ihn in Oberösterreich. ",
        "categories": ["LEBEN"],
        "tags": [],
        "with": [
            "kichert der irre Horrorclown im 10-sekündigen Gruselclip",
            "Das bizarre Drohvideo",
            "das auf sozialen Medien seine Runden dreht",
        ],
        "without": [
            "Kostenlos registrieren und weiterlesen",
            "Schon registriert? Hier einloggen",
            "Was passiert mit meinen Daten?",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://digitalcourage.de/blog/2023/buch-digitale-muendigkeit": {
        "file": "digitalcourage.de-Muendigkeit.html",
        "author": "Leena Simon",
        "title": "Mit Digitaler Mündigkeit die Welt retten",
        "date": "2023-10-06",
        "description": "Leena Simon will die Welt retten. Sie findet, das geht nur, indem wir alle gemeinsam unsere Haltung gegenüber digitaler Technik ändern und mehr Verantwortung übernehmen. ",
        "categories": [],
        "tags": [],
        "with": [
            "Haben auch Sie den Eindruck",
            "dass unsere Welt gerade aus den Fugen gerät",
            "Unser achtloser Umgang mit digitalen Medien",
        ],
        "without": [
            "Buch bestellen",
            "Ist Ihnen beim Betreten dieser Seite etwas aufgefallen?",
            "Wir haben Sie nicht mit einer Cookieabfrage genervt.",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://dubisthalle.de/intendanten-wechsel-beim-mdr": {
        "file": "dubisthalle.de-Intendanten-Wechsel.html",
        "author": "ESEPPELT",
        "title": "Intendanten-Wechsel beim MDR",
        "date": "2023-10-31",
        "description": "An der Spitze des Mitteldeutschen Rundfunks steht ein Wechsel bevor: Am heutigen 31. Oktober endet die Amtszeit von Intendantin Karola Wille, ab 1. November ist Ralf Ludwig neuer Intendant. ",
        "categories": [],
        "tags": [
            "AfD",
            "Bahn",
            "Basketball",
            "Baustelle",
            "Bildung",
            "Brand",
            "CDU",
            "Corona",
            "Diebstahl",
            "Drogen",
            "Einbruch",
            "Eishockey",
            "Fahrrad",
            "Feuerwehr",
            "Flughafen",
            "Fußball",
            "Handwerkskammer",
            "HAVAG",
            "HFC",
            "Impfung",
            "Kita",
            "Klima",
            "Körperverletzung",
            "Laternenfest",
            "Lions",
            "Neustadt",
            "Polizei",
            "Raub",
            "Rechtsextremismus",
            "Saale",
            "Bulls",
            "Schule",
            "Silberhöhe",
            "Spd",
            "Stadtrat",
            "Stadtwerke",
            "Statistik",
            "Straßenbahn",
            "Streik",
            "SV",
            "Halle",
            "Terroranschlag",
            "Ukraine",
            "Unfall",
            "Uniklinik",
            "Universität",
            "Zoo",
        ],
        "with": [
            "Von ihren 32 Jahren im MDR",
            "war Karola Wille 27 Jahre in leitenden Funktionen tätig",
            "Im November 1991 begann sie als Referentin",
        ],
        "without": ["MELDUNGEN AUS DER POLITIK", "AKTUELLE POLIZEI-MELDUNGEN", "NEUESTE KOMMENTARE"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://ebike-mtb.com/advanced-offroad-pro-race-mtb-fs-test/": {
        "file": "ebike-mtb.com-OFFROAD.html",
        "author": "Rudolf Fischer, Simon Kohler",
        "title": "Das neue Advanced OFFROAD Pro Race MTB FS im ersten Test – Newcomer mit Renn-Ambitionen",
        "date": "2023-10-31",
        "description": "Das neue Advanced OFFROAD Pro Race MTB FS soll nicht gebaut worden sein, um Rennen zu fahren, sondern um sie zu gewinnen. Ist das abfahrtsorientierte E-MTB nur was für Rennfahrer oder kommen Hobbypiloten damit auch auf ihre Kosten? Wir haben das E-Mountainbike mit kraftvollem Bosch Performance Line CX Race-Motor für euch getestet. ",
        "categories": ["News", "Test"],
        "tags": [],
        "with": [
            "Ihr habt von der deutschen E-Bike-Brand Advanced noch nie etwas gehört?",
            "Macht nix, wir klären euch auf.",
            "Im City- und Trekking-Bereich ist Advanced bereits gut etabliert.",
        ],
        "without": ["Der Artikel gefällt dir?", "Melde dich für unseren Newsletter an!", "Empfohlen für dich"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://elavegan.com/peanut-butter-truffles/": {
        "file": "elavegan.com-Peanut.html",
        "author": "Ela",
        "title": "PEANUT BUTTER TRUFFLES",
        "date": "2023-10-31",
        "description": "These peanut butter truffles contain a creamy sweet PB center, coated with a dark chocolate shell, perfect as a high-protein, bite-sized snack. Plus, this recipe uses just a few ingredients and is dairy-free, gluten-free, vegan, with a refined sugar-free filling! ",
        "categories": ["Vegan Desserts"],
        "tags": [],
        "with": [
            "If you’re obsessed with peanut butter",
            "and looking for a treat that will stop you",
            "from sticking your spoon directly into the jar (guilty!)",
        ],
        "without": ["AMAZON ASSOCIATES DISCLOSURE", "5 Secrets to Healthy Vegan Cooking", "EXPLORE MORE"],
        "comments": [
            "Wow, deliciousThank you for sharing your work with us! Much love from Portugal",
            "So glad you like it, Julia! Sending love to Portugal.",
            "It called for crushed Graham crackers,",
        ],
        "license": "",
        "region": "",
    },
    "https://exxpress.at/zaehne-zusammenbeissen-festspiel-reisen-von-van-der-bellen-kosteten-57-000-euro/": {
        "file": "exxpress.at-zaehne.html",
        "author": "Redaktion",
        "title": "Zähne zusammenbeißen: Festspiel-Reisen von Van der Bellen kosteten 57.000 Euro",
        "date": "2023-11-01",
        "description": "Während viele österreichische Steuerzahler wegen der enormen Teuerung die Zähne zusammenbeißen mussten, ging Alexander Van der Bellen samt “Hofstaat” auf Festspiel-Tour. Der Bundespräsident fuhr um insgesamt 57.000 Euro nach Salzburg, Bregenz, Erl und Mörbisch. ",
        "categories": ["Politik"],
        "tags": [],
        "with": [
            "Die Kosten für Festspielbesuche des Bundespräsidenten",
            "finden vor allem die Freiheitlichen zum Zähneknirschen",
            "Grund: Die Ausflüge von Van der Bellen zu den vier Kulturevents haben unfassbare 57.000 Euro gekostet",
        ],
        "without": [
            "Das könnte Sie auch interessieren",
            "Ihr Beitrag hilft, unsere Berichterstattung noch",
            "weiter auszubauen und diese weiterhin kostenlos",
        ],
        "comments": ["Er zeigt Österreich immer wieder", "wie dankbar er dafür ist", "dass es ihn dereinst aufgenommen hat!"],
        "license": "",
        "region": "AT",
    },
    "https://finanzmarktwelt.de/signa-rene-benko-daten-berater-289554/": {
        "file": "finanzmarktwelt.de-Benko-Firma.html",
        "author": "Claudio Kummerfeld",
        "title": "Rene Benko-Firma Signa in Sorge – Finanzdaten und Berater-Auftrag",
        "date": "2023-11-01",
        "description": "Das Signa-Immobilienimperium von Rene Benko ist angeschlagen. Jetzt zeigen Finanzdaten die Liquiditätssorgen. ",
        "categories": ["IMMOBILIEN"],
        "tags": ["Rene Benko", "Signa", "Top"],
        "with": ["In Hamburg kommt man aktuell", "kaum an dem Thema vorbei", "Bei mehreren Prestigeprojekten"],
        "without": ["Dax und Gold: Szenarien für heutiges Fed Mega-Event", "LESEN SIE AUCH", "HINTERLASSEN SIE EINE ANTWORT"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://freshideen.com/rezepte/dresdner-stollenfest.html": {
        "file": "freshideen.com-Stollenfest.html",
        "author": "Julia Steinhoff",
        "title": "Dresdner Stollenfest, wo jahrhundertelange Tradition auf handwerkliches Können trifft",
        "date": "2023-10-25",
        "description": "Können Sie sich Weihnachten ohne einen leckeren Christstollen vorstellen? ",
        "categories": [],
        "tags": [],
        "with": [
            "Wir eher nicht!",
            "Denn der berühmte Kuchen mit Rosinen",
            "Marzipan oder Schokolade gehört einfach zum Fest",
        ],
        "without": [
            "Verwandte Artikel",
            "Kalorienarmes Tiramisu mit viel Protein für sportich aktive Personen",
            "Schnelles Abendessen – 2 Blitzrezepte für einen angenehmen Feierabend",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.badische-zeitung.de/viele-studierende-sind-noch-verzweifelt-auf-wohnungssuche-in-freiburg": {
        "file": "badische-zeitung.de-Wohnungssuche.html",
        "author": "Lisa Petrich",
        "title": "Viele Studierende sind noch verzweifelt auf Wohnungssuche in Freiburg",
        "date": "2023-10-18",
        "description": "Die Vorlesungen an der Uni und den Hochschulen starten. Aber nicht alle, die fürs Studium nach Freiburg kommen, haben schon ein Zimmer. Manchen bleibt nur die Notunterkunft des Studierendenwerks. ",
        "categories": ["LOKALES"],
        "tags": [],
        "with": [
            "Gesine aus Tübingen läuft die Zeit davon",
            "Die 18-Jährige hat sich",
            "an der Uni Freiburg für ein Jurastudium eingeschrieben",
        ],
        "without": ["Weitere Artikel", "Abonnement hier kündigen", "Kinder helfen Kindern"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://ga.de/bonn/beuel/mural-in-bonn-graffiti-an-stiftung-gemeindepsychatrie-in-beuel_aid-99369101": {
        "file": "ga.de-Graffiti.html",
        "author": "Anna Müller",
        "title": "Was hinter dem neuen Wandgraffiti in Beuel steckt",
        "date": "2023-11-01",
        "description": "Beuel · Seit kurzem schmücken die Wände des Gebäudes der Stiftung Gemeindepsychatrie ein buntes Graffitigemälde. Die Graffiti-Agentur „Highlightz“ hat die Außenwände neugestaltet – was hinter dem Motiv steckt. ",
        "categories": ["Bonn", "Beuel"],
        "tags": [],
        "with": [
            "Riesengroße Köpfe im Profil",
            "ein Mann mit rotem Hut ist schemenhaft über den Kopf",
            "einer Frau mit geflochtenem Zopf in Blau gelegt",
        ],
        "without": [
            "Jetzt weiterlesen mit",
            "Wir liefern mit anspruchsvollem, modernem Journalismus die Informationen",
            "die für Menschen in unserer Region wichtig sind.",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://groove.de/2023/10/31/anti-a100-aktivist-tobias-trommer-es-wird-an-der-zeit-dass-die-clubs-verantwortung-nehmen/": {
        "file": "groove.de-Anti-A100-Aktivist.html",
        "author": "Charlotte Elsen",
        "title": "Anti-A100-Aktivist Tobias Trommer: „Es wird Zeit, dass Clubs Verantwortung übernehmen”",
        "date": "2023-10-31",
        "description": "Anfang September fand der Demorave „A100 Wegbassen” gegen den Ausbau der Autobahn A100 statt. ",
        "categories": [],
        "tags": [],
        "with": [
            "Treffpunkt ist Berlin-Friedrichshain",
            "direkt vor der Renate",
            "einem der fünf Clubs, die vom Bau der A100 gefährdet sind",
        ],
        "without": [
            "TikTok-Techno 2.0: Ist die Blase geplatzt?",
            "Das Phänomen Stella Bossi: Ein nebulöser Sehnsuchtsort, massentauglich gemacht",
            "Die Konkurrenz ist gnadenlos hart geworden",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://hildesheimer-presse.de/2023/11/01/hund-vertreibt-einbrecher-zeugenaufruf/": {
        "file": "hildesheimer-presse.de-hund.html",
        "author": "",
        "title": "Hund vertreibt Einbrecher – Zeugenaufruf",
        "date": "2023-11-01",
        "description": "Am 31.10.2023, gegen 23:40 Uhr, kam es in der Nordstraße in 31167 Bockenem zu einem versuchten Wohnungseinbruchsdiebstahl. ",
        "categories": [],
        "tags": ["Bockenem", "Nordstraße", "Polizei"],
        "with": [
            "Nach aktuellem Kenntnisstand",
            "schlug der Hund des Hausbewohners zur o. g. Zeit plötzlich an",
            "Als der Bewohner nach dem Rechten schauen wollte",
        ],
        "without": ["Beliebte Artikel", "Ambulante Notfallpraxis der KVN Hildesheim", "Nummer gegen Kummer"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://hpd.de/artikel/sie-wissen-nicht-sie-tun-identitaetspolitische-linke-unterschlaegt-den-homosexuellenhass-neuer-21664": {
        "file": "hpd.de-Homosexuellenhass.html",
        "author": "Moritz Pieczewski-Freimuth",
        "title": "Sie wissen (nicht), was sie tun: Identitätspolitische Linke unterschlägt den Homosexuellenhass neuer Qualität",
        "date": "2023-10-18",
        "description": "Ohrenbetäubende Stille herrschte in der Queer-Community. ",
        "categories": ["GESELLSCHAFT"],
        "tags": ["Homophobie", "Homosexualität", "Gewalt", "Identitätslinke", "Islam"],
        "with": [
            "die traurige Nachricht über den Tod des Transmannes Malte C",
            "in Folge der Verletzungen nach einem Faustangriff",
            "auf der Parade des Christopher Street Days (CSD)",
        ],
        "without": [
            "Israels Überlebenskampf gegen den Terror",
            "Politischer Islam durch die Hintertür",
            "Unterdrückte (Homo-)Sexualität: Ein Risikofaktor für islamistische Gewalt",
        ],
        "comments": [
            "trifft auf alle extremen Denkungsarten zu und macht deutlich",
            "Hass und Hetze, fernab jeglicher Vernunft entsteht",
            "aber teilweise etwas unausgegoren",
        ],
        "license": "",
        "region": "DE",
    },
    "https://idw-online.de/de/news823175": {
        "file": "idw-online.de-Hybridbatterie.html",
        "author": "Dr. Karin J. Schmitz Abteilung Öffentlichkeitsarbeit",
        "title": "Effiziente Hybridbatterie",
        "date": "2023-11-01",
        "description": "Schnell ladende mikrobielle Brennstoffzelle und CO2-Elektrolyseur auf der Basis von Ameisensäure ",
        "categories": [],
        "tags": [],
        "with": [
            "In mikrobiellen Brennstoffzellen verstoffwechseln Bakterien",
            "Energieträgermoleküle und erzeugen dadurch Strom",
            "Wenn die Bakterien energiereiche Moleküle als Energieträger",
        ],
        "without": [
            "Die semantisch ähnlichsten Pressemitteilungen im idw",
            "TUB: Kohlendioxid als Rohstoff für die Umwandlung von Solarstrom in wertvolle chemische Produkte",
            "»Strom als Rohstoff« auf ACHEMA 2018: Grüne Energie für eine nachhaltige Chemie",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "http://simmentalzeitung.ch/Simmental/Boltigen/Trinkwasser-in-Schwarzenmatt-belastet-43157.html": {
        "file": "simmeltalzeitung.ch-Trinkwasser.html",
        "author": "",
        "title": "Trinkwasser in Schwarzenmatt belastet",
        "date": "2023-11-01",
        "description": "Am Samstag, 29. Oktober warnte die Gemeinde Boltigen vor belastetem Leitungswasser in Schwarzenmatt. ",
        "categories": ["Aktuelles", "Archiv", "Boltigen"],
        "tags": [],
        "with": [
            "Auf Nachfrage führte die Gemeinde weiter aus",
            "dass «geringe Mengen» des Bakteriums Escherichia coli im Rahmen",
            "von routinemässigen Probenuntersuchungen gefunden wurden",
        ],
        "without": ["INTERESSANTE ARTIKEL", "Artikel bewerten", "Cookies erleichtern die Bereitstellung unserer Dienste"],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://industriemagazin.at/news/luftfahrtbranche-hebt-nach-corona-ab-und-facc-profitiert/": {
        "file": "industriemagazin.at-Luftfahrtbranche.html",
        "author": "Tom Arnold",
        "title": "Luftfahrtbranche hebt nach Corona ab - und FACC profitiert",
        "date": "2023-10-31",
        "description": 'Der heimische Luftfahrtzulieferer FACC produziert von der starken Luftfahrt: "Wir haben einen gewaltigen Auftragseingang", sagte Konzernchef Robert Machtlinger. Welche Neuerungen FACC in den nächsten Jahren plant und warum der Fachkräftemangel für das Unternehmen kein Problem ist. ',
        "categories": ["NEWS"],
        "tags": ["Maschinenbau", "FACC", "FACC AG", "Robert Machtlinger"],
        "with": [
            "In der Luftfahrt geht es nach der Pandemie wieder rasant bergauf.",
            "Davon ist auch der oberösterreichische Luftfahrtzulieferer FACC deutlich betroffen.",
            "Wir haben einen gewaltigen Auftragseingang",
        ],
        "without": ["Entdecken Sie jetzt", "Sie wollen mehr von uns?", "Weitere interessante Artikel"],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.infosperber.ch/politik/madagaskar-wo-francafrique-endet/": {
        "file": "infosperber.ch-Madagaskar.html",
        "author": "",
        "title": "Madagaskar: Wo Françafrique endet",
        "date": "2023-10-31",
        "description": "Die ehemalige französische Kolonie steht vor dem Niedergang. Das wird auch eine Niederlage für Frankreich sein. ",
        "categories": [],
        "tags": [],
        "with": [
            "Der Insel Madagaskar wurde einst",
            "eine blühende Zukunft vorausgesagt",
            "Nun droht das Land wegen Misswirtschaft und Korruption unterzugehen",
        ],
        "without": ["SEIT 10 TAGEN AM MEISTEN GELESEN", "AKTUELLE DOSSIERS", "SEIT 10 TAGEN AM MEISTEN REAKTIONEN"],
        "comments": [
            "Auf «Telepolis» erschien dieser Tage",
            "ein zweiteiliger Artikel, der sich mit der globalen Hegemonie der USA befasst und erklärt",
            "warum diese schlicht kolonialistisch ist",
        ],
        "license": "",
        "region": "CH",
    },
    "https://sw1.news/fussball/fussball-kreisklassen/wenn-man-in-der-heimat-verliert-dann-tuts-in-abwesendheit-vielleicht-ein-bisschen-weniger-weh/": {
        "file": "SW1.News-Heimat.html",
        "author": "mh",
        "title": "Wenn man in der Heimat verliert, dann tut´s in Abwesendheit vielleicht ein bisschen weniger weh",
        "date": "2023-10-15",
        "description": "AUGSFELD – Zuhause verlieren ist nicht unbedingt schön. Und deshalb freute sich Thomas Häußinger zwar insgeheim ein kleines bisschen auch für den Erfolg des FC Augsfeld, weniger aber, dass das Team aus seinem Wohnort ausgerechnet seine eigene Mannschaft besiegte. ",
        "categories": ["fuSWball", "FB-Rhön Hassberge"],
        "tags": [],
        "with": [
            "Der VfB Humprechtshausen spielte",
            "bislang eine recht ordentliche Saison",
            "brachte der SG Abersfeld bisher deren einzige Niederlage bei",
        ],
        "without": [
            "Das könnte Dich auch interessieren:",
            "ANZEIGE - Heute mal ausgehen/bestellen? Wie wäre es mit:",
            "Wie erwartet machen die beiden Strahlunger Spielertrainer über die Saison hinaus weiter",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://journalistenwatch.com/2023/11/01/ladensterben-immer-dramatischer/": {
        "file": "Journalistenwatch.com-Ladensterben.html",
        "author": "Rasender Reporter",
        "title": "Ladensterben immer dramatischer",
        "date": "2023-11-01",
        "description": "Das giftgrüne Wirtschaftswunder hinterlässt seine ersten Spuren, der Mittelstand wird durch Habeck & Genossen zerstört, die einst florierende deutsche Industrie zur leichten Beute multinationaler Konzerne, bald ist hier alles in amerikanischer und chinesischer Hand, ",
        "categories": [],
        "tags": [],
        "with": [
            "Der Handelsverband Deutschland (HDE)",
            "rechnet jetzt auch noch mit einem beschleunigten Ladensterben",
            "Ein Drittel der Mittelständler will sein Geschäft lieber morgen als übermorgen aufgeben",
        ],
        "without": [
            "Schützt Annalena Baerbock weiterhin iranische Terrorbanden?",
            "Das ist die Totenglocke dieser Regierung!",
            "Hupkonzerte und Rufe der Demonstranten in den Innenstädten",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://jungle.world/artikel/2023/43/diskussion-begriff-imperialismus-das-phantom": {
        "file": "jungle.world-Imperialismus-Phantom.html",
        "author": "Ernst Lohoff",
        "title": "Das Imperialismus-Phantom",
        "date": "2023-10-26",
        "description": "Die heutigen Konflikte zwischen autoritären und westlichen Staaten lassen sich mit dem Begriff Imperialismus nicht erklären. Sie sind Teil eines Weltbürgerkriegs, bei dem die Grenze zwischen Außen- und Innenpolitik verschwimmt. ",
        "categories": ["Disko"],
        "tags": ["Russland", "Antiimperialismus", "Kolonialismus", "Ukrainekrieg"],
        "with": [
            "In den vergangenen 100 Jahren",
            "war noch nie so viel von Imperialismus die Rede wie heute",
            "und zwar quer durch die politischen Lager",
        ],
        "without": [
            "Artikel zum Thema",
            "Die Hamas und die blinden Flecken der Linken",
            "Imperialismustheorie statt Antiimperialismus",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://katapult-magazin.de/de/artikel/anzahl-zugelassener-parteien": {
        "file": "KATAPULT-Magazin.de-parteien.html",
        "author": "Tim Ehlers",
        "title": "Anzahl zugelassener Parteien",
        "date": "2023-10-26",
        "description": "Nach einer Wahl werden in den Nachrichten (verständlicherweise) meist nur die Gewinner bzw. die Ergebnisse der großen Volksparteien veröffentlicht. ",
        "categories": [],
        "tags": [],
        "with": [
            "es zu viele sind und viele auch nur",
            "in wenigen Bundesländern mit einer Landesliste antreten",
            "haben wir uns auf die größten beschränkt.",
        ],
        "without": [
            "Neueste Artikel",
            "Rechte in MV nötigen KATAPULT",
            "Rechte, Rechtsextreme und Querdenker aus MV versuchen, KATAPULT einzuschüchtern. Mit erstem Erfolg. Die Lage ist kritisch. Wir wollen das nicht hinnehmen.",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://apolut.net/interview-mit-schriftstellerin-sonja-silberhorn/": {
        "file": "apolut.net-Sonja-Silberhorn.html",
        "author": "Eugen Zentner",
        "title": "Interview mit Schriftstellerin Sonja Silberhorn",
        "date": "2023-10-28",
        "description": "„Es gibt offensichtlich mehr krimilesende Kritiker der Pandemiepolitik als bisher vermutet.“ ",
        "categories": ["apolut Artikel"],
        "tags": [
            "Cancel Culture",
            "Corona-Krise",
            "COVID-Impfung",
            "Eugen Zentner",
            "gesellschaftliche Verwerfungen",
            "herrschende Mehrheitsmeinung",
            "Konformitätsdruck",
            "Kriminalroman",
            "Leitmedien",
            "Maßnahmenkritiker",
            "menschenverachtend",
            "nachdenkseiten",
            "Pandemie",
            "parallele Kulturindustrie",
            "Schriftstellerin",
            "Schwurbler",
            "Sonja Silberhorn",
            "tendenziöser Journalist",
        ],
        "with": [
            "Die deutsche Autorin Sonja Silberhorn",
            "hat die Corona-Krise und ihre gesellschaftlichen Folgen in einem Kriminalroman verarbeitet",
            "Den legte sie einem mittelgroßen",
        ],
        "without": [
            "Auch interessant...",
            "Leuchtturm ARD ORF SRG – Initiative zur Beitragsbefreiung",
            "Mein Leben als Monster",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://kinzig.news/23578/das-steckt-dahinter-nachhaltigkeit-bei-der-spessart-tourismus-gmbh": {
        "file": "kinzig.news-Nachhaltigkeit.html",
        "author": "MORITZ PAPPERT",
        "title": "Interview mit Bernhard Mosbacher und Franziska Weber",
        "date": "2023-11-01",
        "description": "Das steckt dahinter: Nachhaltigkeit bei der Spessart Tourismus GmbH ",
        "categories": [],
        "tags": [],
        "with": [
            "Auf den Tourismus bezogen ist Nachhaltigkeit für uns",
            "dass wir die Entwicklung in der Region mit allen Leistungsträgern",
            "die an der touristischen Wertschöpfungskette beteiligt sind",
        ],
        "without": [
            "MEHR ZUM THEMA",
            "Digitalisierung im Forst: Das sind die Chancen und Herausforderungen",
            "Naturschutzbeamter Lukas Rippl und Revierleiterin Manuela Gebhard zeigen",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://kulturnews.de/fensterputzen-mit-den-ratboys-the-window-live/": {
        "file": "kulturnews.de-Deutschland-Tour.html",
        "author": "Felix Eisenreich",
        "title": "Fensterputzen mit den Ratboys: „The Window“ live",
        "date": "2023-11-01",
        "description": "Die Postcountryband nimmt sich dem Tod als Blick durchs Fenster an und lüftet auf Tour einmal ordentlich durch. ",
        "categories": ["Musik"],
        "tags": ["Ratboys", "Postcountry", "Indierock"],
        "with": [
            "Für Julia Steiner, Sängerin und Frontfrau der Ratboys",
            "war eines unausweichlich",
            "Das neue Album der Postcountryband musste den Titel",
        ],
        "without": [
            "Brecht Reloaded: „Wie der Schnee“ – die neue Single von Soeckers",
            "Gefühle wie Rohdiamanten: „strawberry picking“ – die neue Single von being anne",
            "Befreite Beats: „Kalter Rauch“ – das Singledebüt von HUND",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://kyffhaeuser-nachrichten.de/news/news_lang.php?ArtNr=335614": {
        "file": "kyffhaeuser-nachrichten.de-Regen.html",
        "author": "",
        "title": "So viel Regen gab es lange nicht",
        "date": "2023-10-31",
        "description": "Das Wetter eignet sich ja bekanntermaßen exzellent dazu, behäbige Konversation zu beleben. ",
        "categories": ["NEWS"],
        "tags": [],
        "with": [
            "Statt herkömmlichem Herbstwetter brachte",
            "der Oktober 2023 sehr viel Regen und eine äußerst milde Witterung mit sommerlichen Nuancen",
            "Die Vegetation kleidete sich nur zögerlich herbstlich",
        ],
        "without": [
            "Am meisten gelesen...",
            "Letzte Kommentare",
            "NACHRICHTEN AUS DEM KYFFHÄUSERKREIS - REGIONAL, SCHNELL, KOSTENLOS, SUPER DIGITAL",
        ],
        "comments": [
            "es gab dieses Jahr echt Regen",
            "Schön so. Ja. Jetzt gleicht sich die Natur wieder aus",
            "So isses halt.",
        ],
        "license": "",
        "region": "DE",
    },
    "https://lebensmittelpraxis.de/handel-aktuell/38519-olympische-spiele-in-paris-getraenke-per-schiff-ins-stadtzentrum.html": {
        "file": "Lebensmittelpraxis.de-Stadtzentrum.html",
        "author": "",
        "title": "Getränke per Schiff ins Stadtzentrum",
        "date": "2023-11-01",
        "description": "Im Anlauf zu den Olympischen Spielen im kommenden Sommer in Paris wird eine Belieferung mit Getränken über die Seine getestet, insbesondere um den Transport von Getränken möglichst umweltfreundlich zu organisieren und den Verkehr zu entlasten. Die Supermarktkette Franprix hat damit bereits Erfahrung. ",
        "categories": ["HANDEL"],
        "tags": ["ALKOHOLFREIE GETRÄNKE", "LOGISTIK UND VERPACKUNG", "LOGISTIK", "FRANKEICH", "GETRÄNKEWIRTSCHAFT"],
        "with": [
            "Dazu werden die Getränke per Schiff",
            "von einem Lager im Umland zu einem Kai gegenüber dem Eiffelturm geliefert",
            "teilte die Pariser Hafengesellschaft mit",
        ],
        "without": ["Das könnte Sie auch interessieren", "Viel gelesen in Handel", "Supermarkt des Jahres 2023"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://literaturkritik.de/franke-cotten-die-anleitungen-der-vorfahren,30063.html": {
        "file": "literaturkritik.de-Ann-Cotten.html",
        "author": "Vanessa Franke",
        "title": "Vom Boden aus gedacht",
        "date": "2023-11-01",
        "description": "Ann Cotten verwebt in „Die Anleitungen der Vorfahren“ Lokales und Globales ",
        "categories": [],
        "tags": [],
        "with": [
            "Es braucht ein wenig Zeit",
            "um sich auf diesen Text einzulassen",
            "Weder Lyrikband noch ethnologischer Bericht noch Erzählung",
        ],
        "without": [
            "Ergebnisse einer internationalen Tagung zu einem Forschungsprojekt",
            "über Heimat, Raum und Emotion in der Literatur seit 1945 bis zur Gegenwart",
            "Ich habe die Portraits mit großem Vergnügen gelesen",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://lokalo.de/artikel/310144/weinbergsbahnen-in-erden-nicht-manipuliert-ermittlungen-zu-trittenheimer-fall-gehen-weiter/": {
        "file": "lokalo.de-Weinbergsbahnen.html",
        "author": "",
        "title": "Weinbergsbahnen in Erden nicht manipuliert – Ermittlungen zu Trittenheimer Fall gehen weiter",
        "date": "2023-11-01",
        "description": "ERDEN. Wie von lokalo.de berichtet, meldete die Polizei Anfang Oktober, dass an zwei Zahnradbahnen in der Weinlage “Erdener Prälat” an der B53 zwischen Ürzig und Kinheim technische Manipulationen zur Anzeige gebracht worden waren. Vermutet wurde damals bewusste Sabotage an den Monorackbahnen. ",
        "categories": ["Blaulicht"],
        "tags": ["Blaulicht", "Trier & Region", "Trier-Saarburg", "Bernkastel-Wittlich"],
        "with": [
            "Vorausgegangen war ein Fall in Trittenheim",
            "bei dem sich ein 21-jähriger Winzersohn",
            "aus dem Ort am 25.9.2023 nur durch einen beherzten Sprung retten konnte",
        ],
        "without": [
            "++ Wetter in der Region: Aussichten bis Freitag mild, aber ungemütlich ++",
            "FDP-Landes- und Kommunalpolitiker stellen Bundes-Ampel infrage – sieben aus RLP",
            "VOLKSWAGEN ZENTRUM TRIER",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://makronom.de/warum-es-ein-ressourcenschutzgesetz-braucht-45273": {
        "file": "makronom.de-Ressourcenschutzgesetz.html",
        "author": "CLARA LÖW, SIDDHARTH PRAKASH & KLAUS JACOB",
        "title": "Warum es ein Ressourcenschutzgesetz braucht",
        "date": "2023-10-26",
        "description": "Der jährliche Rohstoffkonsum in Deutschland muss bis Mitte des Jahrhunderts mindestens halbiert werden. Dafür braucht es eine Verbindlichkeit, die in einem Ressourcenschutzgesetz analog zum Klimaschutzgesetz festgehalten werden sollte. ",
        "categories": ["ENERGIE & UMWELT"],
        "tags": [],
        "with": [
            "Es besteht ein direkter Zusammenhang",
            "zwischen Rohstoffnutzung und Auswirkungen",
            "auf den Zustand der Umwelt und Ökosysteme",
        ],
        "without": [
            "MEHR ZUM THEMA",
            "CIRCULAR ECONOMY UND NACHHALTIGE SOZIALE MARKTWIRTSCHAFT",
            "Unser kostenloser Newsletter informiert Sie über unsere neuesten Beiträge.",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://mein-mmo.de/silkroad-online-erstes-mmorpg-cringe-dieb/": {
        "file": "mein-mmo.de-MMORPG.html",
        "author": "Cortyn",
        "title": "Mein 1. MMORPG Silkroad Online hat mich zum Cringe-Dieb gemacht und zu Hentai geführt",
        "date": "2023-11-01",
        "description": "MeinMMO-Dämon Cortyn erzählt vom ersten MMORPG. In Silkroad Online war die Welt noch in Ordnung – oder so ähnlich. Denn die erste Gilde wollte viel und konnte gar nichts. ",
        "categories": [],
        "tags": [],
        "with": [
            "Die erste große MMORPG-Liebe ist etwas ganz besonderes",
            "Selbst wenn viele Erinnerungen inzwischen ein wenig verschwommen sind",
            "weiß ich noch sehr gut",
        ],
        "without": ["MEHR KOLUMNEN AUF MEINMMO", "KOMMENDE SPIELE", "NEUESTE ARTIKEL"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://missy-magazine.de/blog/2023/10/30/interabled-sex-education/": {
        "file": "missy-magazine.de-interabled.html",
        "author": "Evan Tepest",
        "title": "Interabled Sex Education",
        "date": "2023-10-30",
        "description": "Evan Tepest und Selma Kay Matter beschreiben, wie Dating zwischen chronisch kranker und able-bodied Person aussehen kann. ",
        "categories": ["Kolumnen"],
        "tags": [],
        "with": [
            "Sex ist immer schon etwas anderes als es selbst.",
            "Müssen wir verstehen, was wir begehren?",
            "Wo fängt die Lust an und wer entscheidet",
        ],
        "without": ["Verträge kündigen", "weitere Artikel", "Körper&Sex"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://nachtkritik.de/kolumnen-georg-kasch/kolumne-queer-royal-ueber-dragqueens-und-dragkings-auf-und-jenseits-der-buehne": {
        "file": "nachtkritik.de-Dragqueens.html",
        "author": "Georg Kasch",
        "title": "Im Schlepptau",
        "date": "2023-10-31",
        "description": "Dragqueens sind Kunstfiguren aus Make-Up und Glitter, auf Partys und in Shows, auch in der Freien Szene und im Stadttheater. Jetzt finden sie sich zunehmend in den Schusslinien der Identitätsdebatten wieder. ",
        "categories": ["kolumnen"],
        "tags": [],
        "with": [
            "Woher kommt eigentlich der Hass auf Dragqueens?",
            "Früher, als Travestiekünstler wie Georg Preuße",
            "und Reiner Kohler noch als Mary und Gordy die Bühnen beherrschten",
        ],
        "without": ["neueste kommentare", "mehr Kolumnen", "impressum & kontakt"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://nh24.de/2023/11/06/mitarbeiter-fordern-bundeswehr-auftraege-fuer-deutsche-unternehmen/#more-244202": {
        "file": "nh24.de-Bundeswehr.html",
        "author": "",
        "title": "Mitarbeiter fordern Bundeswehr-Aufträge für deutsche Unternehmen",
        "date": "2023-11-06",
        "description": "In Sorge um ihre Arbeitsplätze demonstrierten am Montag etwa 500 Mitarbeiter von Airbus Helicopters Technik und Airbus Helicopters Deutschland in Calden vor dem Werkstor unter dem Motto „Für unsere Sicherheit“. ",
        "categories": ["Panorama"],
        "tags": ["CALDENIG", "METALL", "LANDKREIS KASSEL"],
        "with": [
            "Die Befürchtung der Beschäftigten resultiert",
            "aus der vermehrten Beschaffung von Flugzeugen",
            "und Hubschraubern für die Bundeswehr aus US-Produktion",
        ],
        "without": ["PLAG-ADVENTS-ANGEBOT", "BESTATTUNGSHAUS WILLE IN KNÜLLWALD", "SCHUHHAUS HERCHE RÄUMUNGSVERKAUF"],
        "comments": [
            "Seit Bestehen der Bundeswehr 1956 starben 3.387",
            "Im Straßenverkehr starben in manche Jahren 11.300 Verkehrsteilnehmer",
            "In der heutigen Zeit ist es sehr wichtig in ein schlagkräftiges Militär zu investieren",
        ],
        "license": "",
        "region": "DE",
    },
    "https://n-land.de/top-story/74-jaehriger-stirbt-nach-unfall-in-simmelsdorf": {
        "file": "n-land.de-Simmelsdorf.html",
        "author": "",
        "title": "74-Jähriger stirbt nach Unfall in Simmelsdorf",
        "date": "2023-11-06",
        "description": "Am Samstag, 4. November, gegen 17.50 Uhr, ist ein 74-Jähriger mit seinem PKW in Simmelsdorf in Richtung Ortsmitte gefahren. ",
        "categories": [],
        "tags": ["Unfall", "Rettungsdienst", "Simmelsdorf", "Polizei"],
        "with": [
            "Gegenüber einer Verkehrsteilnehmerin",
            "die sich mit ihrem Fahrzeug hinter dem Pkw-Fahrer befand",
            "gab er gesundheitliche Probleme an und verlor das Bewusstsein",
        ],
        "without": [
            "Das könnte Sie auch interessieren",
            "Unbekannter stiehlt mehrere E-Bikes aus Kellerabteilen in Altdorf",
            "Über drei Promille: Alkoholisierter Fahrer baut Unfall in Lauf",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://nnz-online.de/news/news_lang.php?ArtNr=335853": {
        "file": "nnz-online.de-Quantensprung.html",
        "author": "",
        "title": "Ein Quantensprung für Nordhausen Nord",
        "date": "2023-11-06",
        "description": 'In Nord wurde am Freitag die neue Spiel- und Freizeitanlage, der "Nordpark" eröffnet. Für das Quartier sei die neue Mehrgenerationenanlage ein "Quantensprung", hieß es aus dem Rathaus… ',
        "categories": ["NEWS"],
        "tags": [],
        "with": [
            "Gemeinsam mit Kindern der Kindertageseinrichtung",
            "des Jugendclubs Mitte sowie Jugendlichen des Kinder- und Jugendstadtrates",
            "eröffnete Oberbürgermeister Kai Buchmann am vergangenen Freitag",
        ],
        "without": ["Am meisten gelesen...", "Letzte Kommentare", "Top 10 Artikel der letzten 10 Tage als RSS"],
        "comments": [
            "Quantensprung? Wohl eher ein kleiner Schritt.",
            'Ich will den Nordhäusern ihre neue "Attraktion" gar nicht madig machen',
            "und es ist auch schön, dass man daran arbeitet",
        ],
        "license": "",
        "region": "DE",
    },
    "https://omr.com/de/daily/cowboyboots-und-crocs": {
        "file": "omr.com-Schuhbrand.html",
        "author": "TANJA KARRASCH",
        "title": "Jetzt auch noch Cowboyboots: Crocs erzielt Milliardenumsätze durch verrückte Releases und Kollaborationen",
        "date": "2023-11-03",
        "description": "Für 2023 rechnet das US-Unternehmen aus Colorado mit 3,9 Milliarden US-Dollar Umsatz. Aber nicht alle Geschäftsbereiche laufen gut ",
        "categories": ["Daily"],
        "tags": ["Social", "Commerce"],
        "with": [
            "Während Birkenstocks aber im Vergleich zum Crocs",
            "der gewisse Funfaktor fehle",
            "sagt Landowski, bringe man Crocs nicht mit den typischen Birkenstocks-Attributen",
        ],
        "without": [
            "Empfohlener redaktioneller Inhalt",
            "Aktuelle Stories und die wichtigsten News für Marketeers direkt in dein Postfach!",
            "OMR Family Member",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://onlinemarketing.de/social-media-marketing/instagram-neue-videofunktion-stories": {
        "file": "OnlineMarketing.de-Instagram.html",
        "author": "Swantje Schemmerling",
        "title": "Instagram arbeitet an neuer Videofunktion für Stories",
        "date": "2023-11-06",
        "description": "Das Meta-Unternehmen Instagram arbeitet an einem neuen Feature für die Stories. Dieses ist vor allem für Creator interessant. ",
        "categories": ["Social Media Marketing"],
        "tags": [],
        "with": [
            "Nutzer:innen haben die Möglichkeit",
            "ein bis zu 15 Sekunden langes Video mit ihrem Smartphone aufzunehmen",
            "und danach über Instagram in ihren Stories hochzuladen.",
        ],
        "without": ["Dein personalisierter Newsletter", "Whitepaper kostenlos downloaden", "Webinare zu digitalen Themen"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://ostbelgiendirekt.be/tv-tipp-loriot-100-367167": {
        "file": "Ostbelgiendirekt.be-ARD-Doku.html",
        "author": "",
        "title": "TV-TIPP – „Loriot 100“: ARD-Doku zum 100. Geburtstag des größten deutschen Humoristen",
        "date": "2023-11-06",
        "description": "Mit seinen Figuren, Sketchen und Filmen voller Wortwitz und skurriler Komik schrieb Vicco von Bülow alias Loriot im deutschsprachigen Raum TV-Geschichte. Die ARD feiert seinen Hundertsten – am 12. November – unter anderem mit einer liebevollen Doku. ",
        "categories": ["Nachrichten"],
        "tags": [],
        "with": [
            "Die ARD hat für ihre Mediathek",
            "eine umfangreiche Schau mit Loriots bekanntesten Werken",
            "Das Widget mit den ikonischen Sketch- und Cartoon-Klassikern von SWR",
        ],
        "without": ["Populäre Artikel der letzten 7 Tage", "Aktuelle Kommentare", "Alles nur Satire"],
        "comments": [
            "LORIOT hätte es heutzutage schwer im Fernsehen",
            "besser gesagt, man würde ihn für politisch inkorrekt erklären",
            "und auf die rote Liste von Künstlern setzen, die man diffamieren kann und muss",
        ],
        "license": "",
        "region": "DE",
    },
    "https://osthessen-news.de/n11752374/claudia-brandes-und-ihr-links-gruenes-buendnis-muessen-jetzt-liefern.html": {
        "file": "Osthessen-news.de-Buergermeisterwahl.html",
        "author": "Christian P. Stadtfeld",
        "title": "Claudia Brandes und ihr links-grünes Bündnis müssen jetzt liefern",
        "date": "2023-11-06",
        "description": "Sensation in der schwarzen Hochburg Petersberg bei Fulda! Aus dem Stand heraus wird die 32 Jahre alte Claudia Brandes Bürgermeisterin der wirtschaftlich und strukturell bestens aufgestellten Großgemeinde und erreicht damit einen Höhepunkt in ihrem abwechslungsreichen Leben. ",
        "categories": ["NACHRICHTEN"],
        "tags": [],
        "with": [
            "Zunächst ist festzustellen",
            "dass die CDU in Petersberg und ihr Bürgermeister",
            "in den vergangenen sechs Jahren nicht unbedingt einen harmonischen Eindruck hinterlassen haben",
        ],
        "without": ["DEIN HEIMATPODCAST", "Petersberg Bürgermeisterwahl - weitere Artikel", "DEN RICHTIGEN FINDEN"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://peppermynta.de/fashion-guides/fair-fashion-strick-nachhaltige-strickmode-mulesingfrei-knitwear/": {
        "file": "peppermynta.de-Strickmode.html",
        "author": "JULIA ESDAR",
        "title": "FAIR FASHION STRICK – UNSERE LIEBSTEN LABELS FÜR NACHHALTIGE STRICKMODE",
        "date": "2023-11-06",
        "description": "Was wäre Wintermode ohne kuschelige Knitwear? Ob grob oder fein gestrickt, in Form von flauschigen Pullovern oder schicken Strickkleidern: Von fairer Strickmode können wir gerade im Herbst und Winter nicht genug bekommen. Wir stellen euch heute unsere liebsten Fair Fashion Strick Labels vor, bei denen ihr nachhaltige Strickmode findet – schön eingekuschelt sind wir gewappnet für die kalte Jahreszeit. ",
        "categories": [],
        "tags": [
            "achiy",
            "alpakawolle",
            "cashmere",
            "chiengora",
            "claudia-lanius",
            "eco-knitwear",
            "edelziege",
            "faible-and-failure",
            "fair-fashion-cardigan",
            "fair-fashion-pullover",
            "fair-fashion-strick",
            "fair-fashion-strickjacke",
            "fair-fashion-strickpullover",
            "fair-produzierte-strickmode",
            "handarbeit",
            "handgestrickt",
            "handgestrickte-knitwear",
            "handgestrickte-pullover",
            "handmade",
            "hanishken",
            "hessnatur",
            "hundewolle",
            "isabelle-mann",
            "jann-june",
            "kaschmir",
            "kaschmirwolle",
            "knitwear",
            "kontrolliert-biologische-tierhaltung",
            "lanius",
            "living-crafts",
            "maiami",
            "merino-wolle",
            "merinowolle",
            "merz-b-schwanen",
            "mila-vert",
            "modus-intarsia",
            "mulesing",
            "mulesingfree",
            "mulesingfrei",
            "mulesingfreie-merinowolle",
            "nachhaltige-strickmode",
            "naturfasern",
            "recolution",
            "wolle",
            "wunderwerk",
            "yak-wolle",
        ],
        "with": [
            "Was wäre Wintermode ohne kuschelige Knitwear",
            "und ist gerade in der konventionellen Tierhaltung oftmals mit viel Tierleid verbunden",
            "Fairer Strick Made in Europe",
        ],
        "without": [
            "Das könnte Dich auch noch interessieren",
            "Kennt ihr schon unseren Brandfinder?",
            "Studiert im Master European Culture and Economy",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://pinkstinks.de/das-patriarchat-als-kulturtechnik/": {
        "file": "pinkstinks.de-Kulturtechnik.html",
        "author": "Nils Pickert",
        "title": "DAS PATRIARCHAT ALS KULTURTECHNIK",
        "date": "2023-10-25",
        "description": "Für gewöhnlich beginne ich Texte nicht mit Zitaten aus Max Webers Wirtschaft und Gesellschaft. ",
        "categories": ["Allgemein"],
        "tags": [],
        "with": [
            "Zum einen sind wir hier nicht in einem Proseminar Soziologie.",
            "Zum anderen haben Soziologinnen wie Eva Cyba mit Geschlecht und soziale Ungleichheit",
            "Existenz und Wirkweise des Patriarchats sehr viel deutlicher herausgearbeitet als Max Weber",
        ],
        "without": ["FOLGT UNS!", "AKTUELLE BEITRÄGE", "ÄHNLICHE BEITRÄGE"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://polizeiticker.ch/artikel/studen-be-a6-nach-toedlichem-unfall-fuer-mehrere-stunden-gesperrt-219645": {
        "file": "polizeiticker.ch-Unfall.html",
        "author": "Redaktion Polizeiticker Schweiz",
        "title": "Studen BE - A6 nach tödlichem Unfall für mehrere Stunden gesperrt",
        "date": "2023-11-06",
        "description": "Am Sonntagabend kam es auf der A6 bei Studen zu einem schweren Verkehrsunfall. Ein Autofahrer verstarb noch auf der Unfallstelle. Eine weitere Autofahrerin wurde verletzt ins Spital gebracht. Die A6 zwischen Brügg und Lyss Nord war für mehrere Stunden gesperrt. Der Unfall wird untersucht. ",
        "categories": [
            "Polizeiticker Bern",
            "Unfälle (Unfälle heute, Unfall mit Todesfolge heute, Arbeitsunfälle, Freizeitunfälle) ",
            "Verkehr (Staumeldungen, Radarwarnungen, Geschwindigkeitskontrollen, Strassensperrungen)",
        ],
        "tags": [],
        "with": [
            "Am Sonntag, 5. November 2023, kurz nach 21.25 Uhr",
            "wurde der Kantonspolizei Bern auf der A6 bei Studen ein schwerer Verkehrsunfall gemeldet",
            "Aus ungeklärten Gründen fuhr ein Autolenker im Bereich der Ausfahrt",
        ],
        "without": ["KANTONS-SUDOKU", "KANTONSÜBERSICHT", "FAHNDUNGEN"],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://popkultur.de/homosexuelle-schauspieler/": {
        "file": "Popkultur.de-Schauspieler.html",
        "author": "Lisa Borch",
        "title": "Die 25 erfolgreichsten homosexuellen Schauspieler aller Zeiten",
        "date": "2023-05-06",
        "description": "Tauche ein in die beeindruckenden Karrieren der erfolgreichsten homosexuellen Schauspieler aller Zeiten. Diese Stars haben die Filmwelt nachhaltig geprägt. ",
        "categories": ["Filme & Serien", "Schauspieler/innen"],
        "tags": ["featured", "Top-Thema"],
        "with": [
            "Über die Jahre hinweg haben homosexuelle Schauspieler",
            "ihren unverwechselbaren Stempel auf die Welt des Entertainments gesetzt.",
            "Trotz Hindernissen und Vorurteilen",
        ],
        "without": [
            "Neue Beiträge",
            "Die zehn besten & schönsten Smartwatches für Frauen",
            "Die 25 erfolgreichsten schwedischen Sänger & Sängerinnen",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://presse-augsburg.de/augsburger-verkehrs-und-tarifverbund-avv-erhoeht-die-oepnv-preise-deutlich/909665/": {
        "file": "presse-ausburg.de-Tarifverbund.html",
        "author": "Presse Augsburg",
        "title": "Augsburger Verkehrs- und Tarifverbund AVV erhöht die ÖPNV-Preise deutlich",
        "date": "2023-11-06",
        "description": "Die Ticketpreise im AVV werden ab 1. Januar 2024 um durchschnittlich 12,7 Prozent angehoben. ",
        "categories": [],
        "tags": ["Thema", "Wirtschaft", "Region", "News", "Newsletter"],
        "with": [
            "Wir müssen insbesondere die stark gestiegenen Kosten",
            "für Energie und Kraftstoff an die Verkehrsunternehmer ausgleichen",
            "um die Grundlage zu schaffen",
        ],
        "without": [
            "Jetzt Singles finden",
            "Nachrichten für Augsburg und Bayerisch-Schwaben.",
            "Pro Asyl nennt EU-Migrationsdeal „historischen Tiefpunkt“",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://public.spot-on-news.de/neue-traumfrau-bei-sturm-der-liebe-so-geht-es-am-fuerstenhof-weiter/": {
        "file": "public.spot-on-news.de-Traumfrau.html",
        "author": "",
        "title": "Neue Traumfrau bei „Sturm der Liebe“: So geht es am Fürstenhof weiter",
        "date": "2023-11-06",
        "description": "Seit 2005 läuft die beliebte ARD-Telenovela „Sturm der Liebe“ bereits im TV ",
        "categories": ["TV"],
        "tags": [],
        "with": [
            "Und jetzt steht die 20. Staffel der Erfolgsserie",
            "rund um die Geschehnisse am Fürstenhof in den Startlöchern",
            "Wie die Macher bekannt gaben",
        ],
        "without": [
            "Mehr über TV",
            "Judith Williams als Rategast im „The Masked Singer“-Finale",
            "Lindholm zurück in Hannover: „Tatort“-Ende für das Göttinger Team",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://publikum.net/japan-und-die-hpv-impfungen/": {
        "file": "publikum.net-HPV-Impfungen.html",
        "author": "Der Spendenteddy",
        "title": "Japan und die HPV-Impfungen",
        "date": "2023-07-30",
        "description": "Die unglaubliche Geschichte eines Verbotes, das es nie gab ",
        "categories": ["IMPFEN"],
        "tags": [],
        "with": [
            "Vor langer, langer Zeit hatte ich schon einmal",
            "die Behauptung aufgegriffen",
            "Japan hätte die HPV-Impfungen verboten",
        ],
        "without": [
            "Werde teil der Community!",
            "Melde dich jetzt an, um selbst Artikel zu verfassen",
            "zu kommentieren und mitzubestimmen",
        ],
        "comments": ["Anonym", "was soll dieser", "faschistische dreck?"],
        "license": "",
        "region": "",
    },
    "https://raptastisch.net/2023/11/06/bushido-antwortet-auf-seitenhieb-von-azad-und-erklaert-ihn-fuer-finished/": {
        "file": "Raptastisch.net-Seitenhieb.html",
        "author": "Octavius Hallenstein",
        "title": "Bushido antwortet auf Seitenhieb von Azad und erklärt ihn für „finished“",
        "date": "2023-11-06",
        "description": "Deutschrap befindet sich weiterhin im Diss-Modus. Mit seinen „Knaben Bars“ meldete sich kürzlich Animus wieder zurück und droppte seinen ersten Track seit seinem Umzug nach Deutschland. In dem Song wird scharf gegen verschiedenste Interpreten geschossen. Darunter auch Legenden wie Kool Savas und Azad. ",
        "categories": ["Raptastisch", "Allgemein", "Diss", "Information"],
        "tags": ["Azad", "Bushido", "finished", "Seitenhieb"],
        "with": [
            "Azad war mein Vorbild, doch ist innerlich am Sack",
            "Weil er mit fünfzig Jahren nichts außer Erinnerungen hat",
            "Ich half ihm bis zum letzten Satz wie einem Onkel",
        ],
        "without": [
            "Kranke Zahlen – Bushido führt im privaten Verkaufsbattle gegen Bonez MC",
            "Nie wieder – Fard gibt Statement zu Farid Bang ab",
            "Raptastisch auf Facebook",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://reitschuster.de/post/tagesschau-unterschlaegt-hass-demo-in-essen/": {
        "file": "reitschuster.de-Hass-Demo.html",
        "author": "Daniel Weinmann",
        "title": "Tagesschau unterschlägt Hass-Demo in Essen",
        "date": "2023-11-06",
        "description": "Sie ist nicht nur – nach eigenen Angaben – die erfolgreichste Nachrichtensendung Deutschlands. ",
        "categories": ["Antisemitismus", "Öffentlich-Rechtliche"],
        "tags": ["ARD", "Demonstrationen", "Tagesschau"],
        "with": [
            "Auch die Tagesschau-Verantwortlichen drehten bei",
            "In der 20 Uhr-Ausgabe vom Sonntagabend präsentierte man",
            "doch einen Bericht über die Großdemonstration in Essen vom Vorabend",
        ],
        "without": ["Mein Tweet des Tages", "Meine aktuellen Videos", "Besuchen Sie unseren Fan-Shop!"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://report24.news/so-nah-kam-eine-iranische-drohne-einem-us-flugzeugtraeger/": {
        "file": "report24.news-Drohne.html",
        "author": "Heinz Steiner",
        "title": "So nah kam eine iranische Drohne einem US-Flugzeugträger",
        "date": "2023-11-06",
        "description": "Die iranische Nachrichtenagentur Tasnim hat Videoaufnahmen einer Drohne veröffentlicht, die unbehelligt über den US-amerikanischen Flugzeugträger USS Eisenhower flog. Ein Angriff wäre problemlos möglich gewesen. ",
        "categories": [],
        "tags": [],
        "with": [
            "Wie das nachfolgende auf X verbreitete",
            "Video der iranischen Nachrichtenagentur",
            "Tasnim News verdeutlicht",
        ],
        "without": [
            "Neueste Artikel",
            "EHRUNG FÜR WIDERSTÄNDIGE - JETZT BESTELLEN!",
            "JETZT VORSORGEN - SPAREN SIE BIS ZU 500 EURO!",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://scienceblogs.de/mathlog/2023/11/06/muenzwuerfe-sind-nicht-zufaellig/": {
        "file": "scienceblogs.de-zufaellig.html",
        "author": "Thilo",
        "title": "Münzwürfe sind nicht zufällig",
        "date": "2023-11-06",
        "description": "In Vorlesungen über Wahrscheinlichkeitstheorie oder Statistik erzähle ich den Studenten, dass es Zufall ausserhalb der Mikrowelt der Quantenphysik nicht gibt. ",
        "categories": [],
        "tags": ["Münzwurf", "Präzession", "wahrscheinlichkeit"],
        "with": [
            "Alles ist im Prinzip berechenbar",
            "Zufall entsteht nur durch unvollständige Information",
            "Der Wurf einer Münze ist nicht zufällig",
        ],
        "without": ["Neueste Beiträge", "Top Posts from WordPress stats", "ScienceBlogs ist ein geschütztes Markenzeichen."],
        "comments": [
            "Aber ist der makroskopische",
            "scheinbare Zufall letztlich nicht auch durch den quantenmechanischen Zufall bedingt",
            "Die Molekülbewegungen in der Luft",
        ],
        "license": "",
        "region": "DE",
    },
    "https://winfuture.de/news,139377.html": {
        "file": "winfuture.de-NASA.html",
        "author": "Christian Kahle",
        "title": "NASA+ startet: Streaming ohne Gebühren, Werbung oder Registrierung",
        "date": "2023-11-03",
        "description": "Die Weltraumorganisation NASA hat ebenso spektakuläre und span­nende Dinge zu bieten wie große Medienkonzerne. Davon können sich Nutzer bald selbst überzeugen: Am Mittwoch startet man mit NASA+ einen eigenen Streaming-Dienst und eine passende App. ",
        "categories": [],
        "tags": ["NASA"],
        "with": [
            "Wir starten mehr als Raketen",
            "Der Start der Plattform ist Bestandteil einer weitgehenden Überarbeitung",
            "der digitalen Plattformen, die die NASA im Sommer angekündigt hatte",
        ],
        "without": ["Neue NASA-Fotos", "Videos zum Thema", "Beiträge aus dem Forum"],
        "comments": [
            "Finde ich spannend",
            "ich bin auch mit der NASA zum Mars geflogen",
            "O,k,, nicht physisch, aber auf dem Mars liegt nun ein USB-Stick mit meinen",
        ],
        "license": "",
        "region": "DE",
    },
    "https://t3n.de/news/apple-eigener-iphone-akku-1587177/": {
        "file": "t3n.de-Laufzeit.html",
        "author": "Andreas Floemer",
        "title": "Apple arbeitet angeblich an eigenen iPhone-Akkus für mehr Laufzeit",
        "date": "2023-11-06",
        "description": "Apple arbeitet einem Bericht aus Südkorea zufolge an eigenen Akkus, die zunächst in iPhones verbaut werden sollen. Dank einer neuen Zellchemie soll der Energiespeicher länger halten und schneller laden. ",
        "categories": ["News", "Hardware & Gadgets"],
        "tags": ["Apple", "iPhone"],
        "with": [
            "Laut ET-News ziele Apple darauf ab",
            "innovative Batterien zu entwickeln, die bisher weltweit noch nicht kommerzialisiert wurden",
            "Die Nachfrage nach Hochleistungsbatterien ist mit der Erweiterung",
        ],
        "without": [
            "Spreading knowledge & future optimism.",
            "Verpasse keine News zu Hardware & Gadgets",
            "Foldables von Apple? Der Fokus soll derzeit noch woanders liegen",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://tageswoche.ch/gesellschaft/wir-sind-dann-mal-weg-und-dieser-titel-muss-auch-weg-oder/index.html": {
        "file": "Tageswoche.ch-weg.html",
        "author": "Ronja Beck",
        "title": "Wir sind dann mal weg (und dieser Titel muss auch weg! Oder?)",
        "date": "2018-11-16",
        "description": "Wie ist das, wenn das Ende kurz bevorsteht? Ein Einblick in die letzten Tage der TagesWoche-Redaktion. ",
        "categories": [],
        "tags": ["Gesellschaft", "Medien", "TagesWoche"],
        "with": [
            "Sportredaktor Samuel ist es nach etwas Dramatik",
            "singt er halblaut, aber mit Leidenschaft hinter seinem Bildschirm",
            "seufzt Catherine eine Pult-Insel entfernt",
        ],
        "without": [
            "Nächster Artikel",
            "Liebe Verkehrspolitiker, traut euch bitte endlich was!",
            "Parkplatzgebühren, Fahrverbote, Velowege",
        ],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://tarnkappe.info/artikel/empfehlungen/happy-halloween-hide-me-senkt-kurzfristig-die-preise-282156.html": {
        "file": "tarnkappe.info-Black.html",
        "author": "Lars Sobiraj",
        "title": "Black Friday Deal jetzt schon sichern: hide.me senkt kurzfristig die Preise!",
        "date": "2023-11-01",
        "description": "Der verschwiegene VPN-Anbieter hide.me senkt anlässlich von Black Friday die Abo-Preise. Das Angebot gilt aber nur für exakt einen Monat. ",
        "categories": ["Artikel", "Empfehlungen"],
        "tags": [],
        "with": [
            "Das zweijährige Abo kostet ab den 1. November pro Monat nur 2,22 Euro",
            "Insgesamt werden für 27 Monate folglich knapp 60 Euro fällig",
            "Zumindest was die Verschleierung der eigenen IP-Adresse betrifft",
        ],
        "without": [
            "Kein Bock auf Werbung?",
            "Wir auch nicht. Dennoch kannst Du Dir",
            "sicher vorstellen, dass hinter dieser Webseite viel Zeit und Arbeit steckt.",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://tegernseerstimme.de/klimavorreiter-oberland-energie-effizienz-netzwerktreffen-in-egling/": {
        "file": "tegernseerstimme.de-Klimavorreiter.html",
        "author": "Birgit Posselt",
        "title": "Klimavorreiter Oberland?",
        "date": "2018-11-16",
        "description": "Welchen Weg schlägt die kommunale Wärmeplanung ein? Was hat das mit kalter Nahwärme zu tun? ",
        "categories": ["Aktuelles", "Allgemein", "Energie"],
        "tags": [],
        "with": [
            "Die Vertreter der Gemeinden und Fachleute diskutierten",
            "auch über die sogenannte energieeffiziente",
            "welche in Neubaugebieten gut genutzt werden kann",
        ],
        "without": [
            "Autounfall in St. QuirinAutounfall in St. Quirin",
            "MVV-Beitritt bringt Touristen auf die Schienen",
            "Diskutieren Sie mit uns",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://teslamag.de/news/musk-firma-xai-modell-nutzung-tesla-computer-moeglich-62317": {
        "file": "teslamag.de-Musk.html",
        "author": "",
        "title": "Musk-Firma xAI veröffentlicht für Tests erstes Modell, Nutzung auf Tesla-Computern möglich",
        "date": "2023-11-06",
        "description": "In diesem Frühjahr gehörte Tesla-CEO Elon Musk zu mehreren hundert Fachleuten, die wegen Gefahren dieser Technologie ein Moratorium bei der Entwicklung von leistungsfähigen KI-Sprachmodellen wie GPT forderten, aber viel geholfen hat das nicht. ",
        "categories": [],
        "tags": ["Elon Musk", "KI", "Tesla", "Twitter"],
        "with": [
            "Grok sei als künstliche Intelligenz dem Buch",
            "Per Anhalter durch die Galaxis",
            "also dazu gedacht, fast jegliche Fragen zu beantworten und sogar selbst Fragen vorzuschlagen",
        ],
        "without": [
            "NEUESTE BEITRÄGE",
            "Widersprüchliche Daten: Tesla-Fahrer haben",
            "laut Auswertung in USA die meisten Unfälle",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://uebermedien.de/89676/gute-tabus-schlechte-tabus-die-vertauschten-rollen-in-der-debatte-ueber-israel/": {
        "file": "uebermedien.de-Israel.html",
        "author": "Stefan Niggemeier",
        "title": "Gute Tabus, schlechte Tabus: Die vertauschten Rollen in der Debatte über Israel",
        "date": "2023-11-03",
        "description": " ",
        "categories": [],
        "tags": ["Antisemitismus", "Gaza", "Israel", "Meinungsfreiheit", "Nahost"],
        "with": [
            "Was folgt aus diesen Beobachtungen?",
            "Natürlich könnte man sich wünschen",
            "dass es Verständnis für das Gegenüber weckt",
        ],
        "without": [
            "Aus Solidarität mit Israel verzichtet „Bild“ darauf",
            "über palästinensische Opfer in Gaza zu berichten",
            "Die Magie der Zuschauer-Call-ins",
        ],
        "comments": [
            "Ich finde, Sie vermengen hier zwei Dinge",
            "die nicht zusammengehören. Das eine ist inhaltlich",
            "dass ich die antisemitische Hetze von FFF-international verteidigen wollte",
        ],
        "license": "",
        "region": "DE",
    },
    "https://uncutnews.ch/digitale-id-diktat-un-und-gates-stiftung-setzen-auf-totale-kontrolle/": {
        "file": "uncutnews.ch-ID-Diktat.html",
        "author": "uncut-news.ch",
        "title": "Digitale ID-Diktat: UN und Gates-Stiftung setzen auf totale Kontrolle!",
        "date": "2023-11-06",
        "description": "Das UN-Programm fördert digitale öffentliche Infrastruktur, während die EU und die Gates-Stiftung bis 2030 für digitale IDs werben ",
        "categories": [],
        "tags": ["Geheimdienste", "NSA", "Überwachung", "BigData"],
        "with": [
            "Im besten Fall sollen DPIs die Entwicklung auf vielfältige Weise fördern",
            "Kritiker, die jedoch hinter die Fassade aus Plattitüden",
            "entlarven den Begriff und die dahinterstehende Politik als Vorwand",
        ],
        "without": [
            "UNMANIPULIERTE & FREIE MEDIEN",
            "Wir werden nicht von Vereinen, Verbänden, Parteien oder sonstigen Lobbygruppen unterstützt.",
            "Wir schalten keine Werbung, wir belästigen auch nicht mit lästigen Pop-ups oder nötigen unsere Besucher",
        ],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://unzensuriert.at/209302-von-der-leyen-will-kriegsland-ukraine-in-eu-holen-oesterreich-zahlt-die-zeche/": {
        "file": "unzensuriert.at-Zeche.html",
        "author": "",
        "title": "Von der Leyen will Kriegsland Ukraine in EU holen – Österreich zahlt die Zeche",
        "date": "2023-11-06",
        "description": "EU-Kommissionspräsidentin Ursula von der Leyen will die Ukraine lieber heute als morgen in die EU holen und Nettozahler wie Österreich die Rechnungen von Präsident Wolodymyr Selenskyj bezahlen lassen. ",
        "categories": [],
        "tags": [],
        "with": [
            "Die Aussage von EU-Kommissionspräsidentin Ursula von der Leyen",
            "dass die Ukraine den Weg für Beitrittsgespräche fast geschafft hätte",
            "lässt bei FPÖ-Europasprecherin Petra Steger die Alarmglocken läuten.",
        ],
        "without": [
            "Alle Politik-Artikel lesen",
            "Bidens Bruder teilt trotz Freundin...",
            "Wenn Sie dieses Youtube-Video sehen möchten, müssen Sie die externen YouTube-cookies akzeptieren.",
        ],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://utopia.de/news/was-haben-bhs-mit-eisbergen-zu-tun-kim-kardashian-polarisiert-mit-werbung-nippel/": {
        "file": "utopia.de-Werbung.html",
        "author": "Katharina Schmidt",
        "title": "Polarisierende BH-Werbung: Kim Kardashian, Eisberge und falsche Nippel",
        "date": "2023-11-06",
        "description": "Auf Instagram zeigt Milliardärin Kim Kardashian sich besorgt um die Klimakrise – um mit viel Ironie Werbung für ein neues Produkt zu machen. Nicht alle finden das lustig. ",
        "categories": ["Mode"],
        "tags": ["Greenwashing", "Kleidung", "Konsum", "News", "Promis"],
        "with": [
            "Kim Kardashian hat 2019 die inklusive Shapewear-Marke",
            "mitgegründet und macht nun Werbung für ein neues Produkt",
            "Auf Instagram erschien vor kurzem ein Spot",
        ],
        "without": ["Aktuelle News", "Beliebte Beiträge", "Beliebte Bestenlisten"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://vipflash.de/contents/176739-ehezoff-der-pochers-eskaliert-jetzt-schiesst-olli-gegen-amira-und-ihren-neuen?locale=en": {
        "file": "vipflash.de-Ehezoff.html",
        "author": "Olga",
        "title": "Ehezoff der Pochers eskaliert - Jetzt schießt Olli gegen Amira und ihren Neuen",
        "date": "2023-11-06",
        "description": "Die Situation im Pocher-Ehedrama ist aktuell ziemlich angespannt. ",
        "categories": ["Stars"],
        "tags": [],
        "with": [
            "Oliver Pocher sieht die Dinge jedoch anders und äußert sich recht deutlich",
            "Exclusiv Weekend Spezial: Die Stars im NFL-Fieber",
            "sagt Pocher in einem Live-Interview mit Moderatorin Frauke Ludowig",
        ],
        "without": ["Blaulicht", "Datenschutz", "Kontakt"],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://volksblatt.at/chronik/oesterreich/oesterreich-tranken-pro-kopf-111-liter-alkohol-im-jahr-822151/": {
        "file": "volksblatt.at-Alkoholkonsum.html",
        "author": "Jens Büttner",
        "title": "Österreich erneut im Spitzenfeld bei Alkoholkonsum",
        "date": "2023-11-07",
        "description": "Die Österreicherinnen und Österreicher sind ein trinkfreudiges Volk: Das zeigt der aktuelle umfassende OECD-Gesundheitsbericht „Health at a Glance“. ",
        "categories": [],
        "tags": [],
        "with": [
            "Spitzenreiter Lettland führt das Ranking dabei mit 12,2 Litern pro Kopf an",
            "Der OECD-Schnitt liegt dagegen bei 8,6 Litern pro Kopf",
            "Der OECD-Bericht „Health at a Glance“ erfasst regelmäßig zahlreiche Daten zum Zustand",
        ],
        "without": [
            "DAS KÖNNTE SIE AUCH INTERESSIEREN",
            "OMV verliert Beteiligung an russischem Gasfeld",
            "Signa verkauft Chrysler Building und Medienbeteiligungen",
        ],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.volksstimme.ch/gute-loehne-alleine-reichen-nicht": {
        "file": "Volksstimme.ch-loehne.html",
        "author": "Baselbiet, Ormalingen",
        "title": "Gute Löhne alleine reichen nicht",
        "date": "2023-11-07",
        "description": "So bleibt man als Arbeitgeber attraktiv ",
        "categories": [],
        "tags": [],
        "with": [
            "Das Zentrum Ergolz lud zur Gesprächsrunde ein",
            "Die Teilnehmenden sprachen darüber",
            "wie Arbeitgeber in Zeiten des Fachkräftemangels genügend Personal finden",
        ],
        "without": ["Möchten Sie weiterlesen?", "Ja. Ich bin Abonnent.", "Ja. Ich benötige ein Abo."],
        "comments": [],
        "license": "",
        "region": "CH",
    },
    "https://world.kbs.co.kr/service/news_view.htm?lang=e&Seq_Code=181595": {
        "file": "world.kbs.co.kr-Temperatures.html",
        "author": "",
        "title": "Colder Temperatures Forecast for Wed. after Cold Wave Alert Tues.",
        "date": "2023-11-07",
        "description": "Anchor: After heavy downpours on Monday, Tuesday morning was met with strong, cold winds that brought early winter temperatures. ",
        "categories": ["Domestic"],
        "tags": [],
        "with": [
            "Although the first cold wave alerts of the season were issued in anticipation of frigid morning lows on Tuesday",
            "Wednesday is forecast to be even colder.",
            "People out on the streets were seen wearing layers throughout the day as Tuesday’s temperatures",
        ],
        "without": ["Most Viewed News", "Headline News", "Most Viewed Content"],
        "comments": [],
        "license": "",
        "region": "KR",
    },
    "https://www.1000things.at/blog/wellnessoasen-thermen-vulkanland/": {
        "file": "1000things.at-Wellnessoasen.html",
        "author": "Evgenia Karp",
        "title": "6 Wellnessoasen für eure Auszeit im Thermen- & Vulkanland",
        "date": "2023-11-06",
        "description": "Was hilft am besten gegen die niedrigen Temperaturen? Richtig: dampfendes Thermalwasser, kristallklare Luft und richtig gutes Essen. All das bekommt ihr im Thermen- & Vulkanland in der Steiermark. Wo genau? Das erfahrt ihr hier. ",
        "categories": ["ERHOLUNG", "ANZEIGE"],
        "tags": ["HOTEL", "MASSAGE", "URLAUB", "WELLNESS", "WINTER", "WINTERURLAUB", "STEIERMARK", "SÜDOSTSTEIERMARK"],
        "with": [
            "Wusstest ihr, dass die stressabbauende Wirkung von Thermalwasser",
            "im Thermen- & Vulkanland wissenschaftlich belegt ist?",
            "Kein Wunder also, dass schon ein paar Tage Urlaub im Winter hier die reinste Energieladung sind.",
        ],
        "without": [
            "Ein Roadtrip entlang der Route 66 im Thermen- & Vulkanland",
            "Herbstlicher Wochenend-Ausflug in die Südoststeiermark",
            "Mehr von 1000things",
        ],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www1.wdr.de/nachrichten/correctiv-recherche-deutsche-waffen-fuer-russland-100.html": {
        "file": "www1.wdr.de-Correctiv-Recherche.html",
        "author": "",
        "title": "Correctiv-Recherche: Deutsche Waffen für Russland",
        "date": "2023-11-07",
        "description": 'Seit Beginn des russischen Angriffskriegs auf die Ukraine gelangen weiter Waffen und Munition westlicher Hersteller nach Russland – auch aus Deutschland. Das ist das Ergebnis einer Recherche von "Correctiv". ',
        "categories": ["Wirtschaft", "Nachrichten", "Ukraine"],
        "tags": [],
        "with": [
            "Die Hersteller dürfen sie demnach ins Ausland verkaufen",
            "weil sie offiziell als Jagd- oder Sportwaffen gelten",
            "und deshalb nicht unter das Kriegswaffen-Kontrollgesetz fallen",
        ],
        "without": [
            "WDR aktuell Whatsapp-Kanal abonnieren - so geht's",
            "App-Symbol: WDR aktuellDie App WDR aktuell begleitet Sie durch den Tag",
            "Wie wir mit Gendern umgehen",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://www.5min.at/5lokales/villachs-meister-proper-expandiert-nach-wien/": {
        "file": "5min.at-Villachs.html",
        "author": "",
        "title": "Villachs „Meister Proper“ expandiert nach Wien",
        "date": "2023-11-05",
        "description": "Saubere Sache: Filana - euer Top-Ansprechpartner für Reinigungs- und Hausmeisterdienste - wächst nun über die Grenzen Kärntens hinaus und expandiert bis in die Bundeshauptstadt. ",
        "categories": [],
        "tags": [],
        "with": [
            "Chef Boris Dujakovic gründete Filana",
            "vor über vier Jahren als Hausmeisterservice",
            "In den letzten 2 Jahren hat er sich aber vor allem auf Grundreinigung",
        ],
        "without": ["Mehr Interessantes", "Wetter aktuell", "Meistgeklickt"],
        "comments": [],
        "license": "",
        "region": "AT",
    },
    "https://www.90min.de/posts/bundesliga-tabelle-2023-24-ohne-fehlentscheidungen-01hdgzyyg1b1": {
        "file": "90min.de-Bundesliga-Tabelle.html",
        "author": "Jan Kupitz",
        "title": "So sähe die Bundesliga-Tabelle 23/24 nach dem 10. Spieltag ohne Fehlentscheidungen aus",
        "date": "2023-10-24",
        "description": "Die ersten zehn Spieltage der Bundesliga sind gespielt. Wie sähe die Tabelle ohne Fehlentscheidungen aus? ",
        "categories": [],
        "tags": ["Bundesliga", "Eintracht Frankfurt", "SC Freiburg", "VfL Wolfsburg"],
        "with": [
            "Mittlerweile vergeht kein Wochenende mehr",
            "an dem nicht über den Schiedsrichter und/oder den VAR diskutiert wird",
            "Auch am 10. Spieltag der Bundesliga gab es gleich mehrere strittige Entscheidungen",
        ],
        "without": [
            "So sähe die Tabelle der Bundesliga",
            "2023/24 nach dem 14. Spieltag ohne Fehlentscheidungen aus",
            "Das Fußball-Portal wahretabelle.de nimmt strittige",
        ],
        "comments": [],
        "license": "",
        "region": "DE",
    },
    "https://theintercept.com/2023/11/08/gaza-hospitals-babies-doctors-patients/": {
        "file": "theintercept.com-Gaza.html",
        "author": "Ibtisam Mahdi, Ruwaida Kamal Amer",
        "title": "WHAT IT’S LIKE TO GIVE BIRTH IN GAZA",
        "date": "2023-11-08",
        "description": "With most hospitals closed, Gaza’s doctors struggle to care for premature babies — often without power. ",
        "categories": [],
        "tags": [],
        "with": ["The shortages led to what in the West", "would be unthinkable decisions", "choosing between patients who"],
        "without": [
            "U.S. Weapons Transfers to Israel Shrouded in Secrecy — but Not Ukraine",
            "Inside the Biden White House, Doubts About Gaza War Are Beginning to Creep In",
            "GOP Representative Denies Existence",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://abc13.com/aishas-salon-and-spa-houston-lewd-act-man-pleasures-himself-on-camera-harris-county-sheriffs-office/14030671/": {
        "file": "abc13.com-Copperfield.html",
        "author": "Alex Bozarjian",
        "title": "Aisha's Salon and Spa chain bans men from entering any of its 25 locations after man's lewd act",
        "date": "2023-11-09",
        "description": "HOUSTON, Texas (KTRK) -- A Houston-area beauty business is taking drastic measures after the owner said a man entered one of their salons on Tuesday and inappropriately touched himself. ",
        "categories": ["Lewdness"],
        "tags": [
            "HARRIS COUNTY",
            "LEWDNESS",
            "CAUGHT ON TAPE",
            "CAUGHT ON VIDEO",
            "SEX CRIME",
            "HARRIS COUNTY SHERIFFS OFFICE",
            "CAUGHT ON CAMERA",
            "SEX CRIMES",
        ],
        "with": [
            "The Harris County Sheriff's Office is now",
            "investigating the incident at the salon chain's location in the Copperfield area.",
            "According to the owner, only female stylists are employed there",
        ],
        "without": [
            "Man admits to taking violating pics of women for months, police say",
            "Man was pleasuring himself inside HCC library, woman says",
            "Suspects robbed shoe store before chase ended in fiery crash, HPD says",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.kxan.com/news/texas/voters-pass-increase-for-retired-public-education-workers-but-future-shortfalls-likely-to-emerge/": {
        "file": "kxan.com-Voters.html",
        "author": "Cora Neas",
        "title": "Voters pass increase for retired public education workers, but future shortfalls likely to emerge",
        "date": "2023-11-08",
        "description": "AUSTIN (KXAN) — Texas voters approved an amendment to the state constitution on Tuesday that will grant billions of dollars to the Teacher Retirement System for a cost-of-living adjustment. ",
        "categories": [],
        "tags": [],
        "with": ["So many of our retirees", "been living in this high-inflation environment", "are living on credit cards"],
        "without": ["AUSTIN WEATHER", "TRENDING STORIES", "APD addresses Kaitlin Armstrong’s online searches"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://gothamist.com/news/rezoning-plan-plagues-bronx-city-councilmembers-re-election-bid": {
        "file": "gothamist.com-plagues.html",
        "author": "David Brand and Ramsey Khalifeh",
        "title": "Rezoning plan plagued Bronx re-election bid for city councilmember",
        "date": "2023-11-08",
        "description": "A controversial rezoning proved to be a central issue in a heated City Council race in the East Bronx, where Democratic incumbent Marjorie Velázquez trailed her Republican challenger Kristy Marmorato by more than 700 votes on Wednesday. ",
        "categories": ["NEWS"],
        "tags": [],
        "with": [
            "pitch to build a casino at the foot of the Whitestone Bridge",
            "buying the contract to operate Trump Golf Links Ferry Point",
            "earlier this year is also sparking opposition.",
        ],
        "without": [
            "We rely on your support to make local news available to all",
            "NYC election results: A surprisingly tight race in the Bronx as incumbents lead elsewhere",
            "Early Addition: Big year for sleeping with tape over your mouth",
        ],
        "comments": [
            "see why the rezoning was so controversial",
            "This building is no more bulky with a larger FAR",
            "than others nearby like the office parks off of the Hutchinson River",
        ],
        "license": "",
        "region": "",
    },
    "https://www.laweekly.com/meet-cultural-cultivation-artist-alexandria-douziech/": {
        "file": "laweekly.com-Cultivation.html",
        "author": "SHANA NYS DAMBROT",
        "title": "MEET CULTURAL CULTIVATION ARTIST ALEXANDRIA DOUZIECH",
        "date": "2023-11-06",
        "description": "Cultivation is more than a metaphor for creativity in the plant-forward work of artist and educator Alexandria Douziech. ",
        "categories": [],
        "tags": [],
        "with": [
            "I try to position plants as storytellers",
            "living archives that reflect the legacy of colonialism",
            "as well as the power of human resilience",
        ],
        "without": ["SUBSCRIBE TO OUR NEWSLETTER", "LATEST ARTICLES", "SEARCH LA WEEKLY"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://observer.com/2023/11/bernard-arnault-lvmh-louvre-chardin/": {
        "file": "observer.com-LVMH.html",
        "author": "Alexandra Tremayne-Pengelly",
        "title": "Bernard Arnault’s LVMH Gives the Louvre a $16M Boost to Acquire a Chardin Masterpiece",
        "date": "2023-11-08",
        "description": "The still life is the seventh French national treasure LVMH has helped purchase. ",
        "categories": ["ARTS"],
        "tags": [],
        "with": [
            "For over a year, the Louvre has fought to acquire",
            "an 18th-century painting by Jean Siméon Chardin for its national collection",
            "Now, the museum is receiving help in the form of 15 million euros",
        ],
        "without": ["Advertising Guidelines", "Editorial Ethics", "Do not sell my data"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.bostonherald.com/2023/11/08/brothel-catering-to-politicians-doctors-lawyers-busted-in-boston/": {
        "file": "bostonherald.com-Brothel-catering.html",
        "author": "GRACE ZOKOVITCH",
        "title": "Brothel catering to politicians, doctors, lawyers busted in Boston",
        "date": "2023-11-08",
        "description": "Johns paid up to $600 an hour for sex services ",
        "categories": [],
        "tags": [],
        "with": [
            "sex ring catering to wealthy doctors",
            "lawyers, politicians, and military officers who paid up to $600 an hour",
            "prostitutes was busted in Boston, the feds announced",
        ],
        "without": ["MOST POPULAR", "TRENDING NATIONALLY", "MORE IN LOCAL NEWS"],
        "comments": [],
        "license": "",
        "region": "US",
    },
    "https://abc7news.com/camp-margaritaville-resort-napa-county-lake-berryessa-hotel-jimmy-buffett/14031465/": {
        "file": "abc7news.com-Napa.html",
        "author": "J.R. Stone",
        "title": "Napa Co. enters exclusive agreement that could bring Margaritaville Resort to Lake Berryessa",
        "date": "2023-11-09",
        "description": "NAPA COUNTY, Calif. (KGO) -- A plan to bring a Margaritaville Resort, made popular by the late Jimmy Buffett, to the Bay Area is one step closer. ",
        "categories": ["BUSINESS"],
        "tags": ["BUSINESS", "NAPA COUNTY", "HOTEL", "ECONOMY", "DEVELOPMENT"],
        "with": [
            "so I think anyone that wants to do business in this area",
            "as an incredible opportunity to make sure",
            "it is done fair responsibly",
        ],
        "without": ["Top Stories", "LIVE STREAMS", "Building A Better Bay Area"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.phillyvoice.com/sixers-76ers-score-record-news-analysis-celtics-joel-embiid-tyrese-maxey-jayson-tatum/": {
        "file": "phillyvoice.com-Sixers.html",
        "author": "ADAM AARONSON",
        "title": "Sixers game notes: Joel Embiid leads Sixers to statement victory over Celtics",
        "date": "2023-11-08",
        "description": "The Sixers captured their biggest win of the year Wednesday night. ",
        "categories": [],
        "tags": [],
        "with": [
            "It was an underwhelming first quarter on both sides",
            "as the Sixers and Celtics each struggled mightily to knock down shots",
            "The Sixers went 0-for-9 from three-point range in the period",
        ],
        "without": ["Certain personality traits", "like being an extrovert", "may lower risk for dementia"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.villagevoice.com/party-like-its-1923-will-donald-trump-write-his-own-mein-kampf-in-jail/": {
        "file": "villagevoice.com-Party.html",
        "author": "R.C. BAKER",
        "title": "Party Like It’s 1923: Will Donald Trump Write His Own ‘Mein Kampf’ in Jail?",
        "date": "2023-11-05",
        "description": "After his failed Beer Hall Putsch, in Munich 100 years ago, Adolf Hitler dictated his racist bestseller in the slammer. ",
        "categories": ["POLITICS"],
        "tags": [],
        "with": [
            "Trump has been known to contradict himself",
            "in depositions, and when being grilled by the New York Attorney",
            "office on business fraud charges earlier this year",
        ],
        "without": [
            "The advertising disclaimer below does not apply to this article",
            "nor any originating from the Village Voice editorial department",
            "Advertising disclosure: We may receive compensation",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://wsvn.com/news/local/miami-dade/15-year-old-driver-killed-14-year-old-passenger-critical-in-sw-miami-dade-crash/": {
        "file": "wsvn.com-crash.html",
        "author": "JESSICA HOLLY, GAIL LEVY, 7 NEWS WSVN",
        "title": "15-year-old driver killed, 14-year-old passenger critical in SW Miami-Dade crash",
        "date": "2023-11-08",
        "description": "SOUTHWEST MIAMI-DADE, FLA. (WSVN) - An overnight crash in Southwest Miami-Dade resulted in the death of a 15-year-old boy who was behind the wheel and critical injuries to a 14-year-old girl in the passenger seat, officials said. ",
        "categories": [],
        "tags": [],
        "with": [
            "Investigators said a patrol unit turned on its lights",
            "with plans to attempt a traffic stop in the area of Southwest 118th Avenue.",
            "the driver lost control of the vehicle",
        ],
        "without": ["Join our Newsletter", "for the latest news right to your inbox", "CHILDRENS PROGRAMMING"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.twincities.com/2023/11/08/st-louis-park-elects-a-new-mayor-apparently-the-first-somali-american-to-lead-a-u-s-city/": {
        "file": "twincities.com-mayor.html",
        "author": "STAFF AND NEWS SERVICE REPORTS",
        "title": "St. Louis Park elects a new mayor, apparently the first Somali American to lead a U.S. city",
        "date": "2023-11-08",
        "description": "Nadia Mohamed, 27, won with 58% of the vote in Tuesday’s municipal election, defeating Dale Anderson, who got 41% of the vote. She has served on the City Council since she was elected at age 23 in 2019. ",
        "categories": ["NEWS", "POLITICS"],
        "tags": [],
        "with": [
            " What I had learned the first time is that this is just a milestone.",
            "It is not the destination",
            "Mohamed told the Sahan Journal.",
        ],
        "without": ["MOST POPULAR", "RELATED ARTICLES", "TRENDING NATIONALLY"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.metrotimes.com/food-drink/detroits-mezcal-restaurant-goes-beyond-familiar-mexican-fare-34565910": {
        "file": "metrotimes.com-Mezcal.html",
        "author": "Jane Slaughter",
        "title": "Detroit’s Mezcal restaurant goes beyond familiar Mexican fare",
        "date": "2023-11-09",
        "description": "The second location opened in Midtown following the first in Ferndale ",
        "categories": ["RESTAURANT REVIEWS"],
        "tags": [
            "Mexican restaurants in Detroit",
            "Mexican restaurants in Ferndale",
            "mezcal bars in metro Detroit",
            "Mezcal Mexican Bar & Kitchen",
            "Mezcal Mexican Bar & Kitchen",
        ],
        "with": [
            "The Mariachi Mexico 2020 quartet",
            "plays every other Sunday and they are a treat",
            "really good voices, and they take requests.",
        ],
        "without": [
            "Join Detroit Metro Times Newsletters",
            "Scroll to read more Restaurant reviews articles",
            "The Red Sea in Dearborn is a great catch",
        ],
        "comments": [],
        "license": "",
        "region": "US",
    },
    "https://citylimits.org/2023/11/08/video-voting-on-nychas-future/": {
        "file": "citylimits.org-Nycha.html",
        "author": "Tatyana Turner",
        "title": "VIDEO: Voting on NYCHA’s Future",
        "date": "2023-11-08",
        "description": "This City Limits video delves into the complexities of a vote that will impact Nostrand Houses tenants in the near term, and explores the choices thousands of additional public housing tenants will have to make in the coming years. ",
        "categories": [],
        "tags": [],
        "with": [
            "Wednesday is a monumental day for the New York City",
            "Housing Authority and residents at the Nostrand Houses in Sheepshead Bay, Brooklyn",
            "For the first time, tenants will begin to vote",
        ],
        "without": ["LATEST ARTICLES", "more stories", "City Limits uses investigative journalism through the prism"],
        "comments": [
            "My comment is this all the lower class",
            "as we call them middle class apartments in NYCHA buildings are",
            "going to the upper and upper class people if you",
        ],
        "license": "",
        "region": "",
    },
    "https://www.publishedreporter.com/2023/11/08/scientists-confirm-2023-as-hottest-year-ever-in-the-making/": {
        "file": "publishedreporter.com-Hottest.html",
        "author": "Alejandro Villamor",
        "title": "Scientists Confirm 2023 As Hottest Year Ever In The Making",
        "date": "2023-11-08",
        "description": "According to scientists, 2023 is slated to be the hottest year on record as the Earth continues its relentless climb in temperature. ",
        "categories": ["Health", "Science", "U.S. News"],
        "tags": ["Climate Change", "El Niño", "Global warming", "Newsbreak", "Scientist", "US News"],
        "with": [
            "From the Copernicus Climate Change Service",
            "Samantha Burgess confirms with high certainty",
            "that the global temperature has surpassed pre-industrial averages",
        ],
        "without": [
            "Advertising Disclosure",
            "This site participates in the Amazon Associate program",
            "and earns revenue from qualifying purchases",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.miamitodaynews.com/2023/11/07/transit-tax-trust-rejects-countys-south-dade-transitway-data/": {
        "file": "miamitodaynews.com-Transitway.html",
        "author": "Miami Today",
        "title": "Transit tax trust rejects county’s South Dade Transitway data",
        "date": "2023-11-07",
        "description": " ",
        "categories": ["Transportation "],
        "tags": [],
        "with": [
            "Also delaying the response, Mr. Cueto said",
            "was that the county made the video presentation and then briefed",
            "accurate and is aligned with those funding partners",
        ],
        "without": [
            "South Dade rapid transit will be rapid in only one direction",
            "Send South Dade Transitway back to square one, trust urged",
            "County vowed a transit Rolls Royce; we’re getting a Ford",
        ],
        "comments": [
            "Enough with the buses",
            "start laying down rails and stringing electric",
            "catenary for fixed dedicated right of way streetcars, trolleys and trams",
        ],
        "license": "",
        "region": "US",
    },
    "https://www.heartlandnewsfeed.com/2023/10/27/christian-county-police-blotters/": {
        "file": "heartlandnewsfeed.com-Christian.html",
        "author": "HLNF Staff Report",
        "title": "Christian County police blotters",
        "date": "2023-10-27",
        "description": "TAYLORVILLE — The following are arrest and accident reports as recorded by the Taylorville Police Department and the Christian County Sheriff’s Department. The blotter is as follows: ",
        "categories": ["Illinois", "Local"],
        "tags": [],
        "with": [
            "A vehicle driven by Kimberly Carrell, no age or address reported",
            "was southbound on 1600E Road near 400N Road when a deer entered the roadway",
            "The vehicle was unable to avoid striking the deer",
        ],
        "without": [
            "a subsidiary partnership by Heartland Internet Media Networks",
            "Heartland Media Group of Central Illinois",
            "published by Heartland Newsfeed staff is covered by the BipCot NoGov license",
        ],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://roughdraftatlanta.com/2023/11/08/brookhaven-village-closed-due-to-gas-leak/": {
        "file": "reporternewspapers.net-Brookhaven.html",
        "author": "Logan C. Ritchie",
        "title": "UPDATE: Brookhaven Village closed a second time for gas leak",
        "date": "2023-11-08",
        "description": "Dresden Drive is experiencing a gas leak for the second time in 24 hours. There are no evacuations as of 2:30 p.m. on Thursday, Nov. 9. ",
        "categories": ["BROOKHAVEN", "DEKALB", "NEWS"],
        "tags": ["Brookhaven", "gas leak"],
        "with": [
            "Brookhaven Police Department is reporting",
            "a construction company struck another gas line in the area of Dresden Drive",
            "near Parkside Drive. Road closure signs have been placed to shut the roadway down.",
        ],
        "without": ["TRENDING ON ROUGH DRAFT", "RECENT STORIES", "PROUDLY POWERED BY NEWSPACK BY AUTOMATTIC"],
        "comments": [],
        "license": "",
        "region": "",
    },
    "https://www.springer.com/de/acht-produkte-mit-sustainable-award-in-finance-praemiert/19837156": {
        "file": "springer.com-produkte.html",
        "author": "",
        "title": "Acht Produkte mit Sustainable Award in Finance prämiert",
        "date": "2021-11-11",
        "with": [
            "Corona-Verordnung des Landes Hessen statt.",
            "AG sowie die Berlin Hyp",
            "Wiesbaden werden Fachzeitschriften,",
        ],  # 3 segments
        "without": ["Kontakt", "Logo des Sustainable Award in Finance", "Rechtliches"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.kulturkaufhaus.de/de/kultur-magazin/blogDetail/DIY-Farbbuch-artcBlog?bpmctrl=bpmrownr.1%7Cforeign.323438-1-0-267787": {
        "file": "kulturkaufhaus.de-basteln.html",
        "author": "",
        "title": "Kreatives Basteln mit Kids",
        "date": "2022-02-09",
        "with": [
            "wie man ein Büchlein aus einem A3",
            "1 Wasserglas mit Wasser",
            "wenn ihr unser DIY nachbastelt",
        ],  # 3 segments
        "without": ["Kategorien", "Du möchtest in Ruhe nachbasteln?", "Zuletzt besuchte Seiten"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.juraforum.de/recht-gesetz/ohne-ernsthafte-bewerbungsbemuehungen-kein-wohngeld-722430": {
        "file": "juraforum.de-Wohngeld.html",
        "author": "Sebastian Einbock",
        "title": "Ohne ernsthafte Bewerbungsbemühungen kein Wohngeld",
        "date": "2022-02-18",
        "with": [
            "Verwaltungsgericht hielt die ablehnenden Wohngeldentscheidung",
            "Standort abgelehnt, ohne jedoch",
            "Er habe aber keinerlei ernsthaften",
        ],  # 3 segments
        "without": ["KOMMENTAR SCHREIBEN", "Lexware für Unternehmer", "BISHERIGE KOMMENTARE ZUR"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.haufe.de/recht/kanzleimanagement/buss-und-ordnungsgeld-gegen-anwalt-wegen-maskenverweigerung_222_560754.html": {
        "file": "haufe.de-ordnungsgeld.html",
        "author": "",
        "title": "Buß- und Ordnungsgeld gegen Anwalt wegen Maskenverweigerung",
        "date": "2022-02-06",
        "with": [
            "auf Norderney erhielt er wegen",
            "Aufforderungen des Vorsitzenden zum Anlegen",
            "der Corona-Pandemie allgemein für zulässig",
        ],  # 3 segments
        "without": ["Schlagworte zum Thema", "Produktempfehlung", "Verweigert der Anwalt die Maske,"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://www.datev-magazin.de/archiv/sichere-und-digitale-mandantenkommunikation-73813": {
        "file": "datev-magazin.de-kommunikation.html",
        "author": "",
        "title": "Sichere und digitale Mandantenkommunikation",
        "date": "2022-02-15",
        "with": [
            "Vorteilen eines sicheren und durchgängig",
            "Registrierung ist die WebAkte innerhalb",
            "weitere Informationen erhalten",
        ],  # 3 segments
        "without": ["Ähnliche Beiträge", "Meistgelesene Artikel", "Aktuelle Meldungen"],  # 3 segments
        "comments": [],  # 0 or 3 segments
        "license": "",  # if CC-...
        "region": "DE",  # if obvious: DE, CH, AT
    },
    "https://advertising.jodel.com/": {
        "file": "jodel.com.advertising.html",
        "with": [
            "Was sorgt dafür, dass deine Marke auf Jodel sicher ist?",
            "Visuelle und Text-Posts werden in einer 2. Stufe",
            "Lass dich inspirieren und starte deine Erfolgsgeschichte heute",
        ],
        "without": ["Welche Unternehmen bereits Jodel vertrauen", "Termin wählen", "All Rights Reserved."],
    },
    "https://www.geeks3d.com/hacklab/20190110/python-3-simple-http-request-with-the-socket-module/": {
        "file": "geeks3d.com.hacklab.html",
        "with": [
            "This module provides access to the BSD socket interface",
            "Host:www.google.com",
            "http_response_len = len(http_response)",
        ],
        "without": [
            "(Demo) APP Launcher",
            "Demos: geexlab-demopack-python3/socket/01-socket-http-request/main.xml",
            "Your email address will not be published",
        ],
    },
    "https://github.com/golemfactory/yapapi": {
        "file": "github.com.yapapi.html",
        "with": ["Golem application development", "poetry add yapapi", "YAGNA_PAYMENT_DRIVER"],
        "without": ["Watchers", "2022 GitHub", "Failed to load latest commit information"],
    },
    "https://www.telegraph.co.uk/news/uknews/law-and-order/9209302/Plumber-jailed-after-boiler-killed-millionaires-daughter.html": {
        "file": "telegraph.co.uk.plumber.html",
        "with": [
            "The deadly fumes leaked out of the dodgy boiler flue pipe",
            "The quality of work fell below your normal high standards",
            "sobbed in court as Hartley was led to begin his sentence",
        ],
        "without": ["More stories", "2:54pm", "Follow us on"],
    },
    "https://german.stackexchange.com/questions/10376/when-to-use-wurde-versus-war-eg-ich-wurde-ausgeraubt-vs-ich-war-ausgerau": {
        "file": "german.stackexchange.com.ausgeraubt.html",
        "with": ["How does one know", "Ich wurde ausgeraubt", "in that context"],
        "without": ["2 months ago", "20:37", "Sorted by"],
        "comments": ["is simply not correct.", "Unless of what?", "Daher gebe ich hier -1"],
    },
    "https://docs.docker.com/engine/install/": {
        "file": "docs.docker.com.install.html",
        "with": ["Docker Desktop for Windows", "0.0.0-YYYYmmddHHMMSS-abcdefabcdef", "Please DO NOT file a public issue"],
        "without": ["Installation per distro", "On this page:", "Toggle navigation"],
        "tags": ["docker", "installation", "install", "Docker Engine", "Docker Engine", "docker editions", "stable", "edge"],
    },
    "https://www.thebalance.com/coinbase-vs-coinbase-pro-5116733": {
        "file": "thebalance.com.coinbase.html",
        "with": [
            "Coinbase and Coinbase Pro are two of the most popular cryptocurrency exchanges",
            " At a Glance ",
            "1 GBP withdrawal",
        ],
        "without": ["Jacob Wade is a personal finance expert", "Kraken vs. Coinbase", "We recommend the best products"],
    },
}
