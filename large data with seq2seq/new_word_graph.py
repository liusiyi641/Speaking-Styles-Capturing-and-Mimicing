import math
import os
import random
import sys
import time
import logging

import pickle

import numpy as np
from six.moves import xrange  # pylint: disable=redefined-builtin

import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import nltk
from operator import itemgetter
import networkx as nx
import pylab
import matplotlib.pyplot as plt
highest_freq_list = []
hot_words = []


class Node:
  def __init__(self, tuple, prev_word):
    self.word = tuple[0]
    self.pos = tuple[1]
    self.next = {}
    self.nextList = []
    self.prev = [prev_word]
    self.prev = set(self.prev)
    self.freq = 1

  def add_next(self, word):
    if word in self.next.keys():
      self.next[word] += 1
    else:
      self.next.update({word: 1})
      
  def add_nextWord(self, word, frequence):
    for i in self.nextList:
      if (word == i[0]):
        i[1]+=1
        return
    self.nextList.append([word,frequence])

  def add_prev(self, prev_word):
    self.prev.add(prev_word)
    self.prev = set(self.prev)


class Graph:
  counter = 0

  def __init__(self):
    self.word_dict = {}

  def update_word_dict(self, node):
    if node.word in self.word_dict.keys():
      node_list = self.word_dict.get(node.word)
      node_list.append(node.word)
      #print(node_list)
      #print(node_list)
      self.word_dict.update({node.word: node_list})
    else:
      self.word_dict.update({node.word: [node]})

  def check_word_dict(self, word, pos):
    if word in self.word_dict.keys():
      pos_dict = self.word_dict.get(word)
      if pos in pos_dict.keys():
        #print(pos)
        #print(pos_dict.get(pos))
        return pos_dict.get(pos)
      return "No pos"
    return "No word"

  def add_sentence(self, tokens):
    tokens.insert(0, ('XSTARTX', 'X'))
    tokens.insert(len(tokens), ('XENDX', 'X'))
    prev_word = None
    prev_node = None
    for pair in tokens:
      if pair[1] == 'CD':
        continue
      curr_node = self.check_word_dict(pair[0], pair[1])
      if curr_node == "No word":
        curr_node = Node(pair, prev_word)
        self.word_dict.update({curr_node.word: {curr_node.pos: curr_node}})
      elif curr_node == "No pos":
        curr_node = Node(pair, prev_word)
        node_dict = self.word_dict.get(curr_node.word)
        node_dict.update({curr_node.pos: curr_node})
        self.word_dict.update({curr_node.word: node_dict})
      else:
        curr_node.freq += 1
        curr_node.add_prev(prev_word)
        #print(curr_node.word, 'here')
        # changed here
        # append node to our freq list if its freq is higher than a threshold
        # still have a problem that we could have a lot of
        # meaningless words like "the, to" that everyone uses a lot
        # A potential way to solve is to check if the word is top 100 used words
        # and check its pos before adding
        if curr_node.freq >= 2:
            highest_freq_list.append(curr_node)    
      if prev_node != None:
        prev_node.add_next(curr_node.word)
        prev_node.add_nextWord(curr_node.word+"_"+curr_node.pos, curr_node.freq)
      prev_word = curr_node.word
      prev_node = curr_node
      

  def print_graph(self):
    print(self.word_dict.keys())
    for node in self.word_dict.keys():
      print("NODE " + node)
      pos_dict = self.word_dict.get(node)
      for pos in pos_dict:
        value = pos_dict.get(pos)
        print(value.word,  value.pos, str(value.freq))
        print(value.prev)
        print(value.next)
        print("number of incoming and outgoing edges", len(value.prev) + len(value.next))
  def draw_graph(self):
    g = nx.DiGraph()
    for node in self.word_dict.keys():
      pos_dict = self.word_dict.get(node)
      for pos in pos_dict:
        value = pos_dict.get(pos)
        print(value.nextList, value.word)
        current_word = value.word+"_"+value.pos
        g.add_nodes_from([current_word])
        for i in value.nextList:
            #print(i)
            g.add_edge(current_word, i[0], w=i[1])
        #next_word = value.next.word+'_'+value.next.pos
        
##        for i in value.next:
##            g.add_edge(current_word, i, weight=value.next[i])
        #g.add_edge(current_word, next_word)
