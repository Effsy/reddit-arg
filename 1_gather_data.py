import json

import praw

# Create new praw instance with credentials from praw.ini
reddit = praw.Reddit('arg-mining')

print(reddit.read_only)

arg = {}

for submission in reddit.subreddit('changemyview').hot(limit=10):
    print(submission.title)





with open('raw_arguments.json', 'w') as fp:
    json.dump(arg, fp)
