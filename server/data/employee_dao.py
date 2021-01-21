from flask import g
from datetime import datetime

from ..common.db_connect import sql_command, sql_select


def get_all_employees():
    '''Retrieve all employees from the all_employees view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_employees;'
    data = ()
    return sql_select(query, data)


def get_employee(employee_id):
    '''Retrieve the employee from the all_employees view matching the target ID.

    Args:
        employee_id: Target employee ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = f'SELECT * FROM all_employees WHERE id = {employee_id};'
    data = ()
    return sql_select(query, data)


def update_employee(employee):
    '''Update the data fields for the row of the employees table that matches the employee ID.

    Args:
        employee: Employee class object.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('UPDATE users SET email = %s, role = %s, first = %s, last = %s, address = %s, city = %s, state = %s, zip = %s, phone = %s, modified_by = %s, modified_on = %s WHERE id = %s;')
    data = (employee.email, employee.role, employee.first, employee.last, employee.address,
            employee.city, employee.state, employee.zip, employee.phone, g.id, datetime.now(), employee.id)
    return sql_command(query, data)


def delete_employee(employee_id):
    '''Delete the row from the users table that matches the target ID.

    Args:
        employee_id: Target employee ID.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('DELETE FROM users WHERE id = %s;')
    data = (employee_id,)
    return sql_command(query, data)
