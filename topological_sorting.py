from collections import defaultdict
from node import Node

def topological_sort(in_graph: defaultdict[str, set], in_degree: defaultdict[str, int]) -> list[Node]:
    graph: dict[str, Node] = dict()
    queue: list[Node] = []
    sorted_list: list[Node] = []
    for node_name in in_graph:
        graph[node_name] = Node(node_name, in_graph[node_name], in_degree[node_name])

    for node_name in graph.items():
        if graph[node_name].degree == 0:
            queue.append(graph[node_name])

    # TODO
    while len(queue) > 0:
        node = queue.pop(0)
        sorted_list.append(node)

        for vertex in node.vertices:
            w = graph[vertex]
            w.degree -= 1
            if w.degree == 0:
                queue.append(w)

    if len(sorted_list) != len(in_graph):
        print("contains cycle")

    return sorted_list

def nodes_to_dict(nodes: list[Node]) -> defaultdict[str, set[str]]:
    node_dict: defaultdict[str, set[str]] = defaultdict(set)

    for node in nodes:
        node_dict[node.name] = node.vertices

    return node_dict
