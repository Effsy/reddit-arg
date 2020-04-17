import string

import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences

class RelationsPredictor():
    """A class used to predict the relations between arguments.
    
    The class requires the relations model to be stored in ./models/rel_identification_model.h5
    The class requires the word embeddings to be stored in ./word_vectors/glove.6B.100d.txt
    """

    # Constants - must be the same as the model constants
    MAX_NUM_WORDS = 50000
    MAX_SEQUENCE_LENGTH = 200
    
    def __init__(self):
        self.rel_model = load_model('./models/rel_identification_model.h5')
        self.word_index = self.init_word_index()

    def init_word_index(self):
        """Initialise the word index from the glove embeddings"""

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
        """Convert a string to a sequence of integers according to the word index"""
        tokens = text_to_word_sequence(text)
        return [self.word_index.get(w) for w in tokens if w in self.word_index]

    def texts_to_sequences(self, texts):
        """Convert each string in a list to a sequence of integers according to the word index"""
        sequences = []
        for text in texts:
            tokens = text_to_word_sequence(text)
            sequences.append([self.word_index.get(w) for w in tokens if w in self.word_index])
        return sequences

    
    def predict_relation(self, originator, responder):
        """Predict the relation for a single pair
        
        neither = 0
        attack = 1
        """
        originator_data = pad_sequences([self.text_to_sequence(originator)], maxlen=RelationsPredictor.MAX_SEQUENCE_LENGTH)
        responder_data = pad_sequences([self.text_to_sequence(responder)], maxlen=RelationsPredictor.MAX_SEQUENCE_LENGTH)
        
        # Predict (attack = 0, neither = 1)
        predictions = self.rel_model([originator_data, responder_data])[0]
        
        # Flip values for neither and attack (improves usability)
        return not np.argmax(predictions)

    def predict_relations(self, pairs):
         """Predict the relation for a list of pairs
        
        neither = 0
        attack = 1
        """

        # Extract data for each branch
        originator_sentences = [sentence[0] for sentence in pairs]
        responder_sentences = [sentence[1] for sentence in pairs]
        print("working")
        originator_data = pad_sequences(self.texts_to_sequences(originator_sentences), maxlen=RelationsPredictor.MAX_SEQUENCE_LENGTH)
        responder_data = pad_sequences(self.texts_to_sequences(responder_sentences), maxlen=RelationsPredictor.MAX_SEQUENCE_LENGTH)
        
        # Predict (attack = 0, neither = 1)
        predictions = self.rel_model([originator_data, responder_data])
        predictions = np.argmax(predictions, axis=1).tolist()

        # Flip values for neither and attack (improves usability)
        predictions = [not i for i in predictions]
        return predictions
