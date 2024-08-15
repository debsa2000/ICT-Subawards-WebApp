import pandas as pd
import warnings
warnings.filterwarnings("ignore")

excel_file = 'Subawards Under FY18-FY24 IGA.xlsx'

data = pd.read_excel(excel_file)

for i, col in enumerate(data.columns):
  if col.startswith('FY20'):
    data.iloc[0,i]=data.iloc[0,i]+ ' ' + str(col)
    data.iloc[0,i+1]=data.iloc[0,i+1]+ ' ' + str(col)
    data.iloc[0,i+2]=data.iloc[0,i+2]+ ' ' + str(col)
    data.iloc[0,i+3]=data.iloc[0,i+3]+ ' ' + str(col)

for i, col in enumerate(data.columns):
  if pd.isnull(data.loc[0,col]):
    data.loc[0,col]=""
    data.loc[0,col]=str(col)

new_header = data.iloc[0] #grab the first row for the header
data = data[1:] #take the data less the header row
data.columns = new_header

data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

data = data[data['Project Number:'].notna()]

def get_dataframe():
    dataframe=data
    return dataframe