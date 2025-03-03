# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 18:56:10 2025

@author: Smit3
"""

from dtreg.load_datatype import load_datatype
from dtreg.to_jsonld import to_jsonld
import pandas as pd
from Results import prepare_data

file_path = "covid-aqs-database_2021-03-24_version_1.csv"  # Replace with your actual file path
df = pd.read_csv(file_path, sep=";")

Acc_For_Meteorology = prepare_data(df)

stats = Acc_For_Meteorology.groupby("SI_Category")["PM25_prcnt_change"].describe(percentiles=[0.1, 0.9])


dt1 = load_datatype("https://doi.org/21.T11969/feeb33ad3e4440682a4d") # Data analysis
dt2 = load_datatype("https://doi.org/21.T11969/5b66cb584b974b186f37") # Descriptive Statistics

instance = dt1.data_analysis(
    is_implemented_by="Results.py",
    has_part=dt2.descriptive_statistics(
        label="Descriptive statistics for PM2.5 percent change across SI categories accounting Meteorogical effects",
        targets=dt2.component(label="PM25_prcnt_change"),
        has_input=dt2.data_item(
            label="Filtered dataset for PM2.5 analysis",
            source_table=Acc_For_Meteorology[["SI_Category", "PM25_prcnt_change"]],
        ),
        has_output=dt2.data_item(
            source_table=stats,
            has_part=[
                dt2.component(label="count"),
                dt2.component(label="mean"),
                dt2.component(label="std"),
                dt2.component(label="min"),
                dt2.component(label="10%"),   
                dt2.component(label="25%"),
                dt2.component(label="50%"),
                dt2.component(label="75%"),
                dt2.component(label="90%"),
                dt2.component(label="max")
            ]
        )
    )
)

with open("data-analysis-1.json", "w") as f:
    f.write(to_jsonld(instance))