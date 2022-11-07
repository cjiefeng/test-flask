import pymysql
from flask import Blueprint, current_app, request

from internal.util import response
from internal.db import items

item_bp = Blueprint("example_bp", __name__)


@item_bp.route('/add_item', methods=['POST'])
def add_item():
    request_content = request.get_json()
    current_app.logger.info(request_content)
    item = request_content['item']
    quantity = request_content['quantity']
    try:
        items.add_item(item, quantity)
    except pymysql.Error as e:
        current_app.logger.error(e)
        return response.bad_response(e)
    return response.success_response({'message': 'ok'})


@item_bp.route('/get_all_items', methods=['GET'])
def get_all_items():
    try:
        res = items.get_all_items()
    except pymysql.Error as e:
        current_app.logger.error(e)
        return response.bad_response(e)
    return response.success_response(res)
