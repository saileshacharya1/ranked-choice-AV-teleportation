# ---------------------------------------------------------------------------------------------------------------------#

# import modules
import pandas as pd
import shutil
import os

# import biogeme modules
import biogeme
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models

import biogeme.messaging as msg
from biogeme import vns
from biogeme import assisted
from biogeme.expressions import (
    Beta,
    log,
    Elem,
    Numeric,
    Variable,
    PanelLikelihoodTrajectory,
    MonteCarlo,
    bioDraws,
)

from biogeme.assisted import (
    DiscreteSegmentationTuple,
    TermTuple,
    SegmentedParameterTuple,
)


# ---------------------------------------------------------------------------------------------------------------------#
# import prepared data
df = pd.read_pickle("../data/processed/prepared_data.pkl")
df.describe

# define the data as biogeme global database
database = db.Database("mydata", df)

# define the variables - mode availabililty and choice
hv_avail = Variable("hv_avail")
av_avail = Variable("av_avail")
tp_avail = Variable("tp_avail")
chosen = Variable("chosen")

# define the variables - sociodemographics
age_grp_2 = Variable("age_grp_2")
age_grp_3 = Variable("age_grp_3")
gender_1 = Variable("gender_1")
education_2 = Variable("education_2")
education_3 = Variable("education_3")
school_2 = Variable("school_2")
school_3 = Variable("school_3")
employment_2 = Variable("employment_2")
employment_3 = Variable("employment_3")
race_1 = Variable("race_1")
hh_adult = Variable("hh_adult")
hh_child = Variable("hh_child")
income_grp_2 = Variable("income_grp_2")
income_grp_3 = Variable("income_grp_3")
income_grp_4 = Variable("income_grp_4")
income_grp_5 = Variable("income_grp_5")
driving_exp = Variable("driving_exp")
hh_vehs = Variable("hh_vehs")
mode_commute_3 = Variable("mode_commute_3")
mode_shopping_3 = Variable("mode_shopping_3")
mode_personal_3 = Variable("mode_personal_3")
mode_social_3 = Variable("mode_social_3")
citation_1 = Variable("citation_1")
crash_exp_1 = Variable("crash_exp_1")
rec_trips = Variable("rec_trips")
av_fam = Variable("av_fam")

# define the variables - trip characterstics
time = Variable("time")
cost = Variable("cost")
veh_own_1 = Variable("veh_own_1")
veh_type_1 = Variable("veh_type_1")
veh_type_2 = Variable("veh_type_2")
veh_type_3 = Variable("veh_type_3")
veh_feature_1 = Variable("veh_feature_1")
veh_feature_2 = Variable("veh_feature_2")
veh_feature_3 = Variable("veh_feature_3")
veh_feature_4 = Variable("veh_feature_4")
veh_feature_5 = Variable("veh_feature_5")
veh_feature_6 = Variable("veh_feature_6")
veh_feature_7 = Variable("veh_feature_7")
companion_tot = Variable("companion_tot")
companion_1 = Variable("companion_1")
companion_2 = Variable("companion_2")
companion_3 = Variable("companion_3")
companion_4 = Variable("companion_4")
companion_5 = Variable("companion_5")
per_drive_3 = Variable("per_drive_3")
per_drive_4 = Variable("per_drive_4")
per_drive_5 = Variable("per_drive_5")
trip_exp_1 = Variable("trip_exp_1")
trip_exp_3 = Variable("trip_exp_3")
trip_exp_4 = Variable("trip_exp_4")

# define the variables - TBA and TU
tba_hv_1 = Variable("tba_hv_1")
tba_hv_2 = Variable("tba_hv_2")
tba_hv_3 = Variable("tba_hv_3")
tba_hv_4 = Variable("tba_hv_4")
tba_hv_5 = Variable("tba_hv_5")
tba_hv_6 = Variable("tba_hv_6")
tba_hv_7 = Variable("tba_hv_7")
tba_hv_8 = Variable("tba_hv_8")
tba_hv_9 = Variable("tba_hv_9")
tba_hv_10 = Variable("tba_hv_10")
tba_hv_11 = Variable("tba_hv_11")
tba_hv_12 = Variable("tba_hv_12")
tba_hv_13 = Variable("tba_hv_13")
tba_hv_14 = Variable("tba_hv_14")
tba_hv_15 = Variable("tba_hv_15")
tba_hv_16 = Variable("tba_hv_16")
tba_hv_17 = Variable("tba_hv_17")
tba_av_1 = Variable("tba_av_1")
tba_av_2 = Variable("tba_av_2")
tba_av_3 = Variable("tba_av_3")
tba_av_4 = Variable("tba_av_4")
tba_av_5 = Variable("tba_av_5")
tba_av_6 = Variable("tba_av_6")
tba_av_7 = Variable("tba_av_7")
tba_av_8 = Variable("tba_av_8")
tba_av_9 = Variable("tba_av_9")
tba_av_10 = Variable("tba_av_10")
tba_av_11 = Variable("tba_av_11")
tba_av_12 = Variable("tba_av_12")
tba_av_13 = Variable("tba_av_13")
tba_av_14 = Variable("tba_av_14")
tba_av_15 = Variable("tba_av_15")
tba_av_16 = Variable("tba_av_16")
tba_av_17 = Variable("tba_av_17")

