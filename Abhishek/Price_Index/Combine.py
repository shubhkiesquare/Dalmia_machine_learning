import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")
def dashboard(df):
    # Gauge Chart: Price Index and Share of Wallet
    g1 = df.groupby(['Year-Week'], as_index=False).apply(lambda group: pd.Series({
        'N_Weekly_dist_DAL WSP': ((group['agg_Weekly_Dist_DAL WSP'] * group['Weekly_Dist_Bill_Qty']).sum()) / group['Weekly_Dist_Bill_Qty'].sum(),
        'N_Weekly_Dist_Bill Qty': group['Weekly_Dist_Bill_Qty'].sum(),'SOW':group['SOW'].mean()
    }))
    g2 = df.groupby(['Year-Week'], as_index=False).apply(lambda group: pd.Series({
        'N_Weekly_dist_UT WSP': ((group['agg_Weekly_Dist_UT WSP'] * group['Weekly_Dist_Bill_Qty']).sum()) / group['Weekly_Dist_Bill_Qty'].sum(),
        'N_Weekly_Dist_Bill Qty': group['Weekly_Dist_Bill_Qty'].sum()
    }))
    g3=pd.merge(g1,g2, how='inner',left_on=['Year-Week'],right_on=['Year-Week'])

    g3['N_Price_Index_Weekly']= g3['N_Weekly_dist_DAL WSP']/g3['N_Weekly_dist_UT WSP']
    g3['N_Price_Index_Weekly_Change'] =  g3['N_Price_Index_Weekly'].diff()
    g3['N_Price_Index_Weekly_Change'] = g3['N_Price_Index_Weekly_Change'].ffill()
    g3['N_Price_Index_Weekly_Change'] = g3['N_Price_Index_Weekly_Change'].bfill()
    g3['N_Price_Index_Weekly_Change'] = (g3['N_Price_Index_Weekly_Change']/g3['N_Price_Index_Weekly'])*100
    # # Generate random percentages between 0 and 100
    # random_percentages = np.random.uniform(40, 41, size=53)

    # # Assign the random percentages to a new column in the dataframe
    # g3['Share_of_wallet'] = random_percentages
    g3['SOW_Diff'] =  g3['SOW'].diff()
    g3['SOW_Diff'] = g3['SOW_Diff'].ffill()
    g3['SOW_Diff'] = g3['SOW_Diff'].bfill()
    g3['Share_of_wallet_Change'] =  (g3['SOW_Diff']/g3['SOW'])*100
    # Set page title
    # st.title("Price Index Analysis")

    # Create a dropdown to select the Year-Week
    selected_year_week = st.selectbox("Select Year-Week:", g3['Year-Week'].unique())

    # Filter the dataframe based on the selected Year-Week
    selected_data = g3[g3['Year-Week'] == selected_year_week]
    price_index = round(selected_data['N_Price_Index_Weekly'].values[0], 2)
    change_in_price_index = round(selected_data['N_Price_Index_Weekly_Change'].values[0], 2)
    share_wallet = round(selected_data['SOW'].values[0], 2)
    change_in_share_wallet = round(selected_data['Share_of_wallet_Change'].values[0], 2)
    
    ## Total Weekly Volumne
    total_sales = selected_data['N_Weekly_Dist_Bill Qty_y'].sum()
    total_sales = round(total_sales,2)
    # Display the total sales value in Streamlit
    st.write("Total Volume:", total_sales, "MT")
    ## Correlation between Price Index and Volumn
    correlation = g3['N_Price_Index_Weekly'].corr(g3['N_Weekly_Dist_Bill Qty_x'])
    correlation = round(correlation,2)
    st.write("Correlation:", correlation)
    # st.set_page_config(layout="wide")
    col1, col2 = st.columns(2)
    with col1:
        # Create a gauge chart for price index
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=price_index,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0.95, 1.05]}},
            title={'text': "<b>Price Index</b>", 'font': {'family': 'bold'}}
        ))
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
        change_indicator_text_price = f"{price_indicator_symbol} {change_in_price_index}%"
        indicator_style = {'font-size': '20px', 'margin': '10px'}
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(f"<p style='text-align: center; color:{price_indicator_color};'>{change_indicator_text_price}</p>", unsafe_allow_html=True)
    with col2:
        # Create a gauge chart for share of wallet
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=share_wallet,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]}},
            title={'text': "<b>Share of Wallet</b>", 'font': {'family': 'bold'}},
            number={'suffix': '%'}
        ))
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
        change_indicator_text_wallet = f"{wallet_indicator_symbol} {change_in_share_wallet}%"
        indicator_style = {'font-size': '20px', 'margin': '10px'}
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f"<p style='text-align: center; color:{wallet_indicator_color};'>{change_indicator_text_wallet}</p>", unsafe_allow_html=True)

    # Set up the change indicator text and style
    change_indicator = f"Price Index: {change_in_price_index}% | Share of Wallet: {change_in_share_wallet}%"

    # # Set up the change indicator symbol and color for price index
    # if change_in_price_index > 0:
    #     price_indicator_symbol = u"\u25B2"  # upper triangular symbol
    #     price_indicator_color = 'green'
    # elif change_in_price_index < 0:
    #     price_indicator_symbol = u"\u25BC"  # lower triangular symbol
    #     price_indicator_color = 'red'
    # else:
    #     price_indicator_symbol = ''  # no indicator
    #     price_indicator_color = 'black'

    # # Set up the change indicator symbol and color for share of wallet
    # if change_in_share_wallet > 0:
    #     wallet_indicator_symbol = u"\u25B2"  # upper triangular symbol
    #     wallet_indicator_color = 'green'
    # elif change_in_share_wallet < 0:
    #     wallet_indicator_symbol = u"\u25BC"  # lower triangular symbol
    #     wallet_indicator_color = 'red'
    # else:
    #     wallet_indicator_symbol = ''  # no indicator
    #     wallet_indicator_color = 'black'

    # change_indicator_text_price = f"{price_indicator_symbol} {change_in_price_index}%"
    # change_indicator_text_wallet = f"{wallet_indicator_symbol} {change_in_share_wallet}%"
    # indicator_style = {'font-size': '20px', 'margin': '10px'}

    # Display the gauge chart and change indicator with symbols and colors
    # st.plotly_chart(fig1)
    # st.markdown(f"<p style='color:{price_indicator_color};'>{change_indicator_text_price}</p>", unsafe_allow_html=True)
    # st.title("Share of Wallet Gauge Chart")
    # st.plotly_chart(fig2)
    # st.markdown(f"<p style='color:{wallet_indicator_color};'>{change_indicator_text_wallet}</p>", unsafe_allow_html=True)

    #--------------------------#
    #--------------------------#
    #--------------------------#

    ## Price Index vs Volume
    st.write(" ")
    st.write(" ")
    # Create a subplot grid
    col11, col22 = st.columns(2)
    with col11:
        # fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

        # # Add the Price_Index trace to the subplot
        # fig.add_trace(go.Scatter(x=g3['Year-Week'], y=g3['N_Price_Index_Weekly'], name='Price_Index', line=dict(color='blue')), secondary_y=False)

        # # Add the Bill_Quantity trace to the subplot
        # fig.add_trace(go.Scatter(x=g3['Year-Week'], y=g3['N_Weekly_Dist_Bill Qty_x'], name='Volume', line=dict(color='red')), secondary_y=True)

        # # Set x-axis label and tick format
        # fig.update_xaxes(title_text='Year-Week', tickformat='%Y-%W')

        # # Set y-axes labels
        # fig.update_yaxes(title_text='Price_Index', color='blue', secondary_y=False)
        # fig.update_yaxes(title_text='Volume', color='red', secondary_y=True)
        fig, ax1 = plt.subplots(figsize=(18, 10))
        plt.xticks(rotation=45)
        # Plot the Price_Index on the left y-axis
        ax1.plot(g3['Year-Week'], g3['N_Price_Index_Weekly'], color='blue')
        ax1.set_ylabel('Price Index', color='blue', fontsize=16)

        # Create a second y-axis
        ax2 = ax1.twinx()

        # Plot the Bill_Quantity on the right y-axis
        ax2.plot(g3['Year-Week'], g3['N_Weekly_Dist_Bill Qty_x'], color='red')
        ax2.set_ylabel('Volume', color='red', fontsize=16)

        # Set labels and title
        ax1.set_xlabel('Year-Week', fontsize=14)
        st.markdown("<h5 style='text-align: center; color: white;'>Price Index vs Volume </h2>", unsafe_allow_html=True)
        # Display the plot
        st.pyplot(fig)

    #--------------------------#
    #--------------------------#
    #--------------------------#

    ## Price Index and Change in Price Index: Zone Level

    with col22:
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
        z3['Change_in_Price_Index'] = z3.groupby('SH Location')['Change_in_Price_Index'].ffill()
        z3['Change_in_Price_Index'] = z3.groupby('SH Location')['Change_in_Price_Index'].bfill()
        z3['Price_Index'] = z3['Price_Index'].round(3)
        z3['Change_in_Price_Index'] = (z3['Change_in_Price_Index']/z3['Price_Index'])*100
        z3['Change_in_Price_Index'] =z3['Change_in_Price_Index'].round(2)

        # Filter the dataset based on the selected week
        week_data = z3[z3['Year-Week'] == selected_year_week]

        # Apply conditional formatting with colors to the rows
        def highlight_row(row):
            color = 'green' if row['Change_in_Price_Index'] > 1 or  row['Change_in_Price_Index'] < -1 else 'black' 
            return ['background-color: {}'.format(color)] * len(row)

        styled_week_data =week_data[['SH Location', 'Price_Index', 'Change_in_Price_Index']].style.apply(highlight_row, axis=1)
        st.markdown("<h5 style='text-align: center; color: white;'>Price Index and Change in Price Index: Zone Level </h2>", unsafe_allow_html=True)
        # st.write(" ")
        # st.write(" ")
        # st.write(" ")
        # st.write(" ")
        # st.write(" ")
        st.write(" ")
        # Display the styled data table
        st.dataframe(styled_week_data, use_container_width=True)

    #--------------------------#
    #--------------------------#
    #--------------------------#

    ## Delta_PI/PI vs Delta_Vol/Vol
    st.write(" ")
    st.markdown("<h5 style='text-align: center; color: white;'>Delta_PI/PI vs Delta_Vol/Vol</h2>", unsafe_allow_html=True)
    p1= df.copy()

    p1['change_PI'] = p1.groupby(['SH Location','DISTRICT'],as_index=False)['Price_Index_Weekly_Dist'].diff()
    p1['change_Volume'] = p1.groupby(['SH Location','DISTRICT'],as_index=False)['Weekly_Dist_Bill_Qty'].diff()
    p1['change_PI'] = p1.groupby('SH Location')['change_PI'].ffill()
    p1['change_PI'] = p1.groupby('SH Location')['change_PI'].bfill()
    p1['change_Volume'] = p1.groupby('SH Location')['change_Volume'].ffill()
    p1['change_Volume'] = p1.groupby('SH Location')['change_Volume'].bfill()
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

    # # Define the update_plot function
    # def update_plot(sh_location, year_week):
    #     # Filter the DataFrame based on the selected SH Location and Year-Week
    #     filtered_df = df_selected[(df_selected['SH Location'] == sh_location) & (df_selected['Year-Week'] == year_week)]
        
    #     # Sort the filtered DataFrame by rate_of_change_PI
    #     sorted_df = filtered_df.sort_values('rate_of_change_PI')
        
    #     trace1 = go.Bar(
    #         x=sorted_df['DISTRICT'],
    #         y=sorted_df['rate_of_change_PI'],
    #         name='Delta_PI/PI (%)',
    #         marker_color='#6495ED',
    #         yaxis='y1',  # Use the left y-axis
    #         text=sorted_df['rate_of_change_PI'],  # Add the values as text
    #         textposition='auto',  # Automatically position the text above the bars
    #         texttemplate='%{text:.2f}%',  # Format the text as percentage with 2 decimal places
    #     )

    #     # Create the bar plot trace for Delta_Vol/Vol
    #     trace2 = go.Bar(
    #         x=sorted_df['DISTRICT'],
    #         y=sorted_df['rate_of_change_Vol'],
    #         name='Delta_Vol/Vol (%)',
    #         marker_color='#FF6347',
    #         yaxis='y2',  # Use the right y-axis
    #         text=sorted_df['rate_of_change_Vol'],  # Add the values as text
    #         textposition='auto',  # Automatically position the text above the bars
    #         texttemplate='%{text:.2f}%',  # Format the text as percentage with 2 decimal places
    #     )
        
    #     # Create the layout
    #     layout = go.Layout(
    #         barmode='group',
    #         xaxis=dict(title='District'),
    #         yaxis=dict(
    #             title='Delta_PI/PI (%)',
    #             side='left',
    #             color='blue',
    #             titlefont=dict(color='blue'),
    #             tickfont=dict(color='blue')
    #         ),
    #         yaxis2=dict(
    #             title='Delta_Vol/Vol (%)',
    #             side='right',
    #             overlaying='y',
    #             color='red',
    #             titlefont=dict(color='red'),
    #             tickfont=dict(color='red')
    #         ),
    #         legend=dict(x=0.8, y=1.0)
    #     )
        
    #     # Create the figure
    #     fig = go.Figure(data=[trace1, trace2], layout=layout)
        
    #     # Update the figure size
    #     fig.update_layout(
    #         height=600,  # Set the height of the figure
    #         width=1600  # Set the width of the figure
    #     )
        
    #     # Show the figure
    #     st.plotly_chart(fig, use_container_width=True)
    # Define the update_plot function
    def update_plot(sh_location, year_week):
        # Filter the DataFrame based on the selected SH Location and Year-Week
        filtered_df = df_selected[(df_selected['SH Location'] == sh_location) & (df_selected['Year-Week'] == year_week)]

        # Sort the filtered DataFrame by rate_of_change_PI
        sorted_df = filtered_df.sort_values('rate_of_change_PI')

        # Create the bar plot trace for Delta_PI/PI
        trace1 = go.Bar(
            x=sorted_df['DISTRICT'],
            y=sorted_df['rate_of_change_PI'],
            name='Delta_PI/PI (%)',
            marker_color='#6495ED',
            text=sorted_df['rate_of_change_PI'],  # Add the values as text
            textposition='auto',  # Automatically position the text above the bars
            texttemplate='%{text:.2f}%',  # Format the text as percentage with 2 decimal places
        )

        # Create the layout for the first plot
        layout1 = go.Layout(
            xaxis=dict(title='District'),
            yaxis=dict(title='Delta_PI/PI (%)'),
            legend=dict(x=0.8, y=1.0)
        )

        # Create the figure for the first plot
        fig1 = go.Figure(data=[trace1], layout=layout1)

        # Update the figure size for the first plot
        fig1.update_layout(height=600, width=800)

        # Create the bar plot trace for Delta_Vol/Vol
        trace2 = go.Bar(
            x=sorted_df['DISTRICT'],
            y=sorted_df['rate_of_change_Vol'],
            name='Delta_Vol/Vol (%)',
            marker_color='#FF6347',
            text=sorted_df['rate_of_change_Vol'],  # Add the values as text
            textposition='auto',  # Automatically position the text above the bars
            texttemplate='%{text:.2f}%',  # Format the text as percentage with 2 decimal places
        )

        # Create the layout for the second plot
        layout2 = go.Layout(
            xaxis=dict(title='District'),
            yaxis=dict(title='Delta_Vol/Vol (%)'),
            legend=dict(x=0.8, y=1.0)
        )

        # Create the figure for the second plot
        fig2 = go.Figure(data=[trace2], layout=layout2)

        # Update the figure size for the second plot
        fig2.update_layout(height=600, width=800)

        # Show the figures side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)


    # Call the update_plot function
    update_plot(sh_location_dropdown, year_week_dropdown)
    return



