class Employee:
    def __init__(self, employee_id, email, role, first, last, address, city, state, zip_code, phone):
        self.id = employee_id
        self.email = email
        self.role = role
        self.first = first
        self.last = last
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.phone = phone

    def as_dict(self):
        return vars(self)
