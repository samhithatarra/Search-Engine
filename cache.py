import ast
    
def create_cache():
#-------------
# Creating a cache to store the posting lists of 
# frequently occurring tokens to speed up query time
# Creating the offset so as to seek a particular token baased on the line number 
# of the token saved in index_of_index_tf.txt. 
#-------------
    f = open(path + "tfidf_index.txt", 'r')
    
    cache_list = ['in','the','and','of','an','for','to','that','this','they',
                'there','if','are','is','was','be','or','not','will','where',"can", 'cannot', 'could', "couldn", 
                'did', "didn", 'do', 'does', "doesn", 'doing', "don",
                'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn", 'has', "hasn", 'have',
                'having', 'he', 'her', 'here', 'hers', 'herself', 'him','haven'
                'himself', 'his', 'how', "how's", 'into',
                "isn", 'it', 'its', 'itself', 'me', 'more', 'most', "mustn", 'my', 'myself',
                'no', 'nor', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
                'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she',
                'should', "shouldn", 'so', 'some', 'such', 'than', 'their', 'theirs',
                'them', 'themselves', 'then', 'there', 'these',
                'those', 'through', 'too', 'under', 'until', 'up', 'very', 'was', "wasn",
                'we', 'were', "weren", 'what', 'when',
                'where', 'which', 'while', 'who', 'whom', 'why', 'with', "won",
                'would', "wouldn", 'you', "ll", "re", "ve", 'your', 'yours', 'yourself',
                'yourselves' ]
    offset = 0
    for line in f:
        line_dict = ast.literal_eval(line)
        line_key = [*line_dict.keys()][0]
        if line_key in cache_list:
            cache_dict[line_key] = line_dict[line_key]
        line_offset.append(offset)
        offset += len(line)
    f.close()
    
    with open(path+"cache.txt",'w') as cache:
        cache.write(str(cache_dict))
    with open(path+"offset.txt",'w') as offset:
        offset.write(str(line_offset))
    
    #--------------------------
    # Storing the sum of the idf scores of the token 
    # so as to calculate the weight of the query and the token
    # when the query is dispatched.
    #--------------------------

    f1 = open(path + "query_weight.txt", 'w')
    weight_dict = {}
    for line in f:
        line_dict = ast.literal_eval(line)
        line_key = [*line_dict.keys()][0]
        for doc,tfidf in line_dict[line_key].items():
            if line_key in weight_dict:
                weight_dict[line_key] += tfidf
            else:
                weight_dict[line_key] = tfidf
    f1.write(str(weight_dict))
    
if __name__ == "__main__":
    
    line_offset = []
    cache_dict = {}
    path = "/Users/kamaniya/Documents/Search-Engine/"
    create_cache()