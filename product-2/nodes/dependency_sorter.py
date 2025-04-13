from collections import defaultdict, deque
import os

def simplify_dependency_name(dep):
    return dep.split('.')[-1]

def strip_extension(filename):
    return os.path.splitext(filename)[0]

def build_dependency_graph(file_data):
    name_to_file = {strip_extension(f["file_name"]): f for f in file_data}
    graph = defaultdict(list)
    indegree = defaultdict(int)

    for file in file_data:
        current_file = strip_extension(file["file_name"])
        dependencies = file.get("internal_dependencies", [])

        for dep in dependencies:
            dep_file = simplify_dependency_name(dep)
            if dep_file in name_to_file:
                graph[dep_file].append(current_file)
                indegree[current_file] += 1

        if current_file not in indegree:
            indegree[current_file] = 0

    return graph, indegree

def detect_cycles(graph, indegree):
    queue = deque([node for node in indegree if indegree[node] == 0])
    visited = set()

    while queue:
        node = queue.popleft()
        visited.add(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    cycle_nodes = [node for node in indegree if node not in visited]
    return cycle_nodes

async def topological_sort(file_data, fail_on_cycle=False):
    print("[INFO] Building dependency graph...")
    graph, indegree = build_dependency_graph(file_data)
    original_indegree = indegree.copy()
    
    name_to_file = {strip_extension(f["file_name"]): f for f in file_data}

    zero_dep_queue = deque(sorted([name for name in indegree if indegree[name] == 0]))
    sorted_file_names = []

    while zero_dep_queue:
        current = zero_dep_queue.popleft()
        sorted_file_names.append(current)

        for neighbor in sorted(graph[current]):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                zero_dep_queue.append(neighbor)

    if len(sorted_file_names) != len(indegree):
        cycle_nodes = detect_cycles(graph, original_indegree)
        print(f"[ERROR] Cycle detected! Involved files: {cycle_nodes}")
        if fail_on_cycle:
            raise Exception(f"Cycle detected in internal dependencies: {cycle_nodes}")
        else:
            print("[WARN] Continuing with partial sort. Cyclic files will be appended unsorted.")
            for cycle_file in cycle_nodes:
                if cycle_file not in sorted_file_names:
                    sorted_file_names.append(cycle_file)

    print(f"[INFO] Final sorted file count: {len(sorted_file_names)}")
    return [name_to_file[name] for name in sorted_file_names]