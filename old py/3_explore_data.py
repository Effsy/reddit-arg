import pandas as pd

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import wordcloud

import matplotlib.pyplot as plt
# plt.show()
pd.set_option('max_colwidth', 190)
pd.set_option('display.max_rows', 5000)
# Read document-term matrix
df_dtm = pd.read_pickle("dtm.pkl")
df_tdm = df_dtm.transpose()

# Read corpus
df = pd.read_pickle("corpus.pkl")

#################### EXPLORE DATA ####################

# Number of args and not-arg
print("number of arg labels: " + str(len(df[df["label"] == "arg"])))
print("number of not-arg labels: " + str(len(df[df["label"] == "not-arg"])))

####### Sentence length #######

dtm_arg = df_dtm.loc[df.index[df["label"] == "arg"].tolist()]
dtm_notarg = df_dtm.loc[df.index[df["label"] == "not-arg"].tolist()]

print("argument sentence length: " + str(dtm_arg.sum(axis=1).mean()))
print("not argument sentence length: " + str(dtm_notarg.sum(axis=1).mean()))

####### Most Common Words #######

# Quantitative Representation
print(dtm_arg.sum().sort_values(ascending=False).head(30))
print(dtm_notarg.sum().sort_values(ascending=False).head(30))

# Visual Representation

df_arg = df[df["label"] == "arg"]
df_notarg = df[df["label"] == "not-arg"]
concat_arg = " ".join(arg for arg in df_arg.text)
concat_notarg = " ".join(arg for arg in df_notarg.text)

wordcloud_arg = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(concat_arg)
wordcloud_notarg = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(concat_notarg)

plt.imshow(wordcloud_arg, interpolation='bilinear')
plt.axis("off")
# plt.show()

plt.imshow(wordcloud_notarg, interpolation='bilinear')
plt.axis("off")

# Full vocabulary of dataset
print(pd.DataFrame(dtm_arg.sum()))