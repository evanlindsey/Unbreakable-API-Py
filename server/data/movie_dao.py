from ..models.movie_model import Movie
from ..common.db_connect import sql_command, sql_select


def add_movie(movie):
    '''Add a row to the movies table using the given information.

    Args:
        movie: NewMovie class object.

    Returns:
        boolean: The return value. Movie ID if successful. -1 if error.
    '''
    query = ('INSERT INTO movies (category_id, title, genres, year, minutes, language, actors, director, imdb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);')
    data = (movie.category, movie.title, movie.genres, movie.year,
            movie.minutes, movie.language, movie.actors, movie.director, movie.imdb)
    try:
        return sql_command(query, data)
    except:
        return -1


def get_all_movies():
    '''Retrieve all movies from the all_movies view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_movies;'
    data = ()
    try:
        res = sql_select(query, data)
        if len(res) > 0:
            return [Movie(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]).as_dict() for x in res]
        return -1
    except:
        return -1


def get_movie(movie_id):
    '''Retrieve the movie from the all_movies view matching the target ID.

    Args:
        movie_id: Target movie ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = f'SELECT * FROM all_movies WHERE id = {movie_id};'
    data = ()
    try:
        res = sql_select(query, data)
        if len(res) == 1:
            x = res[0]
            return Movie(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]).as_dict()
        return -1
    except:
        return -1
