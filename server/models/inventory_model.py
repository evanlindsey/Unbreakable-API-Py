class Inventory:
    def __init__(self, movie_id, upc):
        self.movie_id = movie_id
        self.upc = upc

    def as_dict(self):
        return vars(self)
