import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
@st.cache_data
def read():
    data = pd.read_excel('Price_PD_WSP_Apr_22-Feb_23_with_QTY_ASO.xlsx')
    return data