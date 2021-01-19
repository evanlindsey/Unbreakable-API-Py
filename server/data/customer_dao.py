from flask import g
from datetime import datetime

from ..models.customer_model import Customer
from ..common.db_connect import sql_command, sql_select


def add_customer(customer):
    '''Add a row to the customers table using the given information.

    Args:
        customer: Customer class object.

    Returns:
        int: The return value. Customer ID if successful. -1 if error.
    '''
    query = ('INSERT INTO customers (first, last, email, address, city, state, zip, phone, modified_by, modified_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
    data = (customer.first, customer.last, customer.email, customer.address,
            customer.city, customer.state, customer.zip, customer.phone, g.id, datetime.now())
    try:
        return sql_command(query, data)
    except:
        return -1
    return -1


def get_all_customers():
    '''Retrieve all customers from the all_customers view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_customers;'
    data = ()
    res = None
    try:
        res = sql_select(query, data)
    except:
        return -1
    if len(res) > 0:
        return [Customer(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]).as_dict() for x in res]
    return -1


def get_customer(customer_id):
    '''Retrieve the customer from the all_customers view matching the target ID.

    Args:
        customer_id: Target customer ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = 'SELECT * FROM all_customers WHERE id = %s;'
    data = (customer_id,)
    try:
        res = sql_select(query, data)
        if len(res) == 1:
            x = res[0]
            return Customer(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]).as_dict()
        return -1
    except:
        return -1


def update_customer(customer):
    '''Update the data fields for the row of the customers table that matches the customer ID.

    Args:
        customer: Customer class object.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_customer(customer.id)
    if res != -1:
        query = ('UPDATE customers SET first = %s, last = %s, email = %s, address = %s, city = %s, state = %s, zip = %s, phone = %s, modified_by = %s, modified_on = %s WHERE id = %s;')
        data = (customer.first, customer.last, customer.email, customer.address, customer.city,
                customer.state, customer.zip, customer.phone, g.id, datetime.now(), customer.id)
    else:
        return -1
    try:
        return sql_command(query, data)
    except:
        return -1


def delete_customer(customer_id):
    '''Delete the row from the customers table that matches the target ID.

    Args:
        customer_id: Target customer ID.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_customer(customer_id)
    if res != -1:
        query = ('DELETE FROM customers WHERE id = %s;')
        data = (customer_id,)
        try:
            return sql_command(query, data)
        except:
            return -1
    return -1
