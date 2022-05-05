import boto3
import streamlit as st


def getAgents():
    session = boto3.Session(aws_access_key_id = st.secrets["Access_Key_ID"],aws_secret_access_key = st.secrets["Secret_Access_Key"])
    client = boto3.client('s3', aws_access_key_id = st.secrets["Access_Key_ID"],aws_secret_access_key = st.secrets["Secret_Access_Key"])
    s3 = session.resource('s3')
    AgentList = []
    prefix ='audio/'
    result = client.list_objects(Bucket='audio-analysis-data', Prefix=prefix, Delimiter='/')
    for o in result.get('CommonPrefixes'):
        AgentList.append(o.get('Prefix').rsplit("/")[1])
    return AgentList


