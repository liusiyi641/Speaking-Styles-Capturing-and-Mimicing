import nltk
import pandas as pd
import string
from tfidf3 import find_pattern, tf, idf
import itertools
import pickle
import numpy as np
from stopwords import stopWords
from incremental import Node, Graph, incremental_method, union, initialize, adding_into_graph
from pick_and_transform import pick_pattern, transform, break_sentence
import copy
from vectorizer_and_similarity import vectorizing, similarity


doc = pickle.load(open('cleaned_doc.pickle', 'rb'))

print(len(doc))
#print(doc[:300])

doc = [tmp for tmp in doc if len(tmp)<=15]

find_p_doc = copy.deepcopy(doc[:1700])
test_doc = doc[:1700]
#print(test_doc)
doc1 = doc[:100]
doc2 = doc[100:170]
doc3 = doc[170:340]
doc4 = doc[340:850]
doc5 = doc[850:1700]
##doc6 = doc[1700:3400]
##doc7 = doc[3400:6800]
##
####doc1 = doc[:10]
##doc2 = doc[10:17]
##doc3 = doc[17:34]
##doc4 = doc[34:85]
##doc5 = doc[85:170]



#print(doc)
graph = initialize(doc1)
#print(graph.pattern_list)
print("shit")
original_graph, temp_graph, new_graph = adding_into_graph(doc2, graph)
ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
print("shit")
original_graph = new_graph
original_graph, temp_graph, new_graph = adding_into_graph(doc3, graph)
ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
print("shit")
original_graph = new_graph
original_graph, temp_graph, new_graph = adding_into_graph(doc4, graph)
ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
print("shit")
original_graph = new_graph
original_graph, temp_graph, new_graph = adding_into_graph(doc5, graph)
ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
print("shit")

##original_graph = new_graph
##original_graph, temp_graph, new_graph = adding_into_graph(doc6, graph)
##ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
##print("shit")
##original_graph = new_graph
##original_graph, temp_graph, new_graph = adding_into_graph(doc7, graph)
##ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
##print("shit")
##


ng_pl.sort()
#print("fuck you!")
print(ng_pl[:10])
print('ngram',len(ng_pl))


##with open('1000_0.005_ngram.pickle', 'wb') as handle:
##    pickle.dump(ng_pl, handle, protocol=pickle.HIGHEST_PROTOCOL)


##ng_pl = pickle.load(open('small_trump_ngram.pickle', 'rb'))

#print(ng_pl)


# make it to same format
patterns = [temp.split(' ') for temp in ng_pl] 
patterns.sort(key=len, reverse=True)
#print(patterns[:10])



#print(doc[:10])
pat = find_pattern(patterns, find_p_doc)
#print(doc[:10])
print(pat[:10])
print(len(pat))

# remove ['*']
pat = [each for each in pat if each != ['*']]

# remove stop_words
res = []
for each_pat in pat:
    for p in each_pat:
        if p not in list(stopWords) + ['*']:
            res.append(each_pat)
            break

res = [tmp for tmp in res if '*' in tmp]



#print(res[:20])
print(len(res))
print('pat',res)

with open('1700_0.006_pat.pickle', 'wb') as handle:
    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)


##res = pickle.load(open('1000_0.005_pat.pickle', 'rb'))

# get all vectors for each pattern
pat_with_vec = []

#del res[3]
#del res[4]

#print(test_doc)

# find all the vectors for the pattern
for each_pattern in res:
    #print(each_pattern)
    #print(doc[:300])
    res = tf(each_pattern, test_doc)
    if res[-1] != 'invalid pat':
        pat_with_vec.append((res[2], res[3], res[4],res[5]))
    #print(res[2])

    #print(res[3])
    #print(res[4])

##with open('small_embeddings_lst.pickle', 'wb') as handle:
##    pickle.dump(pat_with_vec, handle, protocol=pickle.HIGHEST_PROTOCOL)


##with open('small_trump_pat.pickle', 'wb') as handle:
##    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)
##    
##
with open('1700_0.006_embed_lst.pickle', 'wb') as handle:
    pickle.dump(pat_with_vec, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(len(pat_with_vec))



input_sent = 'im rich'.split(' ')

tar_pat = pick_pattern(input_sent, pat_with_vec)

print()
print('input',input_sent)
print()
print('chosen pattern',tar_pat[0])
print()


broken_lst = break_sentence(input_sent, len(tar_pat[1])-1)

possible_sent = []
for sent in broken_lst:
    possible_sent.append(transform(sent,tar_pat))


max_score = 0
final_res = []
for each in possible_sent:
    vec = vectorizing(each)
    tmp = similarity(vec,tar_pat[-1][0])
    if tmp>max_score:
        max_score = tmp
        final_res = each

print('final sentence',final_res)
            





  


