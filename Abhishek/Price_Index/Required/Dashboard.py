import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
import numpy as np
import Combine, Read, manipulation
from Combine import *
from Read import *
from manipulation import *
from PIL import Image
#st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
# st.set_page_config(layout="wide")
col_fig1,col_title,col_fig2=st.columns(3)
with col_fig1:
    image1 = Image.open('Dalmia-Cement.jpg')
    st.image(image1, width=200)
with col_fig2:
    image2 = Image.open('Kie Square.jpeg')
    st.image(image2, width=200)
with col_title:
    st.title("Price Index Analysis")
data = read()
df = manipulation(data)

dashboard(df)
