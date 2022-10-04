# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:15:50 2018

@author: samak

Training for Natural Language Processing
"""

import pandas as pd
import nltk
from nltk.stem.lancaster import LancasterStemmer
import ANN
import numpy as np
import pickle


def learn_language(training_databse_name, sheet_name, out_learn_data):

#nltk.download('punkt') for nltk.word_tokenize TO WORK

	raw_data = pd.read_excel(training_databse_name,sheet_name = sheet_name)

		
	stemmer = LancasterStemmer();    
	words = [];
	classes = [];
	corpus = [];
	ignore_words = ['?','!','.',"'s","'ll","'",';',',']

	#looping through each sentence in training data
	for index, pattern in raw_data.iterrows():
		#tokenize each word in sentence
		w = nltk.word_tokenize(pattern['Message'])
		
		#add words to list of words to be learned
		words.extend(w)
		
		#add words with classes to the corpus
		corpus.append((w, pattern['Class'])); #appending a tuple to the list
		
		#create list of classes
		if pattern['Class'] not in classes:
			classes.append(pattern['Class'])
		
	#stem and lower each word (and ignore certain words)
	words = [stemmer.stem(word.lower()) for word in words if word not in ignore_words]
		
	#remove duplicates of words
	words = list(set(words))

	#remove duplicates of classes
	classes = list(set(classes))



	##--------------------------------------------------------##
	#----GENERATING TRAINING DATA ------------------------------------##

	#Training Data
	train = []; #input
	output_class = []; #output

	#Empty Output
	output_empty = [0]*len(classes) #for data


	#Training Set
	#Create a bag of words for each sentence
	for sentence in corpus:
		#initialize bag of words
		bag = []; #features extracted from data
		
		#get list of tokenized words
		pattern_message = sentence[0]; #first tuple is the message
		
		#stem each word in the message
		pattern_message = [stemmer.stem(word.lower()) for word in pattern_message]
		
		#create bag of words array (features with 0s and 1s)
		for word in words:
			bag.append(1) if word in pattern_message else bag.append(0)
			
		#add to input of training data
		train.append(bag)
		
		output_row = list(output_empty) #getting empty output
		output_row[classes.index(sentence[1])] = 1; #get the index of the class in the message in the list of classes and label that part 1
		
		#add to the output of the training data
		output_class.append(output_row)
		


	X = np.array(train);
	y = np.array(output_class)

	learning_params = ANN.learn(X,y,10,10000,0.01)

	weights1 = learning_params.weights1
	weights2 = learning_params.weights2

	#Output Important Data for Prediction
	with open(str(out_learn_data) + '.pkl', 'wb') as f:
		pickle.dump([weights1, weights2, words, classes], f)
		
	return out_learn_data