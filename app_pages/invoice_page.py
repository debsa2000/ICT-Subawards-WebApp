import streamlit as st
import mysql.connector as connection
import pandas as pd
import datetime
import sys

def invoice_page_func():
    try:
        mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
    except Exception as e:
        st.write(str(e))
    
    query1 = "SELECT * FROM project;"
    result_df = pd.read_sql(query1,mydb)
    existing_projects_list = result_df['project_number'].unique().tolist()  
    inv_project = st.selectbox('Select existing project to get invoices:', existing_projects_list)

    query2 = "SELECT * FROM invoice WHERE proj_ref='" + str(inv_project) + "';"
    existing_invoices = pd.read_sql(query2,mydb, index_col=['invoice_number'])
    st.table(existing_invoices)

    query3 = "SELECT COUNT(*) FROM invoice WHERE proj_ref='" + str(inv_project) + "';"
    count_invoices = pd.read_sql(query3,mydb)
    # print(count_invoices.iloc[0][0])

    query4 = "SELECT end_date FROM invoice WHERE proj_ref='" + str(inv_project) + "' ORDER BY invoice_number DESC LIMIT 1;"
    latest_end_date = pd.read_sql(query4,mydb)
    # print(latest_end_date.iloc[0][0])
    # print(type(latest_end_date.iloc[0][0]))
    # print(latest_end_date.iloc[0][0] + datetime.timedelta(days=1))
    
    with st.form("add_new_invoice_form"):
        st.subheader("Add new invoice")

        inv_number = int(count_invoices.iloc[0][0]) + 1
        inv_start_date = latest_end_date.iloc[0][0] + datetime.timedelta(days=1)
        inv_end_date = st.date_input("Select end date for the new invoice billing period:", format="MM-DD-YYYY", value=None)
        inv_amount = st.number_input("Enter invoice amount in USD:")
        inv_cost_share = st.number_input("Enter cost share amount for this invoice in USD:")
        
        final = st.checkbox("This is the final invoice")
        if final:
            inv_final=1
        else:
            inv_final=0

        uploaded_file = st.file_uploader("Upload invoice pdf:")

        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # st.write("Project?", inv_project, "Inv number", inv_number, "Start date", inv_start_date, "End date", inv_end_date, "Inv $", inv_amount, "Inv Cost Share", inv_cost_share, "Final?", inv_final)
            mycursor = mydb.cursor()
            query = "INSERT INTO invoice (invoice_number, start_date, end_date, invoice_amount, cost_share, final, proj_ref) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            val = (inv_number, inv_start_date, inv_end_date, inv_amount, inv_cost_share, inv_final, inv_project)
            mycursor.execute(query, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")

    # Edit existing invoice
    st.subheader("Edit existing invoice:")
    edit_invoices = pd.read_sql(query2,mydb)
    selected_invoice = st.selectbox("Select invoice to edit:", edit_invoices)

    query5= "SELECT * FROM invoice WHERE proj_ref='" + str(inv_project) + "' AND invoice_number=" + str(selected_invoice) + ";"
    edit_invoice = pd.read_sql(query5,mydb)
    edit_invoice = edit_invoice.astype(str)
    edit_invoice = edit_invoice.transpose()
    edit_invoice = edit_invoice.reset_index()
    edit_invoice.columns = ['Invoice details','Current Value']
    st.dataframe(edit_invoice, hide_index=True, width=500)

    changeable_attributes= edit_invoice['Invoice details'].tolist()
    changeable_attributes.remove('proj_ref')
    changeable_attributes.remove('invoice_number')
    # print(type(changeable_attributes))
    # print(changeable_attributes)
    selected_changes = st.multiselect("Choose which attributes to change:", changeable_attributes)

    for attribute in selected_changes:
        if attribute=='start_date':
            new_start_date = st.date_input("Change start date to:", format="MM-DD-YYYY", value=None)
            # print(new_start_date)

        if attribute=='end_date':
            new_end_date = st.date_input("Change end date to:", format="MM-DD-YYYY", value=None)
            # print(new_end_date)
        
        if attribute=='invoice_amount':
            new_inv_amount = st.number_input("Change invoice amount to (in USD):")
            # print(new_inv_amount)
        
        if attribute=='cost_share':
            new_cost_share = st.number_input("Change cost share amount for this invoice to (in USD):")
            # print(new_cost_share)

        if attribute=='final':
            new_final = st.radio('Make this final invoice', ['Yes','No'])
            if new_final=='Yes':
                new_inv_final=1
            if new_final=='No':
                new_inv_final=0
            # print(new_inv_final)
    
    new_changes_submitted = st.button("Submit Changes")

    # if new_changes_submitted:
        # print("changes submitted clicked")
        # st.write("Project?", inv_project, "Inv number", inv_number, "Start date", inv_start_date, "End date", inv_end_date, "Inv $", inv_amount, "Inv Cost Share", inv_cost_share, "Final?", inv_final)
        # mycursor = mydb.cursor()
        # query = "INSERT INTO invoice (invoice_number, start_date, end_date, invoice_amount, cost_share, final, proj_ref) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        # val = (inv_number, new_start_date, new_end_date, new_inv_amount, new_cost_share, new_inv_final, inv_project)
        # mycursor.execute(query, val)
        # mydb.commit()
        # print(mycursor.rowcount, "record changed.")


    mydb.close()