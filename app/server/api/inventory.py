from flask import Blueprint, request, jsonify

from ..responses import success, error
from ..auth.jwt import authorize, admin_only
from ..models.inventory_model import Inventory
from ..data.inventory_dao import add_inventory_item, get_available_inventory, get_inventory, delete_inventory

inventory = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@inventory.route('/', methods=['POST'])
@authorize
@admin_only
def create(jwt_info):
    '''Inventory item create endpoint (restricted to admins)
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
                id:
                    type: string
                title:
                    type: string
                full:
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
            description: Inventory Item ID
            schema:
                properties:
                    InventoryItemID:
                        type: object
                        properties:
                            id:
                                type: string
        400:
            description: Unable to create inventory item
            schema:
                properties:
                    error:
                        type: string
    '''
    payload = request.get_json()
    item_id = add_inventory_item(payload['movie_id'], payload['upc'])
    if item_id is not None and item_id != -1:
        return jsonify({'id': item_id})
    return error('unable to create inventory item.')


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
                full:
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
        400:
            description: Unable to retrieve inventory
            schema:
                properties:
                    error:
                        type: string
    '''
    inventory = get_available_inventory()
    if inventory != -1:
        return jsonify(inventory)
    return error('unable to retrieve inventory.')


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
                full:
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
        400:
            description: Unable to retrieve inventory item
            schema:
                properties:
                    error:
                        type: string
    '''
    inventory_id = request.args.get('id')
    if inventory_id is None or inventory_id == 'null' or inventory_id == 'undefined':
        return error('inventory item id was not provided.')
    item = get_inventory(inventory_id)
    if item != -1:
        return jsonify(item)
    return error('unable to retrieve inventory item.')


@inventory.route('/', methods=['DELETE'])
@authorize
@admin_only
def delete(jwt_info):
    '''Inventory item delete endpoint (restricted to admins)
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
    if inventory_id is None or inventory_id == 'null' or inventory_id == 'undefined':
        return error('inventory item id was not provided.')
    res = delete_inventory(inventory_id)
    if res is not None and res != -1:
        return success('inventory item removed.')
    return error('unable to remove inventory item.')
