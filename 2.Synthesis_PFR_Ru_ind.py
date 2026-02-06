# Ammonia synthesis PFR results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'
#%% data load
parameter_data = pd.read_csv('synthesis LHHW aspen parameter Ru.csv',encoding='CP949')

#%%
#set
T_C_list = [300,350,400,450,500] #°C
# T_C = 500

P_bar = 150 #bar

GHSV_list = [12000,18000,24000,36000,60000,72000] #L/h/kg
#GHSV = 36000 #L/h/kg #6000,12000,18000,24000,30000,36000
vol_flowrate = 127737002 #L/h # 500MW electorlysis 기준 H2 8.88 ton/h
R = 8.314 # J mol−1 K−1
#%%
# link aspen file
path = os.getcwd()
file_path = '3. Aspen_file_PFR_scaleup/Ammonia synthesis_PFR_scaleup.apw'
link = win32.gencache.EnsureDispatch("Apwn.Document")
link.InitFromArchive2(os.path.abspath(file_path))
link.Visible = False

for T_C in T_C_list:
    for GHSV in GHSV_list:
        conversion_hydrogen_PFR_list = []
        error_index_overall_list =[]
        conversion_hydrogen_equil_list=[]
        for i in range(0,len(parameter_data),1): #i=0

            
            cat_usage = vol_flowrate / GHSV #kg
            void_fraction = 0.5
            cat_density = 800 #kg/m3
            reactor_volume = cat_usage / cat_density / void_fraction #m3
            L_D_ratio = 5.9 #https://www.sciencedirect.com/science/article/pii/S1369703X24002249#fig0005
            D = (4*reactor_volume/L_D_ratio/3.14)**(1/3)
            L = L_D_ratio * D

            
            #calculated
            T = T_C + 273.15 #°C->K
            P = P_bar * 0.9869 # bar->atm
        
            
            response_error = 1
            wait_time = 30

            while response_error == 1:
                try:
                    # data input
                    #driving force
                    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF1_A/1").Value = 0
                    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = 5.056
                    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = -4609
                    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_C/1").Value = 2.69
                    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_D/1").Value = 0.000127
                    
                    # data input
                    #driving force
                    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= parameter_data.iloc[i,0] # A_f = 100000
                    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = parameter_data.iloc[i,1] #J/mol # Ea_f=100000
                    
                    
                    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = parameter_data.iloc[i,2]
                    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = parameter_data.iloc[i,3]
                    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = parameter_data.iloc[i,4]
                    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = parameter_data.iloc[i,5]
                    
                    #Set condition
                    link.Tree.FindNode("/Data/Streams/H2N2/Input/TOTFLOW/MIXED").Value = vol_flowrate # L h-1  
                    link.Tree.FindNode("/Data/Blocks/COMP1/Input/PRES").Value = P # comp pressure # atm
                    
                    link.Tree.FindNode("/Data/Blocks/COOL1/Input/PRES").Value = P # PFR pressure # atm
                    link.Tree.FindNode("/Data/Blocks/COOL1/Input/TEMP").Value = T # PFR Temperature # K
        
                    
                    link.Tree.FindNode("/Data/Blocks/SYN1/Input/LENGTH").Value = L # PFR length # m
                    link.Tree.FindNode("/Data/Blocks/SYN1/Input/DIAM").Value = D # PFR diameter # m
                    
                    #gibss reactor
                    link.Tree.FindNode("/Data/Blocks/B1/Input/PRES").Value = P # PFR pressure # atm
                    link.Tree.FindNode("/Data/Blocks/B1/Input/TEMP").Value = T # PFR pressure # atm
                    link.Tree.FindNode("/Data/Blocks/B3/Input/PRES").Value = P # PFR pressure # atm
                    link.Tree.FindNode("/Data/Streams/S1/Input/TOTFLOW/MIXED").Value = vol_flowrate # L h-1  
                    
                    link.Engine.Run2()
                    
                    if not link.Engine.IsRunning:
                        initial_hydrogen = link.Tree.FindNode("/Data/Streams/H2N2/Output/MOLEFLOW/MIXED/H2").Value #mole
                        remained_hydrogen = link.Tree.FindNode("/Data/Streams/NH3-1/Output/MOLEFLOW/MIXED/H2").Value #mole
                        conversion_hydrogen_PFR = (initial_hydrogen - remained_hydrogen)/initial_hydrogen * 100 #%
                        conversion_hydrogen_PFR_list.append(conversion_hydrogen_PFR)
                    
                        
                        error_index = link.Tree.FindNode("/Data/Results Summary/Run-Status/Output/PER_ERROR").Value #1==error, 0=ok
                        error_index_overall_list.append(error_index)
                        
                        
                        initial_hydrogen_eq = link.Tree.FindNode("/Data/Streams/S1/Output/MOLEFLOW/MIXED/H2").Value #mole
                        remained_hydrogen_eq = link.Tree.FindNode("/Data/Streams/S2/Output/MOLEFLOW/MIXED/H2").Value #mole
                        conversion_hydrogen_eq = (initial_hydrogen_eq - remained_hydrogen_eq)/initial_hydrogen_eq * 100 #%
                        
                        response_error = 0
                except:
                    print('waiting {} sec for link again'.format(wait_time))
                    time.sleep(wait_time)
                    response_error = 1
                    pass
            
            print('H2 conversion(%):',conversion_hydrogen_PFR)
            print('H2 conversion at eq(%):',conversion_hydrogen_eq)
            print('error_index:',error_index)
            
        # Plot
        num_columns = len(conversion_hydrogen_PFR_list)
        catalyst_list = [f"{i}" for i in range(1, len(conversion_hydrogen_PFR_list)+1)]
        df_result = pd.DataFrame({
            'Catalyst#': catalyst_list,
            'H2 Conversion PFR(%)': conversion_hydrogen_PFR_list,
            'error overall': error_index_overall_list})
        df_result_sorted = df_result.sort_values(by='H2 Conversion PFR(%)', ascending=False).reset_index(drop=True)



        #Catalyst vs PFR conversion
        plt.figure(figsize=(12, 5), dpi=300)
        plt.bar(df_result_sorted.iloc[:,0], df_result_sorted.iloc[:,1],color='black')
        for i, value in enumerate(df_result_sorted.iloc[:,1]):
            plt.text(i, value + 0, f'{value:.1f}', ha='center', va='bottom',fontsize=8)
        plt.axhline(y=conversion_hydrogen_eq, color='red', linestyle='--')
        plt.text(len(df_result_sorted.iloc[:,0])-1, conversion_hydrogen_eq, f'{conversion_hydrogen_eq:.1f}%', color='red', ha='right', va='bottom')
        plt.title(f'Ru \nTemperature: {T_C}°C, Pressure: {P_bar}bar, GHSV: {GHSV}L/h/kg',fontsize=14)
        plt.xlabel('Catalyst type',fontsize=12)
        plt.ylabel('H$_{2}$ conversion(%)',fontsize=12)
        plt.grid(True, axis='y')
        wd = os.getcwd()
        saving_path = wd+"/Guideline table/PFR_ind/{}_{}_{}_{}.png"
        save_file = saving_path.format('PFR', T_C, GHSV, 'Ru') 
        plt.savefig(save_file)  
        plt.show()


        # save
        wd = os.getcwd()
        saving_path = wd+"/Guideline table/PFR_ind/{}_{}_{}_{}.csv" ##파일명 stage 숫자 바꾸기
        save_file = saving_path.format('PFR', T_C, GHSV, 'Ru') 
        df_result.to_csv(save_file, index=False)

    
if link is not None:
    link.Close()
else:
    pass