tba_g1_hv = Variable("tba_g1_hv")
tba_g2_hv = Variable("tba_g2_hv")
tba_g3_hv = Variable("tba_g3_hv")
tba_g4_hv = Variable("tba_g4_hv")
tba_g5_hv = Variable("tba_g5_hv")
tba_g6_hv = Variable("tba_g6_hv")
tba_g7_hv = Variable("tba_g7_hv")

tba_g1_av = Variable("tba_g1_av")
tba_g2_av = Variable("tba_g2_av")
tba_g3_av = Variable("tba_g3_av")
tba_g4_av = Variable("tba_g4_av")
tba_g5_av = Variable("tba_g5_av")
tba_g6_av = Variable("tba_g6_av")
tba_g7_av = Variable("tba_g7_av")

tba_g1_hv_d = Variable("tba_g1_hv_d")
tba_g2_hv_d = Variable("tba_g2_hv_d")
tba_g3_hv_d = Variable("tba_g3_hv_d")
tba_g4_hv_d = Variable("tba_g4_hv_d")
tba_g5_hv_d = Variable("tba_g5_hv_d")
tba_g6_hv_d = Variable("tba_g6_hv_d")
tba_g7_hv_d = Variable("tba_g7_hv_d")

tba_g1_av_d = Variable("tba_g1_av_d")
tba_g2_av_d = Variable("tba_g2_av_d")
tba_g3_av_d = Variable("tba_g3_av_d")
tba_g4_av_d = Variable("tba_g4_av_d")
tba_g5_av_d = Variable("tba_g5_av_d")
tba_g6_av_d = Variable("tba_g6_av_d")
tba_g7_av_d = Variable("tba_g7_av_d")


tu_hv = Variable("tu_hv")
tu_av = Variable("tu_av")
tu_diff = Variable("tu_diff")

tba_tot_hv = Variable("tba_tot_hv")
tba_tot_av = Variable("tba_tot_av")

# define the variables - latent variables
av_usefulness = Variable("av_usefulness")
av_concern = Variable("av_concern")
tech_savviness = Variable("tech_savviness")
driving_enjoyment = Variable("driving_enjoyment")
polychronicity = Variable("polychronicity")
envt_concern = Variable("envt_concern")

# ---------------------------------------------------------------------------------------------------------------------#
## mnl
# dichotomous grouped tba-hv and tba-av in utilities of all alternatives
# continuous tu-hv and tu-av in utilities of all alternatives

# parameters to be estimated - alternative specific constants
asc_av = Beta("asc_av", 0, None, None, 0)
asc_tp = Beta("asc_tp", 0, None, None, 0)

# parameters to be estimated - sociodemographics
b_age_grp_2_av = Beta("b_age_grp_2_av", 0, None, None, 0)
b_age_grp_3_av = Beta("b_age_grp_3_av", 0, None, None, 0)
b_gender_1_av = Beta("b_gender_1_av", 0, None, None, 0)
b_education_2_av = Beta("b_education_2_av", 0, None, None, 0)
b_education_3_av = Beta("b_education_3_av", 0, None, None, 0)
b_employment_2_av = Beta("b_employmentl_2_av", 0, None, None, 0)
b_employment_3_av = Beta("b_employment_3_av", 0, None, None, 0)
b_race_1_av = Beta("b_race_1_av", 0, None, None, 0)
b_hh_adult_av = Beta("b_hh_adult_av", 0, None, None, 0)
b_hh_child_av = Beta("b_hh_child_av", 0, None, None, 0)
b_income_grp_2_av = Beta("b_income_grp_2_av", 0, None, None, 0)
b_income_grp_3_av = Beta("b_income_grp_3_av", 0, None, None, 0)
b_income_grp_4_av = Beta("b_income_grp_4_av", 0, None, None, 0)
b_income_grp_5_av = Beta("b_income_grp_5_av", 0, None, None, 0)
b_driving_exp_av = Beta("b_driving_exp_av", 0, None, None, 0)
b_hh_vehs_av = Beta("b_hh_vehs_av", 0, None, None, 0)
b_mode_commute_3_av = Beta("b_mode_commute_3_av", 0, None, None, 0)
b_mode_shopping_3_av = Beta("b_mode_shopping_3_av", 0, None, None, 0)
b_mode_personal_3_av = Beta("b_mode_personal_3_av", 0, None, None, 0)
b_mode_social_3_av = Beta("b_mode_social_3_av", 0, None, None, 0)
b_citation_1_av = Beta("b_citation_1_av", 0, None, None, 0)
b_crash_exp_1_av = Beta("b_crash_exp_1_av", 0, None, None, 0)
b_rec_trips_av = Beta("b_rec_trips_av", 0, None, None, 0)
b_av_fam_av = Beta("b_av_fam_av", 0, None, None, 0)

