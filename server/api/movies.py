from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize
from ..models.movie_model import Movie
from ..data.movie_dao import add_movie, get_all_movies, get_movie, update_movie, delete_movie

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
        - name: Movie
          in: body
          required: true
          schema:
            $ref: '#/definitions/Movie'
    definitions:
        Movie:
            type: object
            properties:
                title:
                    type: string
                    description: The movie title.
                    default: "Starship Troopers"
                genres:
                    type: string
                    description: The movie genres.
                    default: "Action, Sci-Fi, War"
                year:
                    type: string
                    description: The movie year.
                    default: "1997"
                minutes:
                    type: string
                    description: The movie runtime in minutes.
                    default: "129"
                language:
                    type: string
                    description: The movie language.
                    default: "English"
                actors:
                    type: string
                    description: The movie top billed actors.
                    default: "Casper Van Dien, Denise Richards"
                director:
                    type: string
                    description: The movie director.
                    default: "Paul Verhoeven"
                imdb:
                    type: string
                    description: The user email.
                    default: "https://www.imdb.com/title/tt0120201/"
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
    '''
    x = request.get_json()
    payload = Movie(None, '1', x['title'], x['genres'], x['year'],
                    x['minutes'], x['language'], x['actors'], x['director'], x['imdb'])
    movie_id = add_movie(payload)
    return jsonify({'id': movie_id})


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
    '''
    return jsonify(get_all_movies())


@movies.route('/', methods=['GET'])
def read():
    '''Movie read endpoint
    ---
    parameters:
        - name: id
          in: query
          type: int
          required: true
    definitions:
        Movie:
            type: object
            properties:
                id:
                    type: string
                title:
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
    '''
    movie_id = request.args.get('id')
    return jsonify(get_movie(movie_id))


@movies.route('/', methods=['PUT'])
@authorize
def update(jwt_info):
    '''Movie update endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: id
          in: query
          type: int
          required: true
        - name: Movie
          in: body
          required: true
          schema:
            $ref: '#/definitions/Movie'
    definitions:
        Movie:
            type: object
            properties:
                title:
                    type: string
                    description: The movie title.
                    default: "Starship Troopers"
                genres:
                    type: string
                    description: The movie genres.
                    default: "Action, Sci-Fi, War"
                year:
                    type: string
                    description: The movie year.
                    default: "1997"
                minutes:
                    type: string
                    description: The movie runtime in minutes.
                    default: "129"
                language:
                    type: string
                    description: The movie language.
                    default: "English"
                actors:
                    type: string
                    description: The movie top billed actors.
                    default: "Casper Van Dien, Denise Richards"
                director:
                    type: string
                    description: The movie director.
                    default: "Paul Verhoeven"
                imdb:
                    type: string
                    description: The user email.
                    default: "https://www.imdb.com/title/tt0120201/"
    responses:
        200:
            description: Movie information
            schema:
                $ref: '#/definitions/Movie'
        400:
            description: Unable to update movie
            schema:
                properties:
                    error:
                        type: string
    '''
    movie_id = request.args.get('id')
    x = request.get_json()
    payload = Movie(movie_id, '1', x['title'], x['genres'], x['year'],
                    x['minutes'], x['language'], x['actors'], x['director'], x['imdb'])
    res = update_movie(payload)
    if res == 0:
        return jsonify(payload.as_dict())
    return error(res)


@movies.route('/', methods=['DELETE'])
@authorize
def delete(jwt_info):
    '''Movie delete endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: id
          in: query
          type: int
          required: true
    responses:
        200:
            description: Movie removed
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to remove movie
            schema:
                properties:
                    error:
                        type: string
    '''
    movie_id = request.args.get('id')
    res = delete_movie(movie_id)
    if res == 0:
        return success('movie removed.')
    return error(res)
