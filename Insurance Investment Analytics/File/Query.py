import mysql.connector
import streamlit as st

# Connection settings
conn = mysql.connector.connect(
    host="localhost",
    port="3306",          # Fixed: Changed from 330 to 3306
    user="root",
    password="leanna_miya",
    database="salesdb"  # Make sure this matches your actual phpMyAdmin database name!
)
c = conn.cursor()

# Fetch data
def view_all_data():
    c.execute('SELECT * FROM us_insurance_analytics_data ORDER BY id ASC')
    data = c.fetchall()
    return data


