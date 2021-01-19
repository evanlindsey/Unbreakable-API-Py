import mysql.connector
import os


def sql_connect():
    '''Connect to the MySQL database using credentials from class properties.

    Returns:
        MySQLConnection: The return value. Object to perform MySQL actions on.
    '''
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PSWD'],
        database=os.environ['DB_DATA']
    )


def sql_command(query, data):
    '''Execute the given query against the MySQL connection.

    Args:
        query: Target query to execute.
        data: Variables to inject in the query.

    Returns:
        int: The return value. Row ID (auto-increment column) if insert. 0 if anything else.
    '''
    cnx = sql_connect()
    cursor = cnx.cursor()
    cursor.execute(query, data)
    row_id = cursor.lastrowid
    cnx.commit()
    cursor.close()
    cnx.close()
    return row_id


def sql_select(query, data):
    '''Execute the given select statement against the MySQL connection.

    Args:
        query: Target select statement to execute.
        data: Variables to inject in the select statement.

    Returns:
        list: The return value. Row results from the select statement.
    '''
    cnx = sql_connect()
    cursor = cnx.cursor()
    cursor.execute(query, data)
    res = [x for x in cursor.fetchall()]
    cursor.close()
    cnx.close()
    return res
