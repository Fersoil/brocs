import logging
import time
from dataclasses import dataclass
from typing import List

import networkx as nx

from brocs.algorithms.base import ColoringAlgorithm
from brocs.helpers import delta, validate_coloring
from brocs.visualization import show_colored_graph

logger = logging.getLogger(__name__)


def time_ns_to_human_readable(time_ns: int) -> str:
    if time_ns < 1000:
        return f"{time_ns} ns"
    elif time_ns < 1000000:
        return f"{time_ns / 1000} μs"
    elif time_ns < 1000000000:
        return f"{time_ns / 1000000} ms"
    else:
        return f"{time_ns / 1000000000} s"


@dataclass(slots=True)
class EvaluationResults:
    graph: nx.Graph
    number_of_nodes: int
    delta: int

    unique_colors: int
    is_coloring_correct: bool
    coloring: List[int]
    time_elapsed: int

    def visualize_coloring(self):
        show_colored_graph(self.graph, self.coloring)


def evaluate_graph(
    G: nx.Graph, coloring_algorithm: ColoringAlgorithm
) -> EvaluationResults:
    nodes = list(G.nodes())
    m = len(nodes)

    start = time.time_ns()
    colors = coloring_algorithm.color_graph(G)
    time_elapsed = time.time_ns() - start

    unique_colors = len(set(colors))

    G_delta = delta(G)
    G_coloring_correct = validate_coloring(G, colors)

    logger.info(
        f"Colored graph G of {G.number_of_nodes()} vertices and {G.number_of_edges()} edges"
    )
    logger.info(f"with maximum vertex degree of {G_delta}")
    logger.info(f"colored using {coloring_algorithm.__class__.__name__}.")
    logger.info(f"Resulted in a {'NOT' * (not G_coloring_correct)} valid coloring")
    logger.info(f"Used {unique_colors} colors")
    logger.info(f"Time elapsed: {time_ns_to_human_readable(time_elapsed)}")

    evaluation_results = EvaluationResults(
        graph=G,
        number_of_nodes=m,
        delta=G_delta,
        unique_colors=unique_colors,
        is_coloring_correct=G_coloring_correct,
        coloring=colors,
        time_elapsed=time_elapsed,
    )

    return evaluation_results
