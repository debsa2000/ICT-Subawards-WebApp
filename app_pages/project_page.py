import streamlit as st
import mysql.connector as connection
import pandas as pd

def project_page_func():
    try:
        mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
    except Exception as e:
        st.write(str(e))
        return
    
    query_igas = "SELECT * FROM iga;"
    df_igas = pd.read_sql(query_igas,mydb)
    existing_igas =  df_igas['iga_fy_range'].to_list()

    selected_iga = st.selectbox('Choose iga that new project belongs to:', existing_igas)
    
    for i,row in df_igas.iterrows():
        if row['iga_fy_range']==selected_iga:
            start_year=row['iga_start_year']
            end_year=row['iga_end_year']
            selected_iga_code=row['iga_code']
    
    year_options=[]
    for year in range(start_year,end_year+1):
        year_options.append(year)



        
    # selected_years = st.multiselect('Choose years for which project is budgeted:', year_options, default=None)  
    # for year in selected_years:
    #     idot_share_year = "idot_share_"+ str(year)
    #     cost_share_year = "cost_share_"+ str(year)
    #     subadmin_cost_year = "subadmin_cost_year_"+ str(year)
    #     total_budget_year = "total_budget_"+ str(year)
    #     st.write("For year", str(year), ":")
    #     idot_share_year = st.number_input("IDOT share:", value=None, format="%0.2f", key=idot_share_year)
    #     cost_share_year = st.number_input("Cost share:", value=None, format="%0.2f", key=cost_share_year)
    #     subadmin_cost_year = st.number_input("Subadmin cost:", value=None, format="%0.2f", key=subadmin_cost_year)
    #     total_budget_year = st.number_input("Total budget for project for the year:", value=None, format="%0.2f", key=total_budget_year)
    with st.form("add_new_project"):
        st.write("Add new project:")
        proj_no = st.text_input("Enter project number:")
        proj_title = st.text_input("Enter project title:")
        proj_sub_no = st.text_input("Enter sub number:")
        proj_grant_code = st.text_input("Enter grant code:")
        proj_sub_name = st.text_input("Enter sub name:")
        proj_pi = st.text_input("Enter PI (Principal Investigator):")
        proj_end_date= st.date_input("Select planned end date for project:", format="MM-DD-YYYY", value=None)    
        proj_total_budget= st.number_input("Enter total budget: ", step=0.01)
        
        submitted= st.form_submit_button("Submit project")
        
        if submitted:
            mycursor = mydb.cursor()
            query_insert_project = "INSERT INTO project (project_number, project_title, sub_number, grant_code, sub_name, p_i, iga_ref, planned_end_date, total_project_budget) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val = (proj_no, proj_title, proj_sub_no, proj_grant_code, proj_sub_name, proj_pi, selected_iga_code, proj_end_date, proj_total_budget)
            mycursor.execute(query_insert_project, val)
            mydb.commit()

        
    mydb.close() #close the connection