import csv
from pathlib import Path

BASE = Path(__file__).parent

def load_csv(filename):
    path = BASE / filename
    rows = []
    with path.open(encoding="utf-8-sig") as f:  # utf-8-sig fixes Windows CSV header issue
        reader = csv.DictReader(f)
        for row in reader:
            # clean header/key spaces
            clean = {str(k).strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k is not None}
            rows.append(clean)
    return rows

def main():
    locations = load_csv("locations_checked.csv")
    relationships = load_csv("relationships_checked.csv")
    sources = load_csv("sources.csv")

    print("=== Data load check ===")
    print("Locations:", len(locations))
    print("Relationships:", len(relationships))
    print("Sources:", len(sources))
    print()

    belongs = 0
    connected = 0
    for r in relationships:
        rel = r.get("relationship", "")
        if rel == "BELONGS_TO":
            belongs += 1
        elif rel == "CONNECTED_TO":
            connected += 1

    print("BELONGS_TO:", belongs)
    print("CONNECTED_TO:", connected)
    print()

    print("Main route nodes (is_route_node = yes):")
    for loc in locations:
        flag = str(loc.get("is_route_node", "")).strip().lower()
        if flag == "yes":
            loc_id = loc.get("id", "?")
            name = loc.get("name", "?")
            print(" -", loc_id, name)

if __name__ == "__main__":
    main()