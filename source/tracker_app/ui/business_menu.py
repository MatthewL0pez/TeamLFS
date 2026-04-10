from pathlib import Path
import sys

# Allow direct execution like `python3 source/tracker_app/ui/business_menu.py`.
if __package__ in {None, ""}:
    current_file = Path(__file__).resolve()
    source_root = current_file.parents[2]
    project_root = current_file.parents[3]

    for path in (project_root, source_root):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

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

from tracker_app.ui.input_helpers import ask_non_empty, ask_int, ask_float, choose_from_list, pause
from tracker_app.storage.business_storage import create_business, list_businesses, get_business_by_id, update_business
from tracker_app.service.location_service import list_city_names
from tracker_app.app.app_state import set_active_business, clear_active_business, load_state


def _print_active_business():  # display what business is currently selected
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


def _list_businesses():  # Prints all businesses stored in businesses.json
    businesses = list_businesses()

    if len(businesses) == 0:
        print("\nNo businesses found yet.")
        return

    print("\nBusinesses:")
    for b in businesses:
        print(f"- ID {b.business_id}: {b.business_name} ({b.location_city})")


def _create_business():  # Creates a new business and stores it using business_storage
    print("\nCreate Business")

    name = ask_non_empty("Business name: ")

    # Location must come from locations.json
    cities = list_city_names()
    options = cities + ["Enter Custom Location"]
    choice = choose_from_list("Choose a business location (from locations.json):", options)

    if choice is None:
        print("No locations available, cannot create business.")
        return
    
    lat, lon = None, None
    
    if choice == "Enter Custom Location":
        city = ask_non_empty("Enter City Name: ")
        lat = ask_float("Enter Latitude (e.g., 34.05): ", min_value=-90, max_value=90)
        lon = ask_float("Enter Longitude (e.g., -118.24): ", min_value=-180, max_value=180)
    else:
        city = choice

    new_biz = create_business(name, city, custom_lat=lat, custom_lon=lon)
    print(f"\nCreated business: {new_biz.business_name} (ID {new_biz.business_id}) at {new_biz.location_city}")


def _select_business():  # Lets user choose an existing business and sets it as active in app_state
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


def _logout_business():  # "Deallocate" selection = clear active business and user in app_state
    clear_active_business()
    print("\nLogged out. No business is selected now.")


def _manage_selected_business():  # Manage the currently active business
    state = load_state()
    active_id = state.get("active_business_id")

    if active_id is None:
        print("\nNo business selected. Please select a business first.")
        return

    biz = get_business_by_id(active_id)
    if biz is None:
        print("\nActive business not found.")
        return

    print(f"\nManaging: {biz.business_name} (ID {biz.business_id}) - {biz.location_city}")
    while True:
        # Reload to stay in sync with any external changes
        biz = get_business_by_id(active_id)

        print("\n--- Manage Business ---")
        print("1) Add Section")
        print("2) Add Employee")
        print("3) Assign Package to Section")
        print("4) Move Package Between Sections")
        print("5) View Sections")
        print("0) Back")

        choice = ask_int("Choose option: ", min_value=0, max_value=5)

        if choice == 1:
            section = ask_non_empty("Section name: ")
            if section in biz.sections:
                print(f"Section '{section}' already exists.")
            else:
                biz.sections[section] = []
                update_business(biz)
                print(f"Section '{section}' added.")

        elif choice == 2:
            emp_id = ask_non_empty("Employee ID: ")
            biz.employees.append(emp_id)
            update_business(biz)
            print(f"Employee ID {emp_id} added.")

        elif choice == 3:
            if not biz.sections:
                print("No sections exist yet. Add a section first.")
            else:
                section = ask_non_empty("Section name: ")
                pkg = ask_non_empty("Package ID: ")
                if section not in biz.sections:
                    print(f"Section '{section}' does not exist.")
                else:
                    biz.sections[section].append(pkg)
                    biz.total_packages += 1
                    update_business(biz)
                    print(f"Package {pkg} assigned to '{section}'.")

        elif choice == 4:
            if not biz.sections:
                print("No sections exist yet.")
            else:
                from_s = ask_non_empty("From section: ")
                to_s = ask_non_empty("To section: ")
                pkg = ask_non_empty("Package ID: ")
                if from_s in biz.sections and pkg in biz.sections[from_s]:
                    biz.sections[from_s].remove(pkg)
                    biz.sections.setdefault(to_s, []).append(pkg)
                    update_business(biz)
                    print(f"Package {pkg} moved from '{from_s}' to '{to_s}'.")
                else:
                    print("Package not found in that section.")

        elif choice == 5:
            if not biz.sections:
                print("\nNo sections defined yet.")
            else:
                print(f"\nSections for {biz.business_name}:")
                for sec, pkgs in biz.sections.items():
                    pkg_list = ", ".join(pkgs) if pkgs else "(empty)"
                    print(f"  [{sec}]  {pkg_list}")

        elif choice == 0:
            break


def run_business_menu():  # Main loop for the business menu
    while True:
        print("\n==============================")
        print(" Business Menu")
        print("==============================")
        _print_active_business()
        print("1) List businesses")
        print("2) Create business")
        print("3) Select business")
        print("4) Logout business")
        print("5) Manage selected business")
        print("0) Back")

        choice = ask_int("\nChoose an option: ", min_value=0, max_value=5)

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
        elif choice == 5:
            _manage_selected_business()
            pause()
        elif choice == 0:
            break


def main():
    run_business_menu()


if __name__ == "__main__":
    main()
