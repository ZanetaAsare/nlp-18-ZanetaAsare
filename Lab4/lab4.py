import sys
import pandas as pd
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder

######################################################################################################################################


filelist = ['yelp_labelled.txt','imdb_labelled.txt','amazon_cells_labelled.txt']
data = [pd.read_table(file, sep ='\t',header=None,names=['sentence','class']) for file in filelist]
big_data = pd.concat(data)


######################################################################################################################################


if sys.argv[2] == 'n':
    #performing word normalization
    big_data['sentence'] = big_data.sentence.map(lambda x: x.lower())            #converting all words to lowercase
    big_data['sentence'] = big_data.sentence.str.replace('[^\w\s]', '')           #removing punctuations from sentences


    big_data['sentence'] = big_data['sentence'].apply(nltk.word_tokenize)          #performing word tokenization

    #performing word stemming
    stemmer = PorterStemmer()                                                        
    big_data['sentence'] = big_data['sentence'].apply(lambda x: [stemmer.stem(y) for y in x]) 

elif sys.argv[2] == 'u':
    big_data['sentence'] = big_data['sentence'].apply(nltk.word_tokenize)          #performing word tokenization

else:
    print('Please enter a valid normalization method')



########################################################################################################################


#This section is used for feature extraction
# This converts the list of words into space-separated strings
big_data['sentence'] = big_data['sentence'].apply(lambda x: ' '.join(x))

vectorizer = CountVectorizer()                                             #an algorithm for extracting the features
counts = vectorizer.fit_transform(big_data['sentence'])

#this is for assigning weights to words in terms of frequency and importance
transformer = TfidfTransformer().fit(counts)
counts = transformer.transform(counts)



########################################################################################################################

    #this section is used for training the naive bayes classifier
if sys.argv[1] == 'nb':

    #the data is first split into training and testing data
    x_train, x_test, y_train, y_test = train_test_split(counts, big_data['class'], test_size=0.1, random_state=69)

    #the training set is used to train the classifier
    model = MultinomialNB().fit(x_train, y_train) 


elif sys.argv[1] == 'lr':
    #this section is used for training the logistic regression classifier

    #the data is first split into training and testing data
    x_train, x_test, y_train, y_test = train_test_split(counts, big_data['class'], test_size=0.1, random_state=69)

    #the actual training
    model = LogisticRegression().fit(x_train, y_train)

else:
    print('Please enter a valid classifier type')


####################################################################################################################################    
#vectorizing the test file
testfile = sys.argv[3]

test_data = pd.read_table(testfile, sep='\t',header=None,names=['sentence'])

test_data['sentence'] = test_data['sentence'].apply(nltk.word_tokenize)

test_data['sentence'] = test_data['sentence'].apply(lambda x: ' '.join(x))

#an algorithm for extracting the features

newcount = vectorizer.transform(test_data['sentence'])


predicted = model.predict(newcount)
#print(accuracy_score(y_test,predicted) * 100) 
#print(confusion_matrix(y_test, predicted))


#######################################################################################################################################


result = open(("results-{}-{}.txt".format(sys.argv[1],sys.argv[2])), "w")

for val in predicted:
    result.write(str(val) + '\n')
    
result.close()
print('Check current folder for your results file')
