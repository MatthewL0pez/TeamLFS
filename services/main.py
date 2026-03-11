import json
import os
import argparse
from distance_service import DistanceService
from pricing_service import PricingService


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

    print("\nEnter two city names (available cities listed below):")
    for name in sorted(locations.keys()):
        print("-", name)
    
    # Fernando: Split 'if not city1 or city2' into two separate conditional branch groups
    #
    # Also placed city1 and city2 input phases in while loops to give user another chance to
    # input an allowed city if initial input is invalid instead of just exiting program

    while True:
        if not city1:
            city1 = input("City 1 (Source): ").strip()

        try:
            city1_key = find_city_key(city1, locations)
            break

        except KeyError as e:
            print(e)
            city1 = None


    while True:
        if not city2:
            city2 = input("City 2 (Destination): ").strip()

        try:
            city2_key = find_city_key(city2, locations)
            # New condition checks if cities are the same, and prompts user to input
            # another valid city if source and destination are duplicates
            if city2_key == city1_key:
                print("Source and Destination locations cannot be the same. Try again.")
                city2 = None
                continue
            break

        except KeyError as e:
            print(e)
            city2 = None


    # Calculates distance between city1 and city2, and prints to terminal
    distance_km = DistanceService.get_distance(city1_key, city2_key, locations)
    print(f"\nDistance between {city1_key} and {city2_key}: {distance_km:.2f} km")

    # Calculates shipping cost based on distance and weight of package (using placeholder of 1 kg for now)
    placeholder_weight = 1.0
    shipping_cost = PricingService.calculate_shipping_cost(distance_km, placeholder_weight)
    
    # Creates an invoice dictionary that holds all relevant info about a package
    invoice = PricingService.generate_invoice_data(city1_key, city2_key, distance_km, placeholder_weight, shipping_cost)

    # Example of how package data can be displayed on terminal screen (taken from invoice dict)
    print("\n--- SHIPPING QUOTE ---")
    print(f"Route:        {invoice['Route']}")
    print(f"Distance:     {invoice['Distance']}")
    print(f"Weight:       {invoice['Weight']} (Placeholder)")   # Since package creation isn't implemented yet, all packages have placeholder weight of 1 kg
    print(f"Total Cost:   {invoice['Total Price']}")
    print("----------------------")

if __name__ == "__main__":
    main()
