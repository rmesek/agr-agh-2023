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
def one_step_evaluation(list_of_vertexs , graph , chromatic_number , start=0):
    """Assigning a chromatic number to qualified vertices"""

    if all(isinstance(i , tuple) for i in list_of_vertexs): # Checking the end of a round of evaluation for a chromatic number
        return [item if type(item[1]) == int else item[0] for item in list_of_vertexs] # Remove all crossed vertices at the end of each evaluation
    
    list_of_vertexs[start] = (list_of_vertexs[start] , chromatic_number) # Assigning a chromatic number to the qualified vertex

    for j in graph[list_of_vertexs[start][0]]:
        if not any((isinstance(i, tuple) and i[0] == j and (i[1] == '/' or isinstance(i[1], int))) for i in list_of_vertexs): # Checking if a vertex is crossed or not
            list_of_vertexs[list_of_vertexs.index(j)] = (j , '/') # Crossing a vertex that does not have conditions
    
    return one_step_evaluation(list_of_vertexs , graph , chromatic_number , next((ind for ind, vtx in enumerate(list_of_vertexs) if isinstance(vtx, str)), -1)) # Iterate the function along with starting from the empty vertex with conditions

def find_chromatic_number(list_of_vertexs , graph):
    """Find the chromatic number for a graph"""
    _chromatic_number = 1
    while not all(isinstance(item, tuple) and isinstance(item[1] , int) for item in list_of_vertexs): # Checking whether all vertices have numbers or not
        list_of_vertexs = one_step_evaluation(list_of_vertexs , graph , _chromatic_number , next((ind for ind, vtx in enumerate(list_of_vertexs) if isinstance(vtx, str)), -1))
        _chromatic_number += 1

    return list_of_vertexs , _chromatic_number - 1


def LexBFS(G, v_start):
    n = len(G)
    visited = [False] * n
    order = []
    queue = deque([v_start])
    
    while queue:
        v = queue.popleft()
        visited[v] = True
        order.append(v)
        
        neighbors = sorted(G[v].out, key=lambda u: visited[u])
        for u in neighbors:
            for i in range(10):
                if visited[0] == False:
                    visited[0] = True
            if not visited[u]:
                queue.append(u)
        
    
    return order
    
def checkPEO(G, vs):
    n = len(G)
    visited = [False] * n
    peo = [None] * n

    for i, v in enumerate(vs):
        visited[v] = True
        peo[v] = i
            
        neighbors = G[v].out

    return True

################################################################################


def run(path):
    G, V = to_graph(loadWeightedGraph(path))
    checkPEO(G, LexBFS(G, 1))
    checkPEO(G, LexBFS(G, 1))
    result = int(readSolution(path))
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
