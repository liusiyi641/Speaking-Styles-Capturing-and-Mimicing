from itertools import combinations
from common import doc, doc2, doc3, minisup
import copy

class Node():
    def __init__(self, name):
        self.name = name
        self.times = 0
        self.children = []
        self.parents = []

    def __repr__(self):
        return str(self.times)

class Graph():
    def __init__(self):
        self.word_dict = {}
        self.patterns = {}
        self.pattern_list = []
        self.NB = []
        self.word = 0
    
    def add_sentence(self, sentence):
        self.word += len(sentence)
        for i in range(len(sentence)):
            #print(sentence)
            #comb = combinations(sentence, len(sentence)-i)
            #print("there is comb: ", list(comb))
            for j in self.consecutive_combinations(sentence, len(sentence)-i):
                #print("this is j: ", j)
                #print(type(comb))
                curr_node = Node(' '.join(j))
                self.add_times(curr_node)
                self.update_word_dict(curr_node)
                #print("this is the curr_node: ", curr_node.name)
                #print("children of this ", curr_node.name)
                for k in self.consecutive_combinations(j, len(j)-1):
                    temp_node = Node(' '.join(k))
                    #print("this is the temp node: ", temp_node.name)
                    if self.check_node(temp_node):
                        temp_node = self.get_node(temp_node)
                    if self.check_node(curr_node):
                        curr_node = self.get_node(curr_node)
                    self.update_word_dict(temp_node)
                    self.add_parents(temp_node, curr_node)
                    self.add_children(temp_node, curr_node)
                    #print(k)
            #print("")
            #print("different line")
            #print("")
        self.add_times(Node(''))

    def add_times(self, node):
        if node.name in self.word_dict.keys():
            self.word_dict.get(node.name).times += 1
        else:
            node.times = 1    
    
    def update_word_dict(self, node):
        if node.name not in self.word_dict.keys():
            self.word_dict.update({node.name:node})

    def check_node(self, node):
        return node.name in self.word_dict.keys()

    def get_node(self, node):
        return self.word_dict.get(node.name)

    def add_parents(self, children_node, parent_node):
        children_node.parents.append(parent_node.name)

    def add_children(self, children_node, parent_node):
        parent_node.children.append(children_node.name)

    def __repr__(self):
        return str(self.word_dict)
        #return sorted(self.word_dict.items(), key=lambda item: item[1].times)

    def find_patterns(self):
        temp_list = []
        for key, value in self.word_dict.items():
            if value.times >= minisup * self.word_dict.get('').times:#* self.word:
                self.patterns.update({key:value})
        [temp_list.append([k]) for k in self.patterns.keys()]
        self.pattern_list = temp_list
        return self.pattern_list

    def pattern_dictionary(self):
        self.patterns = {}
        for i in self.pattern_list:
            #print("this is i :", i)
            if (type(i) == list):
                self.patterns.update({i[0]:0})
            else:
                self.patterns.update({i:0})

    def negative_boarder(self):
        for key, value in self.word_dict.items():
            if key not in self.patterns:
                flag = True
                for child in value.children:
                    if child not in self.patterns:
                        flag = False
                        break
                if flag:
                    self.NB.append(key)
        return self.NB

    def consecutive_combinations(self, sentence, length):
        lst = []
        for i in range(len(sentence)):
            if (i + length <= len(sentence)):
                lst.append(sentence[i:i+length])
        return lst



def incremental_method(original_graph, increase_graph, new_graph):
    L_db = increase_graph.find_patterns()
    L_DB_plus = []
    L_DB = original_graph.pattern_list
    for s in L_DB:
        #print(s)
        if (type(s) == list):
            if (s[0] in original_graph.word_dict and s[0] in increase_graph.word_dict and original_graph.word_dict[s[0]].times + increase_graph.word_dict[s[0]].times > minisup * new_graph.word_dict.get('').times):#* (original_graph.word + increase_graph.word)):
                L_DB_plus.append(s)
        else:
            if (s in original_graph.word_dict and s in increase_graph.word_dict and original_graph.word_dict[s].times + increase_graph.word_dict[s].times > minisup * new_graph.word_dict.get('').times):#* (original_graph.word + increase_graph.word)):
                L_DB_plus.append(s)
    
    for s in L_db:
        if (type(s) == list):
            if (s[0] not in original_graph.word_dict and s[0] in original_graph.NB and original_graph.word_dict[s[0]].times + increase_graph.word_dict[s[0]].times > minisup * new_graph.word_dict.get('').times):#(original_graph.word + increase_graph.word)):
                    L_DB_plus.append(s)
        else:
            if (s not in original_graph.word_dict and s in original_graph.NB and original_graph.word_dict[s].times + increase_graph.word_dict[s[0]].times > minisup * new_graph.word_dict.get('').times):#(original_graph.word + increase_graph.word)):
                L_DB_plus.append(s)

    L_DB.sort()
    L_DB_plus.sort()
    new_graph.pattern_list = L_DB_plus
    new_graph.pattern_dictionary()
    if L_DB != L_DB_plus:
        new_graph.negative_boarder()
    else:
        new_graph.NB = original_graph.NB
    
    merge_DB = union(L_DB, original_graph.NB)
    merge_DB_plus = union(L_DB_plus, new_graph.NB)
    if (merge_DB != merge_DB_plus):
        S = L_DB_plus
        check = S

        new_graph.pattern_list = merge_DB_plus
        new_graph.pattern_dictionary()
        S = new_graph.negative_boarder()
        S.sort()
        check.sort()
        while S != check:
            #print(1)
            check = S
            new_graph.pattern_list = merge_DB_plus
            new_graph.pattern_dictionary()
            S = new_graph.negative_boarder()
            S.sort()
            check.sort()
        
        temp_pattern = []
        for i in S:
            if new_graph.word_dict[i].times >= minisup * new_graph.word_dict.get('').times and i not in temp_pattern:
                temp_pattern.append(i)
        new_graph.pattern_list = temp_pattern
        new_graph.pattern_dictionary()
        new_graph.negative_boarder()
    return new_graph.NB, new_graph.pattern_list, new_graph

def union(pattern, NB):
    S = set()
    for i in pattern:
        if (type(i) == list):
            S.add(i[0])
        else:
            S.add(i)
    for j in NB :
        if j not in S:
            S.add(j)
    S = list(S)
    ret = []
    for i in S:
        ret.append([i])
    ret.sort()
    return ret


def initialize(document):
    graph = Graph()
    for i in document:
        graph.add_sentence(i)
    graph.find_patterns()
    graph.negative_boarder()
    return graph

def adding_into_graph(document, original_graph):
    temp_graph = Graph()
    new_graph = original_graph
    for i in document:
        temp_graph.add_sentence(i)
        new_graph.add_sentence(i)
    return original_graph, temp_graph, new_graph


graph = initialize(doc)
original_graph, temp_graph, new_graph = adding_into_graph(doc2, graph)
ng_nb, ng_pl, new_graph = incremental_method(original_graph, temp_graph, new_graph)
ng_pl.sort()
print(ng_pl)
