from pathlib import Path
import sys

if __package__ in {None, ""}: # direct execution from this file
    current_file = Path(__file__).resolve()
   
    # works whether the is inside source/tracker_app/ui/ or elsewhere temporarily
    possible_roots = [current_file.parent, *current_file.parents]
    for root in possible_roots:
        source_root = root / "source"
        project_pkg = source_root / "tracker_app"
        if project_pkg.exists():
            for path in (root, source_root):
                path_str = str(path)
                if path_str not in sys.path:
                    sys.path.insert(0, path_str)
            break

from tracker_app.app.app_state import load_state, set_active_business, set_active_user
from tracker_app.service.location_service import list_city_names, get_location_dict_for_math
from tracker_app.storage.business_storage import (
    create_business,
    list_businesses,
    get_business_by_id,
    update_business,
)
from tracker_app.storage.user_storage import (
    create_user,
    list_users_for_business,
    get_user_by_id,
)
from tracker_app.storage.package_storage import (
    create_package,
    get_packages_by_business,
    get_packages_by_user,
)
from services.distance_service import DistanceService
from services.pricing_service import PricingService


# print helpers

def print_line():
    print("=" * 72)


def print_title(title):
    print()
    print_line()
    print(title)
    print_line()

# find existing demo data helpers

def find_business_by_name(business_name):
    for business in list_businesses():
        if business.business_name == business_name:
            return business
    return None


def find_user_for_business(business_id, email):
    for user in list_users_for_business(business_id):
        if user.email == email:
            return user
    return None


def find_package_for_business(business_id, description):
    for package in get_packages_by_business(business_id):
        if package.description == description:
            return package
    return None

# step 1 - location display

def show_allowed_locations():
    cities = list_city_names()

    print_title("STEP 1 - ALLOWED SHIPPING LOCATIONS")
    print(f"This is the current list the UI can choose from. Total cities: {len(cities)}")
    for city in cities:
        print(f"- {city}")

    return cities

# step 2 - business creation

def setup_demo_business(cities):
    demo_business_name = "Presentation Demo Shipping"
    demo_city = "Los Angeles"

    if demo_city not in cities and cities:
        demo_city = cities[0]

    print_title("STEP 2 - CREATE OR REUSE BUSINESS PROFILE")
    print("This simulates the business menu create/select flow.")
    print(f"Business name entered : {demo_business_name}")
    print(f"Business city chosen  : {demo_city}")

    business = find_business_by_name(demo_business_name)

    if business is None:
        business = create_business(demo_business_name, demo_city)
        print("Result: created new business profile.")
    else:
        print("Result: business already existed, so the demo reused it.")

    set_active_business(business.business_id)

    print(f"Business ID           : {business.business_id}")
    print(f"Stored location       : {business.location_city}")
    print(f"Active business set   : {business.business_id}")

    return get_business_by_id(business.business_id)

# step 3 - user creation under business

def setup_demo_user(business):
    demo_first_name = "Demo"
    demo_last_name = "User"
    demo_email = "presentation.demo@email.com"
    demo_phone = "555-0101"
    demo_billing = "VISA DEMO 1111"

    print_title("STEP 3 - CREATE OR REUSE USER PROFILE UNDER ACTIVE BUSINESS")
    print("This shows the rule that a user is created under a selected business.")
    print(f"Selected business     : {business.business_name} (ID {business.business_id})")
    print(f"First name entered    : {demo_first_name}")
    print(f"Last name entered     : {demo_last_name}")
    print(f"Email entered         : {demo_email}")
    print(f"Phone entered         : {demo_phone}")
    print(f"Billing entered       : {demo_billing}")

    user = find_user_for_business(business.business_id, demo_email)

    if user is None:
        user = create_user(
            demo_first_name,
            demo_last_name,
            demo_email,
            demo_phone,
            demo_billing,
            business.business_id,
        )
        print("Result: created new user profile under the active business.")
    else:
        print("Result: user already existed under this business, so the demo reused it.")

    set_active_user(user.user_id)

    print(f"User ID               : {user.user_id}")
    print(f"Linked business ID    : {user.business_id}")
    print(f"Active user set       : {user.user_id}")

    return get_user_by_id(user.user_id)

# step 4 - package creation

