import graphviz

# TODO: Finalize
def render(graph):
    dot = graphviz.Digraph('deps')

    for node in graph:
        vertices = graph[node]
        dot.node(node)
        for vertice in vertices:
            dot.edge(vertice, node)

    dot.render("output/graph")