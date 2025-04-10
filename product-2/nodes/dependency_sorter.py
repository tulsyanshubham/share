import json
import re
from collections import defaultdict, deque

def simplify_dependency_name(dep):
    """Convert a class reference to its corresponding Java filename."""
    return dep.split('.')[-1] + ".java"  # Handles both fully qualified and plain class names

def build_dependency_graph(file_data):
    """Creates a graph and indegree map from file dependencies."""
    name_to_file = {f["file_name"]: f for f in file_data}
    graph = defaultdict(list)
    indegree = defaultdict(int)

    for file in file_data:
        current_file = file["file_name"]
        dependencies = file.get("internal_dependencies", [])

        for dep in dependencies:
            dep_file = simplify_dependency_name(dep)
            if dep_file in name_to_file:
                graph[dep_file].append(current_file)
                indegree[current_file] += 1

        # Ensure all files are in the indegree map
        if current_file not in indegree:
            indegree[current_file] = 0

    return graph, indegree

def topological_sort(file_data):
    """Sorts files so each file appears after its dependencies."""
    graph, indegree = build_dependency_graph(file_data)
    name_to_file = {f["file_name"]: f for f in file_data}

    # Start with files that have 0 dependencies, sorted for stability
    zero_dep_queue = deque(sorted([name for name in indegree if indegree[name] == 0]))
    sorted_file_names = []

    while zero_dep_queue:
        current = zero_dep_queue.popleft()
        sorted_file_names.append(current)

        for neighbor in sorted(graph[current]):  # Sort neighbors for consistency
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_dep_queue.append(neighbor)

    if len(sorted_file_names) != len(indegree):
        raise Exception("Cycle detected in internal dependencies!")

    return [name_to_file[name] for name in sorted_file_names]

def sort_file_analysis(input_path, output_path):
    """Reads the input file, sorts by internal dependency, and saves the result."""
    with open(input_path, 'r') as f:
        file_data = json.load(f)

    sorted_files = topological_sort(file_data)

    with open(output_path, 'w') as out:
        json.dump(sorted_files, out, indent=2)

    print(f"[SUCCESS] Files sorted and saved to {output_path}")

# Example usage
if __name__ == "__main__":
    sort_file_analysis("file_analysis.json", "file_analysis_sorted.json")