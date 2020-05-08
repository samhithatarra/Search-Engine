# --- Source Citation ---
# https://www.geeksforgeeks.org/python-stemming-words-with-nltk/ 
# Used above link to understand how PorterStemmer is used
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
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict
from collections import OrderedDict
from merge import merge_files
import os

indexer_list = dict()
docId = 0
num_unique_tokens = 0
count_tokens = []  

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
        fin_text = ''.join(word.findAll(text=True))
        fin_text = fin_text.lower()
        fin_text = re.sub('[^a-zA-Z0-9]+', ' ', fin_text)

        for token in fin_text.split():
            if len(token) > 2:
                token_lst.append(token)

    return token_lst

def add_to_postings(token, docId, token_frequency):
    #-------------
    # Adds the posting for a token.
    # If token exists, it adds a key and value
    # and if not, it creates a ordered dict
    #-------------

    global indexer_list
    if token not in indexer_list.keys():
        posting_dict = OrderedDict()
        posting_dict[docId] = token_frequency
        indexer_list[token] = posting_dict

    else:
        posting_dict = indexer_list[token]
        posting_dict[docId] = token_frequency
        indexer_list[token] = posting_dict

def frequency_calculation(unique_tokens,tags_dict):
    #-------------
    # Calculates the frequency count for each token and stores
    # the docId and the frequency in the indexer_list for
    # each document.
    #-------------

    for token in unique_tokens:
        token_frequency = 0
        if token in tags_dict['headers']:
            token_frequency += tags_dict['headers'][token]
        if token in tags_dict['p']:
            token_frequency += tags_dict['p'][token]
        
        add_to_postings(token, docId, token_frequency)

if __name__ == "__main__":

    counter_file = 0
    path_direc = "/Users/sarthakgupta/Desktop/Search-Engine-master/DEV"   
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
                            token=ps.stem(token)
                            if token not in unique_tokens:
                                unique_tokens.append(token)
                            count_tokens.append(token)
                            token_freq_dict[token]+=1
                            total_token_count +=1
                        tags_dict[tag] = token_freq_dict
                        num_unique_tokens += len(unique_tokens)
                    
                    frequency_calculation(unique_tokens,tags_dict)
                
                # Offloading 4 times 
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

    # ********** MERGING ************************** 
    file1 = "/Users/sarthakgupta/Search-Engine/0.txt"
    file2 = "/Users/sarthakgupta/Search-Engine/1.txt"
    file3 = "/Users/sarthakgupta/Search-Engine/2.txt"
    file4 = "/Users/sarthakgupta/Search-Engine/3.txt"
    merge_1 = "/Users/sarthakgupta/Search-Engine/{}.txt".format('merge_1')
    merge_2 = "/Users/sarthakgupta/Search-Engine/{}.txt".format('merge_2')
    final_merge = "/Users/sarthakgupta/Search-Engine/{}.txt".format('final_merge')
    merge_files(file1,file2,merge_1)
    merge_files(file3,file4,merge_2)
    merge_files(merge_1,merge_2,final_merge)
    
    
    print("************** FEEDBACK REPORT **************")
    print("Number of Indexed Documents:", docId)
    print("Number of Unique Words:", len(set(count_tokens)))
    complete_index_file = "/Users/sarthakgupta/Search-Engine/final_merge.txt"
    file_info = os.stat(complete_index_file)
    print("Complete Index File Size in KB: ", float(file_info.st_size) / 1024)
    print("************** FEEDBACK REPORT **************")
