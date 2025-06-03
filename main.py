import os
import graphviz
import webbrowser

from dependency_graph_builder import BuildDependencyGraph
from topological_sorting import Topological

def main():
    """Main function to orchestrate the script."""
    target_directory = input("Enter the root directory of the Go project: ")
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{os.path.abspath(target_directory)}' not found.")
        return

    builder = BuildDependencyGraph(target_directory)
    graph, in_degree, all_packages, package_files_map = builder.build_dependency_graph()

    if not all_packages:
        print("No Go packages found or no imports detected.")
        return

    # Filter to show only packages that have .go files within the scanned directory
    # (i.e., locally defined packages)
    local_packages = {pkg for pkg, files in package_files_map.items() if files}
    # Also include packages that were imported but not locally defined, these are external
    external_packages = all_packages - local_packages

    # for key in external_packages:
    #     del in_degree[key]
    #     del graph[key]

    # # NOTE: This prints the packages found separated by external and local packages.
    # print("Found the following packages:")
    # for pkg in sorted(list(local_packages)):
    #     print(f"  - {pkg} (local)")
    # if external_packages:
    #     print("\nReferenced external packages (will be ordered if they are part of dependency chains):")
    #     for pkg in sorted(list(external_packages)):
    #         print(f"  - {pkg} (external/standard library)")

    print("Sorting graph")
    try:
        topological = Topological()
        if topological.is_cyclic(graph):
            print("There is a cycle in the dependencies, can't generate topological sort")
            return

        sorted_nodes = topological.sort_group(graph, in_degree)

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
        output_filename = 'static_graph.html'
        with open(output_filename, 'w') as f:
            f.write(html_content)

        print(f"Graph saved to {os.path.realpath(output_filename)}")

        # Optionally, open the file in a web browser
        webbrowser.open(f'file://{os.path.realpath(output_filename)}')


    except Exception as e:
        print("Error is: ", e)

if __name__ == "__main__":
    main()
