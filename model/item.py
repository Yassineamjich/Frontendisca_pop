class Item:
    def __init__(self, id, name, description, category_id, full_stock, documentation, details=None):
        self.id = id
        self.name = name
        # Use a default message if description is empty
        self.description = description if description else "No description available"
        # Expected to be a list like [category_id, "Category Name"]
        self.category_id = category_id  
        self.full_stock = full_stock
        self.documentation = documentation
        # details is a list of detail dictionaries (or objects)
        self.details = details if details is not None else []

    def __str__(self):
        # Build details summary if details exist
        details_str = ""
        if self.details:
            details_info = []
            for detail in self.details:
                # Extract the location name from the enriched 'location' field or from 'location_id'
                if "location" in detail and detail["location"]:
                    location_name = detail["location"].get("name", "Unknown")
                elif "location_id" in detail and isinstance(detail["location_id"], list):
                    location_name = detail["location_id"][1] if len(detail["location_id"]) > 1 else "Unknown"
                else:
                    location_name = "Unknown"
                
                # Extract the stock value from the detail
                stock = detail.get("stock", "N/A")
                details_info.append(f"[Location: {location_name}, Stock: {stock}]")
            details_str = ", Details: " + " | ".join(details_info)

        return (f"Item(ID: {self.id}, Name: {self.name}, Description: {self.description}, "
                f"Category: {self.category_id[1]}, Full Stock: {self.full_stock}, "
                f"Documentation: {self.documentation}{details_str})")
    
    # Getter methods
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_category_id(self):
        return self.category_id
    
    def get_full_stock(self):
        return self.full_stock
    
    def get_documentation(self):
        return self.documentation
    
    def get_details(self):
        return self.details