def setup_demo_package(business, user, cities):
    description = "Presentation Sample Package"
    weight_kg = 4.5
    destination_city = "Tokyo"

    print_title("STEP 4 - REGISTER OR REUSE PACKAGE")
    print("This shows package registration using the active business and active user.")

    existing_package = find_package_for_business(business.business_id, description)
    if existing_package is not None:
        print("Result: package already existed, so the demo reused it.")
        print(f"Package ID            : {existing_package.package_id}")
        print(f"Route                 : {existing_package.source_city} -> {existing_package.destination_city}")
        print(f"Weight                : {existing_package.weight} kg")
        print(f"Cost                  : ${existing_package.shipping_cost:.2f}")
        return existing_package

    if destination_city not in cities:
        for city in cities:
            if city != business.location_city:
                destination_city = city
                break

    locations = get_location_dict_for_math()
    distance_km = DistanceService.get_distance(business.location_city, destination_city, locations)
    shipping_cost = PricingService.calculate_shipping_cost(distance_km, weight_kg)

    print(f"Source city           : {business.location_city}")
    print(f"Destination city      : {destination_city}")
    print(f"Package description   : {description}")
    print(f"Package weight        : {weight_kg} kg")
    print(f"Calculated distance   : {distance_km:.2f} km")
    print(f"Calculated cost       : ${shipping_cost:.2f}")

    package = create_package(
        business.business_id,
        user.user_id,
        business.location_city,
        destination_city,
        weight_kg,
        description,
        shipping_cost,
    )

    print("Result: package registered and stored.")
    print(f"Package ID            : {package.package_id}")
    print(f"Current status        : {package.current_location}")

    return package

# step 5 - business management demo

def setup_demo_business_management(business, user, package):
    print_title("STEP 5 - BUSINESS MANAGEMENT FEATURES")
    print("This part shows the newer UI additions for sections, employees, and package movement.")

    refreshed_business = get_business_by_id(business.business_id)
    if refreshed_business is None:
        print("Could not reload business data.")
        return None

    if "Receiving" not in refreshed_business.sections:
        refreshed_business.sections["Receiving"] = []
        print("Added section         : Receiving")
    else:
        print("Section already exists: Receiving")

    if "Shipping" not in refreshed_business.sections:
        refreshed_business.sections["Shipping"] = []
        print("Added section         : Shipping")
    else:
        print("Section already exists: Shipping")

    if user.user_id not in refreshed_business.employees:
        refreshed_business.employees.append(user.user_id)
        print(f"Added employee ID     : {user.user_id}")
    else:
        print(f"Employee already added: {user.user_id}")

    pkg_id_text = str(package.package_id)

    in_receiving = pkg_id_text in refreshed_business.sections.get("Receiving", [])
    in_shipping = pkg_id_text in refreshed_business.sections.get("Shipping", [])

    if not in_receiving and not in_shipping:
        refreshed_business.sections.setdefault("Receiving", []).append(pkg_id_text)
        refreshed_business.total_packages += 1
        print(f"Assigned package      : {pkg_id_text} -> Receiving")
    elif in_receiving:
        print(f"Package already in    : Receiving")
    elif in_shipping:
        print(f"Package already in    : Shipping")

    if pkg_id_text in refreshed_business.sections.get("Receiving", []):
        refreshed_business.sections["Receiving"].remove(pkg_id_text)
        refreshed_business.sections.setdefault("Shipping", []).append(pkg_id_text)
        print(f"Moved package         : {pkg_id_text} Receiving -> Shipping")
    else:
        print(f"Move skipped          : package already not in Receiving")

    update_business(refreshed_business)

    saved_business = get_business_by_id(business.business_id)
    print()
    print("Saved business section view:")
    for section_name, packages in saved_business.sections.items():
        shown_packages = ", ".join(packages) if packages else "(empty)"
        print(f"- {section_name}: {shown_packages}")

    print(f"Employees stored      : {saved_business.employees}")
    print(f"Total packages count  : {saved_business.total_packages}")

    return saved_business

# step 6 - data readback summary

def show_final_summary(business, user):
    business_packages = get_packages_by_business(business.business_id)
    user_packages = get_packages_by_user(user.user_id)
    state = load_state()

    print_title("FINAL DEMO SUMMARY")
    print(f"Active business ID    : {state.get('active_business_id')}")
    print(f"Active user ID        : {state.get('active_user_id')}")
    print(f"Business package count: {len(business_packages)}")
    print(f"User package count    : {len(user_packages)}")

    print()
    print("Saved business packages:")
    if not business_packages:
        print("- none")
    else:
        for package in business_packages:
            print(
                f"- Package {package.package_id}: {package.description} | "
                f"{package.source_city} -> {package.destination_city} | "
                f"{package.weight} kg | ${package.shipping_cost:.2f} | {package.current_location}"
            )

    print()
    print("What the current project demo proves:")
    print("1. Allowed locations load from JSON and can be displayed.")
    print("2. A business profile can be created and selected.")
    print("3. A user profile can be created under the selected business.")
    print("4. A package can be registered under the active business and user.")
    print("5. Distance and price calculation are working.")
    print("6. Business management features can add sections and employees.")
    print("7. A package can be assigned to and moved between sections.")
    print("8. Data is saved and can be read back from storage files.")


# main runner

def run_demo():
    print_title("TEAM LFS TRACKING PROGRAM - MANUAL DEMO TEST")
    print("This file is a readable walkthrough of what the current program can do so far.")

    cities = show_allowed_locations()
    business = setup_demo_business(cities)
    user = setup_demo_user(business)
    package = setup_demo_package(business, user, cities)
    business = setup_demo_business_management(business, user, package)
    show_final_summary(business, user)


if __name__ == "__main__":
    run_demo()