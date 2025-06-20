import os
import re
from collections import defaultdict

class BuildDependencyGraph:
    """
    Encapsulates the logic for finding Go files, extracting imports,
    determining package names, and building a dependency graph for a Go project.
    """
    def __init__(self, directory):
        """
        Initializes the BuildDependencyGraph with the project's root directory.

        Args:
            directory (str): The root directory of the Go project.
        """
        self.base_dir = os.path.abspath(directory)
        self.module_prefix = self._determine_module_prefix()

    def _determine_module_prefix(self):
        """
        Tries to determine the module prefix from a go.mod file in the base directory.
        """
        go_mod_path = os.path.join(self.base_dir, "go.mod")
        with open(go_mod_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^module\s+([^\s]+)', content, re.MULTILINE)
            return match.group(1).strip()

    def find_go_files(self):
        """Finds all .go files in the base directory and its subdirectories."""
        go_files = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".go") and not file.endswith("_test.go"):
                    go_files.append(os.path.join(root, file))
        return go_files

    @staticmethod
    def extract_imports(file_path):
        """
        Extracts imported packages from a single Go file.
        This method is static as it doesn't depend on the instance's state and
        now correctly handles both single-line and grouped imports.
        """
        imports = set()
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Find and parse grouped imports: import (...)
        # The re.DOTALL flag allows '.' to match newlines.
        import_block_match = re.search(r'import\s+\((.*?)\)', content, re.DOTALL)
        if import_block_match:
            # Extract the content within the parentheses
            block_content = import_block_match.group(1)
            # Find all quoted package paths within the block. This is simpler and
            # more robust than parsing line by line.
            found_imports = re.findall(r'"([^"]+)"', block_content)
            for imp in found_imports:
                imports.add(imp)

        # 2. Find all single-line imports: import "..."
        single_imports = re.findall(r'import\s+"([^"]+)"', content)
        for imp in single_imports:
            imports.add(imp)

        return imports

    def get_package_name_from_path(self, file_path):
        """
        Determines the Go package name from its file path.
        Uses the module prefix found in go.mod in the naming convention.
        """
        abs_file_path = os.path.abspath(file_path)

        if not abs_file_path.startswith(self.base_dir):
            # Should not happen if find_go_files is used correctly from self.base_dir
            # but as a fallback, use the directory name of the file.
            return os.path.basename(os.path.dirname(abs_file_path))

        relative_dir_path = os.path.relpath(os.path.dirname(abs_file_path), self.base_dir)

        # Normalize to forward slashes for Go package paths
        package_path_suffix = relative_dir_path.replace(os.sep, '/')

        if package_path_suffix == ".": # File is in the root of self.base_dir
            return self.module_prefix
        return f"{self.module_prefix}/{package_path_suffix}"

    def build_dependency_graph(self) -> tuple[defaultdict, defaultdict, set, defaultdict, str]:
        """
        Builds a dependency graph from Go files in the configured base directory.

        Returns:
            graph (defaultdict): A dict where keys are package names and values are sets of its dependency packages.
            in_degree (defaultdict): A dict where keys are package names and values are their in-degrees.
            all_packages (set): A set of all unique package names found (both local and external).
            package_files (defaultdict): A dict mapping package names to a list of their .go files.
        """
        graph = defaultdict(set)
        in_degree = defaultdict(int)
        package_files = defaultdict(list)
        all_packages = set()

        go_files = self.find_go_files()

        # First pass: identify all packages defined in the directory
        defined_packages = set()
        for go_file in go_files:
            pkg_name = self.get_package_name_from_path(go_file)
            defined_packages.add(pkg_name)
            package_files[pkg_name].append(go_file)
            all_packages.add(pkg_name)

        # Second pass: build graph
        for go_file in go_files:
            current_pkg_name = self.get_package_name_from_path(go_file)
            imports = self.extract_imports(go_file)

            for imp in imports:
                all_packages.add(imp)

                # Avoid self-loops in this context
                if imp != current_pkg_name:
                    # Edge from imp to current_pkg_name means imp is a dependency of current_pkg_name
                    graph[imp].add(current_pkg_name)
                    in_degree[current_pkg_name] += 1

        # Ensure all defined packages are in in_degree map, even if they have no incoming internal dependencies
        for pkg in defined_packages:
            if pkg not in in_degree:
                in_degree[pkg] = 0

        # Also ensure all imported packages are there for completeness in in_degree, initialized to 0 if not already set
        for pkg in all_packages:
            if pkg not in in_degree: # This will cover external packages not depending on anything in the project
                in_degree[pkg] = 0

        return graph, in_degree, all_packages, package_files, self.module_prefix
