class LocationModel:
    def __init__(self, id, name, description, location_type="classroom", item_detail_ids=None):
        self.id = id
        self.name = name
        self.description = description
        self.location_type = location_type
        self.item_detail_ids = item_detail_ids or []

    # Getter methods
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_location_type(self):
        return self.location_type
    
    def get_item_detail_ids(self):
        return self.item_detail_ids

    # __str__ method to represent the object as a string
    def __str__(self):
        return f"Location(ID: {self.id}, Name: {self.name}, Description: {self.description}, " \
               f"Location Type: {self.location_type}, Item Details: {self.item_detail_ids})"
