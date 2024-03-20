#!/usr/bin/python3

# boto3 is the Python SDK for AWS
import boto3

# This function is defined separately
from iterate_over_urls import iterate_over_urls

from time import sleep

# Athena client
client = boto3.client("athena")

# Copied from Common Crawl (https://github.com/commoncrawl/cc-index-table/blob/main/src/sql/examples/cc-index/random-sample-urls.sql)
sql_query = "SELECT url FROM ccindex.ccindex TABLESAMPLE BERNOULLI (.000001) WHERE crawl = 'CC-MAIN-2022-27' AND (subset = 'warc' OR subset = 'crawldiagnostics')"

# "common crawl index" database
database = {'Database': 'ccindex', 'Catalog': 'AwsDataCatalog'}

# Personal S3 Bucket
location = {'OutputLocation': 's3://commoncrawltest0.001'}

# Pass SQL query
response = client.start_query_execution(QueryString = sql_query, QueryExecutionContext = database, ResultConfiguration=location)

# Get the ID
query_id = response["QueryExecutionId"]

status = client.get_query_execution(QueryExecutionId=query_id)["QueryExecution"]["Status"]["State"]

while (status != "SUCCEEDED"):
    sleep(0.5)
    status = client.get_query_execution(QueryExecutionId=query_id)["QueryExecution"]["Status"]["State"]
    print(status)

print(status)

# this part is slightly tricky - when you send the query, it responds with a "query object" which is assigned an ID. But the query itself my go on executing for a while.
# So you actually have to write a function that waits and checks for when the query has attained the status "completed" - before retrieving its results.

# this is a very crude solution, but simple. AWS doesn't provide a simple way to trigger when the query is done. But these are small queries that take under 10 seconds. So,
# we just wait 10 seconds at this point.



# Get the ID and the data
query_data = client.get_query_results(QueryExecutionId=query_id)

# index the data to obtain the urls

urls_list = query_data["ResultSet"]["Rows"][1:]

urls = [element["Data"][0]["VarCharValue"] for element in urls_list]

print(urls)

iterate_over_urls(urls)








# 
# 
# Sample query response data
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
