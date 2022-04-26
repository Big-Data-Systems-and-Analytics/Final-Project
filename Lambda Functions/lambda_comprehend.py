import boto3


# def datachunk(para):
#     text_list = []

#     while para:
#         text_list.append(str(para[:4700]))
#         para = para[4700:]
#     return text_list[:25]


# def lambda_handler(event, context):
#     s3 = boto3.client("s3")
#     file_obj = event["Records"][0]
#     bucket = str(file_obj["s3"]["bucket"]["name"])
#     print(bucket)
#     key = str(file_obj["s3"]["object"]["key"])
#     print(key)
#     file = s3.get_object(Bucket=bucket, Key=key)
#     paragraph = str(file["Body"].read().decode("utf-8"))
#     comprehend = boto3.client("comprehend")
#     dict_comprehend = {}
#     text_list = datachunk(paragraph)
#     for t_parts in text_list:
#         print("entering first for loop")
#         sentiment = comprehend.batch_detect_sentiment(
#         TextList=datachunk(paragraph), LanguageCode="en")
#         print(sentiment)
#         print("t_parts[0]",t_parts[0])
#         dict_comprehend[t_parts[0]] = sentiment
#         dict_comprehend[t_parts[0]]['ratio'] = t_parts[0]/float(len(paragraph))
        


#         print(sentiment)
    
#     final_dict = {'Positive':0, 'Negative':0, 'Neutral':0, 'Mixed':0}
#     list_sentiments = ['Positive', 'Negative', 'Neutral', 'Mixed']
#     for s in list_sentiments:
        
#         for key, value in dict_comprehend.items():
            
#             final_dict[s] += value.get('SentimentScore').get(s) * value.get('ratio')
#     print(final_dict)
#     return final_dict


#     return "Thanks"


def datachunk(text):
    
    list_parts = []
    text_for_analysis = ''
    for sentence in text.split('.'):
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
        
        dict_comprehend[t_parts[0]] = sentimentData
        dict_comprehend[t_parts[0]]['ratio'] = t_parts[0]/float(len(text))
    print("sentimentData",sentimentData)
    final_dict = {'Positive':0, 'Negative':0, 'Neutral':0, 'Mixed':0}
    list_sentiments = ['Positive', 'Negative', 'Neutral', 'Mixed']
    for sentiment in list_sentiments:
        for key, value in dict_comprehend.items():
            final_dict[sentiment] += value.get('SentimentScore').get(sentiment) * value.get('ratio')
    
    return final_dict
 
 
 
 
def lambda_handler(event, context):
    s3 = boto3.client("s3")
    file_obj = event["Records"][0]
    bucket = str(file_obj["s3"]["bucket"]["name"])
    print(bucket)
    key = str(file_obj["s3"]["object"]["key"])
    print(key)
    file = s3.get_object(Bucket=bucket, Key=key)
    paragraph = str(file["Body"].read().decode("utf-8"))
    comprehend = boto3.client("comprehend")
    sentiment = comprehend.batch_detect_sentiment(TextList=["datachunk(paragraph)"], LanguageCode="en")
    max_key = max(datachunk(paragraph), key=datachunk(paragraph).get)
    print("final",datachunk(paragraph),max_key)
    #print(max_key)
    return max_key
    return datachunk(paragraph)
    # sentiment = comprehend.batch_detect_sentiment(
    #     TextList=datachunk(paragraph), LanguageCode="en"
    # )
    #print(sentiment)
