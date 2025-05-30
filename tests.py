from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt

# TODO: Generate an usable graph
def test(graph: defaultdict[str, set[str]]):
    g = nx.DiGraph()

    for node in graph:
        vertices = graph[node]
        g.add_nodes_from(graph.keys())
        for vertice in vertices:
            g.add_edge(vertice, node)

    nx.draw_networkx(g, with_labels=True, node_size=30)
    plt.show()