b_age_grp_2_tp = Beta("b_age_grp_2_tp", 0, None, None, 0)
b_age_grp_3_tp = Beta("b_age_grp_3_tp", 0, None, None, 0)
b_gender_1_tp = Beta("b_gender_1_tp", 0, None, None, 0)
b_education_2_tp = Beta("b_education_2_tp", 0, None, None, 0)
b_education_3_tp = Beta("b_education_3_tp", 0, None, None, 0)
b_employment_2_tp = Beta("b_employmentl_2_tp", 0, None, None, 0)
b_employment_3_tp = Beta("b_employment_3_tp", 0, None, None, 0)
b_race_1_tp = Beta("b_race_1_tp", 0, None, None, 0)
b_hh_adult_tp = Beta("b_hh_adult_tp", 0, None, None, 0)
b_hh_child_tp = Beta("b_hh_child_tp", 0, None, None, 0)
b_income_grp_2_tp = Beta("b_income_grp_2_tp", 0, None, None, 0)
b_income_grp_3_tp = Beta("b_income_grp_3_tp", 0, None, None, 0)
b_income_grp_4_tp = Beta("b_income_grp_4_tp", 0, None, None, 0)
b_income_grp_5_tp = Beta("b_income_grp_5_tp", 0, None, None, 0)
b_driving_exp_tp = Beta("b_driving_exp_tp", 0, None, None, 0)
b_hh_vehs_tp = Beta("b_hh_vehs_tp", 0, None, None, 0)
b_mode_commute_3_tp = Beta("b_mode_commute_3_tp", 0, None, None, 0)
b_mode_shopping_3_tp = Beta("b_mode_shopping_3_tp", 0, None, None, 0)
b_mode_personal_3_tp = Beta("b_mode_personal_3_tp", 0, None, None, 0)
b_mode_social_3_tp = Beta("b_mode_social_3_tp", 0, None, None, 0)
b_citation_1_tp = Beta("b_citation_1_tp", 0, None, None, 0)
b_crash_exp_1_tp = Beta("b_crash_exp_1_tp", 0, None, None, 0)
b_rec_trips_tp = Beta("b_rec_trips_tp", 0, None, None, 0)
b_av_fam_tp = Beta("b_av_fam_tp", 0, None, None, 0)

# parameters to be estimated - trip characterstics
b_time_av = Beta("b_time_av", 0, None, None, 0)
b_cost_av = Beta("b_cost_av", 0, None, None, 0)
b_veh_own_1_av = Beta("b_veh_own_1_av", 0, None, None, 0)
b_veh_type_1_av = Beta("b_veh_type_1_av", 0, None, None, 0)
b_veh_type_2_av = Beta("b_veh_type_2_av", 0, None, None, 0)
b_veh_type_3_av = Beta("b_veh_type_3_av", 0, None, None, 0)
b_veh_feature_1_av = Beta("b_veh_feature_1_av", 0, None, None, 0)
b_veh_feature_2_av = Beta("b_veh_feature_2_av", 0, None, None, 0)
b_veh_feature_3_av = Beta("b_veh_feature_3_av", 0, None, None, 0)
b_veh_feature_4_av = Beta("b_veh_feature_4_av", 0, None, None, 0)
b_veh_feature_5_av = Beta("b_veh_feature_5_av", 0, None, None, 0)
b_veh_feature_6_av = Beta("b_veh_feature_6_av", 0, None, None, 0)
b_veh_feature_7_av = Beta("b_veh_feature_7_av", 0, None, None, 0)
b_companion_tot_av = Beta("b_companion_tot_av", 0, None, None, 0)
b_companion_1_av = Beta("b_companion_1_av", 0, None, None, 0)
b_companion_2_av = Beta("b_companion_2_av", 0, None, None, 0)
b_companion_3_av = Beta("b_companion_3_av", 0, None, None, 0)
b_companion_4_av = Beta("b_companion_4_av", 0, None, None, 0)
b_companion_5_av = Beta("b_companion_5_av", 0, None, None, 0)
b_per_drive_3_av = Beta("b_per_drive_3_av", 0, None, None, 0)
b_per_drive_4_av = Beta("b_per_drive_4_av", 0, None, None, 0)
b_per_drive_5_av = Beta("b_per_drive_5_av", 0, None, None, 0)
b_trip_exp_1_av = Beta("b_trip_exp_1_av", 0, None, None, 0)
b_trip_exp_3_av = Beta("b_trip_exp_3_av", 0, None, None, 0)
b_trip_exp_4_av = Beta("b_trip_exp_4_av", 0, None, None, 0)

