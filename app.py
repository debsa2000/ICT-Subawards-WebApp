import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from preprocessing import get_dataframe
from streamlit_navigation_bar import st_navbar

page_names=['Project View','Analytics']
logopath="images/ICTlogo.svg"
# styles = {
#     "nav": {
#         "background-color": " #FF5F05",
#         "justify-content": "left",
#     }
# }
nav_bar = st_navbar(pages=page_names, logo_path=logopath)

df = get_dataframe()

all_projects_list = df['Project Number:'].unique().tolist()
project_selected = st.selectbox('Project Number:', all_projects_list)

df_one = pd.DataFrame()
df_one = df[df['Project Number:']==project_selected]
df_one = df_one.transpose()
df_one = df_one.reset_index()
# df_one.dropna(inplace=True)
df_one.columns = ['Project Attribute', 'Value']
df_one = df_one[df_one['Value'].notna()]

st.dataframe(df_one.astype(str))

years_selected = st.multiselect("Select years to show pie chart",["2018", "2019", "2020", "2021", "2022", "2023", "2024"], default=["2018", "2019", "2020", "2021", "2022", "2023", "2024"])

def check_empty_plot(figure):
    def check_plot(plot):
        # for plots like area, bar, violin and timeline
        if "x" in plot and plot["x"] is None:
            return True
        # for plots like choropleth
        elif "z" in plot and len(plot["z"]) == 0:
            return True
        # for plots like sunburst and treemap
        elif "values" in plot and plot["values"] is None:
            return True
        # for plots like line_mapbox
        elif "lat" in plot and len(plot["lat"]) == 0:
            return True
        return False

    # check if it is an empty go.Figure
    if figure.data == tuple():
        return True
    return all(check_plot(plot) for plot in figure.data)

for e in years_selected:
    if e=="2018":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2018", "Cost Share FY2018", "IDOT Sub Admin Cost FY2018"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==False:
            st.plotly_chart(pie_chart)
    if e=="2019":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2019", "Cost Share FY2019", "IDOT Sub Admin Cost FY2019"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==False:
            st.plotly_chart(pie_chart)
    if e=="2020":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2020", "Cost Share FY2020", "IDOT Sub Admin Cost FY2020"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==True:
            st.plotly_chart(pie_chart)
    if e=="2021":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2021", "Cost Share FY2021", "IDOT Sub Admin Cost FY2021"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==True:
            st.plotly_chart(pie_chart)
    if e=="2022":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2022", "Cost Share FY2022", "IDOT Sub Admin Cost FY2022"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==True:
            st.plotly_chart(pie_chart)
    if e=="2023":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2023", "Cost Share FY2023", "IDOT Sub Admin Cost FY2023"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==True:
            st.plotly_chart(pie_chart)
    if e=="2024":
        df_one_year = df_one[df_one['Project Attribute'].isin(["IDOT Share FY2024", "Cost Share FY2024", "IDOT Sub Admin Cost FY2024"])]
        pie_chart = px.pie(df_one_year, values='Value', names='Project Attribute')
        if check_empty_plot(pie_chart)==True:
            st.plotly_chart(pie_chart)


with st.form("add_new_invoice_form"):
    st.write("Add new invoice")
    
    inv_start_date = st.date_input("Select start date for invoice billing period:", format="MM-DD-YYYY", value=None)
    inv_end_date = st.date_input("Select end date for invoice billing period:", format="MM-DD-YYYY", value=None)
    print(inv_start_date, inv_start_date)
    
    invoice_amount = st.text_input("Enter invoice amount:")
    print(invoice_amount)
    
    invoice_cost_share = st.text_input("Enter invoice cost share amount:")
    print(invoice_cost_share)
   
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write("Start date", inv_start_date, "End date", inv_end_date, "Inv $", invoice_amount, "Inv Cost Share", invoice_cost_share)