import os

from dependency_graph_builder import BuildDependencyGraph
from render import render
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
    print(f"graph: {graph}")
    print(f"in_degree: {in_degree}")

    print("Sorting graph")
    try:
        topological = Topological(graph)
        if topological.is_cyclic():
            print("There is a cycle in the dependencies, can't generate topological sort")
            return

        sorted_nodes = topological.sort_group(graph, in_degree)

        render(graph, sorted_nodes, external_packages)

    except Exception as e:
        print("An unexpected error occurred: ", e)

if __name__ == "__main__":
    main()
