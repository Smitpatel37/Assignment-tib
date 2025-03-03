# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 19:03:43 2025

@author: Smit3
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import dtreg

# Load the CSV file
file_path = "covid-aqs-database_2021-03-24_version_1.csv"  # Replace with your actual file path
df = pd.read_csv(file_path, sep=";")

# Display basic information about the dataset
print("\nBasic Info:")
print(df.info())

# print("\nUnique Values Per Column:")
# for col in df.select_dtypes(include=['object']).columns:
#     print(f"{col}: {df[col].nunique()} unique values")

print(df['methods'].unique())

def prepare_data(df):
    """
    Prepares the dataset by selecting relevant columns, filtering based on methods,
    categorizing Stringency Index, and removing insufficient data points.
    
    Parameters:
    df (pd.DataFrame): The input dataset containing air quality and lockdown information.
    
    Returns:
    pd.DataFrame: The processed dataset ready for analysis.
    """
    # Define important columns
    Imp_Columns = ["Country", "StringencyIndex", 'PM25_prcnt_change',
                   'PM25_prcnt_change_er', 'PM25_ugm3_Reference_avg',
                   'PM25_ugm3_Reference_sd', 'PM25_ugm3_Lockdown_avg',
                   'PM25_ugm3_Lockdown_sd']
    
    # Filter data based on methods
    Acc_For_Meteorology = df[
        (df['methods'] == 'Accounting for Effects of Meteorology, Atmospheric Chemistry, and Long-term Trends') |
        (df['methods'] == 'Air Quality Modeling and Emission Inventories Constrained by Observed Changes')
    ][Imp_Columns].copy()

    # Define SI bins and labels
    bins = [20, 40, 60, 80, 100]
    labels = ["20-40", "40-60", "60-80", "80-100"]

    # Categorize Stringency Index
    Acc_For_Meteorology["SI_Category"] = pd.cut(
        Acc_For_Meteorology["StringencyIndex"], bins=bins, labels=labels, include_lowest=True
    )

    # Drop rows with NaN values in PM2.5 percentage change
    Acc_For_Meteorology.dropna(subset=["PM25_prcnt_change"], inplace=True)

    # Drop SI categories with fewer than 19 occurrences
    Acc_For_Meteorology = Acc_For_Meteorology[
        Acc_For_Meteorology["SI_Category"].astype(str).map(Acc_For_Meteorology["SI_Category"].value_counts()) >= 19
    ]

    return Acc_For_Meteorology

Acc_For_Meteorology = prepare_data(df)
# Print category counts
print(Acc_For_Meteorology["SI_Category"].value_counts())

# Set figure size
plt.figure(figsize=(10, 6))

# Create boxplot
sns.boxplot(data=Acc_For_Meteorology, whis=[10, 90], x="SI_Category", y="PM25_prcnt_change", showfliers=False, palette="Set2")

# Customize plot
plt.xlabel("Stringency Index (%)")
plt.ylabel("PM2.5 Percent Change")
plt.title("Boxplot of PM2.5 Change by Stringency Index considering Meteorological Effects")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show plot
plt.show()
    
#plot_pm25(Direct_Comparison)
# plot_pm25(Acc_For_Meteorology)
