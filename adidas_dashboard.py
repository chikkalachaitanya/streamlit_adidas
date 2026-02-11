import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_excel(r"C:\work\streamlit\Adidas.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
Image = Image.open(r"C:/work/streamlit/adidas-logo.jpg")

col1,col2 = st.columns([0.1,0.9])
with col1:
    st.image(Image)
with col2:
    st.title("Adidas Interactive Sales Dashboard")

col3,col4,col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")
with col4:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")  