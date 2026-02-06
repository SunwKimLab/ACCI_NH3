
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import csv
import math
import time
wd = os.getcwd()
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'
#%% file load
df = pd.read_csv('decomposition catalyst experiment data Ru.csv',encoding='CP949')
experiment_data = df
#%% 
R = 8.314 # J mol−1 K−1

#%%
rxn_rate_exp = experiment_data.iloc[:,13].to_numpy().reshape(-1,1)
#%% Data fit 
par_1_fin_list= []
par_2_fin_list= []
par_3_fin_list= []
par_4_fin_list= []
par_5_fin_list= []
par_6_fin_list= []
par_7_fin_list= []
par_8_fin_list= []
par_9_fin_list= []
par_10_fin_list= []
par_11_fin_list= []
par_12_fin_list= []



r2_fin_list = []
mse_fin_list = []
rmse_fin_list = []
mae_fin_list = []

rxn_rate_aspen_fin_list = []
nh3_out_aspen_fin_list = []

#%%
for i in range(0, len(df), 14):#14개씩 #len(df) i=0
#촉매 선택
#n=1
#i = 14*(n-1)
    #list setup
    par_1_list= []
    par_2_list= []
    par_3_list= []
    par_4_list= []
    par_5_list= []
    par_6_list= []
    par_7_list= []
    par_8_list= []
    par_9_list= []
    par_10_list= []
    par_11_list= []
    par_12_list= []

    
    r2_list = []
    mse_list = []
    rmse_list = []
    mae_list = []
    print(int((i+14)/14),'th fitting start')
    tol_list = [1e-0,5e-1,1e-1,5e-2,1e-2,5e-3,1e-3,5e-4,1e-4,5e-5,1e-5,5e-6,1e-6] #tol=1e-2
    
    response_error = 1
    wait_time = 30
    
    while response_error == 1:
        try:
    
            for tol in tol_list:
                print('tol', tol)
                
                #link aspen file
                path = os.getcwd()
                file_path = '1. Aspen_file_PFR_fitting_datafit/Ammonia decomposition_PFR_fit.apw'
                link = win32.gencache.EnsureDispatch("Apwn.Document")
                link.InitFromArchive2(os.path.abspath(file_path))
                link.Visible = False
                
                rxn_rate_aspen_list = []
                nh3_out_aspen_list = []
                
                
                # data input
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#1\T\INPUT").Value = experiment_data.iloc[i,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#2\T\INPUT").Value = experiment_data.iloc[i+1,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#3\T\INPUT").Value = experiment_data.iloc[i+2,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#4\T\INPUT").Value = experiment_data.iloc[i+3,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#5\T\INPUT").Value = experiment_data.iloc[i+4,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#6\T\INPUT").Value = experiment_data.iloc[i+5,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#7\T\INPUT").Value = experiment_data.iloc[i+6,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#8\T\INPUT").Value = experiment_data.iloc[i+7,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#9\T\INPUT").Value = experiment_data.iloc[i+8,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#10\T\INPUT").Value = experiment_data.iloc[i+9,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#11\T\INPUT").Value = experiment_data.iloc[i+10,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#12\T\INPUT").Value = experiment_data.iloc[i+11,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#13\T\INPUT").Value = experiment_data.iloc[i+12,9] #K
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#14\T\INPUT").Value = experiment_data.iloc[i+13,9] #K
                
                
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#1/NH3OUT\RESULT").Value = experiment_data.iloc[i,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#2/NH3OUT\RESULT").Value = experiment_data.iloc[i+1,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#3/NH3OUT\RESULT").Value = experiment_data.iloc[i+2,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#4/NH3OUT\RESULT").Value = experiment_data.iloc[i+3,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#5/NH3OUT\RESULT").Value = experiment_data.iloc[i+4,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#6/NH3OUT\RESULT").Value = experiment_data.iloc[i+5,12] ##mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#7/NH3OUT\RESULT").Value = experiment_data.iloc[i+6,12] ##mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#8/NH3OUT\RESULT").Value = experiment_data.iloc[i+7,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#9/NH3OUT\RESULT").Value = experiment_data.iloc[i+8,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#10/NH3OUT\RESULT").Value = experiment_data.iloc[i+9,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#11/NH3OUT\RESULT").Value = experiment_data.iloc[i+10,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#12/NH3OUT\RESULT").Value = experiment_data.iloc[i+11,12] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#13/NH3OUT\RESULT").Value = experiment_data.iloc[i+12,12] ##mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#14/NH3OUT\RESULT").Value = experiment_data.iloc[i+13,12] #mol/g/h
                
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#0/NH3OUT\RESULT").Value = tol*np.std(experiment_data.iloc[i:i+14,12]) #standard deviation
                
                
                link.Tree.FindNode("/Data/Streams/NH3-1/Input/TOTFLOW/MIXED").Value = experiment_data.iloc[i,5]/1000 # GHSV # L/h/g
                link.Tree.FindNode("/Data/Blocks/DEC1/Input/PRES").Value = experiment_data.iloc[i,7] # P # atm
                
            
                
                # run
                link.Engine.Run2()
                
                
                if not link.Engine.IsRunning:   
                    A_f = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/1").Value 
                    Ea_f = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/2").Value 
                    C_ad2_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/3").Value
                    C_ad2_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/4").Value
                    C_ad3_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/5").Value 
                    C_ad3_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/6").Value 
                    C_ad4_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/7").Value 
                    C_ad4_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/8").Value 
                    C_ad5_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/9").Value 
                    C_ad5_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/10").Value 
                    C_ad6_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/11").Value 
                    C_ad6_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/12").Value 
                    
                    par_1_list.append(A_f)
                    par_2_list.append(Ea_f)
                    par_3_list.append(C_ad2_A)
                    par_4_list.append(C_ad2_B)
                    par_5_list.append(C_ad3_A)
                    par_6_list.append(C_ad3_B)
                    par_7_list.append(C_ad4_A)
                    par_8_list.append(C_ad4_B)
                    par_9_list.append(C_ad5_A)
                    par_10_list.append(C_ad5_B)
                    par_11_list.append(C_ad6_A)
                    par_12_list.append(C_ad6_B)
                    
                if link is not None:
                    link.Close()
                else:
                    pass
                
                print(int((i+14)/14),'th fitting done')   
                
                print(int((i+14)/14),'th validation start')   
                
                # Validation
                path = os.getcwd()
                file_path = '1. Aspen_file_PFR_fitting_datafit/Ammonia decomposition_PFR_val.apw'
                link = win32.gencache.EnsureDispatch("Apwn.Document")
                link.InitFromArchive2(os.path.abspath(file_path))
                link.Visible = False
                
                
                # data input
                #driving force
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= A_f # A_f = 100000
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = Ea_f #J/mol # Ea_f=100000
                #adsorption
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = C_ad2_A
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = C_ad2_B
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = C_ad3_A
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = C_ad3_B
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/4").Value = C_ad4_A
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/4").Value = C_ad4_B
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/5").Value = C_ad5_A
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/5").Value = C_ad5_B
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/6").Value = C_ad6_A
                link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/6").Value = C_ad6_B

                for j in range(i, i+14, 1):
                
                    link.Tree.FindNode("/Data/Streams/NH3-1/Input/TOTFLOW/MIXED").Value = experiment_data.iloc[j,5]/1000 # GHSV # L/h/g
                    link.Tree.FindNode("/Data/Streams/NH3-1/Input/TEMP/MIXED").Value = 273.15 #K
                    link.Tree.FindNode("/Data/Blocks/DEC1/Input/PRES").Value = experiment_data.iloc[j,7] # CSTR pressure # atm
                    link.Tree.FindNode("/Data/Blocks/DEC1/Input/REAC_TEMP").Value = experiment_data.iloc[j,9] # CSTR Temperature # K
                
                    link.Engine.Run2()
                    
                    if not link.Engine.IsRunning:

                        nh3_out_aspen = link.Tree.FindNode("/Data/Streams/H2N2-1/Output/MOLEFLOW/MIXED/NH3").Value*1000*3600 #kmol/s -> mol/h
                        nh3_out_aspen_list.append(nh3_out_aspen)
                        rxn_rate_aspen = 1.5*(experiment_data.iloc[j,5]/1000*0.0445896223 - nh3_out_aspen)/1 #mol/g/h
                        rxn_rate_aspen_list.append(rxn_rate_aspen)
                
                if link is not None:
                    link.Close()
                else:
                    pass
                    
                ### r2
                r2= r2_score(experiment_data.iloc[i:i+14,13], rxn_rate_aspen_list)
                r2_list.append(r2)
                mse= mean_squared_error(experiment_data.iloc[i:i+14,13], rxn_rate_aspen_list)
                mse_list.append(mse)
                rmse = np.sqrt(mse)
                rmse_list.append(rmse)
                mae = mean_absolute_error(experiment_data.iloc[i:i+14,13], rxn_rate_aspen_list)
                mae_list.append(mae)
                
                print(int((i+14)/14),'th r2:',r2) 
                print(int((i+14)/14),'th validation done')   
                print('---------------------------------------------------------------')
                
                # Stop iterating if r2 is greater than or equal to 0.98
                if r2 >= 0.97:
                    break
                
            response_error = 0
        except:
            print('waiting {} sec for link again'.format(wait_time))
            time.sleep(wait_time)
            response_error = 1
            pass    
    
    
    
    #가장 좋은 tol, 파라미터 설정
    r2_best_th = r2_list.index(max(r2_list))
    tol_best = tol_list[r2_best_th]
    A_f = par_1_list[r2_best_th]
    Ea_f = par_2_list[r2_best_th]
    C_ad2_A = par_3_list[r2_best_th]
    C_ad2_B = par_4_list[r2_best_th]
    C_ad3_A= par_5_list[r2_best_th] 
    C_ad3_B = par_6_list[r2_best_th]
    C_ad4_A = par_7_list[r2_best_th]
    C_ad4_B = par_8_list[r2_best_th]
    C_ad5_A = par_9_list[r2_best_th]
    C_ad5_B = par_10_list[r2_best_th]
    C_ad6_A = par_11_list[r2_best_th]
    C_ad6_B = par_12_list[r2_best_th]
    
    #
    par_1_fin_list.append(A_f)
    par_2_fin_list.append(Ea_f)
    par_3_fin_list.append(C_ad2_A)
    par_4_fin_list.append(C_ad2_B)
    par_5_fin_list.append(C_ad3_A)
    par_6_fin_list.append(C_ad3_B)
    par_7_fin_list.append(C_ad4_A)
    par_8_fin_list.append(C_ad4_B)
    par_9_fin_list.append(C_ad5_A)
    par_10_fin_list.append(C_ad5_B)
    par_11_fin_list.append(C_ad6_A)
    par_12_fin_list.append(C_ad6_B)         
    
    print(int((i+14)/14),'th validation start')   
    # Validation
    path = os.getcwd()
    file_path = '1. Aspen_file_PFR_fitting_datafit/Ammonia decomposition_PFR_val.apw'
    link = win32.gencache.EnsureDispatch("Apwn.Document")
    link.InitFromArchive2(os.path.abspath(file_path))
    link.Visible = False
                
    # data input
    #driving force
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= A_f # A_f = 100000
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = Ea_f #J/mol # Ea_f=100000
    #adsorption
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = C_ad2_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = C_ad2_B
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = C_ad3_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = C_ad3_B
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/4").Value = C_ad4_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/4").Value = C_ad4_B
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/5").Value = C_ad5_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/5").Value = C_ad5_B
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/6").Value = C_ad6_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/6").Value = C_ad6_B           
                
    for j in range(i, i+14, 1):
    
        link.Tree.FindNode("/Data/Streams/NH3-1/Input/TOTFLOW/MIXED").Value = experiment_data.iloc[j,5]/1000 # GHSV # L/h/g
        link.Tree.FindNode("/Data/Streams/NH3-1/Input/TEMP/MIXED").Value = 273.15 #K
        link.Tree.FindNode("/Data/Blocks/DEC1/Input/PRES").Value = experiment_data.iloc[j,7] # CSTR pressure # atm
        link.Tree.FindNode("/Data/Blocks/DEC1/Input/REAC_TEMP").Value = experiment_data.iloc[j,9] # CSTR Temperature # K
    
        link.Engine.Run2()
        
        if not link.Engine.IsRunning:

            nh3_out_aspen = link.Tree.FindNode("/Data/Streams/H2N2-1/Output/MOLEFLOW/MIXED/NH3").Value*1000*3600 #kmol/s -> mol/h
            nh3_out_aspen_fin_list.append(nh3_out_aspen)
            rxn_rate_aspen = 1.5*(experiment_data.iloc[j,5]/1000*0.0445896223 - nh3_out_aspen)/1 #mol/g/h
            rxn_rate_aspen_fin_list.append(rxn_rate_aspen)
    
    if link is not None:
        link.Close()
    else:
        pass            
                
             
    ### Plot
    T = df.iloc[i:i+14,9].to_numpy().reshape(-1,1)
    r_dec_exp = df.iloc[i:i+14,13].to_numpy().reshape(-1,1)
    fig, ax = plt.subplots(dpi=300, figsize=[7, 5.5])
    
    #exp
    ax.plot(T, r_dec_exp, 'o', markersize = 9, alpha = 0.6, mfc = 'b',
            mec = 'k', markeredgewidth =1.5, label='Exp data')
    
    #cal
    r_dec_sim= rxn_rate_aspen_fin_list[i:i+14]
    ax.plot(T, r_dec_sim, linewidth = 2.1, label='Fitting data')
    
    title_row = df.iloc[i]
    title = f"{title_row['Catalyst']}({title_row['Doping wt%']}%)/{title_row['Support (Promoter)']}"
    plt.title(title,size=15)
    
    plt.grid(linestyle = '--')
    plt.xlabel("Temperature (K)", fontsize=12)
    plt.ylabel("H$_{2}$ production rate (mol g$^{-1}$ h$^{-1}$)", fontsize=12)
    plt.legend()
    filename = f"\{title_row['Number']}.{title_row['Catalyst']}({title_row['Doping wt%']}%)_{title_row['Support (Promoter)']}.png"
    wd = os.getcwd()
    saving_path = wd+"\par_fit_figure/Ru"
    full_path = saving_path + filename
    plt.savefig(full_path)  
    plt.show()
    
    ### r2
    r2= r2_score(experiment_data.iloc[i:i+14,13], rxn_rate_aspen_fin_list[i:i+14])
    r2_fin_list.append(r2)
    mse= mean_squared_error(experiment_data.iloc[i:i+14,13], rxn_rate_aspen_fin_list[i:i+14])
    mse_fin_list.append(mse)
    rmse = np.sqrt(mse)
    rmse_fin_list.append(rmse)
    mae = mean_absolute_error(experiment_data.iloc[i:i+14,13], rxn_rate_aspen_fin_list[i:i+14])
    mae_fin_list.append(mae)
    
    print(int((i+14)/14),'th r2:',r2) 
    print(int((i+14)/14),'th validation done')   
    print('---------------------------------------------------------------')             
                
                
