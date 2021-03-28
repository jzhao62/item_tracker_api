import os

import boto3
from flask import Flask, jsonify, make_response
from config.settings import USERS_TABLE
from leetcode_crud.crud import get_all_items

app = Flask(__name__)

dynamodb_resource = boto3.resource('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


@app.route("/")
def echo():
    return "ECHO"


@app.route('/items')
def get_all_items():
    item = get_all_items(dynamodb_resource)
    return jsonify(item)


@app.route('/items/<string:title>')
def get_item_by_title(title):
    item = get_item_by_title(title, dynamodb_resource)

    if not item:
        return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    return jsonify({
        'title': item.get('title').get('S'),
        'info': item.get('info')
    })

@app.route('/')


@app.route('/users/<string:user_id>')
def get_user(user_id):
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    return jsonify(
        {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    )


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
