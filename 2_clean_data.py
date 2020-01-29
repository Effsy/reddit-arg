import unicodedata

# Normalize characters with accents
# arg = unicodedata.normalize('NFKD', arg)
# arg = unicodedata.normalize('NFKD', arg).encode('ascii', 'ignore').decode('utf-8', 'ignore')

import json
import pandas as pd
import pickle

# Create dataframe
pd.set_option('max_colwidth', 190)
pd.set_option('display.max_rows', 1000)

data = []

with open('./labelled_data/1000_labelled_argument_sentences_8.json') as f:
    for line in f:
        json_line = json.loads(line)
        arg = {"text": json_line["content"], "label": json_line["annotation"]["labels"][0]}

        data.append(arg)

df = pd.DataFrame().from_dict(data, orient='columns')

print(df)

# Count number of args and not_args in dataframe
print(df[df["label"] == "arg"].count())
print(df[df["label"] == "not-arg"].count())

# Save 
df.to_pickle("corpus.pkl")
#

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words='english')
data_cv = cv.fit_transform(df.text)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = df.index
print(data_dtm)