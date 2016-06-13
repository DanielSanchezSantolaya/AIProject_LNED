
import csv
import ast
import json
import requests
import LNED as mlned
import string
from nltk.corpus import stopwords
import unicodedata


uri = "http://localhost:9200/_search"
name_file = "D:\\@UVA_IA\\@ AI Project\\Data\\anchors_no_textcount.tsv.gz_new.tsv"
cachedStopWords = stopwords.words("english")
windows_size = 20

#def get_articles(term, field):
#    
#    term = term.replace('/','//')
#    #Example of get 
#    """Simple Elasticsearch Query"""
#    query = json.dumps({
#        "query": {
#            "query_string": {
#                "query": term,
#                "fields": [field]
#            }
#        }
#    })
#    
#    articles = es.search('wikipedia', 'article', body=query)
#
#    articles = []
#    for result in results['hits']['hits']:
#        article = {}
#        article['wiki_page_id'] = result['_source']['wiki_page_id']
#        article['wiki_title'] = result['_source']['wiki_title']
#        article['plain_text'] = result['_source']['plain_text']
#        articles.append(article)
#    return articles

def get_articles(term, field):
    
    term = term.replace('/','//')
    #Example of get 
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "query_string": {
                "query": term,
                "fields": [field]
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)

    articles = []
    for result in results['hits']['hits']:
        article = {}
        article['wiki_page_id'] = result['_source']['wiki_page_id']
        article['wiki_title'] = result['_source']['wiki_title']
        article['plain_text'] = result['_source']['plain_text']
        if field == 'plain_text':
            if term in article['plain_text']: 
                articles.append(article)
        else:
            articles.append(article)
    return articles

def process_doc(text):
    #If Mention Document Find the context according the windows size 
    #text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    words = text.translate(None,string.punctuation).lower().split()
    words = [word for word in words if word not in cachedStopWords]
    return words

def get_context(text, word):
    text_split = text.split()
    indices = [i for i, x in enumerate(text_split) if x == word]
    end_last_index = -1
    contexts = []
    for index in indices:
        start = index - windows_size
        if start < 0:
            start = 0
        if start <= end_last_index:
            start = min(index, end_last_index)
        end = index + windows_size
        if end >= len(text_split):
            end = len(text_split) - 1
        end_last_index = end
        context = text_split[start:end]
        contexts.append(' '.join(context))
    return contexts


with open(name_file) as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
        text = line[0]
        candidates = ast.literal_eval(line[3])
        cand_ids = [x[0] for x in candidates]
        if len(candidates) > 1: #Get only ambiguos entities
            print text
            #Get candidate documents
            candidate_docs = []
            for cand in candidates:
                candidate_doc = get_articles(str(cand[0]), 'wiki_page_id')
                if len(candidate_doc) > 0:
                    candidate_docs.extend(candidate_doc)
            if len(candidate_docs) > 0:
                #Get mention documents
                mention_docs = get_articles(text, 'plain_text')
                #Process documents
                candidate_texts = []
                for candidate_doc in candidate_docs:
                    candidate_texts.append(process_doc(candidate_doc['plain_text']))
                mention_texts = []
                for mention_doc in mention_docs:
                    if mention_doc['wiki_page_id'] not in cand_ids:
                        #Get context (d_surround)
                        contexts = get_context(mention_doc['plain_text'], text)
                        for context in contexts:
                            mention_texts.append(process_doc(context))
                #Run LNED
                lned = mlned.LNED()
                lned.run(mention_texts, candidate_texts)
                lned.get_c_dist()
                lned.get_bg_dist()
                lned.get_ud_dist()
                lned.get_doc_dist()
            

    
    
            
            

            
            
            