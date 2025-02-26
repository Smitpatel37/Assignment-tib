# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 19:03:43 2025

@author: Smit3
"""

import pandas as pd
import dtreg

# Load the CSV file
file_path = "covid-aqs-database_2021-03-24_version_1.csv"  # Replace with your actual file path
df = pd.read_csv(file_path, sep=";")

# Display basic information about the dataset
print("\nBasic Info:")
print(df.info())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# # Get summary statistics for numerical columns
# print("\nSummary Statistics:")
# print(df.describe())

# Check column names
print("\nColumn Names:")
print(df.columns)

# Check unique values for categorical columns
print("\nUnique Values Per Column:")
for col in df.select_dtypes(include=['object']).columns:
    print(f"{col}: {df[col].nunique()} unique values")




