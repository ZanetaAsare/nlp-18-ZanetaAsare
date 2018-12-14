#This function compares the similarities of 2 sentences or documents using cosine similarities, suitable for QandAs and Topic Modeling

import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import sys


###########################################################################################################

def normalize(s):
    words = []
    sentences = []
    stop_words = set(stopwords.words('english'))

    for line in s:
        split = line.split(' ')
        new_split = []

        for ch in split:
            nw = ch.lower()
            nw = re.compile(r'\W+', re.UNICODE).split(nw)
            nw = ''.join(nw)

            if nw not in stop_words:
                new_split.append(nw)
       
        sentences.append(new_split)
       

        for x in new_split:
            words.append(x)

    return words, sentences

######################################################################################################

def counter(s):
    vectors = []
    bow = normalize(s)[0]
    sentence = normalize(s)[1]
    for sent in sentence:
        vector = []
        for word in bow:
            if word in sent:
                vector.append(1)
            else:
                vector.append(0)
        vectors.append(vector)
    return vectors
    
############################################################################################################

def cos_sim(s):
    vectors = counter(s)
    #print(vectors)
    array_ans = []

    for a in vectors:
        dot_product = np.dot(a, vectors[-1])
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(vectors[-1])
        ans = dot_product / (norm_a * norm_b)
            #print(str(ans))
            #print('\n')
        array_ans.append(ans)


    array_ans.pop()
    max_prob = max(array_ans)
    index = array_ans.index(max_prob)
    # print(answers[index])

    return answers[index]


############################################################################################################

s = []
answers = []

file = open("Questions.txt", "r")
for line in file:
    s.append(line)

if sys.argv[1] == "topic":
    choice = "Topics.txt"

elif sys.argv[1] == "qa":
    choice = "Answers.txt"

file2 = open(choice,"r")
for line in file2:
    answers.append(line)

############################################################################################################

quest = []
res = []

inputfile = open(sys.argv[2], "r")
for line in inputfile:
    quest.append(line)

for ques in quest:
    s.append(ques)
    res.append(cos_sim(s))

#############################################################################################################

result = open(("{}_results.txt".format(sys.argv[1])), "w")

for val in res:
    result.write(str(val) + '\n')
    
result.close()
print('Check current folder for your results file')
