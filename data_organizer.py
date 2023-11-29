import pandas as pd
import tensorflow as tf
import pyodbc
excel_file_path = r'C:\Users\varun\OneDrive\Desktop\coding\Coding Projects\Data Science\Sales by Product - 20231127-162215666 (1).xlsx'
sheet_for_analysis = 'Sales by Product'
def read_excel_to_df(path, sheetName):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_for_analysis)
    return df

def extract_brand(product_name):
    """
    Extracts the brand name from the product name string, considering multiple words
    and special characters, with the assumption that the first hyphen encountered
    separates the brand from the product.
    
    Parameters:
    - product_name: The full product name string.
    
    Returns:
    - The extracted brand name.
    """
    # Split the product name at the first hyphen.
    # The '1' argument in split() function ensures only the first hyphen is used to split.
    parts = product_name.split('-', 1)
    
    # The brand name is assumed to be the part before the first hyphen.
    brand = parts[0].strip()
    
    # Optionally, clean the brand name of any leading/trailing special characters or numbers.
    # This step depends on the consistency of your data.
    return brand
def add_brand_column(df):
    """
    Adds a new 'Brand' column to the DataFrame at the very front.
    
    Parameters:
    - df: The pandas DataFrame with the product data.
    
    Returns:
    - The DataFrame with an additional 'Brand' column at the front.
    """
    # Apply the extract_brand function to the 'Product' column to create a new 'Brand' column
    df['Brand'] = df['Product'].apply(extract_brand)
    
    # Reorder the columns to put 'Brand' at the front
    cols = df.columns.tolist()
    cols = ['Brand'] + [col for col in cols if col != 'Brand']
    df = df[cols]
    
    return df

def organize_by_category(df):
    """
    Organizes products by their categories.
    
    Parameters:
    - df: The pandas DataFrame with the product data.
    
    Returns:
    - A dictionary with categories as keys and DataFrames of products as values.
    """
    category_groups = df.groupby('Classification')
    return {category: category_groups.get_group(category) for category in category_groups.groups}

def organize_by_brand(df):
    """
    Organizes products by their brands.
    
    Parameters:
    - df: The pandas DataFrame with the product data.
    
    Returns:
    - A dictionary with brands as keys and DataFrames of products as values.
    """
    brand_groups = df.groupby('Brand')
    return {brand: brand_groups.get_group(brand) for brand in brand_groups.groups}


df = read_excel_to_df(excel_file_path, sheet_for_analysis)
#print(df.head())
df_with_brands = add_brand_column(df)
#print(df_with_brands)
organized_data = organize_by_category(df_with_brands)
# 'organized_data' is a dictionary with categories as keys
# You can iterate over it and work with each category's DataFrame
#for category, category_df in organized_data.items():
#    print(f"Category: {category}")
#    print(category_df)

#for brand, brand_df in organize_by_brand(df_with_brands).items():
#    print(f"Brand: {brand}")
#    print(brand_df)