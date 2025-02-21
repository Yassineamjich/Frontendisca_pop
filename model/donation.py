class Donation:
    def __init__(self, id, item_id, location_id, donation_date, donated_by, stock_shared,
                 reserved=False, reserved_by=None, destination_location_id=None, item_detail=None):
        self.id = id
        self.item_id = item_id  # Integer
        self.location_id = location_id  # Integer
        self.donation_date = donation_date
        self.donated_by = donated_by  # Integer
        self.stock_shared = stock_shared
        self.reserved = reserved
        self.reserved_by = reserved_by
        self.destination_location_id = destination_location_id  # Optional
        self.item_detail = item_detail  # Dictionary expected
        self.item = None  # Full item object
        self.location = None  # Full location object

    def __str__(self):
        # Destination location string
        dest_loc_str = f", Destination Location: {self.destination_location_id}" if self.destination_location_id else ""

        # Item details string
        item_str = ""
        if self.item:
            item_str = (f", Item: [ID: {self.item.id}, Name: {self.item.name}, "
                        f"Category: {self.item.category_id[1]}, Full Stock: {self.item.full_stock}]")

        # Location details string
        location_str = ""
        if self.location:
            location_str = (f", Location: [ID: {self.location.id}, Name: {self.location.name}, "
                            f"Type: {self.location.location_type}]")

        # Item detail dictionary formatting
        item_detail_str = ""
        if self.item_detail:
            item_detail_str = f", Item Detail(ID: {self.item_detail.get('id')}, Remaining Stock: {self.item_detail.get('remaining_stock')})"

        return (f"Donation(ID: {self.id}, Item ID: {self.item_id}, Location ID: {self.location_id}, "
                f"Donation Date: {self.donation_date}, Donated By: {self.donated_by}, "
                f"Stock Shared: {self.stock_shared}, Reserved: {self.reserved}, "
                f"Reserved By: {self.reserved_by}{dest_loc_str}{item_str}{location_str}{item_detail_str})")