b_time_tp = Beta("b_time_tp", 0, None, None, 0)
b_cost_tp = Beta("b_cost_tp", 0, None, None, 0)
b_veh_own_1_tp = Beta("b_veh_own_1_tp", 0, None, None, 0)
b_veh_type_1_tp = Beta("b_veh_type_1_tp", 0, None, None, 0)
b_veh_type_2_tp = Beta("b_veh_type_2_tp", 0, None, None, 0)
b_veh_type_3_tp = Beta("b_veh_type_3_tp", 0, None, None, 0)
b_veh_feature_1_tp = Beta("b_veh_feature_1_tp", 0, None, None, 0)
b_veh_feature_2_tp = Beta("b_veh_feature_2_tp", 0, None, None, 0)
b_veh_feature_3_tp = Beta("b_veh_feature_3_tp", 0, None, None, 0)
b_veh_feature_4_tp = Beta("b_veh_feature_4_tp", 0, None, None, 0)
b_veh_feature_5_tp = Beta("b_veh_feature_5_tp", 0, None, None, 0)
b_veh_feature_6_tp = Beta("b_veh_feature_6_tp", 0, None, None, 0)
b_veh_feature_7_tp = Beta("b_veh_feature_7_tp", 0, None, None, 0)
b_companion_tot_tp = Beta("b_companion_tot_tp", 0, None, None, 0)
b_companion_1_tp = Beta("b_companion_1_tp", 0, None, None, 0)
b_companion_2_tp = Beta("b_companion_2_tp", 0, None, None, 0)
b_companion_3_tp = Beta("b_companion_3_tp", 0, None, None, 0)
b_companion_4_tp = Beta("b_companion_4_tp", 0, None, None, 0)
b_companion_5_tp = Beta("b_companion_5_tp", 0, None, None, 0)
b_per_drive_3_tp = Beta("b_per_drive_3_tp", 0, None, None, 0)
b_per_drive_4_tp = Beta("b_per_drive_4_tp", 0, None, None, 0)
b_per_drive_5_tp = Beta("b_per_drive_5_tp", 0, None, None, 0)
b_trip_exp_1_tp = Beta("b_trip_exp_1_tp", 0, None, None, 0)
b_trip_exp_3_tp = Beta("b_trip_exp_3_tp", 0, None, None, 0)
b_trip_exp_4_tp = Beta("b_trip_exp_4_tp", 0, None, None, 0)

# parameters to be estimated - TBA and TU
b_tba_hv_1_av = Beta("b_tba_hv_1_av", 0, None, None, 0)
b_tba_hv_2_av = Beta("b_tba_hv_2_av", 0, None, None, 0)
b_tba_hv_3_av = Beta("b_tba_hv_3_av", 0, None, None, 0)
b_tba_hv_4_av = Beta("b_tba_hv_4_av", 0, None, None, 0)
b_tba_hv_5_av = Beta("b_tba_hv_5_av", 0, None, None, 0)
b_tba_hv_6_av = Beta("b_tba_hv_6_av", 0, None, None, 0)
b_tba_hv_7_av = Beta("b_tba_hv_7_av", 0, None, None, 0)
b_tba_hv_8_av = Beta("b_tba_hv_8_av", 0, None, None, 0)
b_tba_hv_9_av = Beta("b_tba_hv_9_av", 0, None, None, 0)
b_tba_hv_10_av = Beta("b_tba_hv_10_av", 0, None, None, 0)
b_tba_hv_11_av = Beta("b_tba_hv_11_av", 0, None, None, 0)
b_tba_hv_12_av = Beta("b_tba_hv_12_av", 0, None, None, 0)
b_tba_hv_13_av = Beta("b_tba_hv_13_av", 0, None, None, 0)
b_tba_hv_14_av = Beta("b_tba_hv_14_av", 0, None, None, 0)
b_tba_hv_15_av = Beta("b_tba_hv_15_av", 0, None, None, 0)
b_tba_hv_16_av = Beta("b_tba_hv_16_av", 0, None, None, 0)
b_tba_hv_17_av = Beta("b_tba_hv_17_av", 0, None, None, 0)
b_tba_av_1_av = Beta("b_tba_av_1_av", 0, None, None, 0)
b_tba_av_2_av = Beta("b_tba_av_2_av", 0, None, None, 0)
b_tba_av_3_av = Beta("b_tba_av_3_av", 0, None, None, 0)
b_tba_av_4_av = Beta("b_tba_av_4_av", 0, None, None, 0)
b_tba_av_5_av = Beta("b_tba_av_5_av", 0, None, None, 0)
b_tba_av_6_av = Beta("b_tba_av_6_av", 0, None, None, 0)
b_tba_av_7_av = Beta("b_tba_av_7_av", 0, None, None, 0)
b_tba_av_8_av = Beta("b_tba_av_8_av", 0, None, None, 0)
b_tba_av_9_av = Beta("b_tba_av_9_av", 0, None, None, 0)
b_tba_av_10_av = Beta("b_tba_av_10_av", 0, None, None, 0)
b_tba_av_11_av = Beta("b_tba_av_11_av", 0, None, None, 0)
b_tba_av_12_av = Beta("b_tba_av_12_av", 0, None, None, 0)
b_tba_av_13_av = Beta("b_tba_av_13_av", 0, None, None, 0)
b_tba_av_14_av = Beta("b_tba_av_14_av", 0, None, None, 0)
b_tba_av_15_av = Beta("b_tba_av_15_av", 0, None, None, 0)
b_tba_av_16_av = Beta("b_tba_av_16_av", 0, None, None, 0)
b_tba_av_17_av = Beta("b_tba_av_17_av", 0, None, None, 0)
b_tu_hv_av = Beta("b_tu_hv_av", 0, None, None, 0)
b_tu_av_av = Beta("b_tu_av_av", 0, None, None, 0)
b_tba_tot_hv_av = Beta("b_tba_tot_hv_av", 0, None, None, 0)
b_tba_tot_av_av = Beta("b_tba_tot_av_av", 0, None, None, 0)

