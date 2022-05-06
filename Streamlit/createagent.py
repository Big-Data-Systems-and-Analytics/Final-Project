import boto3
import streamlit as st

client = boto3.client('s3', aws_access_key_id = st.secrets["Access_Key_ID"],aws_secret_access_key = st.secrets["Secret_Access_Key"])

def new_agent(agentname):
    """Gets name of the agent from the user and creates a dedicated folder for the agent in an S3 bucket

    Parameters
    ----------
    user : str
        Username provided by the user

    """
    bucket_name = "audio-analysis-data"
    folder_name = agentname
    client.put_object(Bucket=bucket_name, Key=('audio'+'/'+folder_name+'/'))