import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import plost


# set page title, icon, and layout
st.set_page_config(
    page_title='Dashboard Sample',
    page_icon="✅",
    layout="wide"
)

backgroundColor = "#262C46"
primaryColor = "#262C46",
secondaryBackgroundColor = "#ffffff",
textColor = "#003d5b",
font = "Arial"

# Custom theme using CSS
custom_css = f"""
    <style>
    /* General Styling */
    body {{
        background-color: {'#262C46'};
        color: {'#E0EAEF'};
        font-family: {font}, sans-serif;
    }}
    /* Header Styling */
    h1, h2, h3, h4, h5, h6 {{
        color: {primaryColor};
    }}
    /* Sidebar Styling */
    .sidebar .sidebar-content {{
        background-color: {secondaryBackgroundColor};
    }}
    /* Button Styling */
    .stButton {{
        background-color: {primaryColor};
        color: #fff; /* White text */
        font-weight: bold;
    }}
    /* Data Table Styling */
    .dataframe, th, td {{
        border: 1px solid {primaryColor};
    }}
    /* Other Customizations */
    /* Add your additional CSS customizations here */
    </style>
"""

# Apply the custom theme using st.markdown()
st.markdown(custom_css, unsafe_allow_html=True)


# load data using pandas
df = pd.read_csv('final_data.csv', na_values='NULL')

# set dashboard title
st.title('Dashboard Template')

store_filter = st.selectbox("Select a store", pd.unique(df["Store"].sort_values()))
s = df[df['Store'] == store_filter]

week_filter = st.selectbox("Select a week", pd.unique(s["Week"].sort_values()))
w = s[s['Week'] == week_filter]

col1, col2, col3 = st.columns(3)
with col1:
    total_sales = w['TotalSalesPrice'].sum()
    st.header('Total Sales')
    st.subheader(f'${total_sales}')

    st.header('Total Inventory')
    st.subheader(w['EndInv'].sum())

    st.header('Incoming Inventory')
    st.subheader(w['PurchaseQuantity'].sum())

with col2:
    st.markdown(
        """
        <div style="text-align:center">
            <h3>Inventory Value by Product</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    brand_sales = s.groupby('Brand')['InventoryValue'].sum().reset_index().head(10)
    brand_sales.index = brand_sales['Brand']
    st.bar_chart(brand_sales['InventoryValue'])
# min and max to be 1st and 3rd quartile values
with col3:
    st.markdown(
        """
        <div style="text-align:center">
            <h3>Days Inventory Outstanding</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    def create_half_circle_gauge(value, max_value):
        # Calculate the angle for the value on the half circle
        angle = (value / max_value) * 180
        if angle > 180:
            angle = 180
        elif value <= 0:
            angle = 0

        # Create a half-circle gauge using matplotlib
        fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
        fig.set_facecolor('#262C46')
        ax.set_facecolor('#262C46')
        ax.add_patch(
            patches.Arc((0.5, 0.5), 0.8, 0.8, theta1=0, theta2=180, facecolor='white', edgecolor='white', lw=3))
        ax.add_patch(
            patches.Arc((0.5, 0.5), 0.8, 0.8, theta1=180 - angle, theta2=180, facecolor='red', edgecolor='red', lw=3))

        # Add the indicator
        indicator = np.radians(180 - angle)
        x = 0.5 + 0.35 * np.cos(indicator)
        y = 0.5 + 0.35 * np.sin(indicator)
        ax.arrow(0.5, 0.5, x - 0.5, y - 0.5, width=0.02, head_width=0.04, head_length=0.04, fc='#E0EAEF', ec='#E0EAEF',
                 alpha=0.8)

        # Add labels
        plt.text(0.5, 0.7, f"{value} Days", fontsize=18, ha='center', va='center', color='#E0EAEF')
        # plt.text(0.5, 0.85, label, fontsize=12, ha='center', va='center')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Display the half-circle gauge chart in Streamlit
        st.pyplot(fig)


    # Sample values
    value = round(w['DOI'].median(), 2)
    max_value = w['DOI'].quantile(0.75)
    # label = "Days Inventory Outstanding"

    # Create the half-circle gauge chart with an indicator
    create_half_circle_gauge(value, max_value)

col4, col5 = st.columns(2)
with col4:
    st.markdown(
        """
        <div style="text-align:center">
            <h3>Inventory Turnover by Brand</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    brand_filter = st.selectbox("Select a brand", pd.unique(s["Brand"].sort_values()))
    b = s[s['Brand'] == brand_filter]
    b.index = range(1, 10)
    st.line_chart(b['InventoryTurnover'])

with col5:
    st.markdown(
        """
        <div style="text-align:center">
            <h3>Total Purhcase Quantity by Vendor</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    vendor = pd.read_csv('vendor.csv').groupby('Vendorname')['total_purchases_quantity'].sum().reset_index()
    plost.bar_chart(
        data=vendor.sort_values('total_purchases_quantity').head(15),
        bar='Vendorname',
        value='total_purchases_quantity',
        direction='horizontal')

col6, col7, col8 = st.columns(3)
with col6:
    st.markdown(
        """
        <div style="text-align:center">
            <h3>Days Inventory Outstanding by Week</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    s_week = s.groupby('Week')['DOI'].mean().reset_index()
    st.bar_chart(data=s_week['DOI'])

with col7:
    st.markdown(
        """
        <div style="text-align:center">
            <h3>Stock Summary</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    stock_summary = s[s['Week'] == 9].groupby('Description')[['SalesQuantity', 'PurchaseQuantity', 'EndInv']].sum().reset_index()
    stock_summary.index = stock_summary['Description']
    st.dataframe(stock_summary[['SalesQuantity', 'PurchaseQuantity', 'EndInv']], height=350)

    if stock_summary['EndInv'].min() < 100:
        st.warning('The units in stock is below our target', icon="⚠️")
with col8:
    st.markdown(
        """
        <div style="text-align:center">
            <h4>Total Sales Price & Cost of Goods Sold</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.area_chart(s[['TotalSalesPrice', 'COGS']])
