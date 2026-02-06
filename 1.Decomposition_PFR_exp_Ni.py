# Ammonia synthesis CSTR results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'
#%% data load
parameter_data = pd.read_csv('decomposition LHHW aspen parameter Ni.csv',encoding='CP949')

#%%
#set
#T_C_list = [450,400] #°C#
T_C_list = list(range(400, 510, 10)) #[500,450,400,350,300] #°C

#T_C = 450 #°C

P_bar = 1 

GHSV_list = [6000,12000,18000,24000,30000,36000] #L/h/kg
#GHSV = 6000 #L/h/kg #6000,12000,18000,24000,30000,36000
vol_flowrate = 60*60*10**(-3) #60ml/min -> 60*60*10**(-3)L/h  #High pressure ammonia decomposition on Ru–K/CaO catalysts
R = 8.314 # J mol−1 K−1
#%%


for T_C in T_C_list:
    for GHSV in GHSV_list:
        conversion_ammonia_PFR_list = []
        error_index_overall_list =[]
        
        #link aspen file
        path = os.getcwd()
        file_path = '1. Aspen_file_PFR_experiment/Ammonia decomposition_PFR_experiment.apw'
        link = win32.gencache.EnsureDispatch("Apwn.Document")
        link.InitFromArchive2(os.path.abspath(file_path))
        link.Visible = False
        
        
        for i in range(0,len(parameter_data),1): #i=0


            cat_usage = vol_flowrate / GHSV #kg
            void_fraction = 0.5
            cat_density = 800 #kg/m3
            reactor_volume = cat_usage / cat_density / void_fraction #m3
            L_D_ratio = 10.8 #https://www.sciencedirect.com/science/article/pii/S1369703X24002249#fig0005
            D = (4*reactor_volume/L_D_ratio/3.14)**(1/3)
            L = L_D_ratio * D


            #calculated
            T = T_C + 273.15 #°C->K
            P = P_bar*0.986923 # bar->atm
        
            

            # data input
            link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = -51
            link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = 13026

            #driving force
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= parameter_data.iloc[i,0]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = parameter_data.iloc[i,1]
            

            #adsorption
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = parameter_data.iloc[i,2]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = parameter_data.iloc[i,3]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = parameter_data.iloc[i,4]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = parameter_data.iloc[i,5]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/4").Value = parameter_data.iloc[i,6]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/4").Value = parameter_data.iloc[i,7]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/5").Value = parameter_data.iloc[i,8]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/5").Value = parameter_data.iloc[i,9]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/6").Value = parameter_data.iloc[i,10]
            link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/6").Value = parameter_data.iloc[i,11]
            
            # reactor volume
            link.Tree.FindNode("/Data/Blocks/DEC1/Input/LENGTH").Value = L # PFR length # m
            link.Tree.FindNode("/Data/Blocks/DEC1/Input/DIAM").Value = D # PFR diameter # m
            
            # GHSV
            link.Tree.FindNode("/Data/Streams/NH3-1/Input/TOTFLOW/MIXED").Value = vol_flowrate # GHSV=36000 # L/hkg
            
            # Pressure
            link.Tree.FindNode("/Data/Blocks/DEC1/Input/PRES").Value = P # P=10 # atm
            # Temperature
            link.Tree.FindNode("/Data/Blocks/DEC1/Input/REAC_TEMP").Value = T #  Temperature # K
            
            #gibbs
            link.Tree.FindNode("/Data/Blocks/B1/Input/PRES").Value = P # P=10 # atm
            link.Tree.FindNode("/Data/Blocks/B1/Input/TEMP").Value = T # CSTR Temperature # K
            link.Tree.FindNode("/Data/Streams/S1/Input/TOTFLOW/MIXED").Value = vol_flowrate # GHSV=36000 # L/hkg
            
            
            link.Engine.Run2()
            
            if not link.Engine.IsRunning:
                initial_ammonia = link.Tree.FindNode("/Data/Streams/NH3-1/Output/MOLEFLOW/MIXED/NH3").Value #mole
                remained_ammonia = link.Tree.FindNode("/Data/Streams/H2N2-1/Output/MOLEFLOW/MIXED/NH3").Value #mole
                conversion_ammonia_PFR = (initial_ammonia - remained_ammonia)/initial_ammonia * 100 #%
                conversion_ammonia_PFR_list.append(conversion_ammonia_PFR)
                print('conversion_ammonia_PFR',conversion_ammonia_PFR)
                
                error_index = link.Tree.FindNode("/Data/Results Summary/Run-Status/Output/PER_ERROR").Value #1==error, 0=ok
                error_index_overall_list.append(error_index)
                print('error_index:',error_index)
                
                initial_ammonia_eq = link.Tree.FindNode("/Data/Streams/S1/Output/MOLEFLOW/MIXED/NH3").Value #mole
                remained_ammonia_eq = link.Tree.FindNode("/Data/Streams/S2/Output/MOLEFLOW/MIXED/NH3").Value #mole
                conversion_ammonia_eq = (initial_ammonia_eq - remained_ammonia_eq)/initial_ammonia_eq * 100 #%
                print('NH3 conversion at eq(%):',conversion_ammonia_eq)
                
        if link is not None:
            link.Close()
        else:
            pass
                
            
            
        # Plot
        num_columns = len(conversion_ammonia_PFR_list)
        catalyst_list = [f"{i}" for i in range(1, len(conversion_ammonia_PFR_list)+1)]
        df_result = pd.DataFrame({
            'Catalyst#': catalyst_list,
            'NH3 Conversion PFR(%)': conversion_ammonia_PFR_list,
            'error overall': error_index_overall_list})
        df_result_sorted = df_result.sort_values(by='NH3 Conversion PFR(%)', ascending=False).reset_index(drop=True)



        #Catalyst vs CSTR conversion
        plt.figure(figsize=(12, 5), dpi=300)
        plt.bar(df_result_sorted.iloc[:,0], df_result_sorted.iloc[:,1],color='black')
        for i, value in enumerate(df_result_sorted.iloc[:,1]):
            plt.text(i, value + 0, f'{value:.1f}', ha='center', va='bottom',fontsize=8)
        plt.axhline(y=conversion_ammonia_eq, color='red', linestyle='--')
        plt.text(len(df_result_sorted.iloc[:,0])-1, conversion_ammonia_eq, f'{conversion_ammonia_eq:.1f}%', color='red', ha='right', va='bottom')
        plt.title(f'Ni \nTemperature: {T_C}°C, Pressure: {P_bar}bar, GHSV: {GHSV}L/h/kg',fontsize=14)
        plt.xlabel('Catalyst type',fontsize=12)
        plt.ylabel('NH$_{3}$ conversion(%)',fontsize=12)
        plt.grid(True, axis='y')
        wd = os.getcwd()
        saving_path = wd+"/Guideline table/PFR_exp/{}_{}_{}_{}.png"
        save_file = saving_path.format('PFR_exp', T_C, GHSV, 'Ni') 
        plt.savefig(save_file)  
        plt.show()


        # save
        wd = os.getcwd()
        saving_path = wd+"/Guideline table/PFR_exp/{}_{}_{}_{}.csv" ##파일명 stage 숫자 바꾸기
        save_file = saving_path.format('PFR_exp', T_C, GHSV, 'Ni') 
        df_result.to_csv(save_file, index=False)

