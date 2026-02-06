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
parameter_data = pd.read_csv('synthesis LHHW aspen parameter Fe.csv',encoding='CP949')

#%%
#set
#T_C_list = [500,450,400,350,300] #°C
#T_C_list = list(range(300, 510, 10)) #[500,450,400,350,300] #°C
T_C_list = list(range(390, 510, 10))

# T_C = 500

P_bar = 10 #bar


GHSV_list = [12000,18000,24000,36000,60000,72000] #L/h/kg
#GHSV = 12000 #L/h/kg #6000,12000,18000,24000,30000,36000
vol_flowrate = 60*60*10**(-3) #L/h #60 ml/min #Low-Temperature Ammonia Synthesis on Iron Catalyst with an Electron Donor

R = 8.314 # J mol−1 K−1
#%%

for T_C in T_C_list:
    for GHSV in GHSV_list:
        conversion_hydrogen_PFR_exp_list = []
        error_index_overall_list =[]
        conversion_hydrogen_equil_list=[]
        
        # link aspen file
        path = os.getcwd()
        file_path = '2. Aspen_file_PFR_experiment/Ammonia synthesis_PFR_exp.apw'
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
            link.Tree.FindNode("/Data/Streams/H2N2/Input/TEMP/MIXED").Value = 273.15 #K
            link.Tree.FindNode("/Data/Blocks/SYN1/Input/PRES").Value = P # PFR pressure # atm
            link.Tree.FindNode("/Data/Blocks/SYN1/Input/REAC_TEMP").Value = T # PFR Temperature # K

            
            link.Tree.FindNode("/Data/Blocks/SYN1/Input/LENGTH").Value = L # PFR length # m
            link.Tree.FindNode("/Data/Blocks/SYN1/Input/DIAM").Value = D # PFR diameter # m
            
            #gibss reactor
            link.Tree.FindNode("/Data/Blocks/B1/Input/PRES").Value = P # PFR pressure # atm
            link.Tree.FindNode("/Data/Blocks/B1/Input/TEMP").Value = T # PFR pressure # atm
            link.Tree.FindNode("/Data/Blocks/B3/Input/PRES").Value = P # PFR pressure # atm
            link.Tree.FindNode("/Data/Blocks/B3/Input/TEMP").Value = T # PFR pressure # atm
            link.Tree.FindNode("/Data/Streams/S1/Input/TOTFLOW/MIXED").Value = vol_flowrate # L h-1  
            
            link.Engine.Run2()
            
            if not link.Engine.IsRunning:
                initial_hydrogen = link.Tree.FindNode("/Data/Streams/H2N2/Output/MOLEFLOW/MIXED/H2").Value #mole
                remained_hydrogen = link.Tree.FindNode("/Data/Streams/NH3-1/Output/MOLEFLOW/MIXED/H2").Value #mole
                conversion_hydrogen_PFR_exp = (initial_hydrogen - remained_hydrogen)/initial_hydrogen * 100 #%
                conversion_hydrogen_PFR_exp_list.append(conversion_hydrogen_PFR_exp)
            
                
                error_index = link.Tree.FindNode("/Data/Results Summary/Run-Status/Output/PER_ERROR").Value #1==error, 0=ok
                error_index_overall_list.append(error_index)
                
                
                initial_hydrogen_eq = link.Tree.FindNode("/Data/Streams/S1/Output/MOLEFLOW/MIXED/H2").Value #mole
                remained_hydrogen_eq = link.Tree.FindNode("/Data/Streams/S2/Output/MOLEFLOW/MIXED/H2").Value #mole
                conversion_hydrogen_eq = (initial_hydrogen_eq - remained_hydrogen_eq)/initial_hydrogen_eq * 100 #%
                        
            
            print('H2 conversion(%):',conversion_hydrogen_PFR_exp)
            print('H2 conversion at eq(%):',conversion_hydrogen_eq)
            print('error_index:',error_index)
            
        if link is not None:
            link.Close()
        else:
            pass
               
        
        # Plot
        num_columns = len(conversion_hydrogen_PFR_exp_list)
        catalyst_list = [f"{i}" for i in range(1, len(conversion_hydrogen_PFR_exp_list)+1)]
        df_result = pd.DataFrame({
            'Catalyst#': catalyst_list,
            'H2 Conversion PFR(%)': conversion_hydrogen_PFR_exp_list,
            'error overall': error_index_overall_list})
        df_result_sorted = df_result.sort_values(by='H2 Conversion PFR(%)', ascending=False).reset_index(drop=True)


        '''
        #Catalyst vs PFR conversion
        plt.figure(figsize=(12, 5), dpi=300)
        plt.bar(df_result_sorted.iloc[:,0], df_result_sorted.iloc[:,1],color='black')
        for i, value in enumerate(df_result_sorted.iloc[:,1]):
            plt.text(i, value + 0, f'{value:.1f}', ha='center', va='bottom',fontsize=8)
        plt.axhline(y=conversion_hydrogen_eq, color='red', linestyle='--')
        plt.text(len(df_result_sorted.iloc[:,0])-1, conversion_hydrogen_eq, f'{conversion_hydrogen_eq:.1f}%', color='red', ha='right', va='bottom')
        plt.title(f'Fe \nTemperature: {T_C}°C, Pressure: {P_bar}bar, GHSV: {GHSV}L/h/kg',fontsize=14)
        plt.xlabel('Catalyst type',fontsize=12)
        plt.ylabel('H$_{2}$ conversion(%)',fontsize=12)
        plt.grid(True, axis='y')
        wd = os.getcwd()
        saving_path = wd+"/Guideline table/PFR_exp/{}_{}_{}_{}.png"
        save_file = saving_path.format('PFR', T_C, GHSV, 'Fe') 
        #plt.savefig(save_file)  
        plt.show()
        '''


        # save
        wd = os.getcwd()
        saving_path = wd+"/Guideline table/PFR_exp/{}_{}_{}_{}.csv" ##파일명 stage 숫자 바꾸기
        save_file = saving_path.format('PFR', T_C, GHSV, 'Fe') 
        df_result.to_csv(save_file, index=False)

