# input_helpers

# Helper functions for UI menus to stay simple
# Instead of repeating input-checking

def ask_non_empty(prompt):  # Keeps asking until the user types something non-empty
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("Please type something (cannot be blank).")

def ask_int(prompt, min_value=None, max_value=None): # Keeps asking until user types a valid integer 
    while True:
        text = input(prompt).strip()

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
    input("\nPress Enter to continue...")
