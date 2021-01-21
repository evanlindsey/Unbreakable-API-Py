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
    '''
    x = request.get_json()
    payload = Movie(None, x['category'], x['title'], x['genres'], x['year'],
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
        - name: Movie
          in: body
          required: true
          schema:
            $ref: '#/definitions/Movie'
    definitions:
        Movie:
            type: object
            properties:
                id:
                    type: string
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
    x = request.get_json()
    payload = Movie(x['id'], x['category'], x['title'], x['genres'], x['year'],
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
          type: string
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
