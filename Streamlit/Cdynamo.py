import boto3
import os
from keys import access_key, secret_key
import requests
client = boto3.client(
    'dynamodb',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key
    )
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
    )
ddb_exceptions = client.exceptions

response = dynamodb.Table('sentiment').scan()

#for i in response['Items']:
   # print(i)

for i in  response['Items']:
    if i['partition_key'] == '4065.json':
        print(i['Sentiment'])


