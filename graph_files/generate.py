from pathlib import Path

import networkx as nx
import numpy as np

from brocs.graphs import bipartite, fence, fish, path


def write_graph_to_file(graph: nx.Graph, name: str):
    path = Path(__file__).parent / f"{name}.npy"
    if path.exists():
        print("Warning: File already exists, overwriting")
    matrix = nx.adjacency_matrix(graph).toarray()
    np.save(path, matrix)


if __name__ == "__main__":
    graph_creators = [fish, path, fence, bipartite]
    for graph_creator, name in zip(
        graph_creators, ["fish", "path", "fence", "bipartite"]
    ):
        write_graph_to_file(graph_creator(), name)
