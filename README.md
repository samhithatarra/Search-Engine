ABOUT
-------------------------
A search engine from the ground up that is capable of handling tens of thousands of JSON files given in the DEV folder, 
under harsh operational constraints, ranked through the cosine-similarity and having a query response time under 300ms.


ARCHITECTURE
-------------------------

### PYTHON FILES

**main.py**: 

- Finds significant HTML content from DEV json files
- Uses porter stemmer and tokenizer to create tokens for each URL
- Calculates frequencies to be used in TF-IDF calculation at a later time
- Offloads 4 times by creating partial indexes that contain the token and its associated posting list
- Stores a final merge of all posting lists
- Structure of index: 
  {token: {docID: [posting], docID: [posting], docID: [posting]}
  [posting] = [token_frequency(total_frequency), header frequency, body_frequency]


**merge.py**:

- Used to merge two files at a time and store the results in a separate text file

**tfidf.py**:

- Used lnc.ltc scheme to create normalizing scores for each document so as to convert the token 
  document weight into a vector and then use that to calculate 
  the tf score normalized for the document. 
- Structure of index: 
  - {token: {docID: [posting], docID: [posting], docID: [posting]}
  - [posting] = [tf_score]
- Calculate the IDF score for each token so as to calculate token query weight. 
- Calculate the length array so as to normalize the cosine scores for the documents retrieved after the query is entered.
- Makes index of index so as to seek posting lists when the query is dispatched. 


**cache.py**:

- Creates a dictionary of the posting lists of the frequently used words and 
  creates an offset to seek a particular token based on the line number of the 
  token saved in index_of_index_tf.txt

**query.py**:

- Takes user input for a query to be searched
- Uses porter stemmer and tokenizer to ensure query tokens are processed the same way documents were
- For each token in query input, a function calculates the query weight, 
  normalizes and finally determines cosine similarity scores 
- Has function to read and use cache dictionary to speed up query processing when possible
- Retrieves seek position dictionary to find tokens and their associated documents quickly
- Calculates query search time
- Returns 10 most relevant URLs to the user checking and removing any similar/exact URLs


**gui.py**:

- Extra credit GUI implementation using tkinter


### TEXT FILES

**0.txt, 1.txt, 2.txt and 3.txt**: Text files that store the partial indexes

**merge_1.txt and merge_2.txt**: Merges 0.txt, 1.txt and stores it in merge_1.txt; Merges 2.txt, 3.txt and 
stores it in merge_2.txt

**final_merge.txt**: Final merge that merges merge_1.txt and merge_2.txt files

**urls.txt**: A dictionary that contains a url and its associated doc ID

**normalize.txt**: A dictionary that contains documents and its associated normalizing weight

**tf_doc_index.txt**: A final index that has the structure: {token: 
{docID: [posting]}, {docID: [posting]}, {docID: [posting]....}
[posting] = [tf_score]

**idf_token_index.txt**: A dictionary that contains the token and its associated idf score 

**length.txt**: A dictionary that has the document as its key and the number of words in the document as its value

**index_of_index_tf.txt**: A dictionary that contains the token and its corresponding line number in the text file - index of index of the final index.

**cache.txt**: A dictionary that contains the posting lists of the frequently occurring terms

**offset.txt**: A text file that contains a list of the seek positions of a particular token




### AUTHORS

- Vaanya Gupta
- Kamaniya Sathish Kumar
- Vani Anilkumar
- Samhitha Tarra
