from datetime import datetime


class Rental:
    def __init__(self, rental_id, customer_name, customer_id, titles, movie_ids, rented_on, due_date):
        self.id = rental_id
        self.customer_name = customer_name
        self.customer_id = customer_id
        self.titles = titles
        self.movie_ids = movie_ids
        dt_frmt = '%m/%d/%Y %I:%M %p'
        self.rented_on = rented_on.strftime(
            dt_frmt) if rented_on is not None else None
        self.due_date = due_date.strftime(
            dt_frmt) if due_date is not None else None

    def as_dict(self):
        return vars(self)


class NewRental:
    def __init__(self, customer_id, inventory_ids, payment_amount):
        self.customer_id = customer_id
        self.inventory_ids = inventory_ids
        self.payment_amount = payment_amount

    def as_dict(self):
        return vars(self)


class ReturnInfo:
    def __init__(self, rental_id, customer_id, movie_ids, ratings):
        self.id = rental_id
        self.customer_id = customer_id
        self.movie_ids = movie_ids
        self.ratings = ratings

    def as_dict(self):
        return vars(self)
