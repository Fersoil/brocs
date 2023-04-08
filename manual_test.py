import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from brocs.algorithms import ConnectedSequential, BrooksAlgorithm
from brocs import graphs
from brocs.helpers import delta
from brocs.visualization import show_graph, show_colored_graph

cs = ConnectedSequential()
br = BrooksAlgorithm()

g = graphs.fish()
# g = graphs.path()
# g = graphs.fence()
# g = graphs.domek()
# g = graphs.lopata()
# g = graphs.bipartite()
# g = nx.graph_atlas(1200)


print(f"Delta of the graph G: {delta(g)}")
show_graph(g)



cs_res = cs.color_graph(g)
print(f"Colors used (CS): {len(set(cs_res))}")

show_colored_graph(g, cs_res)

br_res = br.color_graph(g)
print(f"Colors used (Brooks): {len(set(br_res))}")

show_colored_graph(g, br_res)

