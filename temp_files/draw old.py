import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

graph = nx.read_multiline_adjlist('self.graph.adjlist1', create_using=nx.DiGraph)

# options = {"node_size": 50, "linewidths": 0, "width": 0.18}
# nx.draw(graph, with_labels=True, **options)
# nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph), labels=lab, font_size=12)
# plt.show()

net = Network(notebook=True)
net.from_nx(graph)
net.show("res.html")
