# reddit-arg

## Setup

Create virtualenv and install dependencies
```bash
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
```

## Configuration

PRAW requires configurations. Create a `praw.ini` file in the root directory as follows:

```bash
[arg-mining]
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
user_agent=USER_AGENT

; <OPTIONAL>
username=USERNAME
password=PASSWORD
```
## Run scripts

`python3 1_gather_data`
`python3 2_clean_data`
; `python3 3_gather_data`
; `python3 1_gather_data`
; `python3 1_gather_data`


1 gather data
subtask - label gathered data
2 clean data
3 extract features
4 classify labelled data
