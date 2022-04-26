import streamlit as st
import pandas as pd


st.title("Employee ")

menu = ["Upload","Performance"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Upload":
    option = st.selectbox( 'Select Agents',("Agent-1","Agent-2","Agent-3"))

    st.write('You selected:', option)

    if option :
        uploaded_file1 = st.file_uploader("Choose a file")
    if uploaded_file1 is not None:
     
     bytes_data1 = uploaded_file1.getvalue()
     st.write(bytes_data1)
        
elif choice == "Performance":
    st.subheader("Dashboards")
    option = st.selectbox( 'Select Agents',("Agent-1","Agent-2","Agent-3"))
    st.write('You selected:', option)
    if option :
        print("Dashboards for each")
