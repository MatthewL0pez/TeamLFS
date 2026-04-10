# saves/loads business profiles to JSON.
#
# It assigns the business_id like (1,2,3...)

from pathlib import Path
import sys

if __package__ in {None, ""}:
    current_file = Path(__file__).resolve()
    source_root = current_file.parents[2]
    project_root = current_file.parents[3]

    for path in (project_root, source_root):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

from services.distance_service import DistanceService
from tracker_app.models.businessprofile import BusinessProfile
from tracker_app.service.location_service import get_city_coords
from tracker_app.storage.json_store import read_json, write_json
from tracker_app.storage.paths import data_file

BUSINESSES_FILE = "businesses.json"


def _default_db():
    return {
        "next_business_id": 1,
        "businesses": [],
    }


def _normalize_db(db):
    default_db = _default_db()

    if not isinstance(db, dict):
        return default_db

    businesses = db.get("businesses", [])
    if not isinstance(businesses, list):
        businesses = []

    existing_ids = [
        business.get("business_id")
        for business in businesses
        if isinstance(business, dict) and isinstance(business.get("business_id"), int)
    ]
    next_available_id = max(existing_ids, default=0) + 1

    next_business_id = db.get("next_business_id", next_available_id)
    if not isinstance(next_business_id, int) or next_business_id < 1:
        next_business_id = next_available_id
    else:
        next_business_id = max(next_business_id, next_available_id)

    return {
        "next_business_id": next_business_id,
        "businesses": businesses,
    }


def _load_db():
    path = data_file(BUSINESSES_FILE)
    return _normalize_db(read_json(path, _default_db()))


def _save_db(db):
    path = data_file(BUSINESSES_FILE)
    write_json(path, _normalize_db(db))


def list_businesses():
    db = _load_db()
    result = []

    for business in db["businesses"]:
        if isinstance(business, dict):
            result.append(BusinessProfile.from_dict(business))

    return result


def get_business_by_id(business_id):
    db = _load_db()

    for business in db["businesses"]:
        if isinstance(business, dict) and business.get("business_id") == business_id:
            return BusinessProfile.from_dict(business)

    return None


def _coords_for_city(city_name):
    coords = get_city_coords(city_name)
    if coords is None and isinstance(city_name, str) and "," in city_name:
        coords = get_city_coords(city_name.split(",", 1)[0].strip())
    return coords


def create_business(business_name, location_city, custom_lat=None, custom_lon=None):
    db = _load_db()
    businesses = db.setdefault("businesses", [])
    new_id = db["next_business_id"]

    # Use custom coords if provided, otherwise look up from locations.json
    if custom_lat is not None and custom_lon is not None:
        latitude, longitude = custom_lat, custom_lon
    else:
        coords = _coords_for_city(location_city)
        latitude = coords[0] if coords else None
        longitude = coords[1] if coords else None

    business = BusinessProfile(
        business_name=business_name,
        location_city=location_city,
        business_id=new_id,
        latitude=latitude,
        longitude=longitude,
    )

    businesses.append(business.to_dict())
    db["next_business_id"] = new_id + 1
    _save_db(db)
    return business


def update_business(business):
    """Save changes to an existing business back to JSON."""
    db = _load_db()
    for i, b in enumerate(db["businesses"]):
        if isinstance(b, dict) and b.get("business_id") == business.business_id:
            db["businesses"][i] = business.to_dict()
            _save_db(db)
            return True
    return False


def get_distance_between(id1, id2):
    business_one = get_business_by_id(id1)
    business_two = get_business_by_id(id2)

    if business_one is None or business_two is None:
        return None

    coords_one = _resolve_business_coords(business_one)
    coords_two = _resolve_business_coords(business_two)

    if coords_one is None or coords_two is None:
        return None

    return DistanceService.haversine(coords_one, coords_two)
def get_closest_business(from_id):
    base = get_business_by_id(from_id)

    if base is None:
        return None

    closest = None
    min_dist = float('inf')

    for b in list_businesses():
        if b.business_id == from_id:
            continue

        dist = get_distance_between(from_id, b.business_id)

        if dist is not None and dist < min_dist:
            min_dist = dist
            closest = b

    return closest

def _resolve_business_coords(business):
    if business.latitude is not None and business.longitude is not None:
        return (business.latitude, business.longitude)

    coords = _coords_for_city(business.location_city)
    if coords is None:
        return None

    business.latitude, business.longitude = coords
    return coords
def get_route_order(start_id):
    businesses = list_businesses()

    if not businesses:
        return []

    visited = set()
    route = []

    current_id = start_id
    visited.add(current_id)

    route.append(get_business_by_id(current_id))

    while len(visited) < len(businesses):
        closest = None
        min_dist = float('inf')

        for b in businesses:
            if b.business_id in visited:
                continue

            dist = get_distance_between(current_id, b.business_id)

            if dist is not None and dist < min_dist:
                min_dist = dist
                closest = b

        if closest is None:
            break

        route.append(closest)
        visited.add(closest.business_id)
        current_id = closest.business_id

    return route
def get_route_distance(route):
    total = 0

    for i in range(len(route) - 1):
        dist = get_distance_between(route[i].business_id, route[i+1].business_id)
        if dist:
            total += dist

    return total
