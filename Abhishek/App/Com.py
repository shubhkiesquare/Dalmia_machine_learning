import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel('Weekly_Pie.xlsx')

# Set page title
st.title("Price Index Gauge Chart")

# Create a dropdown to select the Year-Week
selected_year_week = st.selectbox("Select Year-Week:", df['Year-Week'].unique())

# Filter the dataframe based on the selected Year-Week
selected_data = df[df['Year-Week'] == selected_year_week]
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



