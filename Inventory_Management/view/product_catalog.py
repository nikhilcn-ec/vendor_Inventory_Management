import streamlit as st
import mysql.connector  
import os

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory"
)
cursor = mydb.cursor()

st.title("Product_catalog")

tab1, tab2, tab3, tab4 = st.tabs(['Add Products', 'Remove Products', 'Update Products', 'View Products'])

with tab1:
    # Streamlit interface
    st.header("Vendor Product Upload")

    # Inputs from the user
    product_name = st.text_input("Enter Product Name")
    category = st.text_input("Enter Product Category")
    mrp = st.number_input("Enter MRP", min_value=0.0, format="%.2f")
    discount = st.number_input("Enter Discount (%)", min_value=0.0, format="%.2f")
    image = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])

    if st.button("Save Product"):
        if product_name and category and mrp:
            # Create the directory to store images if it doesn't exist
            image_directory = "product_images"
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            # Save the uploaded image to the local directory
            image_path = os.path.join(image_directory, image.name)
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

            # SQL query to insert the product data into the database
            query = """
                INSERT INTO vendor_products (product_name, category, mrp, discount, image)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (product_name, category, mrp, discount, image_path))
            mydb.commit()
            st.success("Product added successfully with image!")
        else:
            st.error("Please fill all fields and upload an image!")


with tab2:
    st.header("Product Catalog - Remove Products")

    # Retrieve products from the database
    cursor.execute("SELECT product_id, product_name FROM vendor_products")
    products = cursor.fetchall()

    # Display the list of products for removal
    if products:
        product_options = {f"{prod[1]} (ID: {prod[0]})": prod[0] for prod in products}
        selected_product = st.selectbox("Select a Product to Remove", options=list(product_options.keys()))

        # When the "Remove Product" button is clicked
        if st.button("Remove Product"):
            product_id = product_options[selected_product]
            
            # Delete the selected product from the database
            delete_query = "DELETE FROM vendor_products WHERE product_id = %s"
            cursor.execute(delete_query, (product_id,))
            mydb.commit()
            
            st.success(f"Product '{selected_product}' has been removed successfully.")
    else:
        st.write("No products available to remove.") 



with tab3:
    st.header("Product Catalog - Update Products")

    # Retrieve products from the database
    cursor.execute("SELECT product_id, product_name FROM vendor_products")  # Changed 'id' to 'product_id'
    products = cursor.fetchall()

    if products:
        product_options = {f"{prod[1]} (ID: {prod[0]})": prod[0] for prod in products}
        selected_product = st.selectbox("Select a Product to Update", options=list(product_options.keys()))

        # Fetch current product details for the selected product
        product_id = product_options[selected_product]
        cursor.execute("SELECT product_name, category, mrp, discount, image FROM vendor_products WHERE product_id = %s", (product_id,))  # Changed 'id' to 'product_id'
        product_data = cursor.fetchone()

        # Prefill current details in the form
        if product_data:
            product_name = st.text_input("Product Name", value=product_data[0])
            category = st.text_input("Category", value=product_data[1])
            mrp = st.number_input("MRP", value=float(product_data[2]), format="%.2f")
            discount = st.number_input("Discount (%)", value=float(product_data[3]), format="%.2f")
            
            # Option to update the image
            current_image = product_data[4]
            st.write(f"Current Image: {current_image}")
            image = st.file_uploader("Upload New Image (optional)", type=["jpg", "jpeg", "png"])

            if st.button("Update Product"):
                # Handle image update if a new image is uploaded
                if image:
                    image_directory = "product_images"
                    if not os.path.exists(image_directory):
                        os.makedirs(image_directory)
                    
                    # Save new image to the local directory
                    image_path = os.path.join(image_directory, image.name)
                    with open(image_path, "wb") as f:
                        f.write(image.getbuffer())
                else:
                    # Keep the old image path if no new image is uploaded
                    image_path = current_image

                # SQL query to update the product details in the database
                update_query = """
                    UPDATE vendor_products
                    SET product_name = %s, category = %s, mrp = %s, discount = %s, image = %s
                    WHERE product_id = %s  # Changed 'id' to 'product_id'
                """
                cursor.execute(update_query, (product_name, category, mrp, discount, image_path, product_id))
                mydb.commit()
                st.success(f"Product '{product_name}' has been updated successfully.")
    else:
        st.write("No products available to update.")


with tab4:
    st.header("Product Catalog - View Products")

    # Retrieve products from the database
    cursor.execute("SELECT product_name, image FROM vendor_products")
    products = cursor.fetchall()

    if products:
        # Create a grid layout with columns
        for idx, product in enumerate(products):
            product_name = product[0]
            product_image = product[1]

            # Create a new row every 3 products
            if idx % 3 == 0:
                cols = st.columns(3)

            # Display each product in a card-like structure
            with cols[idx % 3]:
                # Check if product image is a valid local path or a URL
                if product_image:
                    if product_image.startswith("http"):  # If it's a URL
                        st.image(product_image, use_column_width=True)
                    elif os.path.isfile(product_image):  # If it's a local file
                        st.image(product_image, use_column_width=True)
                    else:  # Handle missing image
                        st.image("https://via.placeholder.com/150?text=No+Image", use_column_width=True)
                        st.write("_Image not available_")
                else:  # If no image is provided in the database
                    st.image("https://via.placeholder.com/150?text=No+Image", use_column_width=True)
                    st.write("_Image not available_")

                st.write(f"**{product_name}**")
    else:
        st.write("No products available to view.")

