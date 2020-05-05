# https://www.geeksforgeeks.org/python-stemming-words-with-nltk/ used for tokenizing and stemming

import pathlib
import json
import nltk
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import lxml
from linkedlist import LinkedList
from collections import defaultdict
import math

posting = dict()
docId = 0

def find_content(path):
    #-------------
    # Finds the content from the json file. 
    # Retruns a dictionary with two keys: headers and p
    # value of key 'headers': a list of sentences from h1.h2,h3, bold and strong tags
    # value of key 'p'': a list of sentences from p tag
    #-------------

    tags_dict = defaultdict(list)
    header_lst = []
    with open(path, "r") as current_file:
        json_obj = json.load(current_file)
        content = json_obj['content']
        #rint(json_obj['url'])
        soup = BeautifulSoup(content,"lxml")
        tags_dict['p'] = [s for s in soup.findAll('p')]
        header_lst = [s for s in soup.findAll('h1')]
        for s in soup.findAll('h2'):
            header_lst.append(s)
        for s in soup.findAll('h3'):
            header_lst.append(s)
        for s in soup.findAll('title'):
            header_lst.append(s)
        for s in soup.findAll('b'):
            header_lst.append(s)
        for s in soup.findAll('strong'):
            header_lst.append(s)
        tags_dict['headers'] = header_lst
    return tags_dict

def find_tokens(words_lst):
    #-------------
    # Finds the tokens from the sentences found from the 
    # content and returns a list of tokens found in a 
    # particular tag. 
    #-------------

    token_lst = []
    for word in words_lst:
        fin_text = ''.join(word.findAll(text=True))
        fin_text = fin_text.lower()
        nltk_tokens = nltk.word_tokenize(fin_text)

        for token in nltk_tokens:
            if len(token) >= 2:
                token_lst.append(token)
    return token_lst

def add_to_postings(token, docId, header_freq, body_freq, token_frequency):
    #-------------
    # Adds the posting for a token.
    # If token exists, it add a linkedlist 
    # and if not, it creates a linkedlist 
    #-------------

    global posting
    if token not in posting.keys():
        posting_list = LinkedList()
        posting_list.sorted_add_node(docId, header_freq, body_freq, token_frequency)
        posting[token] = posting_list
    else:
        posting_list = posting[token]
        posting_list.sorted_add_node(docId, header_freq, body_freq, token_frequency)
    
    #print ('token: ', token, "ID: ", posting[token].print_func())
    


def tf_calculation(unique_tokens,tags_dict,total_token_count):
    #-------------
    # Calculates the tf score for each token and stores 
    # the docId and the tf score in the token node for 
    # each doucment. 
    #-------------

    for token in unique_tokens:
        # Need to initialize new node for linked list
        header_freq = 0
        body_freq = 0
        token_frequency = 0
        if token in tags_dict['headers']:
            header_freq += tags_dict['headers'][token]
            token_frequency += header_freq
        if token in tags_dict['p']:
            body_freq += tags_dict['p'][token]
            token_frequency += body_freq
        # <--
        header_freq = float(header_freq)/total_token_count
        body_freq = float(body_freq)/total_token_count
        
        # Calls function to add node into the index
        add_to_postings(token, docId, header_freq, body_freq, token_frequency)
    
def calculate_tf_idf(docId):
    #-------------
    # Calculates the tf_idf score for each token and stores 
    # the tf-idf score in the token node for each document
    # by calling : calculate_tfidf. 
    #-------------

    corpus_size = docId
    for token, posting_lst in posting.items():
        occurences_token = posting[token].len_of_list()
        # Idf score for a token
        idf_score = math.log(float(corpus_size)/(occurences_token+1))
        #print("----IDF SCORE----:", idf_score)
        # calculate the tf-idf for each doc in the linked list 
        posting[token].calculate_tfidf(idf_score)
        ## print ('token: ', token, "ID: ", posting[token].print_func())

if __name__ == "__main__":
    # /Users/sarthakgupta/Search-Engine/ANALYST
    path_direc = "/Users/samhithatarra/Desktop/Search-Engine/DEV"
    for direc in pathlib.Path(path_direc).iterdir():
        for path in pathlib.Path(direc).iterdir():
            if path.is_file():
                docId+=1 
                total_token_count = 0
                unique_tokens = []
                tags_dict = find_content(path)
            
                for tag, words_lst in tags_dict.items():
                    token_lst = find_tokens(words_lst)
                    ps = PorterStemmer()
                    token_freq_dict = defaultdict(int)
                    for token in token_lst:
                        # Stemming the token 
                        token=ps.stem(token)   
                        if token not in unique_tokens:
                            # List of unique tokens for each json file 
                            unique_tokens.append(token)  
                        token_freq_dict[token]+=1
                        total_token_count +=1
                    tags_dict[tag] = token_freq_dict 

                #tf calculation
                tf_calculation(unique_tokens,tags_dict,total_token_count)
                print(docId)
                # for k,v in tags_dict.items():
                #     print("***KEY***:", k, "VALUE:", v)

    #tf-idf calculation
    calculate_tf_idf(docId)

# STRUCTURE 

# (nodes: header freq, body freq, tf-idf score)  (nodes: header freq, body freq, tf-idf score)
#                     ^                                    ^
#                     |                                    |
# posting: {token: docId-x -> docId-y -> ..... , token: docId-v -> docId-z -> .... , ...}
# SORTED BY DOC ID 
    print("************** FEEDBACK REPORT **************")
    print("Number of Indexed Documents:", docId)
    print("Number of Unique Words:", len(posting.keys()))
    print("************** FEEDBACK REPORT **************")