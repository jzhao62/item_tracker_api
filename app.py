import os

from flask import Flask, jsonify, make_response
from flask import request

from leetcode_crud.crud import *
from logger.logger import *

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

app = Flask(__name__)

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


@app.route('/', methods=['GET'])
def echo():
    log(TABLE_NAME, "ECHO")
    return jsonify(TABLE_NAME)


@app.route('/items', methods=['GET'])
def _fetch_all_items():
    items = get_all_items(dynamodb)
    return jsonify(items)


@app.route('/items/<item_id>', methods=['GET'])
def _fetch_by_id(item_id):
    return jsonify(get_item_by_id(item_id, dynamodb))


@app.route('/items/<item_id>', methods=['PUT'])
def _update_item(item_id):
    title = request.get_json()["title"]
    detail = request.get_json()["detail"]
    return jsonify(update_item(item_id, title, detail, dynamodb))


@app.route('/items/<item_id>', methods=["DELETE"])
def del_item(item_id):
    title = request.args.get('title')
    return jsonify(delete_item_by_id(item_id, dynamodb))


@app.route('/items', methods=['POST'])
def _create_item():
    title = request.get_json()["title"]
    detail = request.get_json()["detail"]

    return jsonify(create_item(title, detail, dynamodb))


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
