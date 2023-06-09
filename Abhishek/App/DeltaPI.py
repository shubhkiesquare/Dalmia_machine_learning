import streamlit as st
import pandas as pd
import plotly.graph_objects as go
df = pd.read_excel('Week_District.xlsx')
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
