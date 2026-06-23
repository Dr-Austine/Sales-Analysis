import streamlit as st
import mysql.connector

def view_all_data():
    # Streamlit securely pulls these variables from your Secrets settings in the cloud dashboard
    conn = mysql.connector.connect(
        host=st.secrets["db_host"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        database=st.secrets["db_name"],
        port=int(st.secrets.get("db_port", 3306))
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table_name") # Double check your actual table name here!
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