b_tba_hv_1_tp = Beta("b_tba_hv_1_tp", 0, None, None, 0)
b_tba_hv_2_tp = Beta("b_tba_hv_2_tp", 0, None, None, 0)
b_tba_hv_3_tp = Beta("b_tba_hv_3_tp", 0, None, None, 0)
b_tba_hv_4_tp = Beta("b_tba_hv_4_tp", 0, None, None, 0)
b_tba_hv_5_tp = Beta("b_tba_hv_5_tp", 0, None, None, 0)
b_tba_hv_6_tp = Beta("b_tba_hv_6_tp", 0, None, None, 0)
b_tba_hv_7_tp = Beta("b_tba_hv_7_tp", 0, None, None, 0)
b_tba_hv_8_tp = Beta("b_tba_hv_8_tp", 0, None, None, 0)
b_tba_hv_9_tp = Beta("b_tba_hv_9_tp", 0, None, None, 0)
b_tba_hv_10_tp = Beta("b_tba_hv_10_tp", 0, None, None, 0)
b_tba_hv_11_tp = Beta("b_tba_hv_11_tp", 0, None, None, 0)
b_tba_hv_12_tp = Beta("b_tba_hv_12_tp", 0, None, None, 0)
b_tba_hv_13_tp = Beta("b_tba_hv_13_tp", 0, None, None, 0)
b_tba_hv_14_tp = Beta("b_tba_hv_14_tp", 0, None, None, 0)
b_tba_hv_15_tp = Beta("b_tba_hv_15_tp", 0, None, None, 0)
b_tba_hv_16_tp = Beta("b_tba_hv_16_tp", 0, None, None, 0)
b_tba_hv_17_tp = Beta("b_tba_hv_17_tp", 0, None, None, 0)
b_tba_av_1_tp = Beta("b_tba_av_1_tp", 0, None, None, 0)
b_tba_av_2_tp = Beta("b_tba_av_2_tp", 0, None, None, 0)
b_tba_av_3_tp = Beta("b_tba_av_3_tp", 0, None, None, 0)
b_tba_av_4_tp = Beta("b_tba_av_4_tp", 0, None, None, 0)
b_tba_av_5_tp = Beta("b_tba_av_5_tp", 0, None, None, 0)
b_tba_av_6_tp = Beta("b_tba_av_6_tp", 0, None, None, 0)
b_tba_av_7_tp = Beta("b_tba_av_7_tp", 0, None, None, 0)
b_tba_av_8_tp = Beta("b_tba_av_8_tp", 0, None, None, 0)
b_tba_av_9_tp = Beta("b_tba_av_9_tp", 0, None, None, 0)
b_tba_av_10_tp = Beta("b_tba_av_10_tp", 0, None, None, 0)
b_tba_av_11_tp = Beta("b_tba_av_11_tp", 0, None, None, 0)
b_tba_av_12_tp = Beta("b_tba_av_12_tp", 0, None, None, 0)
b_tba_av_13_tp = Beta("b_tba_av_13_tp", 0, None, None, 0)
b_tba_av_14_tp = Beta("b_tba_av_14_tp", 0, None, None, 0)
b_tba_av_15_tp = Beta("b_tba_av_15_tp", 0, None, None, 0)
b_tba_av_16_tp = Beta("b_tba_av_16_tp", 0, None, None, 0)
b_tba_av_17_tp = Beta("b_tba_av_17_tp", 0, None, None, 0)

b_tba_g1_hv_av = Beta("b_tba_g1_hv_av", 0, None, None, 0)
b_tba_g2_hv_av = Beta("b_tba_g2_hv_av", 0, None, None, 0)
b_tba_g3_hv_av = Beta("b_tba_g3_hv_av", 0, None, None, 0)
b_tba_g4_hv_av = Beta("b_tba_g4_hv_av", 0, None, None, 0)
b_tba_g5_hv_av = Beta("b_tba_g5_hv_av", 0, None, None, 0)
b_tba_g6_hv_av = Beta("b_tba_g6_hv_av", 0, None, None, 0)
b_tba_g7_hv_av = Beta("b_tba_g7_hv_av", 0, None, None, 0)
b_tba_g1_av_av = Beta("b_tba_g1_av_av", 0, None, None, 0)
b_tba_g2_av_av = Beta("b_tba_g2_av_av", 0, None, None, 0)
b_tba_g3_av_av = Beta("b_tba_g3_av_av", 0, None, None, 0)
b_tba_g4_av_av = Beta("b_tba_g4_av_av", 0, None, None, 0)
b_tba_g5_av_av = Beta("b_tba_g5_av_av", 0, None, None, 0)
b_tba_g6_av_av = Beta("b_tba_g6_av_av", 0, None, None, 0)
b_tba_g7_av_av = Beta("b_tba_g7_av_av", 0, None, None, 0)

