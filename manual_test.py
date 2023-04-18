import logging
from pathlib import Path

from brocs import graphs
from brocs.main import run_program_on_graph

logging.basicConfig(level=logging.INFO)

g = graphs.fish()


class MockSettings:
    input = Path("test")
    lovas = True
    connected_sequential = False
    visualization = True


run_program_on_graph(g, MockSettings())
