# https://marcinlos.github.io/algograf/lab2
from pathlib import Path
import timeit
from collections import deque
from dimacs import *

GRAPHS_PATH = Path(__file__).parent.absolute() / "graphs"


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
    graph = to_graph(loadWeightedGraph(path))
    result = ford_fulkerson(graph, 0, len(graph) - 1)
    print(
        f"{f'GOT {result} EXPECTED {int(readSolution(path))}' if result != int(readSolution(path)) else f'{result}'}"
    )


def to_graph(G):
    V, L = G
    graph = [[0 for _ in range(V)] for _ in range(V)]
    for u, v, w in L:
        graph[u - 1][v - 1] = w
    return graph


def find_paths(path, paths=[]) -> list[Path]:
    for item in path.iterdir():
        if item.is_file():
            paths.append(item)
        elif item.is_dir():
            paths.extend(find_paths(GRAPHS_PATH / item, []))
    return paths


def bfs(graph, start, end, parent):
    visited = [False] * len(graph)
    queue = deque()
    queue.append(start)
    visited[start] = True

    while queue:
        u = queue.popleft()
        for vertex, capacity in enumerate(graph[u]):
            if visited[vertex] == False and capacity > 0:
                queue.append(vertex)
                visited[vertex] = True
                parent[vertex] = u

    return visited[end]


def ford_fulkerson(graph, source, sink):
    max_flow = 0
    n = len(graph)
    parent = [-1] * n

    while bfs(graph, source, sink, parent):
        path_flow = float("inf")
        s = sink

        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = sink

        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]

    return max_flow


if __name__ == "__main__":
    main()
