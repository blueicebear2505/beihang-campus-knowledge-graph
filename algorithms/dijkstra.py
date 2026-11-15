import sys
from pathlib import Path
import heapq

sys.path.append(str(Path(__file__).resolve().parents[1]))

from graph_model import load_csv, build_graph

def dijkstra(graph, start_id):
    """
    Dijkstra shortest path.
    Uses edge weights (distance_m).
    Returns:
      dist: shortest distance from start to each node
      parent: previous node on the shortest path
    """
    if start_id not in graph:
        return {}, {}

    dist = {start_id: 0.0}
    parent = {start_id: None}
    heap = [(0.0, start_id)]  # (distance, node)

    while heap:
        d, current = heapq.heappop(heap)

        # skip outdated heap entries
        if d > dist.get(current, float("inf")):
            continue

        for neighbor, weight in graph[current]:
            if weight is None:
                continue  # skip edges without distance

            new_dist = d + float(weight)
            if new_dist < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    return dist, parent

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

    dist, parent = dijkstra(graph, start)

    print("=== Dijkstra from South Gate (L19) ===")
    print("Shortest distances (metres):")
    for place_id in sorted(dist.keys()):
        name = nodes.get(place_id, {}).get("name", "?")
        print(f"  {place_id} ({name}): {dist[place_id]:.1f} m")

    path = reconstruct_path(parent, start, goal)
    print()
    print("Shortest path L19 -> L04:")
    if path is None:
        print("  No path found")
    else:
        nice = [f"{p}({nodes.get(p, {}).get('name', '?')})" for p in path]
        print("  " + " -> ".join(nice))
        print(f"  total distance: {dist.get(goal, float('inf')):.1f} m")

if __name__ == "__main__":
    main()