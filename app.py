import os

import boto3
from flask import Flask, jsonify, make_response

from botocore.exceptions import ClientError

app = Flask(__name__)

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


@app.route("/")
def echo():
    return "ECHO"


@app.route('/items', methods=['GET'])
def get_all_items():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('leetcode-tracker-prod')

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

    return jsonify(items)


@app.route('/items/<string:title>', methods=['GET'])
def get_item_by_title(title):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('leetcode-tracker-prod')
    try:
        response = table.delete_item(
            Key={
                'title': title
            },
        )
        item = response.get('item')

        if not item:
            return jsonify({'error': 'Could not find notes with provided "title"'}), 404

        return jsonify({
            'title': item.get('title').get('S'),
            'info': item.get('info')
        })


    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
