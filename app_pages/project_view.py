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
    
    query_get_existing_igas = "SELECT * FROM iga;"
    df_igas = pd.read_sql(query_get_existing_igas,mydb)
    # print(df_igas)
    iga_fy_ranges = []
    for i,row in df_igas.iterrows():
        start_year=row['iga_start_year']
        end_year=row['iga_end_year']
        fy_range= "FY" + str(start_year) + "-FY" + str(end_year)
        iga_fy_ranges.append(fy_range)
    # print(iga_fy_ranges)
    selected_iga_fy_range= st.selectbox('Select IGA:', iga_fy_ranges)
    # print(selected_iga_fy_range)
    
    for i,row in df_igas.iterrows():
        if row['iga_fy_range']==selected_iga_fy_range:
            selected_iga_code=row['iga_code']

    query_projects_in_selected_iga = "SELECT project_number FROM project where iga_ref=" + str(selected_iga_code) + ";"
    result_projects_in_selected_iga = pd.read_sql(query_projects_in_selected_iga,mydb)
    existing_projects = result_projects_in_selected_iga['project_number'].tolist()

    if len(existing_projects)==0:
        st.write("No projects added yet for currently selected IGA.")
        return
    else:
        selected_project = st.selectbox('Select Project:', existing_projects)
        # print(selected_project)
    
    query_selected_project = "SELECT * FROM project WHERE project_number='" + str(selected_project) + "' and iga_ref=" + str(selected_iga_code) + ";"
    df_selected_project= pd.read_sql(query_selected_project,mydb)
    # print(df_selected_project)

    st.write("")

    st.subheader("Project Details")

    st.write("Project Title : ", df_selected_project['project_title'][0])
    st.write("Subaward # : ", df_selected_project['sub_number'][0])
    st.write("Grant Code: ",df_selected_project['grant_code'][0])
    st.write("Sub : ", df_selected_project['sub_name'][0])
    st.write("Principal Investigator: ", df_selected_project['p_i'][0])

    st.write("")

    # Chart 1

    st.subheader("Total Project Budget for IGA " + selected_iga_fy_range)

    query_get_project_budgets = "SELECT * FROM budget WHERE project_ref='" + selected_project + "'"
    df_budgets = pd.read_sql(query_get_project_budgets,mydb)
    df_budgets = df_budgets.drop(['project_ref'], axis=1)

    df_budgets_styler = df_budgets.style.format({"idot_share": lambda x : '$ {:,.2f}'.format(x),
                                          "cost_share": lambda x : '$ {:,.2f}'.format(x),
                                          "subadmin_cost": lambda x : '$ {:,.2f}'.format(x),
                                          "total_budget": lambda x : '$ {:,.2f}'.format(x)})
    st.dataframe(df_budgets_styler,
                 hide_index=True,
                 column_config={"fy": st.column_config.NumberColumn("FY", format="%d"),
                                "idot_share" : "IDOT share",
                                "cost_share": "Cost share",
                                "subadmin_cost": "Sub-Admin cost",
                                "total_budget": "Total budget for year"})
    
    df_pie1 = pd.DataFrame(columns=['label','value'])

    sum_idot_shares=0

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

    fig1 = px.pie(df_pie1, values='value', names='label')
    fig1.update_traces(textinfo='value+percent+label')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1)

    st.write("")

    # Chart 2

    st.subheader("Current Invoicing Status")

    query_get_invoices = "SELECT * FROM invoice WHERE proj_ref='" + selected_project + "'"
    df_invoices = pd.read_sql(query_get_invoices,mydb)
    df_invoices = df_invoices.drop(['proj_ref'], axis=1)
    # st.dataframe(df_invoices)

    query_sum_invoices = "SELECT SUM(invoice_amount) FROM invoice WHERE proj_ref='" + selected_project + "'"
    sum_invoice_amounts = pd.read_sql(query_sum_invoices,mydb)
    sum_invoices = round(sum_invoice_amounts.iloc[0][0],2)
    # print(sum_invoices)
    # print(sum_idot_shares)

    df_pie2 = pd.DataFrame(columns=['label','value'])
    df_pie2 = df_pie2._append({'label': 'Total invoiced amount', 'value': sum_invoices}, ignore_index=True)
    df_pie2 = df_pie2._append({'label': 'Amount available to invoice', 'value': sum_idot_shares-sum_invoices}, ignore_index=True)
    st.dataframe(df_pie2)

    fig2 = px.pie(df_pie2, values='value', names='label')
    fig2.update_traces(textposition='outside', textinfo='value+percent+label')
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2)


    # Chart 3

    st.header("Cost Share Status")

    query_sum_cost_shares = "SELECT SUM(cost_share) FROM invoice WHERE proj_ref='" + selected_project + "'"
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
    fig3.update_layout(xaxis_title="Cost Share", yaxis_title="Amount in $")
    st.plotly_chart(fig3)


    mydb.close()