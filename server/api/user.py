from flask import Blueprint, request, jsonify

from ..common.responses import success, auth_error
from ..auth.jwt import authorize, encode_jwt
from ..models.user_model import User, Creds
from ..data.user_dao import add_user, auth_user, get_role, set_role

user = Blueprint('user', __name__, url_prefix='/api/user')


@user.route('/', methods=['POST'])
def create():
    '''User create endpoint
    ---
    parameters:
        - name: Creds
          in: body
          required: true
          schema:
            $ref: '#/definitions/Creds'
    definitions:
        Creds:
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
        User:
            type: object
            properties:
                info:
                    type: object
                    properties:
                        id:
                            type: string
                        first:
                            type: string
                        last:
                            type: string
                token:
                    type: string
    responses:
        200:
            description: JWT access token and user information
            schema:
                $ref: '#/definitions/User'
        401:
            description: Unable to create user
            schema:
                properties:
                    auth_error:
                        type: string
    '''
    x = request.get_json()
    payload = Creds(x['email'], x['password'])
    user_role = 'employee'
    user_id = add_user(payload)
    set_role(user_id, user_role)
    user = auth_user(payload)
    user['token'] = encode_jwt({'id': user_id, 'role': user_role})
    return jsonify(user)


@user.route('/auth', methods=['POST'])
def auth():
    '''User authentication endpoint
    ---
    parameters:
        - name: Creds
          in: body
          required: true
          schema:
            $ref: '#/definitions/Creds'
    definitions:
        Creds:
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
        User:
            type: object
            properties:
                info:
                    type: object
                    properties:
                        id:
                            type: string
                        first:
                            type: string
                        last:
                            type: string
                token:
                    type: string
    responses:
        200:
            description: JWT access token and user information
            schema:
                $ref: '#/definitions/User'
        401:
            description: Unable to authenticate user
            schema:
                properties:
                    auth_error:
                        type: string
    '''
    x = request.get_json()
    payload = Creds(x['email'], x['password'])
    user = auth_user(payload)
    if user is None or user == -1:
        return auth_error('unable to authenticate user.')
    user_id = user['info']['id']
    user_role = get_role(user_id)['role']
    user['token'] = encode_jwt({'id': user_id, 'role': user_role})
    return jsonify(user)


@user.route('/self/role', methods=['GET'])
@authorize
def self_role(jwt_info):
    '''User role endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
    responses:
        200:
            description: User Role
            schema:
                properties:
                    UserRole:
                        type: object
                        properties:
                            role:
                                type: string
        401:
            description: Unable to retrieve user
            schema:
                properties:
                    auth_error:
                        type: string
    '''
    try:
        return jsonify({'role': jwt_info['role']})
    except:
        return auth_error('unable to get user role.')


@user.route('/self/id', methods=['GET'])
@authorize
def self_id(jwt_info):
    '''User ID endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
    responses:
        200:
            description: User ID
            schema:
                properties:
                    UserID:
                        type: object
                        properties:
                            id:
                                type: string
        401:
            description: Unable to retrieve user
            schema:
                properties:
                    auth_error:
                        type: string
    '''
    try:
        return jsonify({'id': jwt_info['id']})
    except:
        return auth_error('unable to get user ID.')
