import repackage
repackage.up()

import json
from libs.get_files import get_file_to_df
from libs.treat_files import init_new_df, complete_new_df
import pandas as pd
from functools import reduce


year = 17 # Choose the year you retrieve the data from (2017 --> 17)

# Define columns for every field your are retrieving (if only the year changes you won't need to modify this section)
df_co_col = [f"C{year}_FAM", f"C{year}_COUPAENF", f"C{year}_FAMMONO", f"C{year}_COUPSENF"],
df_ef_col = f"C{year}_FAM", [f"C{year}_NE24F0", f"C{year}_NE24F1", f"C{year}_NE24F2", f"C{year}_NE24F3", f"C{year}_NE24F4P"],
df_cs_col = [f"C{year}_ACT1564", f"C{year}_ACT1564_CS1", f"C{year}_ACT1564_CS2", f"C{year}_ACT1564_CS3", f"C{year}_ACT1564_CS4", f"C{year}_ACT1564_CS5", f"C{year}_ACT1564_CS6"],
df_tr_col = [f"C{year}_ACTOCC15P", f"C{year}_ACTOCC15P_PAS", f"C{year}_ACTOCC15P_MAR", f"C{year}_ACTOCC15P_2ROUESMOT", f"C{year}_ACTOCC15P_VOIT", f"C{year}_ACTOCC15P_TCOM"],
df_di_col = [f"P{year}_NSCOL15P", f"P{year}_NSCOL15P_DIPLMIN", f"P{year}_NSCOL15P_CAPBEP", f"P{year}_NSCOL15P_BAC", f"P{year}_NSCOL15P_SUP2"],
df_lo_col = [f"P{year}_LOG", f"P{year}_MAISON", f"P{year}_APPART"],
df_pi_col = [f"P{year}_RP", f"P{year}_RP_1P", f"P{year}_RP_2P", f"P{year}_RP_3P", f"P{year}_RP_4P", f"P{year}_RP_5PP"],
df_oc_col = [f"P{year}_RP", f"P{year}_RP_PROP", f"P{year}_RP_LOC", f"P{year}_RP_LOCHLMV", f"P{year}_RP_GRAT"],
df_vo_col = [f"P{year}_MEN", f"P{year}_RP_VOIT1P", f"P{year}_RP_VOIT1", f"P{year}_RP_VOIT2P"]

with open("config.json") as config_file:
    data = json.load(config_file) # Get all urls
  
# Retrieve data from the website
df_b_co = get_file_to_df(data["df_b_co"])
df_b_ef = get_file_to_df(data["df_b_ef"])
df_b_cs = get_file_to_df(data["df_b_cs"])
df_b_tr = get_file_to_df(data["df_b_tr"])
df_b_di = get_file_to_df(data["df_b_di"])
df_b_lo = get_file_to_df(data["df_b_lo"])
df_b_pi = get_file_to_df(data["df_b_pi"])
df_b_oc = get_file_to_df(data["df_b_oc"])
df_b_vo = get_file_to_df(data["df_b_vo"])

# Init all DataFrames
df_co = init_new_df(df_b_co, df_co_col)
df_ef = init_new_df(df_b_ef, df_ef_col)
df_cs = init_new_df(df_b_cs, df_cs_col)
df_tr = init_new_df(df_b_tr, df_tr_col)
df_di = init_new_df(df_b_di, df_di_col)
df_lo = init_new_df(df_b_lo, df_lo_col)
df_pi = init_new_df(df_b_pi, df_pi_col)
df_oc = init_new_df(df_b_oc, df_oc_col)
df_vo = init_new_df(df_b_vo, df_vo_col)

# Complete all DataFrames
df_co_complete = complete_new_df(df_co, 3, "fr_co#")
df_ef_complete = complete_new_df(df_ef, 5, "fr_ef#")
df_cs_complete = complete_new_df(df_cs, 6, "fr_cs#", start=1) # start = 1 because CS0 doesn't exist
df_tr_complete = complete_new_df(df_tr, 5, "fr_tr#")
df_di_complete = complete_new_df(df_di, 4, "fr_di#")
df_lo_complete = complete_new_df(df_lo, 2, "fr_lo#")
df_pi_complete = complete_new_df(df_pi, 5, "fr_pi#")
df_oc_complete = complete_new_df(df_oc, 4, "fr_oc#")
df_vo_complete = complete_new_df(df_vo, 3, "fr_vo#")

# Merge all DataFrames together to get the final one
dfs = [df_co_complete, df_ef_complete, df_cs_complete, df_tr_complete, df_di_complete, df_lo_complete, df_pi_complete, df_oc_complete, df_vo_complete]
df_merged = reduce(lambda  left, right: pd.merge(left, right, on=["COD_IRIS"], how="left"), dfs)

compression_opts = dict(method="zip", archive_name="IRIS_DATA_20%s.csv" % year)  
df_merged.to_csv("IRIS_DATA_20%s.zip" % year, index=False, compression=compression_opts)  




