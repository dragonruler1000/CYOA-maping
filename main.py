import json
import os

# Load the book data from a JSON file, if it exists
def load_book_data(filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_directory, filename)

    if os.path.exists(full_path):
        with open(full_path, "r") as file:
            return json.load(file)
    else:
        print(f"File '{filename}' does not exist. Starting a new book data file.")
        return {"choices": {}, "endings": []}  # Initialize with structure for choices and endings

# Save the book data to a JSON file in the script's directory
def save_book_data(filename, book_data):
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_directory, filename)

        with open(full_path, "w") as file:
            json.dump(book_data, file, indent=4)
        print(f"Book data has been saved to '{full_path}'.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Add a new choice to the book data
def add_choice(book_data, current_page, choice_description, next_page):
    if current_page not in book_data["choices"]:
        book_data["choices"][current_page] = {}
    book_data["choices"][current_page][choice_description] = next_page

# Add an ending to the book data
def add_ending(book_data, page):
    if page not in book_data["endings"]:
        book_data["endings"].append(page)
        print(f"Page {page} has been added as an ending.")
    else:
        print(f"Page {page} is already marked as an ending.")

# Function to find a path to a specific ending
def find_path(book_data, start, ending, path=None):
    if path is None:
        path = [start]

    if start == ending:
        return path

    if start not in book_data["choices"]:
        return None

    for choice, next_page in book_data["choices"][start].items():
        if next_page not in path:  # Avoid loops
            new_path = find_path(book_data, next_page, ending, path + [next_page])
            if new_path:
                return new_path

    return None

# Generate and display a graph of choices
def display_graph(book_data):
    print("\nGraph of Choices:")
    for page, choices in book_data["choices"].items():
        print(f"Page {page}:")
        for choice_description, next_page in choices.items():
            print(f"  -> '{choice_description}' leads to Page {next_page}")
    
    print("\nEndings:")
    for ending in book_data["endings"]:
        print(f"  - Page {ending}")

# Main function to interact with the user
def main():
    filename = input("Enter the name of the book data file (e.g., 'book_data.json'): ")
    book_data = load_book_data(filename)

    while True:
        print("\nChoose an option:")
        print("1. Add a new choice")
        print("2. Add an ending")
        print("3. Find a path to an ending")
        print("4. Display graph of choices and endings")
        print("5. Save and exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            current_page = input("Enter the current page number: ")
            choice_description = input("Enter a description of the choice: ")
            next_page = input("Enter the page number this choice leads to: ")
            add_choice(book_data, current_page, choice_description, next_page)
            print(
                f"Added choice from page {current_page} -> '{choice_description}' -> page {next_page}"
            )

        elif choice == "2":
            ending_page = input("Enter the page number to mark as an ending: ")
            add_ending(book_data, ending_page)

        elif choice == "3":
            start_page = input("Enter the starting page: ")
            desired_ending = input("Enter the ending page: ")
            path_to_ending = find_path(book_data, start_page, desired_ending)

            if path_to_ending:
                print("To reach", desired_ending, "follow these steps:")
                for step in path_to_ending:
                    print("->", step)
            else:
                print("No path found to", desired_ending)

        elif choice == "4":
            display_graph(book_data)

        elif choice == "5":
            print("Attempting to save the book data...")
            save_book_data(filename, book_data)
            print("Save operation completed. Exiting...")
            input("Press Enter to exit...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
