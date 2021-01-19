class RentalFee:
    def __init__(self, rental_id, customer_id, titles, fee, is_returned):
        self.rental_id = rental_id
        self.customer_id = customer_id
        self.titles = titles
        self.fee = fee
        self.is_returned = is_returned

    def as_dict(self):
        return vars(self)


class PaymentInfo:
    def __init__(self, rental_id, payment_type, payment_amount, card_ending):
        self.rental_id = rental_id
        self.payment_type = payment_type
        self.payment_amount = payment_amount
        self.card_ending = card_ending

    def as_dict(self):
        return vars(self)
