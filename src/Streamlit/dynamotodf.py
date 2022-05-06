import boto3
import pandas as pd
import streamlit as st

def dbtodf():

    """Gets username and password, authenticates them against AWS Cognito users and returns status code

    Parameters
    ----------
    user : str
        Username provided by the user
    password : str
        Password provided by the user

    Returns
    -------
    int
        An integer representing the status code of the authentication request
    """
   
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=st.secrets["Access_Key_ID"],aws_secret_access_key=st.secrets["Secret_Access_Key"],region_name='us-east-1')
    
    response = dynamodb.Table('sentiment2').scan()
    x = response['Items']
    df = pd.DataFrame(x)
    df['Neutral'] = df['Neutral'].astype(float, errors = 'raise')
    df['Negative'] = df['Negative'].astype(float, errors = 'raise')
    df['Mixed'] = df['Mixed'].astype(float, errors = 'raise')
    df['Positive'] = df['Positive'].astype(float, errors = 'raise')
    df['Duration'] = df['Duration'].astype(float, errors = 'raise')
    return df

def checkfile(data,key):

    """Checks and gets data corresponding to the key

    Parameters
    ----------
    data : dataframe
        Dataframe with data from the dynamodb returned by dbtodf() function
    key : str
        partition_key which is combination of agent name and audio file name

    Returns
    -------
    dataframe
        A dataframe corresponding to the key
    """

    if data.loc[data['partition_key'] == key].shape[0] == 1:
        return data.loc[data['partition_key'] == key]
    else:
        return pd.DataFrame()

def getAgentData(data,agent):

    """Gets data corresponding to an agent

    Parameters
    ----------
    data : dataframe
        Dataframe with data from the dynamodb returned by dbtodf() function
    agent : str
        Name of the agent

    Returns
    -------
    dataframe
        Data corresponding to the agent
    dataframe
        Sentiment count corresponding to the agent
    """
    agent_df = data.loc[data['Agent']== agent]
    sentimentcountdf = agent_df['Sentiment']
    sentimentcountdf = sentimentcountdf.value_counts()
    return agent_df,sentimentcountdf