import boto3
from botocore.exceptions import ClientError
from config.settings import TABLE_NAME, REGION
import time
import calendar
from decimal import *
import uuid

ts = Decimal(calendar.timegm(time.gmtime()))


def create_item(title, details, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'time_created': ts,
            'item_title': title,
            'detail': details
        }
    )
    return response


def get_all_items(dynamodb=None):
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


def get_item_by_id(item_id, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table(TABLE_NAME)
    try:
        response = table.get_item(Key={'id': item_id})

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response: return response['Item']
        return []


def update_item(item_id, title, details, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)

    response = table.update_item(
        Key={
            'id': item_id,
        },
        UpdateExpression="set item_title=:t, detail=:d, time_created = :s",
        ExpressionAttributeValues={
            ':t': title,
            ':d': details,
            ':s': ts
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def delete_item_by_id(item_id, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(TABLE_NAME)

    try:
        response = table.delete_item(
            Key={'id': item_id},
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response
