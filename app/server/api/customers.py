from flask import Blueprint, request, jsonify

from ..responses import success, error
from ..auth.jwt import authorize
from ..models.customer_model import Customer
from ..data.customer_dao import add_customer, get_all_customers, get_customer, update_customer, delete_customer

customers = Blueprint('customers', __name__, url_prefix='/api/customers')


@customers.route('/', methods=['POST'])
@authorize
def create(jwt_info):
    '''Customer create endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: Customer
          in: body
          required: true
          schema:
            $ref: '#/definitions/Customer'
    definitions:
        Customer:
            type: object
            properties:
                id:
                    type: string
                first:
                    type: string
                last:
                    type: string
                full:
                    type: string
                email:
                    type: string
                address:
                    type: string
                city:
                    type: string
                state:
                    type: string
                zip:
                    type: string
                phone:
                    type: string
    responses:
        200:
            description: Customer ID
            schema:
                properties:
                    CustomerID:
                        type: object
                        properties:
                            id:
                                type: string
        400:
            description: Unable to create customer
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = Customer(None, x['first'], x['last'], None, x['email'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    customer_id = add_customer(payload)
    if customer_id is not None and customer_id != -1:
        return jsonify({'id': customer_id})
    return error('unable to create customer.')


@customers.route('/all', methods=['GET'])
@authorize
def read_all(jwt_info):
    '''All customers read endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
    definitions:
        Customer:
            type: object
            properties:
                id:
                    type: string
                first:
                    type: string
                last:
                    type: string
                full:
                    type: string
                email:
                    type: string
                address:
                    type: string
                city:
                    type: string
                state:
                    type: string
                zip:
                    type: string
                phone:
                    type: string
    responses:
        200:
            description: All customers in the system
            schema:
                properties:
                    Customers:
                        type: array
                        items:
                            schema:
                                id: Customer
                                schema:
                                    $ref: '#/definitions/Customer'
        400:
            description: Unable to retrieve customers
            schema:
                properties:
                    error:
                        type: string
    '''
    customers = get_all_customers()
    if customers != -1:
        return jsonify(customers)
    return error('unable to retrieve customers.')


@customers.route('/', methods=['GET'])
@authorize
def read(jwt_info):
    '''Customer read endpoint
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
    definitions:
        Customer:
            type: object
            properties:
                id:
                    type: string
                first:
                    type: string
                last:
                    type: string
                full:
                    type: string
                email:
                    type: string
                address:
                    type: string
                city:
                    type: string
                state:
                    type: string
                zip:
                    type: string
                phone:
                    type: string
    responses:
        200:
            description: Customer information matching target ID
            schema:
                $ref: '#/definitions/Customer'
        400:
            description: Unable to retrieve customer
            schema:
                properties:
                    error:
                        type: string
    '''
    customer_id = request.args.get('id')
    if customer_id is None or customer_id == 'null' or customer_id == 'undefined':
        return error('customer id was not provided.')
    customer = get_customer(customer_id)
    if customer != -1:
        return jsonify(customer)
    return error('unable to retrieve customer.')


@customers.route('/', methods=['PUT'])
@authorize
def update(jwt_info):
    '''Customer update endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: Customer
          in: body
          required: true
          schema:
            $ref: '#/definitions/Customer'
    definitions:
        Customer:
            type: object
            properties:
                id:
                    type: string
                first:
                    type: string
                last:
                    type: string
                full:
                    type: string
                email:
                    type: string
                address:
                    type: string
                city:
                    type: string
                state:
                    type: string
                zip:
                    type: string
                phone:
                    type: string
    responses:
        200:
            description: Customer information
            schema:
                $ref: '#/definitions/Customer'
        400:
            description: Unable to update customer
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = Customer(x['id'], x['first'], x['last'], x['full'], x['email'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    res = update_customer(payload)
    if res is not None and res != -1:
        return jsonify(payload.as_dict())
    return error('unable to update customer.')


@customers.route('/', methods=['DELETE'])
@authorize
def delete(jwt_info):
    '''Customer delete endpoint
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
            description: Customer removed
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to remove customer
            schema:
                properties:
                    error:
                        type: string
    '''
    customer_id = request.args.get('id')
    if customer_id is None or customer_id == 'null' or customer_id == 'undefined':
        return error('customer id was not provided.')
    res = delete_customer(customer_id)
    if res is not None and res != -1:
        return success('customer removed.')
    return error('unable to remove customer.')
