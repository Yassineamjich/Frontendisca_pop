import datetime
from model.donation import Donation  # Import Donation model properly
from controllers.controllerItem import ControllerItem
from controllers.controllerLocation import ControllerLocation

class ControllerDonation:
    def __init__(self, session, base_url=None):
        """
        Initialize the donation controller with a requests session and base URL.
        """
        self.session = session
        self.base_url = base_url.rstrip('/') if base_url else ""

    def get_all_donations(self):
        url = f"{self.base_url}/api/iscapop/donations"
        response = self.session.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None

            if "donations" in data:  # Ensure donations key exists
                donations_list = []
                
                # Initialize controllers for fetching related data with the same session
                # (in case you want to fetch full objects if necessary)
                item_controller = ControllerItem(self.session, self.base_url)
                location_controller = ControllerLocation(self.session, self.base_url)

                for donation_data in data["donations"]:
                    # Extract item info from the "item" key
                    if "item" in donation_data and isinstance(donation_data["item"], dict):
                        item_obj_data = donation_data["item"]
                        item_name = item_obj_data.get("name", "Unknown Item")
                        item_id = item_obj_data.get("id")
                        # Optionally, fetch the full item details using its ID
                        full_item = item_controller.get_item(item_id) if item_id else None
                    else:
                        item_name = "Unknown Item"
                        full_item = None

                    # Extract location info from the "location_id" list
                    location_info = donation_data.get("location_id")
                    if location_info and isinstance(location_info, list) and len(location_info) >= 2:
                        location_id = location_info[0]
                        location_name = location_info[1]
                        full_location = location_controller.get_location(location_id)
                    else:
                        location_name = "Unknown Location"
                        full_location = None

                    # Extract donated_by info from the "donated_by" list
                    donated_by_info = donation_data.get("donated_by")
                    if donated_by_info and isinstance(donated_by_info, list) and len(donated_by_info) >= 2:
                        donated_by_name = donated_by_info[1]
                    else:
                        donated_by_name = "Unknown Donor"

                    # Create the Donation object using the extracted values
                    donation_obj = Donation(
                        id=donation_data.get("id"),
                        item_id=item_name,           # Using the name instead of the ID
                        location_id=location_name,     # Using the name instead of the ID
                        donation_date=donation_data.get("donation_date"),
                        donated_by=donated_by_name,    # Using the name instead of the ID
                        stock_shared=donation_data.get("stock_shared"),
                        reserved=donation_data.get("reserved", False),
                        reserved_by=donation_data.get("reserved_by"),
                        destination_location_id=donation_data.get("destination_location_id"),
                        item_detail=None  # You might want to fetch this separately
                    )

                    # Attach fetched full objects
                    donation_obj.item = full_item
                    donation_obj.location = full_location

                    donations_list.append(donation_obj)

                return donations_list
            else:
                print("Donations key not found in response.")
                return None
        else:
            print(f"Failed to fetch donations: {response.status_code}")
            return None

    
    def add_donation(self, item_id, stock_shared):
     
        # Fetch the item using the provided item_id
        item_controller = ControllerItem(self.session, self.base_url)
        item_obj = item_controller.get_item(item_id)
        
        if not item_obj or not item_obj.details:
            print("Error: Item details not found or missing location.")
            return None

        # Extract the item detail from the first entry
        item_detail = item_obj.details[0]
        detail_id = item_detail.get("id")
        if not detail_id:
            print("Error: Item detail id not found.")
            return None

        # Get the destination location from the item detail
        destination_location_id = item_detail.get("location", {}).get("id")
        if not destination_location_id:
            print("Error: No destination location found for the item detail.")
            return None

        url = f"{self.base_url}/api/iscapop/donation"
        
        payload = {
            "item_detail_id": detail_id,  # Use the id extracted from item detail
            "stock_shared": stock_shared,
            "destination_location_id": destination_location_id
        }
        
        response = self.session.post(url, json=payload)
        
        if response.status_code in [200, 201]:
            try:
                data = response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None

            if "result" in data and "donation" in data["result"]:
                donation_data = data["result"]["donation"]
                item_detail_data = data["result"].get("item_detail", {})

                # Fetch additional location information
                location_controller = ControllerLocation(self.session, self.base_url)
                location_obj = location_controller.get_location(donation_data["location_id"])
                
                donation_obj = Donation(
                    id=donation_data.get("id"),
                    item_id=item_obj.get_id() if item_obj else donation_data["item_id"],
                    location_id=location_obj.get_id() if location_obj else donation_data["location_id"],
                    donation_date=donation_data.get("donation_date"),
                    donated_by=donation_data.get("donated_by"),
                    stock_shared=donation_data.get("stock_shared"),
                    reserved=donation_data.get("reserved", False),
                    destination_location_id=donation_data.get("destination_location_id"),
                    item_detail=item_detail_data
                )

                return donation_obj

        print(f"Failed to add donation: {response.status_code}, {response.text}")
        return None