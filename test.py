import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from brocs.algorithms import ConnectedSequential, BrooksAlgorithm
from brocs import graphs
from brocs.helpers import delta

cs = ConnectedSequential()
br = BrooksAlgorithm()

# g = graphs.fish()
g = graphs.path()
# g = graphs.fence()
# g = graphs.domek()
# g = graphs.lopata()

print(f"Delta of the graph G: {delta(g)}")
nx.draw(g, with_labels=True)
plt.show()
plt.clf()


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

random_colors = [
    rgb_to_hex(*np.random.choice(range(256), size=3))
    for _ in range(len(g))
]

cs_res = cs.color_graph(g)
cs_coloring = [random_colors[value] for value in cs_res]
print(f"Colors used (CS): {len(set(cs_res))}")

nx.draw(g, node_color=cs_coloring, with_labels=True)
plt.show()
plt.clf()

br_res = br.color_graph(g)
br_coloring = [random_colors[value] for value in br_res]
print(f"Colors used (Brooks): {len(set(br_res))}")

nx.draw(g, node_color=br_coloring, with_labels=True)
plt.show()
plt.clf()

