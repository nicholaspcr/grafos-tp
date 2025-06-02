import os
import graphviz
import webbrowser

from dependency_graph_builder import BuildDependencyGraph
from topological_sorting import Topological

def main():
    """Main function to orchestrate the script."""
    target_directory = input("Enter the root directory of the Go project: ")
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found.")
        return

    builder = BuildDependencyGraph(target_directory)
    graph, in_degree, all_packages, package_files_map = builder.build_dependency_graph()

    if not all_packages:
        print("No Go packages found or no imports detected.")
        return

    # # Filter to show only packages that have .go files within the scanned directory
    # # (i.e., locally defined packages)
    # local_packages = {pkg for pkg, files in package_files_map.items() if files}
    # # Also include packages that were imported but not locally defined, these are external
    # external_packages = all_packages - local_packages

    # # NOTE: This prints the packages found separated by external and local packages.
    # print("Found the following packages:")
    # for pkg in sorted(list(local_packages)):
    #     print(f"  - {pkg} (local)")
    # if external_packages:
    #     print("\nReferenced external packages (will be ordered if they are part of dependency chains):")
    #     for pkg in sorted(list(external_packages)):
    #         print(f"  - {pkg} (external/standard library)")

    try:
        topological = Topological()
        if topological.is_cyclic(graph):
            print("There is a cycle in the dependencies, can't generate topological sort")
            return

        sorted_nodes = topological.sort_group(graph, in_degree)
        print(f"Sorted nodes: {sorted_nodes}")

        dot = graphviz.Digraph('DependencyGraph', comment='Topological Sort')
        dot.attr(rankdir='TB', splines='ortho') # Using orthogonal lines can look cleaner
        dot.attr('node', shape='box', style='rounded') # Style for nodes

        for layer in sorted_nodes:
            with dot.subgraph() as s:
                s.attr(rank='same')
                for node_name in layer:
                    s.node(node_name)

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
        <html>
        <head>
            <title>Graphviz in HTML</title>
            <style>
                body {{ font-family: sans-serif; display: flex; justify-content: center; }}
            </style>
        </head>
        <body>
            <div>
                <h1>Static Graphviz Graph</h1>
                {svg_output}
            </div>
        </body>
        </html>
        """

        # Save the HTML to a file
        output_filename = 'static_graph.html'
        with open(output_filename, 'w') as f:
            f.write(html_content)

        print(f"Graph saved to {output_filename}")

        # Optionally, open the file in a web browser
        webbrowser.open(f'file://{os.path.realpath(output_filename)}')


    except Exception as e:
        print("Error is: ", e)

if __name__ == "__main__":
    main()
