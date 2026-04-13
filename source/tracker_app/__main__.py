"""
Main entry point for the Business Packaging Program.
Connects all modules: Business Menu, User Menu, Package Menu, and Logistics Tools.

Author: Saif Al Habashneh (Frontend Integration & Logistics)
Team: LFS — CPSC 362
"""

from tracker_app.storage.business_storage import (
    list_businesses,
    get_closest_business,
    get_route_order,
    get_route_distance,
)
from tracker_app.ui.business_menu import run_business_menu
from tracker_app.ui.user_menu import run_user_menu
from tracker_app.ui.package_menu import run_package_menu
from tracker_app.ui.input_helpers import ask_int, pause


# ──────────────────────────────────────────────
#  Logistics Tools  (Saif's contribution)
#  Haversine-based closest business & route
# ──────────────────────────────────────────────

def _find_closest():
    """Find the closest business to a given business ID using haversine distance."""
    businesses = list_businesses()
    if len(businesses) == 0:
        print("\nNo businesses registered yet.")
        return

    print("\nRegistered Businesses:")
    for b in businesses:
        print(f"  ID {b.business_id}: {b.business_name} ({b.location_city})")

    try:
        bid = ask_int("\nEnter business ID to find closest neighbor: ", min_value=1)
    except (ValueError, KeyboardInterrupt):
        print("Cancelled.")
        return

    result = get_closest_business(bid)

    if result:
        print(f"\n  Closest to ID {bid}:")
        print(f"  → {result.business_name} ({result.location_city})")
    else:
        print("\n  Could not find a closest business. Check the ID and try again.")


def _show_route():
    """Display optimal route order and total distance from a starting business."""
    businesses = list_businesses()
    if len(businesses) == 0:
        print("\nNo businesses registered yet.")
        return

    print("\nRegistered Businesses:")
    for b in businesses:
        print(f"  ID {b.business_id}: {b.business_name} ({b.location_city})")

    try:
        bid = ask_int("\nStart route from business ID: ", min_value=1)
    except (ValueError, KeyboardInterrupt):
        print("Cancelled.")
        return

    route = get_route_order(bid)

    if not route:
        print("\n  Could not compute route. Check the ID and try again.")
        return

    print("\n  ┌─────────────────────────────────┐")
    print("  │         OPTIMAL ROUTE           │")
    print("  └─────────────────────────────────┘")
    for i, b in enumerate(route, 1):
        print(f"  {i}. {b.business_name} ({b.location_city})")

    total = get_route_distance(route)
    print(f"\n  Total distance: {total:.2f} km")


def _run_logistics_menu():
    """Logistics tools sub-menu — closest business finder and route optimizer."""
    while True:
        print("\n================================")
        print("  Logistics Tools")
        print("================================")
        print("\n1) Find Closest Business")
        print("2) Show Optimal Route")
        print("0) Back")

        choice = ask_int("\nChoose an option: ", min_value=0, max_value=2)

        if choice == 1:
            _find_closest()
            pause()
        elif choice == 2:
            _show_route()
            pause()
        elif choice == 0:
            break


# ──────────────────────────────────────────────
#  Main Menu
# ──────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════════════╗")
    print("║      Business Packaging Program      ║")
    print("║              Team LFS                ║")
    print("╚══════════════════════════════════════╝")

    while True:
        print("\n================================")
        print("  Main Menu")
        print("================================")
        print("\n1) Business Management")
        print("2) User Management")
        print("3) Package Management")
        print("4) Logistics Tools")
        print("0) Exit")

        choice = ask_int("\nChoose an option: ", min_value=0, max_value=4)

        if choice == 1:
            run_business_menu()
        elif choice == 2:
            run_user_menu()
        elif choice == 3:
            run_package_menu()
        elif choice == 4:
            _run_logistics_menu()
        elif choice == 0:
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()