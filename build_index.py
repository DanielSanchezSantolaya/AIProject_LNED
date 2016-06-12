import json
from elasticsearch import Elasticsearch
import requests
import time

ES_HOST = {"host" : "localhost", "port" : 9200}

INDEX_NAME = 'wikipedia'
TYPE_NAME = 'article'

ID_FIELD = 'wiki_page_id'


# create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))


# since we are running locally, use one shard and no replicas
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))



#name_file = 'test.json'
name_file = 'D:\@UVA_IA\@ AI Project\Data\wiki-2015-02-parsed-dump.json'
bulk_data = [] 
i = 0
error_file = "errors.json"
data_batch = []
with open(name_file) as f:
    for line in f:
        i += 1
        data_dict = json.loads(line)
        data_batch.extend(data_dict)
        #index
        op_dict = {
            "index": {
                "_index": INDEX_NAME, 
                "_type": TYPE_NAME, 
                "_id": data_dict[ID_FIELD]
            }
        }
        bulk_data.append(op_dict)
        bulk_data.append(data_dict)
        # bulk index the data
        if( i % 5000 == 0):
            print("bulk indexing..." + str(i))
            try:
                res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True ,request_timeout=90)
                data_batch = []                
                bulk_data = []
            except Exception as ex:
                print("Error indexing, added record to " + str(error_file))
                j = json.dumps(data_batch)
                f = open('errortest.json', 'a')
                print >> f, j
                f.close()
                data_batch = []
                bulk_data = []
                
#Create error file
#j = json.dumps(d, indent=4)
#f = open('sample.json', 'w')
#print >> f, j
#f.close()
        


#Example of get 
uri = "http://localhost:9200/_search"
term = "yamaha motor"
"""Simple Elasticsearch Query"""
query = json.dumps({
    "query": {
        "query_string": {
            "query": term,
            "fields": ["plain_text"]
        }
    }
})
response = requests.get(uri, data=query)
results = json.loads(response.text)

print 'articles recovered: '
for article in results['hits']['hits']:
    wiki_title = article['_source']['wiki_title']
    print wiki_title
