# reddit-arg

## Setup

Create python virtual environment and install dependencies
```bash
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
```

Download the (Wikipedia 100d glove word vectors)[https://nlp.stanford.edu/projects/glove/]
Save the file to `./word_vectors/glove.6B.100d.txt`

The relations model is a large file that must be downloaded separately here:

## Configuration

PRAW requires configuration. (Sign up for access to the Reddit API)[https://www.reddit.com/wiki/api#wiki_reddit_api_access] to retrieve the credentials.
Create a `praw.ini` file in the root directory, using your credentials where appropriate:

```bash
[arg-mining]
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
user_agent=USER_AGENT

; <OPTIONAL>
username=USERNAME
password=PASSWORD
```
## Running the Code

### Model Development Scripts

The notebooks contain the source code used to build the models and outline the process.

These should be run in any (jupyter notebook environment)[https://github.com/jupyter/notebook]

```bash
1_fetch_data_argument_detection.ipynb
2_eda_argument_detection.ipynb
3_argument_detection.ipynb
4_fetch_data_relations_identification.ipynb
5_relations_identification.ipynb
```

### Running the Argumentation Miner

The argumentation miner is a python script that can simply be run with:

```bash
python3 build_argument_graph.py <THREAD_ID>
```

This will build the argumentation graph for the thread ID provided. The thread ID for a reddit thread is a 6 character string can be found in the url of the post.

The graphs are stored in `./graphs/data/<THREAD_ID>.json` 

### Rendering the Graphs

A utility is provided for rendering the graphs for visualisation. This can be run with:

```bash
python3 draw_graph.py <THREAD_ID>
```

### Using the Argument Prediction and Relations Prediction Modules

## Source Code Structure

The models are stored in the ./models file 

...? is this necessary?