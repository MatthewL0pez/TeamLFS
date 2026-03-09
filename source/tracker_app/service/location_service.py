# Location Service

# Reads data/locations.json and provides helper functions:
# - list_city_names() -> ["Long Beach", "Los Angeles", ...]
# - get_city_coords(city) -> (lat, lon) or None if not found
#
# This keeps "allowed locations" in one place.
# The UI can call list_city_names() so the user can only pick
# from the approved list (locations.json).

from tracker_app.storage.paths import data_file
from tracker_app.storage.json_store import read_json


LOCATIONS_FILENAME = "locations.json"

def load_locations():

#    EXAMPLE HOW TO IT LOADS:

#   Loads the locations.json file as a Python dictionary.
#   Shows format >>>>>
#     {
#       "locations": [
#         {"city_name": "...", "coordinates": {"latitude": 0, "longitude": 0}},
#         ...
#       ]
#     }

    path = data_file(LOCATIONS_FILENAME)
    default_value = {"locations": []}
    return read_json(path, default_value)

def list_city_names():

#   Returns a sorted list of allowed city names from locations.json.
    data = load_locations()

    city_names = []
    for loc in data.get("locations", []):
        name = loc.get("city_name", "")
        if name != "":
            city_names.append(name)

    city_names.sort()
    return city_names

def get_city_coords(city_name):

#    Returns (latitude, longitude) for a given city name.
#    If not found, returns None.

    data = load_locations()

    for loc in data.get("locations", []):
        name = loc.get("city_name", "")
        if name == city_name:
            coords = loc.get("coordinates", {})
            lat = coords.get("latitude", None)
            lon = coords.get("longitude", None)
            return (lat, lon)

    return None

# Example implementation:

# from tracker_app.service.location_service import list_city_names, get_city_coords
#
# print(list_city_names())
# print(get_city_coords("Long Beach"))