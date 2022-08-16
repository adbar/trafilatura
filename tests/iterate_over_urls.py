

import os

def iterate_over_urls(urls):

# These are the parameters for each annotation:


# 'https://www.faz.net/aktuell/wirtschaft/nutzerbasierte-abrechnung-musik-stars-fordern-neues-streaming-modell-16604622.html': {
    # 'file': 'faz.net.streaming.html',
    # 'author': 'Benjamin Fischer und Marcus Theurer',
    # 'title': 'Nutzerbasierte Abrechnung: Musik-Stars fordern neues Streaming-Modell',
    # 'date': '2020-01-28',
    # 'description': 'Die Abogebühr eines Nutzers soll nur noch unter den Künstlern verteilt werden, die er gehört hat, so das Ziel der Initiative. Dabei gehe es auch um „kulturelle Vielfalt“. Welche Chancen hat diese Forderung?',
    # 'categories': [],
    # 'tags': [],
    # 'with': ['„Die Liste der Künstler', 'nicht bloß um höhere Einkünfte', 'Der Wandel der Musikbranche'],
    # 'without': ['Etwa 100 deutsche Reisende', 'Abonnieren Sie unsere', 'Joe Kaeser deutet vage', 'Redakteur in der Wirtschaft.'],
    # 'comments': ['keinen Bock auf solche Buchhalter', 'Verklagt eure Labels', 'Zur Verdeutlichung ein Extrembeispiel:'],
    # 'license': '',
    # 'region': 'DE',


    single_parameters = ["url", "file", "author", "title", "date", "description", "license", "region"]
    multi_parameters = ["categories", "tags", "with", "without", "comments"]




    # for each url
    for url in urls:


        annotation = {}


        # open that url in firefox
        os.system("open -a Firefox " + url)


            for item in single_parameters:
                annotation[item] = input(item)

            for item in multi_parameters:

                annotation[item] = [x while x := input(item)]



                 




