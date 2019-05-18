from nltk.corpus import stopwords

global stopWords
stopWords = set(stopwords.words('english'))
stopWords.add('I')
stopWords.add('i')
