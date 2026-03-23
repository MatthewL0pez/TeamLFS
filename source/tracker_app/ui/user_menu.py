# User Menu UI

# Simple text menu for user profiles.
# rule:
# - A user can ONLY be created if a business is selected.
#
# It uses:
# - user_storage.py   (to store/list users)
# - business_storage.py (to confirm selected business)
# - app_state.py      (active_business_id + active_user_id)

from tracker_app.ui.input_helpers import ask_non_empty, ask_int, pause
from tracker_app.storage.user_storage import create_user, list_users_for_business, get_user_by_id
from tracker_app.storage.business_storage import get_business_by_id
from tracker_app.app.app_state import load_state, set_active_user, clear_active_user

def _get_active_business(): # Returns the active business object or None
    state = load_state()
    biz_id = state.get("active_business_id")

    if biz_id is None:
        return None

    return get_business_by_id(biz_id)


def _print_active_info(): # Shows current selected business and selected user
    state = load_state()
    biz = _get_active_business()

    if biz is None:
        print("Active Business: (none)")
    else:
        print(f"Active Business: {biz.business_name} (ID {biz.business_id})")

    user_id = state.get("active_user_id")
    if user_id is None:
        print("Active User: (none)")
    else:
        user = get_user_by_id(user_id)
        if user is None:
            print("Active User: (missing / deleted?)")
        else:
            print(f"Active User: {user.first_name} {user.last_name} (ID {user.user_id})")

def _list_users(): # Lists users only for the active business
    biz = _get_active_business()
    if biz is None:
        print("\nYou must select a business first (Business Menu).")
        return

    users = list_users_for_business(biz.business_id)
    if len(users) == 0:
        print("\nNo users found for this business yet.")
        return

    print(f"\nUsers for {biz.business_name}:")
    for u in users:
        print(f"- ID {u.user_id}: {u.first_name} {u.last_name} | {u.email}")


def _create_user(): # Creates a user under the active business
    biz = _get_active_business()
    if biz is None:
        print("\nYou must select a business first (Business Menu).")
        return

    print(f"\nCreate User for business: {biz.business_name}")

    first = ask_non_empty("First name: ")
    last = ask_non_empty("Last name: ")
    email = ask_non_empty("Email: ")
    phone = ask_non_empty("Phone: ")
    billing = ask_non_empty("Billing info (simple text): ")

    new_user = create_user(first, last, email, phone, billing, biz.business_id)
    print(f"\nCreated user: {new_user.first_name} {new_user.last_name} (ID {new_user.user_id})")

def _select_user(): # Select a user by ID only within the active business
    biz = _get_active_business()
    if biz is None:
        print("\nYou must select a business first (Business Menu).")
        return

    _list_users()
    picked_id = ask_int("\nEnter user ID to select: ", min_value=1)

    user = get_user_by_id(picked_id)
    if user is None:
        print("That user ID was not found.")
        return

    # user must belong to active business
    if not user.belongs_to_business(biz.business_id):
        print("That user does not belong to the currently selected business.")
        return

    set_active_user(user.user_id)
    print(f"\nSelected user: {user.first_name} {user.last_name} (ID {user.user_id})")


def _clear_user():
    clear_active_user()
    print("\nCleared active user selection.")

def run_user_menu():  # Main loop for the user menu
    while True:
        print("\n==============================")
        print(" User Menu")
        print("==============================")
        _print_active_info()

        print("\n1) List users (for active business)")
        print("2) Create user (requires active business)")
        print("3) Select user")
        print("4) Clear selected user")
        print("0) Back")

        choice = ask_int("\nChoose an option: ", min_value=0, max_value=4)

        if choice == 1:
            _list_users()
            pause()
        elif choice == 2:
            _create_user()
            pause()
        elif choice == 3:
            _select_user()
            pause()
        elif choice == 4:
            _clear_user()
            pause()
        elif choice == 0:
            break


# Example usage 

# from tracker_app.ui.user_menu import run_user_menu
# run_user_menu()