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
for submission in reddit.subreddit('changemyview').new(limit=50):
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
    return text

for key, thread in arg_threads.items():
    arg_threads[key] = [clean_text(arg) for arg in thread]

# arg_threads = [clean_text(arg) for thread in arg_threads.values() for arg in thread]
print(arg_threads.values())

# Split all sentences containing \n into separate sentences
for key, thread in arg_threads.items():
    arg_threads[key] = [split_args for arg in thread for split_args in arg.splitlines()]

# Remove empty strings or whitespace from list
for key, thread in arg_threads.items():
    arg_threads[key] = [arg for arg in thread if arg.strip()]

# Check if string starts with: any number of whitespace, followed by >, followed by any number of whitespace
print(arg_threads.values())


#################### STORING ####################

# Take the first 10 threads that contain at least 100 arguments

for key, thread in list(arg_threads.items()):
    if len(thread) < 100:
        del arg_threads[key]
        del arg_titles[key]

args = [thread for thread in arg_threads.values()][:10]
arg_titles = [title for title in arg_titles.values()][:10]

# args = [thread for thread in arg_threads.values() if len(thread) >= 100][:10]

# Take a random sample of 100 arguments from each argument thread
args = [arg for thread in args for arg in random.sample(thread, 100)]

print(args)

# Write data to file

with open('./raw_data/1000_raw_argument_sentences_6.txt', 'w') as write_file:
    for arg in args:
        write_file.write(arg + '\n')

# Write titles to file

with open('./raw_data/argument_titles_6.txt', 'w') as write_file:
    for title in arg_titles:
        write_file.write(title + '\n')
