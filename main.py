import repackage
repackage.up()

import json
from libs.get_files import get_file_to_df
from libs.treat_files import init_new_df, complete_new_df
import pandas as pd
from functools import reduce


year = 17 # Choose the year you retrieve the data from (2017 --> 17)

with open("config.json") as config_file:
    data = json.load(config_file) # Get all urls

# Create dicts {"suffix": [number of cols you want, should the last col be the result of (first col) - (sum of others)]} 
suffixes = {
    "co": [3, False],
    "ef": [5, False],
    "cs": [7, True],
    "tr": [5, False],
    "di": [4, False],
    "lo": [2, False],
    "pi": [5, False],
    "oc": [4, False],
    "vo": [3, False]
}

# Define columns for every field your are retrieving (if only the year changes you won't need to modify this section)
dict_df_cols = {
    "co": [f"C{year}_FAM", f"C{year}_COUPAENF", f"C{year}_FAMMONO", f"C{year}_COUPSENF"],
    "ef": [f"C{year}_FAM", f"C{year}_NE24F0", f"C{year}_NE24F1", f"C{year}_NE24F2", f"C{year}_NE24F3", f"C{year}_NE24F4P"],
    "cs": [f"C{year}_ACT1564", f"C{year}_ACT1564_CS1", f"C{year}_ACT1564_CS2", f"C{year}_ACT1564_CS3", f"C{year}_ACT1564_CS4", f"C{year}_ACT1564_CS5", f"C{year}_ACT1564_CS6"],
    "tr": [f"C{year}_ACTOCC15P", f"C{year}_ACTOCC15P_PAS", f"C{year}_ACTOCC15P_MAR", f"C{year}_ACTOCC15P_2ROUESMOT", f"C{year}_ACTOCC15P_VOIT", f"C{year}_ACTOCC15P_TCOM"],
    "di": [f"P{year}_NSCOL15P", f"P{year}_NSCOL15P_DIPLMIN", f"P{year}_NSCOL15P_CAPBEP", f"P{year}_NSCOL15P_BAC", f"P{year}_NSCOL15P_SUP2"],
    "lo": [f"P{year}_LOG", f"P{year}_MAISON", f"P{year}_APPART"],
    "pi": [f"P{year}_RP", f"P{year}_RP_1P", f"P{year}_RP_2P", f"P{year}_RP_3P", f"P{year}_RP_4P", f"P{year}_RP_5PP"],
    "oc": [f"P{year}_RP", f"P{year}_RP_PROP", f"P{year}_RP_LOC", f"P{year}_RP_LOCHLMV", f"P{year}_RP_GRAT"],
    "vo": [f"P{year}_MEN", f"P{year}_RP_VOIT1P", f"P{year}_RP_VOIT1", f"P{year}_RP_VOIT2P"]
}
  
# Retrieve data from the website
dict_df_b = {suffix: get_file_to_df(data[f"df_b_{suffix}"]) for suffix in suffixes}

# Init all DataFrames
dict_df = {suffix: init_new_df(dict_df_b[suffix], dict_df_cols[suffix]) for suffix in suffixes}

# Complete all DataFrames
dict_df_complete = {suffix: complete_new_df(dict_df[suffix], suffixes[suffix][0], f"fr_{suffix}#", last_is_total_minus_sum=suffixes[suffix][1]) for suffix in suffixes}

# Merge all DataFrames together to get the final one
dfs = list(dict_df_complete.values())
    
df_merged = reduce(lambda left, right: pd.merge(left, right, on=["COD_IRIS"], how="left"), dfs)

# Export to csv
compression_opts = dict(method="zip", archive_name="IRIS_DATA_20%s.csv" % year)  
df_merged.to_csv("IRIS_DATA_20%s.zip" % year, index=False, compression=compression_opts, decimal=",")  
