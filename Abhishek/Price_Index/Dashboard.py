import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
import Combine
import Combine, Read, manipulation, datamanipulation, read_new
from Combine import *
# from Read import *
# from manipulation import *
from datamanipulation import *
from read_new import *
from PIL import Image
#st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
# st.set_page_config(layout="wide")
col_fig1,col_title,col_fig2=st.columns(3)
with col_fig1:
    col11,col22,col33= st.columns(3)
    with col11:
        st.write(" ")
    with col22:
        image1 = Image.open('Dalmia-Cement.jpg')
        st.image(image1, width=200)
    with col33:
        st.write(" ")
with col_fig2:
    col11,col22,col33= st.columns(3)
    with col11:
        st.write(" ")
    with col22:
        image1 = Image.open('Kie Square.jpeg')
        st.image(image1, width=200)
    with col33:
        st.write(" ")
with col_title:
    st.markdown("<h1 style='text-align: center; color: white;'>Price Index Analysis</h1>", unsafe_allow_html=True)

df1,df2,df3 = read_all()
df = datamanipulation(df1,df2,df3)
dashboard(df)
