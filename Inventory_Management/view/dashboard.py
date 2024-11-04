import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# CSS to enhance UI with dark mode background and aligned metric boxes of equal size
st.markdown("""
    <style>
    body {
        background-color: #121212;  /* Dark mode background */
        color: #ffffff;  /* White text for dark mode */
    }
    .stApp {
        background-color: #121212;  /* Set full app background */
    }
    .main {
        background-color: #121212;
        color: #ffffff;
    }
    .stMetric {
        background-color: #ffffff; 
        border-radius: 10px; 
        padding: 15px; 
        margin: 10px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    .metric-box {
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        flex-grow: 1;
        flex-basis: 0;  /* Ensures all metric boxes are the same width */
    }
    .custom-chart {
        width: 80%;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory"
)
cursor = mydb.cursor()

# Query data from MySQL
query = "SELECT * FROM sales"
cursor.execute(query)
data = cursor.fetchall()

# Define column names as per the database
columns = ['sale_id', 'product_id', 'quantity', 'sale_amount', 'sale_date', 'location', 'customer_age', 'customer_gender', 'payment_type', 'sale_channel']

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Convert sale_date to datetime format
df['sale_date'] = pd.to_datetime(df['sale_date'])

# Sidebar for filtering data
st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))
selected_location = st.sidebar.multiselect("Select Location", df['location'].unique())
selected_product = st.sidebar.multiselect("Select Product ID", df['product_id'].unique())

# Filter data based on selections
filtered_data = df[(df['sale_date'] >= pd.to_datetime(start_date)) & (df['sale_date'] <= pd.to_datetime(end_date))]

if selected_location:
    filtered_data = filtered_data[filtered_data['location'].isin(selected_location)]

if selected_product:
    filtered_data = filtered_data[filtered_data['product_id'].isin(selected_product)]

# Display key metrics in three small boxes at the top
st.title("📊 Sales Analytics Dashboard")

# Metrics calculation
total_sales = filtered_data['sale_amount'].sum()
unique_locations = filtered_data['location'].nunique()
expected_revenue = filtered_data['sale_amount'].sum()

st.markdown("""
    <div class="metric-container">
        <div class="metric-box">
            <h3>💵 Total Sales</h3>
            <h2>${:,.2f}</h2>
        </div>
        <div class="metric-box">
            <h3>📍 Unique Locations</h3>
            <h2>{}</h2>
        </div>
        <div class="metric-box">
            <h3>📈 Expected Revenue</h3>
            <h2>${:,.2f}</h2>
        </div>
    </div>
""".format(total_sales, unique_locations, expected_revenue), unsafe_allow_html=True)

# Sales by Day, Month, or Year (with selection box)
st.sidebar.header("Sales View Options")
view_by = st.sidebar.selectbox("View sales by", ["Day", "Month", "Year"])

st.header(f"Sales Overview ({view_by})")

# Custom resizing for the only sales chart (small-sized one)
st.markdown("<div class='custom-chart'>", unsafe_allow_html=True)
fig = None

if view_by == "Day":
    sales_by_period = filtered_data.groupby(filtered_data['sale_date'].dt.date)['sale_amount'].sum().reset_index()
    fig = px.line(sales_by_period, x='sale_date', y='sale_amount', title="Sales by Day")
elif view_by == "Month":
    sales_by_period = filtered_data.groupby(filtered_data['sale_date'].dt.to_period("M"))['sale_amount'].sum().reset_index()
    sales_by_period['sale_date'] = sales_by_period['sale_date'].astype(str)  # Convert Period to string
    fig = px.bar(sales_by_period, x='sale_date', y='sale_amount', title="Sales by Month")
else:  # Year
    sales_by_period = filtered_data.groupby(filtered_data['sale_date'].dt.year)['sale_amount'].sum().reset_index()
    fig = px.bar(sales_by_period, x='sale_date', y='sale_amount', title="Sales by Year")

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sales by Location with heatmap
st.header("📍 Sales Heatmap by Location")
sales_by_location = filtered_data.groupby('location')['sale_amount'].sum().reset_index()
fig = px.density_heatmap(sales_by_location, x='location', y='sale_amount', title="Sales by Location", labels={'sale_amount': 'Sales Amount', 'location': 'Location'}, color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

# Most Sold Products
st.header("🛒 Top Products Sold")
top_products = filtered_data.groupby('product_id')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False)
fig = px.bar(top_products, x='product_id', y='quantity', title="Top Products Sold", labels={'product_id': 'Product ID', 'quantity': 'Quantity Sold'}, color='quantity', color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

# Sales Channel Analysis
st.header("💻 Sales by Channel")
sales_by_channel = filtered_data.groupby('sale_channel')['sale_amount'].sum().reset_index()
fig = px.pie(sales_by_channel, names='sale_channel', values='sale_amount', title="Sales Distribution by Channel", color_discrete_sequence=px.colors.sequential.Teal)
st.plotly_chart(fig)

# Customer Demographics (Gender, Age)
st.header("👥 Customer Demographics")
gender_distribution = filtered_data.groupby('customer_gender')['sale_amount'].sum().reset_index()
fig = px.pie(gender_distribution, names='customer_gender', values='sale_amount', title="Sales by Gender", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig)

age_distribution = filtered_data.groupby('customer_age')['sale_amount'].sum().reset_index()
fig = px.bar(age_distribution, x='customer_age', y='sale_amount', title="Sales by Customer Age", labels={'customer_age': 'Customer Age', 'sale_amount': 'Sales Amount'}, color='sale_amount', color_continuous_scale=px.colors.sequential.Turbo)
st.plotly_chart(fig)

# Close MySQL connection
cursor.close()
mydb.close()
