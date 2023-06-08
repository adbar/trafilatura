"""
Unit tests for JSON metadata extraction.
"""

import logging
import sys

from lxml import html
from trafilatura.metadata import extract_metadata, extract_meta_json, Document


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_json_extraction():
    ## JSON extraction
    metadata = extract_metadata('''<html><body><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsArticle","description":"The president and his campaign competed again on Monday, with his slash-and-burn remarks swamping news coverage even as his advisers used conventional levers to try to lift his campaign.","image":[{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/2020/10/19/us/politics/19campaign/19campaign-videoSixteenByNineJumbo1600.jpg","height":900,"width":1600,"caption":"In Arizona on Monday, President Trump aired grievances against people including former President Barack Obama and Michelle Obama; Joseph R. Biden Jr. and Hunter Biden; Dr. Anthony S. Fauci; and two female NBC News hosts. "},{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/2020/10/19/us/politics/19campaign/merlin_178764738_11d22ae6-9e7e-4d7a-b28a-20bf52b23e86-superJumbo.jpg","height":1365,"width":2048,"caption":"In Arizona on Monday, President Trump aired grievances against people including former President Barack Obama and Michelle Obama; Joseph R. Biden Jr. and Hunter Biden; Dr. Anthony S. Fauci; and two female NBC News hosts. "},{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/2020/10/19/us/politics/19campaign/19campaign-mediumSquareAt3X.jpg","height":1800,"width":1800,"caption":"In Arizona on Monday, President Trump aired grievances against people including former President Barack Obama and Michelle Obama; Joseph R. Biden Jr. and Hunter Biden; Dr. Anthony S. Fauci; and two female NBC News hosts. "}],"mainEntityOfPage":"https://www.nytimes.com/2020/10/19/us/politics/trump-ads-biden-election.html","url":"https://www.nytimes.com/2020/10/19/us/politics/trump-ads-biden-election.html","inLanguage":"en","author":[{"@context":"http://schema.org","@type":"Person","url":"https://www.nytimes.com/by/maggie-haberman","name":"Maggie Haberman"},{"@context":"http://schema.org","@type":"Person","url":"https://www.nytimes.com/by/shane-goldmacher","name":"Shane Goldmacher"},{"@context":"http://schema.org","@type":"Person","url":"https://www.nytimes.com/by/michael-crowley","name":"Michael Crowley"}],"dateModified":"2020-10-20T01:22:07.000Z","datePublished":"2020-10-19T22:24:02.000Z","headline":"Trump Team Unveils $55 Million Ad Blitz on a Day of Scattershot Attacks","publisher":{"@id":"https://www.nytimes.com/#publisher"},"copyrightHolder":{"@id":"https://www.nytimes.com/#publisher"},"sourceOrganization":{"@id":"https://www.nytimes.com/#publisher"},"copyrightYear":2020,"isAccessibleForFree":false,"hasPart":{"@type":"WebPageElement","isAccessibleForFree":false,"cssSelector":".meteredContent"},"isPartOf":{"@type":["CreativeWork","Product"],"name":"The New York Times","productID":"nytimes.com:basic"}}</script><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsMediaOrganization","name":"The New York Times","logo":{"@context":"http://schema.org","@type":"ImageObject","url":"https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png","height":40,"width":250},"url":"https://www.nytimes.com/","@id":"https://www.nytimes.com/#publisher","diversityPolicy":"https://www.nytco.com/diversity-and-inclusion-at-the-new-york-times/","ethicsPolicy":"https://www.nytco.com/who-we-are/culture/standards-and-ethics/","masthead":"https://www.nytimes.com/interactive/2019/admin/the-new-york-times-masthead.html","foundingDate":"1851-09-18","sameAs":"https://en.wikipedia.org/wiki/The_New_York_Times"}</script><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"BreadcrumbList","itemListElement":[{"@context":"http://schema.org","@type":"ListItem","name":"U.S.","position":1,"item":"https://www.nytimes.com/section/us"},{"@context":"http://schema.org","@type":"ListItem","name":"Politics","position":2,"item":"https://www.nytimes.com/section/politics"}]}</script></body></html>''')
    assert metadata.author == 'Maggie Haberman; Shane Goldmacher; Michael Crowley'
    assert metadata.pagetype == 'newsarticle'

    metadata = extract_metadata('''<html><body><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsArticle","mainEntityOfPage":{"@type":"WebPage","@id":"https://www.perthnow.com.au/news/government-defends-graphic-covid-19-ad-after-backlash-c-3376985"},"dateline":null,"publisher":{"@type":"Organization","name":"PerthNow","url":"https://www.perthnow.com.au","logo":{"@type":"ImageObject","url":"https://www.perthnow.com.au/static/publisher-logos/publisher-logo-60px-high.png","width":575,"height":60}},"keywords":["News","News","Australia","Politics","Federal Politics","News","TAS News"],"articleSection":"News","headline":"Government defends graphic Covid-19 ad after backlash","description":"A graphic COVID-19 ad showing a young woman apparently on the verge of death has prompted a backlash, but the government insists it wasn’t done lightly.","dateCreated":"2021-07-12T00:11:50.000Z","datePublished":"2021-07-12T00:11:50.000Z","dateModified":"2021-07-12T01:25:20.617Z","isAccessibleForFree":"True","articleBody":"The man tasked with co-ordinating Australia&rsquo;s Covid-19 vaccine rollout insists a confronting ad depicting a woman on the verge of death was not run lightly. The 30-second clip, depicting a woman apparently in her 20s or 30s gasping for air on a hospital bed, was filmed last year, but the federal government held off running it as no outbreak was deemed serious enough to warrant it. The government has been forced to defend the ad, reminiscent of the &ldquo;Grim Reaper&rdquo; HIV ads in the 1980s, after it prompted a backlash over claims it was too confronting. A more temperate series of ads, depicting arms on ordinary Australians with the moniker &ldquo;Arm Yourself&rdquo;, began last week, but Covid-19 taskforce commander Lieutenant General John Frewen said the escalating situation in Sydney called for a more explicit response. &ldquo;It is absolutely confronting and we didn&rsquo;t use it lightly. There was serious consideration given to whether it was required and we took expert advice,&rdquo; he told Today on Monday. &ldquo;It is confronting but leaves people in no doubt about the seriousness of getting Covid, and it seeks to have people stay home, get tested and get vaccinated as quickly as they can.&rdquo; NSW on Sunday confirmed another 77 cases, 31 of which had been in the community while infectious, and Premier Gladys Berejiklian warned she would be &ldquo;shocked&rdquo; if the number did not exceed 100 on Monday. General Frewen said the &ldquo;concerning situation&rdquo; had prompted the government to shift an additional 300,000 doses to NSW over the coming fortnight. &ldquo;The Delta variant is proving to be very difficult to contain, so we&rsquo;re working very closely with NSW authorities and standing ready to help them in any way we can,&rdquo; he said. Agriculture Minister David Littleproud said the ad was designed to shock Sydneysiders into action as the situation deteriorated. &ldquo;This is about shooting home that this is a serious situation and can get anybody. The fact we&rsquo;re actually debating this I think says to me that the campaign we&rsquo;ve approved is working,&rdquo; he said. The age of the woman in the ad has sparked controversy, with most younger Australians still ineligible to receive their vaccine. But with 11 of the 52 people in hospital across NSW under 35, Labor frontbencher Tanya Plibersek warned the Delta variant was &ldquo;hitting younger people as well&rdquo;. Labor had long demanded a national Covid-19 advertising campaign, which Ms Plibersek said was delayed as a result of the government&rsquo;s sluggish vaccine rollout. &ldquo;Perhaps the reason it&rsquo;s taken so long is if you encourage people to go and get vaccinated, you&rsquo;ve got to have enough of the vaccine available. We simply haven&rsquo;t; we&rsquo;ve been absolutely behind the eight ball in getting another vaccine for Australians,&rdquo; she told Sunrise. Labor frontbencher Chris Bowen, whose western Sydney electorate was in the grip of the outbreak, said the issue was &ldquo;not vaccine hesitancy so much, it&rsquo;s vaccine scarcity&rdquo;. He accepted there was a role for &ldquo;pointing out the consequences of not getting vaccinated&rdquo; to those that were hesitant about the jab, but said the new campaign lacked the &ldquo;creative spark&rdquo; of the Grim Reaper ads. &ldquo;That was a very tough message, a very stark message, but in a very creative way. I think the government really needs to rethink this advertising campaign from scratch; it&rsquo;s too late, and it&rsquo;s pretty low impact,&rdquo; he told ABC radio. He also dismissed the &ldquo;Arm Yourself&rdquo; campaign as &ldquo;very low energy&rdquo;. &ldquo;I don&rsquo;t think that&rsquo;s going to have any impact,&rdquo; he said.","image":[{"@type":"ImageObject","url":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-16x9-x0y444w1151h647.jpg","width":1151,"height":647},{"@type":"ImageObject","url":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-4x3-x0y336w1151h863.jpg","width":1151,"height":863}],"thumbnailUrl":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-16x9-x0y444w1151h647.jpg","url":"https://www.perthnow.com.au/news/government-defends-graphic-covid-19-ad-after-backlash-c-3376985","author":{"@type":"Organization","name":"NCA NewsWire"},"name":"Government defends graphic Covid-19 ad after backlash"}</script><span itemprop="author name">Jenny Smith</span></span></body></html>''')
    assert metadata.author == 'Jenny Smith'
    assert metadata.pagetype == 'newsarticle'

    metadata = extract_metadata(
        '''<html><body><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org/","@type":"NewsArticle","mainEntityOfPage":{"@type":"WebPage","@id":"https://google.com/article"},"description":"At least three people have died after a shooting Monday night at Michigan State University, police said. Follow for live updates.","publisher":{"@type":"Organization","name":"CNN","logo":{"@type":"ImageObject","url":"https://dynaimage.cdn.cnn.com/cnn/q_auto,h_60/%2F%2Fcdn.cnn.com%2Fcnn%2F.e%2Fimg%2F4.0%2Flogos%2Fcnn_logo_social.jpg"}},"url":"https://www.cnn.com/us/live-news/michigan-state-university-shooting-updates-2-13-23/index.html","headline":"Live updates: Michigan State University shooting, East Lansing campus","image":{"@type":"ImageObject","url":"https://cdn.cnn.com/cnnnext/dam/assets/230213183317-01-michigan-state-shooting-0213-super-tease.jpg","height":"1100","width":"619"},"datePublished":"2023-02-14T02:46:42Z","dateModified":"2023-02-14T07:17:52Z","author":{"@type":"Person","name":"By <a href=\"/profiles/amir-vera\">Amir Vera</a>, Seán Federico O'Murchú, <a href=\"/profiles/tara-subramaniam\">Tara Subramaniam</a> and Adam Renton, CNN"},"speakable":{"@type":"SpeakableSpecification","cssSelector":[".speakable"]}}</script></body></html>''')
    assert metadata.author == "Amir Vera; Seán Federico O'Murchú; Tara Subramaniam; Adam Renton; CNN"
    assert metadata.pagetype == 'newsarticle'

    metadata = extract_metadata(
        '''<html><body><script data-rh="true" type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Organization","@id":"https://traveltomorrow.com/#organization","name":"Travel tomorrow","url":"https://traveltomorrow.com/","sameAs":["https://www.facebook.com/traveltomorrow.eu","https://www.instagram.com/traveltomorrow.eu/","https://www.linkedin.com/company/traveltomorrow/","https://twitter.com/TravelTomorrowX"],"logo":{"@type":"ImageObject","@id":"https://traveltomorrow.com/#logo","inLanguage":"en-GB","url":"https://traveltomorrow.com/wp-content/uploads/2020/05/logo-travel-tomorrow-vertical.png","width":3508,"height":1154,"caption":"Travel tomorrow"},"image":{"@id":"https://traveltomorrow.com/#logo"}},{"@type":"WebSite","@id":"https://traveltomorrow.com/#website","url":"https://traveltomorrow.com/","name":"Travel Tomorrow","description":"","publisher":{"@id":"https://traveltomorrow.com/#organization"},"potentialAction":[{"@type":"SearchAction","target":"https://traveltomorrow.com/?s={search_term_string}","query-input":"required name=search_term_string"}],"inLanguage":"en-GB"},{"@type":"ImageObject","@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#primaryimage","inLanguage":"en-GB","url":"https://traveltomorrow.com/wp-content/uploads/2023/03/2905262_new.jpeg","width":1800,"height":1274},{"@type":"WebPage","@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#webpage","url":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/","name":"Traditional and classical music from Kazakhstan to hit Brussels - Travel Tomorrow","isPartOf":{"@id":"https://traveltomorrow.com/#website"},"primaryImageOfPage":{"@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#primaryimage"},"datePublished":"2023-03-22T11:46:01+00:00","dateModified":"2023-03-22T12:29:54+00:00","inLanguage":"en-GB","potentialAction":[{"@type":"ReadAction","target":["https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/"]}]},{"@type":"Article","@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#article","isPartOf":{"@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#webpage"},"author":{"@id":"https://traveltomorrow.com/#/schema/person/793ea32cfc4e3c0d891ddf002ed1ea2e"},"headline":"Traditional and classical music from Kazakhstan to hit Brussels","datePublished":"2023-03-22T11:46:01+00:00","dateModified":"2023-03-22T12:29:54+00:00","mainEntityOfPage":{"@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#webpage"},"publisher":{"@id":"https://traveltomorrow.com/#organization"},"image":{"@id":"https://traveltomorrow.com/traditional-and-classical-music-from-kazakhstan-to-hit-brussels/#primaryimage"},"articleSection":"Culture,Music,\ud83c\udde7\ud83c\uddea Belgium","inLanguage":"en-GB"},{"@type":"Person","@id":"https://traveltomorrow.com/#/schema/person/793ea32cfc4e3c0d891ddf002ed1ea2e","name":"Deborah O'Donoghue","image":{"@type":"ImageObject","@id":"https://traveltomorrow.com/#personlogo","inLanguage":"en-GB","url":"http://2.gravatar.com/avatar/27467e77f62506f419a9fbe6eef750c4?s=96&d=mm&r=g","caption":"Deborah O'Donoghue"},"description":"Deborah O\u2019Donoghue is a British-Irish writer who has lived in the UK, France and Belgium. She has travelled all over the world and worked in car body repairs, in the best fish \u2018n\u2019 chip shop in Brighton, and been a gopher in a comedy club, as well as a teacher. She\u2019s a past winner of the Commonwealth Broadcasting Association Short Story Prize. Her d\u00e9but novel, Sea of Bones, was published by Legend Press in 2019 and comes out in Germany in 2021. Follow Deborah on Twitter and Instagram."}]}</script></body></html>''')
    print(metadata)
    assert metadata.author == "Deborah O'Donoghue"
    assert metadata.pagetype == 'website'

    metadata = extract_metadata(
        '''<html><body><script data-rh="true" type="application/ld+json">{"@context":"https://schema.org","dateModified":"2022-10-18T07:02:26+0100","image":{"@type":"ImageObject","url":"https://i.dailymail.co.uk/1s/2022/10/18/06/63581747-0-image-a-54_1666070195906.jpg","height":"1146","width":"1908"},"author":[{"@type":"Person","name":"Sam McPhee"},{"@type":"Person","name":"¿\ttara Cosoleto"}],"video":{"width":1024,"height":576,"uploadDate":"2022-10-16T23:49:15+0100","contentUrl":"https://videos.dailymail.co.uk/video/backup/2022/10/16/8580444913529736888/1024x576_MP4_8580444913529736888.mp4","name":"Today weather crew catches looters rifling through evacuated home","thumbnailUrl":"https://i.dailymail.co.uk/1s/2022/10/16/23/63534109-0-image-a-21_1665960603330.jpg","duration":"PT00M28S","@type":"VideoObject","description":"Today weather presenter Tim Davies and his camera crew catch looters in face masks and hoodies rifling through an evacuated home in Maribyrnong, Melbourne: 'It's a sickening sight'"},"id":"https://www.dailymail.co.uk/news/article-11326469/Victoria-floods-Echuca-looters-steal-sandbags-item-towns-work-waters-bay.html","mainEntityOfPage":{"@type":"WebPage","@id":"https://www.dailymail.co.uk/news/article-11326469/Victoria-floods-Echuca-looters-steal-sandbags-item-towns-work-waters-bay.html","name":"Victoria floods: Echuca looters steal sandbags item as towns work to keep waters at bay","headline":"Victoria floods: Echuca looters steal sandbags item as towns work to keep waters at bay","image":"https://i.dailymail.co.uk/1s/2022/10/18/06/63581747-0-image-a-54_1666070195906.jpg","url":"https://www.dailymail.co.uk/news/article-11326469/Victoria-floods-Echuca-looters-steal-sandbags-item-towns-work-waters-bay.html","mainEntity":{"@type":"Thing","name":"Victoria floods: Echuca looters steal sandbags item as towns work to keep waters at bay"}},"name":"Victoria floods: Echuca looters steal sandbags item as towns work to keep waters at bay","articleBody":"Looters stealing sandbags from outside flood-affected homes in Victoria. Echuca woman Abby said hundreds of bags disappeared from cousin's house. Channel Nine weatherman also caught group of men looting family home. More wet weather is due for Victoria for the remainder of the week","publisher":{"@type":"Organization","name":"Daily Mail","sameAs":["DailyMail","https://www.facebook.com/DailyMail","https://twitter.com/MailOnline","https://www.youtube.com/user/MailOnlineVideo","https://www.instagram.com/dailymail/","https://www.snapchat.com/discover/Daily-Mail/8392137033","https://flipboard.com/@DailyMailUS","https://www.pinterest.co.uk/dailymail/"],"logo":{"@type":"ImageObject","url":"https://i.dailymail.co.uk/i/sitelogos/sd-dailymail.png","width":"600","height":"60"},"address":{"@type":"PostalAddress","streetAddress":"Northcliffe House, 2 Derry Street","addressLocality":"London","addressRegion":"London","postalCode":"W8 5TT","addressCountry":{"@type":"Country","name":"GB"}}},"datePublished":"2022-10-18T07:02:26+0100","@type":"NewsArticle","description":"Shameful looters have resorted to stealing the sandbags protecting homes in Victoria as the state braces for more heavy rainfall.","headline":"Victoria floods: Echuca looters steal sandbags item as towns work to keep waters at bay"}</script></body></html>''')
    assert metadata.author == "Sam McPhee; Tara Cosoleto"
    assert metadata.pagetype == 'newsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''<html><body><script type="application/ld+json" class="yoast-schema-graph">{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage","url":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/","name":"Jean S\u00e9villia : \"L'\u00c9tat fran\u00e7ais et l'\u00c9tat alg\u00e9rien doivent reconna\u00eetre les crimes commis des deux c\u00f4t\u00e9s\" - Boulevard Voltaire","datePublished":"2018-09-13T12:21:13+00:00","dateModified":"2018-09-14T12:33:14+00:00","inLanguage":"fr-FR"},{"@type":"Article","@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#article","isPartOf":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage"},"author":{"@id":"https://www.bvoltaire.fr/#/schema/person/96c0ed8f089950c46afc2044cb23e8da"},"headline":"Jean S\u00e9villia : &#8220;L&#8217;\u00c9tat fran\u00e7ais et l&#8217;\u00c9tat alg\u00e9rien doivent reconna\u00eetre les crimes commis des deux c\u00f4t\u00e9s&#8221;","datePublished":"2018-09-13T12:21:13+00:00","dateModified":"2018-09-14T12:33:14+00:00","mainEntityOfPage":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage"},"publisher":{"@id":"https://www.bvoltaire.fr/#organization"},"image":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#primaryimage"},"keywords":"Guerre d'Alg\u00e9rie","articleSection":"Audio,Editoriaux,Entretiens,Histoire","inLanguage":"fr-FR"},{"@type":"Person","@id":"https://www.bvoltaire.fr/#/schema/person/96c0ed8f089950c46afc2044cb23e8da","name":"Jean S\u00e9villia","image":{"@type":"ImageObject","@id":"https://www.bvoltaire.fr/#personlogo","inLanguage":"fr-FR","url":"https://secure.gravatar.com/avatar/1dd0ad5cb1fc3695880af1725477b22e?s=96&d=mm&r=g","caption":"Jean S\u00e9villia"},"description":"R\u00e9dacteur en chef adjoint au Figaro Magazine, membre du comit\u00e9 scientifique du Figaro Histoire, et auteur de biographies et d\u2019essais historiques.","sameAs":["https://www.bvoltaire.fr/"]}]}</script></body></html>'''), metadata)
    assert metadata.author == "Jean Sévillia"
    assert metadata.pagetype == 'webpage'

    ### Test for potential errors
    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
