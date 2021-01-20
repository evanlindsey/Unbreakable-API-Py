from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize
from ..models.rental_model import NewRental, ReturnInfo
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
        - name: NewRental
          in: body
          required: true
          schema:
            $ref: '#/definitions/NewRental'
    definitions:
        NewRental:
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
        400:
            description: Unable to return rental
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = NewRental(x['customer_id'], x['inventory_ids'], None)
    rental_id = add_rental(payload)
    if rental_id is not None and rental_id != -1:
        return jsonify({'id': rental_id})
    return error('unable to rent movie(s).')


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
        400:
            description: Unable to retrieve current rentals
            schema:
                properties:
                    error:
                        type: string
    '''
    rentals = get_all_current_rentals()
    if rentals != -1:
        return jsonify(rentals)
    return error('unable to retrieve current rentals.')


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
        400:
            description: Unable to retrieve rental
            schema:
                properties:
                    error:
                        type: string
    '''
    rental_id = request.args.get('id')
    if rental_id is None or rental_id == 'null' or rental_id == 'undefined':
        return error('rental id was not provided.')
    rental = get_current_rental(rental_id)
    if rental != -1:
        return jsonify(rental)
    return error('unable to retrieve rental.')


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
        - name: ReturnInfo
          in: body
          required: true
          schema:
            $ref: '#/definitions/ReturnInfo'
    definitions:
        ReturnInfo:
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
    payload = ReturnInfo(x['id'], x['customer_id'],
                         x['movie_ids'], x['ratings'])
    res = return_rentals(payload)
    if res is not None and res != -1:
        return success('rental returned.')
    return error('unable to return rental.')
