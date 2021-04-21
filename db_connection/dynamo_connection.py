from rest_framework.decorators import api_view
import psycopg2
import boto3
import sys
from boto3.dynamodb.conditions import Key, Attr
import json
import os
from os import environ


def Get_details(user_id, LastEvaluatedKey):
    aws_accesskey_id = os.getenv('aws_access_key_id')
    print(os.environ.get('aws_access_key_id'))
    env_dict = dict(environ)
    print(env_dict['aws_access_key_id'])

    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIATJCOVRZIUPERV3M3',
            aws_secret_access_key='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',
            region_name='ap-south-1',
        )
        dynamodbTable = dynamodb.Table('userinfo')

        last_key = dict()
        items = []

        if LastEvaluatedKey != '':
            last_key = json.loads(LastEvaluatedKey)

        if LastEvaluatedKey == '':
            response = dynamodbTable.query(
                KeyConditionExpression=Key('username').eq(user_id),
                # ScanIndexForward=False,
                Limit=2,
                ReturnConsumedCapacity='INDEXES'
            )
        else:
            lkey = dict()
            lkey['username'] = last_key['username']
            timestamp = last_key['timestamp'].replace("T", " ")
            lkey['timestamp'] = timestamp

            response = dynamodbTable.query(
                KeyConditionExpression=Key('username').eq(user_id),
                ScanIndexForward=False,
                Limit=3,
                ExclusiveStartKey=lkey
            )

        if 'LastEvaluatedKey' in response:
            LastEvaluatedKey = response['LastEvaluatedKey']
        else:
            LastEvaluatedKey = {
                'timestamp': '2021-01-19 12:12:13.562451', 'username': ''}

        if response['Count'] != 0:
            items = response['Items']
            items[0].update({'LastEvaluatedKey': LastEvaluatedKey})

        else:
            items.append({'liked': 'thor'})
            items[0].update({'caption': ''})
            items[0].update({'postpath': 'thor/34354'})
            items[0].update({'timestamp': '2021-01-21 09:12:12.800802'})
            items[0].update({'posttag': ''})
            items[0].update({'posttype': 'Image'})
            items[0].update({'posthashtag': ''})
            items[0].update({'username': 'man'})
            items[0].update({'post_location': ''})
            items[0].update({'LastEvaluatedKey': LastEvaluatedKey})

        '''for item in items:
                    size = sys.getsizeof(item)
                    print(size)'''

        return items

    except (Exception, psycopg2.Error) as error:
        print("Failed to send records", error)


def Get_like_comment(list_post):
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIATJCOVRZIUPERV3M3',
            aws_secret_access_key='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',
            region_name='ap-south-1',
        )
        dynamodbTable = dynamodb.Table('like_post')
        #exclusive_start_key = request_msg.get("exclusive_start_key")
        like_comment_list = []
        for post_id in list_post:
            response = dynamodbTable.query(
                KeyConditionExpression=Key('post_id').eq(post_id),
                ScanIndexForward=False,
                ProjectionExpression='#like, #comment_id',
                ExpressionAttributeNames={
                    '#like': 'like', '#comment_id': 'comment_id'},
                ReturnConsumedCapacity='TOTAL'
                #ExclusiveStartKey = exclusive_start_key
            )
            items = response['Items']
            like_comment_list.append(items)
            size = sys.getsizeof(items)
            print(size)
            print("Consumed Capacity",
                  response['ConsumedCapacity']['CapacityUnits'])
        #last_key = response['LastEvaluatedKey']
        '''for item in items:
                    size = sys.getsizeof(item)
                    print(size)'''

        return like_comment_list

    except (Exception, psycopg2.Error) as error:
        print("Failed to send records", error)
