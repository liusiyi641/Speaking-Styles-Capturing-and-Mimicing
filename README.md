# Speaking-Styles-Capturing-and-Mimicing

Mirroring is the behavior in which one personsubconsciously  imitates  the  gesture,  speechpattern, or attitude of another (Chartrand and Bargh, 1999).  In conversations, mirroring often  signals  the  speakers’  enjoyment  and  engagement in their communication. In chatbots, to  make  human-computer  interactions  more enjoyable and engaging to users, methods have been proposed to add personas to the chatbots and to train them to speak or to shift their dialogue style to that of the personas.  However, they often require a large dataset consisting ofdialogues of the target personalities to train. In this work, we explore a method that can learn to  mirror  the  speaking  styles  of  a  person  incrementally.  The advantage of our method is that  it  can  enable  chatbots  to  learn  to  adapt their speaking styles to match the user’s as the conversation progresses just as humans would. Our  method  extracts  n-grams  that  capture  a person’s speaking styles and uses the n-grams to  create  patterns  for  transforming  sentences to  the  person’s  speaking  styles.   Our  experiments  show  that  our  method  is  able  to  capture patterns of speaking style that can be used to transform regular sentences into sentences with the target style.



Basically, there are four main functions that do all the jobs by calling other scripts, three for neural network approach and one for incremental, and here's all the details you need to know. 


For large dataset neural network approach:

	main.py: Given the Trump's speech data, it will first run the 'data_cleaning.py' to clean the data, and save the cleaned document as a pickle file. It will then call the frequent.py to run frequent itemset mining algorithm and find all the frequent ngrams. After we have the ngrams, we can then run the find_pattern method from tfidf3.py and find all the patterns containing the ngrams. It will then save all the patterns in a pickle file. 

	new_main.py: Given a cleaned document and all the patterns we found, new_main.py will call the tfidf3.py and find all the wildcard sentences. And we can use them to train our seq2seq model.

	training_main.py: Given that now we have all the sentences with patterns (original sentences) and sentences without patterns (wildcard sentences) saved as input_sent and input_pat sentences, we can just input them to a seq2seq model and train it to learn the patterns and transform our input sentence! 
	The code was mainly adapted from a tutorial given by tensorflow: https://www.tensorflow.org/alpha/tutorials/sequences/nmt_with_attention#download_and_prepare_the_dataset


For incremental small dataset approach:

	incremental_main.py: Given a cleaned document, it will first construct word graphs used for incremental itemset mining. You could adjust the amount of data you want to pass in, but make sure to also comment/uncomment parts of the codes below to make sure the graph is constructed correctly. Then it calls the same function to find the pattern using the ngrams we found from incremental itemset mining. Then it calls tfidf3.py to find all wildcard sentences and compute their vectors (requires Bert-as-service library from github). It will output a list in the form of [appear_times, appear_times/len(document), pattern, separate_vec, [whole_vector], [original_vec]]. At last it calls the pick_and_transform.py to compute the best pattern for our input sentence using cosine similarity. 

