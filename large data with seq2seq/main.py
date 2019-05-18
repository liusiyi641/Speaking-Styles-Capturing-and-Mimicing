# -*- coding: utf-8 -*-

from new_word_graph import Graph, Node
import nltk
import pandas as pd
import string
from data_cleaning import remove_http, special_characters
from frequent import initialize_gram, n_gram, merge, get_sentence_lst, check
from tfidf3 import find_pattern, tf, idf
import itertools
import pickle
from stopwords import stopWords
import copy

# finding all the patterns

doc = []
with open ('speeches.txt', 'r', encoding='utf-8-sig') as file:
    for line in file.readlines():
        line = line.split('.')
        for sent in line:
            doc.append(sent)

#print(doc[:10])

print('data cleaning')
doc = remove_http(doc)


with open('cleaned_doc.pickle', 'wb') as handle:
    pickle.dump(doc, handle, protocol=pickle.HIGHEST_PROTOCOL)

#print(data)
print(len(doc))


find_p_doc = copy.deepcopy(doc)


str_data = []
for i in doc:
    str_data.append([' '.join(i)])

#print(str_data)

graph = Graph()
#test = 'news likewise dopey mort zuckermans nydailynews'
#token = nltk.pos_tag([word.strip(string.punctuation) for word in test.split(" ")])


print('adding sentence to the graph')
for sent in str_data:
    if sent[0] != '':
        token = nltk.pos_tag([word.strip(string.punctuation) for word in sent[0].split(" ")])
        Graph.add_sentence(graph, tokens = token)

print('initializing graph')

# lst = initialize_gram(graph)
# #print(lst)

# print("get sentence lst")
# sentence_lst = get_sentence_lst(doc)

# print('finding ngrams')
# r = n_gram(doc, 5, lst, sentence_lst)
# #print(merge(r, lst))


# print('merging')
# patterns = merge(r,lst)

patterns = n_gram(doc, 8)

patterns = [temp[0].split() for temp in patterns]

print(patterns[:10])
print()
print(patterns[-1])

#print(patterns[:30])



with open('Trumps_ngram.pickle', 'wb') as handle:
    pickle.dump(patterns, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('finding patterns')



pat = find_pattern(patterns, find_p_doc)
# remove dup
print(pat[:10])
print()
print(pat[-1])




# remove duplicates

# remove ['*']
pat = [each for each in pat if each != ['*']]


#pat.sort()
#pat = list(pat or pat,_ in itertools.groupby(pat))


#pat = [['*', 'a', '*']] + pat
#print(len(pat))
#print(pat[:10])

# remove stopwords
res = []
for each_pat in pat:
    for p in each_pat:
        if p not in list(stopWords) + ['*']:
            res.append(each_pat)
            break
        

print(len(res))
 

# final patterns
with open('Trumps_patterns.pickle', 'wb') as handle:
    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    


#for each_pattern in pat:
#    res = tf(each_pattern, doc)
#    #print(res[0])
#    if res[0] >=100:
#        print()
#        print(res[2], 'appeared', res[0], 'times out of', len(doc))
