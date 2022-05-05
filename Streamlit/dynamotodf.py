import boto3
import pandas as pd
import streamlit as st

def dbtodf():
   
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=st.secrets["Access_Key_ID"],aws_secret_access_key=st.secrets["Secret_Access_Key"],region_name='us-east-1')
    
    response = dynamodb.Table('sentiment').scan()
    x = response['Items']
    df = pd.DataFrame(x)
    df['Neutral'] = df['Neutral'].astype(float, errors = 'raise')
    df['Negative'] = df['Negative'].astype(float, errors = 'raise')
    df['Mixed'] = df['Mixed'].astype(float, errors = 'raise')
    df['Positive'] = df['Positive'].astype(float, errors = 'raise')
    df['Duration'] = df['Duration'].astype(float, errors = 'raise')
    return df

def checkfile(data,key):
  
    if data.loc[data['partition_key'] == key].shape[0] == 1:
        return data.loc[data['partition_key'] == key]
    else:
        return None

def getAgentData(data,agent):
    agent_df = data.loc[data['Agent']== agent]
    sentimentcountdf = agent_df['Sentiment']
    sentimentcountdf = sentimentcountdf.value_counts()
    return agent_df,sentimentcountdf