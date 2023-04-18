import argparse
import logging
from pathlib import Path
from typing import Optional, Protocol

import networkx as nx
import numpy as np

from brocs.algorithms import BrooksAlgorithm, ConnectedSequential
from brocs.evaluation import evaluate_graph

"""
Dzień dobry, najlepiej przygotować kilka przykładowych grafów do wczytania z osobnego pliku, tak aby łatwo można było dodać kolejne grafy. W tym kilka małych grafów, na których można sprawdzić jak nasze kolorowanie wygląda i co najmniej 2 większe do testów prędkości obliczeń. Do tego przy uruchomieniu aplikacji wyświetlić pytanie "Który algorytm chcesz przetestować?" z opcjami 1. connected sequential, 2. algorytm Lovasa, 3. oba. Jeśli algorytmy mają elementy randomizacji (np. losowy wybór wierzchołka przy "remisie" w kryterium wyboru) można dodatkowo spytać "Ile testów chcesz wykonać?". Potem "Podaj nazwę pliku z grafem do pokolorowania". Wczytuje podany plik i koloruje. Zwraca 1. liczbę użytych kolorów, 2. czas obliczeń, 3. wrzuca do pliku otrzymane kolorowanie (liczba kolorów i czas też mogą być w pliku, w przypadku kilku testów albo zapisujemy wszystkie kolorowania, albo tylko jedno). Dla wielu testów najlepiej wyświetlić uśrednione liczby kolorów i czasy obliczeń, a przy stosunkowo małej liczbie testów można też podać poszczególne wyniki. A potem pyta "Czy chcesz wybrać inny algorytm?" i "Czy chcesz zmienić graf?", no i liczymy od początku. Można to tak zaimplementować, żeby najpierw sprawdzał, czy już nie ma pliku z wynikiem i jeśli tak omija obliczenia lub pyta użytkownika czy chce liczyć ponownie, czy wyświetlić poprzedni wynik. Wszelkie komunikaty oczywiście mogą Państwo napisać po swojemu. Właściwie wszystko można inaczej niż napisałam, daję tylko wstępną propozycję.
"""

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Brocs")
    parser.add_argument(
        "input",
        help="path to a input file with graph matrix or a directory with input files",
    )
    parser.add_argument(
        "--lovas", action="store_true", help="run Lovas Algorithm on input"
    )
    parser.add_argument(
        "--connected-sequential",
        "--cs",
        action="store_true",
        help="run Connected Sequential Algorithm on input",
    )
    parser.add_argument(
        "--visualization",
        action="store_true",
        help="Show visualization of the graph coloring",
    )

    args = parser.parse_args()
    args.input = Path(args.input).expanduser()

    run_program(args)  # type: ignore


class Settings(Protocol):
    input: Path
    lovas: bool
    connected_sequential: bool
    visualization: bool


def run_program_on_graph(graph: nx.Graph, settings: Settings):
    if settings.lovas:
        print("Running Lovas Algorithm")
        raport = evaluate_graph(graph, BrooksAlgorithm())
        if settings.visualization:
            raport.visualize_coloring()

    if settings.connected_sequential:
        print("Running Connected Sequential")
        raport = evaluate_graph(graph, ConnectedSequential())
        if settings.visualization:
            raport.visualize_coloring()


def load_graph_from_file(file: Path) -> Optional[nx.Graph]:
    loaded_file = np.load(file)

    if not isinstance(loaded_file, np.matrix):
        logger.error(f"File {file} is not a numpy matrix. Skipping...")
        return

    if loaded_file.shape[0] != loaded_file.shape[1]:
        logger.error(f"File {file} is not a square matrix. Skipping...")
        return

    return nx.from_numpy_array(loaded_file)


def run_program(settings: Settings):
    if not settings.input.exists():
        logger.error(f"Path {settings.input} does not exist")
        # TODO: Add print info
        exit(1)

    if not settings.lovas and not settings.connected_sequential:
        logger.error("You have to choose at least one algorithm")
        # TODO: Add print info
        exit(1)

    if settings.input.is_dir():
        logger.info("Running program on a directory")
        # Iterate over files that are numpy files
        input_file_list = list(settings.input.glob("*.npy"))
        # Change that to f string
        logger.info(
            f"Found {len(input_file_list)} npy files in directory {settings.input}"
        )  # noqa

        for file in input_file_list:
            graph = load_graph_from_file(file)
            if graph:
                run_program_on_graph(graph, settings)
    else:
        graph = load_graph_from_file(settings.input)
        if graph is None:
            logger.error("Given graph file is not a valid graph")
            exit(1)
        run_program_on_graph(graph, settings)


if __name__ == "__main__":
    main()
