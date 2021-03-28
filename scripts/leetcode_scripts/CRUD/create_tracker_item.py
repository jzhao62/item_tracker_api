from pprint import pprint
import boto3


def create_tracker_item(title, description=None, link=None, dynamodb=None):
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
    return response


if __name__ == '__main__':
    tracker_resp = create_tracker_item("Sample Question_3", "Description for Sample 1232141")
    print("Add tracker succeed")
    pprint(tracker_resp, sort_dicts=False)
