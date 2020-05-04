from node import Node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def sorted_add_node(self, docId, header_freq, body_freq, token_frequency):
        new_node = Node(docId, header_freq, body_freq, token_frequency)
        
        # if this is the first node, make the head and tail point to the first node
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            #if the new value is smaller than head make it the new head
            if docId < self.head.docId:
                new_node.next = self.head
                self.head = new_node
            else:
                
                #store the previous pointers starting with head
                previous = self.head
                
                #go through list to find place to add (go through all smaller numbers and move previous) 
                #make sure to stop if the end of the list is reached 
                while previous.docId < new_node.docId and previous.next != None and previous.next.docId < new_node.docId:
                    #print('made', previous.docID)
                    previous = previous.next 
                
                #if end of the loop is reached then add the new node as the last one and update tail 
                if previous.next == None:
                    previous.next = new_node
                    self.tail = new_node
                else:
                    #otherwise insert new node in between previous and previous.next
                    prev_next = previous.next
                    previous.next = new_node
                    new_node.next = prev_next
                
    
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
                #print(current.docId, "HEADER SCORE:", current.header_freq, "BODY SCORE:", current.body_freq, "TF-IDF SCORE:", current.tf_idf_score)
            current = current.next