from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize
from ..models.rental_model import Rental, Return
from ..data.rental_dao import add_rental, return_rentals, get_all_current_rentals, get_current_rental

rentals = Blueprint('rentals', __name__, url_prefix='/api/rentals')


@rentals.route('/rent', methods=['POST'])
@authorize
def create_rental(jwt_info):
    '''Rental rent endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: Rental
          in: body
          required: true
          schema:
            $ref: '#/definitions/Rental'
    definitions:
        Rental:
            type: object
            properties:
                customer_id:
                    type: string
                inventory_ids:
                    type: string
    responses:
        200:
            description: Rental ID
            schema:
                properties:
                    RentalID:
                        type: object
                        properties:
                            id:
                                type: string
    '''
    x = request.get_json()
    payload = Rental(x['customer_id'], x['inventory_ids'], None)
    rental_id = add_rental(payload)
    return jsonify({'id': rental_id})


@rentals.route('/current/all', methods=['GET'])
def read_all_current():
    '''All current rentals read endpoint
    ---
    definitions:
        Rental:
            type: object
            properties:
                id:
                    type: string
                customer_name:
                    type: string
                customer_id:
                    type: string
                titles:
                    type: string
                movie_ids:
                    type: string
                rented_on:
                    type: string
                due_date:
                    type: string
    responses:
        200:
            description: Current rentals in the system
            schema:
                properties:
                    Rentals:
                        type: array
                        items:
                            schema:
                                id: Rental
                                schema:
                                    $ref: '#/definitions/Rental'
    '''
    return jsonify(get_all_current_rentals())


@rentals.route('/current', methods=['GET'])
def read_current():
    '''Current rental read endpoint
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: true
    definitions:
        Rental:
            type: object
            properties:
                id:
                    type: string
                customer_name:
                    type: string
                customer_id:
                    type: string
                titles:
                    type: string
                movie_ids:
                    type: string
                rented_on:
                    type: string
                due_date:
                    type: string
    responses:
        200:
            description: Rental information matching target ID
            schema:
                $ref: '#/definitions/Rental'
    '''
    rental_id = request.args.get('id')
    return jsonify(get_current_rental(rental_id))


@rentals.route('/return', methods=['POST'])
@authorize
def create_return(jwt_info):
    '''Rental return endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: Return
          in: body
          required: true
          schema:
            $ref: '#/definitions/Return'
    definitions:
        Return:
            type: object
            properties:
                id:
                    type: string
                customer_id:
                    type: string
                movie_ids:
                    type: string
                ratings:
                    type: string
    responses:
        200:
            description: Rental returned
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to return rental
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = Return(x['id'], x['customer_id'],
                         x['movie_ids'], x['ratings'])
    res = return_rentals(payload)
    if res == 0:
        return success('rental returned.')
    return error(res)
