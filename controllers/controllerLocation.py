import model.location

class ControllerLocation:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url.rstrip('/') if base_url else ""

    def get_all_locations(self):
        url = f"{self.base_url}/api/iscapop/location"
        response = self.session.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return []
            location_list = []
            for location in data.get("locations", []):
                location_obj = model.location.LocationModel(
                    location["id"],
                    location["name"],
                    location["description"],
                    location["location_type"],
                    location.get("item_detail_ids", [])
                )
                location_list.append(location_obj)
            return location_list
        else:
            print("Error while fetching locations:", response.status_code)
            return []

    def get_location(self, location_id):
        url = f"{self.base_url}/api/iscapop/location/{location_id}"
        response = self.session.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None

            # Depending on your API, the response might include a single "location"
            # or a list under "locations"
            if "location" in data:
                location_data = data["location"]
            elif "locations" in data and len(data["locations"]) > 0:
                location_data = data["locations"][0]
            else:
                print("Location not found in response")
                return None

            location_obj = model.location.LocationModel(
                location_data["id"],
                location_data["name"],
                location_data["description"],
                location_data["location_type"],
                location_data.get("item_detail_ids", [])
            )
            return location_obj
        else:
            print(f"Error while fetching location with id {location_id}: {response.status_code}")
            return None

   
