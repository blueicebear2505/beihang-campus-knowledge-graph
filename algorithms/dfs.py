import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from graph_model import load_csv, build_graph

def dfs(graph, start_id):
    """
    Depth-First Search.
    Goes deep along one path, then backtracks.
    """
    if start_id not in graph:
        return [], {}

    order = []
    parent = {start_id: None}
    stack = [start_id]
    visited = set()

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        order.append(current)

        neighbors = list(graph[current])
        for neighbor, _distance in reversed(neighbors):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                stack.append(neighbor)

    return order, parent

def reconstruct_path(parent, start_id, goal_id):
    if goal_id not in parent and goal_id != start_id:
        return None

    path = []
    cur = goal_id
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()

    if not path or path[0] != start_id:
        return None
    return path

def main():
    locations = load_csv("locations_checked.csv")
    relationships = load_csv("relationships_checked.csv")
    nodes, graph = build_graph(locations, relationships)

    start = "L19"  # South Gate
    goal = "L04"   # Student Dormitory

    order, parent = dfs(graph, start)

    print("=== DFS from South Gate (L19) ===")
    for i, place_id in enumerate(order):
        name = nodes.get(place_id, {}).get("name", "?")
        print(f"  {i}. {place_id} ({name})")

    path = reconstruct_path(parent, start, goal)
    print()
    print("DFS path L19 -> L04:")
    if path is None:
        print("  No path found")
    else:
        nice = [f"{p}({nodes.get(p, {}).get('name', '?')})" for p in path]
        print("  " + " -> ".join(nice))
        print("  hops:", len(path) - 1)

if __name__ == "__main__":
    main()