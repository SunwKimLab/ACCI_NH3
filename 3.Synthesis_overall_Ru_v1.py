# Ammonia synthesis overall results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
from Economic_NH3 import *

from Synthesis_Ru_def import *


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'


#%%
T_C = 500

P_bar = 150 #bar

GHSV = 12000 #L/h/kg #6000,12000,18000,24000,30000,36000


solar_irradiance_rich = 2351.25 #set #하나로 고정하고 돌려보기

cat_idx = 2

#%%
path = os.getcwd()
file_path = '4. Aspen_file_overall_scaleup/Ammonia synthesis_overall_scaleup_v2.apw'
link = win32.gencache.EnsureDispatch("Apwn.Document")
link.InitFromArchive2(os.path.abspath(file_path))
link.Visible = False
#%%

results = sim_NH3_syn_Ru(link, solar_irradiance_rich, cat_idx, T_C, P_bar, GHSV)


results['LCOA']['LCOA_catX']

#%%

if link is not None:
    link.Close()
else:
    pass

#%%




