import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import numpy as np

img = Image.open('images/ICTlogo.png')
st.image(img)

excel_file = 'processed.xlsx'

df = pd.read_excel(excel_file)
df = df.drop(df.columns[[0]], axis=1)


all_projects_list = df['Project Number:'].unique().tolist()
project_selected = st.selectbox('Project Number:', all_projects_list)

df_one = pd.DataFrame()
df_one = df[df['Project Number:']==project_selected]
df_one = df_one.transpose()
df_one = df_one.reset_index()
df_one.dropna(inplace=True)
df_one.columns = ['Project Attribute', 'Value']

st.dataframe(df_one)

pie_chart = px.pie(df_one, title= 'Pie chart title', values='Value', names='Project Attribute')

st.plotly_chart(pie_chart)