from pathlib import Path
import sys

if __package__ in {None, ""}:
    current_file = Path(__file__).resolve()
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

from tracker_app.app.app_state import set_active_business, set_active_user, load_state
from tracker_app.service.location_service import list_city_names, get_location_dict_for_math
from tracker_app.storage.business_storage import create_business, list_businesses, get_business_by_id
from tracker_app.storage.user_storage import create_user, list_users_for_business, get_user_by_id
from tracker_app.storage.package_storage import create_package, get_packages_by_business
from services.distance_service import DistanceService
from services.pricing_service import PricingService


class DemoReport:
    def __init__(self):
        self.lines = []

    def add(self, text=""):
        self.lines.append(str(text))

    def line(self, char="=", width=78):
        self.lines.append(char * width)

    def title(self, text):
        self.add()
        self.line("=")
        self.add(text)
        self.line("=")

    def section(self, text):
        self.add()
        self.line("-")
        self.add(text)
        self.line("-")

    def kv(self, label, value):
        self.add(f"{label:<28}: {value}")

    def bullet(self, text):
        self.add(f"- {text}")

    def render(self):
        return "\n".join(self.lines)

    def save(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.render(), encoding="utf-8")
        return output_path

    def print_report(self):
        print(self.render())


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


def create_or_get_business(business_name, business_city):
    business = find_business_by_name(business_name)
    if business is None:
        business = create_business(business_name, business_city)
        return business, "Created new business"
    return business, "Reused existing business"


def create_or_get_user(first_name, last_name, email, phone, billing, business_id):
    user = find_user_for_business(business_id, email)
    if user is None:
        user = create_user(first_name, last_name, email, phone, billing, business_id)
        return user, "Created new user"
    return user, "Reused existing user"


def create_demo_package(business, user, description, weight_kg, destination_city):
    locations = get_location_dict_for_math()
    distance_km = DistanceService.get_distance(
        business.location_city,
        destination_city,
        locations,
    )
    shipping_cost = PricingService.calculate_shipping_cost(distance_km, weight_kg)

    package = create_package(
        business.business_id,
        user.user_id,
        business.location_city,
        destination_city,
        weight_kg,
        description,
        shipping_cost,
    )

    return package, distance_km, shipping_cost


def run_business_user_case(report, case_data):
    report.section(case_data["case_name"])

    business, business_result = create_or_get_business(
        case_data["business_name"],
        case_data["business_city"]
    )
    set_active_business(business.business_id)

    user, user_result = create_or_get_user(
        case_data["first_name"],
        case_data["last_name"],
        case_data["email"],
        case_data["phone"],
        case_data["billing"],
        business.business_id
    )
    set_active_user(user.user_id)

    report.kv("Business name input", case_data["business_name"])
    report.kv("Business city input", case_data["business_city"])
    report.kv("Business result", business_result)
    report.kv("Business ID", business.business_id)

    report.kv("User first name", case_data["first_name"])
    report.kv("User last name", case_data["last_name"])
    report.kv("User email", case_data["email"])
    report.kv("User phone", case_data["phone"])
    report.kv("User billing", case_data["billing"])
    report.kv("User result", user_result)
    report.kv("User ID", user.user_id)
    report.kv("Linked business ID", user.business_id)

    if case_data.get("make_package"):
        package, distance_km, shipping_cost = create_demo_package(
            business,
            user,
            case_data["package_description"],
            case_data["package_weight"],
            case_data["destination_city"]
        )

        report.kv("Package description", case_data["package_description"])
        report.kv("Package weight", f'{case_data["package_weight"]} kg')
        report.kv("Destination city", case_data["destination_city"])
        report.kv("Distance", f"{distance_km:.2f} km")
        report.kv("Shipping cost", f"${shipping_cost:.2f}")
        report.kv("Package ID", package.package_id)

    return business, user


def run_demo(output_filename="manual_demo_report.txt", also_print=True):
    report = DemoReport()

    report.title("TEAM LFS TRACKING PROGRAM - BUSINESS/USER INPUT TEST DEMO")
    report.add("This demo runs 5 different business and user creation scenarios.")
    report.add("Each test case shows input values and the output produced by the program.")

    cities = list_city_names()

    test_cases = [
        {
            "case_name": "TEST CASE 1 - Retail Store Business",
            "business_name": "Sunset Retail",
            "business_city": "Los Angeles",
            "first_name": "Maria",
            "last_name": "Lopez",
            "email": "maria.sunset@email.com",
            "phone": "555-1001",
            "billing": "Visa 1111",
            "make_package": True,
            "package_description": "Clothing Shipment",
            "package_weight": 2.0,
            "destination_city": "London",
        },
        {
            "case_name": "TEST CASE 2 - Warehouse Business",
            "business_name": "Global Storage Hub",
            "business_city": "London",
            "first_name": "David",
            "last_name": "Nguyen",
            "email": "david.global@email.com",
            "phone": "555-1002",
            "billing": "Mastercard 2222",
            "make_package": True,
            "package_description": "Storage Parts",
            "package_weight": 6.5,
            "destination_city": "Tokyo",
        },
        {
            "case_name": "TEST CASE 3 - Tech Office Business",
            "business_name": "NextByte Tech",
            "business_city": "Tokyo",
            "first_name": "Emily",
            "last_name": "Chen",
            "email": "emily.nextbyte@email.com",
            "phone": "555-1003",
            "billing": "Amex 3333",
            "make_package": True,
            "package_description": "Computer Equipment",
            "package_weight": 4.2,
            "destination_city": "Los Angeles",
        },
        {
            "case_name": "TEST CASE 4 - Food Distribution Business",
            "business_name": "FreshRoute Foods",
            "business_city": "Buenos Aires",
            "first_name": "Carlos",
            "last_name": "Martinez",
            "email": "carlos.freshroute@email.com",
            "phone": "555-1004",
            "billing": "Visa 4444",
            "make_package": True,
            "package_description": "Dry Food Boxes",
            "package_weight": 7.8,
            "destination_city": "London",
        },
        {
            "case_name": "TEST CASE 5 - Medical Supply Business",
            "business_name": "CareBridge Supply",
            "business_city": "Sydney",
            "first_name": "Ava",
            "last_name": "Patel",
            "email": "ava.carebridge@email.com",
            "phone": "555-1005",
            "billing": "Discover 5555",
            "make_package": True,
            "package_description": "Medical Equipment",
            "package_weight": 5.3,
            "destination_city": "Tokyo",
        },
    ]

    valid_test_cases = []
    for case in test_cases:
        if case["business_city"] in cities and case["destination_city"] in cities:
            valid_test_cases.append(case)

    last_business = None
    last_user = None

    for case in valid_test_cases:
        last_business, last_user = run_business_user_case(report, case)

    state = load_state()
    report.title("FINAL SUMMARY")
    report.kv("Last active business ID", state.get("active_business_id"))
    report.kv("Last active user ID", state.get("active_user_id"))

    if last_business is not None:
        business_packages = get_packages_by_business(last_business.business_id)
        report.kv("Last business package count", len(business_packages))

    report.kv("Total test cases run", len(valid_test_cases))

    output_path = Path(__file__).resolve().parents[3] / "reports" / output_filename
    saved_path = report.save(output_path)

    if also_print:
        report.print_report()
        print()
        print(f"Report saved to: {saved_path}")

    return saved_path


if __name__ == "__main__":
    run_demo()