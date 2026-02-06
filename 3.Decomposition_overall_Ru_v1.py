import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
from Economic_NH3 import *

from Decomposition_Ru_def import *

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'

#%%
T_C = 800

P_bar = 8 #bar

GHSV = 12000 #L/h/kg #6000,12000,18000,24000,30000,36000

ammonia_cost = 0.7 
 

d_km =7065

cat_idx = 2
#%%


# link aspen file
path = os.getcwd()
file_path = '4. Aspen_file_overall_scaleup/Ammonia decomposition_overall_v4.apw'
link = win32.gencache.EnsureDispatch("Apwn.Document")
link.InitFromArchive2(os.path.abspath(file_path))
link.Visible = False

#%%

results = sim_NH3_dec_Ru(link, ammonia_cost, d_km, cat_idx, T_C, P_bar, GHSV)

results['LCOH']['LCOH_catX']

#%%

if link is not None:
    link.Close()
else:
    pass