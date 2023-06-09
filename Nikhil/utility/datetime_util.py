import pandas as pd 
import numpy as np
import datetime

def create_date_columns(df_list):#pass the dataframe in the list format 
    new_df = pd.DataFrame()
    for i in df_list:
        i['date'] = pd.to_datetime(i['Billing Date'])
        i['Month_Year'] = pd.to_datetime(i['date']).dt.strftime('%Y-%m')
        i['Year'] = pd.to_datetime(i['date']).dt.year
        i['Quarter'] = i['date'].dt.to_period('Q')
        new_df = pd.concat([new_df,i], axis=0)

    return new_df

def timeseries_conversion(excel_serial_number):
    reference_date = datetime.datetime(1900, 1, 1)
    dt = reference_date + datetime.timedelta(days=excel_serial_number - 2)
    return dt
