import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
from datetime import datetime
import psycopg2
@st.cache_data
def read_all():
    conn_string = "host='database-dalmia.cms6cet2hwec.ap-south-1.rds.amazonaws.com' dbname='dalmia_digital' user='postgres' password='dalmia123'"
    conn_2 = psycopg2.connect(conn_string)
    df1= pd.read_sql_query("select sales_region, sales_zone,sold_to_party_district_name, billing_date, sold_to_party_code,sales_type, bill_quantity from dalmia_sales.sales_data where (billing_date > '2022-01-01' AND brand = 'DALMIA') AND (sold_to_party_code > 7*10^6 AND sold_to_party_code < 71*10^5) AND (bill_quantity >= 0 AND sales_type = 'Trade')",  conn_2)
    df2= pd.read_sql_query("select * from dalmia_sales.sales_pd_wsp", conn_2)
    df3= pd.read_sql_query("select * from dalmia_sales.south_sales_pd_wsp", conn_2)
    df4= pd.read_sql_query("select * from dalmia_sales.dap_data_sow", conn_2)
    return df1,df2,df3,df4
# @st.clear_cache