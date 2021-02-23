import boto3
import json
import time
import decimal

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


def get_resource():
    with open('certs.txt') as certs:
        keys = certs.readlines()

    lines = []
    for line in keys:
        key = line.strip()
        lines.append(key)

    return boto3.resource('dynamodb', aws_access_key_id=lines[0],
                              aws_secret_access_key=lines[1],
                              region_name='eu-north-1')


def create_device_table(dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.create_table(
        TableName = 'Devices',
        KeySchema = [
            {
                'AttributeName': 'timestamp',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'devicename',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'devicename',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    return table


def store_devices(users, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('Devices')
    for user in users:
        print(user)
        table.put_item(Item=user)


def get_device_by_name(name, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('Devices')
    try:
        response = table.query(KeyConditionExpression=Key('devicename').eq(name))
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']


def store_device_entry(tableName, name, position, currentStatus, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

        timeStamp = decimal.Decimal(time.time())

    table = dynamodb.Table(tableName)

    response = table.put_item(Item={
            'timestamp': timeStamp,
            'devicename': name,
            'info': {
                'position': position,
                'status': currentStatus
            }
        })

    return response


def get_all_devices(tableName, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table(tableName)

    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']
