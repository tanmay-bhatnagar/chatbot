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
    