from new_word_graph import Graph, Node
import nltk
import pandas as pd
import string
from data_cleaning import remove_http, special_characters
from frequent import initialize_gram, n_gram, merge, get_sentence_lst, check
from tfidf3 import find_pattern, tf, idf
import itertools
import pickle
import numpy as np

# using the patterns to find star sentences for training

#df = pd.read_excel('2017_01_28 - Trump Tweets.xlsx')

#print(type(df['Tweet']))

#doc = df['Tweet'].tolist()

#doc = doc[:30000]


#print('data cleaning')
#doc = remove_http(doc)

#with open('cleaned_doc.pickle', 'wb') as handle:
#    pickle.dump(doc, handle, protocol=pickle.HIGHEST_PROTOCOL)


doc = pickle.load(open('cleaned_doc.pickle', 'rb'))

pat = pickle.load(open("Trumps_patterns.pickle", "rb"))

#print(pat[:40])


input_pat = []
input_sent = []

for each_pattern in pat:
    if '*' in each_pattern:
        res = tf(each_pattern, doc)
        #print(res[0])
        #if res[3][0] != 0:
        #    print(res[3])
        #print(len(res[3]))
        #print(len(res[4]))
        assert(len(res[3]) == len(res[4]))
        input_pat = input_pat + res[3]
        input_sent = input_sent + res[4]
        #print('pat',input_pat)
        #print('sent',input_sent)
        if res[0] >=100:
            print()
            print(res[2], 'appeared', res[0], 'times out of', len(doc))
    
input_pat = [' '.join(a) for a in input_pat]
print(input_pat[:10])
print(input_sent[:10])
print(len(input_pat))
print(len(input_sent))

with open('input_pat.pickle', 'wb') as handle:
    pickle.dump(input_pat, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('input_sent.pickle', 'wb') as handle:
    pickle.dump(input_sent, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('done')
