import json
import datetime
import boto3


def endpoint(event, context):
    source_ddb = boto3.client('dynamodb','us-east-1')
    destination_ddb = boto3.client('dynamodb','us-west-1')
    sync_ddb_table(event['source_db'], event['dest_db'])
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, the current time is " + str(current_time)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def sync_ddb_table(source_ddb, destination_ddb):
    response = source_ddb.scan(TableName='table1')
    for item in response['Items']:
        destination_ddb.put_item(TableName='table2', Item=item)
