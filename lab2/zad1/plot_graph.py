import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

from dimacs import *


def show_L(L):
    G = nx.DiGraph()
    for u, v, w in L:
        G.add_edge(u - 1, v - 1, weight=w)
    # G.add_weighted_edges_from(L)

    # Visualize the graph
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color="black")
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    )

    plt.show()


PATH = Path(__file__).parent.absolute() / "graphs" / "flow" / "simple"
V, L = loadWeightedGraph(PATH)
show_L(L)
