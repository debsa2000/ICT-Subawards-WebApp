import streamlit as st
import mysql.connector as connection
import pandas as pd
import datetime

def iga_page_func():
    try:
        mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                database = 'dbmaster_deb',
                                user="subaward_user",
                                passwd="ict_use_webapp",
                                use_pure=True)
    except Exception as e:
        st.write(str(e))
    
    st.subheader("Existing IGAs:")
    query1 = "SELECT * FROM iga;"
    igas = pd.read_sql(query1, mydb, index_col=['iga_code'])
    df_igas = igas.style.format({"iga_subaward_total": lambda x : '$ {:,.2f}'.format(x)})
    no_of_igas = len(df_igas.index)

    st.table(df_igas)
                #  hide_index=True,
                #  column_config={"iga_code": "IGA code",
                #                 "iga_fy_range" : "IGA FY range",
                #                 "iga_subaward_total": st.column_config.NumberColumn("IGA Subaward Total"),
                #                 "iga_start_year": st.column_config.NumberColumn("IGA start year", format="%d"),
                #                 "iga_end_year": st.column_config.NumberColumn("IGA end year", format="%d")})
    
    # Add new IGA form:
    with st.form("add_new_iga"):
        st.subheader("Add new IGA:")
        query2 = "SELECT COUNT(*) FROM iga;"
        count_igas = pd.read_sql(query2,mydb)
        no_of_igas = int(count_igas.iloc[0][0])

        this_year = datetime.date.today().year
        iga_start_year = st.selectbox("Select IGA start year:", range(2024, this_year+30, 1), index=None, placeholder="Select start year")
        iga_end_year = st.selectbox("Select IGA end year:", range(2024, this_year+30, 1), index=None, placeholder="Select end year")
        iga_subaward_total = st.number_input("Enter total subaward amount for new IGA: ", step=0.01)
        iga_code = no_of_igas+1
        iga_fy_range = "FY"+str(iga_start_year)+"-FY"+str(iga_end_year)
        
        submitted = st.form_submit_button("Submit IGA")
        
        if submitted:
            # print(new_iga_code, new_iga_start_year, new_iga_end_year, new_iga_total_subaward)
            mycursor = mydb.cursor()
            query_insert = "INSERT INTO iga (iga_code, iga_fy_range, iga_subaward_total, iga_start_year, iga_end_year) VALUES (%s, %s, %s, %s, %s);"
            val = (iga_code, iga_fy_range, iga_subaward_total, iga_start_year, iga_end_year)
            mycursor.execute(query_insert, val)
            mydb.commit()

    # Edit existing IGA form
    st.subheader("Edit existing IGA:")

    existing_igas =  igas['iga_fy_range'].to_list()
    selected_iga = st.selectbox('Choose IGA to be edited:', existing_igas)

    edit_iga = igas[igas['iga_fy_range'] == selected_iga]
    edit_iga = edit_iga.astype(str)
    edit_iga = edit_iga.transpose()
    edit_iga = edit_iga.reset_index()
    edit_iga.columns = ['IGA details','Current Value']
    st.dataframe(edit_iga, hide_index=True, width=500)

    changeable_attributes= edit_iga['IGA details'].tolist()
    changeable_attributes.remove('iga_fy_range')
    selected_changes = st.multiselect("Choose which attributes to change:", changeable_attributes)

    for attribute in selected_changes:
        if attribute=='iga_subaward_total':
            new_iga_subaward_total = st.number_input("Change total subaward amount to (in USD): ", step=0.01)
        if attribute=='iga_start_year':
            new_iga_start_year = st.selectbox("Change IGA start year to:", range(2024, this_year+30, 1), index=None)
        if attribute=='iga_end_year':
            new_iga_end_year = st.selectbox("Change IGA start year to:", range(2024, this_year+30, 1), index=None)

    
    mydb.close()