from tracker_app.ui.input_helpers import ask_non_empty, ask_int, ask_float, choose_from_list, pause
from tracker_app.storage.package_storage import create_package, get_packages_by_business, get_packages_by_user
from tracker_app.storage.business_storage import get_business_by_id
from tracker_app.storage.user_storage import get_user_by_id
from tracker_app.service.location_service import list_city_names, get_location_dict_for_math
from tracker_app.app.app_state import load_state
from services.distance_service import DistanceService
from services.pricing_service import PricingService
from services.finance_service import FinanceService

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
    
    # 1. Destination Selection with Custom Option
    cities = list_city_names()
    options = cities + ["ENTER CUSTOM COORDINATES"]
    choice = choose_from_list(f"Shipping from {biz.location_city}. Choose destination:", options)
    
    if choice is None: return

    dest_lat, dest_lon = None, None
    
    if choice == "ENTER CUSTOM COORDINATES":
        dest_city = ask_non_empty("Enter destination city name/address: ")
        dest_lat = ask_float("Enter Destination Latitude: ", min_value=-90, max_value=90)
        dest_lon = ask_float("Enter Destination Longitude: ", min_value=-180, max_value=180)
        dest_coords = (dest_lat, dest_lon)
    else:
        dest_city = choice
        locations = get_location_dict_for_math()
        dest_coords = locations.get(dest_city)
        dest_lat, dest_lon = dest_coords

    # 2. Package Details
    desc = ask_non_empty("Package description: ")
    weight = ask_float("Package weight (kg): ", min_value=0.1)

    # 3. UPDATED CALCULATION LOGIC
    # Get coordinates for the source from the BUSINESS object itself
    # This uses the latitude/longitude saved in businesses.json
    source_coords = (biz.latitude, biz.longitude)

    # Safety check: if business has no coords, try a fallback to the city name
    if source_coords[0] is None or source_coords[1] is None:
        locations = get_location_dict_for_math()
        source_coords = locations.get(biz.location_city)

    # Use the haversine method directly since we have both pairs of coordinates
    if source_coords and dest_coords:
        dist = DistanceService.haversine(source_coords, dest_coords)
        cost = PricingService.calculate_shipping_cost(dist, weight)
    else:
        print("\nERROR: Could not resolve coordinates for this route.")
        pause()
        return
    
    print(f"\n  ┌─────────────────────────────┐")
    print(f"  │      LOGISTICS QUOTE        │")
    print(f"  └─────────────────────────────┘")
    print(f"  Route    : {biz.location_city} → {dest_city}")
    print(f"  Distance : {dist:.2f} km")
    print(f"  Weight   : {weight:.2f} kg")
    print(f"  Cost     : ${cost:.2f}")
    confirm = ask_non_empty("\nConfirm registration? (y/n): ").lower()

    if confirm == 'y':
        new_pkg = create_package(biz_id, user_id, biz.location_city, dest_city, weight, desc, cost, dest_lat, dest_lon, dist)
        print(f"\n  Package registered! Tracking ID: #{new_pkg.package_id}")

def _list_biz_packages():
    state = load_state()
    biz_id = state.get("active_business_id")

    pkgs = get_packages_by_business(biz_id)
    if not pkgs:
        print("\nNo packages found for this business.")
        return
    
    print(f"\n{'ID':<5} {'Description':<20} {'Route':<30} {'Weight':>7} {'Cost':>9} {'Status'}")
    print("-" * 80)
    for p in pkgs:
        route = f"{p.source_city} → {p.destination_city}"
        print(f"{p.package_id:<5} {p.description:<20} {route:<30} {p.weight:>6.1f}kg ${p.shipping_cost:>7.2f}  {p.current_location}")

def _list_user_packages():
    state = load_state()
    user_id = state.get("active_user_id")

    pkgs = get_packages_by_user(user_id)
    if not pkgs:
        print("\nNo packages found for this user.")
        return

    print(f"\n{'ID':<5} {'Description':<20} {'Route':<30} {'Weight':>7} {'Cost':>9} {'Status'}")
    print("-" * 80)
    for p in pkgs:
        route = f"{p.source_city} → {p.destination_city}"
        print(f"{p.package_id:<5} {p.description:<20} {route:<30} {p.weight:>6.1f}kg ${p.shipping_cost:>7.2f}  {p.current_location}")

def _view_financial_report():
    state = load_state()
    biz_id = state.get("active_business_id")
    user_id = state.get("active_user_id")

    biz = _get_active_business()
    user = _get_active_user()

    biz_pkgs = get_packages_by_business(biz_id)
    user_pkgs = get_packages_by_user(user_id)
    
    biz_report = FinanceService.calculate_business_report(biz_pkgs)
    user_report = FinanceService.calculate_user_expenditures(user_pkgs)

    print(f"\n  ┌─────────────────────────────┐")
    print(f"  │      FINANCIAL REPORT       │")
    print(f"  └─────────────────────────────┘")
    
    if biz_report:
        print(f"\n [BUSINESS: {biz.business_name} (ID {biz.business_id})]")
        print(f"  Packages Processed  : {biz_report['package_count']}")
        print(f"  Total Volume        : {biz_report['total_weight']:.2f} kg")
        print(f"  Gross Revenue       : ${biz_report['revenue']:.2f}")
        print(f"  Operating Costs     : -${biz_report['expenses']:.2f}")
        print(f"  -------------------------------")
        print(f"  NET PROFIT          : ${biz_report['profit']:.2f}")
        print(f"  Profit Margin       : {biz_report['margin']:.1f}%")
        print(f"  Avg Package Price   : ${biz_report['avg_pkg_price']:.2f}")
        print("\n" + "="*42)
    else:
        print(f"\n [BUSINESS: {biz.business_name} (ID {biz.business_id})]")
        print("  No financial data available yet.")
        print("\n" + "="*42)
    
    if user_report:
        print(f"\n [USER: {user.first_name} {user.last_name} (ID {user.user_id})]")
        print(f"  Lifetime Spent      : ${user_report['total_spent']:.2f}")
        print(f"  Packages Registered : {user_report['package_count']}")
        print(f"  Avg Package Cost    : ${user_report['avg_cost_per_pkg']:.2f}")

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
        print("4) View Financial Report")
        print("0) Back")

        choice = ask_int("\nChoice: ", min_value=0, max_value=4)
        if choice == 1:
            _list_biz_packages()
            pause()
        elif choice == 2:
            _list_user_packages()
            pause()
        elif choice == 3:
            _register_package()
            pause()
        elif choice == 4:
            _view_financial_report()
            pause()
        elif choice == 0:
            break