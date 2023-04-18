import networkx as nx
import matplotlib.pyplot as plt
import logging

from brocs.algorithms.cs import ConnectedSequential
from brocs.evaluation import evaluate_graph
from brocs.graphs import fish_graph
from brocs.log import setup_custom_logger

logger = setup_custom_logger("main", logging.DEBUG)


def main():
    G = fish_graph()
    nx.draw(G)  # uncolored
    plt.show()
    plt.clf()

    cs = ConnectedSequential()
    eval = evaluate_graph(G, cs)
    logger.info(eval)


if __name__ == "__main__":
    main()
