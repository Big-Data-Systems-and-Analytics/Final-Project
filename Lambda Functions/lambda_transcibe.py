import json
import boto3
import time
from urllib.request import urlopen
#print("started.....")

def lambda_handler(event, context):
    # TODO implement
    print("started.....")
    transcribe = boto3.client("transcribe")
    s3 = boto3.client("s3")
    if event:
        file_obj = event["Records"][0]
        bucket_name = str(file_obj["s3"]["bucket"]["name"])
        print(bucket_name)
        file_name = str(file_obj["s3"]["object"]["key"])
        print(file_name)
        s3_uri = create_uri(bucket_name, file_name)
        file_type = file_name.split(".")[1]
        job_name = context.aws_request_id

        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": s3_uri},
            MediaFormat=file_type,
            LanguageCode="en-US",
            Settings={
                # 'VocabularyName': 'string',
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": 2,
                "ChannelIdentification": False,
            })
        while True:
            status=transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED','FAILED']:
                break
            print("its in progress")
            time.sleep(10)
            
        load_url = urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        load_json = json.dumps(json.load(load_url))
        
        s3.put_object(Bucket = bucket_name, Key = "transcripts/{}.json".format(job_name), Body=load_json)
        
    return {
        'statusCode': 200,
        'body': json.dumps("Transcription job created!")
    }    
            
def create_uri(bucket_name, file_name):
    return "s3://" + bucket_name + "/" + file_name            
