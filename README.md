# Vendor Inventory Management

## Overview
This project is a streamlined inventory management system that enables vendors to efficiently manage stock levels, product catalog, and sales tracking. The application is built with Python and Streamlit for the frontend and MySQL for the backend database. 

## Features
- Add, update, and view product stock.
- View and edit product catalog with images.
- Monitor inventory with data visualizations.

## Prerequisites
To run this project, ensure you have the following software and tools installed:
1. **Python** (version 3.12.5)
2. **MySQL** (for database management)

## Installation Guide

### Step 1: Clone the Repository
Clone this repository to your local system:
```bash
git clone https://github.com/yourusername/vendor-inventory-management.git
cd vendor-inventory-management
```

### Step 2: Install Python Dependencies
Install the necessary Python libraries using the `requirements.txt` file provided:
```bash
pip install -r requirements.txt
```

The required libraries include:
- `streamlit` - for creating the user interface.
- `mysql-connector-python` - for MySQL database connection.
- `pandas` - for data manipulation.
- `plotly` - for data visualization.

Alternatively, if you don't have `requirements.txt`, you can install the libraries manually:
```bash
pip install streamlit mysql-connector-python pandas plotly
```

### Step 3: Set Up MySQL Database
1. **Open MySQL** in your system and execute the following SQL commands to create the required database and tables.

#### Database and Table Creation

1. **Create the Database**:
   ```sql
   CREATE DATABASE IF NOT EXISTS inventory;
   USE inventory;
   ```

2. **Create `product_stock` Table**:
   ```sql
   CREATE TABLE product_stock (
       stock_id INT PRIMARY KEY,
       product_id INT NOT NULL,
       quantity INT NOT NULL,
       minimum_stock INT NOT NULL,
       maximum_stock INT NOT NULL
   );
   ```

3. **Create `vendor_products` Table**:
   ```sql
   CREATE TABLE vendor_products (
       product_id INT PRIMARY KEY,
       product_name VARCHAR(255) NOT NULL,
       product_price DECIMAL(10, 2) NOT NULL,
       discount_percentage DECIMAL(5, 2),
       product_image VARCHAR(255)
   );
   ```

4. **Insert Sample Data**:
   To load some initial data into the tables, you can use these sample insert commands:
   ```sql
   INSERT INTO product_stock (stock_id, product_id, quantity, minimum_stock, maximum_stock) VALUES
   (1, 1, 100, 20, 150),
   (2, 2, 50, 10, 200);
   
   INSERT INTO vendor_products (product_id, product_name, product_price, discount_percentage, product_image) VALUES
   (1, 'Sample Product A', 25.00, 10.0, 'path/to/image_a.jpg'),
   (2, 'Sample Product B', 15.50, 5.0, 'path/to/image_b.jpg');
   ```

**Note**: Update `product_image` paths based on where you store your images.

### Step 4: Configure Database Connection in Python
In the main project file (e.g., `app.py`), update the database connection details with your MySQL credentials:
```python
import mysql.connector

mydb = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="inventory"
)
```

### Step 5: Run the Application
Once the setup is complete, you can run the Streamlit application using:
```bash
streamlit run app.py
```

The application will open in your browser, typically at `http://localhost:8501`.

## Usage
- **Inventory Management**: View, add, and update inventory levels with dynamic data visualizations.
- **Product Catalog**: Add new products, including images, prices, and discounts. View products in a card-based layout.
- **Stock Monitoring**: Check product levels and receive feedback on low or high stock levels.

## Project Structure
Here’s a quick overview of the file structure:

```
vendor-inventory-management/
├── app.py                     # Main application file
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── sql_setup.sql              # SQL script for database setup
└── images/                    # Directory to store product images
```

## Troubleshooting
- **Database Connection Issues**: Ensure that your MySQL service is running and that the connection details in `app.py` are correct.
- **Module Not Found Errors**: Reinstall dependencies using `pip install -r requirements.txt` to ensure all libraries are installed.

---

This README file should help you quickly set up and start using the Vendor Inventory Management project.