#%%
# par -> dataframe
par_df = pd.concat([pd.DataFrame({
    'A_f': par_1_fin_list,
    'Ea_f': par_2_fin_list,
    'C_ad2_A': par_3_fin_list,
    'C_ad2_B': par_4_fin_list,
    'C_ad3_A': par_5_fin_list,
    'C_ad3_B': par_6_fin_list,
    'C_ad4_A': par_7_fin_list,
    'C_ad4_B': par_8_fin_list,
    'C_ad5_A': par_9_fin_list,  
    'C_ad5_B': par_10_fin_list,
    'C_ad6_A': par_11_fin_list,
    'C_ad6_B': par_12_fin_list,
})], ignore_index=True)

###data 저장
#par
par_df.to_csv('decomposition LHHW aspen parameter Ru.csv', index=False)  
#rxn_rate_simulation
with open('decomposition rxn rate aspen Ru.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for item in rxn_rate_aspen_fin_list:
        writer.writerow([item]) 

#par converted
A_f_fin_list = par_1_fin_list
Ea_f_fin_list = par_2_fin_list
A_1_fin_list = [np.exp(item) for item in par_3_fin_list]
Ea_1_fin_list = [-R * item for item in par_4_fin_list]
A_2_fin_list = [np.exp(item) for item in par_5_fin_list]
Ea_2_fin_list = [-R * item for item in par_6_fin_list]
A_3_fin_list = [np.exp(item) for item in par_7_fin_list]
Ea_3_fin_list = [-R * item for item in par_8_fin_list]
A_4_fin_list = [np.exp(item) for item in par_9_fin_list]
Ea_4_fin_list = [-R * item for item in par_10_fin_list]
A_5_fin_list = [np.exp(item) for item in par_11_fin_list]
Ea_5_fin_list = [-R * item for item in par_12_fin_list]



par_converted_df = pd.concat([pd.DataFrame({
    'A_f': A_f_fin_list,
    'Ea_f(J/mol)': Ea_f_fin_list,
    'A_1': A_1_fin_list,
    'Ea_1(J/mol)': Ea_1_fin_list,
    'A_2': A_2_fin_list,
    'Ea_2(J/mol)': Ea_2_fin_list,
    'A_3': A_3_fin_list,
    'Ea_3(J/mol)': Ea_3_fin_list,
    'A_4': A_4_fin_list,
    'Ea_4(J/mol)': Ea_4_fin_list,
    'A_5': A_5_fin_list,
    'Ea_5(J/mol)': Ea_5_fin_list,
})], ignore_index=True)

par_converted_df.to_csv('decomposition LHHW parameter Ru.csv', index=False)                

#%%
ex = experiment_data.iloc[:,13]
cal = rxn_rate_aspen_fin_list 

# Plot
plt.figure(figsize=(7, 5.5), dpi=300)
plt.scatter(ex, cal,c='blue',edgecolor='blue')
x=np.linspace(min(experiment_data.iloc[:,13]),max(experiment_data.iloc[:,13]),100)
y=x
plt.plot(x,y,c='red')
plt.title('H$_{2}$ production rate (mol g$^{-1}$ h$^{-1}$) (Ru)',fontsize=17)
plt.xlabel('Experiment Data',fontsize=17)
plt.ylabel('Simulation Data',fontsize=17)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.grid(linestyle = '--')
wd = os.getcwd()
saving_path = wd+"\par_fit_figure/Ru/Parity plot (Ru)"
plt.savefig(saving_path)  
plt.show()

#%%
#r2
r2_overall= r2_score(ex, cal)
print('Overall r2:',r2_overall)
#mse
mse_overall= mean_squared_error(ex, cal)
print('Overall MSE:',mse_overall)
#rmse
rmse_overall = np.sqrt(mse_overall)
print('Overall RMSE:',rmse)
#mae
mae_overall= mean_absolute_error(ex, cal)
print('Overall MAE:',mae_overall)

### error
r2_fin_list.append(r2_overall)
mse_fin_list.append(mse_overall)
rmse_fin_list.append(rmse_overall)
mae_fin_list.append(mae_overall)

#error
error_df = pd.concat([pd.DataFrame({
    'r2': r2_fin_list,
    'mse': mse_fin_list,
    'rmse': rmse_fin_list,
    'mae': mae_fin_list      
})], ignore_index=True)
error_df.to_csv('decomposition rxn rate error Ru.csv', index=False) 