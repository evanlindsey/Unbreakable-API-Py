from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize, admin_only
from ..models.employee_model import Employee
from ..models.user_model import Creds
from ..data.employee_dao import get_all_employees, get_employee, update_employee, delete_employee
from ..data.user_dao import add_user

employees = Blueprint('employees', __name__, url_prefix='/api/employees')


@employees.route('/', methods=['POST'])
@authorize
@admin_only
def create(jwt_info):
    '''Employee create endpoint (restricted to admins)
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
                password:
                    type: string
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
        400:
            description: Unable to create employee
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = Creds(x['email'], x['password'])
    user_id = add_user(payload)
    if user_id is None or user_id == -1:
        return error('unable to create employee.')
    payload = Employee(user_id, x['email'], x['role'], x['first'], x['last'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    res = update_employee(payload)
    if res is not None and res != -1:
        return jsonify({'id': user_id})
    return error('unable to create employee.')


@employees.route('/all', methods=['GET'])
def read_all():
    '''All employees read endpoint
    ---
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
        400:
            description: Unable to retrieve employees
            schema:
                properties:
                    error:
                        type: string
    '''
    employees = get_all_employees()
    if employees != -1:
        return jsonify(employees)
    return error('unable to retrieve employees.')


@employees.route('/', methods=['GET'])
def read():
    '''Employee read endpoint
    ---
    parameters:
        - name: id
          in: query
          type: string
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
        400:
            description: Unable to retrieve employee
            schema:
                properties:
                    error:
                        type: string
    '''
    employee_id = request.args.get('id')
    if employee_id is None or employee_id == 'null' or employee_id == 'undefined':
        return error('employee id was not provided.')
    employee = get_employee(employee_id)
    if employee != -1:
        return jsonify(employee)
    return error('unable to retrieve employee.')


@employees.route('/', methods=['PUT'])
@authorize
@admin_only
def update(jwt_info):
    '''Employee update endpoint (restricted to admins)
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
    x = request.get_json()
    payload = Employee(x['id'], x['email'], x['role'], x['first'], x['last'],
                       x['address'], x['city'], x['state'], x['zip'], x['phone'])
    res = update_employee(payload)
    if res is not None and res != -1:
        return jsonify(payload.as_dict())
    return error('unable to update employee.')


@employees.route('/', methods=['DELETE'])
@authorize
@admin_only
def delete(jwt_info):
    '''Employee delete endpoint (restricted to admins)
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
    if employee_id is None or employee_id == 'null' or employee_id == 'undefined':
        return error('employee id was not provided.')
    res = delete_employee(employee_id)
    if res is not None and res != -1:
        return success('employee removed.')
    return error('unable to remove employee.')