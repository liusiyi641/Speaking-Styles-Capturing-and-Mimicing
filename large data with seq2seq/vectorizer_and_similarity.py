from bert_serving.client import BertClient
import numpy as np
from numpy import linalg as LA


def vectorizing(sent):
    # same
    bc = BertClient()
    res = bc.encode(sent)
    return res[0]



def similarity(sent1,sent2):
    A_norm = LA.norm(sent1)
    B_norm = LA.norm(sent2)

    res = np.dot(sent1, sent2) / np.dot(A_norm, B_norm)

    return res
