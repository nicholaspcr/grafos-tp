from collections import defaultdict, deque

class Topological:
    """
    Encapsulates the logic for generating the topological sort of the dependency graph.
    """

    def __init__(self, graph):
        """
        Initializes Topological.

        Args:
            directory (str): The root directory of the Go project.
        """
        self.graph = graph
        self.visited = defaultdict(bool)
        self.recursion_stack = defaultdict(bool)

    def _is_cyclic_util(
        self,
        node: str,
    ):
        # If the node is already in the current recursion stack, a cycle is detected
        if self.recursion_stack[node]:
            return True

        # If the node is already visited and not part of the recursion stack, skip it
        if self.visited[node]:
            return False

        self.visited[node] = True
        self.recursion_stack[node] = True

        for v in self.graph[node]:
            if self._is_cyclic_util(v):
                return True

        # Remove the node from the recursion stack before returning
        self.recursion_stack[node] = False
        return False

    def is_cyclic(self) -> bool:
        # clears all keys
        self.visited.clear()
        self.recursion_stack.clear()

        for node in self.graph:
            self.visited[node] = False
            self.recursion_stack[node] = False

        for node in list(self.graph):
            if not self.visited[node] and self._is_cyclic_util(node):
                return True
        return False


    def sort_group(self, graph: defaultdict[str, set], in_degree: defaultdict[str, int]) -> list[str]:
        """
        Performs a topological sort on a directed acyclic graph (DAG).
        Uses Kahn's algorithm.
        """
        queue = deque()
        leaves_matrix: list[str] = []

        leaves_nodes = []
        for v in graph:
            if in_degree[v] == 0:
                leaves_nodes.append(v)
        queue.append(leaves_nodes)

        while queue:
            leaves_list = queue.popleft()
            leaves_matrix.append(leaves_list)
            new_leaves = []

            for node in leaves_list:
                for v in graph[node]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        new_leaves.append(v)

            if new_leaves:
                queue.append(new_leaves)

        return leaves_matrix
