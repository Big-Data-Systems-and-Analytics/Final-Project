from dynamotodf import checkfile,getAgentData,dbtodf
from userlogin import login,signup
import pandas as pd
data = dbtodf()


def test_checkfile():

    assert checkfile(dbtodf(),'Agen10_9').empty == True
    assert checkfile(dbtodf(),'').empty == True
    assert checkfile(dbtodf(),'Agent1_001').equals(data.loc[data['partition_key'] == 'Agent1_001'])
    assert checkfile(dbtodf(),'Agent1_001').equals(data.loc[data['partition_key'] == 'Agent1_001']) == True
    assert checkfile(dbtodf(),'Agent3_4074').equals(data.loc[data['partition_key'] == 'Agent3_4157']) == False
    

def test_getAgentData():
    agent_df,sentimentcountdf = getAgentData(data,'Agent2')  
    assert agent_df.equals(data.loc[data['Agent']== "Agent2"]) == True
    assert sentimentcountdf.equals(data.loc[data['Agent']== 'Agent2']['Sentiment'].value_counts()) == True
    agent_df,sentimentcountdf = getAgentData(data,'Agent5')
    assert agent_df.equals(data.loc[data['Agent']== "Agent3"]) == False
    assert sentimentcountdf.equals(data.loc[data['Agent']== 'Agent3']['Sentiment'].value_counts()) == False


def test_fileformat():
    filename = "3123.txt"
    wavfilename = "3123.wav"
    assert (filename.rsplit( ".", 1 )[ 1 ] == "wav") == False
    assert (wavfilename.rsplit( ".", 1 )[ 1 ] == "wav") == True

def test_login():
    assert login('knjbnmbhj','sdhjb436') == 400
    assert login('','') == 400
    assert login('test12345*','Test12345*') == 200

def test_signup():
    assert signup('scsjj','ksjsh') == 400
    assert signup('Pytest004*','Pytest004*') == 200