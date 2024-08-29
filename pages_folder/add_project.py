import streamlit as st
import mysql.connector as connection
import time



def add_project_func():

    iga_1 = "FY2018-FY2024"
    iga_2 = "FY2025-FY2030"

    # Define options for the first dropdown
    igas = [iga_1, iga_2]

    # Create the first dropdown
    selected_iga = st.selectbox('Choose iga for project:', igas)
    
    if selected_iga==iga_1:
        proj_iga=1
    elif selected_iga==iga_2:
        proj_iga=2

    # Define options for the second dropdown based on the first selection
    years = {iga_1: ['2018', '2019','2020', '2021', '2022', '2023', '2024'], iga_2: ['2025', '2026', '2027', '2028', '2029', '2030']}

    # Create the second dropdown
    selected_years = st.multiselect('Choose years for which project is budgeted:', years[selected_iga], default=None)

    # Display the selected item
    # st.write(f'You selected: {selected_years}')

    proj_no = st.text_input("Enter project number:")
    proj_title = st.text_input("Enter project title:")
    proj_sub_no = st.text_input("Enter sub number:")
    proj_grant_code = st.text_input("Enter grant code:")
    proj_sub_name = st.text_input("Enter sub name:")
    proj_pi = st.text_input("Enter PI (Principal Investigator):")

    # st.write("submitted data:", proj_no, proj_title, proj_sub_no, proj_grant_code, proj_sub_name, proj_pi)
        
    for year in selected_years:
        idot_share_year = "idot_share_"+year
        cost_share_year = "cost_share_"+year
        subadmin_cost_year = "subadmin_cost_year_"+year
        total_budget_year = "total_budget_"+year
        st.write("For year:", year)
        idot_share_year = st.number_input("IDOT share:", value=None, format="%0.2f", key=idot_share_year)
        cost_share_year = st.number_input("Cost share:", value=None, format="%0.2f", key=cost_share_year)
        subadmin_cost_year = st.number_input("IDOT share:", value=None, format="%0.2f", key=subadmin_cost_year)
        total_budget_year = st.number_input("IDOT share:", value=None, format="%0.2f", key=total_budget_year)
        st.write(idot_share_year, cost_share_year)

    mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)

    if st.button("Submit"):
        mycursor = mydb.cursor()
        query_insert_project = "INSERT INTO project (project_number, project_title, sub_number, grant_code, sub_name, p_i, iga_ref) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        val = (proj_no, proj_title, proj_sub_no, proj_grant_code, proj_sub_name, proj_pi, proj_iga)
        mycursor.execute(query_insert_project, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        mydb.close() #close the connection
        st.write("submitted to database")
       
    # with st.form("add_new_project_form"):
    #     st.write("Add new project")

    #     proj_no = st.text_input("Enter project number:")
    #     proj_title = st.text_input("Enter project title:")
    #     proj_sub_no = st.text_input("Enter sub number:")
    #     proj_grant_code = st.text_input("Enter grant code:")
    #     proj_sub_name = st.text_input("Enter sub name:")
    #     proj_pi = st.text_input("Enter PI (Principal Investigator):")

    #     if selected_iga==iga_1:
    #         proj_iga=1
    #         # years_selected = st.multiselect("Select fiscal years to add project budgets:", ["2018", "2019", "2020", "2021", "2022", "2023", "2024"],default=None)
    #     elif selected_iga==iga_2:
    #         proj_iga=2
    #         # years_selected = st.multiselect("Select fiscal years to add project budgets:", ["2025", "2026", "2027", "2028", "2029", "2030"],default=None)
        
    #     for year in selected_years:
    #         st.write("For year:", year)
    #         idot_share = st.text_input("IDOT share: ",key=idot_share)
    #         cost_share = st.text_input("Cost share: ",key=cost_share)
    #         st.write(idot_share, cost_share)

    #     submitted = st.form_submit_button("Submit")
        
    #     if submitted:
    #         st.write("submitted data:", proj_iga, proj_no, proj_title, proj_sub_no, proj_grant_code, proj_sub_name, proj_pi)