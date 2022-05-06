# Customer Support Call Intelligence and Analytics


## Team Members

#### Bala Yeshwant M
#### Greeshma Tatineni
#### Kashyap Datta Kovvali
#### Swathi Sharma


## Project Report

<img width="742" alt="image" src="https://user-images.githubusercontent.com/91439390/167069671-eea6865d-daab-42d9-938a-679657ff647e.png">


## Project Proposal 

https://codelabs-preview.appspot.com/?file_id=1_Ycc7fLGvPxIqPCUQGJnXBAODftM13Q0FktpYkdfYbE#0


## Web Application - Hosted on Streamlit


https://share.streamlit.io/kashyap-datta/callanalyticsportal_streamlit/main/app.py


## Introduction

As part of an academic project for the course Big Data Systems & Intelligence Analytics, we have built an application for customer support in call centers.
Through this application we uncover insights from conversations of customers with call center agents, to help businesses manage script compliance and find new opportunities to satisfy the customers.



## Architecture

<img width="742" alt="image" src="https://user-images.githubusercontent.com/91439390/167064138-16f66117-6426-46a1-9b0e-87d6c9fe5ce4.png">



## Folder Structure




## Getting Started

### Prequisites

1. Python 3.7+
2. Streamlit
3. Amazon Web Services

The pipeline requires an Amazon Web Services (AWS) account set up for deploying.
The pipeline requires the following AWS services :

 - S3
 - Lambda
 - Transcribe
 - Comprehend
 - DynamoDb
 - Athena
 - IAM
 - CloudWatch
 - Cognito
 - Quicksight


## Setup

1. AWS - Create an AWS account, if you don't have one already
2. Quicksight Access - 
The marketing manager and the customer service manager will be given access to the quicksight dashboard to view the analytics. They need to follow the below steps to acces the dashboard via the link: https://us-east-1.quicksight.aws.amazon.com/sn/dashboards/aab311a1-27ba-40fc-80ba-532ddd1c8dd2
  1. Create a quicksight account once the email with the invitation is received
  2. account name: bigdata-team7, make sure the correct account name is passsed during login
  3. View the interactive dashboard


## Workflow

### Admin Uploads the Call Recording


<img width="108" alt="image" src="https://user-images.githubusercontent.com/91439390/167067264-ecc32a22-2737-4b54-8966-6878b5fc8dd1.png"> An admin can sign up as a new user, and later can log into Streamlit with a designated username and password.  He/She can then upload a recording of agent speaking with a customer on the Streamlit frontend, of the format .wav or .mp3 
 

<img width="108" alt="image" src="https://user-images.githubusercontent.com/91439390/167067445-9009df3f-4366-4888-bad7-8686bbb6b06a.png"> AWS Cognito is used for user authentication while logging into Streamlit. Only authenticated users will be able to access the Dashboard on Streamlit


<img width="45" alt="image" src="https://user-images.githubusercontent.com/91439390/167067479-05e3617b-c957-4a03-83d7-e6801ec02e96.png"> AWS S3 to store Audio files - After a call recording has been uploaded on Streamlit frontend, it is stored as an object in the AWS S3 bucket. For every new recording being uploaded, it is stored as a new object in the same bucket. This way, we will be storing all the audio files in one place.

<img width="45" alt="image" src="https://user-images.githubusercontent.com/91439390/167067520-3d5073b7-84be-4ec9-af3d-8251ec208e46.png"> AWS Lambda to Trigger Transcribe Job - When an audio file is created as an object, a lambda function is triggered in ordered to start the Transcribe job


<img width="40" alt="image" src="https://user-images.githubusercontent.com/91439390/167067595-bd5ab3a8-f5ce-414e-b52c-c22f8bef2e65.png"> AWS Transcribe - Amazon Transcribe is an automatic speech recognition service that makes it easy to add speech to text capabilities to any application. Transcribe’s features enable it to ingest audio input, produce easy to read and review transcripts, improve accuracy with customization, and filter content to ensure customer privacy. The lambda function that triggered the transcribe job previously, gives us a transcription everytime a new audio file is placed in the S3 bucket. This transcripted text is then saved in another (new) bucket in .json format.


