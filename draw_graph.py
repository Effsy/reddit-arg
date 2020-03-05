import os
import sys
import json
import textwrap

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt

submission_id = sys.argv[1]
filename = "./graphs/data/%s.json" % submission_id

with open(filename) as f:
    json_obj = json.load(f)
    graph = json_obj["graph"]

# Make sentences wrap for easier reading
for node in graph:
    node[0] = textwrap.fill(node[0], 30)
    node[1] = textwrap.fill(node[1], 30)

# draw graph
G = nx.DiGraph(directed=True)
G.add_edges_from(graph)

# Write to png file
A = to_agraph(G)

A.layout('dot')
filename_png = "./graphs/rendered/%s/dot.png" % submission_id

# Make dir if doesn't exist
os.makedirs(os.path.dirname(filename_png), exist_ok=True)
A.draw(filename_png)

A.layout('fdp')
filename_png = "./graphs/rendered/%s/fdp.png" % submission_id
A.draw(filename_png)

A.layout('sfdp')
filename_png = "./graphs/rendered/%s/sfdp.png" % submission_id
A.draw(filename_png)