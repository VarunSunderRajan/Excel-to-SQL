import pandas as pd
import numpy as np
import sqlite3
import os
import sys
import sqlalchemy as sqla
from sqlalchemy import create_engine
import tensorflow as tf
import pyodbc
def create_brands_table(cursor):
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Brands' and xtype='U')
        CREATE TABLE Brands (
            BrandID INT PRIMARY KEY IDENTITY(1,1),
            BrandName NVARCHAR(255)
        )
    """)
def create_categories_table(cursor):
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Categories' and xtype='U')
        CREATE TABLE Categories (
            CategoryID INT PRIMARY KEY IDENTITY(1,1),
            CategoryName NVARCHAR(255)
        )
    """)
def create_products_table(cursor):
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Products' and xtype='U')
        CREATE TABLE Products (
            ProductID INT PRIMARY KEY IDENTITY(1,1),
            SKU NVARCHAR(255),
            ProductName NVARCHAR(255),
            BrandID INT,
            CategoryID INT,
            FOREIGN KEY (BrandID) REFERENCES Brands(BrandID),
            FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
        )
    """)
def create_salesdata_table(cursor):
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SalesData' and xtype='U')
        CREATE TABLE SalesData (
            SalesID INT PRIMARY KEY IDENTITY(1,1),
            ProductID INT,
            DateID INT, -- If you have a Dates table
            ItemsSold INT,
            TotalSales DECIMAL(18, 2),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
            -- FOREIGN KEY (DateID) REFERENCES Dates(DateID) -- If using Dates table
        )
    """)

def insert_brands(df, cursor):
    unique_brands = df['Brand'].unique()
    for brand in unique_brands:
        cursor.execute("INSERT INTO Brands (BrandName) VALUES (?)", brand)

def insert_categories(df, cursor):
    unique_categories = df['Classification'].unique()
    for category in unique_categories:
        cursor.execute("INSERT INTO Categories (CategoryName) VALUES (?)", category)

def insert_products(df, cursor):
    for index, row in df.iterrows():
        # Retrieve BrandID and CategoryID
        cursor.execute("SELECT BrandID FROM Brands WHERE BrandName = ?", row['Brand'])
        brand_id = cursor.fetchone()[0]

        cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = ?", row['Classification'])
        category_id = cursor.fetchone()[0]

        # Insert product data
        cursor.execute("INSERT INTO Products (SKU, ProductName, BrandID, CategoryID) VALUES (?, ?, ?, ?)",
                       row['SKU'], row['Product'], brand_id, category_id)

def insert_salesdata(df, cursor):
    for index, row in df.iterrows():
        # Retrieve ProductID
        cursor.execute("SELECT ProductID FROM Products WHERE SKU = ?", row['SKU'])
        product_id = cursor.fetchone()[0]

        # Adjust the column names to match your DataFrame's column names
        items_sold = row.get('Items Sold', 0)  # Use 'Items Sold' as per your Excel file
        gross_sales = row.get('Gross Sales', 0.0)  # Use 'Gross Sales' as per your Excel file

        # Update the query with correct column names as per your SalesData table
        cursor.execute("INSERT INTO SalesData (ProductID, ItemsSold, TotalSales) VALUES (?, ?, ?)",
                       product_id, items_sold, gross_sales)

def print_table_data(table_name, cursor):
    print(f"Data from {table_name} table:")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in cursor.description]
        print(", ".join(columns))  # Print column names
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
    print("\n")

def query_data_by_brand(brand_name, cursor):
    print(f"\nData for brand: {brand_name}")
    try:
        cursor.execute("""
            SELECT p.ProductName, p.SKU, sd.ItemsSold, sd.TotalSales
            FROM Products p
            JOIN Brands b ON p.BrandID = b.BrandID
            JOIN SalesData sd ON p.ProductID = sd.ProductID
            WHERE b.BrandName = ?
        """, brand_name)
        print("ProductName, SKU, ItemsSold, TotalSales")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Error fetching data for brand {brand_name}: {e}")
    print("\n")


def query_data_by_category(category_name, cursor):
    print(f"\nData for category: {category_name}")
    try:
        cursor.execute("""
            SELECT c.CategoryName, b.BrandName, p.ProductName, p.SKU, sd.ItemsSold, sd.TotalSales
            FROM Categories c
            JOIN Products p ON c.CategoryID = p.CategoryID
            JOIN Brands b ON p.BrandID = b.BrandID
            JOIN SalesData sd ON p.ProductID = sd.ProductID
            WHERE c.CategoryName = ?
        """, category_name)
        print("CategoryName, BrandName, ProductName, SKU, ItemsSold, TotalSales")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Error fetching data for category {category_name}: {e}")

