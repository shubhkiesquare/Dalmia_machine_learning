import pandas as pd
import numpy as np
from datetime import datetime
import psycopg2
@st.cache_data

## Read all the require data from DB
def read_all():
    conn_string = "host='database-dalmia.cms6cet2hwec.ap-south-1.rds.amazonaws.com' dbname='dalmia_digital' user='postgres' password='dalmia123'"
    conn_2 = psycopg2.connect(conn_string)
    df1= pd.read_sql_query("select sales_region, sales_zone,sold_to_party_district_name, billing_date, sold_to_party_code,sales_type, bill_quantity from dalmia_sales.sales_data where (billing_date > '2022-01-01' AND brand = 'DALMIA') AND (sold_to_party_code > 7*10^6 AND sold_to_party_code < 71*10^5) AND (bill_quantity >= 0 AND sales_type = 'Trade')",  conn_2)
    df2= pd.read_sql_query("select * from dalmia_sales.sales_pd_wsp", conn_2)
    df3= pd.read_sql_query("select * from dalmia_sales.south_sales_pd_wsp", conn_2)
    return df1,df2,df3

## Data Cleaning 
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
    
    ## WSP Data: South
    d3 = df3[df3['segment']=='Trade'].copy() 
    d3['billing_date']=pd.to_datetime(d3['billing_date'], infer_datetime_format=True, format='mixed' )
    d3['SH_Location']=df3['state']
    # State re-define
    d3['state'] = d3['state'].replace('Karnataka North','Karnataka')
    d3['state'] = d3['state'].replace('Karnataka South','Karnataka')
    d3['state'] = d3['state'].replace('TN1','Tamil Nadu')
    d3['state'] = d3['state'].replace('TN2','Tamil Nadu')
    d3['state'] = d3['state'].replace('TN3','Tamil Nadu')
    d3['state'] = d3['state'].replace('Maharashtra-A','Maharashtra')
    d3['state'] = d3['state'].replace('Maharashtra-B','Maharashtra')

    # SH Location re-define
    d3['SH_Location'] = d3['SH_Location'].replace('Karnataka North','KAN')
    d3['SH_Location'] = d3['SH_Location'].replace('Karnataka South','KAS')
    d3['SH_Location'] = d3['SH_Location'].replace('Telangana','TLG')
    d3['SH_Location'] = d3['SH_Location'].replace('Maharashtra-A','MHA')
    d3['SH_Location'] = d3['SH_Location'].replace('Maharashtra-B','MHB')
    d3['SH_Location'] = d3['SH_Location'].replace('Maharashtra','MH')
    d3['SH_Location'] = d3['SH_Location'].replace('Andhra Pradesh','ANDH PRD')
    d3['SH_Location'] = d3['SH_Location'].replace('Andaman','Others-S')

    selected_columns = ['state', 'SH_Location', 'district', 'billing_date', 'dalmia_wsp', 'ut_wsp']
    d3 = d3[selected_columns].copy()
    d3.rename(columns={'state': 'State', 'sh_location' : 'SH_Location', 'district': 'District', 'billing_date':'Date', 'dalmia_wsp':'DAL WSP', 'ut_wsp':'UT WSP'}, inplace=True)
    d3['DAL WSP'] = d3.groupby(['State','SH_Location', 'District', 'Date'])['DAL WSP'].transform('sum')
    d3['UT WSP'] = d3.groupby(['State','SH_Location', 'District', 'Date'])['UT WSP'].transform('sum')

    # Deal with NaN
    d3['DAL WSP'] = d3.groupby(['State', 'SH_Location', 'District'])['DAL WSP'].fillna(method='ffill').fillna(method='bfill')
    d3['UT WSP'] = d3.groupby(['State', 'SH_Location', 'District'])['UT WSP'].fillna(method='ffill').fillna(method='bfill')
    d3['District'] = d3['District'].str.upper()
    d3.sort_values(['State', 'SH_Location', 'District', 'Date'], inplace=True)
    
    ## Combine WSP Data and Sales Data 
    df_east = pd.merge(a3,d2, how='inner',left_on=['District', 'Date'],right_on=['District', 'Date'])
    df_east1= df_east[df_east['Sales_Region']=='East'].copy()
    df_south = pd.merge(a3,d3, how='inner',left_on=['District', 'Date'],right_on=['District', 'Date'])
    df_south1= df_south[df_south['Sales_Region']=='South'].copy()
    df = df_east1._append(df_south1, ignore_index=True)
    selected_cols= ['Sales_Region', 'State', 'SH_Location', 'District', 'Date', 'Dealers', 'DAL WSP', 'UT WSP', 'Volume']
    df= df[selected_cols].copy()
    df.sort_values(['Sales_Region', 'State', 'SH_Location', 'District', 'Date'], inplace=True)
        
    ## Price Index Caluclation Weekly
    # df_east['Year-Week'] = df_east['Date'].dt.strftime('%Y-%U')
    df['Year-Month'] = df['Date'].dt.strftime('%Y-%m')
    w1 = df.groupby(['Sales_Region','State', 'SH_Location', 'District', 'Year-Month'], as_index=False).apply(lambda group: pd.Series({
    'Monthly_UT WSP': ((group['UT WSP'] * group['Volume']).sum()) / group['Volume'].sum(),
    'Monthly_Volume': group['Volume'].sum(), 'Monthly_Dealers': group['Dealers'].sum()
    }))
    w2 = df.groupby(['Sales_Region','State', 'SH_Location', 'District', 'Year-Month'], as_index=False).apply(lambda group: pd.Series({
        'Monthly_DAL WSP': ((group['DAL WSP'] * group['Volume']).sum()) / group['Volume'].sum()
    }))
    w=pd.merge(w2,w1, how='inner',left_on=['Sales_Region', 'State', 'SH_Location', 'District','Year-Month'],right_on=['Sales_Region', 'State', 'SH_Location', 'District', 'Year-Month'])
    w.sort_values(by=['Sales_Region', 'State', 'SH_Location', 'District', 'Year-Month'], inplace=True)
    w['Price_Index'] = w['Monthly_DAL WSP']/w['Monthly_UT WSP']
    return w