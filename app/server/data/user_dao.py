import json
import mysql.connector
from flask import g
from datetime import datetime

from ..db_connect import sql_command, sql_select
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
    try:
        return sql_select(query, data)
    except:
        return -1


def auth_user(creds):
    '''Retrieve the given email from the users table and compare the passwords.

    Args:
        creds: Creds class object.

    Returns:
        int: The return value. User class object if successful. -1 if error.
    '''
    res = check_user(creds.email)
    if res != -1 and len(res) == 1:
        data = json.loads(res[0][3])
        salt = data['salt']
        hashed = data['hash']
        if check_password(creds.password, hashed, salt):
            user_id = res[0][0]
            first = res[0][1]
            last = res[0][2]
            query = ('UPDATE users SET last_login = %s WHERE id = %s;')
            data = (datetime.now(), user_id)
            try:
                sql_command(query, data)
            except:
                return -1
            return User(user_id, first, last).as_dict()
    return -1


def get_role(user_id):
    '''Retrieve the role for the user that matches the target ID.

    Args:
        user_id: Target user ID.

    Returns:
        string: The return value. User role if successful. -1 if error.
    '''
    query = ('SELECT role FROM users WHERE id = %s;')
    data = (user_id,)
    res = None
    try:
        res = sql_select(query, data)
    except:
        return -1
    if len(res) == 1:
        role = res[0][0]
        return role
    return -1


def add_user(creds):
    '''Add a row to the users table using the given information.

    Args:
        creds: Creds class object.

    Returns:
        boolean: The return value. User class object if successful. -1 if error.
    '''
    res = check_user(creds.email)
    if res != -1 and len(res) == 0:
        query = (
            'INSERT INTO users (email, password, modified_by, modified_on) VALUES (%s, %s, %s, %s);')
        salt = get_salt()
        hashed = hash_password(creds.password, salt)
        password = json.dumps({'salt': salt, 'hash': hashed})
        data = (creds.email, password, None, datetime.now())
        try:
            return sql_command(query, data)
        except:
            return -1
    return -1


def get_user(user_id):
    '''Retrieve the row from the users table that matches the target ID.

    Args:
        user_id: Target user ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = ('SELECT first, last FROM users WHERE id = %s;')
    data = (user_id,)
    res = None
    try:
        res = sql_select(query, data)
    except:
        return -1
    if len(res) == 1:
        first = res[0][0]
        last = res[0][1]
        return User(user_id, first, last).as_dict()
    return -1


def update_user(user):
    '''Update the data fields for the row of the users table that matches the user ID.

    Args:
        user: User class object.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    user = user.info
    res = get_user(user.id)
    if res != -1:
        query = (
            'UPDATE users SET first = %s, last = %s, modified_by = %s, modified_on = %s WHERE id = %s;')
        data = (user.first, user.last, g.id, datetime.now(), user.id)
    else:
        return -1
    try:
        return sql_command(query, data)
    except:
        return -1


def delete_user(user_id):
    '''Delete the row from the users table that matches the target ID.

    Args:
        user_id: Target user ID.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_user(user_id)
    if res != -1:
        query = ('DELETE FROM users WHERE id = %s;')
        data = (user_id,)
        try:
            return sql_command(query, data)
        except:
            return -1
    return -1
