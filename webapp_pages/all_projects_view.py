import streamlit as st
import mysql.connector as connection
import pandas as pd

def all_projects_view_func():

    mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
    
    query_get_all_projects_data = "SELECT * FROM project;"
    df_all= pd.read_sql(query_get_all_projects_data,mydb)

    st.dataframe(df_all)

    mydb.close()