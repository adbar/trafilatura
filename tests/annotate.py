#!/usr/bin/python3
# (this shebang depends on where on your system your python installation is located. on my system, python is located at /usr/bin/python3)
# (due to the way shebangs work, you can run this script either with "./annotate.py" or "python3 annotate.py")











# to-do:

# push to github

# clean the code in VS code

# debug

# draft the iteration-over-urls loop







 







### ABOUT




# This script automates the process of annotating web pages for the Trafilatura library's test data. 

# It makes use of Common Crawl, an open source web crawling database that stores information about the web. 

# They have an "index" with which you can access URLs at random, which are evenly representative of the web at large. 

# That way, the test data is more balanced and does not favor certain kinds of web pages over others

# (which would cause the data to be incomplete, so it would be less certain if the tool were universally effective).












# SET-UP

# (TBD: Try to automate the installation dependencies.)

# This script requires Python and the package boto3; it was written for macOS; it requires you to make an Amazon Web Services account with an Identity Access Management user, with the Athena service enabled; 
# and it requires you to have Firefox installed with a certain configuration (described below). 
# 



# AWS ATHENA

# Common Crawl's archives are hosted on Amazon Web Services and are therefore accessible via SQL queries through their service "Athena".

# To access them, you need to make an AWS account and enable the service Athena.
# You actually first have to make a root/admin account, then use that to make a second IAM user.
# Then you install the AWS CLI and enter an access token into it.

# As long as you have an authenticated AWS CLI installed, you can use the pip package Boto3 to make queries through Athena.
# Boto3 is just the Python SDK for Amazon Web Services.




# FIREFOX

# Download Firefox if you don't already have it installed (https://www.mozilla.org/en-GB/firefox/)

# You need to change the settings so that when Firefox opens a link from the command line, it opens it in the current tab, not a new one - 
# that way the script won't accumulate 70 new tabs by the end of execution.

# This is the general documentation page about how to configure Firefox (https://support.mozilla.org/en-US/kb/about-config-editor-firefox),
# but this page describes the specific steps you will need: https://support.mozilla.org/en-US/questions/1226151

# Here are the steps:


'''
To make Firefox open all links in the same tab, follow these instructions:

    Type about:config in the Firefox address bar
    Bypass the security warning
    Find the browser.link.open_newwindow.restriction preference
    Double click it to change the value to 0
    Find the browser.link.open_newwindow preference
    Double click it to change the value to 1 


    NOTE: You may need to restart Firefox for the changes to take effect.
'''

# The command for opening a URL from the command line with Firefox on MacOS is:

# open -a Firefox [URL]

# (Note that the URL must be prepended with "https://" or else the shell will think it's a local file being passed.)

# Test that the above configuration worked by running the below command from the terminal a couple times:

# "open -a Firefox https://www.google.com"

# If it worked, you can now close Firefox completely. The script launches Firefox on its own.






# At that point you should be ready to execute the script. The rest of this file contains the code, with documentation.







# THE SCRIPT.



# How the script works:
# 
# 1. It retrieves 70 URLs at random from the Common Crawl archives.
# 
# 2. It opens them one at a time in Firefox. 
# 
# 3. It prompts the user for the relevant data from each web page, and saves it in the proper format.
# 
# (The annotations are written to the file "eval-data.py".)




# import the boto3 library with which you can access "AWS Athena" - a service through which you can access the Common Crawl archives.
import boto3


# For modularity, the function that handles annotating is defined separately and imported:
from iterate_over_urls import iterate_over_urls






# From boto3, select the Athena client.
client = boto3.client('athena')





# Use the "start_query_execution" to execute an Athena query.
response = client.start_query_execution(


# The required parameters to this method are "QueryString", "QueryExecutionContext", and "ResultConfiguration", explained below:

# "QueryString": the actual SQL query to be run
# "QueryExecutionContext": where you specify the database you will be querying
# "ResultConfiguration": the location for the output - an Amazon S3 bucket













# Query

QueryString = 

# This SQL query was copied from the Common Crawl documentation (url)

"""

SELECT url FROM ccindex.ccindex TABLESAMPLE BERNOULLI (.000001) WHERE crawl = 'CC-MAIN-2022-27' AND (subset = 'warc' OR subset = 'crawldiagnostics')

"""
,













# Target

QueryExecutionContext = {

# the "common crawl index"
'Database': 'ccindex',

# The "AWS Data Catalog" is general location containing databases
'Catalog': 'AwsDataCatalog'

}
,









# Results

ResultConfiguration={

# a personal S3 Bucket where the SQL query's response is stored
'OutputLocation': 's3://commoncrawltest0.001',
        
}

)








# This command returns a nested structure which containing the ID of the query. 
# 
# Use the "get_query_results" method with that ID to obtain the results.



# the query ID is under "QueryExecutionId"
queryid = response["QueryExecutionId"]




# now just pass that query ID as the sole parameter to the "get_query_results" method:
query_data = client.get_query_results(QueryExecutionId=queryid)







# This is what the query response data looks like:


'''
>>> pprint.pprint(response)
'''


# the first key is "ResponseMetadata"
'''
{'ResponseMetadata': 


{'HTTPHeaders': 


{'connection': 'keep-alive',
                                      'content-length': '7720',
                                      'content-type': 'application/x-amz-json-1.1',
                                      'date': 'Fri, 05 Aug 2022 20:09:10 GMT',
                                      'x-amzn-requestid': 'fb9852fa-cb2f-4d04-94cd-cff4f191bd89'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'fb9852fa-cb2f-4d04-94cd-cff4f191bd89',
                      'RetryAttempts': 0

},
'''


# the second key - the one that you need - is "ResultSet"


