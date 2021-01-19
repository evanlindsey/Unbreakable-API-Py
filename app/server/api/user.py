from flask import Blueprint, request, jsonify

from ..responses import success, error, auth_error
from ..auth.jwt import authorize, encode_jwt
from ..models.user_model import User, Creds
from ..data.user_dao import auth_user, get_role, add_user, get_user, update_user, delete_user

user = Blueprint('user', __name__, url_prefix='/api/user')


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
                password:
                    type: string
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
    role = get_role(user_id)
    if role is not None and role != -1:
        user['token'] = encode_jwt({'id': user_id, 'role': role})
        return jsonify(user)
    return auth_error('unable to authenticate user.')


@user.route('/role', methods=['GET'])
@authorize
def role(jwt_info):
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
        400:
            description: Unable to retrieve user
            schema:
                properties:
                    error:
                        type: string
    '''
    try:
        return jsonify({'role': jwt_info['role']})
    except:
        return error('unable to get user role.')


@user.route('/', methods=['POST'])
@authorize
def create(jwt_info):
    '''User create endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
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
                password:
                    type: string
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
            description: User ID
            schema:
                properties:
                    UserID:
                        type: object
                        properties:
                            id:
                                type: string
        400:
            description: Unable to create user
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = Creds(x['email'], x['password'])
    user_id = add_user(payload)
    if user_id is not None and user_id != -1:
        return jsonify({'id': user_id})
    return error('unable to create user.')


@user.route('/', methods=['GET'])
@authorize
def read(jwt_info):
    '''User read endpoint
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
            description: User information matching target ID
            schema:
                $ref: '#/definitions/User'
        400:
            description: Unable to retrieve user
            schema:
                properties:
                    error:
                        type: string
    '''
    user_id = request.args.get('id')
    user = None
    if user_id is None or user_id == 'null' or user_id == 'undefined':
        user_id = jwt_info['id']
    user = get_user(user_id)
    if user is not None and user != -1:
        return jsonify(user)
    return error('unable to retrieve user.')


@user.route('/', methods=['PUT'])
@authorize
def update(jwt_info):
    '''User update endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: User
          in: body
          required: true
          schema:
            $ref: '#/definitions/User'
    definitions:
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
            description: User information
            schema:
                $ref: '#/definitions/User'
        400:
            description: Unable to update user
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()['info']
    payload = User(x['id'], x['first'], x['last'])
    res = update_user(payload)
    if res is not None and res != -1:
        return jsonify(payload.as_dict())
    return error('unable to update user.')


@user.route('/', methods=['DELETE'])
@authorize
def destroy(jwt_info):
    '''User delete endpoint
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
            description: User removed
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to remove user
            schema:
                properties:
                    error:
                        type: string
    '''
    user_id = request.args.get('id')
    if user_id is None or user_id == 'null' or user_id == 'undefined':
        return error('user id was not provided.')
    res = delete_user(user_id)
    if res is not None and res != -1:
        return success('user removed.')
    return error('unable to remove user.')