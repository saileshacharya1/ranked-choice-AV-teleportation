# ---------------------------------------------------------------------------------------------------------------------#
# Author: Sailesh Acharya
# Data: 2023-03-09
# Project name: Ranked choice analysis between human-driven vehicles (hv),
# autonomous vehicles (av), and teleportation (tp).

# This script prepares the data for choice analysis using Biogeme. The data is
# collected from a survey of US national park visitors.
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# import modules
import pandas as pd
import numpy as np
import semopy

# import data
df = pd.read_csv("../data/raw/data.csv")
df.describe
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
## latent variables definition and score estimate

# model specification
mod = """
av_usefulness     =~ av_benefit_1 + av_benefit_2 + av_benefit_3 + \
                     av_benefit_4 + av_benefit_5 + av_benefit_6 + \
                     av_concern_1 + av_concern_4 + av_concern_5
av_concern        =~ av_concern_2 + av_concern_3 + av_concern_6 + \
                     av_concern_7
tech_savviness    =~ tech_savvy_1  + tech_savvy_3
driving_enjoyment =~ enjoy_driving_1 + enjoy_driving_3 + enjoy_driving_4
polychronicity    =~ polychronicity_1 + polychronicity_2 + polychronicity_3
envt_concern      =~ envt_concern_1 + envt_concern_2 + envt_concern_3
"""
# model fit
model = semopy.Model(mod)
model.fit(df, obj="MLW")
pd.set_option("display.max_rows", 500)
model.inspect()
stats = semopy.calc_stats(model)
print(stats.T)

# estimate factor scores
factors = model.predict_factors(df)
df = df.join(factors)

# add several columns of low, medium, and high latent factors' scores
df["av_usefulness_cat"] = pd.qcut(
    df["av_usefulness"], [0, 0.333, 0.666, 1], labels=["low", "med", "high"]
)
df["av_concern_cat"] = pd.qcut(
    df["av_concern"], [0, 0.333, 0.666, 1], labels=["low", "med", "high"]
)
df["tech_savviness_cat"] = pd.qcut(
    df["tech_savviness"], [0, 0.333, 0.666, 1], labels=["low", "med", "high"]
)
df["driving_enjoyment_cat"] = pd.qcut(
    df["driving_enjoyment"], [0, 0.333, 0.666, 1], labels=["low", "med", "high"]
)
df["polychronicity_cat"] = pd.qcut(
    df["polychronicity"], [0, 0.333, 0.666, 1], labels=["low", "med", "high"]
)
df["envt_concern_cat"] = pd.qcut(
    df["envt_concern"], [0, 0.333, 0.666, 1], labels=["low", "med", "high"]
)
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
## calculate tba and tu scores for hv and av

# grouped hv-tba scores
df["tba_g1_hv"] = df["tba_hv_7"]
df["tba_g2_hv"] = df["tba_hv_5"] + df["tba_hv_6"] + df["tba_hv_10"]
df["tba_g3_hv"] = df["tba_hv_3"] + df["tba_hv_4"]
df["tba_g4_hv"] = df["tba_hv_2"] + df["tba_hv_8"] + df["tba_hv_9"]
df["tba_g5_hv"] = df["tba_hv_11"] + df["tba_hv_12"]
df["tba_g6_hv"] = df["tba_hv_13"] + df["tba_hv_14"] + df["tba_hv_15"]
df["tba_g7_hv"] = df["tba_hv_16"]
df["tba_tot_hv"] = (
    df["tba_hv_1"]
    + df["tba_hv_2"]
    + df["tba_hv_3"]
    + df["tba_hv_4"]
    + df["tba_hv_5"]
    + df["tba_hv_6"]
    + df["tba_hv_7"]
    + df["tba_hv_8"]
    + df["tba_hv_9"]
    + df["tba_hv_10"]
    + df["tba_hv_11"]
    + df["tba_hv_12"]
    + df["tba_hv_13"]
    + df["tba_hv_14"]
    + df["tba_hv_15"]
    + df["tba_hv_16"]
    + df["tba_hv_17"]
)

df["tba_g1_hv_d"] = np.where(df.tba_g1_hv > 0, 1, 0)
df["tba_g2_hv_d"] = np.where(df.tba_g2_hv > 0, 1, 0)
df["tba_g3_hv_d"] = np.where(df.tba_g3_hv > 0, 1, 0)
df["tba_g4_hv_d"] = np.where(df.tba_g4_hv > 0, 1, 0)
df["tba_g5_hv_d"] = np.where(df.tba_g5_hv > 0, 1, 0)
df["tba_g6_hv_d"] = np.where(df.tba_g6_hv > 0, 1, 0)
df["tba_g7_hv_d"] = np.where(df.tba_g7_hv > 0, 1, 0)

