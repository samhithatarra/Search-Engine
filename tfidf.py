import math
import ast
from collections import OrderedDict

def calculate_normalized():
    
    #-------------
    # Calculates the normalizing score so as to convert 
    # the weight of the token and the document into a vector. 
    #-------------

    document_dict = {}
    corpus_size = 53387
    normalize = open(path + "normalize.txt","w")
    with open(path + "final_merge.txt","r") as merge_file:
        outer_dict = {}
        for token_dict in merge_file:
            outer_dict = {}
            inner_dict = OrderedDict()
            token_dict = ast.literal_eval(token_dict)
            key = [*token_dict.keys()][0]
            value = token_dict[key]

            for doc_id, posting in value.items():

                header_freq = posting[1]
                body_freq = posting[2]
                tf_idf = ((0.7*header_freq)+(0.3*body_freq))
                 
                if doc_id in document_dict:
                    document_dict[doc_id] = document_dict[doc_id] + (tf_idf*tf_idf)
                else:
                    document_dict[doc_id] = (tf_idf*tf_idf)

        normalize.write(str(document_dict))
    normalize.close()

def calculate_tf():

    #-------------
    # Calculates the tf score for the documents for a 
    # particular token.
    # STRUCTURE: {token:{dociD:[posting]},{dociD:[posting]},{dociD:[posting]}, token:{dociD:[posting]},....}
    # [posting] = [tf_score]
    #-------------

    document_dict = {}
    corpus_size = 53387
    # tf score for a token in a document 
    length_index = open(path+ "tf_doc_index.txt","w")
    normalize = open(path+ "normalize.txt","r")
    line = normalize.read()
    normalize_dict = ast.literal_eval(line)
    with open(path+ "final_merge.txt","r") as merge_file:
        
        for token_dict in merge_file:
            outer_dict = {}
            inner_dict = OrderedDict()
            token_dict = ast.literal_eval(token_dict)
            key = [*token_dict.keys()][0]
            value = token_dict[key]
            occurences_token = len(value.keys())
            idf_score = math.log((float(corpus_size)/(occurences_token)),10)

            for doc_id, posting in value.items():

                header_freq = posting[1]
                body_freq = posting[2]
                tf = ((0.7*header_freq)+(0.3*body_freq))
                normalize_ = math.sqrt(normalize_dict[doc_id])
    
                inner_dict[doc_id] = tf/normalize_

            outer_dict[key] = dict(inner_dict)
            
            length_index.write(str(outer_dict)+'\n')
    
    length_index.close()
    normalize.close()

def calculate_idf():

    #-------------
    # Calculates the idf score for the token so as to calculate the 
    # weight of the query and the token once the query is dispatched. 
    #-------------

    document_dict = {}
    corpus_size = 53387

    # idf score for a token to calculate the query weight
    idf_index = open(path+ "idf_token_index.txt","w")
    with open(path+ "final_merge.txt","r") as merge_file:
        
        outer_dict = {}
        for token_dict in merge_file:
            
            inner_dict = OrderedDict()
            token_dict = ast.literal_eval(token_dict)
            key = [*token_dict.keys()][0]
            value = token_dict[key]
            occurences_token = len(value.keys())
            idf_score = math.log((float(corpus_size)/(occurences_token)),10)

            outer_dict[key] = idf_score
        
        idf_index.write(str(outer_dict))
        idf_index.close()

def calculate_length():

    #-------------
    # Calculates the number of tokens a doc has so as 
    # to normalize the cosine scores. 
    #-------------
    document_dict = {}
    corpus_size = 53387
    
    length = open(path+ "length.txt","w")
    with open(path+ "final_merge.txt","r") as merge_file:
        outer_dict = {}
        for token_dict in merge_file:

            token_dict = ast.literal_eval(token_dict)
            key = [*token_dict.keys()][0]
            value = token_dict[key]

            for doc_id, posting in value.items():

                frequency = posting[0]
                if doc_id in outer_dict:
                    outer_dict[doc_id] +=frequency
                else:
                    outer_dict[doc_id] = frequency

        length.write(str(outer_dict))
    length.close()
  
if __name__ == "__main__":

    calculate_normalized()
    calculate_tf()
    calculate_idf()
    calculate_length()
    
    path = "Users/kamaniya/Documents/Search-Engine"

    # ************ INDEX OF INDEX (each token) ******************
    # creating an index of index that stores the line number of each token
    # so as to seek once the query is dispatched. 

    counter = 0
    index_of_index = {}
    f = open(path+ "tf_doc_index.txt",'r') 
    for line in f:
        counter+=1
        line = ast.literal_eval(line)
        line_key = [*line.keys()][0]
        index_of_index[line_key] = counter
    f.close()
   
    index_ = open(path+ "index_of_index_tf.txt",'w')
    index_.write(str(index_of_index))
    index_.close()