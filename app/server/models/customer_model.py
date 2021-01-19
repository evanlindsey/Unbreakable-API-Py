class Customer:
    def __init__(self, customer_id, first, last, full, email, address, city, state, zip_code, phone):
        self.id = customer_id
        self.first = first
        self.last = last
        self.full = full
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.phone = phone

    def as_dict(self):
        return vars(self)
