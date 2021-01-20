from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize
from ..models.movie_model import Movie, NewMovie
from ..data.movie_dao import add_movie, get_all_movies, get_movie

movies = Blueprint('movies', __name__, url_prefix='/api/movies')


@movies.route('/', methods=['POST'])
@authorize
def create(jwt_info):
    '''Movie create endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: NewMovie
          in: body
          required: true
          schema:
            $ref: '#/definitions/NewMovie'
    definitions:
        NewMovie:
            type: object
            properties:
                category:
                    type: string
                title:
                    type: string
                genres:
                    type: string
                year:
                    type: string
                minutes:
                    type: string
                language:
                    type: string
                actors:
                    type: string
                director:
                    type: string
                imdb:
                    type: string
    responses:
        200:
            description: Movie ID
            schema:
                properties:
                    MovieID:
                        type: object
                        properties:
                            id:
                                type: string
        400:
            description: Unable to create movie
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = NewMovie(x['category'], x['title'], x['genres'], x['year'],
                       x['minutes'], x['language'], x['actors'], x['director'], x['imdb'])
    movie_id = add_movie(payload)
    if movie_id is not None and movie_id != -1:
        return jsonify({'id': movie_id})
    return error('unable to create movie.')


@movies.route('/all', methods=['GET'])
def read_all():
    '''All movies read endpoint
    ---
    definitions:
        Movie:
            type: object
            properties:
                id:
                    type: string
                title:
                    type: string
                full:
                    type: string
                stock:
                    type: string
                rating:
                    type: string
                category:
                    type: string
                genres:
                    type: string
                year:
                    type: string
                minutes:
                    type: string
                language:
                    type: string
                actors:
                    type: string
                director:
                    type: string
                imdb:
                    type: string
    responses:
        200:
            description: All movies in the system
            schema:
                properties:
                    Movies:
                        type: array
                        items:
                            schema:
                                id: Movie
                                schema:
                                    $ref: '#/definitions/Movie'
        400:
            description: Unable to retrieve movies
            schema:
                properties:
                    error:
                        type: string
    '''
    movies = get_all_movies()
    if movies != -1:
        return jsonify(movies)
    return error('unable to retrieve movies.')


@movies.route('/', methods=['GET'])
def read():
    '''Movie read endpoint
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: true
    definitions:
        Movie:
            type: object
            properties:
                id:
                    type: string
                title:
                    type: string
                full:
                    type: string
                stock:
                    type: string
                rating:
                    type: string
                category:
                    type: string
                genres:
                    type: string
                year:
                    type: string
                minutes:
                    type: string
                language:
                    type: string
                actors:
                    type: string
                director:
                    type: string
                imdb:
                    type: string
    responses:
        200:
            description: Movie information matching target ID
            schema:
                $ref: '#/definitions/Movie'
        400:
            description: Unable to retrieve movie
            schema:
                properties:
                    error:
                        type: string
    '''
    movie_id = request.args.get('id')
    if movie_id is None or movie_id == 'null' or movie_id == 'undefined':
        return error('movie id was not provided.')
    movie = get_movie(movie_id)
    if movie != -1:
        return jsonify(movie)
    return error('unable to retrieve movie.')
