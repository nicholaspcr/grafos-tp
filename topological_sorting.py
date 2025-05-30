import sys
from collections import defaultdict

class Node:
    name: str
    vertices: set[str]
    degree: int

    def __init__(self, name: str, vertices: set[str], degree: int):
        self.name = name
        self.vertices = vertices
        self.degree = degree

    def __str__(self):
        return ('Node['
                f'name={self.name},'
                f'vertices={self.vertices},'
                f'degree={self.degree}'
                ']')

    def __repr__(self):
        return self.__str__()

def sort(in_graph: defaultdict[str, set], in_degree: defaultdict[str, int]) -> list[Node]:
    graph: dict[str, Node] = dict()
    queue: list[Node] = []
    sorted_list: list[Node] = []
    for node_name in in_graph:
        graph[node_name] = Node(node_name, in_graph[node_name], in_degree[node_name])

    for node_name in graph:
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

    # TODO
    cycle = False
    for node_name in graph:
        node = graph[node_name]
        if node.degree > 0:
            if not cycle:
                print("Cycling dependencies:", file=sys.stderr)
            cycle = True
            print(f'  - {node_name} (degree={node.degree})', file=sys.stderr)
            for vertex in node.vertices:
                print(f'    - {vertex} (degree={graph[vertex].degree})', file=sys.stderr)

    if cycle:
        return None

    return sorted_list

def nodes_to_dict(nodes: list[Node]) -> defaultdict[str, set[str]]:
    node_dict: defaultdict[str, set[str]] = defaultdict(set)

    for node in nodes:
        node_dict[node.name] = node.vertices

    return node_dict
