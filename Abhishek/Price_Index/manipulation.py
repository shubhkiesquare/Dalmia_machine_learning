import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
@st.cache_data
def manipulation(data):
    selected_columns = ['STATE', 'SH Location', 'DISTRICT CODE', 'DISTRICT', 'Date', 'DAL WSP', 'UT WSP','Bill Qty']
    data1 = data[selected_columns].copy()
    data1 = data1[data1['UT WSP'].notnull() & data1['DAL WSP'].notnull()]
    def convert_to_integer(value):
        if isinstance(value, str) and '-' in value:
            # If the value is a string and '-' is present, split the value and check if it has a valid format
            parts = value.split('-')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                start, end = int(parts[0]), int(parts[1])
                return int((start + end) / 2)
        # If the value is either an integer or a string without '-',
        # convert it directly into an integer
        try:
            return int(value)
        except ValueError:
            return None
        
    data1['DAL WSP'] = data1['DAL WSP'].apply(convert_to_integer)
    data1['UT WSP'] = data1['UT WSP'].apply(convert_to_integer)

    d1 = data1.groupby(['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Date'], as_index=False).apply(lambda group: pd.Series({
        'agg_daily_dist_DAL WSP': ((group['DAL WSP'] * group['Bill Qty']).sum()) / group['Bill Qty'].sum(),
        'Day_Dist_Bill Qty': group['Bill Qty'].sum()
    }))
    d2 = data1.groupby(['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Date'], as_index=False).apply(lambda group: pd.Series({
        'agg_daily_dist_UT WSP': ((group['UT WSP'] * group['Bill Qty']).sum()) / group['Bill Qty'].sum(),
        'Day_Dist_Bill Qty': group['Bill Qty'].sum()
    }))
    d3=pd.merge(d1,d2, how='inner',left_on=['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Date'],right_on=['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Date'])
    d3.sort_values(by=['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Date'], inplace=True)
    d3['Price_Index_Daily_Dist'] = d3['agg_daily_dist_DAL WSP']/d3['agg_daily_dist_UT WSP']
    d3.rename(columns={'Day_Dist_Bill Qty_y': 'Daily_Dist_Bill_Qty'}, inplace=True)
    d3.drop(columns='Day_Dist_Bill Qty_x', axis=1, inplace=True)
    d3['Year-Week'] = d3['Date'].dt.strftime('%Y-%U')

    w1 = d3.groupby(['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Year-Week'], as_index=False).apply(lambda group: pd.Series({
        'agg_Weekly_Dist_DAL WSP': ((group['agg_daily_dist_DAL WSP'] * group['Daily_Dist_Bill_Qty']).sum()) / group['Daily_Dist_Bill_Qty'].sum(),
        'Weekly_Dist_Bill Qty': group['Daily_Dist_Bill_Qty'].sum()
    }))
    w2 = d3.groupby(['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Year-Week'], as_index=False).apply(lambda group: pd.Series({
        'agg_Weekly_Dist_UT WSP': ((group['agg_daily_dist_UT WSP'] * group['Daily_Dist_Bill_Qty']).sum()) / group['Daily_Dist_Bill_Qty'].sum(),
        'Weekly_Dist_Bill Qty': group['Daily_Dist_Bill_Qty'].sum()
    }))
    w3=pd.merge(w1,w2, how='inner',left_on=['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Year-Week'],right_on=['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Year-Week'])
    w3.sort_values(by=['STATE', 'SH Location', 'DISTRICT', 'DISTRICT CODE', 'Year-Week'], inplace=True)
    w3['Price_Index_Weekly_Dist'] = w3['agg_Weekly_Dist_DAL WSP']/w3['agg_Weekly_Dist_UT WSP']
    w3.rename(columns={'Weekly_Dist_Bill Qty_y': 'Weekly_Dist_Bill_Qty'}, inplace=True)
    w3.drop(columns='Weekly_Dist_Bill Qty_x', axis=1, inplace=True)
    df=w3.copy()
    return df