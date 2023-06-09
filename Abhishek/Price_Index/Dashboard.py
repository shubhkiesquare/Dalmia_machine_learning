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
data = read()
df = manipulation(data)
dashboard(df)
