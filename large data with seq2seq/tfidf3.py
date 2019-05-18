from vectorizer_and_similarity import vectorizing, similarity
import numpy as np

#global vec
#vec = np.zeros(192)
# used for tensorflow method

def tf(pattern, document):
    # basically the difference is that we are not doing anything vectors here
    #
    # this function is used to find all the star sentences
    
    """
    Args:
        pattern  (list(list)): the pattern
        
        document (list(list)): the corpus
        
    Output:
        ret      (list): a list containing a lot of things about this pattern
                         in the form of [appear_times, appear_times/len(document), pattern, star_lst, sent_lst]
                         so basically it's used to find all the star sentences
    
    """

    
    appear_times = 0
    star_lst = []
    sent_lst = []
    for sent in document:
        if best_rec(pattern, sent, 0,0):
            appear_times +=1
            star = find_star2(sent,pattern)
            #print('sent', sent)
            #print('star', star)
            #print('pat', pattern)
            #print(pattern)
            if star != [[]] and star != []:
                #print(star, 'star')
                #print(star, 'star')
                #print(star)
               # print(star)
               # print(sent)
                #print(pattern)
                print('pat',pattern)
                print('star',star)
                print('sent', sent)
                sentence = [' '.join(a)for a in star if a!=[]]
                if sentence != []:

                    star_lst.append((sentence))
                    sent_lst.append(' '.join(sent))
                #print('star', star_lst)
                #print('sent', sent_lst)
               # print('pat', pattern)
                #print(star_lst)

    # some star are ''
    #len(max(star_lst,key=len))

    # delete patterns that some star sentences are ''
##    for i in range(len(star_lst)-1):
##        if len(star_lst[i]) != len(star_lst[i+1]):
##            return [0,0,0,0,0,'invalid pat']

    #print(pattern, 'appeard', appear_times, 'out of', len(document))
    return [appear_times, appear_times/len(document), pattern, star_lst, sent_lst]


def idf(number_of_doc, doc_list, pattern):
    # not used
    count = 0
    for document in doc_list:
        for sent in document:
            if best_rec(pattern, sent, 0,0):
                count +=1
                break

    return number_of_doc / count
    


def best_rec(pattern, sent, cur_pat, cur_sent):
    # same as before
    # helper that finds if sent contains pattern

    if cur_pat == len(pattern):
        return True
    if cur_sent == len(sent):
        return False
    if pattern[cur_pat] == "*":
        if cur_pat == len(pattern)-1:
            return True
        
        sub_sent=sent[cur_sent:]
        for i in range(len(sub_sent)):
            #print(sub_sent[i])
            #print(pattern[cur_pat+1])
            if sub_sent[i] == pattern[cur_pat+1]:
                #print(cur_pat+2, cur_sent+i+1)
                return best_rec(pattern, sent, cur_pat+2, cur_sent+i+1)

        return False
    
    else:
        if pattern[cur_pat] != sent[cur_sent]:
            #print('f')
            if cur_pat !=0:
                return best_rec(pattern, sent, cur_pat-1, cur_sent+1)
            elif cur_pat==0 and cur_sent==0:
                return False

        else:
            return best_rec(pattern, sent, cur_pat+1, cur_sent+1)
        

def find_star(sent,pattern):
    # not used
    res = []
    sent_index = 0
    for i in range(len(pattern)):
        if pattern[i] == '*':
            if len(pattern)-1 == i:
                return res.append(sent[i:])

            else:
                for j in range(len(sent)):
                    if sent[j] == pattern[i+1] and i<j:
                        
                        res.append(sent[sent_index:j])
                        sent_index = j+1
        else:
            sent_index +=1
     
    return res

def find_star2(sent, pattern):
    # same as before, used for finding the star parts in this sentence
    
    
    #print(sent)
    #print(pattern)
    res = []
    #subsent = sent
    start= 0
    #end = 0
    #print(pattern)
    while start<len(pattern) and pattern[start] != '*':
        start +=1
    sent = sent[start:]
    pattern = pattern[start:]
#    print(sent)
#    print(start)
    for i in range(len(pattern)-1):
        if pattern[i] == '*' and pattern[i+1] != '*':
            
            subpat = []
            for each in pattern[i+1:]:
                if each == '*':
                    break
                subpat.append(each)
                
                
            for j in range(start,len(sent)-len(subpat)):
                if sent[j:j+len(subpat)] == subpat:
                    #print(start)
                    #print(i)
                    #print(j)
                    res.append(sent[start:j])
                    start = j+1
                    break
        elif pattern[i] !='*' and pattern[i+1] != '*':
            start +=1

    if pattern[-1] == '*':
        if len(pattern)==1:
            res.append(sent)
        else:
            res.append(sent[start:])

    return res
                    
            





##
##
##pattern = ['for', 'example', '*', 'I', '*', 'nlp']
##pattern1 = ['for', 'example', '*', 'I']
##
##sent = ['for', 'example', 'blah', 'blahblah', 'I', 'love', 'nlp']
##
###print(best_rec(pattern, sent, 0,0))
##
##
##doc = [['for', 'example', 'blah', 'blahblah', 'I', 'love', 'nlp'],
##       ['for', 'example', 'I'],
##       ['for', 'example', 'blahblah', 'I']]

