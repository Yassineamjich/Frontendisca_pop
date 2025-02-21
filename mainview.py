import requests
import controllers.controllerCategoria
import controllers.controllerDonation
import controllers.controllerItem
import controllers.controllerLocation

def authenticate():
    BASE_URL = "http://proy.isca.es:15001"
    LOGIN_URL = f"{BASE_URL}/web/session/authenticate"
    
    while True:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        payload = {
            "jsonrpc": "2.0",
            "params": {
                "db": "odooDB",
                "login": email,
                "password": password
            }
        }

        session = requests.Session()
        response = session.post(LOGIN_URL, json=payload)

        if response.ok and response.json().get("result"):
            print("Login OK")
            return session, response.json()["result"]
        else:
            print("Error: Invalid credentials. Please try again.")

# Authenticate and set up controllers
session, auth_data = authenticate()
token = session.cookies.get("session_id")
if token:
    print("Your token (session_id) is:", token)
else:
    print("No session token found!")

#api_url = "http://192.168.215.125:8069"
api_url = "http://proy.isca.es:15001"
controlcategorie = controllers.controllerCategoria.ControllerCategory(session, api_url)
controlDonation   = controllers.controllerDonation.ControllerDonation(session, api_url)
controlitems      = controllers.controllerItem.ControllerItem(session, api_url)
controllocation   = controllers.controllerLocation.ControllerLocation(session, api_url)

