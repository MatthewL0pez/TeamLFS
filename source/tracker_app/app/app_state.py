
# app_state: what is currently selected AKA logged into what

# file stores:
# - active_business_id
# - active_user_id
#
# saves to data/app_state.json so app_state can keep going 
# even if the program closes and opens again.
#
# Logout deallocate is...
#   active_business_id = None
#   active_user_id = None

from tracker_app.storage.paths import data_file
from tracker_app.storage.json_store import read_json, write_json

STATE_FILE = "app_state.json"

def load_state():
    path = data_file(STATE_FILE)

    default_state = {
        "active_business_id": None,
        "active_user_id": None
    }

    return read_json(path, default_state)

def save_state(state_dict):
    path = data_file(STATE_FILE)
    write_json(path, state_dict)

def set_active_business(business_id):
    state = load_state()
    state["active_business_id"] = business_id

    # when you switch businesses, user selection should reset
    state["active_user_id"] = None
    save_state(state)

def clear_active_business():   # "logout" = clear current selection 
    state = load_state()
    state["active_business_id"] = None
    state["active_user_id"] = None
    save_state(state)

def set_active_user(user_id):
    state = load_state()
    state["active_user_id"] = user_id
    save_state(state)

def clear_active_user(): # "logout" = clear current selection
    state = load_state()
    state["active_user_id"] = None
    save_state(state)

# Example usage:

# from tracker_app.app.app_state import set_active_business, clear_active_business, load_state
#
# set_active_business(1)   # now business 1 is "logged in"
# print(load_state())
#
# clear_active_business()  # logout: no business selected, no location selected
# print(load_state())