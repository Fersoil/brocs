# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 15:20:16 2023

Connected sequential algorithm

@author: tymot
"""

import logging
from typing import List, Set, Optional, Tuple

import networkx as nx

logger = logging.getLogger("main")

def check_graph(graph: nx.Graph):
    nodes = set(graph.nodes())
    expected_nodes = set(range(len(nodes)))
    assert len(nodes.union(expected_nodes)) == len(
        nodes
    ), "Graph should have nodes labeled from 0 to n-1"


def delta(G: nx.Graph) -> int:
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


def validate_coloring(G: nx.Graph, colors: List[int]) -> bool:
    nodes = list(G.nodes())

    for v in nodes:
        for neighbor in list(G.neighbors(v)):
            if colors[neighbor] == colors[v]:
                return False
    return True


def find_common_neighbor(G: nx.Graph, a: int, b: int):
    a_neighbors = G.neighbors(a)
    b_neighbors = G.neighbors(b)

    common_neighbors = list(set(a_neighbors) & set(b_neighbors))

    if not common_neighbors:
        raise ValueError("wrong input")

    return common_neighbors[0]


def dist_two(G: nx.Graph) -> Set[Tuple[int, int]]:
    """Find all pairs of vertices of distance 2 between them.
    Might improve one day with a laplacian matrix
    """
    dist_two_set = set()
    for v in G.nodes():
        v_neighbors = list(G.neighbors(v))  # take all neighbors of v
        for v_neighbor in v_neighbors:
            for second_neighbor in G.neighbors(v_neighbor):
                if second_neighbor != v and second_neighbor not in v_neighbors:
                    if second_neighbor <= v:
                        dist_two_set.add((second_neighbor, v))
                    if second_neighbor > v:
                        dist_two_set.add((v, second_neighbor))

    return dist_two_set


def dist_two_from(G: nx.Graph, a: int) -> Optional[int]:
    """Find any vetrex of distance 2 from vetrex a
    Also might improve with laplacian matrix
    """
    a_neighbors = list(G.neighbors(a))

    for v in a_neighbors:
        for second_neighbor in G.neighbors(v):
            if second_neighbor != a and second_neighbor not in a_neighbors:
                return second_neighbor

    return None

