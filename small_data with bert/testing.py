import nltk
import pandas as pd
import string
from tfidf3 import find_pattern, tf, idf
import itertools
import pickle
import numpy as np
from stopwords import stopWords
from incremental import Node, Graph, incremental_method, union, initialize, adding_into_graph
from pick_and_transform import transform, break_sentence
import copy
from vectorizer_and_similarity import vectorizing, similarity
from whole_pick import pick_pattern


pat_with_vec = pickle.load(open('340_0.006_embed_lst.pickle', 'rb'))

for each in pat_with_vec:
    print(each[0])


#input_sent = 'you the fields'.split(' ')

#input_sent = ["lots of people come to china lots of people come to indonesia"]
#input_sent = ['i came i saw i conquered']
input_sent = ['china and europe and the united states']


tar_pat = pick_pattern(input_sent, pat_with_vec)

print()
print('input',input_sent)
print()
print('chosen pattern',tar_pat[0])
print()

input_sent = input_sent[0].split(' ')
#print(len(tar_pat[1]))
broken_lst = break_sentence(input_sent, len(tar_pat[1])-1)
#print(broken_lst)


possible_sent = []
for sent in broken_lst:
    possible_sent.append(transform(sent,tar_pat))

#print(possible_sent)
max_score = 0
final_res = []
for each in possible_sent:
    vec = vectorizing([' '.join(each)])
    tmp = similarity(vec,tar_pat[-1][0])
    if tmp>max_score:
        max_score = tmp
        final_res = each

print('final sentence',final_res)
