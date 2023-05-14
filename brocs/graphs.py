import networkx as nx

def fish() -> nx.Graph:
    return nx.graph_atlas(800)


def path() -> nx.Graph:
    return nx.path_graph(8)


def erdos_renyi() -> nx.Graph:
    return nx.gnm_random_graph(10, 20, seed=44)


def fence() -> nx.Graph:
    G = nx.Graph()

    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (3, 11),
        (11, 8),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
    ]

    G.add_edges_from(edges)

    return G


def bipartite() -> nx.Graph:
    return nx.complete_bipartite_graph(5, 2)

def erdos_renyi() -> nx.Graph:
    return nx.gnm_random_graph(10, 20, seed=44) # brocs performing worse

def cavemen() -> nx.Graph:
    return nx.connected_caveman_graph(3, 4)

def dense_random_gen(n_nodes: int, n_edges: int) -> nx.Graph:
    return nx.dense_gnm_random_graph(n_nodes, n_edges)

def random_gen(n_nodes: int, n_edges: int) -> nx.Graph:
    return nx.gnm_random_graph(n_nodes, n_edges)


def diamond() -> nx.Graph: 
    #https://www.sciencedirect.com/science/article/pii/0166218X94900906

    G = nx.Graph()

    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (4, 2),
        (3, 5),
        (1, 6),
        (6, 7),
        (6, 9),
        (7, 9),
        (7, 8),
        (8, 9),
        (8, 5)
    ]

    G.add_edges_from(edges)
    
    return G

def twin_kite() -> nx.Graph:
    G = nx.Graph()

    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (4, 2),
        (3, 5),
        (1, 6),
        (6, 7),
        (6, 9),
        (7, 9),
        (7, 8),
        (8, 9),
        (8, 5), 
        (5, 10)
    ]
    G.add_edges_from(edges)

    return G


def double_twin_kite() -> nx.Graph:
    G = nx.Graph()

    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 1),
        (4, 2),
        (3, 5),
        (1, 6),
        (6, 7),
        (6, 9),
        (7, 9),
        (7, 8),
        (8, 9),
        (8, 5), 
        (5, 10),
        
        (11, 12),
        (12, 13),
        (13, 14),
        (14, 11),
        (14, 12),
        (13, 10),
        (11, 16),
        (16, 17),
        (16, 19),
        (17, 19),
        (17, 18),
        (18, 19),
        (18, 10)       
    ]
    G.add_edges_from(edges)

    return G

def domek() -> nx.Graph:
    G = nx.Graph()

    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (1, 4), (2, 4), (3, 5)]

    G.add_edges_from(edges)

    return G


def lopata() -> nx.Graph:
    G = nx.Graph()

    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 3)]

    G.add_edges_from(edges)

    return G
