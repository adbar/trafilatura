

import os



def iterate_over_urls(urls):








'''





THESE ARE THE PARAMETERS FOR EACH ANNOTATION:


'https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html': {
    'file': 'faz.net.streaming.html',
    'author': 'Benjamin Fischer und Marcus Theurer',
    'title': 'Nutzerbasierte Abrechnung: Musik-Stars fordern neues Streaming-Modell',
    'date': '2020-01-28',
    'description': 'Die Abogebühr eines Nutzers soll nur noch unter den Künstlern verteilt werden, die er gehört hat, so das Ziel der Initiative. Dabei gehe es auch um „kulturelle Vielfalt“. Welche Chancen hat diese Forderung?',
    'categories': [],
    'tags': [],
    'with': ['„Die Liste der Künstler', 'nicht bloß um höhere Einkünfte', 'Der Wandel der Musikbranche'],
    'without': ['Etwa 100 deutsche Reisende', 'Abonnieren Sie unsere', 'Joe Kaeser deutet vage', 'Redakteur in der Wirtschaft.'],
    'comments': ['keinen Bock auf solche Buchhalter', 'Verklagt eure Labels', 'Zur Verdeutlichung ein Extrembeispiel:'],
    'license': '',
    'region': 'DE',










'''




    parameters = ["url", "file", "author", "title", "date"] 








    for url in urls:

        # it is already time to query GPT-3 for the smoothest overall syntax for this bit........


        # open the url and ask for the data.... but at any and all points allow "done" to break the iteration... ???????

        # open firefox with the url.... so call it as a shell function... import os???

        os.system("open -a Firefox " + url)

        while (x := input()) != ("done" || "Done" || "DONE"):

            for item in parameters:

                 




