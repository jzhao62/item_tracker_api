import boto3
from botocore.exceptions import ClientError


def create_item(title, description=None, link=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('leetcode_tracker_dev')
    response = table.put_item(
        Item={
            'title': title,
            'info': {
                'description': description,
                'link': link
            }
        }
    )
    return response.get('item')


def delete_item_by_title(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('leetcode_tracker_dev')

    try:
        response = table.delete_item(
            Key={
                'title': title
            },
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response.get('item')


def get_all_items(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('leetcode_tracker_dev')
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
