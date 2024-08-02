# https://marcinlos.github.io/algograf/lab1

from pathlib import Path
import heapq

from dimacs import *

GRAPHS_PATH = Path(__file__).parent.absolute() / "graphs"


def main():
    paths = [item for item in GRAPHS_PATH.iterdir() if item.is_file()]
    # zad3(GRAPHS_PATH / "clique5")
    for path in paths:
        zad3(path)


def zad1(path):
    """Napisz skrypt wczytujący przykładowy graf i wypisujący krawędzie."""
    # loadWeightedGraph -> (V, L), where:
    #  V - number of vertices
    #  L -  list of edges in the format (x,y,w)
    print(*loadWeightedGraph(path)[1], sep="\n")


def zad2(path):
    """
    Rozwiązanie oparte of find-union.
    1. Sortujemy krawędzie malejąco.
    2. Kolejne krawędzie dodajemy do unii
    3. Jeśli w unii znajdą się 's' i 't' to istnieje ścieżka między nimi
       oraz ostatnio dodana krawędź jest o najmniejszej wadze w ścieżce.
    """
    V, L = loadWeightedGraph(path)
    edges = []  # (weight, from, to)
    parent = [i for i in range(V)]  # set parent to self for each
    rank = [1 for _ in range(V)]  # initial rank(size) to 1 for each
    s, t = 0, 1  # from, to
    min_weight = -1

    def find(v):
        while v != parent[v]:
            parent[v] = parent[parent[v]]  # optimization
            v = parent[v]
        return v

    def union(v1, v2):
        p1, p2 = find(v1), find(v2)
        if p1 == p2:
            return False
        if rank[p1] > rank[p2]:
            parent[p2] = p1
            rank[p1] += rank[p2]
        else:
            parent[p1] = p2
            rank[p2] += rank[p1]
        return True

    for x, y, w in L:
        heapq.heappush(edges, (-w, x - 1, y - 1))

    while edges:
        w, v1, v2 = heapq.heappop(edges)
        union(v1, v2)
        if find(s) == find(t):
            min_weight = -w
            break

    print(min_weight, readSolution(path), path)
    assert int(readSolution(path)) == min_weight


def zad3(path):
    """
    Rozwiązanie oparte o wyszukiwanie binarne + BFS/DFS.
    """
    V, L = loadWeightedGraph(path)
    G = [[] for i in range(V)]
    edges = []
    s, t = 0, 1

    def dfs(G, value):  # value = discard edges with
        stack = []
        # visited_order = []
        visited = [False for _ in range(V)]
        stack.append(s)
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                # if v == t:  # timeit?
                #     break
                # visited_order.append(v)
                for u, w in G[v]:
                    if not visited[u] and w >= value:
                        stack.append(u)
        return visited[t]

    def binary_search(edges):
        result_index = -1
        low, high = 0, len(edges) - 1
        while low <= high:
            mid = (low + high) // 2
            if dfs(G, edges[mid]):
                result_index = mid
                low = mid + 1
            else:
                high = mid - 1
        return result_index

    for u, v, w in L:
        G[u - 1].append((v - 1, w))
        G[v - 1].append((u - 1, w))
        edges.append(w)
    edges.sort()

    result = binary_search(edges)
    if result != -1:  # if found change index to value
        result = edges[result]

    read_solution = int(readSolution(path))
    print(read_solution, result, path)
    assert read_solution == result


if __name__ == "__main__":
    main()