while True:
    print("\n==== Main Menu ====")
    print("** GET Operations **")
    print("1. Get all items")
    print("2. Get all categories")
    print("3. Get all locations")
    print("4. Get all donations")
    print("\n** CREATE Operations **")
    print("5. Add an item")
    print("6. Add a donation")
    print("\n** MODIFY Operations **")
    print("7. Move an item")
    print("8. Modify a category")
    print("9. Modify an item")
    print("\n** DELETE Operations **")
    print("10. Delete an item")
    print("11. Delete a category")
    print("\n12. Exit")

    op = input("Enter an option: ").strip()

    # GET Operations
    if op == "1":
        print("\nFetching all items...")
        items = controlitems.get_all_items()
        if items:
            for item in items:
                print(item)
        else:
            print("Failed to fetch items.")
    elif op == "2":
        print("\nFetching all categories...")
        categories = controlcategorie.get_all_categories()
        if categories:
            for category in categories:
                print(f"{category['id']}: {category['name']}")
        else:
            print("Failed to fetch categories.")
    elif op == "3":
        print("\nFetching all locations...")
        locations = controllocation.get_all_locations()
        if locations:
            for location in locations:
                # Assuming location is a model object with attributes
                print(f"{location.get_id()}: {location.get_name()}")
        else:
            print("Failed to fetch locations.")
    elif op == "4":
        print("\nFetching all donations...")
        donations = controlDonation.get_all_donations()
        if donations:
            for donation in donations:
                print(donation)
        else:
            print("Failed to fetch donations.")

    # CREATE Operations
    elif op == "5":
        print("\n=== Add a New Item ===")
        name = input("Enter item name: ")
        description = input("Enter item description: ")

        # List and choose a category
        categories = controlcategorie.get_all_categories()
        if categories:
            print("Available categories:")
            for category in categories:
                print(f"{category['id']}: {category['name']}")
            try:
                category_id = int(input("Enter category id: "))
            except ValueError:
                print("Invalid category id. Aborting.")
                continue
        else:
            print("No categories available. Aborting.")
            continue

        # For create_item, the API expects documentation as a string.
        doc_input = input("Enter documentation details (or leave blank): ").strip()
        documentation = doc_input if doc_input else ""
        
        result = controlitems.create_item(name, description, category_id, documentation)
        if result:
            print("Item created successfully:")
            print(result)
        else:
            print("Failed to create item.")

    elif op == "6":
        print("\n=== Add a Donation ===")
        # List items and choose one
        items = controlitems.get_all_items()
        if items:
            print("Available items:")
            for item in items:
                print(f"{item.id}: {item.name}")
            try:
                item_id = int(input("Enter item id: "))
            except ValueError:
                print("Invalid item id. Aborting.")
                continue
        else:
            print("No items available. Aborting.")
            continue

        try:
            stock_shared = int(input("Enter shared stock quantity: "))
        except ValueError:
            print("Invalid stock quantity. Aborting.")
            continue

        donation = controlDonation.add_donation(item_id, stock_shared)
        if donation:
            print("Donation added successfully:")
            print(donation)
        else:
            print("Failed to add donation.")

    # MODIFY Operations
    elif op == "7":
        print("\n=== Move an Item's Details ===")
        items = controlitems.get_all_items()
        if items:
            print("Available items:")
            for item in items:
                print(f"{item.id}: {item.name}")
            try:
                item_id = int(input("Enter the item id to move: "))
            except ValueError:
                print("Invalid item id. Aborting.")
                continue
        else:
            print("No items available. Aborting.")
            continue

        # Check if the selected item exists and has details.
        selected_item = next((item for item in items if item.id == item_id), None)
        if not selected_item:
            print("Item not found. Aborting.")
            continue

        if not selected_item.details:
            print("The selected item has no details to move. Aborting.")
            continue

        # Retrieve available destination locations.
        locations = controllocation.get_all_locations()
        if locations:
            print("Available destination locations:")
            for loc in locations:
                print(f"{loc.get_id()}: {loc.get_name()}")
            try:
                new_location_id = int(input("Enter destination location id: "))
            except ValueError:
                print("Invalid location id. Aborting.")
                continue
        else:
            print("No locations available. Aborting.")
            continue

        # Call move_item with the item id and new location id.
        result = controlitems.move_item(item_id, new_location_id)
        if result:
            print("Item details moved successfully:", result)
        else:
            print("Failed to move item details.")
    elif op == "8":
        print("\n=== Modify a Category ===")
        categories = controlcategorie.get_all_categories()
        if categories:
            print("Available categories:")
            for category in categories:
                print(f"{category['id']}: {category['name']}")
            try:
                category_id = int(input("Enter category id to modify: "))
            except ValueError:
                print("Invalid category id. Aborting.")
                continue
        else:
            print("No categories available. Aborting.")
            continue

        name = input("Enter new category name: ")
        description = input("Enter new category description: ")
        result = controlcategorie.update_category(category_id, name, description)
        if result:
            print("Category updated successfully:", result)
        else:
            print("Failed to update category.")

    elif op == "9":
        print("\n=== Modify an Item ===")
        items = controlitems.get_all_items()
        if items:
            print("Available items:")
            for item in items:
                print(f"{item.id}: {item.name}")
            try:
                item_id = int(input("Enter item id to modify: "))
            except ValueError:
                print("Invalid item id. Aborting.")
                continue
        else:
            print("No items available. Aborting.")
            continue

        categories = controlcategorie.get_all_categories()
        if categories:
            print("Available categories:")
            for category in categories:
                print(f"{category['id']}: {category['name']}")
            try:
                category_id = int(input("Enter new category id: "))
            except ValueError:
                print("Invalid category id. Aborting.")
                continue
        else:
            print("No categories available. Aborting.")
            continue

        name = input("Enter new item name: ")
        description = input("Enter new item description: ")
        doc_input = input("Is documentation available? (yes/no): ").strip().lower()
        documentation = True if doc_input == "yes" else False
        result = controlitems.update_item(item_id, name, description, category_id, documentation)
        if result:
            print("Item updated successfully:", result)
        else:
            print("Failed to update item.")

    # DELETE Operations
    elif op == "10":
        print("\n=== Delete an Item ===")
        items = controlitems.get_all_items()
        if items:
            print("Available items:")
            for item in items:
                print(f"{item.id}: {item.name}")
            try:
                item_id = int(input("Enter item id to delete: "))
            except ValueError:
                print("Invalid item id. Aborting.")
                continue
        else:
            print("No items available. Aborting.")
            continue

        result = controlitems.delete_item(item_id)
        if result:
            print("Item deleted successfully:", result)
        else:
            print("Failed to delete item.")

    elif op == "11":
        print("\n=== Delete a Category ===")
        categories = controlcategorie.get_all_categories()
        if categories:
            print("Available categories:")
            for category in categories:
                print(f"{category['id']}: {category['name']}")
            try:
                category_id = int(input("Enter category id to delete: "))
            except ValueError:
                print("Invalid category id. Aborting.")
                continue
        else:
            print("No categories available. Aborting.")
            continue

        result = controlcategorie.delete_category(category_id)
        if result:
            print("Category deleted successfully:", result)
        else:
            print("Failed to delete category.")

    
   
    elif op == "12":
        print("\nExiting program. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
