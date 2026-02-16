import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Adidas Sales Analytics",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0F0F0F 0%, #1A1A1A 100%);
    }
    
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 18px 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 160, 220, 0.3);
        border: 1px solid rgba(0, 160, 220, 0.3);
    }
    
    .kpi-title {
        font-size: 0.7rem;
        color: #B0B0B0;
        font-weight: 500;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #00A0DC 0%, #7FD957 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        word-wrap: break-word;
    }
    
    .kpi-trend {
        font-size: 0.75rem;
        font-weight: 500;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .trend-up {
        color: #7FD957;
    }
    
    .trend-down {
        color: #FF6B35;
    }
    
    /* Header Styling */
    .dashboard-header {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
        background: linear-gradient(135deg, #00A0DC 0%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .dashboard-subtitle {
        font-size: 1rem;
        color: #B0B0B0;
        margin-top: 5px;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A1A 0%, #0F0F0F 100%);
    }
    
    /* Filter Section */
    .filter-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    /* Streamlit Elements */
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        color: #00A0DC !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00A0DC 0%, #0080B0 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 160, 220, 0.4);
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: rgba(127, 217, 87, 0.2);
        color: #7FD957;
        border: 1px solid #7FD957;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(127, 217, 87, 0.3);
        border-color: #7FD957;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Adidas.xlsx")
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['MonthYear'] = df['InvoiceDate'].dt.strftime('%b %Y')
    df['Quarter'] = df['InvoiceDate'].dt.quarter
    return df

df = load_data()

# Sidebar - Filters
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Filters")
    st.markdown("---")
    
    # Date Range Filter
    st.markdown("#### 📅 Date Range")
    min_date = df['InvoiceDate'].min().date()
    max_date = df['InvoiceDate'].max().date()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start", min_date, min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input("End", max_date, min_value=min_date, max_value=max_date)
    
    st.markdown("---")
    
    # Region Filter
    st.markdown("#### 🌍 Geography")
    regions = st.multiselect(
        "Select Regions",
        options=sorted(df['Region'].unique()),
        default=sorted(df['Region'].unique())
    )
    
    # Product Filter
    st.markdown("#### 👟 Products")
    products = st.multiselect(
        "Select Products",
        options=sorted(df['Product'].unique()),
        default=sorted(df['Product'].unique())
    )
    
    # Retailer Filter
    st.markdown("#### 🏪 Retailers")
    retailers = st.multiselect(
        "Select Retailers",
        options=sorted(df['Retailer'].unique()),
        default=sorted(df['Retailer'].unique())
    )
    
    # Sales Method Filter
    st.markdown("#### 💳 Sales Method")
    sales_methods = st.multiselect(
        "Select Sales Methods",
        options=sorted(df['SalesMethod'].unique()),
        default=sorted(df['SalesMethod'].unique())
    )
    
    st.markdown("---")
    
    # Reset Filters Button
    if st.button("🔄 Reset All Filters"):
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Last Updated:** " + datetime.now().strftime("%d %B %Y, %H:%M"))

# Apply Filters
filtered_df = df[
    (df['InvoiceDate'].dt.date >= start_date) &
    (df['InvoiceDate'].dt.date <= end_date) &
    (df['Region'].isin(regions)) &
    (df['Product'].isin(products)) &
    (df['Retailer'].isin(retailers)) &
    (df['SalesMethod'].isin(sales_methods))
]

# Header Section
logo = Image.open("adidas-logo.jpg")
col_logo, col_title = st.columns([0.1, 0.9])

with col_logo:
    st.image(logo, width=100)

with col_title:
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">Adidas Sales Analytics Dashboard</h1>
            <p class="dashboard-subtitle">Real-time insights into sales performance, profitability, and market trends</p>
        </div>
    """, unsafe_allow_html=True)

# Show active filters
if len(filtered_df) < len(df):
    st.info(f"📊 Showing **{len(filtered_df):,}** of **{len(df):,}** total records based on active filters")

# KPI Metrics Section
st.markdown("### 📈 Key Performance Indicators")

# Calculate KPIs
total_revenue = filtered_df['TotalSales'].sum()
total_units = filtered_df['UnitsSold'].sum()
avg_order_value = filtered_df['TotalSales'].mean()
total_profit = filtered_df['OperatingProfit'].sum()
avg_margin = filtered_df['OperatingMargin'].mean()
total_transactions = len(filtered_df)

# Calculate trends (compare with previous period)
current_period_days = (end_date - start_date).days
previous_start = pd.to_datetime(start_date) - pd.Timedelta(days=current_period_days)
previous_df = df[
    (df['InvoiceDate'].dt.date >= previous_start.date()) &
    (df['InvoiceDate'].dt.date < start_date)
]

prev_revenue = previous_df['TotalSales'].sum() if len(previous_df) > 0 else total_revenue
revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0

# KPI Cards
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

with kpi_col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">${total_revenue/1e6:.2f}M</div>
            <div class="kpi-trend {'trend-up' if revenue_change >= 0 else 'trend-down'}">
                {'▲' if revenue_change >= 0 else '▼'} {abs(revenue_change):.1f}%
            </div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Units Sold</div>
            <div class="kpi-value">{total_units/1000:.1f}K</div>
            <div class="kpi-trend">
                📦 {total_transactions:,} orders
            </div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Order</div>
            <div class="kpi-value">${avg_order_value:,.0f}</div>
            <div class="kpi-trend">
                💰 Per transaction
            </div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Profit</div>
            <div class="kpi-value">${total_profit/1e6:.2f}M</div>
            <div class="kpi-trend trend-up">
                💵 Net earnings
            </div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Margin</div>
            <div class="kpi-value">{avg_margin*100:.1f}%</div>
            <div class="kpi-trend">
                📊 Average
            </div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col6:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Transactions</div>
            <div class="kpi-value">{total_transactions/1000:.1f}K</div>
            <div class="kpi-trend">
                🛒 Total orders
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Row 1: Revenue Analysis
st.markdown("### 💰 Revenue Analysis")
col1, col2 = st.columns(2)

with col1:
    # Revenue by Product
    product_revenue = filtered_df.groupby('Product')['TotalSales'].sum().sort_values(ascending=True)
    fig1 = px.bar(
        product_revenue,
        x=product_revenue.values,
        y=product_revenue.index,
        orientation='h',
        title="Revenue by Product Category",
        labels={'x': 'Total Sales ($)', 'y': 'Product'},
        color=product_revenue.values,
        color_continuous_scale=['#00A0DC', '#7FD957', '#FF6B35'],
        template='plotly_dark'
    )
    fig1.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Revenue Trend Over Time
    monthly_revenue = filtered_df.groupby('MonthYear')['TotalSales'].sum().reset_index()
    monthly_revenue['MonthYear'] = pd.to_datetime(monthly_revenue['MonthYear'], format='%b %Y')
    monthly_revenue = monthly_revenue.sort_values('MonthYear')
    
    fig2 = px.area(
        monthly_revenue,
        x='MonthYear',
        y='TotalSales',
        title="Revenue Trend Over Time",
        labels={'MonthYear': 'Month', 'TotalSales': 'Total Sales ($)'},
        template='plotly_dark',
        color_discrete_sequence=['#00A0DC']
    )
    fig2.update_traces(fill='tozeroy', fillcolor='rgba(0, 160, 220, 0.3)')
    fig2.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Row 2: Geographic Performance
st.markdown("### 🌍 Geographic Performance")
col3, col4 = st.columns(2)

with col3:
    # Sales by Region (Donut Chart)
    region_sales = filtered_df.groupby('Region')['TotalSales'].sum().reset_index()
    fig3 = px.pie(
        region_sales,
        values='TotalSales',
        names='Region',
        title="Sales Distribution by Region",
        hole=0.5,
        color_discrete_sequence=['#00A0DC', '#7FD957', '#FF6B35', '#FFD700', '#9D4EDD'],
        template='plotly_dark'
    )
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Top 10 Cities
    city_sales = filtered_df.groupby('City')['TotalSales'].sum().sort_values(ascending=False).head(10)
    fig4 = px.bar(
        city_sales,
        x=city_sales.values,
        y=city_sales.index,
        orientation='h',
        title="Top 10 Cities by Revenue",
        labels={'x': 'Total Sales ($)', 'y': 'City'},
        color=city_sales.values,
        color_continuous_scale='Viridis',
        template='plotly_dark'
    )
    fig4.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Row 3: Sales Channel & Retailer Analysis
st.markdown("### 🏪 Sales Channel & Retailer Performance")
col5, col6 = st.columns(2)

with col5:
    # Sales Method Comparison
    method_data = filtered_df.groupby('SalesMethod').agg({
        'TotalSales': 'sum',
        'UnitsSold': 'sum'
    }).reset_index()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=method_data['SalesMethod'],
        y=method_data['TotalSales'],
        name='Revenue',
        marker_color='#00A0DC',
        yaxis='y'
    ))
    fig5.add_trace(go.Scatter(
        x=method_data['SalesMethod'],
        y=method_data['UnitsSold'],
        name='Units Sold',
        marker_color='#7FD957',
        yaxis='y2',
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    fig5.update_layout(
        title="Sales Method: Revenue vs Units",
        xaxis=dict(title='Sales Method'),
        yaxis=dict(title='Revenue ($)', side='left'),
        yaxis2=dict(title='Units Sold', overlaying='y', side='right'),
        template='plotly_dark',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # Top Retailers Performance
    retailer_data = filtered_df.groupby('Retailer').agg({
        'TotalSales': 'sum',
        'OperatingMargin': 'mean'
    }).sort_values('TotalSales', ascending=True).tail(8)
    
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
        x=retailer_data['TotalSales'],
        y=retailer_data.index,
        orientation='h',
        name='Revenue',
        marker=dict(
            color=retailer_data['OperatingMargin'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Margin %")
        ),
        text=[f"${x/1e6:.1f}M" for x in retailer_data['TotalSales']],
        textposition='auto'
    ))
    
    fig6.update_layout(
        title="Top Retailers by Revenue (colored by margin)",
        xaxis=dict(title='Total Sales ($)'),
        yaxis=dict(title='Retailer'),
        template='plotly_dark',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Row 4: Profitability Analysis
st.markdown("### 💎 Profitability Analysis")
col7, col8 = st.columns(2)

with col7:
    # Operating Margin by Product (Scatter)
    product_profit = filtered_df.groupby('Product').agg({
        'TotalSales': 'sum',
        'OperatingMargin': 'mean',
        'UnitsSold': 'sum'
    }).reset_index()
    
    fig7 = px.scatter(
        product_profit,
        x='TotalSales',
        y='OperatingMargin',
        size='UnitsSold',
        color='Product',
        title="Product Performance: Sales vs Margin",
        labels={'TotalSales': 'Total Sales ($)', 'OperatingMargin': 'Operating Margin', 'UnitsSold': 'Units Sold'},
        template='plotly_dark',
        color_discrete_sequence=['#00A0DC', '#7FD957', '#FF6B35', '#FFD700', '#9D4EDD', '#06FFA5']
    )
    fig7.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    # Profit Margin Distribution
    fig8 = px.histogram(
        filtered_df,
        x='OperatingMargin',
        nbins=30,
        title="Operating Margin Distribution",
        labels={'OperatingMargin': 'Operating Margin', 'count': 'Frequency'},
        template='plotly_dark',
        color_discrete_sequence=['#7FD957']
    )
    fig8.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Row 5: Deep Dive - Heatmap and Table
st.markdown("### 🔥 Deep Dive Analysis")

# Sales Heatmap (Region x Product)
heatmap_data = filtered_df.pivot_table(
    values='TotalSales',
    index='Region',
    columns='Product',
    aggfunc='sum',
    fill_value=0
)

fig9 = px.imshow(
    heatmap_data,
    labels=dict(x="Product", y="Region", color="Sales ($)"),
    title="Sales Heatmap: Region × Product",
    color_continuous_scale='Turbo',
    template='plotly_dark',
    aspect='auto'
)
fig9.update_layout(
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)
st.plotly_chart(fig9, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Monthly Performance Table
st.markdown("### 📊 Monthly Performance Summary")
monthly_summary = filtered_df.groupby('MonthYear').agg({
    'TotalSales': 'sum',
    'UnitsSold': 'sum',
    'OperatingProfit': 'sum',
    'OperatingMargin': 'mean'
}).reset_index()

monthly_summary.columns = ['Month', 'Revenue ($)', 'Units Sold', 'Profit ($)', 'Avg Margin']
monthly_summary['Revenue ($)'] = monthly_summary['Revenue ($)'].apply(lambda x: f"${x:,.0f}")
monthly_summary['Profit ($)'] = monthly_summary['Profit ($)'].apply(lambda x: f"${x:,.0f}")
monthly_summary['Avg Margin'] = monthly_summary['Avg Margin'].apply(lambda x: f"{x*100:.2f}%")

st.dataframe(monthly_summary, use_container_width=True, height=300)

# Download Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📥 Export Data")

col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    st.download_button(
        label="📊 Download Filtered Data",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f"adidas_filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col_d2:
    st.download_button(
        label="📈 Download Monthly Summary",
        data=monthly_summary.to_csv(index=False).encode('utf-8'),
        file_name=f"adidas_monthly_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col_d3:
    product_summary = filtered_df.groupby('Product').agg({
        'TotalSales': 'sum',
        'UnitsSold': 'sum',
        'OperatingProfit': 'sum'
    }).reset_index()
    st.download_button(
        label="🏷️ Download Product Summary",
        data=product_summary.to_csv(index=False).encode('utf-8'),
        file_name=f"adidas_product_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #B0B0B0; padding: 20px;'>
        <p>🚀 Adidas Sales Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p style='font-size: 0.8rem;'>Data Period: 2020-2021 | Last Updated: """ + datetime.now().strftime("%d %B %Y, %H:%M") + """</p>
    </div>
    """,
    unsafe_allow_html=True
)
