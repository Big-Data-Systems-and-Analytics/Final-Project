import boto3
import json
from decimal import Decimal



def datachunk(text):
    
    
    list_parts = []
    text_for_analysis = ''
    for sentence in text.split('.'):
    #for sentence in results.results.transcripts[0].transcript:
        current_text = text_for_analysis + f'{sentence}.'

        if len(current_text.encode('utf-8')) > 5000:
            list_parts.append([len(text_for_analysis), text_for_analysis])
            text_for_analysis = f'{sentence}.'

        else:
            text_for_analysis += f'{sentence}.'

    list_parts.append([len(text_for_analysis), text_for_analysis])
    dict_comprehend = {}
    

    
    for t_parts in list_parts:
       
        comprehend_client = boto3.client(service_name='comprehend', region_name='us-east-1')
        sentimentData = comprehend_client.detect_sentiment(Text=t_parts[1], LanguageCode='en')
        #sentimentData = comprehend_client.detectSentiment(params, function(err, data)
        
        dict_comprehend[t_parts[0]] = sentimentData
        dict_comprehend[t_parts[0]]['ratio'] = t_parts[0]/float(len(text))
    #print("sentimentData",sentimentData)
    final_dict = {'Positive':0, 'Negative':0, 'Neutral':0, 'Mixed':0}
    list_sentiments = ['Positive', 'Negative', 'Neutral', 'Mixed']
    for sentiment in list_sentiments:
        for key, value in dict_comprehend.items():
            final_dict[sentiment] += value.get('SentimentScore').get(sentiment) * value.get('ratio')
    
    return final_dict
 
 
 
 
def lambda_handler(event, context):
    print(event)
    print("event",str(event))
    s3 = boto3.client("s3")
    file_obj = event["Records"][0]
    bucket = str(file_obj["s3"]["bucket"]["name"])
    print(bucket)
    key = str(file_obj["s3"]["object"]["key"])
    print(key)
    file = s3.get_object(Bucket=bucket, Key=key)
    print("file", file)
    job_name = context.aws_request_id

    para1 = file['Body'].read()
    para=json.loads(para1)
    print(para)
    #json_load = json.load(para)
    for i in range  (len(para)):  
    #print(i) 
        if len(para['results']['transcripts']) > 0:
            paragraph = para['results']['transcripts'][i].get('transcript')
            print("yes")
            

            #paragraph= para['results']['transcripts'][0]['transcript']
            print(paragraph)
            dur= para['results']['items']
            print(dur)    
            dur.reverse()
            for i in range  (len(dur)):   
                if dur[i].get('end_time'):
                    n = dur[i].get('end_time')
                    break
            print("time",round(float(n)/60,2))

            comprehend = boto3.client("comprehend")
            sentiment = comprehend.batch_detect_sentiment(TextList=["datachunk(paragraph)"], LanguageCode="en")
            max_key = max(datachunk(paragraph), key=datachunk(paragraph).get)
            final = datachunk(paragraph)
            json_final = json.dumps(final) 
            print("Agent", key.split("/")[1].split("_")[0])
            y = {"Sentiment":max_key, "partition_key": key.split("/")[1].split(".")[0], "Agent":key.split("/")[1].split("_")[0], "Duration": round(float(n)/60,2)}
            z = json.loads(json_final)
            z.update(y)
            print("partition_key", key.split("/")[1].split(".")[0])
            print("final json",json.dumps(z))
            print("final",final,max_key)
            #print(max_key)
            #return json.dumps(z)
            load_json = json.dumps(z)
            #changed_data = json.loads(json.dumps(data), parse_float=Decimal)
            s3.put_object(Bucket = bucket, Key = "comprehend/{}.json".format(key.split("/")[1].split(".")[0]), Body=load_json)
            break
        
        else:
            print("Transcript not present")    
            break
    
def create_uri(bucket_name, file_name):
    return "s3://" + bucket + "/" + key      
