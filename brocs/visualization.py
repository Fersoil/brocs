from colorsys import hls_to_rgb
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from brocs.helpers import check_graph


def get_random_colors(n: int) -> List[str]:
    colors = []
    for i in np.linspace(0, 1, n + 1):
        hue = i
        lightness = (50 + np.random.rand() * 10) / 100.0
        saturation = (90 + np.random.rand() * 10) / 100.0
        rgb = hls_to_rgb(hue, lightness, saturation)
        r, g, b = [int(256 * i) for i in rgb]
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return colors[:n]


def show_graph(graph: nx.Graph, figsize: tuple = (10, 10)):
    check_graph(graph)

    fig, ax = plt.subplots(figsize=figsize)
    nx.draw(graph, ax=ax, with_labels=True, node_color="skyblue")
    plt.show()
    plt.close(fig)


def show_colored_graph(graph: nx.Graph, coloring: List[int], figsize: tuple = (10, 10)):
    check_graph(graph)

    fig, ax = plt.subplots(figsize=figsize)
    colors = get_random_colors(len(set(coloring)))
    color_map = [colors[i] for i in coloring]

    print(coloring)

    nx.draw(graph, ax=ax, with_labels=True, node_color=color_map)
    plt.show()
    plt.close(fig)
