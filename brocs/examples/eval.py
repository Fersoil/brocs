# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:20:16 2023

Comparison between two algorithms

@author: tymot
"""

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random


from cs import connected_sequential
from brooks import brooks

from scripts import delta, check_coloring







G = nx.graph_atlas(800) # to jest prawie rybka
nx.draw(G) # uncolored
nodes = list(G.nodes())
m = len(nodes)
plt.clf()
random.seed(44)


    
# we could use some wrapper function that would describe the performance of a coloring function

def evaluate(G, func):
    nx.draw(G)
    
    colors = func(G)
    plt.clf()
    
    label_dict = dict(zip(list(range(m)), colors))
    
    nx.draw(G, node_color=colors, labels=label_dict, with_labels=True) # colored graph
    
    unique_colors = len(set(colors))
    time_elapsed = "bardzo mało"
    G_delta = delta(G)
    G_coloring_correct = check_coloring(G, colors)
    
    print(f"Colored graph G of {G.number_of_nodes()} vertices and {G.number_of_edges()} edges with maximum vertex degree of {G_delta}",
          f"colored using {func.__name__}, coloring is correct: {G_coloring_correct}",
          f"Used {unique_colors} colors; Time elapsed: {time_elapsed}")
    
    eval_dict = {"time_elapsed":time_elapsed, "unique_colors":unique_colors}
    
    return eval_dict





evaluate(G, brooks)

    
