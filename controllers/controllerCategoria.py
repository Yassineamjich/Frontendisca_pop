import model.item

class ControllerCategory:
    def __init__(self, session, base_url, headers=None):
        """
        Initialize the controller with a requests session, base URL, and optional headers.
        """
        self.session = session
        self.base_url = base_url.rstrip('/') if base_url else ""
        if headers:
            # Update session headers if provided
            self.session.headers.update(headers)

    def get_all_categories(self):
        """Fetch all categories from API, process them, and return structured JSON."""
        url = f"{self.base_url}/api/iscapop/categories"
        response = self.session.get(url)

        if response.status_code == 200:
            try:
                data = response.json()  # Convert response to JSON
            except Exception as e:
                print("Error decoding JSON:", e)
                return None

            # Check if data is a dictionary and contains "categories"
            if isinstance(data, dict) and "categories" in data:
                categories = data["categories"]  # Extract the list of categories
            else:
                print("Unexpected API response format:", data)
                return None

            # Process categories using a normal for loop
            processed_categories = []
            for category in categories:
                category_obj = {
                    "id": category.get("id"),
                    "name": category.get("name"),
                    "description": category.get("description") or "No description",
                    "child_ids": category.get("child_ids", []),
                    "father_id": category.get("father_id"),
                    "item_ids": category.get("item_ids", [])
                }
                processed_categories.append(category_obj)

            return processed_categories  # Return structured JSON list
        else:
            print(f"Failed to fetch categories: {response.status_code}")
            return None

    def update_category(self, category_id, name, description):
        """
        Update an existing category using PUT /api/iscapop/categories/<category_id>.
        """
        url = f"{self.base_url}/api/iscapop/categories/{category_id}"
        payload = {"name": name, "description": description}

        response = self.session.put(url, json=payload)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None
        else:
            print(f"Failed to update category: {response.status_code}")
            return None

    def delete_category(self, category_id):
        """
        Delete a category using DELETE /api/iscapop/categories/<category_id>.
        """
        url = f"{self.base_url}/api/iscapop/categories/{category_id}"
        response = self.session.delete(url)

        if response.status_code == 200:
            try:
                return response.json()
            except Exception as e:
                print("Error decoding JSON:", e)
                return None
        else:
            print(f"Failed to delete category: {response.status_code}")
            return None
