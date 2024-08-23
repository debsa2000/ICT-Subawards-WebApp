import streamlit as st
import preprocessing
import plotly.express as px

def project_view_func():
    df = preprocessing.get_dataframe()
    df.rename(columns={ df.columns[6]: "FY18-FY24 Subaward Total" }, inplace = True)

    all_projects_list = df['Project Number:'].unique().tolist()
    project_selected = st.selectbox('Project Number:', all_projects_list)

    df_one = df[df['Project Number:']==project_selected]
    df_one = df_one.transpose()
    df_one = df_one.reset_index()
    df_one.columns = ['Project Attribute', 'Value']
    df_one = df_one[df_one['Value'].notna()]

    st.dataframe(df_one.astype(str))

    sum_IDOTShare = 0
    sum_CostShare = 0
    sum_IDOTSubAdminCost = 0
    for i, row in df_one.iterrows():
        if "IDOT Share FY" in row['Project Attribute']:
            sum_IDOTShare = sum_IDOTShare+row['Value']
            # print("sum_IDOTShare:", sum_IDOTShare)
        if "Cost Share FY" in row['Project Attribute']:
            sum_CostShare = sum_CostShare+row['Value']
            # print("sum_CostShare:", sum_CostShare)
        if "IDOT Sub Admin Cost FY" in row['Project Attribute']:
            sum_IDOTSubAdminCost = sum_IDOTSubAdminCost+row['Value']
            # print("sum_IDOTSubAdminCost:", sum_IDOTSubAdminCost)

    #Pie 1
    total_sum=sum_IDOTShare+sum_CostShare+sum_IDOTSubAdminCost
    total_allocated_budget = df_one.loc[6, 'Value']

    pie_chart_1 = px.pie(title="Total Project Budget breakup", values=[sum_IDOTShare, sum_CostShare, sum_IDOTSubAdminCost],
                        names=['sum_IDOTShare', 'sum_CostShare', 'sum_IDOTSubAdminCost'])
    pie_chart_1.update_traces(textposition='outside', textinfo='percent+label')
    pie_chart_1.update_layout(showlegend=False)
    st.plotly_chart(pie_chart_1, use_container_width=True)

    if total_sum==total_allocated_budget:
        st.text("FY18-24 Subaward Total is equal to IDOT share + Cost share + Subadmin cost")
    else:
        st.text("FY18-24 Subaward Total is not equal to IDOT share + Cost share + Subadmin cost")

    #Pie 2
    total_expenditure_to_date = df_one.loc[df_one['Project Attribute']=="Total Bills Recd. to Date"]['Value'].item()
    total_visible_to_sub = sum_IDOTShare+sum_CostShare

    pie_chart_2 = px.pie(title="Total Obligated Subaward Costs", values=[total_expenditure_to_date/total_visible_to_sub, 1-total_expenditure_to_date/total_visible_to_sub],
                        names=['total spent to date of total visible to sub','amount left to be utlized'])
    pie_chart_2.update_traces(textposition='outside', textinfo='percent+label')
    pie_chart_2.update_layout(showlegend=False)
    st.plotly_chart(pie_chart_2, use_container_width=True)

    #Pie 3
    cost_share_required_to_date = total_expenditure_to_date/3
    cost_share_done_to_date = df_one.loc[df_one['Project Attribute']=="Cost Share Recd. To Date"]['Value'].item()

    if cost_share_done_to_date<=cost_share_required_to_date:
        pie_chart_3 = px.pie(values=[cost_share_done_to_date/cost_share_required_to_date, 1-cost_share_done_to_date/cost_share_required_to_date],
                        names=['current cost share','remaining cost share required'])
        pie_chart_3.update_traces(textposition='outside', textinfo='percent+label')
        pie_chart_3.update_layout(showlegend=False)
        st.plotly_chart(pie_chart_3, use_container_width=True)
    else:
        st.text("Cost share recorded to date exceeds cost share required according to expenditure to date.")

    #Pie 4
    itd_exp = df_one.loc[df_one['Project Attribute']=="Total Bills Recd. to Date"]['Value'].item()

    year_selected = st.selectbox("Select year until when you want to view budget",("2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026","2027"))