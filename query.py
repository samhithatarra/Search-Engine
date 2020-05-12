#query.py
# https://stackoverflow.com/questions/620367/how-to-jump-to-a-particular-line-in-a-huge-text-file

from nltk.stem import PorterStemmer
import re
import ast 
import timeit

def get_seek():

    f = open("/Users/kamaniya/Documents/Search-Engine/final_merge.txt", 'r')
    line_offset = []
    offset = 0
    for line in f:
        line_offset.append(offset)
        offset += len(line)
    f.close()
    return(line_offset)

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
    return token_lst

def extract_posting(query_list):
    
    posting_list = []
    posting_dict = {}
    f = open("/Users/kamaniya/Documents/Search-Engine/final_merge.txt", 'r')
    line_offset = get_seek()
    #counter = 0
    for token in query_list:
        counter = 0
        f.seek(line_offset[index_of_index[token]-1])  # gives the line from where we have to start searching
        line = f.readline()  # reads the first line from where we have to start  after seek
        #print (line)
        '''if token[0] == 'z':
            last_line = ''
        elif token[0].isdigit():
            last_line = line_offset[index_of_index['a']]
        else:
            order_ = ord(token[0])+1
            f.seek(line_offset[index_of_index[chr(order_)]-1]) # this finds the last line -- where the loop should end. 
            last_line = f.readline()  # reads the last line
        f.seek(line_offset[index_of_index[token[0]]-1])  # gives the line from where we have to start searching
        line = f.readline()  # reads the first line from where we have to start  after seek
        line_found = 'place holder'  # random string - if we don't find the token
        while counter !=1:
            line = ast.literal_eval(line)
            token_found = [*line.keys()][0]
            if token == token_found:
                counter =1
                line_found = token_found
                break
            elif line == last_line:
                break
            line = f.readline()'''
        #if counter == 1:
            #line_found = line_found.strip()
        line = ast.literal_eval(line)
        dict_ = line
        key = [*dict_.keys()][0]
        value = dict_[key]
        #print(value)
        posting_dict[key] = value
        posting_list.append(posting_dict)

    #print (posting_dict)
    f.close()
    #return 
    find_query(posting_dict)
    #return posting_dict
    
def find_query(posting_dict):
    global start_time
    #stop = timeit.default_timer()
    list_docId =[]
    for token, posting in posting_dict.items():
        list_docId.append(set(posting.keys()))
    
    set_intersection  = set.intersection(*list_docId)
    stop = timeit.default_timer()
    print ("TIME:", (stop - start_time) * 1000, 'milliseconds')
    print()
    set_intersection = list(set_intersection)
    for i in range(0, 5):
        print(urls[set_intersection[i]])

if __name__ == "__main__":
    f2 = open("/Users/kamaniya/Documents/Search-Engine/urls.txt", 'r')
    line = f2.read()
    urls = ast.literal_eval(line)
    f2.close()
    start_time = timeit.default_timer()
    index_of_index = {}
    f = open("/Users/kamaniya/Documents/Search-Engine/index_of_index-1.txt", 'r')
    index = f.read()
    index_of_index = ast.literal_eval(index)
    query = get_query()
    extract_posting(query)
    f.close()
    print() 
 

  
