from flask import g
from datetime import datetime

from ..common.db_connect import sql_command, sql_select


def add_inventory_item(inventory):
    '''Add a row to the inventory table using the given information.

    Args:
        inventory: Inventory class object.

    Returns:
        int: The return value. Inventory item ID if successful.
    '''
    query = (
        'INSERT INTO inventory (movie_id, upc, modified_by, modified_on) VALUES (%s, %s, %s, %s);')
    data = (inventory.movie_id, inventory.upc, g.id, datetime.now())
    return sql_command(query, data)


def get_available_inventory():
    '''Retrieve all available inventory from the available_inventory view.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM available_inventory;'
    data = ()
    return sql_select(query, data)


def get_inventory(inventory_id):
    '''Retrieve the inventory item from the all_inventory view matching the target ID.

    Args:
        inventory_id: Target inventory item ID.

    Returns:
        list: The return value. The row from the select statement.
    '''
    query = f'SELECT * FROM all_inventory WHERE id = {inventory_id};'
    data = ()
    return sql_select(query, data)


def delete_inventory(inventory_id):
    '''Delete the row from the inventory table that matches the inventory item ID.

    Args:
        inventory_id: Target inventory item ID.

    Returns:
        int: The return value. 0 if successful.
    '''
    query = ('DELETE FROM inventory WHERE id = %s;')
    data = (inventory_id,)
    return sql_command(query, data)
