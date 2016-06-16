
import csv
import ast
import json
import requests
import LNED as mlned
import string
from nltk.corpus import stopwords
import unicodedata
import cPickle as pickle


#uri = "http://localhost:9200/_search"
uri = "http://zookst19.science.uva.nl:8005/enwiki-20150205-anchor/article/_search"
anchor_file = "D:\\@UVA_IA\\@ AI Project\\Data\\anchors_no_textcount.tsv.gz_new.tsv"
cachedStopWords = stopwords.words("english")
windows_size = 15
dataset_file = "D:\\@UVA_IA\\@ AI Project\\Data\\entity-linking-datasets\\MSNBC.json"
limit_mention_docs = 100

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

def get_articles_by_text(term):

    term = term.replace('/','//')    
    term_list = []
    for w in term.split():
        term_list.append({"term":{"plain_text":w}})
    
    query = json.dumps({
        "query":{
            "bool":{
                "must":[
                    term_list
                ],
                "must_not":[
                    {"prefix":{"wiki_title.raw":"Category:"}},
                    {"prefix":{"wiki_title.raw":"File:"}},
                    {"prefix":{"wiki_title.raw":"Template:"}}, 
                    {"prefix":{"wiki_title.raw":"Book:"}},
                ],
                "should":[]
            }
        },
        "from":0,
        "size":1000,
        "sort":[],
        "aggs":{}
    })
    
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    articles = []
    for result in results['hits']['hits']:
        article = {}
        article['wiki_page_id'] = result['_source']['wiki_page_id']
        article['wiki_title'] = result['_source']['wiki_title']
        article['plain_text'] = result['_source']['plain_text']
        if not '(disambiguation)' in article['wiki_title']:
            if term.lower() in article['plain_text'].lower(): 
                articles.append(article)
    return articles
    

