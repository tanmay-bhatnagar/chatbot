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
        
#Adding last tokens to both dictionaries
tokens = ['<PAD>' , '<EOS>', '<OUT>' , '<SOS>']
for token in tokens:
        questionswords2int[token] = len(questionswords2int) + 1
for token in tokens:
        answerswords2int[token] = len(answerswords2int) + 1

#Inverse mapping of answerswords2int
answersints2word = {w_i : w for w , w_i in answerswords2int.items()}

for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'
    
#Translating questions and answers to their integer counterpart
#Replacing non frequent words with <OUT>

questions_to_int = []
answers_to_int = []

for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    questions_to_int.append(ints)

for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_to_int.append(ints)


#Sorting questions and answers according to question length
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1 , 25+1):
    for i in enumerate (questions_to_int): 
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])
            
###################################################################################################

#Defining the model
            
def model_inputs():
    inputs = tf.placeholder(tf.int32 , [None,None] , name = 'input')
    targets = tf.placeholder(tf.int32 , [None,None] , name = 'target')
    lr = tf.placeholder(tf.float32,name = 'learning_rate')
    keep_prob = tf.placeholder(tf.float32 , name = 'keep_prob') #For dropout
    return inputs , targets , lr , keep_prob

def preprocess_targets(targets, word2int, batch_size):
    left_side = tf.fill([batch_size , 1] , word2int['<SOS>'])
    right_side = tf.strided_slice(targets, [0,0] , [batch_size , -1], [1,1] )
    preprocessed_targets = tf.concat([left_side,right_side] , 1)
    return preprocessed_targets
a
    
    
