from bert_serving.client import BertClient
import numpy as np
from numpy import linalg as LA


def vectorizing(sent):
    # give the bert representation of a sentence
    
    """
    Args:
        sent  list(string):  the sentence to transform
        
    Output:
        ret   list(dtype): the vector representation of the sentence
    """
    bc = BertClient()
    res = bc.encode(sent)
    return res[0]



def similarity(sent1,sent2):
    # return the cosine similarity of the two sentences representend as vectors
    
    """
    Args:
        sent1  list(dtype): vector of sent1
    
        sent2  list(dtype): vector of sent2
    
    Output:
        ret    (double): their cosine similarity
    """
    
    A_norm = LA.norm(sent1)
    B_norm = LA.norm(sent2)

    res = np.dot(sent1, sent2) / np.dot(A_norm, B_norm)

    return res
