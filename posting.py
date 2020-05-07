class Posting:
    def __init__(self, docId, header_freq, body_freq, token_frequency):
        self.docId = docId
        self.header_freq = header_freq
        self.body_freq = body_freq
        #self.tf_idf_score = 0.0
        self.token_freq = token_frequency