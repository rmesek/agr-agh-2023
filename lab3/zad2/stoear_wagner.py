# https://marcinlos.github.io/algograf/lab3
from pathlib import Path
import timeit
from collections import deque
from random import randint
from dimacs import *

GRAPHS_PATH = Path(__file__).parent.absolute() / "graphs"


class Node:
    def __init__(self):
        self.edges = {}  # słownik par mapujący wierzchołki do których są krawędzie na ich wagi

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight  # dodaj krawędź do zadanego wierzchołka
        # o zadanej wadze; a jeśli taka krawędź
        # istnieje, to dodaj do niej wagę

    def delEdge(self, to):
        del self.edges[to]  # usuń krawędź do zadanego wierzchołka


def main():
    paths = find_paths(GRAPHS_PATH)
    # paths = [GRAPHS_PATH / "clique5"]
    for path in paths:
        print()
        print(path.relative_to(GRAPHS_PATH))
        try:
            start = timeit.default_timer()
            run(path)
            print(f"Time: {timeit.default_timer() - start :.3f}s")
        except KeyboardInterrupt:
            print("Interrupted!")


def run(path):
    G, V = to_graph(loadWeightedGraph(path))
    result = stoer_wagner(G, V)
    print(f"{f'GOT {result} EXPECTED {int(readSolution(path))}' if result != int(readSolution(path)) else f'{result}'}")


def to_graph(G):
    V, L = G
    G = [Node() for i in range(V + 1)]
    for x, y, c in L:
        G[x].addEdge(y, c)
        G[y].addEdge(x, c)
    return G, set([i for i in range(1, V + 1)])


def find_paths(path, paths=[]) -> list[Path]:
    for item in path.iterdir():
        if item.is_file():
            paths.append(item)
        elif item.is_dir():
            paths.extend(find_paths(GRAPHS_PATH / item, []))
    return paths


def print_graph(G):
    for i in range(len(G)):
        print(i, ":", G[i].edges)


def merge(G, x, y):
    y_edges = list(G[y].edges)
    for i in y_edges:
        if i != x:
            G[x].addEdge(i, G[y].edges[i])
            G[i].addEdge(x, G[i].edges[y])
        G[i].delEdge(y)
        G[y].delEdge(i)


def minimum_cut_phase(G, V):
    from queue import PriorityQueue

    Q = PriorityQueue()

    # a = randint(1,len(G)) #arbitrary
    a = next(iter(V))
    S = set([a])

    values = [-G[i].edges.get(a, 0) for i in range(len(G))]
    for i in range(1, len(G)):
        if len(G[i].edges) > 0:
            Q.put((-G[i].edges.get(a, 0), i))

    seen = [False for _ in range(len(G))]
    seen[0] = True
    last_but_one = 0
    last = a

    while not Q.empty():
        q = Q.get()
        v = q[1]
        if seen[v]:
            continue
        seen[v] = True
        cut = -q[0]
        last_but_one = last
        last = v
        for i in G[v].edges:
            values[i] -= G[i].edges.get(v, 0)
            if values[i] < 0:
                Q.put((values[i], i))

    return (last, last_but_one, cut)


def stoer_wagner(G, V):
    # G, V = read(path)
    res = float("inf")
    # print_graph(G)
    while len(V) > 1:
        x, y, r = minimum_cut_phase(G, V)
        # print(x,y,r)
        merge(G, x, y)
        V.remove(y)
        res = min(res, r)
        # print_graph(G)

    return res


if __name__ == "__main__":
    main()
