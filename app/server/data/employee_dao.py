import mysql.connector
from flask import g
from datetime import datetime

from ..models.employee_model import Employee
from ..db_connect import sql_command, sql_select


def get_all_employees():
    '''Retrieve all employees from the all_employees view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_employees;'
    data = ()
    res = None
    try:
        res = sql_select(query, data)
    except:
        return -1
    if len(res) > 0:
        return [Employee(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]).as_dict() for x in res]
    return -1


def get_employee(employee_id):
    '''Retrieve the employee from the all_employees view matching the target ID.

    Args:
        employee_id: Target employee ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = 'SELECT * FROM all_employees WHERE id = %s;'
    data = (employee_id,)
    try:
        res = sql_select(query, data)
        if len(res) == 1:
            x = res[0]
            return Employee(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]).as_dict()
        return -1
    except:
        return -1


def update_employee(employee):
    '''Update the data fields for the row of the employees table that matches the employee ID.

    Args:
        employee: Employee class object.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_employee(employee.id)
    if res != -1:
        query = ('UPDATE users SET email = %s, role = %s, first = %s, last = %s, address = %s, city = %s, state = %s, zip = %s, phone = %s, modified_by = %s, modified_on = %s WHERE id = %s;')
        data = (employee.email, employee.role, employee.first, employee.last, employee.address,
                employee.city, employee.state, employee.zip, employee.phone, g.id, datetime.now(), employee.id)
    else:
        return -1
    try:
        return sql_command(query, data)
    except:
        return -1


def delete_employee(employee_id):
    '''Delete the row from the users table that matches the target ID.

    Args:
        employee_id: Target employee ID.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_employee(employee_id)
    if res != -1:
        query = ('DELETE FROM users WHERE id = %s;')
        data = (employee_id,)
        try:
            return sql_command(query, data)
        except:
            return -1
    return -1
