import csv
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent

def load_csv(filename):
    path = BASE / filename
    rows = []
    with path.open(encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean = {
                str(k).strip(): (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
                if k is not None
            }
            rows.append(clean)
    return rows


def build_graph(locations, relationships):

    nodes = {}

    # Add physical locations
    for loc in locations:
        loc_id = loc.get("id")

        if loc_id:
            nodes[loc_id] = loc

    graph = defaultdict(list)

    # Add category nodes from BELONGS_TO relationships
    for rel in relationships:

        if rel.get("relationship") == "BELONGS_TO":

            category = rel.get("target_id")

            if category and category not in nodes:
                nodes[category] = {
                    "id": category,
                    "name": category,
                    "entity_type": "Category",
                    "category": category
                }

    # Add all relationships
    for rel in relationships:

        relationship = rel.get("relationship")
        src = rel.get("subject_id")
        dst = rel.get("target_id")

        if not src or not dst:
            continue

        if src not in nodes or dst not in nodes:
            continue

        dist_raw = rel.get("distance_m", "").strip()

        try:
            dist = float(dist_raw) if dist_raw else None
        except ValueError:
            dist = None

        graph[src].append((dst, dist, relationship))
        graph[dst].append((src, dist, relationship))

    return nodes, graph

def main():
    locations = load_csv("locations_checked.csv")
    relationships = load_csv("relationships_checked.csv")

    nodes, graph = build_graph(locations, relationships)

    print("=== Graph build check ===")
    print("Nodes:", len(nodes))
    print("Places with at least one connection:", len(graph))
    print()

    print("Connections (adjacency list):")
    for place_id in sorted(graph.keys()):
        name = nodes.get(place_id, {}).get("name", "?")
        neighbors = graph[place_id]
        print(f"{place_id} ({name}):")
        for neighbor_id, dist, relationship in neighbors:
            neighbor_name = nodes.get(neighbor_id, {}).get("name", "?")
            print(
                f"  -> {neighbor_id} ({neighbor_name}), "
                f"relationship={relationship}, distance={dist}"
            )
            
if __name__ == "__main__":
    main()