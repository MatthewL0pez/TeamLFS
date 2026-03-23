# Business Menu UI

# This file is a simple text menu for business profiles
# uses:
# - business_storage.py  (to store/list businesses)
# - location_service.py  (to pick allowed location from locations.json)
# - app_state.py          (to select/logout business)
#
# Gives the way to be able to... 
# 1) Create a business
# 2) List businesses
# 3) Select a business "login"
# 4) Logout business "deallocate selection"

from tracker_app.ui.input_helpers import ask_non_empty, ask_int, choose_from_list, pause
from tracker_app.storage.business_storage import create_business, list_businesses, get_business_by_id
from tracker_app.service.location_service import list_city_names
from tracker_app.app.app_state import set_active_business, clear_active_business, load_state

def _print_active_business(): # display what business is currently selected
    state = load_state()
    active_id = state.get("active_business_id")

    if active_id is None:
        print("Active Business: (none)")
        return

    biz = get_business_by_id(active_id)
    if biz is None:
        print("Active Business: (missing / deleted?)")
        return

    print(f"Active Business: {biz.business_name} (ID {biz.business_id}) - {biz.location_city}")

def _list_businesses(): # Prints all businesses stored in businesses.json
    businesses = list_businesses()

    if len(businesses) == 0:
        print("\nNo businesses found yet.")
        return

    print("\nBusinesses:")
    for b in businesses:
        print(f"- ID {b.business_id}: {b.business_name} ({b.location_city})")

def _create_business(): # Creates a new business and stores it using business_storage
    print("\nCreate Business")

    name = ask_non_empty("Business name: ")

    # Location must come from locations.json
    cities = list_city_names()
    city = choose_from_list("Choose a business location (from locations.json):", cities)

    if city is None:
        print("No locations available, cannot create business.")
        return

    new_biz = create_business(name, city)
    print(f"\nCreated business: {new_biz.business_name} (ID {new_biz.business_id}) at {new_biz.location_city}")

def _select_business(): # Lets user choose an existing business and sets it as active in app_state
    businesses = list_businesses()
    if len(businesses) == 0:
        print("\nNo businesses to select. Create one first.")
        return

    _list_businesses()
    picked_id = ask_int("\nEnter business ID to select: ", min_value=1)

    biz = get_business_by_id(picked_id)
    if biz is None:
        print("That business ID was not found.")
        return

    set_active_business(biz.business_id)
    print(f"\nSelected business: {biz.business_name} (ID {biz.business_id})")

def _logout_business(): # "Deallocate" selection = clear active business and user in app_state
    clear_active_business()
    print("\nLogged out. No business is selected now.")

def run_business_menu(): # Main loop for the business menu
    while True:
        print("\n==============================")
        print(" Business Menu")
        print("==============================")
        _print_active_business()
        print("\n1) List businesses")
        print("2) Create business")
        print("3) Select business")
        print("4) Logout business")
        print("0) Back")

        choice = ask_int("\nChoose an option: ", min_value=0, max_value=4)

        if choice == 1:
            _list_businesses()
            pause()
        elif choice == 2:
            _create_business()
            pause()
        elif choice == 3:
            _select_business()
            pause()
        elif choice == 4:
            _logout_business()
            pause()
        elif choice == 0:
            break

# Example usage

# from tracker_app.ui.business_menu import run_business_menu
# run_business_menu()