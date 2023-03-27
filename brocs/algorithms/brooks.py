# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:20:16 2023

Brooks theorem algorithm

@author: tymot
"""

from typing import List, Optional

import networkx as nx
from matplotlib.pyplot import logging
from networkx.classes import Graph
from networkx.exception import NetworkXNoCycle

from brocs.algorithms.base import ColoringAlgorithm
from brocs.algorithms.cs import ConnectedSequential

logger = logging.getLogger("main")


class BrooksAlgorithm(ColoringAlgorithm):
    """Graphs coloring algorithm based on the proof
    of the Brooks' theorem.

    Args:
        random_state: Seed for random. Makes algorithm deterministic.
    """

    random_state: Optional[int]
    cs_algorithm: ConnectedSequential

    def __init__(self, random_state: Optional[int] = None) -> None:
        super().__init__()
        self.random_state = random_state
        self.cs_algorithm = ConnectedSequential(random_state=random_state)

    def _dist_two(self, G: Graph):
        nodes = list(G.nodes())

        dist_two_set = set()

        for v in nodes:
            v_neighbors = list(G.neighbors(v))  # take all neighbors of v
            for v_neighbor in v_neighbors:
                for second_neighbor in G.neighbors(v_neighbor):
                    if second_neighbor != v and second_neighbor not in v_neighbors:
                        dist_two_set.add((second_neighbor, v))

        return dist_two_set

    def color_graph(self, G: Graph) -> List[int]:
        # read graph structure
        nodes = list(G.nodes())
        m = len(nodes)

        colors = [-1] * m

        # check if graph is a cycle
        try:
            cycle = nx.find_cycle(G, orientation="ignore")
            if len(cycle) == m:
                logger.info("Graph G is a cycle")
                return self.cs_algorithm.color_graph(G)
        except NetworkXNoCycle:
            logger.warn("There is no cycle in graph G")

        S = self._dist_two(G)
        logger.debug(S)

        if S == set():
            logger.info("Graph G is complete")
            return list(range(m))

        for pair in S:
            reduced_vertices = [i for i in range(m) if i not in pair]

            subG = nx.induced_subgraph(G, reduced_vertices)
            if nx.is_connected(subG):
                a, b = pair
                break

        return colors
