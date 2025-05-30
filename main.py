import os
import tests

from time import sleep
from dependency_graph_builder import BuildDependencyGraph
from graph_renderer import render
from topological_sorting import sort, nodes_to_dict


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

    # fail = False
    # for package in all_packages:
    #     if not graph[package]:
    #         if not fail:
    #             print("Packages without node:", file=sys.stderr)
    #         fail = True
    #         print(f'  - {package}', file=sys.stderr)
    # if fail: return

    # Add missing nodes
    for package in all_packages:
        if not graph[package]:
            graph[package] = set()

    # Filter to show only packages that have .go files within the scanned directory
    # (i.e., locally defined packages)
    local_packages = {pkg for pkg, files in package_files_map.items() if files}
    # Also include packages that were imported but not locally defined, these are external
    external_packages = all_packages - local_packages

    print("Found the following packages:")
    for pkg in sorted(list(local_packages)):
        print(f"  - {pkg} (local)")
    if external_packages:
        print("\nReferenced external packages (will be ordered if they are part of dependency chains):")
        for pkg in sorted(list(external_packages)):
            print(f"  - {pkg} (external/standard library)")

    # Make sure stderr doesn't mix with stdout
    sleep(0.01)

    sorted_nodes = sort(graph, in_degree)
    if sorted_nodes is None:
        return
    sorted_nodes_dict = nodes_to_dict(sorted_nodes)

    # render(sorted_nodes_dict)

    # tests.test(sorted_nodes_dict)


if __name__ == "__main__":
    main()
