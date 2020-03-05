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

# nx.draw_networkx(G, 
#     arrows=True, 
#     pos=graphviz_layout(G), 
#     arrowsize=4, 
#     font_size=5, 
#     node_size=8000, 
#     alpha=0.8)

# plt.show()

# Write to png file
A = to_agraph(G)
A.layout('dot')
filename_png = "./graphs/rendered/%s.png" % submission_id
A.draw(filename_png)