import streamlit as st
import preprocessing
import plotly.express as px

def project_view_func():
    df = preprocessing.get_dataframe()
    df.rename(columns={ df.columns[6]: "FY18-FY24 Subaward Total" }, inplace = True)

    
    iga_selected = st.selectbox("Select IGA: ",("FY 2018 - 2024", "FY 2025 - 2030"))


    all_projects_list = df['Project Number:'].unique().tolist()
    project_selected = st.selectbox('Project Number:', all_projects_list)

    df_one = df[df['Project Number:']==project_selected]
    df_one = df_one.transpose()
    df_one = df_one.reset_index()
    df_one.columns = ['Project Attribute', 'Value']
    df_one = df_one[df_one['Value'].notna()]

    st.write("Project Title : ", df_one.iloc[1][1])
    st.write("Subaward # : ", df_one.iloc[2][1])
    st.write("Grant Code: ", df_one.iloc[3][1])
    st.write("Sub : ", df_one.iloc[4][1])
    st.write("Principal Investigator: ", df_one.iloc[5][1])

    st.dataframe(df_one.astype(str), use_container_width=True, hide_index=True)