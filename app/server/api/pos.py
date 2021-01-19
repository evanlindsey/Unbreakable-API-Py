from flask import Blueprint, request, jsonify

from ..responses import success, error
from ..auth.jwt import authorize
from ..models.pos_model import PaymentInfo
from ..data.pos_dao import get_late_fees, add_payment

pos = Blueprint('pos', __name__, url_prefix='/api/pos')


@pos.route('/payment', methods=['POST'])
@authorize
def create_payment(jwt_info):
    '''POS payment endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: PaymentInfo
          in: body
          required: true
          schema:
            $ref: '#/definitions/PaymentInfo'
    definitions:
        PaymentInfo:
            type: object
            properties:
                rental_id:
                    type: string
                payment_type:
                    type: string
                payment_amount:
                    type: string
                card_ending:
                    type: string
    responses:
        200:
            description: Payment received
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to receive payment
            schema:
                properties:
                    error:
                        type: string
    '''
    x = request.get_json()
    payload = PaymentInfo(x['rental_id'], x['payment_type'],
                          x['payment_amount'], x['card_ending'])
    res = add_payment(payload)
    if res is not None and res != -1:
        return success('payment received.')
    return error('unable to receive payment.')


@pos.route('/fees', methods=['GET'])
def get_fees():
    '''POS fees endpoint
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: true
    definitions:
        RentalFee:
            type: object
            properties:
                rental_id:
                    type: string
                customer_id:
                    type: string
                titles:
                    type: string
                fee:
                    type: string
                is_returned:
                    type: boolean
    responses:
        200:
            description: Rental fees matching target ID
            schema:
                $ref: '#/definitions/RentalFee'
        400:
            description: Unable to retrieve fees
            schema:
                properties:
                    error:
                        type: string
    '''
    customer_id = request.args.get('id')
    if customer_id is None or customer_id == 'null' or customer_id == 'undefined':
        return error('customer id was not provided.')
    fees = get_late_fees(customer_id)
    if fees != -1:
        return jsonify(fees)
    return error('unable to retrieve fees.')
