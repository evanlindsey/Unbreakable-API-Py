import json

from flask import g
from datetime import datetime

from ..common.db_connect import sql_command, sql_select
from ..models.user_model import User
from ..auth.hash import get_salt, hash_password, check_password


def check_user(email):
    '''Retrieve the row from the users table that matches the email.

    Args:
        email: Target email.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = ('SELECT id, first, last, password FROM users WHERE email = %s;')
    data = (email,)
    return sql_select(query, data)


def auth_user(creds):
    '''Retrieve the given email from the users table and compare the passwords.

    Args:
        creds: Creds class object.

    Returns:
        int: The return value. User class object if successful.
    '''
    res = check_user(creds.email)
    if len(res) == 1:
        res = res[0]
        data = json.loads(res['password'])
        salt = data['salt']
        hashed = data['hash']
        if check_password(creds.password, hashed, salt):
            query = ('UPDATE users SET last_login = %s WHERE id = %s;')
            data = (datetime.now(), res['id'])
            sql_command(query, data)
            return User(res['id'], res['first'], res['last']).as_dict()
    return -1


def set_role(user_id, user_role='employee'):
    '''Set the role for the user that matches the target ID.

    Args:
        user_id: Target user ID.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('UPDATE users SET role = %s WHERE id = %s;')
    data = (user_role, user_id)
    return sql_command(query, data)


def get_role(user_id):
    '''Retrieve the role for the user that matches the target ID.

    Args:
        user_id: Target user ID.

    Returns:
        string: The return value. User role if successful.
    '''
    query = ('SELECT role FROM users WHERE id = %s;')
    data = (user_id,)
    return sql_select(query, data)[0]


def add_user(creds):
    '''Add a row to the users table using the given information.

    Args:
        creds: Creds class object.

    Returns:
        boolean: The return value. User class object if successful.
    '''
    query = (
        'INSERT INTO users (email, password, modified_by, modified_on) VALUES (%s, %s, %s, %s);')
    salt = get_salt()
    hashed = hash_password(creds.password, salt)
    password = json.dumps({'salt': salt, 'hash': hashed})
    data = (creds.email, password, g.id, datetime.now())
    return sql_command(query, data)