#    nx.draw(g,with_labels=True)
    ppos = nx.spring_layout(g)
#    pylab.figure(1)
    labels = nx.get_edge_attributes(g,'weight')
    nx.draw(g,ppos,with_labels=True)
    #nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
    
    #nx.draw_networkx_edge_labels(g,ppos)
    
##    edges=nx.get_node_attributes(g,'pos')
##    nx.draw(g,edges)
##    labels = nx.get_edge_attributes(g,'weight')
##    nx.draw_networkx_edge_labels(g, edges, edge_labels=labels)
    plt.draw()
    plt.show()       



  def find_most_edges(self):
      res = ""
      res_node = Node((0,0),None)
      for node in self.word_dict.keys():
          #print("NODE",  node)
          pos_dict = self.word_dict.get(node)
          for pos in pos_dict:
              value = pos_dict.get(pos)
              #print(value.word + value.pos + str(value.freq))
              #print(value.prev)
              #print(value.next)
              #print("number of incoming and outgoing edges", len(value.prev) + len(value.next))
              #print(max(value.next, key=value.next.get))
              if value.next != {}:
                  hotword = max(value.next, key=value.next.get)
                  if value.next[hotword] >=2 and value.word!="XSTARTX" and hotword!= "XENDX": #threshold
                      #print('hot words', max(value.next, key=value.next.get))
                      hot_words.append((node,hotword))
                      #print((value.prev))
                      hot = Node((node+hotword,'PH'), None)
                      
                      res = node+hotword
                      hot.freq = value.next[hotword]
                      #print(value.word)
                      for prev in value.prev:
                          hot.add_prev(prev)
                          prev_pos_dict = self.word_dict.get(prev)
                          #print(value.prev)
                          for prev_pos in prev_pos_dict:
                              prev_node = prev_pos_dict.get(prev_pos)
                              prev_node.add_next(res)
                              prev_node.add_nextWord(res+"_"+"PH", value.next[hotword])
                              
                          
                         
                      
                      
                      hotword_pos_dict = self.word_dict.get(hotword)
                      for hot_pos in hotword_pos_dict:
                          hot_node = hotword_pos_dict.get(hot_pos)
                          #print(value.nextList)
                          for i in value.nextList:
                            if (i[0] == hotword+"_"+hot_pos):
                              value.nextList.remove(i)
#                          value.nextList.remove([hotword+"_"+hot_pos,])

                          

                          for nxt in hot_node.next.keys():

                              hot.add_next(nxt)
                              
                              hot_nxt_pos_dict = self.word_dict.get(nxt)
                              
                              for nxt_pos in hot_nxt_pos_dict:
                                  nxt_node = hot_nxt_pos_dict.get(nxt_pos)
                                  nxt_node.add_prev(node+hotword)
                                  hot.add_nextWord(nxt+"_"+nxt_pos, nxt_node.freq)
                      del value.next[hotword]
                      
                      res_node = hot
                                  
      self.word_dict.update({res: {"PH": res_node}})

                          
                              
              

                  
             



# test1 = "I eat a lot."
# test2 =  "hate you."
# test3 = "for example, you are an idiot"
# test4 = "for example, I like banana"
# test5 = "then, for example, he likes apple"
# tokens1 = nltk.pos_tag([word.strip(string.punctuation) for word in test1.split(" ")])
# tokens2 = nltk.pos_tag([word.strip(string.punctuation) for word in test2.split(" ")])
# tokens3 = nltk.pos_tag([word.strip(string.punctuation) for word in test3.split(" ")])
# tokens4 = nltk.pos_tag([word.strip(string.punctuation) for word in test4.split(" ")])
# tokens5 = nltk.pos_tag([word.strip(string.punctuation) for word in test5.split(" ")])

# graph = Graph()
# Graph.add_sentence(graph, tokens=tokens1)
# Graph.add_sentence(graph, tokens=tokens2)
# Graph.add_sentence(graph, tokens=tokens3)
# Graph.add_sentence(graph, tokens=tokens4)
# Graph.add_sentence(graph, tokens=tokens5)
# #Graph.print_graph(graph)
# Graph.find_most_edges(graph)
# #Graph.print_graph(graph)
# graph.draw_graph()

# #print(hot_words)
