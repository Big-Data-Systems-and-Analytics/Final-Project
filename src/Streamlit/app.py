import streamlit as st
import pandas as pd
import boto3
from io import BytesIO
import time
import altair as alt
from dynamotodf import dbtodf,checkfile,getAgentData
from createagent import new_agent
from agentlist import getAgents
from userlogin import login,signup


def main():

    """Lands logged in users here. Allows user to create new customer agents, upload call audio and analyze performance of each agent"""
   
    s3client = boto3.client('s3', aws_access_key_id = st.secrets["Access_Key_ID"], aws_secret_access_key = st.secrets["Secret_Access_Key"])   
    bucket = 'audio-analysis-data'
    menu = ["Upload Audio","Agent Performance","Create Agent"] 
    choice = st.selectbox("Menu",menu)
   
    if choice == "Upload Audio":

        st.subheader("Upload Call")
        AgentList = getAgents()
        option = st.selectbox( 'Select Agents', AgentList)  #Shows the list of agents
        st.write('You selected:', option)

        if option :
            uploaded_file = st.file_uploader("Choose a file") 
       
        if uploaded_file is not None:
            
            if ((uploaded_file.name.rsplit( ".", 1 )[ 1 ]) == "wav"):  #Checks the uploaded file format
                key = option+"_"+uploaded_file.name.rsplit( ".", 1 )[ 0 ]
                dataframe = dbtodf()
                data = checkfile(dataframe,key)
                if data.empty == True:
                    bytes_data = uploaded_file.getvalue()
                    bytesIO = BytesIO(bytes_data)    
                    awspath = "audio/"+option+ "/" + uploaded_file.name

                    with bytesIO as data:
                        with st.spinner('Wait for the file to Upload...'):
                            s3client.upload_fileobj(data, bucket, awspath)  #Uploads the audio data to aws bucket in the specified path
                            time.sleep(10)
                            st.success('Successfully Uploaded!')
                    
                    with st.spinner('Wait for the Analysis...'):
                        time.sleep(90)
                        dataframe = dbtodf() #Gets data from dynamodb 
                        data = checkfile(dataframe,key) 
                        if data.empty == False:
                            st.success('Here is the Analysis about the call')
                            st.write('Sentiment of the call:' +" "+data["Sentiment"].values[0])
                            st.write('Duration of the call:' + " " + str(data["Duration"].values[0])+ " "+"Minutes")
                            chartdata = data.drop(['Sentiment','Agent','partition_key','Duration'],axis=1)
                            st.bar_chart(chartdata)
                        else:
                            st.info("Large audio file uploaded. Please re-upload after sometime for the analysis.")  
                else:
                    st.info("This file is already upload. Getting just the analysis now")
                    dataframe = dbtodf()
                    data = checkfile(dataframe,key)   
                    st.success('Here is the Analysis about the call')
                    st.write('Sentiment of the call:' +" "+data["Sentiment"].values[0])
                    st.write('Duration of the call:' + " " + str(data["Duration"].values[0])+ " "+"Minutes")
                    st.subheader("Sentiment Chart")
                    chartdata = data.drop(['Sentiment','Agent','partition_key','Duration'],axis=1)
                    st.bar_chart(chartdata)  
            else:
                st.error("Unexpexted file format. Upload only .wav files")
            


    elif choice == "Agent Performance":
        st.subheader("Agent Performance")
        AgentList = getAgents()
        option = st.selectbox( 'Select Agents', AgentList)   
        st.write('You selected:', option)
        if option :
            
            dataframe = dbtodf()
            agent_df,sentimentcountdf = getAgentData(dataframe,option)
            agent_df.drop(['Sentiment','Agent','partition_key','Duration'],axis=1,inplace=True)
            st.write("Sentiments for each call:")
            st.bar_chart(agent_df)
            st.write("Overall Call Sentiment Count:")
            st.bar_chart(sentimentcountdf)

    elif choice == "Create Agent": 
        st.subheader("Create a new Call Support Agent")  
        st.write("Provide Agent Name:")
        AgentName = st.text_input('')
        if st.button('Create'):
            if AgentName != '':
                new_agent(AgentName)
                st.success("Agent is created")
            else:
                st.error("Provide name of the Agent")
        


def landing():

    """Landing Screen for the application. Allows user to Sign Up and/or Login"""
  
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
            response = login(user,password)
            if(response!=400):
                st.write("Login Successful")
                main() 
            else:
                st.write("Username/Password is incorrect or Username not confirmed by admin")
                
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        if st.button("Signup"):
            response = signup(new_username,new_password)
            if(response!=400):
                st.write("Signup Successful. You will be able to login after admin approval")
            else:
                st.write("Username already exists")           
            

if __name__ == '__main__':
    landing()