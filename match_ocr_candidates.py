import csv

# Load detected map labels
with open("ocr_candidates.csv", encoding="utf-8") as file:
    candidates = list(csv.DictReader(file))

# Load campus locations
with open("locations_checked.csv", encoding="utf-8-sig") as file:
    locations = list(csv.DictReader(
        line for line in file if line.strip()
    ))

# Load manually confirmed coordinates
try:
    with open("map_coordinates.csv", encoding="utf-8-sig") as file:

        reader = csv.DictReader(
            line for line in file if line.strip()
        )

        print("Manual CSV headers:", reader.fieldnames)

        manual = list(reader)

        manual_ids = {
            row["id"] for row in manual
        }

        print("Existing manual IDs:", manual_ids)

except FileNotFoundError:
    manual_ids = set()

matched = []

for candidate in candidates:

    code = candidate["map_code"]

    matching_locations = [
        loc for loc in locations
        if loc["map_code"].strip().upper() == code
        and loc["is_route_node"].strip().lower() == "yes"
    ]

    for loc in matching_locations:

        if "id" not in loc:
            print("PROBLEMATIC LOCATION:", repr(loc))
            continue

        status = (
            "manual_coordinate_exists"
            if loc["id"] in manual_ids
            else "needs_visual_check"
        )

        matched.append({
            "id": loc["id"],
            "name": loc["name"],
            "map_code": code,
            "x": candidate["x"],
            "y": candidate["y"],
            "confidence": candidate["confidence"],
            "status": status
        })

# Save separately
with open(
    "ocr_matched_candidates.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "id",
            "name",
            "map_code",
            "x",
            "y",
            "confidence",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(matched)

print("Matched records:", len(matched))
print("Saved: ocr_matched_candidates.csv")
