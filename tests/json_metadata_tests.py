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

    metadata = extract_metadata('''<html><body><script data-rh="true" type="application/ld+json">{"@context":"http://schema.org","@type":"NewsArticle","mainEntityOfPage":{"@type":"WebPage","@id":"https://www.perthnow.com.au/news/government-defends-graphic-covid-19-ad-after-backlash-c-3376985"},"dateline":null,"publisher":{"@type":"Organization","name":"PerthNow","url":"https://www.perthnow.com.au","logo":{"@type":"ImageObject","url":"https://www.perthnow.com.au/static/publisher-logos/publisher-logo-60px-high.png","width":575,"height":60}},"keywords":["News","News","Australia","Politics","Federal Politics","News","TAS News"],"articleSection":"News","headline":"Government defends graphic Covid-19 ad after backlash","description":"A graphic COVID-19 ad showing a young woman apparently on the verge of death has prompted a backlash, but the government insists it wasn’t done lightly.","dateCreated":"2021-07-12T00:11:50.000Z","datePublished":"2021-07-12T00:11:50.000Z","dateModified":"2021-07-12T01:25:20.617Z","isAccessibleForFree":"True","articleBody":"The man tasked with co-ordinating Australia&rsquo;s Covid-19 vaccine rollout insists a confronting ad depicting a woman on the verge of death was not run lightly. The 30-second clip, depicting a woman apparently in her 20s or 30s gasping for air on a hospital bed, was filmed last year, but the federal government held off running it as no outbreak was deemed serious enough to warrant it. The government has been forced to defend the ad, reminiscent of the &ldquo;Grim Reaper&rdquo; HIV ads in the 1980s, after it prompted a backlash over claims it was too confronting. A more temperate series of ads, depicting arms on ordinary Australians with the moniker &ldquo;Arm Yourself&rdquo;, began last week, but Covid-19 taskforce commander Lieutenant General John Frewen said the escalating situation in Sydney called for a more explicit response. &ldquo;It is absolutely confronting and we didn&rsquo;t use it lightly. There was serious consideration given to whether it was required and we took expert advice,&rdquo; he told Today on Monday. &ldquo;It is confronting but leaves people in no doubt about the seriousness of getting Covid, and it seeks to have people stay home, get tested and get vaccinated as quickly as they can.&rdquo; NSW on Sunday confirmed another 77 cases, 31 of which had been in the community while infectious, and Premier Gladys Berejiklian warned she would be &ldquo;shocked&rdquo; if the number did not exceed 100 on Monday. General Frewen said the &ldquo;concerning situation&rdquo; had prompted the government to shift an additional 300,000 doses to NSW over the coming fortnight. &ldquo;The Delta variant is proving to be very difficult to contain, so we&rsquo;re working very closely with NSW authorities and standing ready to help them in any way we can,&rdquo; he said. Agriculture Minister David Littleproud said the ad was designed to shock Sydneysiders into action as the situation deteriorated. &ldquo;This is about shooting home that this is a serious situation and can get anybody. The fact we&rsquo;re actually debating this I think says to me that the campaign we&rsquo;ve approved is working,&rdquo; he said. The age of the woman in the ad has sparked controversy, with most younger Australians still ineligible to receive their vaccine. But with 11 of the 52 people in hospital across NSW under 35, Labor frontbencher Tanya Plibersek warned the Delta variant was &ldquo;hitting younger people as well&rdquo;. Labor had long demanded a national Covid-19 advertising campaign, which Ms Plibersek said was delayed as a result of the government&rsquo;s sluggish vaccine rollout. &ldquo;Perhaps the reason it&rsquo;s taken so long is if you encourage people to go and get vaccinated, you&rsquo;ve got to have enough of the vaccine available. We simply haven&rsquo;t; we&rsquo;ve been absolutely behind the eight ball in getting another vaccine for Australians,&rdquo; she told Sunrise. Labor frontbencher Chris Bowen, whose western Sydney electorate was in the grip of the outbreak, said the issue was &ldquo;not vaccine hesitancy so much, it&rsquo;s vaccine scarcity&rdquo;. He accepted there was a role for &ldquo;pointing out the consequences of not getting vaccinated&rdquo; to those that were hesitant about the jab, but said the new campaign lacked the &ldquo;creative spark&rdquo; of the Grim Reaper ads. &ldquo;That was a very tough message, a very stark message, but in a very creative way. I think the government really needs to rethink this advertising campaign from scratch; it&rsquo;s too late, and it&rsquo;s pretty low impact,&rdquo; he told ABC radio. He also dismissed the &ldquo;Arm Yourself&rdquo; campaign as &ldquo;very low energy&rdquo;. &ldquo;I don&rsquo;t think that&rsquo;s going to have any impact,&rdquo; he said.","image":[{"@type":"ImageObject","url":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-16x9-x0y444w1151h647.jpg","width":1151,"height":647},{"@type":"ImageObject","url":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-4x3-x0y336w1151h863.jpg","width":1151,"height":863}],"thumbnailUrl":"https://images.perthnow.com.au/publication/C-3376985/6c07502f73bdccd45d879356219c325574873a6d-16x9-x0y444w1151h647.jpg","url":"https://www.perthnow.com.au/news/government-defends-graphic-covid-19-ad-after-backlash-c-3376985","author":{"@type":"Organization","name":"NCA NewsWire"},"name":"Government defends graphic Covid-19 ad after backlash"}</script><span itemprop="author name">Jenny Smith</span></span></body></html>''')
    assert metadata.author == 'Jenny Smith'

    metadata = Document()
    metadata = extract_meta_json(html.fromstring('''<html><body><script type="application/ld+json" class="yoast-schema-graph">{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage","url":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/","name":"Jean S\u00e9villia : \"L'\u00c9tat fran\u00e7ais et l'\u00c9tat alg\u00e9rien doivent reconna\u00eetre les crimes commis des deux c\u00f4t\u00e9s\" - Boulevard Voltaire","datePublished":"2018-09-13T12:21:13+00:00","dateModified":"2018-09-14T12:33:14+00:00","inLanguage":"fr-FR"},{"@type":"Article","@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#article","isPartOf":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage"},"author":{"@id":"https://www.bvoltaire.fr/#/schema/person/96c0ed8f089950c46afc2044cb23e8da"},"headline":"Jean S\u00e9villia : &#8220;L&#8217;\u00c9tat fran\u00e7ais et l&#8217;\u00c9tat alg\u00e9rien doivent reconna\u00eetre les crimes commis des deux c\u00f4t\u00e9s&#8221;","datePublished":"2018-09-13T12:21:13+00:00","dateModified":"2018-09-14T12:33:14+00:00","mainEntityOfPage":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#webpage"},"publisher":{"@id":"https://www.bvoltaire.fr/#organization"},"image":{"@id":"https://www.bvoltaire.fr/jean-sevillia-letat-francais-et-letat-algerien-doivent-reconnaitre-les-crimes-commis-des-deux-cotes/#primaryimage"},"keywords":"Guerre d'Alg\u00e9rie","articleSection":"Audio,Editoriaux,Entretiens,Histoire","inLanguage":"fr-FR"},{"@type":"Person","@id":"https://www.bvoltaire.fr/#/schema/person/96c0ed8f089950c46afc2044cb23e8da","name":"Jean S\u00e9villia","image":{"@type":"ImageObject","@id":"https://www.bvoltaire.fr/#personlogo","inLanguage":"fr-FR","url":"https://secure.gravatar.com/avatar/1dd0ad5cb1fc3695880af1725477b22e?s=96&d=mm&r=g","caption":"Jean S\u00e9villia"},"description":"R\u00e9dacteur en chef adjoint au Figaro Magazine, membre du comit\u00e9 scientifique du Figaro Histoire, et auteur de biographies et d\u2019essais historiques.","sameAs":["https://www.bvoltaire.fr/"]}]}</script></body></html>'''), metadata)
    assert metadata.author == "Jean Sévillia"

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

    ### Test for potential errors
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


if __name__ == '__main__':
    test_json_extraction()
