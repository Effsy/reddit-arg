import json

with open('./raw_data/1000_raw_argument_sentences.json') as data_file:
    data = json.load(data_file)

row_id = 0

for row in data:
    row['id'] = row_id
    row_id += 1

print(data)

with open('./raw_data/1000_raw_argument_sentences_id.json', 'w') as fp:
    json.dump(data, fp)