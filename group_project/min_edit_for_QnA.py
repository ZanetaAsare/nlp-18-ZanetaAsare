
#%%
import re;
import math;
import sys;
import nltk;

categories = []
normal = []
counts = []
vocab = set()

topic_list = []
qa_dict = {}
answer_list = []
quest_list = []

'''This function normalizes the string passed by removing spaces, numbering, tabs,
newline characters, punctuation marks etc'''

def trimmer(s):
    top = s.strip('\n');
    result = ''.join([i for i in top if not i.isdigit()])
    fin = result.replace(".", "", 1).strip('\t')
    fin = fin.lower()
    fin = re.sub(r'[^\w\s]','',fin)
    return fin



def bags(quest_file, top_file, answer_file):
    dict = {}
    with open(quest_file) as questions:
        quests = questions.readlines()
        quests = quests[:-5] 
        for a in quests:
            quest_list.append(trimmer(a)) 
        
        
    with open(top_file) as topics:
        tops = topics.readlines();
        for a in tops: 
            topic_list.append((trimmer(a))) 
        
    with open(answer_file) as answers:
        answer = answers.readlines();
        for a in answer:  
            answer_list.append((trimmer(a)))         
            for b in quest_list:
                qa_dict[b] = a  
 
bags("Questions.txt", "Topics.txt", "Answers.txt")
# print(answer_list[10])
 

# use minimum edit distance for questions and answers
def find_min(question):
    min = 0
    count = 0
    for q in quest_list:
        distance = nltk.edit_distance(q, question);
        if count == 0:
            min = distance
            count = count + 1
        if distance < min:
            min = distance
            count = count + 1;
        
    return answer_list[count]

def do_task(task):
    if sys.argv[1].casefold() == "topic":
        pass
    elif sys.argv[1].casefold() == "qa":
        pass


def write_file(filename, string):
    f = open(filename, "w+")
    f.write(string)
    
 