<script type="application/ld+json">
{
  "@context":"http://schema.org",
  "@type":"LiveBlogPosting",
  "@id":"http://techcrunch.com/2015/03/08/apple-watch-event-live-blog",
  "about":{
    "@type":"Event",
    "startDate":"2015-03-09T13:00:00-07:00",
    "name":"Apple Spring Forward Event"
  },
  "coverageStartTime":"2015-03-09T11:30:00-07:00",
  "coverageEndTime":"2015-03-09T16:00:00-07:00",
  "headline":"Apple Spring Forward Event Live Blog",
  "description":"Welcome to live coverage of the Apple Spring Forward …",
  "liveBlogUpdate":{
      "@type":"BlogPosting",
      "headline":"Coming this April, HBO NOW will be available exclusively in the U.S. on Apple TV and the App Store.",
      "datePublished":"2015-03-09T13:08:00-07:00",
      "articleBody": "It's $14.99 a month.<br> And for a limited time, …"
    },
}
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == 'Apple Spring Forward Event Live Blog'
    assert metadata is not None and metadata.pagetype == 'liveblogposting'

    ### Test for potential errors
    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
<script type="application/ld+json">
{
  "@context":"http://schema.org",
  "@type":"LiveBlogPosting",
  "@id":"http://techcrunch.com/2015/03/08/apple-watch-event-live-blog",
  "about":{
    "@type":"Event",
    "startDate":"2015-03-09T13:00:00-07:00",
    "name":"Apple Spring Forward Event"
  },
  "coverageStartTime":"2015-03-09T11:30:00-07:00",
  "coverageEndTime":"2015-03-09T16:00:00-07:00",
  "headline":"Apple Spring Forward Event Live Blog",
  "description":"Welcome to live coverage of the Apple Spring Forward …",
    "liveBlogUpdate": [
    {
      "@type":"BlogPosting",
      "headline":"iPhone is growing at nearly twice the rate of the rest of the smartphone market.",
      "datePublished":"2015-03-09T13:13:00-07:00",
      "image":"http://images.apple.com/live/2015-mar-event/images/573cb_xlarge_2x.jpg"
    },
    {
      "@type":"BlogPosting",
      "headline":"See the new flagship Apple Retail Store in West Lake, China.",
      "datePublished":"2015-03-09T13:17:00-07:00",
      "video":{
        "@type":"VideoObject",
        "thumbnail":"http://images.apple.com/live/2015-mar-event/images/908d2e_large_2x.jpg"
    },
  ]
}
</script>
</body></html>'''), metadata)

    assert metadata is not None and metadata.title == 'Apple Spring Forward Event Live Blog'
    assert metadata is not None and metadata.pagetype == 'liveblogposting'

    ### Test for potential errors - Missing content on live blog
    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
    <script type="application/ld+json">
    {
      "@context":"http://schema.org",
      "@type":"LiveBlogPosting",
      "@id":"http://techcrunch.com/2015/03/08/apple-watch-event-live-blog",
      "about":{
        "@type":"Event",
        "startDate":"2015-03-09T13:00:00-07:00",
        "name":"Apple Spring Forward Event"
      },
      "coverageStartTime":"2015-03-09T11:30:00-07:00",
      "coverageEndTime":"2015-03-09T16:00:00-07:00",
      "headline":"Apple Spring Forward Event Live Blog",
      "description":"Welcome to live coverage of the Apple Spring Forward …"
    }
    </script>
    </body></html>'''), metadata)

    assert metadata is not None and metadata.title == 'Apple Spring Forward Event Live Blog'
    assert metadata is not None and metadata.pagetype == 'liveblogposting'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "socialmediaposting",
            "name": "The Hitchhiker's Guide to the Galaxy",
            "genre": "comedy science fiction",
            "startDate": "1979-10-12",
            "endDate": "1992-10-12",
            "abstract": "Earthman Arthur Dent is saved by his friend, Ford Prefect—an alien researcher for the titular Hitchhiker's Guide to the Galaxy, which provides info on every planet in the galaxy—from the Earth just before it is destroyed by the alien Vogons.",
            "author": {
                "@type": "Person",
                "givenName": "Douglas",
                "familyName": "Adams",
                "additionalName": "Noel",
                "birthDate": "1952-03-11",
                "birthPlace": {
                    "@type": "Place",
                    "address": "Cambridge, Cambridgeshire, England"
                },
                "deathDate": "2001-05-11",
                "deathPlace": {
                    "@type": "Place",
                    "address": "Highgate Cemetery, London, England"
                }
            }
        }
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.author == 'Douglas Noel Adams'
    assert metadata is not None and metadata.pagetype == 'socialmediaposting'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        {
            "@context":"https://schema.org",
            "@graph":[
                {
                    "@type": "Article",
                    "author":{
                        "name":"John Smith"
                    },
                    "keywords": [
                        "SAFC",
                        "Warwick Thornton"
                    ],
                    "articleSection": [
                        null
                    ],
                    "inLanguage": "en-AU"
                }
            ]
        }
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and len(metadata.categories) == 0
    assert metadata is not None and metadata.pagetype == 'article'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        {
            "@context":"http://schema.org",
            "@type":"WebPage",
            "url":"https://7news.com.au/sport/golf/mickelson-comments-hurt-new-league-norman-c-6658099",
            "name":"Mickelson comments hurt new league: Norman | 7NEWS",
            "alternateName":"7NEWS",
            "author":{
                "@type":"Person",
                "name":"7NEWS"
            },
            "description":"Greg Norman says a host of the world's top golfers were set to be involved in his new Saudi-funded golf league until Phil Mikelson's controversial comments.",
            "publisher":{
                "@type":"Organization",
                "name":"7NEWS",
                "url":"https://7news.com.au",
                "logo":{
                "@type":"ImageObject",
                "url":"https://7news.com.au/static/social-images/publisher-logo-60px-high.png",
                "width":600,
                "height":60
                }
            },
            "image":{
                "@type":"ImageObject",
                "url":"https://7news.com.au/static/social-images/share-400x400.png",
                "width":400,
                "height":400
            }
        }
    </script>
    <script type="application/ld+json">
        {
            "@context":"http://schema.org",
            "@type":"NewsArticle",
            "mainEntityOfPage":{
                "@type":"WebPage",
                "@id":"https://7news.com.au/sport/golf/mickelson-comments-hurt-new-league-norman-c-6658099"
            },
            "dateline":"Sydney, AU",
            "publisher":{
                "@type":"Organization",
                "name":"7NEWS",
                "url":"https://7news.com.au",
                "logo":{
                "@type":"ImageObject",
                "url":"https://7news.com.au/static/social-images/publisher-logo-60px-high.png",
                "width":600,
                "height":60
            }
            },
            "keywords":[
                "Sport",
                "Golf"
            ],
            "articleSection":"Golf",
            "headline":"Mickelson comments hurt new league: Norman",
            "description":"Greg Norman says a host of the world's top golfers were set to be involved in his new Saudi-funded golf league until Phil Mikelson's controversial comments.",
            "dateCreated":"2022-05-02T23:20:48.000Z",
            "datePublished":"2022-05-02T23:20:48.000Z",
            "dateModified":"2022-05-02T23:20:50.493Z",
            "isAccessibleForFree":true,
            "isPartOf":{
                "@type":[
                    "CreativeWork",
                    "Product"
                ],
                "name":"7NEWS",
                "productID":"7news.com.au:everyday_digital"
            },
            "articleBody":"Greg Norman has declared that Phil Mickelson's controversial comments complicated matters for the lucrative new golf league he is fronting that is backed by Saudi Arabian investment. "There's no question (it) hurt. It hurt a lot of aspects," Norman told ESPN. "It hurt the PGA Tour. It hurt us. It hurt the game of golf. It hurt Phil. So yeah, across all fronts. It wasn't just specifically to us. But it definitely created negative momentum against us." Two-time major championship winner Norman is the CEO of the LIV Golf Invitational Series, formerly known as the Super Golf League. As the venture was trying to get rolling, comments from Mickelson published on February 15, after a November interview with author Alan Shipnuck, caused a firestorm. Mickelson referenced the killing of Washington Post reporter Jamal Khashoggi and called the Saudi Arabians "scary motherf***ers to get involved with." He went on to explain why he still had interest in joining the Saudi-backed league. "(They) have a horrible record on human rights," Mickelson was said, according to Shipnuck. "They execute people over there for being gay. Knowing all of this, why would I even consider it? Because this is a once-in-a-lifetime opportunity to reshape how the PGA Tour operates. "They've been able to get by with manipulative, coercive, strong-arm tactics because we, the players, had no recourse." Norman said on Monday that nearly one third of the top 50 players in the world were committed to playing in the new golf tour. When Mickelson's comments were revealed, many top players instead reaffirmed their commitment to playing on the PGA Tour. "Quite honestly, we were ready to launch (in February)," Norman said to ESPN. "We had enough players in our strength of field, or minimal viable product, ready to come on board. "And when all of that happened, everybody got the jitters, and the PGA Tour threatened people with lifetime bans and stuff like that." Originally set to be a 14-event schedule, the LIV Golf Invitational Series has been restructured to an eight tournament season. Of those, five are expected to take place in the United States with a total of $255 million ($A361m) in prize money. Mickelson has since filed a request to play in an event that conflicts with the PGA Tour, signalling his desire to still play in the LIV Golf Invitational Series. A June 9-11 tournament is set for London and will be open to 48 players set to compete on 12 four-man teams. "I've been very pleasantly surprised," Norman said. "What has been talked about in the media and what is reality are two different things. "We know what's happening with a lot of interest expressed. "From an expectation standpoint, we've got a lot of interest from significantly named players."",
            "image":[
            {
                "@type":"ImageObject",
                "url":"https://images.7news.com.au/publication/C-6658099/47ef62deeb56ad4e91bde98237459c3c66dec3e9-16x9-x0y0w1280h720.jpg",
                "width":1280,
                "height":720
            },
            {
                "@type":"ImageObject",
                "url":"https://images.7news.com.au/publication/C-6658099/47ef62deeb56ad4e91bde98237459c3c66dec3e9-4x3-x160y0w960h720.jpg",
                "width":960,
                "height":720
            }
            ],
            "thumbnailUrl":"https://images.7news.com.au/publication/C-6658099/47ef62deeb56ad4e91bde98237459c3c66dec3e9-16x9-x0y0w1280h720.jpg",
            "url":"https://7news.com.au/sport/golf/mickelson-comments-hurt-new-league-norman-c-6658099",
            "author":[
            {
                "@type":"Person",
                "@id":"/profile/digital-staff",
                "jobTitle":"Writer",
                "name":"Digital Staff",
                "publishingPrinciples":null,
                "description":"Journalist from the 7NEWS.com.au team.",
                "sameas":[
                ],
                "image":null
                }
            ],
            "name":"Mickelson comments hurt new league: Norman"
            }
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == "Mickelson comments hurt new league: Norman" and metadata.sitename == "7NEWS" and metadata.author == "Digital Staff" and "Golf" in metadata.categories and metadata.pagetype == 'newsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        {
            "@context":"http://schema.org",
            "@type":"NewsArticle",
            "author":[
                {
                    "@type":"Person",
                    "name":"Bill Birtles"
                }
            ],
            "dateModified":"2022-05-02T17:58:24+00:00",
            "datePublished":"2022-05-02T17:58:24+00:00",
            "description":"Some Australians caught up in Shanghai's extreme five-week lockdown say the Australian government has done little to help its citizens in distress, and they're pleading with Canberra to arrange charter flights to get them home. ",
            "headline":"Australians stuck in Shanghai's COVID lockdown beg consular officials to help them flee",
            "image":{
                "@type":"ImageObject",
                "height":485,
                "url":"https://live-production.wcms.abc-cdn.net.au/e4c2d55eac0a18fae458413c45915787?impolicy=wcms_crop_resize&cropH=608&cropW=1080&xPos=0&yPos=38&width=862&height=485",
                "width":862
            },
            "keywords":"",
            "mainEntityOfPage":"https://www.abc.net.au/news/2022-05-03/australians-in-shanghai-lockdown-voice-frustration/101031126",
            "publisher":{
                "@type":"Organization",
                "name":"ABC News",
                "logo":{
                    "@type":"ImageObject",
                    "height":60,
                    "url":"https://www.abc.net.au/res/abc/logos/amp-news-logo-60x240.png",
                    "width":240
                }
            }
        }
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == "Australians stuck in Shanghai's COVID lockdown beg consular officials to help them flee" and metadata.author == "Bill Birtles" and metadata.sitename == "ABC News" and metadata.pagetype == 'newsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
    {
        "@context":"http://schema.org",
        "@type":"NewsArticle",
        "description":"The city moved into the medium risk level, known as yellow, as it sees a troubling increase in cases and the mayor weighs bringing back some restrictions.",
        "image":[
            {
                "@context":"http://schema.org",
                "@type":"ImageObject",
                "url":"https://static01.nyt.com/images/2022/05/02/multimedia/02nyvirus-alert2/02nyvirus-alert2-videoSixteenByNineJumbo1600.jpg",
                "height":900,
                "width":1600,
                "caption":"Herald Square in Manhattan on Monday. New York City entered the yellow coronavirus risk level, meaning cases rose above 200 per 100,000 residents per week."
            },
            {
                "@context":"http://schema.org",
                "@type":"ImageObject",
                "url":"https://static01.nyt.com/images/2022/05/02/multimedia/02nyvirus-alert2/02nyvirus-alert2-superJumbo.jpg",
                "height":1366,
                "width":2048,
                "caption":"Herald Square in Manhattan on Monday. New York City entered the yellow coronavirus risk level, meaning cases rose above 200 per 100,000 residents per week."
            },
            {
                "@context":"http://schema.org",
                "@type":"ImageObject",
                "url":"https://static01.nyt.com/images/2022/05/02/multimedia/02nyvirus-alert2/02nyvirus-alert2-mediumSquareAt3X.jpg",
                "height":1801,
                "width":1800,
                "caption":"Herald Square in Manhattan on Monday. New York City entered the yellow coronavirus risk level, meaning cases rose above 200 per 100,000 residents per week."
            }
        ],
        "mainEntityOfPage":"https://www.nytimes.com/2022/05/02/nyregion/nyc-coronavirus-yellow-risk-level.html",
        "url":"https://www.nytimes.com/2022/05/02/nyregion/nyc-coronavirus-yellow-risk-level.html",
        "inLanguage":"en",
        "author":[
            {
                "@context":"http://schema.org",
                "@type":"Person",
                "url":"https://www.nytimes.com/by/sharon-otterman",
                "name":"Sharon Otterman"
            },
            {
                "@context":"http://schema.org",
                "@type":"Person",
                "url":"https://www.nytimes.com/by/emma-g-fitzsimmons",
                "name":"Emma G. Fitzsimmons"
            }
        ],
        "dateModified":"2022-05-02T20:21:32.149Z",
        "datePublished":"2022-05-02T14:31:28.000Z",
        "headline":"New York City Enters Higher Coronavirus Risk Level as Case Numbers Rise",
        "publisher":{
            "@id":"https://www.nytimes.com/#publisher"
        },
        "copyrightHolder":{
            "@id":"https://www.nytimes.com/#publisher"
        },
        "sourceOrganization":{
            "@id":"https://www.nytimes.com/#publisher"
        },
        "copyrightYear":2022,
        "isAccessibleForFree":false,
        "hasPart":{
            "@type":"WebPageElement",
            "isAccessibleForFree":false,
            "cssSelector":".meteredContent"
        },
        "isPartOf":{
            "@type":[
                "CreativeWork",
                "Product"
            ],
            "name":"The New York Times",
            "productID":"nytimes.com:basic"
        }
    }
    </script>
    <script type="application/ld+json">
        {
            "@context":"http://schema.org",
            "@type":"NewsMediaOrganization",
            "name":"The New York Times",
            "logo":{
                "@context":"http://schema.org",
                "@type":"ImageObject",
                "url":"https://static01.nyt.com/images/misc/NYT_logo_rss_250x40.png",
                "height":40,
                "width":250
            },
            "url":"https://www.nytimes.com/",
            "@id":"https://www.nytimes.com/#publisher",
            "diversityPolicy":"https://www.nytco.com/diversity-and-inclusion-at-the-new-york-times/",
            "ethicsPolicy":"https://www.nytco.com/who-we-are/culture/standards-and-ethics/",
            "masthead":"https://www.nytimes.com/interactive/2020/09/08/admin/the-new-york-times-masthead.html",
            "foundingDate":"1851-09-18",
            "sameAs":"https://en.wikipedia.org/wiki/The_New_York_Times"
        }
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == "New York City Enters Higher Coronavirus Risk Level as Case Numbers Rise" and metadata.author == "Sharon Otterman; Emma G Fitzsimmons" and metadata.sitename == "The New York Times" and metadata.pagetype == 'newsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        [
            {
                "@type":"NewsArticle",
                "@context":"http://schema.org",
                "headline":"Decreto permite que consumidor cancele serviços de empresas via WhatsApp",
                "description":"O governo federal estabeleceu mudanças nas regras do SAC (Serviço de Atendimento ao Consumidor). Uma das principais alterações é a obrigação das empresas em disponibilizarem a possibilidade de cancelamento de algum serviço através do mesmo canal em que oc",
                "author":{
                    "name":"Caio Mello",
                    "@type":"Person",
                    "url":"https://uol.com.br/"
                },
                "publisher":{
                    "@type":"Organization",
                    "name":"UOL",
                    "url":"https://www.uol.com.br",
                    "logo":{
                        "@type":"ImageObject",
                        "url":"https://conteudo.imguol.com.br/uolamp/UOL_logo_156x60.png",
                        "width":156,
                        "height":60
                    }
                },
                "url":"https://economia.uol.com.br/noticias/redacao/2022/05/02/empresas-devem-permitir-cancelamento-pelo-whatsapp-a-partir-de-outubro.htm",
                "mainEntityOfPage":"https://economia.uol.com.br/noticias/redacao/2022/05/02/empresas-devem-permitir-cancelamento-pelo-whatsapp-a-partir-de-outubro.htm",
                "image":[
                    "https://conteudo.imguol.com.br/c/noticias/82/2022/01/28/telegram-e-whatsapp-na-tela-do-celular-smartphone-wechat-aps-de-mensageria-mensagem-1643388540478_v2_1x1.jpg",
                    "https://conteudo.imguol.com.br/c/noticias/82/2022/01/28/telegram-e-whatsapp-na-tela-do-celular-smartphone-wechat-aps-de-mensageria-mensagem-1643388540478_v2_3x4.jpg",
                    "https://conteudo.imguol.com.br/c/noticias/82/2022/01/28/telegram-e-whatsapp-na-tela-do-celular-smartphone-wechat-aps-de-mensageria-mensagem-1643388540478_v2_4x3.jpg"
                ],
                "datePublished":"2022-05-02T15:40:13-03:00",
                "dateModified":"2022-05-02T17:52:35-03:00"
            }
        ]
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == "Decreto permite que consumidor cancele serviços de empresas via WhatsApp" and metadata.author == "Caio Mello" and metadata.sitename == "UOL"

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        {
            "@context": "http://schema.org",
            "@type": "NewsArticle",
            "mainEntityOfPage": "https://www.thelocal.de/20190402/12-words-and-phrases-to-help-you-show-off-in-hamburg/",
            "headline": "12 words and phrases you need to survive in Hamburg",
            "datePublished": "2019-04-02T10:18:44+02:00",
            "dateModified": "2022-05-02T16:48:55+02:00",
            "description": "Hamburg is a pretty cosmopolitan place, and you won’t have any problem speaking Hochdeutsch around town. But traditionally, people in the city speak Hamburger Platt, and it&#39;s still very much alive.",
            "keywords": ["language","hamburg"],
            "isAccessibleForFree": true,
            "author": {
                "@type": "Person",
                "name": "Alexander Johnstone",
                "email": "news@thelocal.de",
                "url": "https://www.thelocal.de"
            },
            "publisher": {
                "@type": "Organization",
                "name": "The Local",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://www.thelocal.de/wp-content/themes/thelocal/assets/images/the-local-network-logo-300x60.png",
                    "width": 300,
                    "height": 60
                }
            },
            "isPartOf": {
              "@type": ["CreativeWork", "Product"],
              "name" : "Membership of The Local",
              "productID": "thelocal.de:member"
            },
            "image": {
                "@type": "ImageObject",
                "url": "https://apiwp.thelocal.com/wp-content/uploads/2019/04/c99168bc66462f0a1ae0472c449af4b5c28c9652c1ccf7cb961a8d8cf77b147b.jpg",
                "width": 1500,
                "height": 1000
            },
            "articleBody": "<p><i>Hamburger Platt</i> a quirky variation of Low Saxon (<i>Niederdeutsch</i>), a language which is spoken in northern Germany and eastern parts of the Netherlands.</p><p>It is estimated that are around <a href=\"http://www.hamburg.de/stadtleben/4108598/plattdeutsch-geschichte/\" target=\"_blank\" rel=\"noopener noreferrer\">six million people in eight different German states speak Low Saxon, and around 100,000 speak it in Hamburg itself.</a></p><p><strong>SEE ALSO:<a href=\"https://www.thelocal.de/20190321/local-knowledge-an-insiders-guide-to-life-in-hamburg\"> Local knowledge: an insider guide to life in Hamburg</a></strong></p><p>But it’s on the rise, especially among the young. Some schools teach it from first grade, and there’s even a Hip-Hop group “De fofftig Penns” (“Die fünfzig Pfennige” or \"50 cents\" as pfennig was a former currency) that raps in Plattdeutsch.</p><p>So we thought we should get started on some Hamburger Platt too.</p><p>Here’s a little list of words and phrases to get you started, so that next time you go to Hamburg, you can start to fit in like a true local:</p><p><strong>1. Moin (hello)</strong></p><p><i>Moin</i>, also sometimes <i>moin moin </i>covers a lot of different greetings, as it can mean <i>Guten Morgen</i>, <i>Guten Tag</i> and even <i>Guten Abend</i>. How simple!</p><p><img class=\"size-full wp-image-687931\" src=\"https://apiwp.thelocal.com/wp-content/uploads/2019/04/275024014-scaled.jpg\" alt=\"A shop in Hamburg with the sign 'Moin' outside. \" width=\"2560\" height=\"1673\" /></p><div class=\"post-thumbnail-credit\">A shop in Hamburg with the sign 'Moin' outside. Photo: picture alliance/dpa | Axel Heimken</div><p><strong>2. Schnacken (chat)</strong></p><p><i>Schnack</i> is also the word for chit-chat, and someone who speaks Plattdeutsch could be described as a <i>Plattschnacker</i>.</p><div class=\"ml-manual-widget-container\" style=\"height: 50px; border: 1px solid #c3c3c3; background-color: #dedede;\">Manual widget for ML (class=\"ml-manual-widget-container\")</div><p><strong>3. Macker (lad)</strong></p><p>This means a lad or a mate or even a boyfriend. Or you could try the slang term <i>Digga</i>, which is more equivalent to <i>Alter</i>, meaning dude or man, and has become pretty cool recently.</p><p><strong>4. Klock (clock)</strong></p><p>You probably could've guessed this one. It shows how close some of the words are to English. There isn't always that much difference between the Low Saxon and the Anglo Saxon (which is the route of much of the English language).</p><p><strong>5. Schmöken (smoke)</strong></p><p>Another one that just sounds like English in a German accent! When you're in Hamburg you'll see people <i>schnacken</i> while they <i>schmöken</i> outside a restaurant.</p><p><strong>6. Büx (trousers)</strong></p><p><span style=\"font-size: 10px;\"><i><img style=\"width: 640px; height: 383px;\" src=\"https://www.thelocal.com/wp-content/uploads/2019/04/1511264772_1481025162_buex.jpg\" alt=\"\" />A man holds up a huge pair of </i>Büx<i> at the Hamburg tailor's Herrenkleidung Policke, which makes suits for all sizes imaginable. Photo: DPA</i></span></p><p>Perhaps not one you'll use everyday, but there's also the related verb <i>utbüxen,</i> which means to slip away or escape.</p><p><strong>7. Mall (mad)</strong></p><p>You may well hear \"Bist du mall?!\" being bounded around, which means \"Are you out of you mind?!\"</p><p><strong>8. Sabbelknoken (mobile phone)</strong></p><p>It's definitely a bit of a mouthful, but it is still used by some in Hamburg, and literally translates as a \"mouth bone/limb\".</p><p><strong>9. Wat is de Klock? (What’s the time?)</strong></p><p>You don't need to be Sherlock to deduce this one either, as it sounds like broken English, but it could come in pretty useful on a visit.</p><p><strong>10. En mol Lütt un Lütt (a beer and a schnapps)</strong></p><p>Here's where you might need Sherlock. This is a classic order in a traditional Hamburg pub, but who would have thought that asking for two Lütt could get you both a beer and a shot?</p><p><strong>11. In’n Tüddel koomm (get confused)</strong></p><p>This one almost sounds like what it means, and you almost have to yodel to say it. If you by mistake stumbled into Herbertstraße off the Reeperbahn, you may well <i>in'n Tüddel koomm</i>.</p><p><strong>12. Du bist mein Schietbüdel (you’re my darling)</strong></p><p>And finally one for if you find the right person in Hamburg. It's become really popular in the last few years, and although it used to be an insult, it's now used as a term of endearment. </p>"
          }
    </script>
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == "12 words and phrases you need to survive in Hamburg" and metadata.author == "Alexander Johnstone" and metadata.sitename == "The Local" and metadata.pagetype == 'newsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
    <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": "https://a16z.com/#website",
                    "url": "https://a16z.com/",
                    "name": "Andreessen Horowitz",
                    "potentialAction": {
                        "@type": "SearchAction",
                        "target": "https://a16z.com/?s={search_term_string}",
                        "query-input": "required name=search_term_string"
                    }
                },
                {
                    "@type": "ProfilePage",
                    "@id": "https://a16z.com/author/ben-horowitz/#webpage",
                    "url": "https://a16z.com/author/ben-horowitz/",
                    "inLanguage": "en-US",
                    "name": "- Andreessen Horowitz",
                    "isPartOf": {
                        "@id": "https://a16z.com/#website"
                    }
                },
                {
                    "@type": [
                        "Person"
                    ],
                    "@id": "https://a16z.com/#/schema/person/2022059d3b1b2ba8b3464ff2cc2e4165",
                    "name": null,
                    "image": {
                        "@type": "ImageObject",
                        "@id": "https://a16z.com/#authorlogo",
                        "url": "https://secure.gravatar.com/avatar/?s=96&d=identicon&r=g"
                    },
                    "sameAs": [],
                    "mainEntityOfPage": {
                        "@id": "https://a16z.com/author/ben-horowitz/#webpage"
                    }
                }
            ]
        }
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.author is None and metadata.sitename == "Andreessen Horowitz" and metadata.pagetype == 'website'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
<script type="application/ld+json">
{
  "about":{
    "@type":"Event",
    "startDate":"2015-03-09T13:00:00-07:00",
    "name":"Apple Spring Forward Event"
  },
}
</script>
</body></html>'''), metadata)

    assert metadata is not None and metadata.author is None and metadata.sitename is None and metadata.pagetype is None

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
    <script type="application/ld+json">
    {
      "@context":"http://google.com",
      "@type":"LiveBlogPosting",
      "@id":"http://techcrunch.com/2015/03/08/apple-watch-event-live-blog",
      "about":{
        "@type":"Event",
        "startDate":"2015-03-09T13:00:00-07:00",
        "name":"Apple Spring Forward Event"
      },
      "coverageStartTime":"2015-03-09T11:30:00-07:00",
      "coverageEndTime":"2015-03-09T16:00:00-07:00",
      "headline":"Apple Spring Forward Event Live Blog",
      "description":"Welcome to live coverage of the Apple Spring Forward …",
      "liveBlogUpdate":[{
          "@type":"BlogPosting",
          "headline":"Coming this April, HBO NOW will be available exclusively in the U.S. on Apple TV and the App Store.",
          "datePublished":"2015-03-09T13:08:00-07:00",
          "articleBody": "It's $14.99 a month.<br> And for a limited time, …"
        }],
    }
    </script>
    </body></html>'''), metadata)

    assert metadata is not None and metadata.author is None and metadata.sitename is None and metadata.pagetype == 'liveblogposting'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
