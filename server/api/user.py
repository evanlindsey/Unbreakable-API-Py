from flask import Blueprint, request, jsonify

from ..common.responses import success, auth_error
from ..auth.jwt import authorize, encode_jwt
from ..models.user_model import User, Creds
from ..data.user_dao import auth_user, get_role

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


@user.route('/self/role', methods=['GET'])
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
def read(jwt_info):
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
