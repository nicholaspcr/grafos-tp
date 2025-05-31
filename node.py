class Node:
    """
    Represents the Node used in the graph that represent the dependency relationships between Golang packages.
    """

    name: str
    vertices: set[str]
    in_degree: int

    def __init__(self, name: str, vertices: set[str], in_degree: int):
        """
        Initializes the Node.

        Args:
            name (str): The name of the Vertice.
            vertices (set[str]): A set of vertices to which this Node is connected to.
            in_degree (int): in_degree of the Node.
        """
        self.name = name
        self.vertices = vertices
        self.degree = in_degree

    def __str__(self):
        return ('Node['
                f'name={self.name},'
                f'vertices={self.vertices},'
                f'degree={self.degree}'
                ']')

    def __repr__(self):
        return self.__str__()
