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
pip install streamlit mysql-connector-python pandas plotly matplotlib python-dotenv==1.0.1 google-generativeai==0.3.2
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

   INSERT INTO vendor_products (product_id, product_name, category, mrp, discount, image, created_at) VALUES
   (1, 'Zebronics Mouse', 'Electronics', 500.00, 20.00, 'product_images/mouse.jpeg', '2024-10-18 21:31:31'),
   (2, 'Brown Hat', 'Accessories', 25.99, 0.00, 'product_images/hat.jpeg', '2024-10-18 21:55:05'),
   (3, 'Orange Volkswagen', 'Vehicles', 15500.00, 0.00, 'product_images/car.jpeg', '2024-10-18 21:55:05'),
   (4, 'Assorted Spices', 'Food', 5.99, 0.00, 'product_images/spices.jpeg', '2024-10-18 21:55:05'),
   (5, 'Fresh Salmon Steaks', 'Food', 20.00, 0.00, 'https://images.pexels.com/photos/1860201/pexels-photo-1860201.jpeg', '2024-10-18 21:55:05'),
   (6, 'Apple iPhone 13', 'Smartphones', 799.99, 10.00, 'https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-13-01.jpg', '2024-10-18 22:25:38'),
   (7, 'Sony WH-1000XM4', 'Headphones', 349.99, 15.00, 'https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SL1500_.jpg', '2024-10-18 22:25:38'),
   (8, 'Samsung Galaxy Tab S7', 'Tablets', 649.99, 5.00, NULL, '2024-10-18 22:25:38'),
   (9, 'Dell XPS 13', 'Laptops', 999.99, 8.00, NULL, '2024-10-18 22:25:38'),
   (10, 'Nike Air Max 270', 'Footwear', 150.00, 12.00, NULL, '2024-10-18 22:25:38'),
   -- Continue inserting other records...
   (40, 'Logitech MX Master 3', 'Computer Accessories', 99.99, 15.00, NULL, '2024-10-18 22:33:46');

   INSERT INTO sales (sale_id, product_id, quantity, sale_amount, sale_date, location, customer_age, customer_gender, payment_type, sale_channel) VALUES
   (1, 1, 1, 3199.99, '2023-10-01 00:00:00', 'Seattle, WA', 22, 'Female', 'Credit Card', 'Amazon'),
   (2, 1, 1, 166.99, '2023-10-10 00:00:00', 'San Diego, CA', 34, 'Male', 'Debit Card', 'NextGen'),
   (3, 1, 1, 2133.98, '2023-11-12 00:00:00', 'Los Angeles, CA', 40, 'Female', 'Cash', 'Flipkart'),
   (4, 2, 2, 4119.96, '2023-11-05 00:00:00', 'Chicago, IL', 29, 'Male', 'PayPal', 'Amazon'),
   (5, 2, 1, 129.99, '2024-01-22 00:00:00', 'New York, NY', 34, 'Female', 'Credit Card', 'NextGen'),
   (6, 3, 1, 1399.99, '2024-02-15 00:00:00', 'San Francisco, CA', 28, 'Male', 'Debit Card', 'Flipkart'),
   (7, 3, 2, 2799.98, '2024-03-25 00:00:00', 'Philadelphia, PA', 31, 'Female', 'Credit Card', 'NextGen'),
   (8, 4, 1, 5149.99, '2023-12-10 00:00:00', 'Dallas, TX', 35, 'Male', 'Cash', 'Amazon'),
   (9, 4, 3, 389.97, '2023-12-15 00:00:00', 'Austin, TX', 30, 'Female', 'PayPal', 'Flipkart'),
   (10, 5, 1, 589.99, '2023-12-05 00:00:00', 'Houston, TX', 36, 'Male', 'Debit Card', 'NextGen'),
   (11, 6, 1, 3299.99, '2024-03-17 00:00:00', 'Chicago, IL', 22, 'Female', 'Credit Card', 'Amazon'),
   (12, 7, 1, 659.99, '2023-11-30 00:00:00', 'Los Angeles, CA', 35, 'Male', 'PayPal', 'Flipkart'),
   (13, 8, 1, 2399.99, '2023-10-10 00:00:00', 'New York, NY', 29, 'Female', 'Cash', 'NextGen'),
   (14, 9, 1, 119.99, '2024-01-01 00:00:00', 'San Francisco, CA', 24, 'Male', 'Credit Card', 'Amazon'),
   (15, 10, 1, 4249.99, '2024-03-10 00:00:00', 'San Diego, CA', 36, 'Female', 'Debit Card', 'Flipkart'),
   (16, 10, 2, 249.98, '2024-04-01 00:00:00', 'Dallas, TX', 30, 'Male', 'PayPal', 'NextGen'),
   (17, 11, 1, 599.99, '2023-10-20 00:00:00', 'Phoenix, AZ', 28, 'Female', 'Credit Card', 'Amazon'),
   (18, 12, 1, 249.99, '2023-11-05 00:00:00', 'Seattle, WA', 32, 'Male', 'Cash', 'Flipkart'),
   (19, 13, 1, 3199.99, '2024-02-20 00:00:00', 'Los Angeles, CA', 29, 'Female', 'Debit Card', 'NextGen'),
   (20, 14, 1, 499.99, '2023-12-01 00:00:00', 'Chicago, IL', 41, 'Male', 'PayPal', 'Amazon'),
   -- Add remaining records here following the same pattern...
   -- Ensure to continue with all values up to record 80 or as needed.
   (80, 33, 1, 3199.99, '2024-02-15 00:00:00', 'Houston, TX', 33, 'Male', 'PayPal', 'NextGen');
   
   -- Continue adding more INSERT statements as needed up to the last record provided.

   INSERT INTO product_stock (stock_id, product_id, quantity, minimum_stock, maximum_stock) VALUES
   (1, 1, 103, 20, 151),
   (2, 2, 100, 20, 200),
   (3, 3, 50, 10, 150),
   (4, 4, 200, 30, 300),
   (5, 5, 75, 15, 120),
   (6, 6, 0, 5, 80),
   (7, 7, 120, 25, 250),
   (8, 8, 30, 10, 70),
   (9, 9, 90, 20, 160),
   (10, 10, 40, 5, 100),
   (11, 11, 150, 40, 220),
   (12, 12, 25, 5, 60),
   (13, 13, 80, 20, 140),
   (14, 14, 200, 50, 300),
   (15, 15, 60, 10, 110),
   (16, 16, 0, 0, 30),
   (17, 17, 90, 15, 190),
   (18, 18, 70, 20, 130),
   (19, 19, 110, 25, 210),
   (20, 20, 5, 1, 25),
   (21, 21, 85, 10, 170),
   (22, 22, 45, 5, 100),
   (23, 23, 120, 30, 180),
   (24, 24, 60, 10, 130),
   (25, 25, 95, 15, 165),
   (26, 26, 30, 0, 80),
   (27, 27, 0, 0, 20),
   (28, 28, 75, 15, 130),
   (29, 29, 150, 40, 220),
   (30, 30, 25, 5, 60),
   (31, 31, 100, 20, 200),
   (32, 32, 40, 10, 80),
   (33, 33, 90, 20, 150),
   (34, 34, 60, 10, 130),
   (35, 35, 5, 1, 30),
   (36, 36, 80, 20, 140),
   (37, 37, 0, 0, 10),
   (38, 38, 200, 50, 300),
   (39, 39, 70, 15, 120),
   (40, 40, 110, 25, 200);
   
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