b_tba_g1_hv_tp = Beta("b_tba_g1_hv_tp", 0, None, None, 0)
b_tba_g2_hv_tp = Beta("b_tba_g2_hv_tp", 0, None, None, 0)
b_tba_g3_hv_tp = Beta("b_tba_g3_hv_tp", 0, None, None, 0)
b_tba_g4_hv_tp = Beta("b_tba_g4_hv_tp", 0, None, None, 0)
b_tba_g5_hv_tp = Beta("b_tba_g5_hv_tp", 0, None, None, 0)
b_tba_g6_hv_tp = Beta("b_tba_g6_hv_tp", 0, None, None, 0)
b_tba_g7_hv_tp = Beta("b_tba_g7_hv_tp", 0, None, None, 0)
b_tba_g1_av_tp = Beta("b_tba_g1_av_tp", 0, None, None, 0)
b_tba_g2_av_tp = Beta("b_tba_g2_av_tp", 0, None, None, 0)
b_tba_g3_av_tp = Beta("b_tba_g3_av_tp", 0, None, None, 0)
b_tba_g4_av_tp = Beta("b_tba_g4_av_tp", 0, None, None, 0)
b_tba_g5_av_tp = Beta("b_tba_g5_av_tp", 0, None, None, 0)
b_tba_g6_av_tp = Beta("b_tba_g6_av_tp", 0, None, None, 0)
b_tba_g7_av_tp = Beta("b_tba_g7_av_tp", 0, None, None, 0)

b_tba_g1_hv_d_av = Beta("b_tba_g1_hv_d_av", 0, None, None, 0)
b_tba_g2_hv_d_av = Beta("b_tba_g2_hv_d_av", 0, None, None, 0)
b_tba_g3_hv_d_av = Beta("b_tba_g3_hv_d_av", 0, None, None, 0)
b_tba_g4_hv_d_av = Beta("b_tba_g4_hv_d_av", 0, None, None, 0)
b_tba_g5_hv_d_av = Beta("b_tba_g5_hv_d_av", 0, None, None, 0)
b_tba_g6_hv_d_av = Beta("b_tba_g6_hv_d_av", 0, None, None, 0)
b_tba_g7_hv_d_av = Beta("b_tba_g7_hv_d_av", 0, None, None, 0)
b_tba_g1_av_d_av = Beta("b_tba_g1_av_d_av", 0, None, None, 0)
b_tba_g2_av_d_av = Beta("b_tba_g2_av_d_av", 0, None, None, 0)
b_tba_g3_av_d_av = Beta("b_tba_g3_av_d_av", 0, None, None, 0)
b_tba_g4_av_d_av = Beta("b_tba_g4_av_d_av", 0, None, None, 0)
b_tba_g5_av_d_av = Beta("b_tba_g5_av_d_av", 0, None, None, 0)
b_tba_g6_av_d_av = Beta("b_tba_g6_av_d_av", 0, None, None, 0)
b_tba_g7_av_d_av = Beta("b_tba_g7_av_d_av", 0, None, None, 0)

b_tba_g1_hv_d_tp = Beta("b_tba_g1_hv_d_tp", 0, None, None, 0)
b_tba_g2_hv_d_tp = Beta("b_tba_g2_hv_d_tp", 0, None, None, 0)
b_tba_g3_hv_d_tp = Beta("b_tba_g3_hv_d_tp", 0, None, None, 0)
b_tba_g4_hv_d_tp = Beta("b_tba_g4_hv_d_tp", 0, None, None, 0)
b_tba_g5_hv_d_tp = Beta("b_tba_g5_hv_d_tp", 0, None, None, 0)
b_tba_g6_hv_d_tp = Beta("b_tba_g6_hv_d_tp", 0, None, None, 0)
b_tba_g7_hv_d_tp = Beta("b_tba_g7_hv_d_tp", 0, None, None, 0)
b_tba_g1_av_d_tp = Beta("b_tba_g1_av_d_tp", 0, None, None, 0)
b_tba_g2_av_d_tp = Beta("b_tba_g2_av_d_tp", 0, None, None, 0)
b_tba_g3_av_d_tp = Beta("b_tba_g3_av_d_tp", 0, None, None, 0)
b_tba_g4_av_d_tp = Beta("b_tba_g4_av_d_tp", 0, None, None, 0)
b_tba_g5_av_d_tp = Beta("b_tba_g5_av_d_tp", 0, None, None, 0)
b_tba_g6_av_d_tp = Beta("b_tba_g6_av_d_tp", 0, None, None, 0)
b_tba_g7_av_d_tp = Beta("b_tba_g7_av_d_tp", 0, None, None, 0)

