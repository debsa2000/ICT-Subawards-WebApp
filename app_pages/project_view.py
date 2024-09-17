import streamlit as st
import mysql.connector as connection
import pandas as pd
import plotly.express as px
import warnings
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

def project_view_func():

    mydb = connection.connect(host="ls-0d272b6d055951932dd7f1404e6322222517d8bd.caoof4uxeqnq.us-east-1.rds.amazonaws.com",
                                  database = 'dbmaster_deb',
                                  user="subaward_user",
                                  passwd="ict_use_webapp",
                                  use_pure=True)
    query_get_igas = "SELECT * FROM iga;"
    result_igas = pd.read_sql(query_get_igas,mydb)
    existing_igas = result_igas['iga_fy_range'].unique().tolist()
    selected_iga= st.selectbox('Select IGA:', existing_igas)
    # print(selected_iga)

    query_get_project_numbers = "SELECT project_number FROM project;"
    result_project_numbers = pd.read_sql(query_get_project_numbers,mydb)
    existing_projects_list = result_project_numbers['project_number'].unique().tolist()
    selected_project = st.selectbox('Select Project:', existing_projects_list)
    # print(selected_project)
    
    query_get_all_projects_data = "SELECT * FROM project;"
    df_all= pd.read_sql(query_get_all_projects_data,mydb)
    df_selected = df_all[df_all['project_number']==selected_project]

    query_get_all_projects_data = "SELECT * FROM project;"
    df_all= pd.read_sql(query_get_all_projects_data,mydb)
    df_selected = df_all[df_all['project_number']==selected_project]


    st.write("Project Title : ", df_selected.iloc[0][2])
    st.write("Subaward # : ", df_selected.iloc[0][3])
    st.write("Grant Code: ", df_selected.iloc[0][4])
    st.write("Sub : ", df_selected.iloc[0][5])
    st.write("Principal Investigator: ", df_selected.iloc[0][6])

    sum_idot_shares=0


    # Chart 1

    query_get_project_budgets = "SELECT * FROM budget WHERE project_ref='" + selected_project + "'"
    df_budgets = pd.read_sql(query_get_project_budgets,mydb)
    df_budgets = df_budgets.drop(['project_ref'], axis=1)
    st.dataframe(df_budgets)
    df_pie1 = pd.DataFrame(columns=['label','value'])
    for i,row in df_budgets.iterrows():
        fy=str(row['fy'])[:-2]

        idot_share=row['idot_share']
        sum_idot_shares += idot_share
        label_idot_share="idot_share_"+ fy
        new_row = {'label': label_idot_share, 'value': idot_share}
        df_pie1 = df_pie1._append(new_row, ignore_index=True)

        cost_share=row['cost_share']
        label_cost_share="cost_share_"+ fy
        new_row = {'label': label_cost_share, 'value': cost_share}
        df_pie1 = df_pie1._append(new_row, ignore_index=True)

        subadmin_cost=row['subadmin_cost']
        label_subadmin_cost="subadmin_cost_"+ fy
        new_row = {'label': label_subadmin_cost, 'value': subadmin_cost}
        df_pie1 = df_pie1._append(new_row, ignore_index=True)
        
        # print(i, fy, idot_share, cost_share, subadmin_cost)

    st.dataframe(df_pie1)

    fig1 = px.pie(df_pie1, values='value', names='label', title='Initial allocation of total project budget for selected IGA')
    fig1.update_traces(textinfo='value+percent+label')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1)


    # Chart 2

    query_get_invoices = "SELECT * FROM invoice WHERE proj_ref='" + selected_project + "'"
    df_invoices = pd.read_sql(query_get_invoices,mydb)
    df_invoices = df_invoices.drop(['proj_ref'], axis=1)
    st.dataframe(df_invoices)

    query_sum_invoices = "SELECT SUM(invoice_amount) FROM invoice WHERE proj_ref='" + selected_project + "'"
    sum_invoice_amounts = pd.read_sql(query_sum_invoices,mydb)
    sum_invoices = round(sum_invoice_amounts.iloc[0][0],2)
    # print(sum_invoices)
    # print(sum_idot_shares)

    df_pie2 = pd.DataFrame(columns=['label','value'])
    df_pie2 = df_pie2._append({'label': 'spent', 'value': sum_invoices}, ignore_index=True)
    df_pie2 = df_pie2._append({'label': 'available to spend', 'value': sum_idot_shares-sum_invoices}, ignore_index=True)
    st.dataframe(df_pie2)

    fig2 = px.pie(df_pie2, values='value', names='label', title='Total obligated to date (for all years irrespective of IGA)')
    fig2.update_traces(textposition='outside', textinfo='value+percent+label')
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2)


    # Chart 3

    query_sum_cost_shares = "SELECT SUM(invoice_amount) FROM invoice WHERE proj_ref='" + selected_project + "'"
    sum_cost_share_amounts = pd.read_sql(query_sum_cost_shares,mydb)
    sum_cost_shares= round(sum_cost_share_amounts.iloc[0][0],2)
    # print(sum_cost_shares)
    cost_share_required = sum_invoices/3
    # print(cost_share_required)

    df_bar1 = pd.DataFrame(columns=['label','value'])
    df_bar1 = df_bar1._append({'label': 'cost share commited till last invoice', 'value': sum_cost_shares}, ignore_index=True)
    df_bar1 = df_bar1._append({'label': 'cost share required till last invoice', 'value': cost_share_required}, ignore_index=True)
    fig3 = go.Figure(data=[go.Bar(x=['cost share commited till last invoice','cost share required till last invoice'],
                                  y=[sum_cost_shares,cost_share_required], 
                                  text=[round(sum_cost_shares,2),round(cost_share_required,2)],
                                  textposition="outside")])
    fig3.update_layout(title="Cost Share Status", xaxis_title="Cost Share", yaxis_title="Amount in $")
    st.plotly_chart(fig3)


    mydb.close()
    



    # df = preprocessing.get_dataframe()
    
    # iga_selected = st.selectbox("Select IGA: ",("FY 2018 - 2024", "FY 2025 - 2030"))


    # all_projects_list = df['Project Number:'].unique().tolist()
    # project_selected = st.selectbox('Project Number:', all_projects_list)

    # df_one = df[df['Project Number:']==project_selected]
    # df_one = df_one.transpose()
    # df_one = df_one.reset_index()
    # df_one.columns = ['Project Attribute', 'Value']
    # df_one = df_one[df_one['Value'].notna()]

    # st.write("Project Title : ", df_one.iloc[1][1])
    # st.write("Subaward # : ", df_one.iloc[2][1])
    # st.write("Grant Code: ", df_one.iloc[3][1])
    # st.write("Sub : ", df_one.iloc[4][1])
    # st.write("Principal Investigator: ", df_one.iloc[5][1])

    # st.dataframe(df_one.astype(str), use_container_width=True, hide_index=True)