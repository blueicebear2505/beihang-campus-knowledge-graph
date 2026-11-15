from collections import deque
import sys
from pathlib import Path

# allow importing graph_model from parent folder
sys.path.append(str(Path(__file__).resolve().parents[1]))

from graph_model import load_csv, build_graph

def bfs(graph, start_id):
    """
    Breadth-First Search.
    Explores the graph level by level.
    """
    if start_id not in graph:
        return [], {}, {}

    order = []
    dist_steps = {start_id: 0}
    parent = {start_id: None}
    queue = deque([start_id])
    visited = {start_id}

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor, _distance in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                dist_steps[neighbor] = dist_steps[current] + 1
                parent[neighbor] = current
                queue.append(neighbor)

    return order, dist_steps, parent

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

    order, dist_steps, parent = bfs(graph, start)

    print("=== BFS from South Gate (L19) ===")
    for i, place_id in enumerate(order):
        name = nodes.get(place_id, {}).get("name", "?")
        hops = dist_steps.get(place_id, "?")
        print(f"  {i}. {place_id} ({name})  hops={hops}")

    path = reconstruct_path(parent, start, goal)
    print()
    print("Path L19 -> L04:")
    if path is None:
        print("  No path found")
    else:
        nice = [f"{p}({nodes.get(p, {}).get('name', '?')})" for p in path]
        print("  " + " -> ".join(nice))
        print("  hops:", len(path) - 1)

if __name__ == "__main__":
    main()