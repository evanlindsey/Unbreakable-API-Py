class Rental:
    def __init__(self, customer_id, inventory_ids, payment_amount):
        self.customer_id = customer_id
        self.inventory_ids = inventory_ids
        self.payment_amount = payment_amount

    def as_dict(self):
        return vars(self)


class Return:
    def __init__(self, rental_id, customer_id, movie_ids, ratings):
        self.id = rental_id
        self.customer_id = customer_id
        self.movie_ids = movie_ids
        self.ratings = ratings

    def as_dict(self):
        return vars(self)
