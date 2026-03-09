# saves/loades business profiles to JSON.
#
# It assigns the business_id like (1,2,3...)

from tracker_app.storage.paths import data_file
from tracker_app.storage.json_store import read_json, write_json
from tracker_app.models.businessprofile import BusinessProfile

BUSINESSES_FILE = "businesses.json"

def _load_db():
    path = data_file(BUSINESSES_FILE)     # Loads the "business database" from JSON.
                                          # If file doesn't exist, it starts empty.
    default_db_directory = {            ## db means data base 
        "next_business_id": 1,
        "businesses": []
    }

    return read_json(path, default_db_directory)

def _save_db(db): # save the database directory back to the JSON file 

    path = data_file(BUSINESSES_FILE)
    write_json(path, db)

def list_businesses(): # returns a list of BusinessProfile objects 
    db = _load_db()
    result = []
    for b in db.get("businesses", []):
        result.append(BusinessProfile.from_dict(b))

    return result

def get_business_by_id(business_id): # Finds a business by ID 
    db = _load_db()

    for b in db.get("businesses", []):
        if b.get("business_id") == business_id:
            return BusinessProfile.from_dict(b)

    return None

def create_business(business_name, location_city): # Creates a new business and assigns the next ID
    db = _load_db()

    new_id = db.get("next_business_id", 1)

    biz = BusinessProfile(
        business_name=business_name,
        location_city=location_city,
        business_id=new_id
    )

    db["businesses"].append(biz.to_dict())
    db["next_business_id"] = new_id + 1

    _save_db(db)
    return biz

# Example use:

# from tracker_app.storage.business_storage import create_business, list_businesses
# b = create_business("Test Biz", "loaction city")
# print(b.to_dict())
# print([x.to_dict() for x in list_businesses()])