class Movie:
    def __init__(self, movie_id, title, stock, rating, category, genres, year, minutes, language, actors, director, imdb):
        self.id = movie_id
        self.title = title
        self.stock = stock
        self.rating = str(rating) if rating is not None else '0'
        self.category = category
        self.genres = genres
        self.year = year
        self.minutes = minutes
        self.language = language
        self.actors = actors
        self.director = director
        self.imdb = imdb

    def as_dict(self):
        return vars(self)


class NewMovie:
    def __init__(self, category, title, genres, year, minutes, language, actors, director, imdb):
        self.category = category
        self.title = title
        self.genres = genres
        self.year = year
        self.minutes = minutes
        self.language = language
        self.actors = actors
        self.director = director
        self.imdb = imdb

    def as_dict(self):
        return vars(self)
