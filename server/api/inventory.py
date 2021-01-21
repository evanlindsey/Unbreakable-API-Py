from flask import Blueprint, request, jsonify

from ..common.responses import success, error
from ..auth.jwt import authorize
from ..models.inventory_model import Inventory
from ..data.inventory_dao import add_inventory_item, get_available_inventory, get_inventory, delete_inventory

inventory = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@inventory.route('/', methods=['POST'])
@authorize
def create(jwt_info):
    '''Inventory item create endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: Inventory
          in: body
          required: true
          schema:
            $ref: '#/definitions/Inventory'
    definitions:
        Inventory:
            type: object
            properties:
                movie_id:
                    type: string
                upc:
                    type: string
    responses:
        200:
            description: Inventory Item ID
            schema:
                properties:
                    InventoryItemID:
                        type: object
                        properties:
                            id:
                                type: string
    '''
    payload = request.get_json()
    item_id = add_inventory_item(payload['movie_id'], payload['upc'])
    return jsonify({'id': item_id})


@inventory.route('/all', methods=['GET'])
def read_all():
    '''All inventory read endpoint
    ---
    definitions:
        Inventory:
            type: object
            properties:
                id:
                    type: string
                title:
                    type: string
                movie_id:
                    type: string
                upc:
                    type: string
                charge:
                    type: string
                modified_on:
                    type: string
    responses:
        200:
            description: All inventory in the system
            schema:
                properties:
                    Inventory:
                        type: array
                        items:
                            schema:
                                id: Inventory
                                schema:
                                    $ref: '#/definitions/Inventory'
    '''
    return jsonify(get_available_inventory())


@inventory.route('/', methods=['GET'])
def read():
    '''Inventory item read endpoint
    ---
    parameters:
        - name: id
          in: query
          type: string
          required: true
    definitions:
        Inventory:
            type: object
            properties:
                id:
                    type: string
                title:
                    type: string
                movie_id:
                    type: string
                upc:
                    type: string
                charge:
                    type: string
                modified_on:
                    type: string
    responses:
        200:
            description: Inventory item information matching target ID
            schema:
                $ref: '#/definitions/Inventory'
    '''
    inventory_id = request.args.get('id')
    return jsonify(get_inventory(inventory_id))


@inventory.route('/', methods=['DELETE'])
@authorize
def delete(jwt_info):
    '''Inventory item delete endpoint
    ---
    parameters:
        - name: Authorization
          in: header
          type: string
          required: true
          description: Bearer < JWT >
        - name: id
          in: query
          type: string
          required: true
    responses:
        200:
            description: Inventory item removed
            schema:
                properties:
                    success:
                        type: string
        400:
            description: Unable to remove inventory item
            schema:
                properties:
                    error:
                        type: string
    '''
    inventory_id = request.args.get('id')
    res = delete_inventory(inventory_id)
    if res == 0:
        return success('inventory item removed.')
    return error('unable to remove inventory item.')
