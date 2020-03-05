import string

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences



class RelationsPredictor():
    
    MAX_NUM_WORDS = 50000
    MAX_SEQUENCE_LENGTH = 200
    
    def __init__(self):
        self.rel_model = load_model('./models/rel_identification_model.h5')
        self.word_index = self.init_word_index()

    # Lemmatize all words in a sentence. Uses PoS to identify lemma
    def init_word_index(self):
        embeddings_index = {}
        with open('./word_vectors/glove.6B.100d.txt') as f:
            for line in f:
                if len(embeddings_index) >= RelationsPredictor.MAX_NUM_WORDS:
                    break
                values = line.split()
                word = values[0]
                value = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = value

        word_index = {w: i for i, w in enumerate(embeddings_index.keys(), 1)}
        return word_index

    def text_to_sequence(self, text):
        tokens = text_to_word_sequence(text)
        return [self.word_index.get(w) for w in tokens if w in self.word_index]

    # Predict the relation (attack or neither)
    # attack = 0
    # neither = 1
    def predict_relation(self, originator, responder):
        originator_data = pad_sequences([self.text_to_sequence(originator)], maxlen=RelationsPredictor.MAX_SEQUENCE_LENGTH)
        responder_data = pad_sequences([self.text_to_sequence(responder)], maxlen=RelationsPredictor.MAX_SEQUENCE_LENGTH)
        
        predictions = self.rel_model([originator_data, responder_data])[0]
        return np.argmax(predictions)


