from flask import g
from datetime import datetime

from ..common.db_connect import sql_command, sql_select


def add_customer(customer):
    '''Add a row to the customers table using the given information.

    Args:
        customer: Customer class object.

    Returns:
        int: The return value. Customer ID if successful.
    '''
    query = ('INSERT INTO customers (first, last, email, address, city, state, zip, phone, modified_by, modified_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
    data = (customer.first, customer.last, customer.email, customer.address,
            customer.city, customer.state, customer.zip, customer.phone, g.id, datetime.now())
    return sql_command(query, data)


def get_all_customers():
    '''Retrieve all customers from the all_customers view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_customers;'
    data = ()
    return sql_select(query, data)


def get_customer(customer_id):
    '''Retrieve the customer from the all_customers view matching the target ID.

    Args:
        customer_id: Target customer ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = f'SELECT * FROM all_customers WHERE id = {customer_id};'
    data = ()
    return sql_select(query, data)


def update_customer(customer):
    '''Update the data fields for the row of the customers table that matches the customer ID.

    Args:
        customer: Customer class object.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('UPDATE customers SET first = %s, last = %s, email = %s, address = %s, city = %s, state = %s, zip = %s, phone = %s, modified_by = %s, modified_on = %s WHERE id = %s;')
    data = (customer.first, customer.last, customer.email, customer.address, customer.city,
            customer.state, customer.zip, customer.phone, g.id, datetime.now(), customer.id)
    return sql_command(query, data)


def delete_customer(customer_id):
    '''Delete the row from the customers table that matches the target ID.

    Args:
        customer_id: Target customer ID.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('DELETE FROM customers WHERE id = %s;')
    data = (customer_id,)
    return sql_command(query, data)
