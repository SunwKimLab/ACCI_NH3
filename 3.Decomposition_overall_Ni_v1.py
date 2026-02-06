import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
from Economic_NH3 import *

# from Decomposition_Ni_def import *
from Decomposition_Ni_def_recycleX import *

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'

#%%
T_C = 800

P_bar = 8 #bar

GHSV = 12000 #L/h/kg #6000,12000,18000,24000,30000,36000




ammonia_cost = 0.7 
 

d_km = 7065

cat_idx = 2

ammonia_cost = 0.6198258568850152 # KM1

elec_cost= 0.065
cooling_water_cost= 0.35
catalyst_cost_Ni= 47.02
ads_cost= 3.41
NOxtreat_cost= 2
BlueNH3_cost = 0.25
#%%
# link aspen file
path = os.getcwd()
file_path = '4. Aspen_file_overall_scaleup/Ammonia decomposition_overall_v5.apw'
link = win32.gencache.EnsureDispatch("Apwn.Document")
link.InitFromArchive2(os.path.abspath(file_path))
link.Visible = False

#%%

results = sim_NH3_dec_Ni(link, ammonia_cost, d_km, cat_idx, T_C, P_bar, GHSV, elec_cost, cooling_water_cost, catalyst_cost_Ni, ads_cost, NOxtreat_cost, BlueNH3_cost)

results['LCOH']['LCOH_catX']

#%%

if link is not None:
    link.Close()
else:
    pass











