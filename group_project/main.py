from untitled5 import topic_generator, qna_generator
import sys


if sys.argv[1] == "topic":
    topic_generator(sys.argv[2])
    
if sys.argv[1] == "qa": 
    qna_generator(sys.argv[2])

