
import pandas as pd
import string
import pickle





def remove_http(doc):
    #clean a document
    """
    Args: 
        doc  (list(string)): the corpus
    
    Output:     
        ret  (list(string)): cleaned corpus 
    
    """
    res = []
    for sent in doc:
        sent = sent.split(' ')

        # some special characters have meanings. need to discuss. 
        sent = special_characters(sent)
        
        sent = [word.lower() for word in sent if not (word[:4] == 'http' or word == '')]

        if sent != []:
            res.append(sent)
        
    return res
    

def special_characters(sent):
    # helper for data cleaning
    
    res = []
    for word in sent:
        #print(''.join([i for i in word if i.isalpha()]))
        word = ''.join([i for i in word if i.isalpha()])
        res.append(word)
    return res
    

#test = [' Miami-Dade Mayor drops sanctuary policy. Right decision. Strong! https://t.co/MtPvaDC4jM']
#print(remove_http(test))

#doc = remove_http(doc)

#with open('cleaned_doc.pickle', 'wb') as handle:
#    pickle.dump(doc, handle, protocol=pickle.HIGHEST_PROTOCOL)
