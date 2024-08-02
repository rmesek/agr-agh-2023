# https://marcinlos.github.io/algograf/lab5
from pathlib import Path
import timeit
from collections import deque
from dimacs import *

GRAPHS_PATH = Path(__file__).parent.absolute() / "graphs"


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()  # zbiór sąsiadów

    def connect_to(self, v):
        self.out.add(v)

    def __repr__(self) -> str:
        return f"{self.idx}:{self.out}"


def to_graph(G):
    V, L = G
    G = [None] + [Node(i) for i in range(1, V + 1)]  # żeby móc indeksować numerem wierzchołka
    for u, v, _ in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    return G, set([i for i in range(1, V + 1)])


def find_paths(path, paths=[]) -> list[Path]:
    for item in path.iterdir():
        if item.is_file():
            paths.append(item)
        elif item.is_dir():
            paths.extend(find_paths(GRAPHS_PATH / item, []))
    return paths


def print_graph(G):
    for node in G:
        print(node)


#################################### UNIQUE ####################################
def checkLexBFS(G, vs):
    n = len(G)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n - 1):
        for j in range(i + 1, n - 1):
            Ni = G[vs[i]].out
            Nj = G[vs[j]].out

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True


def LexBFS(G, v_start):
    parents = [set() for _ in range(len(G) + 1)]
    visited_order = [v_start]
    unvisited = [set([node.idx for node in G[1:]]) - set([v_start]), set([v_start])]

    print(unvisited)
    # TODO

    return visited_order


def checkPEO(G, vs):
    pass  # TODO


################################################################################


def run(path):
    G, V = to_graph(loadWeightedGraph(path))
    result = 1 if checkPEO(G, LexBFS(G, 1)) else 0
    print(f"{f'GOT {result} EXPECTED {int(readSolution(path))}' if result != int(readSolution(path)) else f'{result}'}")


def main():
    paths = find_paths(GRAPHS_PATH)
    # paths = [GRAPHS_PATH / "chordal" / "example-fig5"]
    for path in paths:
        print()
        print(path.relative_to(GRAPHS_PATH))
        try:
            start = timeit.default_timer()
            run(path)
            print(f"Time: {timeit.default_timer() - start :.3f}s")
        except KeyboardInterrupt:
            print("Interrupted!")


if __name__ == "__main__":
    main()
