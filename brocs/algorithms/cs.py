# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:20:16 2023

Connected sequential algorithm

@author: tymot
"""

import logging
import random
from queue import Queue
from typing import List, Optional

import networkx as nx
from networkx.classes import Graph

from brocs.algorithms.base import ColoringAlgorithm

"""
Parameters
----------
G : Graph
    Graph G from nx library.

Returns
-------
colors : List

"""

logger = logging.getLogger("main")


class ConnectedSequential(ColoringAlgorithm):
    """Connected Sequential coloring algorithm.

    Args:
        random_state: Seed for random. Makes algorithm deterministic.
    """

    random_state: Optional[int]

    def __init__(self, random_state: Optional[int] = None) -> None:
        super().__init__()
        self.random_state = random_state

    def color_graph(self, G: Graph) -> List[int]:
        if self.random_state is not None:
            random.seed(self.random_state)

        # Relabel graph G
        nodes = G.nodes()
        mapping = dict(zip(nodes, range(len(nodes))))
        G = nx.relabel_nodes(G, mapping)

        nodes = list(G.nodes())
        m = len(nodes)

        # TODO - check if graph is connected

        colors = [-1] * m

        forbidden_colors = []
        q = Queue()
        q.put(random.randint(0, m - 1))  # put random first vertex

        while not q.empty():
            v = q.get()
            if colors[v] == -1:
                # if the actual vertex is uncolored
                neighbors = G.neighbors(v)
                forbidden_colors = []
                for neighbor in neighbors:
                    if colors[neighbor] == -1:
                        q.put(neighbor)
                    else:
                        forbidden_colors.append(colors[neighbor])

                # now we find the smallest color that we can use
                color = 0
                while color in forbidden_colors:
                    color += 1
                colors[v] = color  # color the choosen vertex

        return colors
