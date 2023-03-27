# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 15:20:16 2023

Connected sequential algorithm

@author: tymot
"""

import logging
from typing import List

from networkx import Graph

logger = logging.getLogger("main")


def delta(G: Graph) -> int:
    """
    Returns:
        Delta of G - the maximal degree of verticies
    """
    nodes = list(G.nodes())
    m = len(nodes)
    if m <= 0:
        return 0

    delta = len(list(G.neighbors(nodes[0])))
    v = 0

    for node in nodes:
        number_of_neighbors = len(list(G.neighbors(node)))
        if number_of_neighbors > delta:
            delta = number_of_neighbors
            v = node

    logger.debug(f"The greatest degree has vertex number {v}.")
    logger.debug(f"It has degree of {delta}")
    return delta


def validate_coloring(G: Graph, colors: List[int]) -> bool:
    nodes = list(G.nodes())

    for v in nodes:
        for neighbor in list(G.neighbors(v)):
            if colors[neighbor] == colors[v]:
                return False
    return True