def get_articles_by_wiki_page_id(wiki_page_id):
    
    #Example of get 
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "query_string": {
                "query": wiki_page_id,
                "fields": ["wiki_page_id"]
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
        articles.append(article)
    return articles

def process_doc(text):
    #text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    words = text.translate(None,string.punctuation).lower().split()
    words = [word for word in words if word not in cachedStopWords]
    return words


def get_context(text, word, init_pos = 0, is_query_doc = False):
    #text = (unicodedata.normalize('NFKD', text).encode('ascii','ignore')).lower()
    #word = (unicodedata.normalize('NFKD', word).encode('ascii','ignore')).lower()
    text = text.lower()
    word = word.lower()
    contexts = []
    pos = text.find(word, init_pos)
    windows_size = 10
    while(pos != -1):
        split_left = text[0:pos].split()
        if len(split_left) < windows_size:
            context_left = split_left
        else:
            start = len(split_left) - windows_size
            context_left = split_left[start:]
        split_right = text[pos+len(word):].split()
        if len(split_right) < windows_size:
            context_right = split_right
        else:
            end = windows_size
            context_right = split_right[0:end]
        context = ' '.join(context_left) + ' ' + word + ' ' + ' '.join(context_right)
        if is_query_doc:
            return context
        contexts.append(context)
        pos = text.find(word, pos + 1)
    return contexts

#def get_context(text, word):
#    split1 = s1.split(annotation_text)
#    for i in range(len(split1) - 1):
#        print i
#        split_left = split1[i].split()
#        split_right = split1[i+1].split()
#        if(len(split_left)) < windows_size:
#            context_left = split_left
#        else:
#            start = len(split_left) - windows_size
#            context_left = split_left[start:]
#        if(len(split_right)) < windows_size:
#            context_right = split_right
#        else:
#            end = windows_size
#            context_right = split_right[0:end]
#        context = ' '.join(context_left) + ' ' + annotation_text + ' ' + ' '.join(context_right)
#        print context

#def get_context(text, word):
#    text_split = text.split()
#    indices = [i for i, x in enumerate(text_split) if x == word]
#    end_last_index = -1
#    contexts = []
#    for index in indices:
#        start = index - windows_size
#        if start < 0:
#            start = 0
#        if start <= end_last_index:
#            start = min(index, end_last_index)
#        end = index + windows_size
#        if end >= len(text_split):
#            end = len(text_split) - 1
#        end_last_index = end
#        context = text_split[start:end]
#        contexts.append(' '.join(context))
#    return contexts


def write_line_log(line):
    with open("log.txt", "a") as myfile:
        myfile.write(line + "\n")

#Load dictionary from anchor
def load_anchors():
    anchors = {}
    with open(anchor_file) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
            text = line[0]
            candidates = ast.literal_eval(line[3])
            cand_ids = [x[0] for x in candidates]
            anchors[text] = cand_ids
    return anchors
        
try:
    print 'Loading anchors from file...'
    anchors = pickle.load(open('anchors.pkl', 'rb'))
    print 'Data loaded from anchors.pkl'
except IOError:
    print 'anchors.pkl not found, loading from csv...'
    anchors = load_anchors()
    pickle.dump(anchors,open('anchors.pkl', 'wb'),-1)    
        
        
correct_predictions = 0
total_predictions = 0
num_total_candidates = 0
num_doc = 0
results = []
with open(dataset_file) as f:
    for line in f:
        print 'DOCUMENT ' + str(num_doc)
        num_doc += 1
        sample_dict = json.loads(line)
        result = {}
        result['docId'] = sample_dict['docId']
        result['annotatedSpot'] = []
        print 'num annotations in document: ' + str(len(sample_dict['annotatedSpot']))
        for annotation in sample_dict['annotatedSpot']:
            write_line_log("--------------------------------")
            annotation_text = annotation['spot'].lower()
            annotation_text = unicodedata.normalize('NFKD', annotation_text).encode('ascii','ignore')
            print annotation_text
            #Look for the annotation at the anchor
            if annotation_text in anchors:
                cand_ids = anchors[annotation_text]
                #Add the real entity if it is not in the anchors
                if not annotation['entity'] in cand_ids:
                    cand_ids.append(annotation['entity'])
                if len(cand_ids) > 1: #Get only ambiguos entities
                    write_line_log("Annotation text: " + annotation_text)
                    #Get candidate documents
                    candidate_docs = []
                    candidate_not_founds = []
                    for cand_id in cand_ids:
                        candidate_doc = get_articles_by_wiki_page_id(str(cand_id))
                        if len(candidate_doc) > 0:
                            candidate_docs.extend(candidate_doc)
                            write_line_log("Candidate id: " + str(cand_id) + " candidate title: " + unicodedata.normalize('NFKD', candidate_doc[0]['wiki_title']).encode('ascii','ignore'))
                        else:
                            write_line_log("Candidate id not found: " + str(cand_id))
                            candidate_not_founds.append(cand_id)
                    #Remove candidate not founds
                    for cand in candidate_not_founds:
                        cand_ids.remove(cand)
                    #Check that we have at least one candidate
                    if len(candidate_docs) > 0:
                        #Get mention documents
                        mention_docs = get_articles_by_text(annotation_text)
                        #Process documents
                        candidate_processed = []
                        for candidate_doc in candidate_docs:
                            candidate_processed.append(process_doc(candidate_doc['plain_text']))
                        mention_processed = []
                        num_mentions = 0
                        for mention_doc in mention_docs:
                            if mention_doc['wiki_page_id'] not in cand_ids:
                                if num_mentions >= limit_mention_docs:
                                    break
                                #Get context (d_surround)
                                contexts = get_context(mention_doc['plain_text'], annotation_text)
                                for context in contexts:
                                    mention_processed.append(process_doc(context))
                                    num_mentions += 1
                                    if num_mentions >= limit_mention_docs:
                                        break
                                
                        write_line_log("Num candidates: " + str(len(candidate_processed)) + " Num mention docs: " + str(len(mention_processed)))
                        #RUN LNED
                        lned = mlned.LNED()
                        lned.run(mention_processed, candidate_processed)
                        lned.get_c_dist()
                        lned.get_bg_dist()
                        lned.get_ud_dist()
                        lned.get_doc_dist()
                        query_doc = get_context(sample_dict['text'], annotation_text, annotation['start'], True)
                        query_doc = process_doc(query_doc)
                        lned.run_doc_query(query_doc)
                        lned.get_doc_query_dist()
                        predicted_candidate = lned.get_max_topic_doc_query()
                        ranking = lned.get_candidate_ranking_doc_query()
                        ranking = [cand_ids[int(topic)] for topic in ranking]
                        write_line_log("Ranking generated: " + str(ranking))
                        write_line_log("Real entity: " + str(annotation['entity']))
                        total_predictions += 1
                        num_total_candidates += len(candidate_processed)
                        if ranking[0] == int(annotation['entity']):
                            correct_predictions += 1
                        print str(correct_predictions) + 'correct predictions of ' + str(total_predictions)
                        result_annotation = {}
                        result_annotation['spot'] = annotation_text
                        result_annotation['start'] = annotation['start']
                        result_annotation['end'] = annotation['end']
                        result_annotation['entity'] = ranking[0]
                        result['annotatedSpot'].append(result_annotation)
                    else:
                        write_line_log("Annotation discarded because candidate document have not been found from wikipedia: " + str(annotation_text))
                else:
                    write_line_log("Annotation discarded because no more than 1 candidate have been found: " + str(annotation_text))
            else:
                write_line_log("No candidates found in anchors file for: " + str(annotation_text))
        #save json for results
        results.append(result)
        

print 'Mean candidates per mention: ' + str(num_total_candidates/float(total_predictions))
write_line_log('Mean candidates per mention: ' + str(num_total_candidates/float(total_predictions)))
print 'Accuracy: ' + str(correct_predictions/float(total_predictions))
write_line_log('Accuracy: ' + str(correct_predictions/float(total_predictions)))

with open('results_MSNBC.json', 'a') as outfile:
    for result in results:
        json.dump(result, outfile)
        outfile.write('\n')

#with open(name_file) as tsv:
#    for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
#        text = line[0]
#        candidates = ast.literal_eval(line[3])
#        cand_ids = [x[0] for x in candidates]
#        if len(candidates) > 1: #Get only ambiguos entities
#            print text
#            #Get candidate documents
#            candidate_docs = []
#            for cand in candidates:
#                candidate_doc = get_articles(str(cand[0]), 'wiki_page_id')
#                if len(candidate_doc) > 0:
#                    candidate_docs.extend(candidate_doc)
#            if len(candidate_docs) > 0:
#                #Get mention documents
#                mention_docs = get_articles(text, 'plain_text')
#                #Process documents
#                candidate_texts = []
#                for candidate_doc in candidate_docs:
#                    candidate_texts.append(process_doc(candidate_doc['plain_text']))
#                mention_texts = []
#                for mention_doc in mention_docs:
#                    if mention_doc['wiki_page_id'] not in cand_ids:
#                        #Get context (d_surround)
#                        contexts = get_context(mention_doc['plain_text'], text)
#                        for context in contexts:
#                            mention_texts.append(process_doc(context))
#                #Run LNED
#                lned = mlned.LNED()
#                lned.run(mention_texts, candidate_texts)
#                lned.get_c_dist()
#                lned.get_bg_dist()
#                lned.get_ud_dist()
#                lned.get_doc_dist()
            

    
            
            

            
            
            