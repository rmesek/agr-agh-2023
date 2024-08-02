# https://marcinlos.github.io/algograf/lab7
from pathlib import Path
import timeit
import networkx as nx
from dimacs import *

GRAPHS_PATH = Path(__file__).parent.absolute() / "graphs"


def to_graph(G) -> nx.Graph:
    V, L = G
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, V + 1)])
    for u, v, _ in L:
        G.add_edge(u, v)
    return G


def find_paths(path, paths=[]) -> list[Path]:
    for item in path.iterdir():
        if item.is_file():
            paths.append(item)
        elif item.is_dir():
            paths.extend(find_paths(GRAPHS_PATH / item, []))
    return paths


#################################### UNIQUE ####################################


def check_planarity(G):
    return 1 if nx.algorithms.planarity.check_planarity(G)[0] else 0


################################################################################


def run(path):
    G = to_graph(loadWeightedGraph(path))
    result = check_planarity(G)
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
