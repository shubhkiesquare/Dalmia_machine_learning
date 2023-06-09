import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
from dash.dependencies import Input, Output

# Create a Dash app
app = dash.Dash(__name__)

# Define a dummy dataset
dataset = pd.DataFrame({
    'Week': [1, 2, 3],
    'Value': [75, 60, 90]
})

# Define the layout
app.layout = html.Div(
    children=[
        html.H1("Gauge Chart"),
        dcc.Dropdown(
            id='week-dropdown',
            options=[
                {'label': 'Week 1', 'value': 1},
                {'label': 'Week 2', 'value': 2},
                {'label': 'Week 3', 'value': 3}
            ],
            value=1,
            style={'width': '200px'}  # Set the width of the dropdown
        ),
        daq.Gauge(
            id='gauge-chart',
            showCurrentValue=True,
            color={"gradient": True, "ranges": {"green": [0, 50], "yellow": [50, 70], "red": [70, 100]}},
            label='Gauge Title',
            max=100,
            value=70
        )
    ]
)

# Define the callback function to update the chart
@app.callback(
    Output('gauge-chart', 'value'),
    Input('week-dropdown', 'value')
)
def update_chart(week):
    # Get the corresponding value from the dataset based on the selected week
    value = dataset.loc[dataset['Week'] == week, 'Value'].values[0]
    
    # Return the value for the gauge chart
    return value

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True , port = 8080)
