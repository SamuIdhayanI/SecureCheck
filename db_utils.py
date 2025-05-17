import streamlit as st
import mysql.connector
import pandas as pd

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sacheart$731",
            database="securecheck"
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
                return df
        finally:
            connection.close()
    return pd.DataFrame()
