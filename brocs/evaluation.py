import logging
from typing import Dict
import networkx as nx
from matplotlib import pyplot as plt
from networkx.classes import Graph

from brocs.algorithms.base import ColoringAlgorithm
from brocs.helpers import delta, validate_coloring


logger = logging.getLogger("main")


def evaluate(G: Graph, coloring_algorithm: ColoringAlgorithm) -> Dict[str, str]:
    nodes = list(G.nodes())
    m = len(nodes)

    colors = coloring_algorithm.color_graph(G)
    plt.clf()

    label_dict = dict(zip(list(range(m)), colors))

    nx.draw(G, node_color=colors, labels=label_dict, with_labels=True)  # colored graph

    unique_colors = len(set(colors))
    time_elapsed = "bardzo mało"

    G_delta = delta(G)
    G_coloring_correct = validate_coloring(G, colors)

    logger.info(f"Colored graph G of {G.number_of_nodes()} vertices and {G.number_of_edges()} edges")
    logger.info(f"with maximum vertex degree of {G_delta}")
    logger.info(f"colored using {coloring_algorithm.__class__.__name__}.")
    logger.info(f"Resulted in a {'NOT' * (not G_coloring_correct)} valid coloring")
    logger.info(f"Used {unique_colors} colors; Time elapsed: {time_elapsed}")

    eval_dict = {"time_elapsed": time_elapsed, "unique_colors": unique_colors}

    return eval_dict
