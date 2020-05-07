# https://www.geeksforgeeks.org/python-stemming-words-with-nltk/ used for tokenizing and stemming
import pathlib
import json
import nltk
import pickle
import pandas as pd
import os
# import ssl 
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download()
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import lxml
from linkedlist import LinkedList
from collections import defaultdict
import math
import timeit
from posting import Posting
from collections import OrderedDict
#indexer = dict() **
indexer_list = dict()
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
        #print(json_obj['url'])
        soup = BeautifulSoup(content,"html.parser")
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

    #global indexer **
    global indexer_list 
    if token not in indexer_list.keys():
        # posting_list = []
        # new_post_obj = Posting(docId, header_freq, body_freq, token_frequency)
        # posting_list.append(new_post_obj)
        # indexer_list[token] = posting_list
        posting_dict = OrderedDict()
        posting_dict[docId] = (header_freq, body_freq, token_frequency)
        indexer_list[token] = posting_dict 

    else:
        # posting_list = indexer_list[token]
        # new_post_obj = Posting(docId, header_freq, body_freq, token_frequency)
        # posting_list.append(new_post_obj)
        # indexer_list[token] = posting_list
        posting_dict = indexer_list[token]
        posting_dict[docId] = (header_freq, body_freq, token_frequency)
        indexer_list[token] = posting_dict


    #posting[token].print_func()
    #print("END")
    
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
    
# def calculate_tf_idf(docId):
#     #-------------
#     # Calculates the tf_idf score for each token and stores 
#     # the tf-idf score in the token node for each document
#     # by calling : calculate_tfidf. 
#     #-------------

#     corpus_size = docId
#     for token, posting_lst in indexer.items():
#         occurences_token = indexer[token].len_of_list()
#         # Idf score for a token
#         idf_score = math.log(float(corpus_size)/(occurences_token+1))
#         #print("----IDF SCORE----:", idf_score)
#         # calculate the tf-idf for each doc in the linked list 
#         indexer[token].calculate_tfidf(idf_score)
#         # print ('token: ', token, "ID: ", posting[token].print_func())



if __name__ == "__main__":
    # /Users/sarthakgupta/Search-Engine/ANALYST
    start = timeit.default_timer()
    path_direc = "/Users/kamaniya/Documents/Search-Engine/DEV.nosync"   #"/Users/samhithatarra/Desktop/Search-Engine/DEV"
    for direc in pathlib.Path(path_direc).iterdir():
        print(direc)
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
                time_lst = [1000,5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000]
                if (docId) in time_lst:
                    stop = timeit.default_timer()
                    print ("TIME:",stop-start)
                
                #json version


                    # chunk = pd.read_json(PathToFile, lines = True, chunksize = 100)
                    # for c in chunk:
                    #     print(c)
                    



                # if docId == 300:
                #     PathToFile = "/Users/kamaniya/Documents/Search-Engine/{0}.txt".format("test")
                #     filehandle = open(PathToFile,'wb')
                #     od = OrderedDict(sorted(indexer_list.items()))
                #     pickle.dump(od, filehandle)

                #     indexer_list.clear()
                #     print("LENGTH OF DICT", len(indexer_list.keys()))
                #     filehandle.close()
                #     loaded_index = pickle.load(filehandle)
                #     for key, val in loaded_index.items():
                #         print(key, [x.docId for x in val])
                #     filehandle.close()
                print(docId)
                # for k,v in tags_dict.items():
                #     print("***KEY***:", k, "VALUE:", v)
    PathToFile = "/Users/kamaniya/Documents/Search-Engine/{0}.json".format("test")
    filehandle = open(PathToFile, 'w')
    json.dump(indexer_list, filehandle)
    filehandle.close()
    indexer_list.clear()
    file_stats = os.stat(PathToFile)
    print(f'File size in bytes is {file_stats.st_size}')
    #tf-idf calculation
    #calculate_tf_idf(docId)

# STRUCTURE 

# (nodes: header freq, body freq, tf-idf score)  (nodes: header freq, body freq, tf-idf score)
#                     ^                                    ^
#                     |                                    |
# posting: {token: docId-x -> docId-y -> ..... , token: docId-v -> docId-z -> .... , ...}
# SORTED BY DOC ID 
    print("************** FEEDBACK REPORT **************")
    print("Number of Indexed Documents:", docId)
    print("Number of Unique Words:", len(indexer.keys()))
    print("************** FEEDBACK REPORT **************")