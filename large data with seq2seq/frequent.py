from new_word_graph import Graph, Node
import nltk
import string

threshold = 30

test1 = "for example, I like you"
test2 = "for example, I want to eat"
test3 = "for example, you are an idiot"

tokens1 = nltk.pos_tag([word.strip(string.punctuation) for word in test1.split(" ")])
tokens2 = nltk.pos_tag([word.strip(string.punctuation) for word in test2.split(" ")])
tokens3 = nltk.pos_tag([word.strip(string.punctuation) for word in test3.split(" ")])

graph = Graph()
Graph.add_sentence(graph, tokens=tokens1)
Graph.add_sentence(graph, tokens=tokens2)
Graph.add_sentence(graph, tokens=tokens3)

#Graph.print_graph(graph)
#Graph.find_most_edges(graph)

doc = [['for', 'example', 'I', 'like', 'you'],
       ['for', 'example', 'I', 'want', 'to', 'eat'],
       ['for', 'example', 'you', 'are', 'an', 'idiot']]

def initialize_gram(graph):
    r = {}
    for node in graph.word_dict.keys():
      pos_dict = graph.word_dict.get(node)
      for pos in pos_dict:
        value = pos_dict.get(pos)
        if (value.freq >= threshold and value.word != "XENDX" and value.word != "XSTARTX"):
            r[value.word] = 1
    return r

def get_sentence_lst(doc):
    sentence_lst = {}
    for s_index, sentence in enumerate(doc):
        sentence_lst[s_index] = s_index
    return sentence_lst

def be_sentence(lst_sentence):
    return ' '.join(word for word in lst_sentence)

# def check(string, lst):
#     #print(string == "")
#     if string == "":
#         return True
#     else:
#         noTail = be_sentence(string[:-1])
#         noHead = be_sentence(string[1:])
#         #print(type(noTail))
#         #print("nohead: ", noHead)
#         #print("notail: ", noTail)
#         if noTail in lst and noHead in lst:
#             check(noTail,lst)
#             check(noHead,lst)
#         else:
#             #print("false here ", noTail, " ", noHead)
#             return False

def check(string, lst):
    if len(be_sentence(string)) == 0 or be_sentence(string) in lst:
        #print("here")
        return True
    # if be_sentence(string) not in lst:
    #     print("false: ", be_sentence(string))
    #     return False
    
    else:
        noTail = string[:-1]
        noHead = string[1:]

        if (be_sentence(noTail) not in lst or be_sentence(noHead) not in lst):
            return False
        #print(type(noTail))
        #print("nohead: ", noHead)
        #print("notail: ", noTail)
        return check(noTail,lst) and check(noHead,lst)


# def n_gram(doc, n, lst, sentence_lst):
#     #print(lst)
#     r = []

#     for i in range(2,n+1):
#         print("this is the ", i, " iteration")
#         for s_index, sentence in enumerate(doc):
#             if s_index in sentence_lst:
#                 for index, word in enumerate(sentence):
#                     temp_string = sentence[index:index+i]
#                     print(temp_string, " ", (index + i - 1) < len(sentence), " ", check(temp_string, lst))
#                     if (index + i - 1) < len(sentence) and check(temp_string, lst):
#                         r.append(temp_string)
#                         lst[be_sentence(temp_string)] = 1
#             else:
#                 del sentence_lst[s_index]
#     r.reverse()
#     print(r)

#     for i in lst:
#         print(i)

#     return r


def n_gram(doc, n):
    r = []
    dictionary = {}
    for i in range(1,n+1):
        print("this is the ", i, " iteration")
        for s_index, sentence in enumerate(doc):
            for index, word in enumerate(sentence):
                temp_string = sentence[index:index+i]
                if (index + i - 1) < len(sentence):
                    if (be_sentence(temp_string) in dictionary):
                        dictionary[be_sentence(temp_string)] += 1
                    else:
                        #print(be_sentence(temp_string))
                        dictionary[be_sentence(temp_string)] = 1
        for key, value in dictionary.items() :
            #print(key, value)
            #print(key, dictionary[key])
            if value >= threshold:
                r.append([key])
        dictionary = {}
    r.reverse()
    return r


def merge(r, lst):
    for element in lst:
        r.append([element])
    return r

#r = n_gram(doc, 3)
#print(r)
