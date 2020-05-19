import math
import ast
from collections import OrderedDict

def calculate_idf():
    # STRUCTURE: {token:{dociD:[posting]},{dociD:[posting]},{dociD:[posting]}}
    corpus_size = 55393
    # Idf score for a token
    tf_idf_index = open("/Users/kamaniya/Documents/Search-Engine/tfidf_index.txt","w")

    with open("/Users/kamaniya/Documents/Search-Engine/final_merge.txt","r") as merge_file:
        
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
                tf_idf = ((0.7*header_freq)+(0.3*body_freq))*idf_score 
                inner_dict[doc_id] = tf_idf

            outer_dict[key] = dict(inner_dict)
            
            tf_idf_index.write(str(outer_dict)+'\n')
            
    tf_idf_index.close()

if __name__ == "__main__":
    calculate_idf()
    index_of_index = {}
    counter = 0
    f = open("/Users/kamaniya/Documents/Search-Engine/tfidf_index.txt",'r') 
    for line in f:
        counter+=1
        line = ast.literal_eval(line)
        line_key = [*line.keys()][0]
        index_of_index[line_key] = counter
    f.close()
    index_index = open("/Users/kamaniya/Documents/Search-Engine/index_of_index_tf.txt",'w')
    index_index.write(str(index_of_index))
    index_index.close() 
    