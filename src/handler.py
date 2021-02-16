import json
import datetime
import subprocess

import boto3


def endpoint(event, context):
    filepath = 'demo.tx'
    dict = {}
    dict_usage_with_try_except(dict)
    dict_usage_with_setdefault(dict)
    read_lines(filepath)
    make_complex(10, 12)
    execute("ls")
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


# Bad Code, not explicit
def make_complex(*args):
    x, y = args
    return dict(**locals())


# Bad Code, Not secure
def execute(cmd):
    try:
        retcode = subprocess.call(cmd, shell=True)
    except OSError as e:
        print("error")


# Bad code, Using setDefault or Keyerror Exception to handle missing key error
def dict_usage_with_try_except(dict):
    try:
        sampleval = dict['samplekey']
    except KeyError as exp:
        print("Key not found")


def dict_usage_with_setdefault(dict):
    dict.setdefault('missing_key', 'default value')
    val = dict['missing_key']
    print(val)