b_tu_hv_tp = Beta("b_tu_hv_tp", 0, None, None, 0)
b_tu_av_tp = Beta("b_tu_av_tp", 0, None, None, 0)
b_tba_tot_hv_tp = Beta("b_tba_tot_hv_tp", 0, None, None, 0)
b_tba_tot_av_tp = Beta("b_tba_tot_av_tp", 0, None, None, 0)

# parameters to be estimated - latent variables
b_av_usefulness_av = Beta("b_av_usefulness_av", 0, None, None, 0)
b_av_concern_av = Beta("b_av_concern_av", 0, None, None, 0)
b_tech_savviness_av = Beta("b_tech_savviness_av", 0, None, None, 0)
b_driving_enjoyment_av = Beta("b_driving_enjoyment_av", 0, None, None, 0)
b_polychronicity_av = Beta("b_polychronicity_av", 0, None, None, 0)
b_envt_concern_av = Beta("b_envt_concern_av", 0, None, None, 0)

b_av_usefulness_tp = Beta("b_av_usefulness_tp", 0, None, None, 0)
b_av_concern_tp = Beta("b_av_concern_tp", 0, None, None, 0)
b_tech_savviness_tp = Beta("b_tech_savviness_tp", 0, None, None, 0)
b_driving_enjoyment_tp = Beta("b_driving_enjoyment_tp", 0, None, None, 0)
b_polychronicity_tp = Beta("b_polychronicity_tp", 0, None, None, 0)
b_envt_concern_tp = Beta("b_envt_concern_tp", 0, None, None, 0)


# define utility functions
v1 = 0

v2 = (
    asc_av
    + b_age_grp_2_av * age_grp_2
    + b_age_grp_3_av * age_grp_3
    + b_gender_1_av * gender_1
    + b_education_2_av * education_2
    + b_education_3_av * education_3
    + b_employment_2_av * employment_2
    + b_employment_3_av * employment_3
    + b_race_1_av * race_1
    + b_hh_adult_av * hh_adult
    + b_hh_child_av * hh_child
    + b_income_grp_2_av * income_grp_2
    + b_income_grp_3_av * income_grp_3
    + b_income_grp_4_av * income_grp_4
    + b_income_grp_5_av * income_grp_5
    + b_driving_exp_av * driving_exp
    + b_hh_vehs_av * hh_vehs
    + b_mode_commute_3_av * mode_commute_3
    + b_mode_shopping_3_av * mode_shopping_3
    + b_mode_personal_3_av * mode_personal_3
    + b_mode_social_3_av * mode_social_3
    + b_citation_1_av * citation_1
    + b_crash_exp_1_av * crash_exp_1
    + b_rec_trips_av * rec_trips
    + b_av_fam_tp * av_fam
    + b_time_av * time
    + b_cost_av * cost
    + b_veh_own_1_av * veh_own_1
    + b_veh_type_1_av * veh_type_1
    + b_veh_type_2_av * veh_type_2
    + b_veh_type_3_av * veh_type_3
    + b_veh_feature_1_av * veh_feature_1
    + b_veh_feature_2_av * veh_feature_2
    + b_veh_feature_3_av * veh_feature_3
    + b_veh_feature_4_av * veh_feature_4
    + b_veh_feature_5_av * veh_feature_5
    + b_veh_feature_6_av * veh_feature_6
    + b_veh_feature_7_av * veh_feature_7
    + b_companion_tot_av * companion_tot
    + b_companion_1_av * companion_1
    + b_companion_2_av * companion_2
    + b_companion_3_av * companion_3
    + b_companion_4_av * companion_4
    + b_companion_5_av * companion_5
    + b_per_drive_3_av * per_drive_3
    + b_per_drive_4_av * per_drive_4
    + b_per_drive_5_av * per_drive_5
    + b_trip_exp_1_av * trip_exp_1
    + b_trip_exp_3_av * trip_exp_3
    + b_trip_exp_4_av * trip_exp_4
    + b_tba_g1_hv_d_av * tba_g1_hv_d
    + b_tba_g2_hv_d_av * tba_g2_hv_d
    + b_tba_g3_hv_d_av * tba_g3_hv_d
    + b_tba_g4_hv_d_av * tba_g4_hv_d
    + b_tba_g5_hv_d_av * tba_g5_hv_d
    + b_tba_g6_hv_d_av * tba_g6_hv_d
    + b_tba_g7_hv_d_av * tba_g7_hv_d
    + b_tba_g1_av_d_av * tba_g1_av_d
    + b_tba_g2_av_d_av * tba_g2_av_d
    + b_tba_g3_av_d_av * tba_g3_av_d
    + b_tba_g4_av_d_av * tba_g4_av_d
    + b_tba_g5_av_d_av * tba_g5_av_d
    + b_tba_g6_av_d_av * tba_g6_av_d
    + b_tba_g7_av_d_av * tba_g7_av_d
    + b_tu_hv_av * tu_hv
    + b_tu_av_av * tu_av
    + b_av_usefulness_av * av_usefulness
    + b_av_concern_av * av_concern
    + b_tech_savviness_av * tech_savviness
    + b_driving_enjoyment_av * driving_enjoyment
    + b_polychronicity_av * polychronicity
    + b_envt_concern_av * envt_concern
)

