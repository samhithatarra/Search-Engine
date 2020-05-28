# ---- Sources Used ----
# https://stackoverflow.com/questions/620367/how-to-jump-to-a-particular-line-in-a-huge-text-file
# -----------------------

from nltk.stem import PorterStemmer
import re
import ast 
import timeit
from orderedset import OrderedSet
from collections import defaultdict
import math

def get_cache():

    # -------------
    # Reading the cache dictionary
    # -------------
    global cache_dict
    f = open(path +"cache.txt", 'r')
    cache_ = f.read()
    cache_dict = ast.literal_eval(cache_)
   
    f.close()

def get_seek():
    
    #------------
    # Stores the seek position dictionary in 
    # line_offset. 
    #-------------
    
    global line_offset
    f = open(path +"offset.txt", 'r')
    line_ = f.read()
    line_offset = eval(line_)
    f.close()

def get_query(query_):
    # ------------
    # Taking in search input from the user 
    # tokenizing the query and starting the timer
    # -------------
    
    query = query_
    global start_time 
    start_time =  timeit.default_timer()
    query_lst = tokenize_query(query)
    return query_lst
# 
def tokenize_query(query):

    #-------------
    # Tokenizes the query that the user enters
    # and returns a list of tokens present in the query
    # after stemming.
    #-------------
    
    ps = PorterStemmer()
    token_lst = []
    q_text = query.lower()
    q_text = re.sub('[^a-zA-Z0-9]+',' ', str(q_text))

    for token in q_text.split():
        if len(token) >= 2:
            token=ps.stem(token)
            token_lst.append(token)
    return token_lst

def extract_posting(query_list):
    
    # ------------
    # For each token in the query list we calculate the query weight
    # and storing it in a dictionary. Then we normalize the query token weights
    # and calculate cosine similarity
    # -------------
    global start_time
    global cache_dict
    global score_dict
    posting_dict = {}
    f = open(path+"tf_doc_index.txt", 'r')

    query_weight = 0
    normalize = 0
    token_dict = {}

    # Calculating the weight of the token,query
    for token in set(query_list):
        
        tf = 1+math.log(query_list.count(token))
        idf = weights[token]
        query_weight =  tf * idf
        token_dict[token] = query_weight

    # Normalizing the weight of the token,query
    for token,token_weight in token_dict.items():
        normalize  += token_weight * token_weight
    normalize = math.sqrt(normalize)

    for token in set(query_list):

        weight_token = token_dict[token]/normalize
        
        # If the token exists in the index then we move further. 
        if token in index_of_index: 
        
            if token not in cache_dict:
                
                f.seek(line_offset[index_of_index[token]-1])  
                line = f.readline()  
                line = ast.literal_eval(line)                  
                dict_ = line
                value = dict_[token]
                posting_dict[token] = dict(sorted(value.items(), key = lambda x:x[1], reverse = True)) 
        
            else:

                value = cache_dict[token]
                posting_dict[token] = dict(sorted(value.items(), key = lambda x:x[1], reverse = True)) 
            
            # Calculating cosine similarity and saving it inside score_dict
            for docID, weight_doc in value.items():
                if docID in score_dict:
                    score_dict[docID] += weight_doc * weight_token
                else:
                    score_dict[docID] = weight_doc * weight_token
    
    f.close()
    if (posting_dict!={}):
        return(find_query(posting_dict))

def find_query(posting_dict):
    
    #-------------
    # We sort the posting and intersect the two posting sets one at a time 
    # based on the increasing order of the length of the posting list for 
    # each token.
    #-------------
    
    global start_time
    
    list_docId =[]
    index = -1
   
    for token,posting in sorted(posting_dict.items(), key = lambda x: len(x[1])):
        
        set_ = OrderedSet(posting.keys())
        list_docId.append(set_)
  
    # Set intersection of the posting lists for term in the query in
    # increasing order of length of the list.

    set_intersection = list_docId[0]
    list_docId.pop(0)
    list_docId = sorted(list_docId, key=len)
    if len(list_docId) >= 1:
        for sets in list_docId:
            set_intersection = set_intersection.intersection(sets)
           
    # Calculating Time
    stop = timeit.default_timer()
    print()
    time_ = stop - start_time
    print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
    print()
    set_intersection = list(set_intersection)

    count =0
    list_= ''
    list_+= 'TIME: '+str(time_*1000)+'\n'
    
    # Normalising the total score of the document for the query entered. 
    for doc, score in score_dict.items():
       
        doc_score = score_dict[doc]
        score_dict[doc] = doc_score/length_[doc] 
   
    # Extracting top 5 URLS and 
    # checking exact similarity(Extra Credit)
    exact_checking = []
    for doc, score in sorted(score_dict.items(), key = lambda x:x[1], reverse = True):
        if score not in exact_checking:
            if doc in set_intersection:
                list_+=str(urls[doc])+'\n' 
                print (urls[doc],'** SCORE: **',score)
                count+=1
            elif len(set_intersection)<=count:
                print (urls[doc],'** SCORE: **',score)
                count+=1
            if count == 5:
                break
            exact_checking.append(score)
    return list_
        

score_dict = {}
line_offset = []
cache_dict = {}

path = "/Users/kamaniya/Documents/Search-Engine/"

# For printing out the URL's
f2 = open(path+"urls.txt", 'r')
line = f2.read()
urls = ast.literal_eval(line)
f2.close()
start_time = timeit.default_timer()

# For extracting the posting list 
index_of_index = {}
f = open(path+"index_of_index_tf.txt", 'r')
index = f.read()
index_of_index = ast.literal_eval(index)
f.close()

# For getting the weights of the token
# so as to calculate the token, query weight
weight = {}
f = open(path+"idf_token_index.txt", 'r')
weight_query = f.read()
weights = ast.literal_eval(weight_query)
f.close()

# For normalizing the final scores of the 
# document so that the documents are ranked 
# irrespective of the number of words the 
# document has. 
f = open(path+"length.txt", 'r')
len_ = f.read()
length_ = ast.literal_eval(len_)
f.close()

get_cache()
get_seek()

if __name__ == "__main__":

    choice = 'y'
    while choice == 'y':
        query__ = input('Enter the query to be searched: ')
        query = get_query(query__)
        extract_posting(query)
        print()
        choice = input('Do you want to search another term? (y/n): ')
        score_dict = {}
