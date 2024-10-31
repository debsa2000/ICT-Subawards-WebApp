import streamlit as st
import mysql.connector as connection
import pandas as pd


def invoice_page_func():

    try:
        mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
        query1 = "SELECT * FROM project;"
        result_df = pd.read_sql(query1,mydb)
        existing_projects_list = result_df['project_number'].unique().tolist()
        mydb.close()
    except Exception as e:
        mydb.close()
        st.write(str(e))
    
    with st.form("add_new_invoice_form"):
        st.write("Add new invoice")
        
        inv_project = st.selectbox('Select existing project that invoice belongs to:', existing_projects_list)
        inv_number = st.number_input("Enter invoice number: ", step=1)
        inv_start_date = st.date_input("Select start date for invoice billing period:", format="MM-DD-YYYY", value=None)
        inv_end_date = st.date_input("Select end date for invoice billing period:", format="MM-DD-YYYY", value=None)      
        inv_amount = st.text_input("Enter invoice amount in USD:")
        inv_cost_share = st.text_input("Enter cost share amount for this invoice in USD:")
        
        final = st.checkbox("This is the final invoice")
        if final:
            inv_final=1
        else:
            inv_final=0

        uploaded_file = st.file_uploader("Upload invoice pdf:")

        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.write("Project?", inv_project, "Inv number", inv_number, "Start date", inv_start_date, "End date", inv_end_date, "Inv $", inv_amount, "Inv Cost Share", inv_cost_share, "Final?", inv_final)

    try:
        mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
        mycursor = mydb.cursor()
        query = "INSERT INTO invoice (invoice_number, start_date, end_date, invoice_amount, cost_share, final, proj_ref) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        val = (inv_number, inv_start_date, inv_end_date, inv_amount, inv_cost_share, inv_final, inv_project)
        mycursor.execute(query, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        mydb.close() #close the connection
    except Exception as e:
        mydb.close()
        st.write(str(e))