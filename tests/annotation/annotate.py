#!/usr/bin/python3

# This script annotates web pages for Trafilatura: (https://github.com/adbar/trafilatura).

# See "annotate_info.py" for more info

# boto3 is the Python SDK for AWS
import boto3

# The function for annotation is defined separately
from iterate_over_urls import iterate_over_urls

# Athena client.
client = boto3.client("athena")

# Copied from Common Crawl (https://github.com/commoncrawl/cc-index-table/blob/main/src/sql/examples/cc-index/random-sample-urls.sql)
sql_query = "SELECT url FROM ccindex.ccindex TABLESAMPLE BERNOULLI (.000001) WHERE crawl = 'CC-MAIN-2022-27' AND (subset = 'warc' OR subset = 'crawldiagnostics')"

# the database "common crawl index" in the "AWS Data Catalog"
database = {'Database': 'ccindex', 'Catalog': 'AwsDataCatalog'}

# my personal S3 Bucket
location = {'OutputLocation': 's3://commoncrawltest0.001'}

# the "start_query_execution" method is how you pass the SQL query
response = client.start_query_execution(
QueryString = sql_query,
QueryExecutionContext = database,
ResultConfiguration=location
)

# key "QueryExecutionId"
queryid = response["QueryExecutionId"]

# Use "get_query_results"
query_data = client.get_query_results(QueryExecutionId=queryid)

# Here we document the query response, to understand how to index it properly.

# The key that you need is "ResultSet", then "Rows". That returns a list of dictionaries containing the URLs.

# Discard the first element (it's a header). Iterate over the list, indexing each dictionary with "Data", "[0]" (to unwrap a trivial list), and finally "VarCharValue" to return the URL.

# For the record, this seems terribly designed.

# This is what the query response data looks like. 
# 
#   {'ResponseMetadata': 
#       {'HTTPHeaders': 
#           {'connection': 'keep-alive',
#            'content-length': '7720',
#            'content-type': 'application/x-amz-json-1.1',
#            'date': 'Fri, 05 Aug 2022 20:09:10 GMT',
#            'x-amzn-requestid': 'fb9852fa-cb2f-4d04-94cd-cff4f191bd89'},
#        'HTTPStatusCode': 200,
#        'RequestId': 'fb9852fa-cb2f-4d04-94cd-cff4f191bd89',
#        'RetryAttempts': 0
#   },
#   'ResultSet': {
#       'ResultSetMetadata': 
#           {'ColumnInfo': [{'CaseSensitive': True,
#                           'CatalogName': 'hive',
#                           'Label': 'url',
#                           'Name': 'url',
#                           'Nullable': 'UNKNOWN',
#                           'Precision': 2147483647,
#                           'Scale': 0,
#                           'SchemaName': '',
#                           'TableName': '',
#                           'Type': 'varchar'}]},
#       'Rows': 
#           [{'Data': [{'VarCharValue': 'url'}]},
#           {'Data': [{'VarCharValue': 'https://shakespearesattic.com/collections/bonsai/products/podocarpus-artificial-bonsai-tree-with-planter-by-nearly-natural-14-inches'}
#           ... (lines redacted for brevity)
#           {'Data': [{'VarCharValue': 'https://ffw-prackendorf.de/2021_05_30/30052.html'}]}]},
#   'UpdateCount': 0}

#           



# in summary: access the "rows" from the "result set", but chop off the first one
# querydata["ResultSet"]["Rows"][1:]
# iterate and index with "element["Data"][0]["VarCharValue"]



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