# grouped av-tba scores
df["tba_g1_av"] = df["tba_av_7"]
df["tba_g2_av"] = df["tba_av_5"] + df["tba_av_6"] + df["tba_av_10"]
df["tba_g3_av"] = df["tba_av_3"] + df["tba_av_4"]
df["tba_g4_av"] = df["tba_av_2"] + df["tba_av_8"] + df["tba_av_9"]
df["tba_g5_av"] = df["tba_av_11"] + df["tba_av_12"]
df["tba_g6_av"] = df["tba_av_13"] + df["tba_av_14"] + df["tba_av_15"]
df["tba_g7_av"] = df["tba_av_16"]
df["tba_tot_av"] = (
    df["tba_av_1"]
    + df["tba_av_2"]
    + df["tba_av_3"]
    + df["tba_av_4"]
    + df["tba_av_5"]
    + df["tba_av_6"]
    + df["tba_av_7"]
    + df["tba_av_8"]
    + df["tba_av_9"]
    + df["tba_av_10"]
    + df["tba_av_11"]
    + df["tba_av_12"]
    + df["tba_av_13"]
    + df["tba_av_14"]
    + df["tba_av_15"]
    + df["tba_av_16"]
    + df["tba_av_17"]
)
df["tba_g1_av_d"] = np.where(df.tba_g1_av > 0, 1, 0)
df["tba_g2_av_d"] = np.where(df.tba_g2_av > 0, 1, 0)
df["tba_g3_av_d"] = np.where(df.tba_g3_av > 0, 1, 0)
df["tba_g4_av_d"] = np.where(df.tba_g4_av > 0, 1, 0)
df["tba_g5_av_d"] = np.where(df.tba_g5_av > 0, 1, 0)
df["tba_g6_av_d"] = np.where(df.tba_g6_av > 0, 1, 0)
df["tba_g7_av_d"] = np.where(df.tba_g7_av > 0, 1, 0)

# difference in av-tba and hv-tba scores
for i in range(1, 8):
    df[f"tba_g{i}_diff"] = df[f"tba_g{i}_av"] - df[f"tba_g{i}_hv"]
del i
df["tba_tot_diff"] = df["tba_tot_av"] - df["tba_tot_hv"]

# difference in travel usefulness between AV and HV
df["tu_diff"] = df["tu_av"] - df["tu_hv"]

# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
## data preparation for choice models

# first ranked mode
conditions = [df["rank_hv"] == 1, df["rank_av"] == 1, df["rank_teleport"] == 1]
outputs = [1, 2, 3]
df["first_choice"] = np.select(conditions, outputs)

# second ranked mode
conditions = [df["rank_hv"] == 2, df["rank_av"] == 2, df["rank_teleport"] == 2]
outputs = [1, 2, 3]
df["second_choice"] = np.select(conditions, outputs)

# convert wide to long format
value_vars = list(df.filter(like="rank_").columns)
id_vars = list(df.columns.drop(value_vars))
df = pd.melt(
    df, id_vars=id_vars, value_vars=value_vars, var_name="chosen", value_name="rank"
)

# recode chosen modes to hv -1, av-2, and tp-3
df.chosen = df.chosen.map({"rank_hv": 1, "rank_av": 2, "rank_teleport": 3})

# keep observations with rank 1 and 2 only
df = df[df["rank"] <= 2]

# availabilities of hv, av, and tp
df["hv_avail"] = np.where((df["first_choice"] == 1) & (df["rank"] == 2), 0, 1)
df["av_avail"] = np.where((df["first_choice"] == 2) & (df["rank"] == 2), 0, 1)
df["tp_avail"] = np.where((df["first_choice"] == 3) & (df["rank"] == 2), 0, 1)

# dummy coding of some columns having categorical options

df = pd.get_dummies(
    data=df,
    columns=[
        "age_grp",
        "gender",
        "education",
        "school",
        "income_grp",
        "employment",
        "citation",
        "crash_exp",
        "mode_commute",
        "mode_shopping",
        "mode_personal",
        "mode_social",
        "veh_own",
        "per_drive",
        "av_usefulness_cat",
        "av_concern_cat",
        "tech_savviness_cat",
        "driving_enjoyment_cat",
        "polychronicity_cat",
        "envt_concern_cat",
    ],
)

# pepare data for biogeme with no null values and sorted by id
df = df.drop(df.columns[df.isnull().any()], axis=1)
df = df.select_dtypes(exclude=["object"])
df = df.sort_values("id")

# difference in travel usefulness between HV and AV
df["tu_diff"] = df["tu_av"] - df["tu_hv"]

# export the prepared dataset
df.to_pickle("../data/processed/prepared_data.pkl")
# ---------------------------------------------------------------------------------------------------------------------#
