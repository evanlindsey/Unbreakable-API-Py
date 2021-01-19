import mysql.connector
from flask import g
from datetime import datetime

from ..models.inventory_model import Inventory
from ..db_connect import sql_command, sql_select


def add_inventory_item(movie_id, upc):
    '''Add a row to the inventory table using the given information.

    Args:
        movie_id: Target movie ID.
        upc: UPC number for new inventory item.

    Returns:
        int: The return value. Inventory item ID if successful. -1 if error.
    '''
    query = (
        'INSERT INTO inventory (movie_id, upc, modified_by, modified_on) VALUES (%s, %s, %s, %s);')
    data = (movie_id, upc, g.id, datetime.now())
    try:
        return sql_command(query, data)
    except:
        return -1
    return -1


def get_available_inventory():
    '''Retrieve all available inventory from the available_inventory view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM available_inventory;'
    data = ()
    try:
        res = sql_select(query, data)
        if len(res) > 0:
            return [Inventory(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).as_dict() for x in res]
        return -1
    except:
        return -1


def get_inventory(inventory_id):
    '''Retrieve the inventory item from the all_inventory view matching the target ID.

    Args:
        inventory_id: Target inventory item ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = 'SELECT * FROM all_inventory WHERE id = %s;'
    data = (inventory_id,)
    try:
        res = sql_select(query, data)
        if len(res) == 1:
            x = res[0]
            return Inventory(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).as_dict()
        return -1
    except:
        return -1


def delete_inventory(inventory_id):
    '''Delete the row from the inventory table that matches the inventory item ID.

    Args:
        inventory_id: Target inventory item ID.

    Returns:
        int: The return value. 0 if successful. -1 if error.
    '''
    res = get_inventory(inventory_id)
    if res != -1:
        query = ('DELETE FROM inventory WHERE id = %s;')
        data = (inventory_id,)
        try:
            return sql_command(query, data)
        except:
            return -1
    return -1
