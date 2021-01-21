from ..common.db_connect import sql_command, sql_select


def add_movie(movie):
    '''Add a row to the movies table using the given information.

    Args:
        movie: Movie class object.

    Returns:
        boolean: The return value. Movie ID if successful.
    '''
    query = ('INSERT INTO movies (category_id, title, genres, year, minutes, language, actors, director, imdb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);')
    data = (movie.category, movie.title, movie.genres, movie.year,
            movie.minutes, movie.language, movie.actors, movie.director, movie.imdb)
    return sql_command(query, data)


def get_all_movies():
    '''Retrieve all movies from the all_movies view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_movies;'
    data = ()
    return sql_select(query, data)


def get_movie(movie_id):
    '''Retrieve the movie from the all_movies view matching the target ID.

    Args:
        movie_id: Target movie ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = f'SELECT * FROM all_movies WHERE id = {movie_id};'
    data = ()
    return sql_select(query, data)


def update_movie(movie):
    '''Update the data fields for the row of the movies table that matches the movie ID.

    Args:
        movie: Movie class object.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('UPDATE movies SET category_id = %s, title = %s, genres = %s, year = %s, minutes = %s, language = %s, actors = %s, director = %s, imdb = %s WHERE id = %s;')
    data = (movie.category, movie.title, movie.genres, movie.year,
            movie.minutes, movie.language, movie.actors, movie.director, movie.imdb, movie.id)
    return sql_command(query, data)


def delete_movie(movie_id):
    '''Delete the row from the movies table that matches the target ID.

    Args:
        movie_id: Target movie ID.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('DELETE FROM movies WHERE id = %s;')
    data = (movie_id,)
    return sql_command(query, data)
