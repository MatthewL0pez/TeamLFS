
# saves/loades user profiles to JSON.
#
# It assigns the user_id like (1,2,3...) 


from tracker_app.storage.paths import data_file
from tracker_app.storage.json_store import read_json, write_json
from tracker_app.models.userprofile import UserProfile

USERS_FILE = "users.json"

def _load_db():                     ## note: goto business_storage for 
    path = data_file(USERS_FILE)    ##       explaination of funcs not 
                                    ##       commented on

    default_db = {
        "next_user_id": 1,
        "users": []
    }

    return read_json(path, default_db)


def _save_db(db):
    path = data_file(USERS_FILE)
    write_json(path, db)


def list_users():
    db = _load_db()

    result = []
    for u in db.get("users", []):
        result.append(UserProfile.from_dict(u))

    return result

def list_users_for_business(business_id):  # Returns only users that belong a  business_id
    all_users = list_users()

    result = []
    for u in all_users:
        if u.belongs_to_business(business_id):
            result.append(u)

    return result


def get_user_by_id(user_id):
    db = _load_db()

    for u in db.get("users", []):
        if u.get("user_id") == user_id:
            return UserProfile.from_dict(u)

    return None

def create_user(first_name, last_name, email, phone, billing_info, business_id):
    db = _load_db()

    new_id = db.get("next_user_id", 1)

    user = UserProfile(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        billing_info=billing_info,
        business_id=business_id,
        user_id=new_id
    )

    db["users"].append(user.to_dict())
    db["next_user_id"] = new_id + 1

    _save_db(db)
    return user


# Example use:

# from tracker_app.storage.user_storage import create_user, list_users_for_business
# u = create_user("Matt","Lopez","m@email.com","555","VISA 1111", business_id=1)
# print(u.to_dict())
# print([x.to_dict() for x in list_users_for_business(1)])