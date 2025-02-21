import model.item
import controllers.controllerLocation as control

class ControllerItem:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present

    def get_all_items(self):
        url = f"{self.base_url}/api/iscapop/item"
        response = self.session.get(url)
        
        # Instantiate the location controller with the same session
        controllocation = control.ControllerLocation(self.session, self.base_url)
        
        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None
            
            items_list = []
            for item in data.get('items', []):
                details_list = []
                if item.get("details"):
                    for detail in item["details"]:
                        # Assume location_id is a list [id, name]
                        loc_id = detail["location_id"][0]
                        location_obj = controllocation.get_location(loc_id)
                        if location_obj:
                            detail["location"] = {
                                "id": location_obj.get_id(),
                                "name": location_obj.get_name(),
                                "description": location_obj.get_description(),
                                "location_type": getattr(location_obj, "location_type", None)
                            }
                        details_list.append(detail)
                
                item_obj = model.item.Item(
                    id=item["id"],
                    name=item["name"],
                    description=item["description"] if item["description"] else "No description available",
                    category_id=item["category_id"],
                    full_stock=item["full_stock"],
                    documentation=item["documentation"],
                    details=details_list
                )
                items_list.append(item_obj)
            
            return items_list
        else:
            print(f"Failed to fetch items: {response.status_code}")
            return None

    def create_item(self, name, description, category_id, documentation):
        """
        Create a new item using the POST /api/iscapop/item endpoint.
        Expected payload based on API documentation:
        {
          "name": "Cuaderno",
          "description": "Cuaderno de 100 hojas",
          "category_id": 23,
          "documentation": "Certificado de calidad ISO 9001"
        }
        """
        url = f"{self.base_url}/api/iscapop/item"
        payload = {
            "name": name,
            "description": description,
            "category_id": category_id,
            "documentation": documentation
        }
        response = self.session.post(url, json=payload)
        if response.status_code in [200, 201]:
            try:
                data = response.json()
                # Return the created item if wrapped under key "item"
                return data.get("item", data)
            except Exception as e:
                print("Error decoding JSON:", e)
                return None
        else:
            print(f"Failed to create item: {response.status_code}")
            return None

    def update_item(self, item_id, name, description, category_id, documentation):
        url = f"{self.base_url}/api/iscapop/item/{item_id}"
        payload = {
            "name": name,
            "description": description,
            "category_id": category_id,
            "documentation": documentation
        }
        response = self.session.put(url, json=payload)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None
        else:
            print(f"Failed to update item: {response.status_code}")
            return None

    def delete_item(self, item_id):
        url = f"{self.base_url}/api/iscapop/item/{item_id}"
        response = self.session.delete(url)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None
        else:
            print(f"Failed to delete item: {response.status_code}")
            return None

    def move_item(self, item_id, new_location_id):
            # Use the controller's get_item method (which uses the session) to fetch the item.
            item = self.get_item(item_id)
            if not item:
                print("Item not found.")
                return None
            if not item.details:
                print("The item has no details to move.")
                return None

            # Extract the detail ids from the item's details.
            item_detail_ids = []
            for detail in item.details:
                detail_id = detail.get("id")
                if detail_id is not None:
                    item_detail_ids.append(detail_id)
            
            url = f"{self.base_url}/api/iscapop/move_items"
            payload = {
                "item_detail_ids": item_detail_ids,
                "new_location_id": new_location_id
            }
            response = self.session.put(url, json=payload)
            if response.status_code == 200:
                try:
                    return response.json()
                except Exception as e:
                    print("Error decoding JSON:", e)
                    return None
            else:
                print(f"Failed to move item: {response.status_code}")
                return None

    def get_item(self, item_id):
        url = f"{self.base_url}/api/iscapop/item/{item_id}"
        response = self.session.get(url)
        if response.status_code == 200:
            try:
                item_data = response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None

            # Check if the data is wrapped under "item" or "items"
            if "item" in item_data:
                item = item_data["item"]
            elif "items" in item_data:
                if item_data["items"]:
                    item = item_data["items"][0]
                else:
                    print("Error: 'items' list is empty.")
                    return None
            else:
                # Fall back to using the response directly
                item = item_data

            details_list = []
            if item.get("details"):
                controllocation = control.ControllerLocation(self.session, self.base_url)
                for detail in item["details"]:
                    if "location_id" in detail and isinstance(detail["location_id"], list):
                        loc_id = detail["location_id"][0]
                        location_obj = controllocation.get_location(loc_id)
                        if location_obj:
                            detail["location"] = {
                                "id": location_obj.get_id(),
                                "name": location_obj.get_name(),
                                "description": location_obj.get_description(),
                                "location_type": getattr(location_obj, "location_type", None)
                            }
                    details_list.append(detail)
            
            id_value = item.get("id") or item.get("item_id")
            if id_value is None:
                print("Error: Item data does not contain an 'id' key:", item)
                return None

            item_obj = model.item.Item(
                id=id_value,
                name=item.get("name", "Unknown"),
                description=item.get("description") if item.get("description") else "No description available",
                category_id=item.get("category_id", ["Unknown", "Unknown"]),
                full_stock=item.get("full_stock", 0),
                documentation=item.get("documentation", False),
                details=details_list
            )
            return item_obj
        else:
            print(f"Failed to fetch item: {response.status_code}")
            return None
