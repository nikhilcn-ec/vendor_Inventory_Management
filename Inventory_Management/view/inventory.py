import streamlit as st
import mysql.connector  
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory"
)
cursor = mydb.cursor()

st.title("Inventory Management")

tab1, tab2, tab3 = st.tabs(['Add Stock', 'Update Stock', 'View Stocks'])

with tab1:
    st.header("Add Stock for Product")

    # Retrieve products from the database
    cursor.execute("SELECT product_id, product_name FROM vendor_products")
    products = cursor.fetchall()

    if products:
        product_options = {f"{prod[1]} (ID: {prod[0]})": prod[0] for prod in products}
        selected_product = st.selectbox("Select a Product", options=list(product_options.keys()))

        # Input for stock quantity
        quantity_to_add = st.number_input("Enter Quantity to Add", min_value=0, format="%d")

        # Input fields for minimum and maximum stock levels
        minimum_stock = st.number_input("Enter Minimum Stock Level", min_value=0, format="%d")
        maximum_stock = st.number_input("Enter Maximum Stock Level", min_value=0, format="%d")

        if st.button("Add Stock"):
            if quantity_to_add > 0:
                product_id = product_options[selected_product]

                # Insert stock entry into the product_stock table
                add_stock_query = """
                    INSERT INTO product_stock (product_id, quantity, minimum_stock, maximum_stock)
                    VALUES (%s, %s, %s, %s)
                """

                cursor.execute(add_stock_query, (product_id, quantity_to_add, minimum_stock, maximum_stock))
                mydb.commit()
                st.success(f"Stock added successfully for {selected_product}!")
            else:
                st.error("Please enter a valid quantity to add.")
    else:
        st.write("No products available to add stock.")

with tab2:
    st.header("Update Stock for Products")

    # Retrieve stocks from the database
    cursor.execute(""" 
        SELECT ps.stock_id, vp.product_name, ps.quantity 
        FROM product_stock ps 
        JOIN vendor_products vp ON ps.product_id = vp.product_id 
    """)
    stocks = cursor.fetchall()

    if stocks:
        # Create a dictionary to map product names to stock IDs
        stock_options = {f"{stock[1]} (Stock ID: {stock[0]})": stock[0] for stock in stocks}
        selected_stock = st.selectbox("Select a Product to Update Stock", options=list(stock_options.keys()))

        # Fetch current stock details
        stock_id = stock_options[selected_stock]
        cursor.execute("SELECT quantity FROM product_stock WHERE stock_id = %s", (stock_id,))
        current_quantity = cursor.fetchone()[0]

        # Input for updated stock quantity
        new_quantity = st.number_input("Enter New Stock Quantity", value=current_quantity, min_value=0, format="%d")

        if st.button("Update Stock"):
            update_stock_query = "UPDATE product_stock SET quantity = %s WHERE stock_id = %s"
            cursor.execute(update_stock_query, (new_quantity, stock_id))
            mydb.commit()
            st.success("Stock updated successfully!")
    else:
        st.write("No stock records available to update.")



with tab3:
    st.header("View Product Stocks")

    # Retrieve products and their stock levels from the database
    cursor.execute(""" 
        SELECT vp.product_name, ps.quantity, ps.minimum_stock, ps.maximum_stock 
        FROM product_stock ps 
        JOIN vendor_products vp ON ps.product_id = vp.product_id 
    """)
    stock_data = cursor.fetchall()

    if stock_data:
        # Create a DataFrame for better visualization
        df = pd.DataFrame(stock_data, columns=["Product Name", "Current Stock", "Minimum Stock", "Maximum Stock"])

        # Display the stock table
        st.write(df)

        # Create a candlestick-like visualization
        fig = go.Figure()

        # Add traces for current stock, minimum stock, and maximum stock
        fig.add_trace(go.Bar(
            x=df["Product Name"],
            y=df["Current Stock"],
            name="Current Stock",
            marker_color='blue'
        ))

        fig.add_trace(go.Scatter(
            x=df["Product Name"],
            y=df["Minimum Stock"],
            mode='lines+markers',
            name='Minimum Stock',
            line=dict(color='red', dash='dash')
        ))

        fig.add_trace(go.Scatter(
            x=df["Product Name"],
            y=df["Maximum Stock"],
            mode='lines+markers',
            name='Maximum Stock',
            line=dict(color='green', dash='dash')
        ))

        # Update layout for better visualization
        fig.update_layout(
            title="Current Stock Levels",
            xaxis_title="Products",
            yaxis_title="Stock Quantity",
            barmode='group',
            template='plotly_white'
        )

        st.plotly_chart(fig)


        st.subheader("Stock Distribution")
        pie_fig, pie_ax = plt.subplots(figsize=(8, 8))
        pie_ax.pie(df["Current Stock"], labels=df["Product Name"], autopct='%1.1f%%', startangle=90)
        pie_ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
        st.pyplot(pie_fig)

        # Visualization 3: Line chart for stock levels
        st.subheader("Stock Levels Over Products")
        line_fig, line_ax = plt.subplots(figsize=(10, 6))
        df.plot(x='Product Name', y=['Current Stock', 'Minimum Stock', 'Maximum Stock'], ax=line_ax, marker='o')
        line_ax.set_title("Stock Levels Comparison")
        line_ax.set_ylabel("Stock Quantity")
        line_ax.set_xlabel("Products")
        line_ax.legend(["Current Stock", "Minimum Stock", "Maximum Stock"])
        st.pyplot(line_fig)

        # Visualization 4: Histogram of current stock levels
        st.subheader("Distribution of Current Stock Levels")
        hist_fig, hist_ax = plt.subplots(figsize=(10, 6))
        hist_ax.hist(df["Current Stock"], bins=10, alpha=0.7, color='blue')
        hist_ax.set_title("Histogram of Current Stock Levels")
        hist_ax.set_xlabel("Stock Quantity")
        hist_ax.set_ylabel("Frequency")
        st.pyplot(hist_fig)

    else:
        st.write("No stock records available to view.")
