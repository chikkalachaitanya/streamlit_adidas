import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_excel(r"Adidas.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
Image = Image.open(r"adidas-logo.jpg")

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
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales" : "TotalSales {$}"},
                 title="Total sales by Retailer", hover_data=["TotalSales"],
                 template="gridon", height=500)
    st.plotly_chart(fig, width="stretch")

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise sales")
    data = df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get data",data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv",mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", title="Total Sales over time", template="gridon")
    st.plotly_chart(fig1, width="stretch")

with view2:
    expander = st.expander("Monthly sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get data",data=result.to_csv().encode("utf-8"),
                       file_name="MonthlySales.csv",mime="text/csv")
    
st.divider()

result1 = df.groupby(by="State")[["TotalSales","UnitsSold"]].sum().reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode="lines", name="Units Sold",
                          yaxis="y2"))
fig3.update_layout(
    title = "Total sales and Units sold by State",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total sales", showgrid=False),
    yaxis2 = dict(title="Units sold", overlaying="y", side="right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3, width="stretch")

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    st.expander("View data for sales by units sold")
    expander.write("result1")
with dwn3:
    st.download_button("Get data", data=result1.to_csv().encode("utf-8"),
                       file_name="Sales by units sold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1,1])
treemap = df[["Region","City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum().reset_index()
def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value/1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)
fig4 = px.treemap(treemap, path=["Region","City"], values="TotalSales",
                  hover_name="TotalSales (Formatted)",
                  hover_data=["TotalSales (Formatted)"],
                  color="City", height=700)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total sales by Region and city")
    st.plotly_chart(fig4,width="stretch")

_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result2 = df[["Region","City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum()
    expander = st.expander("View data for Total sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Get data", data=result2.to_csv().encode("utf-8"),
                       file_name="Sales by Region and city.csv",mime="text/csv")

st.divider()

_, view5, dwn5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("View sales Raw data")
    expander.write(df)
with dwn5:
    st.download_button("Get raw data", data=df.to_csv().encode("utf-8"),
                       file_name="Sales raw data.csv", mime="text/csv")

st.divider()


