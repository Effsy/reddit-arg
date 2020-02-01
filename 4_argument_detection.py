#################### PREPARE DATA ####################

import unicodedata

import nltk

df_dtm = pd.read_pickle("dtm.pkl")
df_tdm = df_dtm.transpose()

# Normalize characters (e.g. accents or unicode inconsistencies)
arg = unicodedata.normalize('NFKD', arg)
arg = unicodedata.normalize('NFKD', arg).encode('ascii', 'ignore').decode('utf-8', 'ignore')


# Spelling correction

####### Feature Engineering ######

# n-gram / tf-idf

# Number of words (Sentence length)

# Reddit specific syntactic features - > **

# URLS?

# Parts of Speech number of each

# Sentiment - polarity and subjectivity

# Readability?



####### Model Attempts #######

# 


# Using 

# Test on models

# K nearest neighbours
# Naive Bayes
# Support Vector Machine
# Logistic Regression