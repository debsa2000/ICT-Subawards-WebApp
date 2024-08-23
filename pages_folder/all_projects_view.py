import streamlit as st
import preprocessing

def all_projects_view_func():
    
    df = preprocessing.get_dataframe()
    df.rename(columns={ df.columns[6]: "FY18-FY24 Subaward Total" }, inplace = True)
    st.dataframe(df.astype(str))