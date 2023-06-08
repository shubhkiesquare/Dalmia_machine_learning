import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

df = pd.read_excel('Week_District.xlsx')

## Gauge Chart: Price Index and Share of Wallet
g1 = df.groupby(['Year-Week'], as_index=False).apply(lambda group: pd.Series({
    'N_Weekly_dist_DAL WSP': ((group['agg_Weekly_Dist_DAL WSP'] * group['Weekly_Dist_Bill_Qty']).sum()) / group['Weekly_Dist_Bill_Qty'].sum(),
    'N_Weekly_Dist_Bill Qty': group['Weekly_Dist_Bill_Qty'].sum()
}))
g2 = df.groupby(['Year-Week'], as_index=False).apply(lambda group: pd.Series({
    'N_Weekly_dist_UT WSP': ((group['agg_Weekly_Dist_UT WSP'] * group['Weekly_Dist_Bill_Qty']).sum()) / group['Weekly_Dist_Bill_Qty'].sum(),
    'N_Weekly_Dist_Bill Qty': group['Weekly_Dist_Bill_Qty'].sum()
}))

g3=pd.merge(g1,g2, how='inner',left_on=['Year-Week'],right_on=['Year-Week'])
g3['N_Price_Index_Weekly']= g3['N_Weekly_dist_DAL WSP']/g3['N_Weekly_dist_UT WSP']
g3['N_Price_Index_Weekly_Change'] =  g3['N_Price_Index_Weekly'].diff()
g3['N_Price_Index_Weekly_Change'] = (g3['N_Price_Index_Weekly_Change']/g3['N_Price_Index_Weekly'])*100
# Generate random percentages between 0 and 100
random_percentages = np.random.uniform(40, 41, size=44)

# Assign the random percentages to a new column in the dataframe
g3['Share_of_wallet'] = random_percentages
g3['Share_of_wallet_Change'] =  (g3['Share_of_wallet'].diff()/g3['Share_of_wallet'])*100
# Set page title
st.title("Price Index Gauge Chart")

# Create a dropdown to select the Year-Week
selected_year_week = st.selectbox("Select Year-Week:", g3['Year-Week'].unique())

# Filter the dataframe based on the selected Year-Week
selected_data = g3[g3['Year-Week'] == selected_year_week]
price_index = round(selected_data['N_Price_Index_Weekly'].values[0], 2)
change_in_price_index = round(selected_data['N_Price_Index_Weekly_Change'].values[0], 2)
share_wallet = round(selected_data['Share_of_wallet'].values[0], 2)
change_in_share_wallet = round(selected_data['Share_of_wallet_Change'].values[0], 2)

# Create a gauge chart for price index
fig1 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=price_index,
    domain={'x': [0, 1], 'y': [0, 1]},
    gauge={'axis': {'range': [0.95, 1.05]}},
    title={'text': "<b>Price Index</b>", 'font': {'family': 'bold'}}
))

# Create a gauge chart for share of wallet
fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=share_wallet,
    domain={'x': [0, 1], 'y': [0, 1]},
    gauge={'axis': {'range': [0, 100]}},
    title={'text': "<b>Share of Wallet</b>", 'font': {'family': 'bold'}},
    number={'suffix': '%'}
))

# Set up the change indicator text and style
change_indicator = f"Price Index: {change_in_price_index}% | Share of Wallet: {change_in_share_wallet}%"

# Set up the change indicator symbol and color for price index
if change_in_price_index > 0:
    price_indicator_symbol = u"\u25B2"  # upper triangular symbol
    price_indicator_color = 'green'
elif change_in_price_index < 0:
    price_indicator_symbol = u"\u25BC"  # lower triangular symbol
    price_indicator_color = 'red'
else:
    price_indicator_symbol = ''  # no indicator
    price_indicator_color = 'black'

# Set up the change indicator symbol and color for share of wallet
if change_in_share_wallet > 0:
    wallet_indicator_symbol = u"\u25B2"  # upper triangular symbol
    wallet_indicator_color = 'green'
elif change_in_share_wallet < 0:
    wallet_indicator_symbol = u"\u25BC"  # lower triangular symbol
    wallet_indicator_color = 'red'
