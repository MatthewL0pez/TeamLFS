from tracker_app.ui.input_helpers import ask_non_empty, ask_int, ask_float, choose_from_list, pause
from tracker_app.storage.package_storage import create_package, get_packages_by_business, get_packages_by_user
from tracker_app.storage.business_storage import get_business_by_id
from tracker_app.storage.user_storage import get_user_by_id
from tracker_app.service.location_service import list_city_names, get_location_dict_for_math
from tracker_app.app.app_state import load_state
from services.distance_service import DistanceService
from services.pricing_service import PricingService

def _register_package():
    state = load_state()
    biz_id = state.get("active_business_id")
    user_id = state.get("active_user_id")

    # Safety check: Ensure a user is selected
    if user_id is None:
        print("\nERROR: A specific user must be selected to register a package.")
        pause()
        return

    # Ensure user has valid billing info
    user = get_user_by_id(user_id)
    if not user.billing_info:
        print("\nERROR: No billing info found for this user. Update profile first.")
        pause()
        return
    
    biz = get_business_by_id(biz_id)
    print(f"\nRegistering Package for {biz.business_name}")
    
    # 1. Destination Selection
    cities = list_city_names()
    dest = choose_from_list(f"Shipping from {biz.location_city}. Choose destination:", cities)
    
    if dest is None: return

    # 2. Package Details
    desc = ask_non_empty("Package description: ")
    weight = ask_float("Package weight (kg): ", min_value=0.1)

    # 3. Calculation Logic
    locations = get_location_dict_for_math()
    dist = DistanceService.get_distance(biz.location_city, dest, locations)
    cost = PricingService.calculate_shipping_cost(dist, weight)

    print(f"\nLOGISTICS QUOTE:")
    print(f"Distance: {dist:.2f} km")
    print(f"Total Shipping Cost: ${cost:.2f}")
    confirm = ask_non_empty("Confirm registration? (y/n): ").lower()

    if confirm == 'y':
        new_pkg = create_package(biz_id, user_id, biz.location_city, dest, weight, desc, cost)
        print(f"Success! Tracking ID: {new_pkg.package_id}")

def _list_biz_packages():
    state = load_state()
    biz_id = state.get("active_business_id")

    pkgs = get_packages_by_business(biz_id)
    if not pkgs:
        print("\nNo packages found for this business.")
        return
    
    print("\nYour Packages:")
    for p in pkgs:
        print(f"ID {p.package_id}: {p.description} -> {p.destination_city} | Status: {p.current_location}")

def _list_user_packages():
    state = load_state()
    user_id = state.get("active_user_id")

    pkgs = get_packages_by_user(user_id)
    if not pkgs:
        print("\nNo packages found for this user.")
        return
    
    print("\nYour Packages:")
    for p in pkgs:
        print(f"ID {p.package_id}: {p.description} -> {p.destination_city} | Status: {p.current_location}")
    
def _print_active_info():
    biz = _get_active_business()
    user = _get_active_user()

    print(f"Active Business: {biz.business_name} (ID {biz.business_id})")
    print(f"Active User:     {user.first_name} {user.last_name} (ID {user.user_id})")

def _get_active_business():
    """Returns the BusinessProfile object for the currently active ID, or None."""
    state = load_state()
    biz_id = state.get("active_business_id")
    return get_business_by_id(biz_id) if biz_id else None

def _get_active_user():
    """Returns the UserProfile object for the currently active ID, or None."""
    state = load_state()
    user_id = state.get("active_user_id")
    return get_user_by_id(user_id) if user_id else None

def run_package_menu():
    while True:
        biz = _get_active_business()
        user = _get_active_user()

        if biz is None or user is None:
            print("\nERROR: You must select both a Business AND a User first.")
            pause()
            return 

        print("\n==============================")
        print(" Package Management Menu")
        print("==============================")
        _print_active_info()

        print("\n1) View All Business Packages")
        print("2) View My Packages")
        print("3) Register New Package")
        print("0) Back")

        choice = ask_int("\nChoice: ", min_value=0, max_value=3)
        if choice == 1:
            _list_biz_packages()
            pause()
        elif choice == 2:
            _list_user_packages()
            pause()
        elif choice == 3:
            _register_package()
            pause()
        elif choice == 0:
            break