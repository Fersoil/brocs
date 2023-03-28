import networkx as nx


def fish_graph() -> nx.Graph:
    return nx.graph_atlas(800)



def path() -> nx.Graph:
    return nx.path_graph(8)


def fence() -> nx.Graph:
    G = nx.Graph()
    
    edges = [(1,2), (2, 3), (3, 4), (4, 5),
             (3,11), (11,8), 
             (6, 7), (7,8), (8,9), (9,10)]
    
    G.add_edges_from(edges)
    
    return G


def bipartite() -> nx.Graph:
    return nx.complete_bipartite_graph(5, 2)



def domek() -> nx.Graph:
    G = nx.Graph()
    
    edges = [(1,2), (2, 3), (3, 4), (4, 5),
             (1, 3), (1, 4), (2, 4), (3, 5)]
    
    G.add_edges_from(edges)
    
    return G


def lopata() -> nx.Graph:
    G = nx.Graph()
    
    edges = [(1,2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7,3)]
    
    G.add_edges_from(edges)
    
    return G