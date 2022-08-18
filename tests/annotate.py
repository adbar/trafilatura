#!/usr/bin/python3


# This script annotates web pages for Trafilatura: (https://github.com/adbar/trafilatura).

# It uses Common Crawl (https://commoncrawl.org).

# CC features an "index" offering access to random URLs.

# By using URLs that are evenly sampled, the test data is more balanced.



# Dependencies: 
# - boto3
# 
# The script was written on MacOS.
# 
# The script requires you to have an AWS Athena account and Firefox installed.
# 
# 



# Athena

# Common Crawl's archives are hosted on Amazon Web Services. They're accessible via SQL queries, through the service "Athena".

# You need to make an AWS account and enable that service. First make an admin account, then make an IAM user.
# 
# Then install the AWS command line utility. Configure it with an access token.
#
# Boto3 works as long as you have a configured AWS package.
# 



# FIREFOX

# Download Firefox if you don't have it already: (https://www.mozilla.org/en-GB/firefox/)

# Change the settings so when Firefox opens a link, it opens it in the same tab, not a new one.

# Specific steps you will need (https://support.mozilla.org/en-US/questions/1226151):

'''
    Type about:config in the Firefox address bar
    Change the browser.link.open_newwindow.restriction value to 0
    Change the browser.link.open_newwindow value to 1

'''

# Test that the configuration worked by running this command: "open -a Firefox https://www.google.com"


# (You can run this script either with "./annotate.py" or "python3 annotate.py".)



# The script retrieves 70 URLs at random from Common Crawl, opens them in Firefox, prompts the user for data, then saves it in "eval-data.py".


# import boto3, with which you can access "AWS Athena"
import boto3


# The function for annotating is defined separately
from iterate_over_urls import iterate_over_urls


# Select the Athena client.
client = boto3.client('athena')


# Use the "start_query_execution" to execute SQL
response = client.start_query_execution(


# Required parameters:

# "QueryString", the SQL query
# "QueryExecutionContext", the database
# "ResultConfiguration": the location for the results


QueryString = 

# Copied from Common Crawl (https://github.com/commoncrawl/cc-index-table/blob/main/src/sql/examples/cc-index/random-sample-urls.sql)
"""
SELECT url FROM ccindex.ccindex TABLESAMPLE BERNOULLI (.000001) WHERE crawl = 'CC-MAIN-2022-27' AND (subset = 'warc' OR subset = 'crawldiagnostics')
"""
,



QueryExecutionContext = {

# "common crawl index"
'Database': 'ccindex',

# location where ccindex is stored
'Catalog': 'AwsDataCatalog'},



ResultConfiguration={

# my personal S3 Bucket
'OutputLocation': 's3://commoncrawltest0.001',})




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
'''

'Rows': 

[

'''

# it appears that each dictionary that is part of the list essentially has the following structure:

# the key "Data", which refers to a list, which contains a single-entry dictionary, inside which the key "VarCharValue" corresponds with the actual URLs sought:

# EXCEPT FOR THE FIRST DICTIONARY IN THE LIST, which appears to be a header or mere sample data. So, skip the first:

'''
{'Data': [{'VarCharValue': 'url'}]},
                        

'''

# so now the sample command appears to be:
# querydata["ResultSet"]["Rows"][1:]

'''
{


'Data': 


[

{

'VarCharValue': 

'https://shakespearesattic.com/collections/bonsai/products/podocarpus-artificial-bonsai-tree-with-planter-by-nearly-natural-14-inches'

}




]


},

'''


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
urls_list = query_data["ResultSet"]["Rows"][1:] 

# just to be sure this way of indexing the data works
print(urls_list)






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


