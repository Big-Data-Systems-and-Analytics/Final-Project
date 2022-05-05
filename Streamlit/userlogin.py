import boto3
import streamlit as st
import re
cognito_client = boto3.client('cognito-idp',region_name='us-east-1')

def login(user,password):   
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
        try:
            response = cognito_client.sign_up(
                ClientId = st.secrets["Cognito_Client_ID"],                
                Username= new_username,
                Password= new_password  
            )
            print(response)
            return response['ResponseMetadata']['HTTPStatusCode']
        except:
            return 400