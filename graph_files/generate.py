from pathlib import Path

import networkx as nx
import numpy as np
from random import choices as choices

from brocs.graphs import (
    bipartite,
    fence,
    fish,
    path,
    erdos_renyi,
    twin_kite,
    double_twin_kite,
    diamond,
    cavemen,
    random_gen,
    dense_random_gen,
)


def write_graph_to_file(graph: nx.Graph, name: str, random: bool = False):
    dir = Path(__file__).parent
    if random:
        dir = dir.parent / "random_graph_files"

    path = dir / f"{name}.npy"
    if path.exists():
        print("Warning: File already exists, skipping")
        return 

    matrix = nx.adjacency_matrix(graph).toarray()
    np.save(path, matrix)


def main() -> None:
    graph_creators = [
        fish,
        path,
        fence,
        bipartite,
        erdos_renyi,
        twin_kite,
        double_twin_kite,
        diamond,
        cavemen,
    ]
    for graph_creator, name in zip(
        graph_creators,
        [
            "fish",
            "path",
            "fence",
            "bipartite",
            "erdos_renyi",
            "twin_kite",
            "double_twin_kite",
            "diamond",
            "cavemen",
        ],
    ):
        write_graph_to_file(graph_creator(), name)

    for n_nodes in [10, 20, 50, 100, 200, 500]:
        for n_edges in [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]:
            if n_edges > n_nodes * (n_nodes - 1) / 2:
                continue

            random_graphs = [random_gen(n_nodes, n_edges) for _ in range(20)]
            random_dense_graphs = [dense_random_gen(n_nodes, n_edges) for _ in range(20)]

            connected = [g for g in random_graphs if nx.is_connected(g)]
            connected_dense = [g for g in random_dense_graphs if nx.is_connected(g)]

            if len(connected) < 5 or len(connected_dense) < 5:
                continue

            for i, g in enumerate(choices(connected, k=5)):
                write_graph_to_file(
                    g,
                    f"random_{n_nodes}_{n_edges}_g{i}", random = True
                )

            for i, g in enumerate(choices(connected_dense, k=5)):
                write_graph_to_file(
                    g,
                    f"dense_random_{n_nodes}_{n_edges}_g{i}", random = True
                )


if __name__ == "__main__":
    main()

