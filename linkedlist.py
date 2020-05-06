from node import Node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def sorted_add_node(self, docId, header_freq, body_freq, token_frequency):
        new_node = Node(docId, header_freq, body_freq, token_frequency)

        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
            
    
    def calculate_tfidf(self, idf):
        current = self.head
        while current != None:
            # TF-IDF(headers) *0.7 + TF-IDF(body) *0.3 
            tf_idf = (current.header_freq*idf*0.7)+(current.body_freq*idf*0.3)
            current.tf_idf_score = tf_idf
            current = current.next 
            
    
    def len_of_list(self):
        len_list = 0
        current = self.head
        while current != None:
            len_list += 1
            current = current.next 
        return len_list
    

    def print_func(self):
        current = self.head
        while current != None:
            if current.docId!=None:
                print(current.docId, '->', current.token_freq)
                print(current.docId, "HEADER SCORE:", current.header_freq, "BODY SCORE:", current.body_freq, "TF-IDF SCORE:", current.tf_idf_score)
            current = current.next