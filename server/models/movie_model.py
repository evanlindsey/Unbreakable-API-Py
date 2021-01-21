class Movie:
    def __init__(self, movie_id, category, title, genres, year, minutes, language, actors, director, imdb):
        self.id = movie_id
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
