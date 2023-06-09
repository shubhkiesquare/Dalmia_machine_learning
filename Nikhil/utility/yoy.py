import os
import numpy as np 
import pandas as pd
import datetime



def read_multiple_tables(directory):
    df = pd.DataFrame()
    for folder in os.listdir(directory):
        if folder not in ['.DS_Store', '.ipynb_checkpoints']:
            for file in os.listdir(os.path.join(directory , folder)):
                if file != '.ipynb_checkpoints':
                    files_dir = os.path.join(directory , folder , file)
                    df_1 = pd.read_excel(files_dir)
                df = pd.concat([df , df_1] , axis = 0)
    return df


def timeseries_conversion(excel_serial_number):
    reference_date = datetime.datetime(1900, 1, 1)
    dt = reference_date + datetime.timedelta(days=excel_serial_number - 2)
    return dt

def create_date_columns(df_list):#pass the dataframe in the list format 
    new_df = pd.DataFrame()
    for i in df_list:
        i['date'] = pd.to_datetime(i['Billing Date'])
        i['Month_Year'] = pd.to_datetime(i['date']).dt.strftime('%Y-%m')
        i['Year'] = pd.to_datetime(i['date']).dt.year
        i['Quarter'] = i['date'].dt.to_period('Q')
        new_df = pd.concat([new_df,i], axis=0)

    return new_df

def return_yoy_df(directory):
    print(1)
    df = read_multiple_tables(directory)
    print(2)
    #df['Billing Date'] = df['Billing Date'].apply(timeseries_conversion)
    print(3)
    df_sales = create_date_columns([df])
    print(4)
    df_sales = df_sales[['Sold To Party Code','Month_Year','Bill Quantity']]
    print(5)
    df_sales =df_sales[df_sales['Sold To Party Code']!='DONATION']
    df_group_month = df_sales.groupby(['Sold To Party Code','Month_Year']).agg({'Bill Quantity': ['sum']}).reset_index()
    print(7)
    df_group_month.columns = ['Sold To Party Code', 'Month Year' , 'Sum']
    pivot_table = pd.pivot_table(df_group_month, values='Sum',columns='Month Year', index = 'Sold To Party Code')
    print(8)
    pivot_table.to_csv('pivot_table_march.csv')

if __name__ == '__main__':
    directory = 'data/yoy_calculation'
    print(return_yoy_df(directory))
    
    
    
   