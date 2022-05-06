import json
import boto3
from decimal import Decimal
#from boto3.dynamodb2.table import Table
#import boto3.dynamodb

def lambda_handler(event, context):
    print("event",str(event))
    s3 = boto3.client("s3")
    dynamodb = boto3.resource('dynamodb')
    if event:
        print("started")
        file_obj = event["Records"][0]
        bucket_name = str(file_obj["s3"]["bucket"]["name"])
        print(bucket_name)
        file_name = str(file_obj["s3"]["object"]["key"])
        print(file_name)
        json_object = s3.get_object(Bucket=bucket_name, Key=file_name)
        jsonFileReader = json_object['Body'].read()
        jsonDict = json.loads(jsonFileReader, parse_float=Decimal)
        #print(json.loads(jsonFileReader)
        #print(dynamodb.list_tables()['TableNames'])
        table = dynamodb.Table('sentiment2')
        table.put_item(Item=jsonDict)
        print("ingested into table sentiment2")
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
