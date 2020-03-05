from argument_detection import ArgumentPredictor
from relations_identification import RelationsPredictor

import json
import re
import praw
import nltk
import sys

ap = ArgumentPredictor()
rp = RelationsPredictor()

# download dataset for sentence tokenizer
# nltk.download('punkt')

def clean_text(text):
    # Replace utf-8 single quotes with ascii apostrophes
    text = re.sub(r"(\u2018|\u2019)", "'", text)
    # Replace utf-8 double quotes with ascii double quotes
    text = re.sub(r"(\u201c|\u201d)", '"', text)
    
    return text

def clean_sentences(sentences):
    # Convert common utf-8 punctuation to ascii
    sentences = [clean_text(sentence) for sentence in sentences]
    # Split all sentences containing \n into separate sentences
    sentences = [split_args for sentence in sentences for split_args in sentence.splitlines()]
    # Remove whitespace from arguments and empty strings from thread list
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    # Remove duplicates from the list
    sentences = list(set(sentences))
    return sentences

# Create new praw instance with credentials from praw.ini
reddit_instance = praw.Reddit('arg-mining')

submission_id = sys.argv[1]

# Get submission instance
submission = praw.models.Submission(id=submission_id, reddit=reddit_instance)

# Remove "replace more" from comments results (expand full comment tree)
submission.comments.replace_more(limit=1)

pairs = []

# Get full comment tree under top level comments and add all argument pairs
for comment in submission.comments.list():

    # All arg sentences in the current comment
    comment_sentences = [sentence for sentence in nltk.sent_tokenize(comment.body)]
    comment_sentences = clean_sentences(comment_sentences)
    comment_sentences = [sentence for sentence in comment_sentences if ap.is_arg(sentence)]
    
    # All arg sentences in all replies to the current comment
    reply_sentences = [sentence for reply in comment.replies.list() for sentence in nltk.sent_tokenize(reply.body) ]
    reply_sentences = clean_sentences(reply_sentences)
    reply_sentences = [sentence for sentence in reply_sentences if ap.is_arg(sentence)]
    
    if reply_sentences:
        for comment_sentence in comment_sentences:
            for reply_sentence in reply_sentences:
                pairs.append((comment_sentence, reply_sentence))

# Predict relations for all pairs
arg_graph = [pair for pair, not_attacking in zip(pairs, rp.predict_relations(pairs)) if not not_attacking]


arg_graph_dict = {
    "id": submission_id,
    "title": submission.title,
    "graph": arg_graph
}

filename = "./graphs/%s.json" % submission_id
with open(filename, "w") as f:
    json.dump(arg_graph_dict, f)

print(arg_graph)