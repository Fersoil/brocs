from abc import ABC, abstractmethod
from typing import List

from networkx import Graph


class ColoringAlgorithm(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def color_graph(self, G: Graph) -> List[int]:
        """
        Creates a graph coloring.

        Args:
            G: Graph structure loaded with networkx library

        Returns:
            List of colors (non-negative integers), representing good coloring
            of the Graph G.
        """
        pass
