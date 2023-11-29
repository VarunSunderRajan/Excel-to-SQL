import pandas as pd
import numpy as np
import sqlite3
import os
import sys
import sqlalchemy as sqla
from sqlalchemy import create_engine
import tensorflow as tf
import pyodbc
from sql_server_details import create_new_database, get_db_connection
from data_organizer import read_excel_to_df, extract_brand, add_brand_column, organize_by_category, organize_by_brand
from db_structure import create_brands_table, create_categories_table, create_products_table, create_salesdata_table, insert_brands, insert_categories, insert_products, insert_salesdata, print_table_data, query_data_by_brand, query_data_by_category
excel_file_path = r'C:\Users\varun\OneDrive\Desktop\coding\Coding Projects\Data Science\Sales by Product - 20231127-162215666 (1).xlsx'
sheet_for_analysis = 'Sales by Product'
df = read_excel_to_df(excel_file_path, sheet_for_analysis)
df_with_brands = add_brand_column(df)
categorical_data = organize_by_category(df_with_brands)
brand_data = organize_by_brand(df_with_brands)
#print(categorical_data)
#print(brand_data)
#------------------------------------------------------------
# Gather credentials and other details
#for now here are the relevant server details:
server = 'DESKTOP-1L7VJ7P\SQLEXPRESS'
db_name = 'WeedConsultationDemo'
username = 'sa'
password = 'WestcannaInf0Dem0_Tr1al$'
#server = input("Enter your server name (e.g., 'localhost\\SQLEXPRESS'): ")
#db_name = input("Enter the name of the new database you want to create: ")
#username = input("Enter your username: ")
#password = input("Enter your password: ")

# Create a new database
#create_new_database(server, db_name, username, password)

# ... previous code ...

# Get a connection to the newly created database
conn = get_db_connection(server, db_name, username, password)
cursor = conn.cursor()
#------------------------------------------------------------
# Create the tables
#create_brands_table(cursor)
#print("Brands table created successfully.")

#create_categories_table(cursor)
#print("Categories table created successfully.")

#create_products_table(cursor)
#print("Products table created successfully.")

#create_salesdata_table(cursor)
#print("SalesData table created successfully.")
#------------------------------------------------------------
# Insert data into tables
#insert_brands(df_with_brands, cursor)
#print("Brands data inserted successfully.")

#insert_categories(df_with_brands, cursor)
#print("Categories data inserted successfully.")

#insert_products(df_with_brands, cursor)
#print("Products data inserted successfully.")

#insert_salesdata(df_with_brands, cursor)
#print("Sales data inserted successfully.")
#------------------------------------------------------------
# Print data from each table
#print_table_data('Brands', cursor)
#print_table_data('Categories', cursor)
#print_table_data('Products', cursor)
#print_table_data('SalesData', cursor)
#------------------------------------------------------------
# Query data from the database
query_data_by_brand('Simply Bare', cursor)
query_data_by_category('Pre-Roll', cursor)
# Commit the changes
conn.commit()

# Your code to insert data goes here...

# Close the cursor and connection when done
cursor.close()
conn.close()

