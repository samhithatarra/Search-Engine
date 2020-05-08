# https://www.geeksforgeeks.org/python-stemming-words-with-nltk/ used for tokenizing and stemming

import pathlib
import json
#import nltk
#import pickle
#import os
#import ast
import re
from nltk.stem import PorterStemmer
#from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
#import lxml
#from linkedlist import LinkedList
from collections import defaultdict
import math
import timeit
#from posting import Posting
from collections import OrderedDict

#idf  =  math.log(float(55393)/(8801705+1))
indexer_list = dict()
docId = 0
num_unique_tokens = 0
count_tokens = []  # to count the number of tokens in the whole indexer

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
        print (json_obj['url'])
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
        #print(word)
        fin_text = ''.join(word.findAll(text=True))
        fin_text = fin_text.lower()
        fin_text = re.sub('[^a-zA-Z0-9]+', ' ', fin_text)

        for token in fin_text.split():
            if len(token) > 2:
                token_lst.append(token)

    return token_lst
    #token_lst = []
    #for word in words_lst:
        #fin_text = ''.join(word.findAll(text=True))
        #fin_text = fin_text.encode('ascii', 'ignore')
        #value = value.encode
        #nltk_tokens = nltk.word_tokenize(fin_text.lower())

        #for token in nltk_tokens:
            #if len(token) >= 2:
    #             token_lst.append(token)
    # return token_lst

def add_to_postings(token, docId, header_freq, body_freq, token_frequency):
    #-------------
    # Adds the posting for a token.
    # If token exists, it add a linkedlist
    # and if not, it creates a linkedlist
    #-------------

    global indexer_list
    if token not in indexer_list.keys():
        posting_dict = OrderedDict()
        posting_dict[docId] = (header_freq, body_freq, token_frequency)
        indexer_list[token] = posting_dict

    else:
        posting_dict = indexer_list[token]
        posting_dict[docId] = (header_freq, body_freq, token_frequency)
        indexer_list[token] = posting_dict

def tf_calculation(unique_tokens,tags_dict,total_token_count):
    #-------------
    # Calculates the tf score for each token and stores
    # the docId and the tf score in the token node for
    # each doucment.
    #-------------

    for token in unique_tokens:
        header_freq = 0
        body_freq = 0
        token_frequency = 0
        if token in tags_dict['headers']:
            header_freq += tags_dict['headers'][token]
            token_frequency += header_freq
        if token in tags_dict['p']:
            body_freq += tags_dict['p'][token]
            token_frequency += body_freq
        header_freq = round(float(header_freq)/total_token_count,5)
        body_freq = round(float(body_freq)/total_token_count,5)
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

    start = timeit.default_timer()
    counter_file = 0
    path_direc = "/Users/sarthakgupta/Desktop/Search-Engine-master/DEV"   #"/Users/samhithatarra/Desktop/Search-Engine/DEV"
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
                    if token_lst!=None:
                        for token in token_lst:
                            # Stemming the token
                            token=ps.stem(token)
                            if token not in unique_tokens:
                                # List of unique tokens for each json file
                                unique_tokens.append(token)
                            count_tokens.append(token)
                            token_freq_dict[token]+=1
                            total_token_count +=1
                        tags_dict[tag] = token_freq_dict
                        num_unique_tokens += len(unique_tokens)
                    
                    #tf calculation
                    tf_calculation(unique_tokens,tags_dict,total_token_count)
                    time_lst = [1000,5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55393]
                    if (docId) in time_lst:
                        stop = timeit.default_timer()
                        print ("TIME:",stop-start)
                file_lst = [14000,28000,42000,55393]
                
                PathToFile = "/Users/sarthakgupta/Search-Engine/{0}.txt".format(counter_file)
                dict_ = {}
                if docId in file_lst:
                    with open(PathToFile,'w+') as f:
                        for tokens, postings in sorted(indexer_list.items(), key=lambda item: item[0]):
                            dict_[tokens] = dict(postings)
                            f.write(str(dict_))
                            f.write('\n')
                            dict_={}
                    indexer_list.clear()
                    counter_file+=1
                print(docId)


    print("************** FEEDBACK REPORT **************")
    print("Number of Indexed Documents:", docId)
    print("Number of Unique Words:", len(set(count_tokens)))
    print("************** FEEDBACK REPORT **************")

    # file_info = os.stat(PathToFile)
    # print("************** FEEDBACK REPORT **************")
    # print("Number of Indexed Documents:", docId)
    # print("Number of Unique Words:", num_unique_tokens)
    # print("File size in kb: ", float(file_info.st_size) / 1024)
    # print("************** FEEDBACK REPORT **************")

