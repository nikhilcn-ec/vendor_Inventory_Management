import os
import streamlit as st
from dotenv import load_dotenv
import mysql.connector
import google.generativeai as gen_ai
import plotly.express as px
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro & Sales Data",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Connect to MySQL (sales database)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory"
)
cursor = mydb.cursor()

# Function to handle sales data queries and visualizations
def handle_sales_query(query):
    try:
        # Example query for total sales
        if "total sales" in query.lower():
            cursor.execute("SELECT SUM(sale_amount) FROM sales")
            result = cursor.fetchone()
            return f"Total sales amount is ${result[0]:,.2f}"
        
        # Example query for sales by location with visualization
        elif "sales by location" in query.lower():
            cursor.execute("SELECT location, SUM(sale_amount) FROM sales GROUP BY location")
            result = cursor.fetchall()
            
            # Prepare text response
            response = "Sales by location:\n"
            for row in result:
                response += f"- {row[0]}: ${row[1]:,.2f}\n"
            
            # Prepare data for visualization
            df = pd.DataFrame(result, columns=["Location", "Total Sales"])
            fig = px.bar(df, x="Location", y="Total Sales", title="Sales by Location")
            
            # Return text and figure
            return response, fig
        
        # Example query for sales by product with visualization
        elif "sales by product" in query.lower():
            cursor.execute("SELECT product_id, SUM(sale_amount) FROM sales GROUP BY product_id")
            result = cursor.fetchall()
            
            # Prepare text response
            response = "Sales by product:\n"
            for row in result:
                response += f"- Product {row[0]}: ${row[1]:,.2f}\n"
            
            # Prepare data for visualization
            df = pd.DataFrame(result, columns=["Product ID", "Total Sales"])
            fig = px.bar(df, x="Product ID", y="Total Sales", title="Sales by Product")
            
            # Return text and figure
            return response, fig

        # Example query for sales by day, month, and year with visualization
        elif "sales by day" in query.lower():
            cursor.execute("SELECT DATE(sale_date), SUM(sale_amount) FROM sales GROUP BY DATE(sale_date)")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=["Sale Date", "Total Sales"])
            fig = px.line(df, x="Sale Date", y="Total Sales", title="Sales by Day")
            return "Sales by day visualized below:", fig

        elif "sales by month" in query.lower():
            cursor.execute("SELECT DATE_FORMAT(sale_date, '%Y-%m'), SUM(sale_amount) FROM sales GROUP BY DATE_FORMAT(sale_date, '%Y-%m')")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=["Month", "Total Sales"])
            fig = px.line(df, x="Month", y="Total Sales", title="Sales by Month")
            return "Sales by month visualized below:", fig

        elif "sales by year" in query.lower():
            cursor.execute("SELECT YEAR(sale_date), SUM(sale_amount) FROM sales GROUP BY YEAR(sale_date)")
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=["Year", "Total Sales"])
            fig = px.line(df, x="Year", y="Total Sales", title="Sales by Year")
            return "Sales by year visualized below:", fig
        
        else:
            return "I can only answer questions related to 'total sales', 'sales by location', 'sales by product', or 'sales by day/month/year' for now.", None
    except Exception as e:
        return f"An error occurred: {str(e)}", None

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.markdown("<h2 style='text-align: center;'>🤖 Chat with Gemini-Pro & Sales Data</h2>", unsafe_allow_html=True)

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask anything, including sales queries or visualizations!")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Check if the query is related to sales data
    if "sales" in user_prompt.lower():
        # Handle sales data query and visualization
        sales_response, sales_fig = handle_sales_query(user_prompt)
        
        # Display text response
        with st.chat_message("assistant"):
            st.markdown(sales_response)
        
        # Display visual response if available
        if sales_fig:
            with st.chat_message("assistant"):
                st.plotly_chart(sales_fig)

    else:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Close MySQL connection at the end
cursor.close()
mydb.close()
