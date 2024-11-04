import streamlit as st
import mysql.connector
import subprocess





mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory"
)
cursor=mydb.cursor()

tab1,tab2=st.tabs(['Log-In','Register'])

with tab2:
    with st.container(border=True):
        st.markdown("""<h3 style="text-align:center">Registration Form</h3>""",unsafe_allow_html=True)
        name=st.text_input("Name")
        email=st.text_input("Email")
        phone=st.text_input("Phone Number")
        password=st.text_input("Password",type="password")
        user=st.selectbox("register as?",('Customer','Vendor'),placeholder="choose an option")
        company=None
        if user == 'Vendor':
            company=st.text_input("company")
        submit=st.button("Register")
        if submit:
            sql="insert into users(name,email,phone,password,user_type,company_name) value(%s,%s,%s,%s,%s,%s)"
            value=(name,email,phone,password,user,company)
            cursor.execute(sql,value)
            mydb.commit()
            st.success(f'{user} registred succesfully!')


def email_validation(email):
    cursor.execute("select email from users")
    usr_email=cursor.fetchall()
    for emails in usr_email:
        if emails[0]== email:
            return 1;
        
        

with tab1:
     with st.container(border=True):
        st.markdown("""<h3 style="text-align:center">Sign In</h3>""",unsafe_allow_html=True)
        session_user=st.text_input("Username",key="session_user")
        session_email=st.text_input("email",key="session_email") 
        session_password=st.text_input("Password",type="password",key="session_password")
        if st.button("login"):
            if  email_validation(session_email):
                sql="SELECT name,password,user_type from users WHERE email=%s"
                value=(session_email,)
                cursor.execute(sql,value)
                usr,passw,usr_type=cursor.fetchone()
                if (usr,passw)==(session_user,session_password):
                    st.success("login Successfully")
                    if usr_type=='customer':
                        st.write("customer")
                    else:
                        subprocess.Popen(["streamlit", "run", "vendor.py"])

                else:
                    st.warning("invalid username or password")
            else:
               st.warning("inavlid email")        
            
            




          