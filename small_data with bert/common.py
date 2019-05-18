from nltk.corpus import stopwords

global stopWords
stopWords = set(stopwords.words('english'))
stopWords.add('I')
stopWords.add('i')

##global doc
##global doc2
##global doc3
# doc = [['thank', 'you', 'so', 'much'],
# ['thats', 'so', 'nice'],
# ['isnt', 'he', 'a', 'great', 'guy'], 
# ['he', 'doesnt', 'get', 'a', 'fair', 'press', 'he', 'doesnt', 'get', 'it'], 
# ['its', 'just', 'not', 'fair']]

doc2 = [['I', 'like', 'the', 'people', 'of', 'iowa'],
 ['for', 'example', 'the', 'way', 'it', 'is'], 
 ['like', 'iowa'],
 ['like','iowa']]
doc = [['for', 'example', 'I', 'like', 'you'],
       ['for', 'example', 'I', 'want', 'to', 'eat'],
      ['for', 'example', 'you', 'are', 'an', 'idiot']]
doc3 = [['our', 'president', 'is', 'either', 'grossly', 'incompetent', 'a', 'word', 'that', 'more', 'and', 'more', 'people', 'are', 'using', 'and', 'i', 'think', 'i', 'was', 'the', 'first', 'to', 'use', 'it', 'or', 'he', 'has', 'a', 'completely', 'different', 'agenda', 'than', 'you', 'want', 'to', 'know', 'about', 'which', 'could', 'be', 'possible'], ['in', 'any', 'event', 'washington', 'is', 'broken', 'and', 'our', 'country', 'is', 'in', 'serious', 'trouble', 'and', 'total', 'disarray'], ['very', 'simple'], ['politicians', 'are', 'all', 'talk', 'no', 'action'], ['they', 'are', 'all', 'talk', 'and', 'no', 'action']]
global minisup
minisup = 0.006

global total_length
total_length = 0
