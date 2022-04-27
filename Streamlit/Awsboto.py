
import boto3
import os
from keys import access_key, secret_key
# s3 object create\
client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_key)

for file in os.listdir():
    if '.txt' in file:
        upload_file_bucket = 'finalprojectbucketbalu'
        upload_file_key = 'audio-files/' + str(file)
        # s3.upload_file('file_name','Bucket_name','filename to be displayed')
        client.upload_file(file,upload_file_bucket,upload_file_key ) 