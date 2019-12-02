import json
import re

import praw
import nltk

# download dataset for sentence tokenizer
nltk.download('punkt')

# Create new praw instance with credentials from praw.ini
reddit = praw.Reddit('arg-mining')

args = []

# Add setences from submission title, body and comments to args array
for submission in reddit.subreddit('changemyview').new(limit=10):
    # Add submission body and title to args
    args = args + nltk.sent_tokenize(submission.title) + nltk.sent_tokenize(submission.selftext)

    # Remove "replace more" from comments results
    submission.comments.replace_more(limit=0)

    # Get full comment tree under top level comments
    for comment in submission.comments.list():
        args = args + nltk.sent_tokenize(comment.body)

# Split all sentences containing \n into separate sentences
temp_array = []
for i, val in enumerate(args):
    split_args = val.splitlines()
    temp_array = temp_array + split_args
args = temp_array



# Convert common utf-8 punctuation to ascii
# Clean but still retain the exact same meaning of the text
def clean_text(text):
    # Replace utf-8 single quotes with ascii apostrophes
    text = re.sub(r"(\u2018|\u2019)", "'", text)
    # Replace utf-8 double quotes with ascii quotes
    text = re.sub(r"(\u201c|\u201d)", '"', text)
    return text

args = map(lambda x: clean_text(x), args)

# Write data to file
args_json = []

for arg in args:
    args_json.append({"text": arg})

with open('./raw_data/1000_raw_argument_sentences.json', 'w') as fp:
    json.dump(args_json, fp)
