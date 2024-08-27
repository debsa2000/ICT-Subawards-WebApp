import streamlit as st
import mysql.connector as connection

def add_project_func():
    
       
    with st.form("add_new_project_form"):
        st.write("Add new project")

        iga_selected = st.selectbox("Select IGA FY range for new project: ",("FY 2018 - 2024", "FY 2025 - 2030"))

        if iga_selected=="FY 2018 - 2024":
            proj_iga=1
        if iga_selected=="FY 2025 - 2030":
            proj_iga=2

        proj_no = st.text_input("Enter project number:")
        proj_title = st.text_input("Enter project title:")
        proj_sub_no = st.text_input("Enter sub number:")
        proj_grant_code = st.text_input("Enter grant code:")
        proj_sub_name = st.text_input("Enter sub name:")
        proj_pi = st.text_input("Enter PI (Principal Investigator):")
    
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.write("submitted data:", proj_iga, proj_no, proj_title, proj_sub_no, proj_grant_code, proj_sub_name, proj_pi)

    mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
    
    mycursor = mydb.cursor()
    query_insert_project = "INSERT INTO project (project_number, project_title, sub_number, grant_code, sub_name, p_i, iga_ref) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    val = (proj_no, proj_title, proj_sub_no, proj_grant_code, proj_sub_name, proj_pi, proj_iga)
    mycursor.execute(query_insert_project, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mydb.close() #close the connection