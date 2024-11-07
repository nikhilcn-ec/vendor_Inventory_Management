# Vendor Inventory Management

## Overview
This project provides a streamlined inventory management system that enables vendors to efficiently manage stock levels, product catalogs, and sales tracking. The application is built with **Python** and **Streamlit** for the frontend and **MySQL** as the backend database.

## Features
- **Inventory Management**: Add, update, and view product stock with real-time tracking.
- **Product Catalog**: Add and manage product details, including images, prices, and discounts.
- **Sales Monitoring**: Track sales transactions with details such as location, customer demographics, payment methods, and sale channels.
- **User Management**: Distinguish between customer and vendor users, track user details, and associate vendors with companies.

## Prerequisites
To run this project, ensure the following software and tools are installed:
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

Required libraries include:
- `streamlit` - for creating the user interface.
- `mysql-connector-python` - for MySQL database connection.
- `pandas` - for data manipulation.
- `plotly` - for data visualization.

If you don't have `requirements.txt`, install the libraries manually:
```bash
pip install streamlit mysql-connector-python pandas plotly python-dotenv==1.0.1 google-generativeai==0.3.2
```

### Step 3: Set Up MySQL Database
1. **Open MySQL** in your system and execute the following SQL commands to create the required database and tables.

#### Database and Table Creation

1. **Create the Database**:
   ```sql
   CREATE DATABASE IF NOT EXISTS inventory;
   USE inventory;
   ```

2. **Create `users` Table**:
   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id INT PRIMARY KEY AUTO_INCREMENT,
       name VARCHAR(50) NOT NULL,
       email VARCHAR(100) UNIQUE,
       phone VARCHAR(15),
       password VARCHAR(100),
       user_type ENUM('vendor', 'customer') NOT NULL,
       company_name VARCHAR(100),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **Create `sales` Table**:
   ```sql
   CREATE TABLE IF NOT EXISTS sales (
       sale_id INT PRIMARY KEY AUTO_INCREMENT,
       product_id INT,
       quantity DECIMAL(10, 2),
       sale_amount DECIMAL(10, 2),
       sale_date DATETIME,
       location VARCHAR(100),
       customer_age INT,
       customer_gender ENUM('Male', 'Female'),
       payment_type VARCHAR(20),
       sale_channel VARCHAR(50)
   );
   ```

4. **Create `product_stock` Table**:
   ```sql
   CREATE TABLE IF NOT EXISTS product_stock (
       stock_id INT PRIMARY KEY AUTO_INCREMENT,
       product_id INT NOT NULL,
       quantity INT NOT NULL,
       minimum_stock INT NOT NULL,
       maximum_stock INT NOT NULL,
       FOREIGN KEY (product_id) REFERENCES vendor_products(product_id)
   );
   ```

5. **Create `vendor_products` Table**:
   ```sql
   CREATE TABLE IF NOT EXISTS vendor_products (
       product_id INT PRIMARY KEY AUTO_INCREMENT,
       product_name VARCHAR(255) NOT NULL,
       category VARCHAR(50),
       mrp DECIMAL(10, 2) NOT NULL,
       discount DECIMAL(5, 2),
       image VARCHAR(255),
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP
   );
   ```

6. **Insert Sample Data**:
   Load some initial data into the tables:
   ```sql
   INSERT INTO users (name, email, phone, password, user_type, company_name) VALUES
   ('Nikhil Cn', 'nikhilcnn123@gmail.com', '8123456789', '123', 'vendor', 'evacreare'),
   ('Bipin', 'tekkedha123@gmail.com', '1224272581', '111', 'customer', NULL);

   INSERT INTO vendor_products (product_name, category, mrp, discount, image) VALUES
   ('Zebronics Mouse', 'Electronics', 500.00, 20.00, 'product_images/mouse.jpeg'),
   ('Brown Hat', 'Accessories', 25.99, 0.00, 'product_images/hat.jpeg'),
   ('Orange Volkswagen', 'Vehicles', 15500.00, 0.00, 'product_images/car.jpeg'),
   ('Assorted Spices', 'Food', 5.99, 0.00, 'product_images/spices.jpeg'),
   ('Apple iPhone 13', 'Smartphones', 799.99, 10.00, 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-01.jpg');

   INSERT INTO sales (product_id, quantity, sale_amount, sale_date, location, customer_age, customer_gender, payment_type, sale_channel) VALUES
   (1, 2, 1000.00, '2023-10-01 10:00:00', 'Seattle, WA', 22, 'Female', 'Credit Card', 'Amazon');

   INSERT INTO product_stock (product_id, quantity, minimum_stock, maximum_stock) VALUES
   (1, 100, 10, 200);
   ```

**Note**: Update `image` paths based on where you store your images.

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
- **Sales Tracking**: Review sales transactions, filter by location, date, and payment method.
- **User Management**: Manage users with details on their type, company association, and contact information.

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

This README should guide you through the setup and initial configuration of the Vendor Inventory Management project with a focus on user, sales, and inventory data management.
