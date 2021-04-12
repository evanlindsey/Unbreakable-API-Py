from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize
from ..models.employee_model import Employee
from ..models.user_model import Creds
from ..data.employee_dao import get_all_employees, get_employee, update_employee, delete_employee
from ..data.user_dao import add_user, set_role

employees = Blueprint('employees', __name__, url_prefix='/api/employees')


@employees.route('/', methods=['POST'])
@authorize
def create(jwt_info):
    '''Employee create endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: Employee
          in: body
          required: true
          schema:
            $ref: '#/definitions/Employee'
    definitions:
        Employee:
            type: object
            properties:
                email:
                    type: string
                    description: The user email.
                    default: "hello@world.com"
                password:
                    type: string
                    description: The user password.
                    default: "password123"
    responses:
        200:
            description: Employee ID
            schema:
                properties:
                    EmployeeID:
                        type: object
                        properties:
                            id:
                                type: string
    '''
    x = request.get_json()
    payload = Creds(x['email'], x['password'])
    user_id = add_user(payload)
    set_role(user_id)
    return jsonify({'id': user_id})


@employees.route('/all', methods=['GET'])
def read_all():
    '''All employees read endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
    definitions:
        Employee:
            type: object
            properties:
                id:
                    type: string
                email:
                    type: string
                role:
                    type: string
                first:
                    type: string
                last:
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
            description: All employees in the system
            schema:
                properties:
                    Employees:
                        type: array
                        items:
                            schema:
                                id: Employee
                                schema:
                                    $ref: '#/definitions/Employee'
    '''
    return jsonify(get_all_employees())


@employees.route('/', methods=['GET'])
def read():
    '''Employee read endpoint
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
    definitions:
        Employee:
            type: object
            properties:
                id:
                    type: string
                email:
                    type: string
                role:
                    type: string
                first:
                    type: string
                last:
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
            description: Employee information matching target ID
            schema:
                $ref: '#/definitions/Employee'
    '''
    employee_id = request.args.get('id')
    return jsonify(get_employee(employee_id))


@employees.route('/', methods=['PUT'])
@authorize
def update(jwt_info):
    '''Employee update endpoint
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
        - name: Employee
          in: body
          required: true
          schema:
            $ref: '#/definitions/Employee'
    definitions:
        Employee:
            type: object
            properties:
                email:
                    type: string
                    description: The user email.
                    default: "hello@world.com"
                first:
                    type: string
                    description: The user first name.
                    default: "Jan"
                last:
                    type: string
                    description: The user last name.
                    default: "Smith"
                address:
                    type: string
                    description: The user address.
                    default: "123 Test Ln"
                city:
                    type: string
                    description: The user city.
                    default: "San Francisco"
                state:
                    type: string
                    description: The user state.
                    default: "CA"
                zip:
                    type: string
                    description: The user zip.
                    default: "12345"
                phone:
                    type: string
                    description: The user phone.
                    default: "(123)456-7890)"
    responses:
        200:
            description: Employee information
            schema:
                $ref: '#/definitions/Employee'
        400:
            description: Unable to update employee
            schema:
                properties:
                    error:
                        type: string
    '''
    employee_id = request.args.get('id')
    x = request.get_json()
    payload = Employee(employee_id, x['email'], 'employee', x['first'], x['last'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    res = update_employee(payload)
    if res == 0:
        return jsonify(payload.as_dict())
    return error(res)


@employees.route('/', methods=['DELETE'])
@authorize
def delete(jwt_info):
    '''Employee delete endpoint
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
            description: Employee removed
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to remove employee
            schema:
                properties:
                    error:
                        type: string
    '''
    employee_id = request.args.get('id')
    res = delete_employee(employee_id)
    if res == 0:
        return success('employee removed.')
    return error(res)
