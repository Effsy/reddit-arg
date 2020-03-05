import sys
import json
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt

submission_id = sys.argv[1]
filename = "./graphs/%s.json" % submission_id

with open(filename) as f:
    json_obj = json.load(f)
    graph = json_obj["graph"]

# draw graph
optionss = {
    'node_color': 'red',
    'node_size': 100,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 12,
}
G = nx.DiGraph(directed=True)
G.add_edges_from(graph)

nx.draw_networkx(G, arrows=True, options=optionss)

plt.show()

A = to_agraph(G)
print(A)
A.layout('dot')
filename_png = "./graphs/%s.png" % submission_id
A.draw(filename_png)