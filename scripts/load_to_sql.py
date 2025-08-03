import pandas as pd
import pyodbc

# Load cleaned data
df = pd.read_csv('/home/azureuser/airflow/data/processed/clean_superstore.csv')

# Database connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=<server name>;"
    "DATABASE=<database name);"
    "UID=<userid>;"
    "PWD=<pwd>"
)

# Connect and insert data
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO sales (OrderID, OrderDate, ProductName, Total)
            VALUES (?, ?, ?, ?)
        """, row['Order ID'], row['Order Date'], row['Product Name'], row['Total'])
    
    conn.commit()
