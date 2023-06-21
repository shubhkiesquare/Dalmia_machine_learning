import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
@st.cache_data
def datamanipulation(df1,df2,df3):
    
    ## Sales Data
    d1=df1.copy()
    d1.rename(columns={'sales_region': 'Sales_Region', 'sold_to_party_district_name' : 'District', 'billing_date': 'Date', 'bill_quantity': 'Volume','sold_to_party_code':'Dealers'}, inplace=True)
    d1.drop('sales_zone', axis=1, inplace=True)
    
    a1 = d1.groupby(['Sales_Region','District', 'Date'],as_index=False)['Dealers'].count()
    a2 = d1.groupby(['Sales_Region','District', 'Date'],as_index=False)['Volume'].sum()
    a3 = pd.merge(a1,a2, how='inner',left_on=['Sales_Region','District', 'Date'],right_on=['Sales_Region','District', 'Date'])
    # a3['Volume'] = a2.groupby(['Sales_Region','District'])['Volume'].fillna(method='ffill').fillna(method='bfill')
    a3.sort_values(by=['Sales_Region','District', 'Date'], inplace=True)
    a3['Sales_Region'] = a3['Sales_Region'].replace('North East', 'NE')
    a3['District'] = a3['District'].str.upper()
    a3['Volume'] = a3['Volume']*12
    
    ## WSP DATA: East
    d2=df2.copy()
    selected_columns = ['state', 'sh_location', 'district_code', 'district', 'date', 'dal_wsp', 'ut_wsp']
    d2 = d2[selected_columns].copy()
    d2.rename(columns={'state': 'State', 'sh_location' : 'SH_Location', 'district_code': 'District_Code', 'district': 'District', 'date':'Date', 'dal_wsp':'DAL WSP', 'ut_wsp':'UT WSP'}, inplace=True)
    d2['DAL WSP'] = d2.groupby(['State','SH_Location', 'District', 'Date'])['DAL WSP'].transform('sum')
    d2['UT WSP'] = d2.groupby(['State','SH_Location', 'District', 'Date'])['UT WSP'].transform('sum')
    def convert_to_integer(value):
        if isinstance(value, str) and '-' in value:
        # If the value is a string and '-' is present, split the value and check if it has a valid format
            parts = value.split('-')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                start, end = int(parts[0]), int(parts[1])
                return int((start + end) / 2)
        # If the value is either an integer or a string without '-', convert it directly into an integer
        try:
            return int(value)
        except ValueError:
            return None
    d2['DAL WSP'] = d2['DAL WSP'].apply(convert_to_integer)
    d2['UT WSP'] = d2['UT WSP'].apply(convert_to_integer)
    # Deal with NaN
    d2['DAL WSP'] = d2.groupby(['State', 'SH_Location', 'District_Code', 'District'])['DAL WSP'].fillna(method='ffill').fillna(method='bfill')
    d2['UT WSP'] = d2.groupby(['State', 'SH_Location', 'District_Code', 'District'])['UT WSP'].fillna(method='ffill').fillna(method='bfill')
    d2.sort_values(['State', 'SH_Location', 'District_Code', 'District', 'Date'], inplace=True)
    
    ## Combine East WSP Data and Sales Data
    
    df_east = pd.merge(a3,d2, how='inner',left_on=['District', 'Date'],right_on=['District', 'Date'])
    selected_cols= ['Sales_Region', 'State', 'SH_Location', 'District', 'District_Code', 'Date', 'Dealers', 'DAL WSP', 'UT WSP', 'Volume']
    df_east= df_east[selected_cols].copy()
    df_east.sort_values(['Sales_Region', 'State', 'SH_Location', 'District', 'District_Code', 'Date'], inplace=True)
    df_east = df_east[df_east['Sales_Region']=='East'].copy()
    
    ## Price Index Caluclation Weekly
    
    df_east['Year-Week'] = df_east['Date'].dt.strftime('%Y-%U')
    df_east['Year-Month'] = df_east['Date'].dt.strftime('%Y-%m')
    w1 = df_east.groupby(['State', 'SH_Location', 'District', 'District_Code', 'Year-Month', 'Year-Week'], as_index=False).apply(lambda group: pd.Series({
    'Weekly_UT WSP': ((group['UT WSP'] * group['Volume']).sum()) / group['Volume'].sum(),
    'Weekly_Volume': group['Volume'].sum(), 'Weekly_Dealers': group['Dealers'].sum()
    }))
    w2 = df_east.groupby(['State', 'SH_Location', 'District', 'District_Code', 'Year-Month', 'Year-Week'], as_index=False).apply(lambda group: pd.Series({
        'Weekly_DAL WSP': ((group['DAL WSP'] * group['Volume']).sum()) / group['Volume'].sum()
    }))
    w_east=pd.merge(w2,w1, how='inner',left_on=['State', 'SH_Location', 'District', 'District_Code','Year-Month', 'Year-Week'],right_on=['State', 'SH_Location', 'District', 'District_Code', 'Year-Month', 'Year-Week'])
    w_east.sort_values(by=['State', 'SH_Location', 'District', 'District_Code', 'Year-Month', 'Year-Week'], inplace=True)
    w_east['Price_Index'] = w_east['Weekly_DAL WSP']/w_east['Weekly_UT WSP']
    w_east.rename(columns={'State':'STATE', 'SH_Location': 'SH Location',
                               'District':'DISTRICT', 'District_Code':'DISTRICT CODE','Weekly_Volume':'Weekly_Dist_Bill_Qty',
                               'Price_Index':'Price_Index_Weekly_Dist', 'Weekly_DAL WSP':'agg_Weekly_Dist_DAL WSP',
                               'Weekly_UT WSP':'agg_Weekly_Dist_UT WSP'}, inplace= True)
    return w_east