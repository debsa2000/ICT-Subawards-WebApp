import streamlit as st

def add_invoice_func():
    
    with st.form("add_new_invoice_form"):
        st.write("Add new invoice")
        
        inv_start_date = st.date_input("Select start date for invoice billing period:", format="MM-DD-YYYY", value=None)
        inv_end_date = st.date_input("Select end date for invoice billing period:", format="MM-DD-YYYY", value=None)
        # print(inv_start_date, inv_start_date)
        
        invoice_amount = st.text_input("Enter invoice amount:")
        # print(invoice_amount)
        
        invoice_cost_share = st.text_input("Enter invoice cost share amount:")
        # print(invoice_cost_share)
    
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.write("Start date", inv_start_date, "End date", inv_end_date, "Inv $", invoice_amount, "Inv Cost Share", invoice_cost_share)