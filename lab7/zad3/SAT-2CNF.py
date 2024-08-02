# https://marcinlos.github.io/algograf/lab7
from pathlib import Path
import timeit
import networkx as nx
from dimacs import *

GRAPHS_PATH = Path(__file__).parent.absolute() / "graphs"


def to_graph(G) -> nx.Graph:
    V, L = G
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(1, V + 1)])
    for u, v in L:
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

def satisfiability(G: nx.DiGraph):
    scc = nx.algorithms.components.strongly_connected_components(G)
    for s in scc:
        for x in s:
            if -x in s:
                return False
    return True

def valuation(G: nx.DiGraph):
    H = nx.DiGraph()
    scc = nx.algorithms.components.strongly_connected_components(G)
    for s in scc:
        H.add_node(frozenset(s))
    for u, v in G.edges:
        # TODO: Krok 3
        print(u, v)


def sat_2cnf(G: nx.DiGraph):
    if satisfiability(G):
        valuation(G)

    else:
        return False


################################################################################


def run(path):
    G = to_graph(loadCNFFormula(path))
    result = sat_2cnf(G)
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
