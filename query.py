# https://stackoverflow.com/questions/620367/how-to-jump-to-a-particular-line-in-a-huge-text-file

from nltk.stem import PorterStemmer
import re


'''def get_query():
    query = input('Enter the query to be searched: ')
    return query

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
'''
def find_query():
    
    f = open("/Users/sarthakgupta/Search-Engine/0-.txt", 'r')
    #f.seek(100)
    #print (f.readline())
    #[0,100, 145,...]
    line_offset = []
    offset = 0
    for line in f:
        line_offset.append(offset)
        offset += len(line)
    f.seek(0)
    #counter = dict[a]
    #while counter!=line_offset(dict[b])
    token = 'unkdkdkf'
    print (index_of_index['a'])
    counter = 0
    if token[0] !='z':
        order_ = ord(token[0])+1
        f.seek(line_offset[index_of_index[chr(order_)]-1])
        last_line = f.readline()  # line that starts from v 
    else: 
        last_line = ''
    f.seek(line_offset[index_of_index[token[0]]-1]) #16223
    print (index_of_index['u'])
    line = f.readline() #16223
    line_found = 'place holder'
    while counter !=1:
        if token in line:
            counter =1
            line_found = line
            break
        if line == last_line:
            #print (last_line)
            break
        line = f.readline()
    print (line_found)
    
index_of_index = {}
f = open("/Users/sarthakgupta/Search-Engine/0-.txt",'r')
#counter = 0
alphabet = 'a'
line_number  = 0
ord_a = ord(alphabet)   #65x
index_of_index['numbers'] = 1
for line in f:
    line_number +=1
    if line.startswith("{'"+alphabet) :
        index_of_index[alphabet] = line_number
        alphabet = chr(ord(alphabet)+1)
        index_of_index[alphabet] = line_number
    if alphabet =='z':
        break
print (index_of_index)
find_query()
'''query = get_query()
token_lst = tokenize_query(query)
find_query(token_lst)'''