v3 = (
    asc_tp
    + b_age_grp_2_tp * age_grp_2
    + b_age_grp_3_tp * age_grp_3
    + b_gender_1_tp * gender_1
    + b_education_2_tp * education_2
    + b_education_3_tp * education_3
    + b_employment_2_tp * employment_2
    + b_employment_3_tp * employment_3
    + b_race_1_tp * race_1
    + b_hh_adult_tp * hh_adult
    + b_hh_child_tp * hh_child
    + b_income_grp_2_tp * income_grp_2
    + b_income_grp_3_tp * income_grp_3
    + b_income_grp_4_tp * income_grp_4
    + b_income_grp_5_tp * income_grp_5
    + b_driving_exp_tp * driving_exp
    + b_hh_vehs_tp * hh_vehs
    + b_mode_commute_3_tp * mode_commute_3
    + b_mode_shopping_3_tp * mode_shopping_3
    + b_mode_personal_3_tp * mode_personal_3
    + b_mode_social_3_tp * mode_social_3
    + b_citation_1_tp * citation_1
    + b_crash_exp_1_tp * crash_exp_1
    + b_rec_trips_tp * rec_trips
    + b_av_fam_tp * av_fam
    + b_time_tp * time
    + b_cost_tp * cost
    + b_veh_own_1_tp * veh_own_1
    + b_veh_type_1_tp * veh_type_1
    + b_veh_type_2_tp * veh_type_2
    + b_veh_type_3_tp * veh_type_3
    + b_veh_feature_1_tp * veh_feature_1
    + b_veh_feature_2_tp * veh_feature_2
    + b_veh_feature_3_tp * veh_feature_3
    + b_veh_feature_4_tp * veh_feature_4
    + b_veh_feature_5_tp * veh_feature_5
    + b_veh_feature_6_tp * veh_feature_6
    + b_veh_feature_7_tp * veh_feature_7
    + b_companion_tot_tp * companion_tot
    + b_companion_1_tp * companion_1
    + b_companion_2_tp * companion_2
    + b_companion_3_tp * companion_3
    + b_companion_4_tp * companion_4
    + b_companion_5_tp * companion_5
    + b_per_drive_3_tp * per_drive_3
    + b_per_drive_4_tp * per_drive_4
    + b_per_drive_5_tp * per_drive_5
    + b_trip_exp_1_tp * trip_exp_1
    + b_trip_exp_3_tp * trip_exp_3
    + b_trip_exp_4_tp * trip_exp_4
    + b_tba_g1_hv_d_tp * tba_g1_hv_d
    + b_tba_g2_hv_d_tp * tba_g2_hv_d
    + b_tba_g3_hv_d_tp * tba_g3_hv_d
    + b_tba_g4_hv_d_tp * tba_g4_hv_d
    + b_tba_g5_hv_d_tp * tba_g5_hv_d
    + b_tba_g6_hv_d_tp * tba_g6_hv_d
    + b_tba_g7_hv_d_tp * tba_g7_hv_d
    + b_tba_g1_av_d_tp * tba_g1_av
    + b_tba_g2_av_d_tp * tba_g2_av
    + b_tba_g3_av_d_tp * tba_g3_av
    + b_tba_g4_av_d_tp * tba_g4_av
    + b_tba_g5_av_d_tp * tba_g5_av
    + b_tba_g6_av_d_tp * tba_g6_av
    + b_tba_g7_av_d_tp * tba_g7_av
    + b_tu_hv_tp * tu_hv
    + b_tu_av_tp * tu_av
    + b_av_usefulness_tp * av_usefulness
    + b_av_concern_tp * av_concern
    + b_tech_savviness_tp * tech_savviness
    + b_driving_enjoyment_tp * driving_enjoyment
    + b_polychronicity_tp * polychronicity
    + b_envt_concern_tp * envt_concern
)

# link utility functions with the numbering of alternatives
v = {1: v1, 2: v2, 3: v3}

# availability of each alternatives
avail = {1: hv_avail, 2: av_avail, 3: tp_avail}

# define the model
logprog = models.loglogit(v, avail, chosen)

# create biogeme object
biogeme = bio.BIOGEME(database, logprog, suggestScales=False)
biogeme.modelName = "mnl-ranked-choice"

# get the results in a pandas table
print(biogeme.estimate().getEstimatedParameters())

# move outputs to outputs folder
os.remove("mnl-ranked-choice.pickle")
shutil.move("mnl-ranked-choice.html", "../outputs/mnl-ranked-choice.html")
# ---------------------------------------------------------------------------------------------------------------------#
