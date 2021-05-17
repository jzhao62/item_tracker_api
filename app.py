import os
import boto3
from flask import Flask, jsonify, make_response
from logger.logger import log
from config.settings import TABLE_NAME
from botocore.exceptions import ClientError
from flask import request
from leetcode_crud.crud import get_movie
from decimal import *
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

app = Flask(__name__)

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


@app.route("/")
def echo():
    return "ECHO"


@app.route('/items', methods=['GET'])
def get_item_by_title():
    title = request.args.get('title')
    year = Decimal(request.args.get('year'))
    try:
        if title or year:
            return jsonify(get_movie(title, year, dynamodb))
        else:
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
                log(response, "get_all_items")

            return jsonify(items)

    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
