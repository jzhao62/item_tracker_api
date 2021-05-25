import os
import boto3
from flask import Flask, jsonify, make_response
from logger.logger import log
from config.settings import TABLE_NAME
from botocore.exceptions import ClientError
from flask import request
from leetcode_crud.crud import get_item_by_title, create_item, update_item, delete_item_by_title, get_all
from decimal import *

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

app = Flask(__name__)

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


@app.route('/items', methods=['GET'])
def fetch_all_items():
    items = get_all(dynamodb)
    return jsonify(items)


@app.route('/item', methods=['GET'])
def fetch_item_by_title():
    title = request.args.get('title')
    return jsonify(get_item_by_title(title, dynamodb))


@app.route('/item', methods=['POST'])
def post_item():
    title = request.get_json()["title"]
    details = request.get_json()["details"]

    return jsonify(create_item(title, details, dynamodb))


@app.route('/item', methods=['PUT'])
def put_item():
    title = request.get_json()["title"]
    details = request.get_json()["details"]

    return jsonify(update_item(title, details, dynamodb))


@app.route('/item', methods=["DELETE"])
def del_item():
    title = request.args.get('title')
    return jsonify(delete_item_by_title(title, dynamodb))


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
