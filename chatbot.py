# Importing Libraries

import numpy as np
import tensorflow as tf
import re
import time

#Data Preprocessing

#Import data

lines = open('/home/tanmay/Desktop/Chatbot/chatbot/movie_lines.txt' , encoding = 'utf-8' , errors = 'ignore').read().split('\n')
conversations = open('/home/tanmay/Desktop/Chatbot/chatbot/movie_conversations.txt' , encoding = 'utf-8' , errors = 'ignore').read().split('\n')

#Creating dictionary that maps each line with its ID
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]
        
    
#Creating list of conversations with IDs of each line belonging to a conversation in that conversation
conversations_ids = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'" , "").replace(" " , "")
    #Extracted line numbers ONLY +++$+++ is delimiter, Line numbers in last element after split
    #1:-1 to remove [] and replaces to remove ' and spaces
    conversations_ids.append(_conversation.split(','))

questions = []
answers = []
for conversation in conversations_ids:
        for i in range(len(conversation ) - 1):
            questions.append(id2line[conversation[i]])
            answers.append(id2line[conversation[i+1]])
            
#This function replaces abbreviated words
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm" , "i am" , text)
    text = re.sub(r"he's" , "he is" , text)
    text = re.sub(r"she's" , "she is" , text)
    text = re.sub(r"that's" , "that is" , text)
    text = re.sub(r"where's" , "where is" , text)
    text = re.sub(r"i'm" , "i am" , text)
    text = re.sub(r"\'ll" , " will" , text)
    text = re.sub(r"\'ve" , " have" , text)
    text = re.sub(r"\'s" , " is" , text)
    text = re.sub(r"\'re" , " are" , text)
    text = re.sub(r"\'d" , " would" , text)
    text = re.sub(r"won't" , "will not" , text)
    text = re.sub(r"can't" , "cannot" , text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]" , "" , text)
    text = re.sub(r"don't" , "do not" , text)
    
    return text
    
#Cleaning questions
clean_questions = []  
for question in questions:
    clean_questions.append(clean_text(question))
    
#Cleaning answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer)) 


#Prepare wordcount
word2count = {}

for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
            
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1

#Creating 2 dictionaries to map question words and answer words to a unique integer
threshold = 15
questionswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number += 1
        
answerswords2int = {}
for word, count in word2count.items():
    if count >= threshold:
        answerswords2int[word] = word_number
        word_number += 1
        
    