# input_helpers

# Helper functions for UI menus to stay simple
# Instead of repeating input-checking

def _read_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        raise SystemExit(0)


def ask_non_empty(prompt):  # Keeps asking until the user types something non-empty
    while True:
        text = _read_input(prompt).strip()
        if text != "":
            return text
        print("Please type something (cannot be blank).")

def ask_int(prompt, min_value=None, max_value=None): # Keeps asking until user types a valid integer 
    while True:
        text = _read_input(prompt).strip()

        # must be digits (no decimals)
        if not text.isdigit():
            print("Please enter a whole number.")
            continue

        num = int(text)

        if min_value is not None and num < min_value:
            print(f"Number must be at least {min_value}.")
            continue

        if max_value is not None and num > max_value:
            print(f"Number must be at most {max_value}.")
            continue

        return num

def ask_float(prompt, min_value=None, max_value=None):
    """Keeps asking until user types a valid decimal number (float)."""
    while True:
        text = _read_input(prompt).strip()

        try:
            # We use float() here because it handles decimals and negative signs
            num = float(text)
        except ValueError:
            print("Please enter a valid number (e.g., 1.5 or 10).")
            continue

        if min_value is not None and num < min_value:
            print(f"Value must be at least {min_value}.")
            continue

        if max_value is not None and num > max_value:
            print(f"Value must be at most {max_value}.")
            continue

        return num

def choose_from_list(title, options): # Displays numbered options and returns the chosen item (string)
                                      # options = ["Long Beach", "Los Angeles", ...]
    if len(options) == 0:
        print("No options available.")
        return None

    print("\n" + title)
    for i in range(len(options)):
        print(f"{i + 1}. {options[i]}")

    choice = ask_int("Choose a number: ", min_value=1, max_value=len(options))
    return options[choice - 1]


def pause(): # pause so user can read output before continuing
    _read_input("\nPress Enter to continue...")
