from argument_detection import ArgumentPredictor
from relations_identification import RelationsPredictor

import os
import json
import re
import praw
import nltk
import argparse
import itertools

import networkx as nx
from networkx.readwrite import json_graph

def clean_text(text):
    # Replace utf-8 single quotes with ascii apostrophes
    text = re.sub(r"(\u2018|\u2019)", "'", text)
    # Replace utf-8 double quotes with ascii double quotes
    text = re.sub(r"(\u201c|\u201d)", '"', text)
    # Remove > or - at beginning of sentences(reddit markup for quotes or bullet points)
    # with spaces before or after
    text = re.sub(r"\s*>\s*", "", text)
    text = re.sub(r"\s*-\s*", "", text)
    # Remove double backslash
    text = re.sub(r"\\+", "", text)
    
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

def pair_comments_and_replies(submission):
    pairs = []

    # All arguments in the submission body
    body_sentences = [sentence for sentence in nltk.sent_tokenize(submission.selftext)]
    body_sentences = clean_sentences(body_sentences)
    body_sentences = [sentence for sentence in body_sentences if ap.is_arg(sentence)]
    body_sentences.append(clean_text(submission.title))
    
    # All arguments in all comments
    comment_sentences = []
    for comment in submission.comments.list():
        comment_sentences = [sentence for sentence in nltk.sent_tokenize(comment.body)]
        comment_sentences = clean_sentences(comment_sentences)
        comment_sentences = [sentence for sentence in comment_sentences if ap.is_arg(sentence)]

    pairs = list(itertools.product(body_sentences, comment_sentences))

    # Get full comment tree under top level comments and add all argument pairs
    for comment in submission.comments.list():

        # All arguments in the current comment
        comment_sentences = [sentence for sentence in nltk.sent_tokenize(comment.body)]
        comment_sentences = clean_sentences(comment_sentences)
        comment_sentences = [sentence for sentence in comment_sentences if ap.is_arg(sentence)]
        
        # All arguments in all replies to the current comment
        reply_sentences = [sentence for reply in comment.replies.list() for sentence in nltk.sent_tokenize(reply.body) ]
        reply_sentences = clean_sentences(reply_sentences)
        reply_sentences = [sentence for sentence in reply_sentences if ap.is_arg(sentence)]

        pairs = pairs + list(itertools.product(comment_sentences, reply_sentences))

    return list(pairs)

def pair_all_arguments(submission):
    
    # All arguments in the submission body
    body_sentences = [sentence for sentence in nltk.sent_tokenize(submission.selftext)]
    body_sentences = clean_sentences(body_sentences)
    body_sentences = [sentence for sentence in body_sentences if ap.is_arg(sentence)]
    body_sentences.append(clean_text(submission.title))
    
    sentences = body_sentences
    
    # All arguments in all comments
    for comment in submission.comments.list():
        comment_sentences = [sentence for sentence in nltk.sent_tokenize(comment.body)]
        comment_sentences = clean_sentences(comment_sentences)
        comment_sentences = [sentence for sentence in comment_sentences if ap.is_arg(sentence)]
        
        sentences = sentences + comment_sentences
    pairs = itertools.permutations(sentences, 2)
    return list(pairs)

from time import time
start = time()

# Parse arguments from command line
parser = argparse.ArgumentParser(description='Generate an argument graph for a thread in the subreddit Change My View (CMV).')
parser.add_argument('id', help='the maximum number of comments deep')
parser.add_argument('-M', action='store_true', 
    help='the pairing mode. By default, all possible pairs are made. Set the flag to only pair replies with comments.')
parser.add_argument('--depth', type=int, nargs='?', help='the maximum number of comments deep.')
# parser.add_argument('--prune', nargs='?', type=int, default=0, help='the minimum degree of a node. If a node has less than the specified degree, it is pruned.')

args = parser.parse_args()
print(args)

# Instantiate Models
ap = ArgumentPredictor()
rp = RelationsPredictor()

# Download dataset for sentence tokenizer
nltk.download('punkt')

# Create new praw instance with credentials from praw.ini
reddit_instance = praw.Reddit('arg-mining')
submission_id = args.id

# Get submission instance
submission = praw.models.Submission(id=submission_id, reddit=reddit_instance)

# Remove "replace more" from comments results (expand full comment tree)
submission.comments.replace_more(limit=args.depth)

# Extract pairs of arguments from thread
pairs = None
if args.M:
    # Pair all arguments
    pairs = pair_comments_and_replies(submission)
else:
    pairs = pair_all_arguments(submission)

print("number of pairs")
print(len(pairs))




print("got pairs in")
print((time() - start)/60)

# Predict relations for all pairs (predict_relations returns false if attacking)
arg_graph = itertools.compress(pairs, rp.predict_relations(pairs))

print("got relations in")
print((time() - start)/60)

# arg_graph = [pair for pair, not_attacking in zip(pairs, rp.predict_relations(pairs)) if not not_attacking]

# Swap pairs (in directed graphs, typically the first node points to the second)
arg_graph = [(pair[1], pair[0]) for pair in arg_graph]

print("swapped pairs in")
print((time() - start)/60)

# Remove duplicates
arg_graph = list(set(arg_graph))
print("removed duplicates in")
print((time() - start)/60)

# Generate NetworkX graph
G = nx.DiGraph(directed=True)
G.add_edges_from(arg_graph)

print("num of nodes")
print(G.number_of_nodes())

# Save to json file
arg_graph_dict = {
    "id": submission_id,
    "title": submission.title,
    "tuple_graph": arg_graph,
    "adjacency_graph": json_graph.adjacency_data(G)
}

filename = f"./graphs/data/{submission_id}/{submission_id}.json"

# Make dir if doesn't exist
os.makedirs(os.path.dirname(filename), exist_ok=True)

with open(filename, "w") as f:
    json.dump(arg_graph_dict, f)

# Save to graph format
nx.write_gexf(G, f"./graphs/data/{submission_id}/{submission_id}.gexf")

# # Save to adjacency list
# nx.write_adjlist(G, "./graphs/data/%s/%s" % submission_id)


print("total time in minutes")
print((time() - start)/60)