from tracker_app.storage.paths import data_file
from tracker_app.storage.json_store import read_json, write_json
from tracker_app.models.package import Package

PACKAGES_FILE = "packages.json"

def _load_db():
    path = data_file(PACKAGES_FILE)
    default_db = {"next_package_id": 1, "packages": []}
    return read_json(path, default_db)

def _save_db(db):
    path = data_file(PACKAGES_FILE)
    write_json(path, db)

def get_packages_by_business(business_id):
    """Returns only packages belonging to a specific business."""
    db = _load_db()
    return [Package.from_dict(p) for p in db["packages"] if p["business_id"] == business_id]

def get_packages_by_user(user_id):
    """Finds only packages created by a specific individual."""
    db = _load_db()
    return [Package.from_dict(p) for p in db["packages"] if p.get("user_id") == user_id]

def create_package(business_id, user_id, source, destination, weight, description, cost):
    db = _load_db()
    new_id = db["next_package_id"]

    pkg = Package(
        business_id=business_id,
        user_id=user_id,
        source_city=source,
        destination_city=destination,
        weight=weight,
        description=description,
        shipping_cost=cost,
        package_id=new_id
    )

    db["packages"].append(pkg.to_dict())
    db["next_package_id"] = new_id + 1
    _save_db(db)
    return pkg