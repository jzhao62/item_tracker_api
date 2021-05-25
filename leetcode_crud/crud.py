import boto3
from botocore.exceptions import ClientError
from config.settings import TABLE_NAME, REGION
import time
import calendar
from decimal import *

ts = Decimal(calendar.timegm(time.gmtime()))


def create_item(title, details, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            'time_created': ts,
            'item_title': title,
            'detail': details
        }
    )
    return response


def get_all(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
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
    return items


def get_item_by_title(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table(TABLE_NAME)
    try:
        response = table.get_item(
            Key={
                'item_title': title
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response: return response['Item']
        return []


def update_item(title, details, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)

    response = table.update_item(
        Key={
            'item_title': title
        },
        UpdateExpression="set detail=:d, time_created = :s",
        ExpressionAttributeValues={
            ':d': details,
            ':s': ts
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def delete_item_by_title(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)

    try:
        response = table.delete_item(
            Key={'item_title': title},
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response
