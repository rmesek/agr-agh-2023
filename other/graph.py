from enum import Enum, auto
from dimacs import *


class GraphType(Enum):
    WEIGHTED_GRAPH = auto()
    DIRECTED_WEIGHTED_GRAPH = auto()


class Representation(Enum):
    ADJACENCY_LIST = auto()
    ADJACENCY_MATRIX = auto()


class Graph:
    def __init__(self, path, graph_type):
        self.graph_type = graph_type
        self.representation = Representation.ADJACENCY_LIST
        self.load(path)

    def __str__(self):
        match self.representation:
            case Representation.ADJACENCY_LIST:
                return str(self.graph_type.name) + str(self.graph)

            case Representation.ADJACENCY_MATRIX:
                idx = f"u\\v"
                repr = f"{idx:<5}"
                size = len(self.graph)

                for row in range(1, size):
                    repr += f"{row:<5}"
                repr += "\n"
                for row in range(1, size):
                    repr += f"{row:<5}"
                    for col in range(1, size):
                        repr += f"{str(self.graph[row][col]):<5}"
                    repr += f"\n"
                return repr

            case _:
                raise Exception("Not implemented!")

    def load(self, path):
        match self.graph_type:
            case GraphType.WEIGHTED_GRAPH:
                self.load_weighted_graph(path)

            case GraphType.DIRECTED_WEIGHTED_GRAPH:
                self.load_directed_weighted_graph(path)

            case _:
                raise Exception("Not implemented!")

    def load_weighted_graph(self, path):
        self.graph = {}
        V, L = loadWeightedGraph(path)
        V = int(V)
        for x in range(1, V + 1):
            self.graph[x] = []
        for x, y, w in L:
            self.graph[x].append((y, w))
            self.graph[y].append((x, w))

    def load_directed_weighted_graph(self, path):
        self.graph = {}
        V, L = loadDirectedWeightedGraph(path)
        V = int(V)
        for x in range(1, V + 1):
            self.graph[x] = []
        for x, y, w in L:
            self.graph[x].append((y, w))

    def to_adjacency_matrix(self):
        match self.representation:
            case Representation.ADJACENCY_MATRIX:
                return

            case Representation.ADJACENCY_LIST:
                V = len(self.graph)
                matrix = [[None for _ in range(V + 1)] for _ in range(V + 1)]
                for u in self.graph:
                    for v, w in self.graph[u]:
                        matrix[u][v] = w

                self.graph = matrix
                self.representation = Representation.ADJACENCY_MATRIX
                return

            case _:
                raise Exception("Not implemented!")

    

from pathlib import Path

PATH = Path(__file__).parent.absolute() / "graphs" / "g1"
g = Graph(PATH, GraphType.WEIGHTED_GRAPH)
print(g)
g.to_adjacency_matrix()
print(g)
