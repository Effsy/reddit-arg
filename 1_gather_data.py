import json
import re
import praw
import nltk
import random

# download dataset for sentence tokenizer
nltk.download('punkt')

#################### FETCHING ####################

# Create new praw instance with credentials from praw.ini
reddit = praw.Reddit('arg-mining')

# Threads and their arguments
# key = submission_id
# value = list of arguments
arg_threads = {}

arg_titles = {}

# Add sentences from submission title, body and comments to arg_threads array
for submission in reddit.subreddit('changemyview').hot(limit=50):
    # Add submission body and title to arg_threads[i]
    arg_threads[submission.id] = []
    arg_threads[submission.id] = arg_threads[submission.id] + nltk.sent_tokenize(submission.selftext)
    
    arg_titles[submission.id] = submission.title + " ID: " + submission.id

    # Remove "replace more" from comments results
    submission.comments.replace_more(limit=None)

    # Get full comment tree under top level comments and add to arg_threads
    for comment in submission.comments.list():
        arg_threads[submission.id] = arg_threads[submission.id] + nltk.sent_tokenize(comment.body)


#################### CLEANING ####################

# Convert common utf-8 punctuation to ascii
# Clean but still retain the exact same meaning of the text
def clean_text(text):
    # Replace utf-8 single quotes with ascii apostrophes
    text = re.sub(r"(\u2018|\u2019)", "'", text)
    # Replace utf-8 double quotes with ascii double quotes
    text = re.sub(r"(\u201c|\u201d)", '"', text)
    # Remove all asterisks (bold or italics)
    text = re.sub(r"\*", "", text)

    # Remove arguments starting with > or - (reddit markup for quotes or bullet points)
    # With spaces before or after
    text = re.sub(r"\s*>\s*", "", text)
    text = re.sub(r"\s*-\s*", "", text)
    
    return text

for key, thread in arg_threads.items():
    arg_threads[key] = [clean_text(arg) for arg in thread]



# Split all sentences containing \n into separate sentences
for key, thread in arg_threads.items():
    arg_threads[key] = [split_args for arg in thread for split_args in arg.splitlines()]

# Remove whitespace from arguments and empty strings from thread lists
for key, thread in arg_threads.items():
    arg_threads[key] = [arg.strip() for arg in thread if arg.strip()]

print(arg_threads.values())

# Remove duplicates from the lists
for key, thread in arg_threads.items():
    arg_threads[key] = list(set(thread))


#################### STORING ####################

# Take the first 20 threads that contain at least 100 arguments

for key, thread in list(arg_threads.items()):
    if len(thread) < 50:
        del arg_threads[key]
        del arg_titles[key]

args = [thread for thread in arg_threads.values()][:20]
arg_titles = [title for title in arg_titles.values()][:20]

# Take a random sample of 50 arguments from each argument thread
args = [arg for thread in args for arg in random.sample(thread, 50)]

print(args)

# Write data to file

with open('./raw_data/1000_raw_argument_sentences_1.txt', 'w') as write_file:
    for arg in args:
        write_file.write(arg + '\n')

# Write titles to file

with open('./raw_data/argument_titles_1.txt', 'w') as write_file:
    for title in arg_titles:
        write_file.write(title + '\n')
