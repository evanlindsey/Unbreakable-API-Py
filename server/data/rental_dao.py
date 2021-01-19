from flask import g
from datetime import datetime, timedelta

from ..models.rental_model import Rental, NewRental
from ..common.db_connect import sql_command, sql_select


def add_rental(new_rental):
    '''Add a row to the rentals table using the given information and add a row to the inventory_rentals for each inventory item

    Args:
        new_rental: PaymentInfo class object.

    Returns:
        int: The return value. Rental ID if successful. -1 if error.
    '''
    rental_id = None
    query = (
        'INSERT INTO rentals (customer_id, rented_by, rented_on, due_date) VALUES (%s, %s, %s, %s);')
    data = (new_rental.customer_id, g.id, datetime.now(),
            datetime.now() + timedelta(days=5))
    try:
        rental_id = sql_command(query, data)
    except:
        return -1
    inventory_ids = [x.strip() for x in new_rental.inventory_ids.split(',')]
    for inventory_id in inventory_ids:
        try:
            query = (
                'INSERT INTO inventory_rentals (inventory_id, rental_id) VALUES (%s, %s);')
            data = (inventory_id, rental_id)
            sql_command(query, data)
        except:
            return -1
    return rental_id


def get_all_current_rentals():
    '''Retrieves current rentals from the all_rentals view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM all_rentals WHERE ISNULL(returned_on);'
    data = ()
    try:
        res = sql_select(query, data)
        if len(res) > 0:
            return [Rental(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).as_dict() for x in res]
        return -1
    except:
        return -1


def get_current_rental(rental_id):
    '''Retrieve the current rental from the all_rentals view matching the target rental ID.

    Args:
        rental_id: Target rental ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = 'SELECT * FROM all_rentals WHERE ISNULL(returned_on) AND id = %s;'
    data = (rental_id,)
    try:
        res = sql_select(query, data)
        if len(res) == 1:
            x = res[0]
            return Rental(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).as_dict()
        return -1
    except:
        return -1


def return_rentals(return_info):
    '''Add a row to the ratings table using the given information and add a date to the returned_on column for the rental ID

    Args:
        return_info: ReturnInfo class object.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_current_rental(return_info.id)
    if res != -1:
        if return_info.movie_ids is not None and return_info.ratings is not None:
            movies = [x.strip() for x in return_info.movie_ids.split(',')]
            ratings = [x.strip() for x in return_info.ratings.split(',')]
            for i, movie in enumerate(movies):
                try:
                    query = (
                        'INSERT INTO ratings (rating, movie_id, customer_id) VALUES (%s, %s, %s);')
                    data = (ratings[i], movie, return_info.customer_id)
                    sql_command(query, data)
                except:
                    return -1
    else:
        return -1
    try:
        query = ('UPDATE rentals SET returned_on = %s WHERE id = %s;')
        data = (datetime.now(), return_info.id)
        return sql_command(query, data)
    except:
        return -1
