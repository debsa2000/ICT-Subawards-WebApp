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
        return
    
    query_fetch = "SELECT * FROM iga;"
    iga_table = pd.read_sql(query_fetch,mydb)
    
    st.write("Existing IGAs:")
    df_igas = iga_table.style.format({"iga_subaward_total": lambda x : '$ {:,.2f}'.format(x)})
    no_of_igas = len(df_igas.index)

    st.dataframe(df_igas,
                 hide_index=True,
                 column_config={"iga_code": "IGA code",
                                "iga_fy_range" : "IGA FY range",
                                "iga_subaward_total": st.column_config.NumberColumn("IGA Subaward Total"),
                                "iga_start_year": st.column_config.NumberColumn("IGA start year", format="%d"),
                                "iga_end_year": st.column_config.NumberColumn("IGA end year", format="%d")})
    
    # Add new IGA form:
    with st.form("add_new_iga"):
        st.write("Add new IGA:")
        this_year = datetime.date.today().year
        new_iga_start_year = st.selectbox("Select start year:", range(this_year-20, this_year+30, 1), index=None, placeholder="Select start year")
        new_iga_end_year = st.selectbox("Select end year:", range(this_year-20, this_year+30, 1), index=None, placeholder="Select end year")
        new_iga_total_subaward = st.number_input("Enter total subaward amount for new IGA: ", step=0.01)
        new_iga_code=no_of_igas+1
        new_iga_fy_range = "FY"+str(new_iga_start_year)+"-FY"+str(new_iga_end_year)
        
        submitted = st.form_submit_button("Submit IGA")
        
        if submitted:
            # print(new_iga_code, new_iga_start_year, new_iga_end_year, new_iga_total_subaward)
            mycursor = mydb.cursor()
            query_insert = "INSERT INTO iga (iga_code, iga_fy_range, iga_subaward_total, iga_start_year, iga_end_year) VALUES (%s, %s, %s, %s, %s);"
            val = (new_iga_code, new_iga_fy_range, new_iga_total_subaward, new_iga_start_year, new_iga_end_year)
            mycursor.execute(query_insert, val)
            mydb.commit()

    # Edit existing IGA form
    st.write("Edit existing IGA:")

    existing_igas =  iga_table['iga_fy_range'].to_list()
    selected_iga = st.selectbox('Choose IGA to be edited:', existing_igas)

    iga = iga_table.loc[iga_table['iga_fy_range'] == selected_iga]
    iga=iga.transpose()
    iga=iga.reset_index()
    iga.columns = ['attribute','value']
    iga.set_axis(['attribute', 'value'], axis='columns')
    st.dataframe(iga)
    
    selected = st.multiselect("Choose which attributes to change:", iga['attribute'])
    
    mydb.close()