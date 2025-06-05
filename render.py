import os
import webbrowser
import graphviz

def render(graph, sorted_nodes, external_packages, module_prefix: str):
    dot = graphviz.Digraph('DependencyGraph', comment='Topological Sort')
    dot.attr(rankdir='LR', splines='ortho')
    dot.attr('node', shape='box', style='rounded')

    print("Generating rendered graph")
    for layer in sorted_nodes:
        with dot.subgraph() as s:
            s.attr(rank='same')
            for node_name in layer:
                if node_name in external_packages:
                    s.node(node_name, style='filled', fillcolor='tomato', fontcolor='white')
                else:
                    s.node(node_name, style='filled', fillcolor='lightgrey')

    # --- Step 2: Create all the edges based on the original dependencies ---
    for node in graph:
        for v in graph[node]:
            dot.edge(node, v)

    # output_filename = 'dependency_graph.gv'
    # dot.render(output_filename, view=True, format='pdf')
    # print(f"Graph saved to {output_filename} and {output_filename}.pdf")
    # dot.render('dependency_graph', format='svg', view=True)
    svg_output = dot.pipe(format='svg').decode('utf-8')

    # Create a simple HTML file with the SVG embedded
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Graphviz in HTML</title>
            <style>
                body {{
                    margin: 0;
                    padding: 2rem; /* Add some padding around the body */
                    background-color: #f0f2f5; /* A light background for the page */
                    min-height: 100vh; /* Ensure body takes at least full viewport height */
                    box-sizing: border-box;
                    width: fit-content;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                    margin-bottom: 2rem;
                }}
                .graph-container svg {{
                    display: block; /* Removes extra space below inline SVGs and allows margin auto if needed */
                    width: auto;    /* Allows the SVG to take its natural width as defined by Graphviz */
                }}
            </style>
        </head>
        <body>
            <h1>Static Graphviz Graph</h1>
            <div class="graph-container">
                {svg_output}
            </div>
        </body>
        </html>
        """

    # Save the HTML to a file
    output_filename = f'{module_prefix.replace("/", "_")}.html'
    with open(output_filename, 'w') as f:
        f.write(html_content)

    print(f"Graph saved to {os.path.realpath(output_filename)}")

    # Optionally, open the file in a web browser
    webbrowser.open(f'file://{os.path.realpath(output_filename)}')
