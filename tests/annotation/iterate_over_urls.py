

import os
import json

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


        # open the annotations file, "eval-data.py"
        # this means that the script must be run from the directory "trafilatura/tests" - conveniently, where it is already housed.
        f = json.load("eval-data.py")

        # check if the url is already present in the evaluation data. If so, skip it.
        if url in f: continue



        # you need to retrieve the webpage and save it in the filesystem
        # wget the file into the local directory "eval", while saving and storing its filename as a string - this will be difficult. Ask GPT!!!
        os.system("wget")





        # we re-open and re-write during every step of the iteration so that in case the annotation gets interrupted, all annotations completed that far will have been written and saved
        # and no work will have been lost


        # create a dictionary to contain the annotation's fields
        annotation = {}


        # open the current url in firefox
        os.system("open -a Firefox " + url)

        # go through all the "single value" parameters and add them as entries to the annotation dictionary
        for item in single_parameters:

            # for the current field, request input from the user while printing out that field at the command line. Then add both as an entry to the annotation.
            annotation[item] = input(item + ": ")

        # go through all the "multiple value" parameters and accept input values for them until the user returns nothing
        for item in multi_parameters:

            # for the key "item" (the current field) in the dictionary "annotation", build a list (using a functional programming syntax)
            # which requests input data from the user on a loop, until the user enters nothing.
            annotation[item] = list(iter(input, ''))
            
        # we should now have created a suitable annotation. let's print it out to be safe:

        print(annotation)

        # we did not create this dictionary in the order that the fields need to be written in the annotation file. We do a little reshuffling at the end to prepare it in right
        # format. (Python dictionaries are ordered, so we can just re-build a correct version of the dictionary.)

        final = {annotation["url"] : url}
        


        # finish up by adding, committing and pushing the annotation to GitHub, so the annotations won't be lost
            


                 




