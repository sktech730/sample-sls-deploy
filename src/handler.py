import json
import datetime
import boto3


def endpoint(event, context):
    filepath = 'demo.tx'
    read_lines(filepath)
    source_ddb = boto3.client('dynamodb', 'us-east-1')
    destination_ddb = boto3.client('dynamodb', 'us-west-1')
    sync_ddb_table(source_ddb, destination_ddb)
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, the current time is " + str(current_time)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


# Code Showing AWS pagination Issue
def sync_ddb_table(srs_ddb, dest_ddb):
    response = srs_ddb.scan(TableName='table1')
    for item in response['Items']:
        dest_ddb.put_item(TableName='table2', Item=item)


# Resource leak Code
def read_lines(file):
    lines = []
    f = open(file, 'r')
    for line in f:
        lines.append(line.strip('\n').strip('\r\n'))
    return lines
