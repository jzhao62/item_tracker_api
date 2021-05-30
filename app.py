import os
import boto3
from flask import Flask, jsonify, make_response
from config.settings import TABLE_NAME
from flask import request
from leetcode_crud.crud import get_item_by_id, create_item, update_item, delete_item_by_id

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

app = Flask(__name__)

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


@app.route('/', methods=['GET'])
def echo():
    return jsonify("server is alive")


@app.route('/items', methods=['GET'])
def _fetch_all_items():
    table = dynamodb.Table(TABLE_NAME)
    scan_kwargs = {}
    items = []
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        items = response.get('Items', [])
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    # items = get_all_items(dynamodb)
    return jsonify(items)


@app.route('/items/<item_id>', methods=['GET'])
def _fetch_by_id(item_id):
    return jsonify(get_item_by_id(item_id, dynamodb))


@app.route('/items/<item_id>', methods=['PUT'])
def _update_item(item_id):
    title = request.get_json()["title"]
    details = request.get_json()["details"]
    return jsonify(update_item(item_id, title, details, dynamodb))


@app.route('/items/<item_id>', methods=["DELETE"])
def del_item(item_id):
    title = request.args.get('title')
    return jsonify(delete_item_by_id(item_id, dynamodb))


@app.route('/items', methods=['POST'])
def _create_item():
    title = request.get_json()["title"]
    details = request.get_json()["details"]

    return jsonify(create_item(title, details, dynamodb))


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
