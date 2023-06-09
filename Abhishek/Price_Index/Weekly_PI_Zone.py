import streamlit as st
import pandas as pd
# import plotly.express as px

# Define the dataset
df = pd.read_excel('Week_District.xlsx')  

z1 = df.groupby(['SH Location','Year-Week'], as_index=False).apply(lambda group: pd.Series({
    'Z_Weekly_dist_DAL WSP': ((group['agg_Weekly_Dist_DAL WSP'] * group['Weekly_Dist_Bill_Qty']).sum()) / group['Weekly_Dist_Bill_Qty'].sum(),
    'Z_Weekly_Dist_Bill Qty': group['Weekly_Dist_Bill_Qty'].sum()
}))
z2 = df.groupby(['SH Location','Year-Week'], as_index=False).apply(lambda group: pd.Series({
    'Z_Weekly_dist_UT WSP': ((group['agg_Weekly_Dist_UT WSP'] * group['Weekly_Dist_Bill_Qty']).sum()) / group['Weekly_Dist_Bill_Qty'].sum(),
    'Z_Weekly_Dist_Bill Qty': group['Weekly_Dist_Bill_Qty'].sum()
}))
z3=pd.merge(z1,z2, how='inner',left_on=['SH Location','Year-Week'],right_on=['SH Location','Year-Week'])
z3['Price_Index']= z3['Z_Weekly_dist_DAL WSP']/z3['Z_Weekly_dist_UT WSP']
z3['Change_in_Price_Index'] = z3.groupby(['SH Location'], as_index=False)['Price_Index'].diff()
z3['Price_Index'] = z3['Price_Index'].round(3)
z3['Change_in_Price_Index'] = (z3['Change_in_Price_Index']/z3['Price_Index'])*100
z3['Change_in_Price_Index'] =z3['Change_in_Price_Index'].round(2)
# Set page title
st.title("Price Index and Change in Price Index: Zone Level")

# Create the dropdown for selecting a week
selected_week = st.selectbox("Select a week", z3['Year-Week'].unique())

# Filter the dataset based on the selected week
week_data = z3[z3['Year-Week'] == selected_week]

# Apply conditional formatting with colors to the rows
def highlight_row(row):
    color = 'green' if row['Change_in_Price_Index'] > 1 or  row['Change_in_Price_Index'] < -1 else 'black' 
    return ['background-color: {}'.format(color)] * len(row)

styled_week_data =week_data[['SH Location', 'Price_Index', 'Change_in_Price_Index']].style.apply(highlight_row, axis=1)

# Display the styled data table
st.dataframe(styled_week_data)

