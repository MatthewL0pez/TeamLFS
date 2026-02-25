import json
import os
import argparse
from distance_service import DistanceService


# Load locations from JSON file
def load_locations():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "locations.json")
    with open(file_path, "r") as file:
        data = json.load(file)
        return {
            loc["city_name"]: (loc["coordinates"]["latitude"], loc["coordinates"]["longitude"])
            for loc in data["locations"]
        }


def find_city_key(name, locations):
    if name in locations:
        return name
    # case-insensitive exact
    lower_map = {k.lower(): k for k in locations}
    if name.lower() in lower_map:
        return lower_map[name.lower()]
    # substring match
    for k in locations:
        if name.lower() in k.lower():
            return k
    raise KeyError(f"City '{name}' not found")


def main():
    parser = argparse.ArgumentParser(description="Compute distance between two cities from the locations file")
    parser.add_argument("city1", nargs="?", help="First city name")
    parser.add_argument("city2", nargs="?", help="Second city name")
    parser.add_argument("--list", action="store_true", help="List available cities")
    args = parser.parse_args()

    locations = load_locations()

    if args.list:
        print("Available cities:")
        for name in sorted(locations.keys()):
            print("-", name)
        return

    city1 = args.city1
    city2 = args.city2

    if not city1 or not city2:
        print("Enter two city names (available cities listed below):")
        for name in sorted(locations.keys()):
            print("-", name)
        if not city1:
            city1 = input("City 1: ").strip()
        if not city2:
            city2 = input("City 2: ").strip()

    try:
        city1_key = find_city_key(city1, locations)
        city2_key = find_city_key(city2, locations)
    except KeyError as e:
        print(e)
        return

    distance_km = DistanceService.get_distance(city1_key, city2_key, locations)
    print(f"Distance between {city1_key} and {city2_key}: {distance_km:.2f} km")


if __name__ == "__main__":
    main()