<script type="application/ld+json">
{
  "@context":"http://schema.org",
  "@type":"LiveBlogPosting",
  "@id":"http://techcrunch.com/2015/03/08/apple-watch-event-live-blog",
  "about":{
    "@type":"Event",
    "startDate":"2015-03-09T13:00:00-07:00",
    "name":"Apple Spring Forward Event"
  },
  "coverageStartTime":"2015-03-09T11:30:00-07:00",
  "coverageEndTime":"2015-03-09T16:00:00-07:00",
  "headline":"Apple Spring Forward Event Live Blog",
  "description":"Welcome to live coverage of the Apple Spring Forward …",
  "liveBlogUpdate":[{
      "@type":"BlogPosting",
      "headline":"Coming this April, HBO NOW will be available exclusively in the U.S. on Apple TV and the App Store.",
      "datePublished":"2015-03-09T13:08:00-07:00",
      "articleBody": "It's $14.99 a month.<br> And for a limited time, …"
    }],
}
</script>
</body></html>'''), metadata)
    assert metadata is not None and metadata.title == 'Apple Spring Forward Event Live Blog' and metadata.pagetype == 'liveblogposting'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
<html><body>
<script type="application/ld+json">
{
        "@context": "http:\/\/schema.org",
        "@type": "ReportageNewsArticle",
        "url": "https:\/\/www.bbc.com\/news\/entertainment-arts-51582573",
        "publisher": {
            "@type": "NewsMediaOrganization",
            "name": "BBC News",
            "publishingPrinciples": "http:\/\/www.bbc.co.uk\/news\/help-41670342",
            "logo": {
                "@type": "ImageObject",
                "url": "https:\/\/www.bbc.co.uk\/news\/special\/2015\/newsspec_10857\/bbc_news_logo.png?cb=1"
            }
        },
        "datePublished": "2020-02-21T05:02:18+00:00",
        "dateModified": "2020-02-21T05:02:18+00:00",
        "headline": "EastEnders' June Brown leaves soap 'for good'",
        "image": {
            "@type": "ImageObject",
            "width": 720,
            "height": 405,
            "url": "https:\/\/ichef.bbci.co.uk\/news\/720\/cpsprodpb\/B4EE\/production\/_110981364_hi057715325.jpg"
        },
        "thumbnailUrl": "https:\/\/ichef.bbci.co.uk\/news\/208\/cpsprodpb\/B4EE\/production\/_110981364_hi057715325.jpg",
        "author": {
            "@type": "NewsMediaOrganization",
            "name": "BBC News",
            "logo": {
                "@type": "ImageObject",
                "url": "https:\/\/www.bbc.co.uk\/news\/special\/2015\/newsspec_10857\/bbc_news_logo.png?cb=1"
            },
            "noBylinesPolicy": "http:\/\/www.bbc.co.uk\/news\/help-41670342#authorexpertise"
        },
        "mainEntityOfPage": "https:\/\/www.bbc.com\/news\/entertainment-arts-51582573",
        "video": {
            "@type": "VideoObject",
            "name": "June Brown's 90 years in 90 seconds",
            "description": "EastEnders star June Brown - aka Dot Cotton - is turning 90 on Thursday. Here's a 90-second look back at her life.",
            "duration": "PT1M36S",
            "thumbnailUrl": "https:\/\/ichef.bbci.co.uk\/images\/ic\/208x117\/p04t12n5.jpg",
            "uploadDate": "2017-02-15T18:05:00+00:00"
        }
    }
</script>
</body></html>'''), metadata)

    assert metadata is not None and metadata.title == "EastEnders' June Brown leaves soap 'for good'" and metadata.sitename == "BBC News" and metadata.pagetype == 'reportagenewsarticle'

    metadata = Document()
    metadata.sitename = "https://bbcnews.com"
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
    <script type="application/ld+json">
    {
            "@context": "http:\/\/schema.org",
            "@type": "ReportageNewsArticle",
            "url": "https:\/\/www.bbc.com\/news\/entertainment-arts-51582573",
            "publisher": {
                "@type": "NewsMediaOrganization",
                "name": "BBC News",
                "publishingPrinciples": "http:\/\/www.bbc.co.uk\/news\/help-41670342",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https:\/\/www.bbc.co.uk\/news\/special\/2015\/newsspec_10857\/bbc_news_logo.png?cb=1"
                }
            },
        }
    </script>
    </body></html>'''), metadata)

    assert metadata is not None and metadata.sitename == "BBC News" and metadata.pagetype == 'reportagenewsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "author": "John Doe",
      "interactionStatistic": [
        {
          "@type": "InteractionCounter",
          "interactionService": {
            "@type": "WebSite",
            "name": "Twitter",
            "url": "http://www.twitter.com"
          },
          "interactionType": "https://schema.org/ShareAction",
          "userInteractionCount": "1203"
        },
        {
          "@type": "InteractionCounter",
          "interactionType": "https://schema.org/CommentAction",
          "userInteractionCount": "78"
        }
      ],
      "name": "How to Tie a Reef Knot"
    }
    </script>
    </body></html>'''), metadata)

    assert metadata is not None and metadata.author == "John Doe" and metadata.title == "How to Tie a Reef Knot" and metadata.pagetype == 'article'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
        <script type="application/ld+json">
            {
                "@context":"http://schema.org",
                "@type":"NewsArticle",
                "author":[
                    {
                        "@type":"Person",
                        "name":["Bill Birtles", "John Smith"]
                    }
                ]
            }
        </script>
    </script>
    </body></html>'''), metadata)
    assert metadata is not None and metadata.author == "Bill Birtles; John Smith" and metadata.pagetype == 'newsarticle'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
        <script type="application/ld+json">
        {
          "@context":"http://schema.org",
          "@id":"http://techcrunch.com/2015/03/08/apple-watch-event-live-blog",
          "about":{
            "@type":"Event",
            "startDate":"2015-03-09T13:00:00-07:00",
            "name":"Apple Spring Forward Event"
          },
        }
        </script>
    </body></html>'''), metadata)

    assert metadata is not None and metadata.title is None and metadata.sitename is None and metadata.pagetype is None

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''
    <html><body>
        <script type="application/ld+json">
        {
           "@context":"https://schema.org",
           "@graph":[
              {
                 "@type":"Article",
                 "headline":"21 Best Beaches in the World",
                 "name":"Find perfection in these places where land meets water.",
                 "datePublished":"2017-11-11T22:44:12Z",
                 "dateModified":"2017-11-11T22:44:12Z",
                 "publisher":{
                    "@type":"Organization",
                    "@id":"https://www.nationalgeographic.co.uk/",
                    "name":"National Geographic",
                    "url":"https://www.nationalgeographic.co.uk/",
                    "logo":{
                       "@type":"ImageObject",
                       "url":"https://www.nationalgeographic.co.uk/images/logo.png"
                    }
                 },
                 "author":{
                    "@type":"Person",
                    "name":{
                       "@type":"Person",
                       "name":"Kimberley Lovato"
                    }
                 },
                 "mainEntityOfPage":"https://www.nationalgeographic.co.uk/travel-and-adventure/21-best-beaches-in-the-world",
                 "image":{
                    "@type":"ImageObject",
                    "url":"https://static.nationalgeographic.co.uk/files/styles/image_3200/public/playa-del-amor-mexico.jpg?w=1900&h=1259",
                    "width":1900,
                    "height":1259,
                    "author":{
                       "@type":"Person",
                       "name":"Miguel Naranjo"
                    },
                    "contributor":{
                       "@type":"Person",
                       "name":"Miguel Naranjo"
                    },
                    "caption":"People exploring Playa del Amor in Marieta Islands, Mexico",
                    "name":"playa-del-amor-mexico.jpg",
                    "alternateName":"playa-del-amor-mexico"
                 }
              }
           ]
        }
        </script>
    </body></html>'''), metadata)

    assert metadata is not None and metadata.title == "Find perfection in these places where land meets water." and metadata.sitename == "National Geographic" and metadata.author == "Kimberley Lovato" and metadata.pagetype == 'article'

    # tests that "@type": [] in the JSON doesn't cause an exeption

    metadata = Document()
    metadata = extract_meta_json(html.fromstring(
    """
    <html>
    <body>
        <script type="application/ld+json">
        {
            "@context": "http:\/\/schema.org",
            "@type": [],
            "publishingPrinciples": "https:\/\/www.mercurynews.com\/policies-and-standards\/",
            "image": "https:\/\/www.mercurynews.com\/wp-content\/uploads\/2020\/12\/EBT-L-OSCAR-1211-18.jpg?w=150&strip=all",
            "headline": "Letters: Coddling criminals | Undermining road | Tax dollars | Recount cost | Predicting climate",
            "datePublished": "2023-01-16 16:30:41",
            "author": {
            "@type": "Person",
            "workLocation": {
                "@type": "Place"
            },
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "Journalist"
            },
            "sameAs": ["https:\/\/www.mercurynews.com\/author\/jaimoe0\/"],
            "name": "Jaime Welton"
            }
        }
        </script>
    </body>
    </html>
    """), metadata)

    assert metadata is not None

    # tests if the JSON-LD with html entities is parsed correctly
    metadata = Document()
    metadata = extract_meta_json(html.fromstring(
    """
    <html>
    <body>
        <script type="application/ld+json">
        &#13;{&#13;"@context":"http://schema.org",&#13;"@type":"WebSite",&#13;"url":"https://example.com/",&#13;"potentialAction":{&#13;"@type":"SearchAction",&#13;"target":"https://example.com/?s={search_term_string}",&#13;"query-input":"required name=search_term_string"&#13;}&#13;}&#13;
        </script>
    </body>
    </html>
    """), metadata)

    assert metadata.pagetype == 'website'

if __name__ == '__main__':
    test_json_extraction()