#print(tf(pattern, doc))
#print()
#print(tf(pattern1, doc))
#print()
#print(idf(1,[doc], pattern1))

#pattern =['*', 'a', '*', 'at', 'trumplasvegas', 'with', '*', 'for', '*', 'day', 'weekend', 'sure', 'knows', 'how', 'to', 'make', 'a', 'nice', 'hotel']
#sent = ['nicolastoscano', 'booked', 'a', 'corner', 'suite', 'at', 'trumplasvegas', 'with', 'miketokes', 'for', 'memorial', 'day', 'weekend', 'sure', 'knows', 'how', 'to', 'make', 'a', 'nice', 'hotel']#pattern = ['*', 'a', '*', 'at', 'trumplasvegas', 'with', '*', 'for', '*', 'day', 'weekend']
#pattern1 = ['*', 'example', 'haha']
#pattern2 = ['lalala', 'for', '*']
#print(find_star2(sent,pattern))
#print(' '.join(find_star2(sent,pattern)))
#print(find_star(sent,pattern1))
#print(find_star(sent,pattern2))



def pattern_rec(ngram, sent):
    # return all index of found ngram
    res = []
    for i in range(len(sent)):
        if ngram[0] == sent[i]:
            #print(ngram)
            #print(sent)
            if ngram == sent[i:len(ngram)+i]:
                #print('here')
                res.append(i)

    if res !=[]:
        return res
        
    return [-1]
        

def find_pattern(freq_lst, document):
    #same as before
    # find all the patterns given ngram list
    
    
    pattern_lst = []
    ret = []
    index_lst =[]
    for sent in document:
        # if the ngram list is sorted by length
        ngram_lst = []
        for ngram in freq_lst:
            # delete all unigrams 
            #print(ngram)

            if ' ' not in ' '.join(ngram):
                
                break
            #print('here')
            index = pattern_rec(ngram, sent)
            if index[0] != -1:
                for i in index:
                    ngram_lst.append([i,sent[i:i+len(ngram)]])
                    del sent[i:i+len(ngram)]
                    sent[i:i] = [-1]*len(ngram)
                                 
        for i in range(len(sent)):
            #print(sent[i])
            if sent[i] != -1:
                sent[i] = '*'
           
        for i in range(len(sent)):
            if sent[i] == -1:
                #print(ngram_lst)
                for j in range(len(ngram_lst)):
                    #print(sent[ngram_lst[j][0]:len(ngram_lst[j][1])+ngram_lst[j][0]])
                    del sent[ngram_lst[j][0]:len(ngram_lst[j][1])+ngram_lst[j][0]] 
                    sent[ngram_lst[j][0]:ngram_lst[j][0]] = ngram_lst[j][1]
                    #print(sent)

        res = [sent[i] for i in range(len(sent)-1) if not (sent[i]=='*' and sent[i] == sent[i+1])]

        #if not(sent[-1] == "*" and sent[-2] == "*"):
        res.append(sent[-1])
            
        
        if res not in ret:
            
            ret.append(res)

    #print(ret)
    return ret

        

##ngram = ['for', 'example']
##
##sent1 = ['blah', 'for', 'example', 'blahblah']
##sent2 = ['for', 'example', 'nlp']
##sent3 = ['blahblah', 'for', 'hey', 'example']
##sent4 = ['blah', 'for', 'blahblah', 'for', 'for', 'example']
##
##
##pat = [['for', 'example'],['for'],['example']]
##doc1 = [['blah', 'for', 'example', 'blahblah'],
##        ['for', 'example', 'nlp'],
##        ['blahblah', 'for', 'hey', 'example', "blah"],
##        ['blah', 'for', 'blahblah', 'for', 'for', "blah", "blah",'example'],
##        ['blah', 'for', 'blahblah', 'for', 'blah','for', "blah", "blah",'example']]

#print(pattern_rec(ngram, sent1))
#print(pattern_rec(ngram, sent2))
#print(pattern_rec(ngram, sent3))
#print(pattern_rec(ngram, sent4))

#find_pattern(pat, doc1)


##
##test = 'the regroupment of the french armies to make head against and also to strike at this intruding wedge has been proceeding for several days largely assisted by the magnificent efforts of the royal air force'
##pat = ['*', 'the', 'french', '*', 'has', 'been', '*', 'by', 'the', '*', 'of', 'the', '*', 'air', 'force']
##
##print(best_rec(pat, test.split(' '), 0,0))

#
#pat = ['*', 'thats', 'what', 'theyre', 'doing']
###star = [[], ['want', 'to', 'be', 'tough', 'you', 'know', 'i', 'know', 'a', 'lot', 'of', 'tough', 'guys', 'but', 'theyre', 'not', 'smart', 'and', 'theyre', 'the', 'theyre', 'the', 'easiest']]
#sent =['and', 'thats', 'what', 'theyre', 'doing']
###
#print(find_star2(sent,pat))

