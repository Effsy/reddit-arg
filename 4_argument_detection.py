import unicodedata

import pandas as pd
import nltk

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split


df_dtm_all = pd.read_pickle("dtm_all.pkl")
df_dtm = pd.read_pickle("dtm.pkl")
df_tdm = df_dtm.transpose()

#################### PREPARE DATA ####################
# print(df_dtm.loc[0])
# print(df_dtm.apply(lambda x: x))

# for row in df_tdm:
#     print([df_tdm[row].iloc[value] for value in df_tdm[row] if value == 0])
#     print(df_tdm[row])

# Normalize characters (e.g. accents or unicode inconsistencies)
# arg = unicodedata.normalize('NFKD', arg)
# arg = unicodedata.normalize('NFKD', arg).encode('ascii', 'ignore').decode('utf-8', 'ignore')


# Spelling correction



# Stem / lemmatize

# Create n-gram, create t-df

#################### FEATURE ENGINEERING ####################

print(df_dtm.shape())

# tfidfconverter = TfidfTransformer()
# x = tfidfconverter.fit_transform(x).toarray()

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
# classifier.fit(X_train, y_train) 

# words n-gram / tf-idf

# Number of words (Sentence length)

# print( df_dtm.sum(axis=1))

# print(df_dtm.sum(axis=1))
# print(df_dtm_all.sum(axis=1))
# print(df_dtm.iterrows())
# print(df_dtm[df_dtm == 1].apply(lambda x: x))


# Reddit specific syntactic features - > **

# URLS?

# Parts of Speech - BoW or tf-idf

# Sentiment - polarity and subjectivity

# Readability?


#################### MODEL ATTEMPTS ####################

# Using 

# Test on models

# K nearest neighbours
# Naive Bayes
# Support Vector Machine
# Logistic Regression