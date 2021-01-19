from ..models.pos_model import RentalFee, PaymentInfo
from ..common.db_connect import sql_command, sql_select


def add_payment(payment_info):
    '''Add a row to the payments table using the given information.

    Args:
        payment_info: PaymentInfo class object.

    Returns:
        int: The return value. Payment ID if successful. -1 if error.
    '''
    query = (
        'INSERT INTO payments (rental_id, type, amount, card_ending) VALUES (%s, %s, %s, %s);')
    data = (payment_info.rental_id, payment_info.payment_type,
            payment_info.payment_amount, payment_info.card_ending)
    try:
        return sql_command(query, data)
    except:
        return -1
    return -1


def get_late_fees(customer_id):
    '''Retrieve all late fees from the rental_fee_details view matching the target customer ID.

    Args:
        customer_id: Target customer ID.

    Returns:
        list: The return value. All rows from the select statement.
    '''
    query = 'SELECT * FROM rental_fee_details WHERE customer_id = %s AND fee != 0;'
    data = (customer_id,)
    try:
        res = sql_select(query, data)
        if len(res) > 0:
            return [RentalFee(x[0], x[1], x[2], x[3], x[4]).as_dict() for x in res]
        return [RentalFee(0, 0, 'No current fees', 0, False).as_dict()]
    except:
        return -1
