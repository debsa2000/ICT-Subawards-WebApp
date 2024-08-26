import streamlit as st

def add_project_func():
    
    with st.form("add_new_project_form"):
        st.write("Add new project")

        iga = st.selectbox("Select IGA: ",("FY 2018 - 2024", "FY 2025 - 2030"))
        project_number = st.text_input("Enter project number:")
        project_title = st.text_input("Enter project title:")
        sub_number = st.text_input("Enter sub number:")
        grant_code = st.text_input("Enter grant code:")
        sub_name = st.text_input("Enter sub name:")
        p_i = st.text_input("Enter PI (Principal Investigator):")
    
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.write("submitted data:", iga, project_number, project_title, sub_number, grant_code, sub_name, p_i)