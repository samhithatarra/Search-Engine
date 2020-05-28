# --- Source Citation ---
# https://www.geeksforgeeks.org/python-stemming-words-with-nltk/ 
# Used above link to understand how PorterStemmer is used
# --
# https://itqna.net/questions/68805/remove-comment-tag-and-its-contents-beautifulsoup-4
# Used above link for removing comments in html content
# -----------------------

# --- Team Members ---
# Kamaniya Sathish Kumar (56361951)
# Vaanya Gupta (92052177)
# Samhitha Tarra (69706915)
# Vani Anilkumar (36335618)
# ---------------------

import pathlib
import json
import re
import html5lib
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup, Comment
import bs4
from collections import defaultdict
from collections import OrderedDict
from merge import merge_files
import os
import lxml 
import ast
import math
indexer_list = dict()
docId = 0
num_unique_tokens = 0
count_tokens = []  
doc_url = dict()

def find_content(path):
    #-------------
    # Finds the content from the json file.
    # Returns a dictionary with two keys: headers and p
    # value of key 'headers': a list of sentences from h1.h2,h3, bold and strong tags
    # value of key 'p'': a list of sentences from p tag
    #-------------

    tags_dict = defaultdict(list)
    header_lst = []
    with open(path, "r") as current_file:
        json_obj = json.load(current_file)
        content = json_obj['content']
        # Only extracting webpage content for links without fragments
        if '#' not in str(json_obj['url']): 
            soup = BeautifulSoup(content,"html5lib")
            for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
                comments.extract()
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
    return tags_dict,json_obj['url']

def find_tokens(words_lst,unique_tokens):
    #-------------
    # Finds the tokens from the sentences found from the
    # content and returns a list of tokens found in a
    # particular tag.
    #-------------
    
    ps = PorterStemmer()
    token_lst = []
    find_text = []
    token_freq_dict = defaultdict(int)
   
    for word in words_lst:
        fin_text = ''.join(word.findAll(text=True))
        fin_text = fin_text.lower()
        fin_text = re.sub('[^a-zA-Z0-9]+',' ', str(fin_text))
        find_text.extend(fin_text.split())
  
    for token in find_text:
        if len(token) >= 2:
            token=ps.stem(token)
            if len(token) >= 2:
                token_lst.append(token)
                unique_tokens.append(token)
                count_tokens.append(token)
                token_freq_dict[token]+=1
   
    return (token_freq_dict,list(set(unique_tokens)),token_lst)

def add_to_postings(token, docId, token_frequency, header_freq, body_freq):
    #-------------
    # Adds the posting for a token.
    # If token exists, it adds a key and value
    # and if not, it creates a ordered dict
    # STRUCTURE: {token:{dociD:[posting]},{dociD:[posting]},{dociD:[posting]}, token:{dociD:[posting]},....}
    # [posting] = [token_frequency(total_frequency), header frequency, body frequency]
    #-------------

    global indexer_list
    if token not in indexer_list.keys():
        posting_dict = OrderedDict()
        posting_dict[docId] = [token_frequency,header_freq,body_freq]
        indexer_list[token] = posting_dict

    else:
        posting_dict = indexer_list[token]
        posting_dict[docId] = [token_frequency,header_freq, body_freq]
        indexer_list[token] = posting_dict

def frequency_calculation(unique_tokens,tags_dict):
    #-------------
    # Calculates the frequency count for each token and stores
    # the docId, total frequency, header frequency and body frequency 
    # in the indexer_list for each document.
    #-------------

    for token in unique_tokens:
        token_frequency = 0
        body_freq = 0
        header_freq = 0
        if token in tags_dict['headers']:
            header_freq += tags_dict['headers'][token]
            token_frequency += tags_dict['headers'][token]

        if token in tags_dict['p']:
            body_freq += tags_dict['p'][token]
            token_frequency += tags_dict['p'][token]

        # Calculating the tf scores for the tokens that 
        # appear in the headers 
        if header_freq > 0:
            header_freq = 1 + math.log(float(header_freq))
        else:
            header_freq = 0

        # Calculating the tf scores for the tokens that 
        # appear in the body
        if body_freq > 0:
            body_freq = 1 + math.log(float(body_freq))
        else:
            body_freq = 0
        
        # Adding the posting list along with the docId in the indexer_list
        add_to_postings(token, docId, token_frequency, header_freq, body_freq)

if __name__ == "__main__":

    counter_file = 0
    path_direc = "/Users/kamaniya/Documents/Search-Engine/DEV.nosync"  
    for direc in pathlib.Path(path_direc).iterdir():
        for path in pathlib.Path(direc).iterdir():
            if path.is_file():
                
                total_token_count = 0
                unique_tokens = []

                (tags_dict,url) = find_content(path)
                if (tags_dict!={}):
                    docId+=1
                    doc_url[docId] = url
                    for tag, words_lst in tags_dict.items():
                    
                        (token_freq_dict,unique_tokens,token_lst) = find_tokens(words_lst,unique_tokens)
        
                        if token_lst!=None:
                            tags_dict[tag] = token_freq_dict
                            num_unique_tokens += len(unique_tokens)
                        
                        frequency_calculation(unique_tokens,tags_dict)
                    

    # Offloading 4 times 

            file_lst = [14000,28000,42000]
            PathToFile = "/Users/kamaniya/Documents/Search-Engine/{}.txt".format(counter_file)
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
    PathToFile = "/Users/kamaniya/Documents/Search-Engine/{}.txt".format(counter_file)
    dict_={}
    with open(PathToFile,'w+') as f:
        for tokens, postings in sorted(indexer_list.items(), key=lambda item: item[0]):
            dict_[tokens] = dict(postings)
            f.write(str(dict_))
            f.write('\n')
            dict_={}
    indexer_list.clear()
    counter_file+=1
                    

    # ********** MERGING ************************** 
    file1 = "/Users/kamaniya/Documents/Search-Engine/0.txt"
    file2 = "/Users/kamaniya/Documents/Search-Engine/1.txt"
    file3 = "/Users/kamaniya/Documents/Search-Engine/2.txt"
    file4 = "/Users/kamaniya/Documents/Search-Engine/3.txt"
    merge_1 = "/Users/kamaniya/Documents/Search-Engine/{}.txt".format('merge_1')
    merge_2 = "/Users/kamaniya/Documents/Search-Engine/{}.txt".format('merge_2')
    final_merge = "/Users/kamaniya/Documents/Search-Engine/{}.txt".format('final_merge')
    merge_files(file1,file2,merge_1)
    merge_files(file3,file4,merge_2)
    merge_files(merge_1,merge_2,final_merge)
 

    print("************** FEEDBACK REPORT **************")
    print("Number of Indexed Documents:", docId)
    print("Number of Unique Words:", len(set(count_tokens)))
    complete_index_file = "/Users/kamaniya/Documents/Search-Engine/final_merge.txt"
    file_info = os.stat(complete_index_file)
    print("Complete Index File Size in KB: ", float(file_info.st_size) / 1000)
    print("************** FEEDBACK REPORT **************")