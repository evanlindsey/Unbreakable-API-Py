from flask import g
from datetime import datetime, timedelta

from ..common.db_connect import sql_command, sql_select


def add_rental(new_rental):
    '''Add a row to the rentals table using the given information and add a row to the inventory_rentals for each inventory item

    Args:
        new_rental: PaymentInfo class object.

    Returns:
        int: The return value. Rental ID if successful.
    '''
    query = (
        'INSERT INTO rentals (customer_id, rented_by, rented_on, due_date) VALUES (%s, %s, %s, %s);')
    data = (new_rental.customer_id, g.id, datetime.now(),
            datetime.now() + timedelta(days=5))
    rental_id = sql_command(query, data)

    inventory_ids = [x.strip() for x in new_rental.inventory_ids.split(',')]
    for inventory_id in inventory_ids:
        query = (
            'INSERT INTO inventory_rentals (inventory_id, rental_id) VALUES (%s, %s);')
        data = (inventory_id, rental_id)
        sql_command(query, data)

    return rental_id


def get_all_current_rentals():
    '''Retrieves current rentals from the all_rentals view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_rentals WHERE ISNULL(returned_on);'
    data = ()
    return sql_select(query, data)


def get_current_rental(rental_id):
    '''Retrieve the current rental from the all_rentals view matching the target rental ID.

    Args:
        rental_id: Target rental ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = 'SELECT * FROM all_rentals WHERE ISNULL(returned_on) AND id = %s;'
    data = (rental_id,)
    return sql_select(query, data)


def return_rentals(return_info):
    '''Add a date to the returned_on column for the rental ID

    Args:
        return_info: Return class object.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('UPDATE rentals SET returned_on = %s WHERE id = %s;')
    data = (datetime.now(), return_info.id)
    return sql_command(query, data)
