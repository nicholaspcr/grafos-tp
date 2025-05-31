from collections import defaultdict, deque

def topological_sort(graph: defaultdict[str, set], in_degree: defaultdict[str, int]) -> list[str]:
    """
    Performs a topological sort on a directed acyclic graph (DAG).
    Uses Kahn's algorithm.
    """
    queue = deque()
    result: list[str] = []

    for v in graph:
        if in_degree[v] == 0:
            queue.append(v)

    while queue:
        u = queue.popleft()
        result.append(u)

        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(result) != len(graph):
        raise ValueError("Graph contains a cycle, topological sort is not possible.")

    return result
