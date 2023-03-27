import networkx as nx


def fish_graph() -> nx.Graph:
    return nx.graph_atlas(800)
