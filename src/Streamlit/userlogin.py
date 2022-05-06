import boto3
import streamlit as st
import re
cognito_client = boto3.client('cognito-idp',region_name='us-east-1')

def login(user,password):   
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
    try:
        response = cognito_client.initiate_auth(
            ClientId = st.secrets["Cognito_Client_ID"],
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters = {
                'USERNAME': user,
                'PASSWORD': password
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode']   
    except:
        return  400 

def signup(new_username,new_password):
    """Gets username and password, sends signup request to AWS Cognito
    Parameters
    ----------
    user : str
        Username provided by the user
    password : str
        Password provided by the user

    Returns
    -------
    int
        An integer representing the status code of the signup request
    """
    try:
        response = cognito_client.sign_up(
            ClientId = st.secrets["Cognito_Client_ID"],                
            Username= new_username,
            Password= new_password  
        )
        return response['ResponseMetadata']['HTTPStatusCode']
    except:
        return 400