import streamlit as st
import mysql.connector as connection
import pandas as pd

def project_view_func():

    mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
    query_get_igas = "SELECT * FROM iga;"
    result_igas = pd.read_sql(query_get_igas,mydb)
    existing_igas = result_igas['iga_fy_range'].unique().tolist()
    selected_iga= st.selectbox('Select IGA:', existing_igas)
    print(selected_iga)

    query_get_project_numbers = "SELECT project_number FROM project;"
    result_project_numbers = pd.read_sql(query_get_project_numbers,mydb)
    existing_projects_list = result_project_numbers['project_number'].unique().tolist()
    selected_project = st.selectbox('Select Project:', existing_projects_list)
    print(selected_project)
    
    query_get_all_projects_data = "SELECT * FROM project;"
    df_all= pd.read_sql(query_get_all_projects_data,mydb)
    df_selected = df_all[df_all['project_number']==selected_project]

    query_get_all_projects_data = "SELECT * FROM project;"
    df_all= pd.read_sql(query_get_all_projects_data,mydb)
    df_selected = df_all[df_all['project_number']==selected_project]


    st.write("Project Title : ", df_selected.iloc[0][2])
    st.write("Subaward # : ", df_selected.iloc[0][3])
    st.write("Grant Code: ", df_selected.iloc[0][4])
    st.write("Sub : ", df_selected.iloc[0][5])
    st.write("Principal Investigator: ", df_selected.iloc[0][6])

    mydb.close()
    



    # df = preprocessing.get_dataframe()
    
    # iga_selected = st.selectbox("Select IGA: ",("FY 2018 - 2024", "FY 2025 - 2030"))


    # all_projects_list = df['Project Number:'].unique().tolist()
    # project_selected = st.selectbox('Project Number:', all_projects_list)

    # df_one = df[df['Project Number:']==project_selected]
    # df_one = df_one.transpose()
    # df_one = df_one.reset_index()
    # df_one.columns = ['Project Attribute', 'Value']
    # df_one = df_one[df_one['Value'].notna()]

    # st.write("Project Title : ", df_one.iloc[1][1])
    # st.write("Subaward # : ", df_one.iloc[2][1])
    # st.write("Grant Code: ", df_one.iloc[3][1])
    # st.write("Sub : ", df_one.iloc[4][1])
    # st.write("Principal Investigator: ", df_one.iloc[5][1])

    # st.dataframe(df_one.astype(str), use_container_width=True, hide_index=True)