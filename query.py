#query.py
# https://stackoverflow.com/questions/620367/how-to-jump-to-a-particular-line-in-a-huge-text-file

from nltk.stem import PorterStemmer
import re
import ast 
import timeit
from orderedset import OrderedSet

def get_seek():
    global line_offset
    global cache_dict
    f = open(path +"tfidf_index.txt", 'r')
    
    offset = 0
    for line in f:
        line_dict = ast.literal_eval(line)
        line_key = [*line_dict.keys()][0]
        if line_key == 'of' or line_key == "the" or line_key == "and":
            cache_dict[line_key] = line_dict[line_key]
        line_offset.append(offset)
        offset += len(line)
    f.close()

    #return (line_offset)

def get_query():
    
    query = input('Enter the query to be searched: ')
    global start_time 
    start_time =  timeit.default_timer()
    query_lst = tokenize_query(query)
    return query_lst

def tokenize_query(query):

    ps = PorterStemmer()
    token_lst = []
    q_text = query.lower()
    q_text = re.sub('[^a-zA-Z0-9]+',' ', str(q_text))

    for token in q_text.split():
        if len(token) >= 2:
            token=ps.stem(token)
            token_lst.append(token)
    #print (toe)
    return token_lst

def extract_posting(query_list):
    global start_time
    global cache_dict
    #posting_list = []
    posting_dict = {}
    f = open(path+"tfidf_index.txt", 'r')

    #line_offset = get_seek()
    #try:

    for token in query_list:
            # print (token)
        counter = 0
        
            # Gives the line from where we have to start searching
        
        if token in index_of_index: 
        #try:
            if token not in cache_dict:
                f.seek(line_offset[index_of_index[token]-1])  
                # Reads the first line from where we have to start  after seek
                line = f.readline()  
                line = ast.literal_eval(line)
                dict_ = line
                #key = [*dict_.keys()][0]
                value = dict_[token]
                posting_dict[token] = dict(sorted(value.items(), key = lambda x:x[1], reverse = True)) #value
            
                #print (posting_dict[key])
                #print()
                #posting_list.append(posting_dict)
            #except:
                #print ("query not in the index")
                #f.close()
            else:
                value = cache_dict[token]
                posting_dict[token] = dict(sorted(value.items(), key = lambda x:x[1], reverse = True)) #value
                #posting_list.append(posting_dict)
    f.close()
    if (posting_dict!={}):
        #print("HERE", posting_list)
        #stop = timeit.default_timer()
        #print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
        find_query(posting_dict)

def find_query(posting_dict):
    
    global start_time
    list_docId =[]
    #print(posting_dict)
    #print()
    #print("HERE")
    index = -1
    final_index = 0
    length = 1000
   
    #stop = timeit.default_timer()
    #print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
    for token, posting in posting_dict.items():

        set_ = OrderedSet(posting.keys())
        #print("SET", set_)
        index += 1
        if len(set_) < length:
            final_index = index 
            length = len(set_)
        list_docId.append(set_)
  
    #list_docId.sort(key=len)
    
    set_intersection = list_docId[final_index]
    list_docId.pop(final_index)
    #stop = timeit.default_timer()
    #print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
    list_docId = sorted(list_docId, key=len)
    #stop = timeit.default_timer()
    #print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
    #list_docId.sort(key=len)
    #print (list_docId)
    if len(list_docId) >= 1:
        for sets in list_docId:
            set_intersection = set_intersection.intersection(sets)
            #set_intersection = set_intersection & sets
    #set_intersection  = set.intersection(*list_docId)
    #print (set_intersection)
    stop = timeit.default_timer()
    print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
    print()
    set_intersection = list(set_intersection)
    # print (set_intersection)
    

    url = 0
    while len(set_intersection) > url and url < 5:

        print(urls[set_intersection[url]])
        url = url + 1

if __name__ == "__main__":
    line_offset = []
    cache_dict = {}
    path = "/Users/kamaniya/Documents/Search-Engine/"
    
    f2 = open(path+"urls.txt", 'r')
    line = f2.read()
    urls = ast.literal_eval(line)
    f2.close()
    start_time = timeit.default_timer()
    
    index_of_index = {}
    f = open(path+"index_of_index_tf.txt", 'r')
    index = f.read()
    index_of_index = ast.literal_eval(index)
    get_seek()
    query = get_query()
    extract_posting(query)
    print()
    f.close()