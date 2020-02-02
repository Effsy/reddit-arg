import json
import pandas as pd
import pickle

# Create dataframe from labelled data
pd.set_option('max_colwidth', 190)
pd.set_option('display.max_rows', 1000)

data = []

with open('./labelled_data/1000_labelled_argument_sentences_8.json') as f:
    for line in f:
        json_line = json.loads(line)
        arg = {"text": json_line["content"], "label": json_line["annotation"]["labels"][0]}

        data.append(arg)

df = pd.DataFrame().from_dict(data, orient='columns')

# Remove stop words separately

#################### STORE ####################

# Save unaltered corpus
df.to_pickle("corpus.pkl")

# Tokenize with count vectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Without stop words
cv = CountVectorizer(stop_words='english')
df_cv = cv.fit_transform(df.text)
df_dtm = pd.DataFrame(df_cv.toarray(), columns=cv.get_feature_names())
df_dtm.index = df.index

df_dtm.to_pickle("dtm.pkl")

# With stop words
cv_all = CountVectorizer()
df_cv_all = cv_all.fit_transform(df.text)
df_dtm_all = pd.DataFrame(df_cv_all.toarray(), columns=cv_all.get_feature_names())
df_dtm_all.index = df.index

df_dtm_all.to_pickle("dtm_all.pkl")