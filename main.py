import os
import re
from collections import defaultdict, deque


def find_go_files(directory):
    """Finds all .go files in a directory and its subdirectories."""
    go_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".go"):
                go_files.append(os.path.join(root, file))
    return go_files


def extract_imports(file_path):
    """Extracts imported packages from a single Go file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find import statements, including grouped imports
            # import "fmt"
            # import (
            #   "net/http"
            #   custom "example.com/custom/pkg"
            # )
            import_block_match = re.search(r'import\s*\(([^)]+)\)', content, re.MULTILINE)
            if import_block_match:
                block_content = import_block_match.group(1)
                lines = block_content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('//'): # Skip empty lines and comments
                        continue
                    # Handle aliased imports (e.g., _ "pkg", alias "pkg")
                    parts = line.split()
                    if len(parts) > 0:
                        # The package path is usually the last part, enclosed in quotes
                        pkg_match = re.search(r'"([^"]+)"', parts[-1])
                        if pkg_match:
                            imports.add(pkg_match.group(1))

            # Find single line imports
            single_imports = re.findall(r'import\s+"([^"]+)"', content)
            for imp in single_imports:
                imports.add(imp)

    except Exception as e:
        print(f"Error reading or parsing file {file_path}: {e}")
    return imports


def get_package_name_from_path(file_path, base_dir):
    """
    Determines the Go package name from its file path relative to a base directory.
    Assumes the directory containing the .go files is the package name.
    """
    abs_file_path = os.path.abspath(file_path)
    abs_base_dir = os.path.abspath(base_dir)
    if not abs_file_path.startswith(abs_base_dir):
        # This can happen if file_path is already an absolute path outside base_dir
        # or if base_dir is not a proper prefix.
        # For simplicity, we'll try to infer from the directory.
        return os.path.basename(os.path.dirname(abs_file_path))

    relative_path = os.path.relpath(os.path.dirname(abs_file_path), abs_base_dir)
    # Replace OS-specific path separators with Go's forward slash
    package_name = relative_path.replace(os.sep, '/')
    if package_name == ".": # Files in the root of the scanned directory
        return os.path.basename(abs_base_dir) # Use the base directory's name
    return package_name if package_name else os.path.basename(abs_base_dir)



def build_dependency_graph(directory):
    """
    Builds a dependency graph from Go files in a directory.
    Returns:
        graph: A dict where keys are package names and values are sets of dependencies.
        all_packages: A set of all unique package names found.
        package_files: A dict mapping package names to list of their .go files.
    """
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    all_packages = set()
    package_files = defaultdict(list)
    go_files = find_go_files(directory)
    # First pass: identify all packages defined in the directory
    # This assumes directory structure maps to package structure within the project
    defined_packages = set()
    for go_file in go_files:
        pkg_name = get_package_name_from_path(go_file, directory)
        defined_packages.add(pkg_name)
        package_files[pkg_name].append(go_file)
        all_packages.add(pkg_name) # Ensure defined packages are in all_packages

    # Second pass: build graph
    for go_file in go_files:
        current_pkg_name = get_package_name_from_path(go_file, directory)
        imports = extract_imports(go_file)
        all_packages.add(current_pkg_name) # Ensure current package is in all_packages
        for imp in imports:
            all_packages.add(imp) # Add imported packages to all_packages
            # We only care about dependencies *within* the scanned project
            # or standard library packages (which won't be in defined_packages
            # unless you're scanning the Go source itself).
            # If an import is not a package defined in our project, it's an external dependency.
            # For topological sort *within* the project, we point from dependent to dependency.
            # So, if current_pkg_name imports 'imp', the edge is imp -> current_pkg_name
            # (meaning 'imp' must be processed before 'current_pkg_name').
            if imp != current_pkg_name: # Avoid self-loops in this context
                graph[imp].add(current_pkg_name)
                in_degree[current_pkg_name] += 1
                # print(f"Dependency: {imp} -> {current_pkg_name}")


    # Ensure all defined packages are in in_degree map, even if they have no incoming internal dependencies
    for pkg in defined_packages:
        if pkg not in in_degree:
            in_degree[pkg] = 0
    for pkg in all_packages: # Also ensure all imported packages are there for completeness
        if pkg not in in_degree:
            in_degree[pkg] = 0

    return graph, in_degree, all_packages, package_files


def topological_sort(graph, in_degree, all_packages):
    """
    Performs a topological sort on the dependency graph (Kahn's algorithm).
    The graph should represent 'A depends on B' as an edge B -> A.
    This means B must come before A in the sorted list.
    """
    queue = deque([pkg for pkg in all_packages if in_degree[pkg] == 0])
    sorted_order = []
    # print(f"Initial queue (in_degree 0): {list(queue)}")
    # print(f"Initial in_degrees: {dict(in_degree)}")
    # print(f"Graph: { {k: list(v) for k,v in graph.items()} }")

    while queue:
        u = queue.popleft()
        sorted_order.append(u)

        # For each neighbor v of u, remove edge u-v from graph
        # In our graph, if u -> v, it means u is a dependency of v.
        # So we look for packages v that depend on u.
        # The graph stores dependencies: key depends on elements in its set value.
        # No, the graph is: key -> set of packages that import key
        # So if 'u' is processed, we look at packages 'v' that import 'u'
        for v in sorted(list(graph[u])): # Sort for deterministic output if multiple choices
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                # print(f"Adding {v} to queue. In-degree now 0.")

    # Check for cycles
    if len(sorted_order) != len(all_packages):
        # Identify nodes involved in cycles
        cycled_nodes = set(all_packages) - set(sorted_order)
        # Try to find one cycle path (this is a simplified cycle detection)
        # More robust cycle detection might be needed for complex cases.
        path = []
        visited_in_cycle_detection = set()
        found_cycle_path = []

        # Function to perform DFS to find a cycle
        def find_cycle_dfs(node, current_path_nodes, recursion_stack):
            nonlocal found_cycle_path
            if found_cycle_path: # If a cycle path is already found, stop.
                return

            visited_in_cycle_detection.add(node)
            recursion_stack.add(node)
            current_path_nodes.append(node)

            # The graph represents: dependency -> dependent packages
            # So, if A imports B (A depends on B), the edge is B -> A
            # We need to trace dependencies backwards or invert the graph to find "A imports B"
            # For cycle detection, we want to follow the "imports" relation.
            # Let's consider what our current graph means:
            # graph[dependency_X] = {pkg_A, pkg_B} means pkg_A and pkg_B import dependency_X
            # A cycle exists if A imports B, B imports C, C imports A.
            # This means: B->A, C->B, A->C in our graph.
            # We need to find a path like X -> Y -> Z -> X

            for neighbor in sorted(list(graph.get(node, []))): # For each package that 'node' is a dependency for
                if found_cycle_path: return
                if neighbor in recursion_stack: # Cycle detected
                    # Cycle is from neighbor back to node, and includes elements in recursion_stack
                    try:
                        start_index = current_path_nodes.index(neighbor)
                        found_cycle_path = current_path_nodes[start_index:] + [neighbor]
                    except ValueError: # Should not happen if logic is correct
                         found_cycle_path = current_path_nodes + [neighbor] # fallback
                    return
                if neighbor not in visited_in_cycle_detection:
                    find_cycle_dfs(neighbor, current_path_nodes, recursion_stack)
                    if found_cycle_path: return

            current_path_nodes.pop()
            recursion_stack.remove(node)


        # Attempt to find one cycle path from the remaining nodes
        # To properly detect import cycles like A -> B -> C -> A,
        # we need to build an "imports" graph (A depends on B, so A -> B)
        # and then run DFS on that.
        # Our current `graph` is `dependency -> set_of_dependents`.
        # Let's build the reverse (actual import graph) for cycle reporting.
        imports_graph = defaultdict(set)
        temp_in_degree = defaultdict(int) # For Kahn's on the imports_graph if needed

        # Re-parse or use previously gathered info to build actual imports_graph
        # This is a bit inefficient to re-iterate, but ensures clarity for cycle detection
        # For this example, we'll assume `all_packages` and `package_files` are available
        # and `extract_imports` can give us the direct dependencies.

        # This part is tricky because the `graph` for Kahn's was `dependency -> dependent`
        # For cycle reporting, `A imports B, B imports C, C imports A` is more natural.
        # Let's report the nodes that couldn't be sorted.
        cycle_details = "\nNodes involved in cycles (or unreachable if graph not fully connected):"
        remaining_nodes = set(all_packages) - set(sorted_order)
        for node in remaining_nodes:
            cycle_details += f"\n  - {node} (remaining in-degree: {in_degree[node]})"
            # To show its direct dependencies that might be part of the cycle:
            # We need to find which packages *IT* imports.
            # This requires going back to the original file parsing logic.
            # For simplicity, we'll just list the nodes.
            # A more robust cycle output would trace the actual cycle.

        return None, f"Cycle detected in dependencies. Processing halted. {cycle_details}"

    return sorted_order, None


def main():
    """Main function to orchestrate the script."""
    target_directory = input("Enter the root directory of the Go project: ")
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found.")
        return

    print(f"\nScanning Go files in '{target_directory}'...\n")
    graph, in_degree, all_packages, package_files_map = build_dependency_graph(target_directory)

    if not all_packages:
        print("No Go packages found or no imports detected.")
        return

    print("Found the following packages:")
    # Filter to show only packages that have .go files within the scanned directory
    # (i.e., locally defined packages)
    local_packages = {pkg for pkg, files in package_files_map.items() if files}
    # Also include packages that were imported but not locally defined, these are external
    external_packages = all_packages - local_packages

    for pkg in sorted(list(local_packages)):
        print(f"  - {pkg} (local)")
    if external_packages:
        print("\nReferenced external packages (will be ordered if they are part of dependency chains):")
        for pkg in sorted(list(external_packages)):
            print(f"  - {pkg} (external/standard library)")

    print("\nCalculating topological order of package imports (dependencies first)...")
    sorted_packages, error_message = topological_sort(graph, in_degree, all_packages)

    if error_message:
        print(f"\nError: {error_message}")
    elif sorted_packages:
        print("\nTopological Order (Dependencies first):")
        # Filter the sorted list to primarily show the order relevant to the project's packages
        # External/std lib packages will appear early if they are dependencies.
        for i, pkg_name in enumerate(sorted_packages):
            pkg_type = "(local)" if pkg_name in local_packages else "(external/std lib)"
            # Only print packages that were either defined locally or are direct/transitive
            # dependencies of local packages. Purely external packages that nothing
            # local depends on (if they somehow got into `all_packages` without being imported)
            # might not be relevant here.
            print(f"  {i+1}. {pkg_name} {pkg_type}")
    else:
        print("\nCould not determine topological order. No packages or an unknown error occurred.")


if __name__ == "__main__":
    main()
