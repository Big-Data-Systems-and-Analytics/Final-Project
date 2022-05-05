import boto3
import streamlit as st

client = boto3.client('s3', aws_access_key_id = st.secrets["Access_Key_ID"],aws_secret_access_key = st.secrets["Secret_Access_Key"])

def new_agent(agentname):
    bucket_name = "testteam19"
    folder_name = agentname
    client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))