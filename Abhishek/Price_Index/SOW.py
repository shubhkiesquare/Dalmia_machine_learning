import dash
# import dash_core_components as dcc
import streamlit as st
from dash import dcc
# import dash_html_components as html
from dash import html
import pandas as pd
import plotly.graph_objects as go

# Assuming you have a dataframe called 'df' with columns Year-Week, Price_Index, and Change_in_Price_Index
# Replace 'df' with your actual dataframe name
df = pd.read_excel('Weekly_Pie.xlsx')
# Create a Dash app
app = dash.Dash(__name__)

# Set up the layout
app.layout = html.Div([
    html.H1("Share of Wallet Gauge Chart"),
    html.Div([
        html.Label("Select Year-Week:"),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': x, 'value': x} for x in df['Year-Week'].unique()],
            value=df['Year-Week'].unique()[0]
        ),
    ]),
    html.Div([
        dcc.Graph(id='gauge-chart'),
        html.P(id='change-indicator', style={'text-align': 'center'})
    ])
])


# Define callback function to update the gauge chart and change indicator
@app.callback(
    dash.dependencies.Output('gauge-chart', 'figure'),
    dash.dependencies.Output('change-indicator', 'children'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_chart(selected_year_week):
    # Filter the dataframe based on the selected Year-Week
    selected_data = df[df['Year-Week'] == selected_year_week]
    price_index = round(selected_data['Share_of_wallet'].values[0],2)
    change_in_price_index = round(selected_data['Share_of_wallet_Change'].values[0],2)
    
    # Create a gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=price_index,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 100]}},
        title={'text': "<b>Share of Wallet</b>", 'font': {'family': 'bold'}},
        number={'suffix': '%'}
    ))
    
    # Set up the change indicator text and style
    change_indicator = f"{change_in_price_index}%"
    indicator_style = {'font-size': '20px', 'margin': '10px'}
    
    # Add triangular indicators based on the change in price index
    if change_in_price_index > 0:
        indicator_symbol = u"\u25B2"  # upper triangular symbol
        indicator_style['color'] = 'green'
    elif change_in_price_index < 0:
        indicator_symbol = u"\u25BC"  # lower triangular symbol
        indicator_style['color'] = 'red'
    else:
        indicator_symbol = ''  # no indicator
    
    # Return the updated chart and change indicator
    return fig, html.Span([change_indicator, html.Br(), indicator_symbol], style=indicator_style)
select_dropdown= df['Year-Week'].unique()
option = st.selectbox(
    'Select Year-Week:',
    (select_dropdown))

st.write('Selected_Year-Week:', option)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8030)
