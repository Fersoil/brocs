import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Protocol

import networkx as nx
import numpy as np
import pandas as pd

from brocs.algorithms import BrooksAlgorithm, ColoringAlgorithm, ConnectedSequential
from brocs.evaluation import evaluate_graph, time_ns_to_human_readable
from brocs.visualization import show_colored_graph, show_graph
from brocs.helpers import delta

logger = logging.getLogger(__name__)


class Settings(Protocol):
    input: Path


def load_graph_from_file(file: Path) -> Optional[nx.Graph]:
    loaded_file = np.load(file, allow_pickle=True)

    if not isinstance(loaded_file, np.ndarray):
        logger.error(f"File {file} is not a numpy matrix. Skipping...")
        return

    if loaded_file.shape[0] != loaded_file.shape[1]:
        logger.error(f"File {file} is not a square matrix. Skipping...")
        return

    return nx.from_numpy_array(loaded_file)


@dataclass
class GraphResults:
    graph: nx.Graph
    results: dict[str, Any] = field(default_factory=dict)


@dataclass
class Program:
    settings: Settings
    loaded_graphs: dict[str, GraphResults] = field(default_factory=dict)

    def load_graphs_from_path(self, path: Path) -> dict[str, nx.Graph]:
        new_graphs = {}
        if path.is_dir():
            logger.info(f"Loading graphs from directory {path}")
            # Iterate over files that are numpy files
            input_file_list = list(path.glob("*.npy"))
            logger.info(f"Found {len(input_file_list)} npy files in directory {path}")
            for file in input_file_list:
                graph = load_graph_from_file(file)
                if graph is not None:
                    new_graphs.update({file.stem: graph})
        elif path.is_file():
            graph = load_graph_from_file(path)
            if graph is not None:
                new_graphs.update({path.stem: graph})
        return new_graphs

    def cast_graphs_to_graph_results(
        self, graphs: dict[str, nx.Graph]
    ) -> dict[str, GraphResults]:
        graph_results = {}
        for graph_name, graph in graphs.items():
            graph_results.update({graph_name: GraphResults(graph=graph)})
        return graph_results

    def load_graphs(self, new_graphs_path: Optional[Path] = None):
        path = self.settings.input if new_graphs_path is None else new_graphs_path
        new_graphs = []
        if not path.exists():
            error_message = f"Path {self.settings.input} does not exist. Exiting..."
            print(error_message)
            logger.error(error_message)
            if new_graphs_path is not None:
                return
            exit(1)

        new_graphs = self.load_graphs_from_path(path)
        self.loaded_graphs.update(self.cast_graphs_to_graph_results(new_graphs))
        print(f"Loaded {len(new_graphs)} new graphs")
        print(f"Total number of graphs: {len(self.loaded_graphs)}")

    def visualize_selected_graph(self):
        print("Here are the loaded graphs")
        graph_name_list = list(self.loaded_graphs.keys())
        for i, graph_name in enumerate(graph_name_list):
            print(f"{i+1}. {graph_name}")
        choices = list(range(1, len(self.loaded_graphs) + 1))
        choice = take_user_input("Which graph do you want to visualize? >>> ", choices)
        choosen_graph = graph_name_list[choice - 1]

        graph = self.loaded_graphs[choosen_graph].graph
        results = self.loaded_graphs[choosen_graph].results

        print("Possible views of the graph: ")
        print("1. Barebone Graph")
        choices = [1]
        if "BrooksAlgorithm" in results:
            print("2. Last coloring by Brooks Algorithm")
            choices.append(2)
            if "best_coloring" in results["BrooksAlgorithm"]:
                print("3. Best coloring found by Brooks Algorithm")
                choices.append(3)
        if "ConnectedSequential" in results:
            print("4. Last coloring by Connected Sequential Algorithm")
            choices.append(4)
            if "best_coloring" in results["ConnectedSequential"]:
                print("5. Best coloring found by Connected Sequential Algorithm")
                choices.append(5)
        choice = take_user_input("Which view do you pick? >>> ", choices)

        if choice == 1:
            show_graph(graph)
        elif choice == 2:
            show_colored_graph(
                graph, results["BrooksAlgorithm"]["last_result"].coloring
            )
        elif choice == 3:
            show_colored_graph(graph, results["BrooksAlgorithm"]["best_coloring"])
        elif choice == 4:
            show_colored_graph(
                graph, results["ConnectedSequential"]["last_result"].coloring
            )
        elif choice == 5:
            show_colored_graph(graph, results["ConnectedSequential"]["best_coloring"])

    def run_algorith_on_loaded_graphs(
        self, algorithm: ColoringAlgorithm, repeat: Optional[int] = None
    ):
        if repeat is None:
            for graph_name, graph_results in self.loaded_graphs.items():
                alg_name = algorithm.name
                print(f"\n  Running {algorithm.name} on graph: {graph_name}")
                new_results = evaluate_graph(graph_results.graph, algorithm)
                graph_results.results.update({alg_name: {"last_result": new_results}})
                time_str = time_ns_to_human_readable(new_results.time_elapsed)
                print(
                    f"  Finished running {algorithm.name} on graph: {graph_name} in {time_str}\n"  # noqa
                )
            return

        alg_name = algorithm.name
        for graph_name, graph_results in self.loaded_graphs.items():
            # df results (graph_name, alg_name, time, number_of_colors, coloring)
            all_results = []
            new_results = None

            print(f"\n  Running {algorithm.name} on graph: {graph_name} {repeat} times")
            for _ in range(repeat):
                new_results = evaluate_graph(graph_results.graph, algorithm)
                all_results.append(
                    (
                        graph_name,
                        alg_name,
                        new_results.time_elapsed,
                        new_results.unique_colors,
                        new_results.coloring,
                    )
                )

            df_results = pd.DataFrame(
                all_results,
                columns=[
                    "graph_name",
                    "alg_name",
                    "time",
                    "number_of_colors",
                    "coloring",
                ],
            )

            min_number_of_colors = df_results["number_of_colors"].min()
            best_coloring = df_results[
                df_results["number_of_colors"] == min_number_of_colors
            ]["coloring"].iloc[0]

            average_time = df_results["time"].mean()
            time_str = time_ns_to_human_readable(int(average_time))
            print(
                f"  Finished running {algorithm.name} on graph: {graph_name} in average of {time_str}"
            )
            print(f"  Best coloring had {min_number_of_colors} colors\n")

            graph_results.results.update(
                {
                    alg_name: {
                        "last_result": new_results,
                        "average_time": average_time,
                        "min_number_of_colors": min_number_of_colors,
                        "best_coloring": best_coloring,
                        "df_results": df_results,
                    }
                }
            )

    def export_results_to_csv(self):
        list_graphs = []
        # df graphs (graph_name, num_of_vertices, num_of_edges, big_detla)
        for graph_name, graph_results in self.loaded_graphs.items():
            assert (
                "ConnectedSequential" in self.loaded_graphs[graph_name].results
            ), "No CS results"
            assert (
                "BrooksAlgorithm" in self.loaded_graphs[graph_name].results
            ), "No Brooks results"

            graph = graph_results.graph
            num_of_vertices = graph.number_of_nodes()
            num_of_edges = graph.number_of_edges()
            big_delta = delta(graph)
            list_graphs.append(
                (graph_name, num_of_vertices, num_of_edges, big_delta)
            )

        df_graphs = pd.DataFrame(
            list_graphs,
            columns=["graph_name", "num_of_vertices", "num_of_edges", "big_delta"],
        )
        df_graphs.to_csv("graphs.csv", index=False)

        all_df_results = [
            graph_result.results[alg_name]["df_results"]
            for graph_result in self.loaded_graphs.values()
            for alg_name in ["ConnectedSequential", "BrooksAlgorithm"]
        ]
        df_results = pd.concat(all_df_results)
        df_results.to_csv("results.csv", index=False)

    def run(self):
        print("Here is what you can do: ")
        print("1. Visualize one of the loaded graphs or their calculated colorings")
        print("2. Run CS algorithm on loaded graphs (once)")
        print("3. Run Brooks algorithm on loaded graphs (once)")
        print("4. Run both algorithms on loaded graphs (n times) and compare results ")
        print("5. Load new graphs")
        print("6. Export findings to csv")
        print("7. Exit program")
        choice = take_user_input("What do you want to do? >>> ", list(range(1, 8)))
        if choice == 1:
            self.visualize_selected_graph()
            self.run()
        elif choice == 2:
            self.run_algorith_on_loaded_graphs(ConnectedSequential(random_state=42))
            self.run()
        elif choice == 3:
            self.run_algorith_on_loaded_graphs(BrooksAlgorithm(random_state=42))
            self.run()
        elif choice == 4:
            n = take_user_input(
                "How many times do you want to run the algorithms? >>> ",
                [],
                any_int=True,
            )
            self.run_algorith_on_loaded_graphs(ConnectedSequential(), repeat=n)
            self.run_algorith_on_loaded_graphs(BrooksAlgorithm(), repeat=n)
            # TODO: Add comparison
            self.run()
        elif choice == 5:
            input_path = input("Enter path to the folder with new graphs >>> ")
            self.load_graphs(new_graphs_path=Path(input_path).expanduser())
            self.run()
        elif choice == 6:
            assert self.loaded_graphs, "No graphs loaded"
            print("Exporting findings to csv...")
            self.export_results_to_csv()
            print("Exported findings to csv completed successfully\n\n")

            self.run()
        elif choice == 7:
            print("Exiting program...")
            exit(0)


def take_user_input(message: str, possilities: list[int], any_int=False) -> int:
    while True:
        user_input = input(message)
        if user_input.isdigit():
            if any_int or int(user_input) in possilities:
                return int(user_input)

        str_possibilities = [str(x) for x in possilities]
        print(f"Wrong input. Possible inputs: {', '.join(str_possibilities)}")


USAGE = """
brocs <input>
"""

EPILOG = """
This is a program for calculating graph colorings
using Connected Sequential algorithm and comparing them to
the algorithm that can be derived from Lovash proof of Brooks theorem.
In the program we are calling that new algorithm Brooks algorithm.

After running the program with provided input you will be presented with a menu
"""


def main():
    parser = argparse.ArgumentParser(
        description="Brocs",
        usage=USAGE,
        epilog=EPILOG,
    )
    parser.add_argument(
        "input",
        help="Path to a input file with graph matrix or a directory with input files",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug messages",
    )
    args = parser.parse_args()
    args.input = Path(args.input).expanduser()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    program = Program(args)  # type: ignore
    program.load_graphs()
    program.run()


if __name__ == "__main__":
    main()
