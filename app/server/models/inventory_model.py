class Inventory:
    def __init__(self, inventory_id, title, full, movie_id, upc, charge, modified_on):
        self.id = inventory_id
        self.title = title
        self.full = full
        self.movie_id = movie_id
        self.upc = upc
        self.charge = charge
        dt_frmt = '%m/%d/%Y %I:%M %p'
        self.modified_on = modified_on.strftime(
            dt_frmt) if modified_on is not None else None

    def as_dict(self):
        return vars(self)