'''
'ResultSet': {
'''

# you do not need this key, "ResultSetMetadata":
'''
'ResultSetMetadata': {'ColumnInfo': [{'CaseSensitive': True,
                                                     'CatalogName': 'hive',
                                                     'Label': 'url',
                                                     'Name': 'url',
                                                     'Nullable': 'UNKNOWN',
                                                     'Precision': 2147483647,
                                                     'Scale': 0,
                                                     'SchemaName': '',
                                                     'TableName': '',
                                                     'Type': 'varchar'}]},
               
'''



# this is the second key - "Rows" - again, the one you need.
# Thus far, it is "querydata["ResultSet"]["Rows"]". 
# (That returns a list of small dictionaries.)

'Rows': 

[

# it appears that each dictionary that is part of the list essentially has the following structure:

# the key "Data", which refers to a list, which contains a single-entry dictionary, inside which the key "VarCharValue" corresponds with the actual URLs sought:

# EXCEPT FOR THE FIRST DICTIONARY IN THE LIST, which appears to be a header or mere sample data. So, skip the first:


{'Data': [{'VarCharValue': 'url'}]},
                        



# so now the sample command appears to be:
# querydata["ResultSet"]["Rows"][1:]


{


'Data': 


[

{

'VarCharValue': 

'https://shakespearesattic.com/collections/bonsai/products/podocarpus-artificial-bonsai-tree-with-planter-by-nearly-natural-14-inches'

}




]


},




# So, hopefully at this point you will have a list of dictionaries, and for each element in the list, just index it with "element["Data"][0]["VarCharValue"]

# recall: the 0 is just to access/index the only, exclusive element of the list the actual URL entry is nested inside - that element is a dictionary, so then you have to use the key "VarCharValue".

# I honestly think this is terribly designed and not user-friendly, but it is what it is and has to be used this way, for the time being.

# this is just a SAMPLE of the data, i redacted probably 40-50 lines (as this bernoulli value (0.000001) returns usually about 70 results).
'''
                        {'Data': [{'VarCharValue': 'https://www.jeremysavel-photographe.com/BOUTIQUE-EN-LIGNE-ACHAT-TIRAGE-.RB/s341841p/Photo_a_poster'}]},
                        {'Data': [{'VarCharValue': 'https://meyer-imports.typepad.com/meyer_folder/2010/11/found-on-etsy-mini-version-glass-glitter-christmas-light-bulbs.html'}]},
                        {'Data': [{'VarCharValue': 'https://www.ictpower.it/guide/configurare-e-gestire-azure-dns.htm'}]},
                        {'Data': [{'VarCharValue': 'http://asexbox.net/2014/11/'}]},
                        {'Data': [{'VarCharValue': 'https://truelinkps.ca/8269lsobm58845xs684482'}]},
                        {'Data': [{'VarCharValue': 'https://www.niaid.nih.gov/research/resources?amp%3Bf%5B1%5D=field_disease%3A93&f%5B0%5D=discipline%3A43&f%5B1%5D=discipline%3A44&f%5B2%5D=discipline%3A229&f%5B3%5D=disease%3A83&f%5B4%5D=disease%3A88&f%5B5%5D=disease%3A97&f%5B6%5D=disease%3A102&f%5B7%5D=disease%3A107&f%5B8%5D=stage%3A264&f%5B9%5D=type%3A272&f%5B10%5D=type%3A274'}]},
                        {'Data': [{'VarCharValue': 'https://solutions-entreprise.developpez.com/page/116'}]},
                        {'Data': [{'VarCharValue': 'https://www.argon-verlag.de/hoerbuch/eggers-der-circle-2006018/'}]},
                        {'Data': [{'VarCharValue': 'https://ffw-prackendorf.de/2021_05_30/30052.html'}]}]},
 'UpdateCount': 0}




'''























# Now that that's cleared up, hopefully it should be clear that you just have to access that list of URLs, and then index each element of that list appropriately. So that means the following commands:








# this gets the actual list of URL entries from the general data structure:
urls_list = querydata["ResultSet"]["Rows"][1:] 








# and this is the series of keys to get the url from the list of url elements. We define a function just for brevity:
def extract_url_string(element):
   return element["Data"][0]["VarCharValue"] 







# and this pulls out all the actual URLs from that list of dictionaries:
urls = [extract_url_string(element) for element in urls_list]












# now we should hopefully have our list of URLs. To be safe and make sure it worked, let's print them out:
print(urls)





'''


'https://nurmeinstandpunkt.wordpress.com/2020/01/23/blogposting-01-23-2020/': {
    'file': 'nurmeinstandpunkt.wordpress.com.blogposting.html',
    'author': 'Christian Spließ',
    'title': 'Blogposting 01/23/2020',
    'date': '2020-01-23',
    'description': 'Presseförderung: Studie zweifelt an Stütze vom Staat via Horizont Gewalt im Netz &#8211; Schuldzuweisung statt Opferschutz via netzpolitik.org Künstliche Intelligenz &#8211; EU erwägt Verbot von Ge…',
    'categories': ['Allgemeines'],
    'tags': [],
    'with': ['Presseförderung: Studie zweifelt an Stütze vom Staat', 'via netzpolitik.org', 'via t3n News'],
    'without': ['Hier könnte Ihre Meinung stehen', 'Ein Fehler ist aufgetaucht', 'Es heißt SOCIAL Media'],
    'comments': [],
    'license': 'CC BY-NC-SA 2.0 DE',
    'region': 'DE',
},



this is an example of a sample annotation, many of these fields are optional and can be left blank or omitted altogether, but this is a complete list.






'''






iterate_over_urls(urls)


