
# coding: utf-8

# In[5]:


import math

def my_naive_bayes(testdoc):
    
    doc = open(testdoc,"r")
    result = open("results.txt","w")
    
    for line in doc:        
        doc_split = line.split()           
    
        prob0 = 1
        for i in range(len(doc_split)):           
            res0 = loglikelihood(doc_split[i],0)     #finding the loglikelihood of each of the words
            prob0 = prob0 * res0                   #accumulating loglikelihood of words
        
        prob1 = 1
        for i in range(len(doc_split)):
            res1 = loglikelihood(doc_split[i],1)
            prob1 = prob1 * res1
       
        final_prob0 = prob0 * logprior['0']         #finding the probability of negative class
        final_prob1 = prob1 * logprior['1']         #finding the probablity of positive class
    
     
    
        if final_prob0 > final_prob1:           #comparing to see which class is greater
            result.write('0\n')
            
        else:
            result.write('1\n')
            
    return 
             
    


# In[6]:


def loglikelihood(word,class_type):
    
    amazon = open("amazon_cells_labelled.txt","r")
    yelp = open("yelp_labelled.txt","r")
    imdb = open("imdb_labelled.txt","r")
    
    classes = {}          #dictionary containing the various sentences separated into positive and negative classes
    classes['0'] = []
    classes['1'] = []
    
    for i in range(500):
        yelp_read = yelp.readlines(1)              #reading all three lines
        am_read = amazon.readlines(1)
        im_read = imdb.readlines(1)

        str1 = yelp_read[0]                         #extracting the string out of the list object type above
        str2 = am_read[0]
        str3 = im_read[0]
    
    
        yelp_split = str1.split()                   #splitting the string to get the number at the end of the sentence
        am_split = str2.split()
        im_split = str3.split()

    
    
        if yelp_split.pop() == '0':                 #checking if number is 0 or 1
            list0 = classes['0']                    #the value for classes['0'] is assigned to list0
            list0.append(str1)                      #sentence is appended to list0 
            classes['0'] = list0                    #value for classes['0'] is updated with appended list
        else:
            list1 = classes['1']
            list1.append(str1)
            classes['1'] = list1
    
    
        if am_split.pop() == '0':
            list0 = classes['0']
            list0.append(str2)
            classes['0'] = list0
        else:
            list1 = classes['1']
            list1.append(str2)
            classes['1'] = list1
    
    
        if im_split.pop() == '0':
            list0 = classes['0']
            list0.append(str3)
            classes['0'] = list0
        else:
            list1 = classes['1']
            list1.append(str3)
            classes['1'] = list1    


    list0_len = len(list0)    
    list1_len = len(list1)
    totalnum = list0_len + list1_len
    
    bag_words = {}       #dictionary containing bag of words separated into positive and negative classes
    bag_words['0'] = []
    bag_words['1'] = []
    
 
    i = 0
    word_list0 = []                    #initializing lists for containing the bag of words
    word_list1 = []

    for i in range(list0_len):          #an iteration through the negative list of words assigned to classes['0'] earlier
        sen0 = list0[i]              
    
        sen_split0 = sen0.split()       #extracted string sentences are split by space variable
    
    
        for j in range(len(sen_split0) - 1):        #an iteration through the extracted split string sentences
            word0 = sen_split0[j]
            word_list0.append(word0)              #words are appended into the word list initialized earlier
       
        
        #same process is applied to the positive class
    for i in range(list1_len):               
        sen1 = list1[i]              

        sen_split1 = sen1.split()            
    
        for k in range(len(sen_split1) - 1):       
            word1 = sen_split1[k]
            word_list1.append(word1)        

        
    bag_words['0'] = word_list0           #word lists are assigned to the bag_words dictionary according to their class
    bag_words['1'] = word_list1
    
    
    #calculating probabilities of positive and negative sentences in the document
    logprior = {}
    logprior['0'] = math.log(list0_len/totalnum)
    logprior['1'] = math.log(list1_len/totalnum)
    
    
    V = word_list0 + word_list1    #all the words in the vocabulary
    lenV = len(V)
               
    
    #dictionaries for storing the number of times a word in the vocabulary appears in either the positive or negative class

    count_word0 = {}     
    count_word1 = {}
    

    #counting the number of times a word in the vocabulary appears in either the positive or negative class

    for w in range(lenV):         #an iteration through the vocabulary bag of words
        count = 0
        check = V[w]
    
        for k in range(len(word_list0)):      #for each word in the vocabulary, check the number of times it appears in the negative class and increment count
            if check == word_list0[k]:
                count = count + 1
   
        count_word0[check] = count          #the word and its count value is stored in a dictionary count_word0
    


    for w in range(lenV):           #same process applies to the positive class
        count = 0
        check = V[w]
    
        for k in range(len(word_list1)):
            if check == word_list1[k]:
                count = count + 1
   
        count_word1[check] = count
        
    
    #this section counts the number of times a word in the class appears in the vocabulary and sums it up
    sum_count0 = 0
    sum_count1 = 0

    for w in range(len(word_list0)):          #an iteration through the negative class bag of words
        count = 0
        check = word_list0[w]
    
        for k in range(lenV):          #an iteration through the vocabulary bag of words to check for the number of occurences for word
            if check == V[k]:
                count = count + 1
            
        sum_count0 = sum_count0 + count      #the summer adds the count up till all words in the class are exhausted
    

    for w in range(len(word_list1)):          #same process applies for the positive class
        count = 0
        check = word_list1[w]
    
        for k in range(lenV):
            if check == V[k]:
                count = count + 1
            
        sum_count1 = sum_count1 + count 
    
    
    if class_type == 0:
        if word in count_word0.keys() == True:     #checking to see if word is in bag of words for that class
            count_val0 = count_word0[word]
        else:
            count_val0 = 0             #if not, the count for that word is 0
        ans = math.log((count_val0 + 1)/(sum_count0 + lenV))
        
    else:
        if word in count_word1.keys() == True:
            count_val1 = count_word1[word]
        else:
            count_val1 = 0
        ans = math.log((count_val1 + 1)/(sum_count1 + lenV))
        
        
    amazon.close()
    yelp.close()
    imdb.close()
    
    
    return ans

