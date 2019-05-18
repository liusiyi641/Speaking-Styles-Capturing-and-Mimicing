from vectorizer_and_similarity import similarity, vectorizing



def pick_pattern(sent, lst):
    # given the input sentence and the list of patterns find the best pattern
    
    """
    Args: 
        sent  (str): input sentence that human generates
        
        lst   (list(list)): the list returned by tf, contained with the pattern and a bunch of vectors
        
    Output:
        ret   (list): return the list with the selected pattern
    """
    
    vector = vectorizing(sent)

    max_similarity = 0
    pattern = ()
    for i, pat in enumerate(lst):
        #print(vector)
        #print(pat[2])
        similarity_score = similarity(vector, pat[2][0])
        print(similarity_score)
        if similarity_score > max_similarity:
            max_similarity = similarity_score
            pattern = pat

    #print(pattern[0])       
    return pattern


def transform(sent, lst):
    #  given the broken sentence and the target pattern combine them together
    """
    Args:
        sent  (list(list)): one of the possible broken input sentece
        
        lst   (list(list)): the list with selected pattern and its vectors
        
    Output:
        ret   (list(str)): the combined sentence of the pattern and the possible broken sentence 
    """
    
    pattern = lst[0]
    separate_vec = lst[1]
    num = len(separate_vec)
    index = 0
    #print(num)
    #print(sent)
    
    res = []
    for word in pattern:
        if word != '*':
            res.append(word)
        else:
            #print(sent)
            #print(lst)
            for elem in sent[index]:
                res.append(elem)
        
            index+=1
    #num -=1
        
    return res
        

    


def break_sentence(sent, num):
    # break the input sentence to num+1 many of parts
    """
    Args:
        sent (list): input sentence
        
        num  (int): the number of wildcards
        
    Output:
        ret  (list(list(list))): the sentence broken into parts
    """
    
    
    res = []

    if num ==0:
        return [[sent]]

    if num == 1:
        for i in range(len(sent)):
            res.append([sent[:i], sent[i:]])
            
        res.append([sent[:],[]])
        #print(res)
        return res
    else:
        ret = []
        for i in range(len(sent)):
            front = sent[:i]     
            lst = break_sentence(sent[i:],num-1)
            #print(lst[0])
            for temp in lst:
                temp.insert(0,front)
                ret.append(temp)
            #ret.append(tmp)
        ret.append([sent[:]] +[[]]*num)
        #print(ret)
        return ret
            



#print(break_sentence(['i','like','to','dance'],1))

#print(transform([['i', 'like']], [['hey','*', 'you'], [1234], [1234]]))

#sent_lst = break_sentence(['i','like','to','dance','jazz'],0)
#print(sent_lst)
###print(sent_lst)
##for sent in sent_lst:
##    print(transform(sent, [['*','oh','*', 'you', '*'], [1,2,3],[1]]))
##    
##        
