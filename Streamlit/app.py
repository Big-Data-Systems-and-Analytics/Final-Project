import streamlit as st
import pandas as pd
import boto3
from io import BytesIO
from keys import Access_Key_ID,Secret_Access_Key,Cognito_Client_ID


def main2():

   

    menu = ["Upload","Performance"]  #Add Create an Agent Page
    choice = st.selectbox("Menu",menu)

    if choice == "Upload":
        
        st.subheader("Upload Call")
        option = st.selectbox( 'Select Agents',("Agent-1","Agent-2","Agent-3"))  # Get the Agents Dynamically from s3 folders
 
        st.write('You selected:', option)

        if option :
            uploaded_file1 = st.file_uploader("Choose a file")
        if uploaded_file1 is not None:
        
            bytes_data1 = uploaded_file1.getvalue()
            bytesIO = BytesIO(bytes_data1)    
            s3client = boto3.client('s3', aws_access_key_id = Access_Key_ID, aws_secret_access_key = Secret_Access_Key)
            bucket = 'testteam19'
            #awsclient.upload_file(bytes_data1,bucket,uploaded_file1.name)
            awspath = option + "/" + uploaded_file1.name
            with bytesIO as data:
                s3client.upload_fileobj(data, bucket, awspath)
            #Check the status of lambda
            #dynamotodf
            #visualize the df
        
        


    elif choice == "Performance":
        st.subheader("Agent Performance")
        option = st.selectbox( 'Select Agents',("Agent-1","Agent-2","Agent-3")) # Get the Agents Dynamically from s3 folders
        st.write('You selected:', option)
        if option :
            print("Dashboards for each")


def main():
    st.title("Welcome to Call Intelligence Portal")
    

    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader('Login to Continue. New User? Signup first')

    elif choice == "Login":
        st.subheader("Login Section")

        user = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type='password')
        
        if st.sidebar.checkbox("Login"):
            cognito_client = boto3.client('cognito-idp')
            try:
                response = cognito_client.initiate_auth(
                    ClientId = Cognito_Client_ID,
                    AuthFlow = 'USER_PASSWORD_AUTH',
                    AuthParameters = {
                        'USERNAME': user,
                        'PASSWORD': password
                    }
                )
                if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                    st.write("Login Successful")
                    main2() 
            except:
                st.write("Username/Password is incorrect or Username not confirmed by admin")
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        if st.button("Signup"):
            cognito_client = boto3.client('cognito-idp')
            try:
                response = cognito_client.sign_up(
                    ClientId = Cognito_Client_ID,                
                    Username= new_username,
                    Password= new_password  
                )
                st.write("Signup Successful. You will be able to login after admin approval")
            except:
                st.write("Username already exists")
if __name__ == '__main__':
    main()