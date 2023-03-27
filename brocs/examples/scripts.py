# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 15:20:16 2023

Connected sequential algorithm

@author: tymot
"""

import queue
import random



def delta(G):
    """
    return Delta of G - the maximal degree of vertex
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

    print(f"The greatest degree has vertex number {v}. It has degree of {delta}")
    return delta
    


def check_coloring(G, colors):
    nodes = list(G.nodes())
    m = len(nodes)
    
    
    for v in nodes:
        for neighbor in list(G.neighbors(v)):
            if colors[neighbor] == colors[v]:
                return False
        return True
        
        
        
        
        