else:
    wallet_indicator_symbol = ''  # no indicator
    wallet_indicator_color = 'black'

change_indicator_text_price = f"{price_indicator_symbol} {change_in_price_index}%"
change_indicator_text_wallet = f"{wallet_indicator_symbol} {change_in_share_wallet}%"
indicator_style = {'font-size': '20px', 'margin': '10px'}

# Display the gauge chart and change indicator with symbols and colors
st.plotly_chart(fig1)
st.markdown(f"<p style='color:{price_indicator_color};'>{change_indicator_text_price}</p>", unsafe_allow_html=True)
st.plotly_chart(fig2)
st.markdown(f"<p style='color:{wallet_indicator_color};'>{change_indicator_text_wallet}</p>", unsafe_allow_html=True)

#--------------------------#
#--------------------------#
#--------------------------#

# Delta_PI/PI vs Delta_Vol/Vol
p1= df.copy()

p1['change_PI'] = p1.groupby(['SH Location','DISTRICT CODE'],as_index=False)['Price_Index_Weekly_Dist'].diff()
p1['change_Volume'] = p1.groupby(['SH Location','DISTRICT CODE'],as_index=False)['Weekly_Dist_Bill_Qty'].diff()
p1['rate_of_change_PI'] = (p1['change_PI']/ p1['Price_Index_Weekly_Dist'])*100
p1['rate_of_change_Vol'] = (p1['change_Volume']/ p1['Weekly_Dist_Bill_Qty'])*100
# Define the selected columns
selected_columns = ['SH Location', 'DISTRICT', 'Year-Week', 'rate_of_change_Vol', 'rate_of_change_PI']

# Filter the DataFrame based on the selected columns
df_selected = p1[selected_columns]

# Get unique SH Locations and Year-Weeks
sh_locations = df_selected['SH Location'].unique()
year_weeks = df_selected['Year-Week'].unique()

# Create the dropdown widgets
sh_location_dropdown = st.selectbox('SH Location:', sh_locations)
year_week_dropdown = st.selectbox('Year-Week:', year_weeks)

# Define the update_plot function
def update_plot(sh_location, year_week):
    # Filter the DataFrame based on the selected SH Location and Year-Week
    filtered_df = df_selected[(df_selected['SH Location'] == sh_location) & (df_selected['Year-Week'] == year_week)]
    
    # Sort the filtered DataFrame by rate_of_change_PI
    sorted_df = filtered_df.sort_values('rate_of_change_PI')
    
    trace1 = go.Bar(
        x=sorted_df['DISTRICT'],
        y=sorted_df['rate_of_change_PI'],
        name='Delta_PI/PI (%)',
        marker_color='#6495ED',
        yaxis='y1',  # Use the left y-axis
        text=sorted_df['rate_of_change_PI'],  # Add the values as text
        textposition='auto',  # Automatically position the text above the bars
        texttemplate='%{text:.2f}%',  # Format the text as percentage with 2 decimal places
    )

    # Create the bar plot trace for Delta_Vol/Vol
    trace2 = go.Bar(
        x=sorted_df['DISTRICT'],
        y=sorted_df['rate_of_change_Vol'],
        name='Delta_Vol/Vol (%)',
        marker_color='#FF6347',
        yaxis='y2',  # Use the right y-axis
        text=sorted_df['rate_of_change_Vol'],  # Add the values as text
        textposition='auto',  # Automatically position the text above the bars
        texttemplate='%{text:.2f}%',  # Format the text as percentage with 2 decimal places
    )
    
    # Create the layout
    layout = go.Layout(
        barmode='group',
        xaxis=dict(title='District'),
        yaxis=dict(
            title='Delta_PI/PI (%)',
            side='left',
            color='blue',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Delta_Vol/Vol (%)',
            side='right',
            overlaying='y',
            color='red',
            titlefont=dict(color='red'),
            tickfont=dict(color='red')
        ),
        legend=dict(x=0.8, y=1.0)
    )
    
    # Create the figure
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    
    # Update the figure size
    fig.update_layout(
        height=600,  # Set the height of the figure
        width=1600  # Set the width of the figure
    )
    
    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

# Call the update_plot function
update_plot(sh_location_dropdown, year_week_dropdown)


