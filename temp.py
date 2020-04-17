
from relations_identification import RelationsPredictor

rp = RelationsPredictor()

relations = [("this sucks", "I love it"), ("this is great", "I hate it")]

print(rp.predict_relations(relations))