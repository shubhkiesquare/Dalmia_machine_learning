# Import necessary libraries
import dash
from dash import dcc, html
import pandas as pd
# import dash_table
from dash import dash_table
from dash.dependencies import Input, Output
from dash.dash_table.Format import Group

# Create a Dash app
app = dash.Dash(__name__)

# Define the dataset
dataset = pd.read_csv('Week_Zone_PI.csv')  # Replace 'your_dataset.csv' with the actual filename

app.layout = html.Div(
    children=[
        html.H1("Price Index and Change in Price Index"),
        dcc.Dropdown(
            id='week-dropdown',
            options=[
                {'label': week, 'value': week} for week in dataset['Year-Week'].unique()
            ],
            placeholder="Select a week",
            style={'width': '200px'}
        ),
        dash_table.DataTable(
            id='price-table',
            columns=[
                {'name': 'SH Location', 'id': 'SH Location'},
                {'name': 'Price Index', 'id': 'Price_Index'},
                {'name': 'WoW Change (%)', 'id': 'Change_in_Price_Index'}
            ],
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'fontSize': '16px',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_header={
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{Change_in_Price_Index} > 1'
                    },
                    'backgroundColor': 'green',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{Change_in_Price_Index} < -1'
                    },
                    'backgroundColor': 'red',
                    'color': 'white'
                }
            ]
        )
    ]
)


# Define the callback function
@app.callback(
    Output('price-table', 'data'),
    Input('week-dropdown', 'value')
)
def update_price_table(week):
    if week is None:
        return []
    
    # Filter the dataset based on the selected week
    week_data = dataset[dataset['Year-Week'] == week]
    
    # Prepare the data for the table
    table_data = week_data[['SH Location', 'Price_Index', 'Change_in_Price_Index']].to_dict('records')
    
    return table_data

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
