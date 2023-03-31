# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:20:16 2023

Brooks theorem algorithm

@author: tymot
"""

from typing import List, Optional

import networkx as nx
from matplotlib.pyplot import logging
from queue import Queue, LifoQueue
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

    def _dist_two_from(self, G: Graph, a: int):
        # find vertex of distance 2 from a
        a_neighbors = list(G.neighbors(a))
        
        for v in a_neighbors:
            v_neighbors = list(G.neighbors(v)) # take all neighbors of v
            for second_neighbor in v_neighbors:
                if second_neighbor != a and second_neighbor not in a_neighbors:
                        return second_neighbor
                        
        return None
    

    def _find_common_neighbor(G, a, b):
        a_neighbors = G.neighbors(a)
        b_neighbors = G.neighbors(b)
        
        common_neighbors = list(set(a_neighbors) & set(b_neighbors))
        
        if not common_neighbors:
            raise ValueError("wrong input") #TODO tutaj jakos ladniej trzeba co nie Kuba 
            
        return common_neighbors[0] 


    def color_graph(self, G: Graph) -> List[int]:
        # read graph structure
        nodes = list(G.nodes())
        m = len(nodes)

        colors = [-1] * m

        # relabel graph G
        mapping = dict(zip(G.nodes(), range(m)))
        
        G = nx.relabel_nodes(G, mapping)

        
        colors = [-1] * m
        
        a, b, x = (None, None, None)


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

            is_G_a_b_connected = False
            
        if not is_G_a_b_connected:
            logger.info("G-a-b is not connected")
                        
            G_cut_nodes = nx.minimum_node_cut(G)
            
            if len(G_cut_nodes) == 1:
                logger.info("G is 1-connected")
                x = G_cut_nodes.pop()
                set_x_neighbors = set(G.neighbors(x))
                neighbor_colors = set()
                
                reduced_vertices = [i for i in range(m) if i != x]
            
                subG = nx.induced_subgraph(G, reduced_vertices)
                
                # miejsce do popisu to mozna zoptymalizować
                components = [c for c in nx.connected_components(subG)]
                
                component = components[-1]
                logger.info("coloring and recoloring G")
                
                rest_of_graph = set(range(m)) - set(component)
                
                subG = G.subgraph(component)
                subG_size = len(component)
                sub_colors = self.cs_algorithm.color_graph(subG)
                sub_dict = dict(zip(range(subG_size), subG))
                
                for i in range(subG_size):
                    colors[sub_dict[i]] = sub_colors[i]
                    
                    
                restG = G.subgraph(rest_of_graph)
                restG_size = len(rest_of_graph)
                rest_colors = self.cs_algorithm.color_graph(restG)
                rest_dict = dict(zip(range(restG_size), restG))
                re_rest_dict = dict(zip(restG, range(restG_size)))
                
                for neighbor in set_x_neighbors & set(component):
                    neighbor_colors.add(colors[neighbor])
                    
                
                x_color = rest_colors[re_rest_dict[x]]
                
                if x_color in neighbor_colors:
                    color_for_x = 0
                    
                    while color_for_x in neighbor_colors:
                        color_for_x += 1
                    
                    for i in range(restG_size): # replace the colors
                        if rest_colors[i] == color_for_x:
                            rest_colors[i] = x_color
                        elif rest_colors[i] == x_color:
                            rest_colors[i] = color_for_x
                            
                for i in range(restG_size):
                    colors[rest_dict[i]] = rest_colors[i]
                return colors

            else: # graph is 2-connected         
                logger.info("G is 2-connected")
                t = None
                for v in nodes:
                    if 3 <= G.degree[v] < m-1:
                        t = v 
                        break
                    
                # every vertex has incorrect degree
                if not t:
                    print("Graph is a star graph (not quite) or a cycle")
                    return self.cs_algorithm.color_graph(G)
                
                
                reduced_vertices = [i for i in range(m) if i != t]
                subG = nx.induced_subgraph(G, reduced_vertices)
                cut_nodes = nx.minimum_node_cut(subG)
                
                if cut_nodes >= 2:
                    a = t
                    b = self._dist_two_from(G, a)
                else:
                    # to moze byc zle
                    components =  [c for c in nx.biconnected_components(subG)]
                    
                    # now we look for disjoint points
                    
                    disjoint_points = [-1] * len(components)
                    
                    for i in range(len(components)):
                        for j in range(len(components)):
                            if i != j:
                                common_vertices = (set(components[i]) & set(components[j])).pop()
                                if common_vertices:
                                    disjoint_points[i] = common_vertices
                                    break
                                
                    x = t
                    x_neighbors = set(G.neighbors(x))
                    
                    # select a and b from endblocks
                    a = ((set(components[0]) - {disjoint_points[0]}) & x_neighbors).pop()
                    b = ((set(components[1]) - {disjoint_points[1]}) & x_neighbors).pop()
                         
                
        colors[a], colors[b] = 0, 0
        
        if not x:
            x = self._find_common_neighbor(G, a, b)
        
        nx.draw(G, with_labels=True)
        
        
        q = LifoQueue()
        neighbors_queue = Queue() 
        
        is_visited = [False] * m

        is_visited[a], is_visited[b] = True, True
        neighbors_queue.put(x)
        

        # create sequence 

        while not neighbors_queue.empty():
            #while there exist a vertex not in the sequence
            v = neighbors_queue.get()
            if is_visited[v]:
                continue
            q.put(v)
            for neighbor in G.neighbors(v):
                neighbors_queue.put(neighbor)
            
            is_visited[v] = True

        # color vertices in order given by the sequence
        
        while not q.empty():
            v = q.get()
            if colors[v] == -1: 
                # if the actual vertex is uncolored
                neighbors = G.neighbors(v)
                forbidden_colors = []
                for neighbor in neighbors:
                    if colors[neighbor] != -1:
                        forbidden_colors.append(colors[neighbor])
                
                # now we find the smallest color that we can use
                color = 0
                while color in forbidden_colors:
                    color += 1
                colors[v] = color # color the choosen vertex
        
        return colors
