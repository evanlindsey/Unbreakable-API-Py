from flask import Blueprint, request, jsonify

from ..common.responses import success, error
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
                email:
                    type: string
                    description: The customer email.
                    default: "hello@world.com"
                first:
                    type: string
                    description: The customer first name.
                    default: "Jan"
                last:
                    type: string
                    description: The customer last name.
                    default: "Smith"
                address:
                    type: string
                    description: The customer address.
                    default: "123 Test Ln"
                city:
                    type: string
                    description: The customer city.
                    default: "San Francisco"
                state:
                    type: string
                    description: The customer state.
                    default: "CA"
                zip:
                    type: string
                    description: The customer zip.
                    default: "12345"
                phone:
                    type: string
                    description: The customer phone.
                    default: "(123)456-7890)"
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
    '''
    x = request.get_json()
    payload = Customer(None, x['first'], x['last'], x['email'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    customer_id = add_customer(payload)
    return jsonify({'id': customer_id})


@customers.route('/all', methods=['GET'])
def read_all():
    '''All customers read endpoint
    ---
    definitions:
        GetCustomer:
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
                                    $ref: '#/definitions/GetCustomer'
    '''
    return jsonify(get_all_customers())


@customers.route('/', methods=['GET'])
def read():
    '''Customer read endpoint
    ---
    parameters:
        - name: id
          in: query
          type: integer
          required: true
    definitions:
        GetCustomer:
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
                $ref: '#/definitions/GetCustomer'
    '''
    customer_id = request.args.get('id')
    return jsonify(get_customer(customer_id))


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
        - name: id
          in: query
          type: integer
          required: true
        - name: Customer
          in: body
          required: true
          schema:
            $ref: '#/definitions/Customer'
    definitions:
        Customer:
            type: object
            properties:
                email:
                    type: string
                    description: The customer email.
                    default: "hello@world.com"
                first:
                    type: string
                    description: The customer first name.
                    default: "Jan"
                last:
                    type: string
                    description: The customer last name.
                    default: "Smith"
                address:
                    type: string
                    description: The customer address.
                    default: "123 Test Ln"
                city:
                    type: string
                    description: The customer city.
                    default: "San Francisco"
                state:
                    type: string
                    description: The customer state.
                    default: "CA"
                zip:
                    type: string
                    description: The customer zip.
                    default: "12345"
                phone:
                    type: string
                    description: The customer phone.
                    default: "(123)456-7890)"
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
    customer_id = request.args.get('id')
    x = request.get_json()
    payload = Customer(customer_id, x['first'], x['last'], x['email'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    res = update_customer(payload)
    if res == 0:
        return jsonify(payload.as_dict())
    return error(res)


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
          type: integer
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
    res = delete_customer(customer_id)
    if res == 0:
        return success('customer removed.')
    return error(res)