<img width="45" alt="image" src="https://user-images.githubusercontent.com/91439390/167067530-da250f90-8c0d-4379-a17a-461b1383e621.png"> AWS Lambda to Trigger Comprehend Job - After the transcription file is generated and placed in a new bucket, another lambda function is triggered to fetch this file and perform sentiment analysis using AWS Comprehend

<img width="45" alt="image" src="https://user-images.githubusercontent.com/91439390/167067634-c5d0a09c-bd78-4a54-a2c4-39ce64fed0c6.png"> AWS Comprehend - Amazon Comprehend uses natural language processing (NLP) to extract insights about the content of documents. It develops insights by recognizing the sentiments and other common elements in a document. Every time a new transcripted file is generated, a lambda function is triggered to run the comprehend job. We have utilized chunking of text files as Amazon Comprehend imposes a size limit of 5000 bytes on each text file. Since the audio files’ transcriptions are usually greater than 5000 bytes, chunking the text files into smaller files helps in running the comprehend job successfully. We get a sentiment, as well as a sentiment score for each of the chunks and we then take an aggregate score of the sentiment to declare an overall sentiment of the call. The result is stored as a json file in the S3 bucket.

This process will be repeated each time a new audio recording is uploaded into the S3 bucket. The file gets uploaded to S3, goes through Transcribe to get a transcription and finally goes through Comprehend to get the sentiment of the call for each agent-customer combination. Now that we have the data , we will be performing some analysis to view the results in a concise dashboard, using AWS Quicksight

<img width="45" alt="image" src="https://user-images.githubusercontent.com/91439390/167067690-1b82223a-f5ae-4340-9dba-abd772dfbb8b.png"> AWS DynamoDb - Amazon DynamoDB is a NoSQL database that supports key-value and document data models. The result data that is in the json format is stored in DynamoDB as key:Sentiment and value:Sentiment Score pairs. This is then connected to Amazon Athena using Athena connectors

<img width="51" alt="image" src="https://user-images.githubusercontent.com/91439390/167067723-7f0cdc4f-7d9d-4364-a43d-c8ca9b715d53.png"> AWS Athena - Amazon Athena is an interactive query service that makes it easy to analyze data directly in Amazon S3 using standard SQL. We will be using Athena to query the DynamoDb table and get the results, for further analysis in Quicksight. Since DynamoDb cannot be integrated directly with Quicksight (because of architectural constraints imposed by AWS), we are using Athena as a connection between DynamoDb and Quicksight
AWS Athena - Amazon Athena is an interactive query service that makes it easy to analyze data directly in Amazon S3 using standard SQL. We will be using Athena to query the DynamoDb table and get the results, for further analysis in Quicksight. Since DynamoDb cannot be integrated directly with Quicksight (because of architectural constraints imposed by AWS), we are using Athena as a connection between DynamoDb and Quicksight

<img width="51" alt="image" src="https://user-images.githubusercontent.com/91439390/167067754-0a54f41f-e583-4f94-baaf-e33583581ce1.png"> AWS Quicksight - Amazon QuickSight allows everyone in the organization to understand the data through interactive dashboards. Quicksight will enable call center admins and other stakeholders to view analytics with respect to performance of the agents, number of calls attended and number of happy customers.




## Dataset 

The dataset consists of call recordings between agents and customers. We will be working on these audio files to convert them to text files in order to perform sentiment analysis and visualizations so that the admins can get insights on how well their employees are performing, and how satisfied their customers are.

Dataset Link : https://media.talkbank.org/ca/CallHome/eng/



## Quicksight Dashboard

<img width="615" alt="image" src="https://user-images.githubusercontent.com/91439390/167068296-360899cb-acd5-4507-9457-bf3ae19f1d91.png">



