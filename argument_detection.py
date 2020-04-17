import joblib

import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import string

import numpy as np

class ArgumentPredictor():
    """A class used to predict whether a sentence is argumentative.
    
    The class requires the n-gram model to be stored in ./models/arg_detection_ngram_model.pkl
    The class requires the meta model to be stored in ./models/arg_detection_meta_model.pkl
    """

    def __init__(self):
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('vader_lexicon')

        self.ngram_model = joblib.load('./models/arg_detection_ngram_model.pkl')
        self.meta_model = joblib.load('./models/arg_detection_meta_model.pkl')
    
    def lemmatize_sentence(self, sentence):
        """Lemmatize all words in a sentence. Uses PoS to identify lemma"""
        wnl = WordNetLemmatizer()
        lemma_array = []
        # Adapted from: https://stackoverflow.com/a/39498745
        for word, tag in pos_tag(word_tokenize(sentence)):
            if tag.startswith("NN"):
                lemma_array.append(wnl.lemmatize(word, pos='n'))
            elif tag.startswith('VB'):
                lemma_array.append(wnl.lemmatize(word, pos='v'))
            elif tag.startswith('JJ'):
                lemma_array.append(wnl.lemmatize(word, pos='a'))
            else:
                lemma_array.append(word)

        return ' '.join(lemma_array)

    # Extract features from a sentence
    def extract_features(self, sentence):
        # Predictions based on ngrams from classifier trained on all data       

        # Lemmatize
        sentence_lemma = [self.lemmatize_sentence(sentence)]
        
        # Predict using the ngram model
        ngram_prediction = 1 if self.ngram_model.predict(sentence_lemma)[0] == "arg" else 0
        
        # Sentiment of sentence
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(sentence)['compound']
        
        # Sentence Length
        sentence_length = len(word_tokenize(sentence))
        
        # Number of each parts of speech
        pos_counts = []
        nn = 0
        vb = 0
        jj = 0
        for word, pos in pos_tag(word_tokenize(sentence)):
            if pos.startswith('NN'):
                nn += 1
            elif pos.startswith('VB'):
                vb += 1
            elif pos.startswith('JJ'):
                jj += 1
        pos_counts.append([nn, vb, jj])
        
        # Combine features into numpy matrix
        return np.column_stack([ngram_prediction, sentiment, sentence_length, pos_counts])

    def predict_argument(self, sentence):
        """Predicts whether a single argument is argumentative.
        
        returns a string "arg" if argumentative or "not_arg" if not argumentative
        """

        # Remove punctuation
        sentence_cleaned = sentence.translate(str.maketrans('', '', string.punctuation))
        features = self.extract_features(sentence_cleaned)

        return self.meta_model.predict(features)[0]

    def is_arg(self, sentence):
        """Predicts whether a single argument is argumentative."""
        
        return self.predict_argument(sentence) == "arg"
