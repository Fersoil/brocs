from pathlib import Path

import networkx as nx
import numpy as np

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
    random,
    dense_random,
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

    for i in range(1, 6):
        for n_nodes in [10, 20, 50, 100, 200]:
            for n_edges in [5, 10, 20, 50, 100, 200, 500, 1000]:

                if n_edges > n_nodes * (n_nodes - 1) / 2:
                    continue

                write_graph_to_file(
                    random(n_nodes, n_edges),
                    f"random_{n_nodes}_{n_edges}_g{i}", random = True
                )
                write_graph_to_file(
                    dense_random(n_nodes, n_edges),
                    f"dense_random_{n_nodes}_{n_edges}_g{i}", random = True
                )


if __name__ == "__main__":
    main()

