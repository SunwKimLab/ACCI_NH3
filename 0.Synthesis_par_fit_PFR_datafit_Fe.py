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
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'


#%% file load
df = pd.read_csv('synthesis catalyst experiment data Fe.csv',encoding='CP949')
experiment_data = df


#%% 
R = 8.314 # J mol−1 K−1
# reactor volume
cat_usage = 0.001 #kg #fix
void_fraction = 0.5
cat_density = 800 #kg/m3
reactor_volume = cat_usage / cat_density / void_fraction #m3

L_D_ratio = 10.8 #https://www.sciencedirect.com/science/article/pii/S1369703X24002249#fig0005
D = (4*reactor_volume/L_D_ratio/3.14)**(1/3)
L = L_D_ratio * D
        

#%%
rxn_rate_exp = experiment_data.iloc[:,11].to_numpy().reshape(-1,1)
n2_out_exp = experiment_data.iloc[:,15].to_numpy().reshape(-1,1)

#%%
par_1_fin_list= []
par_2_fin_list= []
par_3_fin_list= []
par_4_fin_list= []
par_5_fin_list= []
par_6_fin_list= []


r2_fin_list = []
mse_fin_list = []
rmse_fin_list = []
mae_fin_list = []

rxn_rate_aspen_fin_list = []

n2_out_aspen_fin_list = []
#%%
for i in range(0, len(df), 10):#10개씩 #len(df) i=10
#촉매 선택
#n=1


    print(int((i+10)/10),'th fitting start')
    
    tol_list = [1e-0,5e-1,1e-1,5e-2,1e-2,5e-3,1e-3,5e-4,1e-4,5e-5,1e-5,5e-6,1e-6] #tol =1e-0
    tol_percent_list = ['1%','0.9%','0.8%','0.7%','0.6%','0.5%','0.4%','0.3%','0.2%','0.1%'] #tol_percent ='0.5%'
    
    
    response_error = 1
    wait_time = 30
    
    while response_error == 1:
        try:
            #list setup
            par_1_list= []
            par_2_list= []
            par_3_list= []
            par_4_list= []
            par_5_list= []
            par_6_list= []

            r2_list = []
            mse_list = []
            rmse_list = []
            mae_list = []
            
            #for tol in tol_list:
            for tol_percent in tol_percent_list:
                #print('tol', tol)
                print('tol_percent', tol_percent)
                
                #link aspen file
                path = os.getcwd()
                file_path = '1. Aspen_file_PFR_fitting_datafit/Ammonia synthesis_PFR_fit.apw'
                link = win32.gencache.EnsureDispatch("Apwn.Document")
                link.InitFromArchive2(os.path.abspath(file_path))
                link.Visible = False
            
                rxn_rate_aspen_list = []
                n2_out_aspen_list = []
            
                
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
                
                
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#1/N2OUT\RESULT").Value = experiment_data.iloc[i,15] #mol/g/h
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#2/N2OUT\RESULT").Value = experiment_data.iloc[i+1,15] 
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#3/N2OUT\RESULT").Value = experiment_data.iloc[i+2,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#4/N2OUT\RESULT").Value = experiment_data.iloc[i+3,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#5/N2OUT\RESULT").Value = experiment_data.iloc[i+4,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#6/N2OUT\RESULT").Value = experiment_data.iloc[i+5,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#7/N2OUT\RESULT").Value = experiment_data.iloc[i+6,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#8/N2OUT\RESULT").Value = experiment_data.iloc[i+7,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#9/N2OUT\RESULT").Value = experiment_data.iloc[i+8,15] #
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#10/N2OUT\RESULT").Value = experiment_data.iloc[i+9,15] 

                
                link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Data-Set\RU\Input\VALUE\#0/N2OUT\RESULT").Value = str(tol_percent) #tol*np.std(experiment_data.iloc[i:i+10,15]) #standard deviation
                
                
                link.Tree.FindNode("/Data/Streams/H2N2/Input/TOTFLOW/MIXED").Value = experiment_data.iloc[i,5]/1000 # GHSV # L/h/g
                link.Tree.FindNode("/Data/Blocks/SYN/Input/PRES").Value = experiment_data.iloc[i,7] # P # atm
                
                link.Tree.FindNode("/Data/Blocks/SYN/Input/LENGTH").Value = L # PFR length # m
                link.Tree.FindNode("/Data/Blocks/SYN/Input/DIAM").Value = D # PFR diameter # m
                
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF1_A/1").Value = 0
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = 5.056
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = -4609
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_C/1").Value = 2.69
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_D/1").Value = 0.000127

                
                
                
                
                # run
                link.Engine.Run2()
                if not link.Engine.IsRunning:   
                    A_f = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/1").Value
                    Ea_f = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/2").Value 
                    C_ad2_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/3").Value 
                    C_ad2_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/4").Value 
                    C_ad3_A = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/5").Value 
                    C_ad3_B = link.Tree.FindNode("\Data\Model Analysis Tools\Data-Fit\Regression\DR-1\Output\ESTVALUE/6").Value 
            
                    
                    par_1_list.append(A_f)
                    par_2_list.append(Ea_f)
                    par_3_list.append(C_ad2_A)
                    par_4_list.append(C_ad2_B)
                    par_5_list.append(C_ad3_A)
                    par_6_list.append(C_ad3_B)

        
                    
                    
                if link is not None:
                    link.Close()
                else:
                    pass
                
                print(int((i+10)/10),'th fitting done')   
                
                print(int((i+10)/10),'th validation start')   
                
                # Validation
                path = os.getcwd()
                file_path = '1. Aspen_file_PFR_fitting_datafit/Ammonia synthesis_PFR_validation.apw'
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
                
                link.Tree.FindNode("/Data/Blocks/SYN/Input/LENGTH").Value = L # PFR length # m
                link.Tree.FindNode("/Data/Blocks/SYN/Input/DIAM").Value = D # PFR diameter # m
                
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF1_A/1").Value = 0
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = 5.056
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = -4609
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_C/1").Value = 2.69
                link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_D/1").Value = 0.000127
                
                
                for j in range(i, i+10, 1): #j=5
                
                    link.Tree.FindNode("/Data/Streams/H2N2/Input/TOTFLOW/MIXED").Value = experiment_data.iloc[j,5]/1000 # GHSV # L/hkg
                    link.Tree.FindNode("/Data/Streams/H2N2/Input/TEMP/MIXED").Value = 273.15 #K
                    link.Tree.FindNode("/Data/Blocks/SYN/Input/PRES").Value = experiment_data.iloc[j,7] # CSTR pressure # atm
                    link.Tree.FindNode("/Data/Blocks/SYN/Input/REAC_TEMP").Value = experiment_data.iloc[j,9] # CSTR Temperature # K

                    link.Engine.Run2()
                    
                    if not link.Engine.IsRunning:
                        n2_out_aspen = link.Tree.FindNode("/Data/Streams/NH3-1/Output/MOLEFLOW/MIXED/N2").Value*1000*3600 #kmol/s -> mol/h
                        n2_out_aspen_list.append(n2_out_aspen)
                        rxn_rate_aspen = 2*(experiment_data.iloc[j,5]/1000/4*0.0445896223 - n2_out_aspen)/1 #mol/g/h
                        rxn_rate_aspen_list.append(rxn_rate_aspen)
                        
                        
                if link is not None:
                    link.Close()
                else:
                    pass
            
                
                ### r2
                r2= r2_score(experiment_data.iloc[i:i+10,12], rxn_rate_aspen_list)
                r2_list.append(r2)
                mse= mean_squared_error(experiment_data.iloc[i:i+10,12], rxn_rate_aspen_list)
                mse_list.append(mse)
                rmse = np.sqrt(mse)
                rmse_list.append(rmse)
                mae = mean_absolute_error(experiment_data.iloc[i:i+10,12], rxn_rate_aspen_list)
                mae_list.append(mae)
                
                print(int((i+10)/10),'th r2:',r2) 
                print(int((i+10)/10),'th validation done')   
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
    C_ad2_B= par_4_list[r2_best_th] 
    C_ad3_A = par_5_list[r2_best_th]
    C_ad3_B = par_6_list[r2_best_th]


    
    #
    par_1_fin_list.append(A_f)
    par_2_fin_list.append(Ea_f)
    par_3_fin_list.append(C_ad2_A)
    par_4_fin_list.append(C_ad2_B)
    par_5_fin_list.append(C_ad3_A)
    par_6_fin_list.append(C_ad3_B)


    
    print(int((i+10)/10),'th validation start')   
    # Validation
    path = os.getcwd()
    file_path = '1. Aspen_file_PFR_fitting_datafit/Ammonia synthesis_PFR_validation.apw'
    link = win32.gencache.EnsureDispatch("Apwn.Document")
    link.InitFromArchive2(os.path.abspath(file_path))
    link.Visible = False
    
    
    # data input
    # data input
    #driving force
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= A_f # A_f = 100000
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = Ea_f #J/mol # Ea_f=100000
    
    #adsorption
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = C_ad2_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = C_ad2_B
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = C_ad3_A
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = C_ad3_B
    
    link.Tree.FindNode("/Data/Blocks/SYN/Input/LENGTH").Value = L # PFR length # m
    link.Tree.FindNode("/Data/Blocks/SYN/Input/DIAM").Value = D # PFR diameter # m
    
    
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF1_A/1").Value = 0
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = 5.056
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = -4609
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_C/1").Value = 2.69
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_D/1").Value = 0.000127
    
    
    for j in range(i, i+10, 1):
    
        link.Tree.FindNode("/Data/Streams/H2N2/Input/TOTFLOW/MIXED").Value = experiment_data.iloc[j,5]/1000 # GHSV # L/hkg
        link.Tree.FindNode("/Data/Streams/H2N2/Input/TEMP/MIXED").Value = 273.15 #K
        link.Tree.FindNode("/Data/Blocks/SYN/Input/PRES").Value = experiment_data.iloc[j,7] # CSTR pressure # atm
        link.Tree.FindNode("/Data/Blocks/SYN/Input/REAC_TEMP").Value = experiment_data.iloc[j,9] # CSTR Temperature # K
    
        link.Engine.Run2()
        
        if not link.Engine.IsRunning:
            n2_out_aspen = link.Tree.FindNode("/Data/Streams/NH3-1/Output/MOLEFLOW/MIXED/N2").Value*1000*3600 #kmol/s -> mol/h
            n2_out_aspen_fin_list.append(n2_out_aspen)
            rxn_rate_aspen = 2*(experiment_data.iloc[j,5]/1000/4*0.0445896223 - n2_out_aspen)/1 #mol/g/h
            rxn_rate_aspen_fin_list.append(rxn_rate_aspen)
    
    if link is not None:
        link.Close()
    else:
        pass
    
    
    ### Plot
    T = df.iloc[i:i+10,9].to_numpy().reshape(-1,1)
    r_syn_exp = df.iloc[i:i+10,12].to_numpy().reshape(-1,1)
    fig, ax = plt.subplots(dpi=300, figsize=[7, 5.5])
    
    #exp
    ax.plot(T, r_syn_exp, 'o', markersize = 9, alpha = 0.6, mfc = 'b',
            mec = 'k', markeredgewidth =1.5, label='Exp data')
    
    #cal
    r_syn_sim= rxn_rate_aspen_fin_list[i:i+10]
    ax.plot(T, r_syn_sim, linewidth = 2.1, label='Fitting data')
    
    title_row = df.iloc[i]
    title = f"{title_row['Catalyst']}({title_row['Doping wt%']}%)/{title_row['Support(Promoter)']}"
    plt.title(title,size=15)
    
    plt.grid(linestyle = '--')
    plt.xlabel("Temperature (K)", fontsize=12)
    plt.ylabel("NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$)", fontsize=12)
    plt.legend()
    filename = f"\{title_row['Number']}.{title_row['Catalyst']}({title_row['Doping wt%']}%)_{title_row['Support(Promoter)']}.png"
    wd = os.getcwd()
    saving_path = wd+"\par_fit_figure\Fe"
    full_path = saving_path + filename
    plt.savefig(full_path)  
    plt.show()
    
    ### r2
    r2= r2_score(experiment_data.iloc[i:i+10,12], rxn_rate_aspen_fin_list[i:i+10])
    r2_fin_list.append(r2)
    mse= mean_squared_error(experiment_data.iloc[i:i+10,12], rxn_rate_aspen_fin_list[i:i+10])
    mse_fin_list.append(mse)
    rmse = np.sqrt(mse)
    rmse_fin_list.append(rmse)
    mae = mean_absolute_error(experiment_data.iloc[i:i+10,12], rxn_rate_aspen_fin_list[i:i+10])
    mae_fin_list.append(mae)
    
    print(int((i+10)/10),'th r2:',r2) 
    print(int((i+10)/10),'th validation done')   
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
})], ignore_index=True)

###data 저장
#par
par_df.to_csv('synthesis LHHW aspen parameter Fe.csv', index=False)  
#rxn_rate_simulation
with open('synthesis rxn rate aspen Fe.csv', 'w', newline='') as file:
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

par_converted_df = pd.concat([pd.DataFrame({
    'A_f': A_f_fin_list,
    'Ea_f(J/mol)': Ea_f_fin_list,
    'A_1': A_1_fin_list,
    'Ea_1(J/mol)': Ea_1_fin_list,
    'A_2': A_2_fin_list,
    'Ea_2(J/mol)': Ea_2_fin_list,
})], ignore_index=True)

par_converted_df.to_csv('synthesis LHHW parameter Fe.csv', index=False)  

#%%
ex = experiment_data.iloc[:,12]
cal = rxn_rate_aspen_fin_list 

# Plot
plt.figure(figsize=(7, 5.5), dpi=300)
plt.scatter(ex, cal,c='blue',edgecolor='blue')
x=np.linspace(min(experiment_data.iloc[:,12]),max(experiment_data.iloc[:,12]),100)
y=x
plt.plot(x,y,c='red')
plt.title('NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$) (Fe)',fontsize=17)
plt.xlabel('Experimental data',fontsize=17)
plt.ylabel('Fitting data',fontsize=17)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.grid(linestyle = '--')
wd = os.getcwd()
saving_path = wd+"\par_fit_figure/Fe/Parity plot (Fe)"
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
error_df.to_csv('synthesis rxn rate error Fe.csv', index=False) 


#%%







#%% 

df_rxn_rate_aspen_Fe = pd.read_csv('synthesis rxn rate aspen Fe.csv',encoding='CP949',header=None)

df_rxn_rate_aspen_Ru = pd.read_csv('synthesis rxn rate aspen Ru.csv',encoding='CP949',header=None)


df_experimental_data_Fe = pd.read_csv('synthesis catalyst experiment data Fe.csv',encoding='CP949')
df_experimental_data_Ru = pd.read_csv('synthesis catalyst experiment data Ru.csv',encoding='CP949')

df_catalyst_name_Fe = pd.read_csv('synthesis catalyst name Fe_2.csv',encoding='CP949')
df_catalyst_name_Ru = pd.read_csv('synthesis catalyst name Ru_2.csv',encoding='CP949')


#%% i=10
for i in range(0, len(df_rxn_rate_aspen_Fe), 10): # i = 0
    ### Plot
    T = df_experimental_data_Fe.iloc[i:i+10,8].to_numpy().reshape(-1,1)
    r_syn_exp = df_experimental_data_Fe.iloc[i:i+10,12].to_numpy().reshape(-1,1)
    fig, ax = plt.subplots(dpi=300, figsize=[7, 5.5])
    
    #exp
    ax.plot(T, r_syn_exp, 'o', markersize = 9, alpha = 0.6, mfc = 'b',
            mec = 'k', markeredgewidth =1.5, label='Experimental data')
    
    #cal
    r_syn_sim= df_rxn_rate_aspen_Fe.iloc[i:i+10,0]
    ax.plot(T, r_syn_sim, linewidth = 2.1, label='Fitted data')
    
    title_row = df_catalyst_name_Fe.iloc[int(i/10),0]
    title = f"{title_row}"
    plt.title(title,size=17)
    
    plt.grid(linestyle = '--')
    plt.xlabel("Temperature ($^\circ$C)", fontsize=17)
    plt.ylabel("NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$)", fontsize=17)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend(fontsize=15)
    
    number = int(i / 10) + 1
    filename = f"\{number}.png"
    
    plt.tight_layout()
    
    wd = os.getcwd()
    saving_path = wd+"\par_fit_figure\Fe"
    full_path = saving_path + filename
    plt.savefig(full_path) 
    
    plt.show()


#%%
for i in range(0, len(df_rxn_rate_aspen_Ru), 10):
    ### Plot
    T = df_experimental_data_Ru.iloc[i:i+10,8].to_numpy().reshape(-1,1)
    r_syn_exp = df_experimental_data_Ru.iloc[i:i+10,12].to_numpy().reshape(-1,1)
    fig, ax = plt.subplots(dpi=300, figsize=[7, 5.5])
    
    #exp
    ax.plot(T, r_syn_exp, 'o', markersize = 9, alpha = 0.6, mfc = 'b',
            mec = 'k', markeredgewidth =1.5, label='Experimental data')
    
    #cal
    r_syn_sim= df_rxn_rate_aspen_Ru.iloc[i:i+10,0]
    ax.plot(T, r_syn_sim, linewidth = 2.1, label='Fitted data')
    
    title_row = df_catalyst_name_Ru.iloc[int(i/10),0]
    title = f"{title_row}"
    plt.title(title,size=17)
    
    plt.grid(linestyle = '--')
    plt.xlabel("Temperature ($^\circ$C)", fontsize=17)
    plt.ylabel("NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$)", fontsize=17)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend(fontsize=15)
    
    number = int(i / 10) + 1
    filename = f"\{number}.png"
    
    plt.tight_layout()

    wd = os.getcwd()
    saving_path = wd+"\par_fit_figure\Ru"
    full_path = saving_path + filename
    plt.savefig(full_path)  
    plt.show()
#%% parity plot

combined_experiment_data = pd.concat([df_experimental_data_Fe, df_experimental_data_Ru], ignore_index=True)
combined_cal = pd.concat([df_rxn_rate_aspen_Fe, df_rxn_rate_aspen_Ru], ignore_index=True)

#r2
r2_overall= r2_score(combined_experiment_data.iloc[:,12], combined_cal)
print('Overall r2:',r2_overall)

# Plot
plt.figure(figsize=(7, 5.5), dpi=300)
plt.scatter(combined_experiment_data.iloc[:,12], combined_cal,c='orange',edgecolor='orange')
x=np.linspace(min(combined_experiment_data.iloc[:,12]),max(combined_experiment_data.iloc[:,12]),100)
y=x
plt.plot(x,y,c='blue')
plt.text(0, 0.085, f'R$^2$ = {r2_overall:.3f}', color='black', fontsize=20, weight='bold')

plt.title('NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$)',fontsize=20)
plt.xlabel('Experimental data',fontsize=20)
plt.ylabel('Fitted data',fontsize=20)
plt.grid(linestyle = '--')
plt.tick_params(axis='both', which='major', labelsize=17)

plt.tight_layout()

wd = os.getcwd()
saving_path = wd+"\par_fit_figure\Synthesis Parity plot"
plt.savefig(saving_path)  
plt.show()



#%% org scale

# X축 데이터 (실험 데이터)
x_data_Fe = df_experimental_data_Fe.iloc[:, 8]
x_data_Ru = df_experimental_data_Ru.iloc[:, 8]

y_exp_Fe = df_experimental_data_Fe.iloc[:, 12]
y_exp_Ru = df_experimental_data_Ru.iloc[:, 12]

y_cal_Fe = df_rxn_rate_aspen_Fe
y_cal_Ru = df_rxn_rate_aspen_Ru


# Fe 그래프
fig, ax = plt.subplots(dpi=300, figsize=(7, 5.5))

# Fe 계산 데이터 (선)
for i in range(0, len(y_cal_Fe), 10):
    x_segment = x_data_Fe.iloc[i:i+10]  # X축 데이터 10개
    y_segment = y_cal_Fe[i:i+10]       # Y축 데이터 10개
    ax.plot(x_segment, y_segment, color='orange', linewidth=1.0, linestyle='--', label='Fitted data' if i == 0 else "")  # 범례 중복 방지

# Fe 실험 데이터 (스캐터)
ax.scatter(
    x_data_Fe, y_exp_Fe, s=30, alpha=0.6, c='blue', edgecolor='k',
    linewidth=1.5, label='Experimental data'
)

# Fe 그래프 스타일링
ax.set_xlabel("Temperature (°C)", fontsize=20)
#ax.set_ylabel(r"$\sqrt{\mathrm{NH_3\ production\ rate\ (mol\ g^{-1}\ h^{-1})}}$", fontsize=35)
ax.set_ylabel('NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$)', fontsize=20)
ax.legend(fontsize=20)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
ax.grid(linestyle='--', alpha=0.7)
ax.set_title("Fe-based", fontsize=20)
plt.tight_layout()
wd = os.getcwd()
saving_path = wd+"\par_fit_figure\Synthesis_Fe T vs rate (org scale)"
plt.savefig(saving_path)  
# Fe 그래프 출력
plt.show()
#%%

# Ru 그래프
fig, ax = plt.subplots(dpi=300, figsize=(7, 5.5))

# Ru 계산 데이터 (선)
for i in range(0, len(y_cal_Ru), 10):
    x_segment = x_data_Ru.iloc[i:i+10]  # X축 데이터 10개
    y_segment = y_cal_Ru[i:i+10]       # Y축 데이터 10개
    ax.plot(x_segment, y_segment, color='orange', linewidth=1.0, linestyle='--', label='Fitted data' if i == 0 else "")  # 범례 중복 방지

# Ru 실험 데이터 (스캐터)
ax.scatter(
    x_data_Ru, y_exp_Ru, s=30, alpha=0.6, c='blue', edgecolor='k',
    linewidth=1.5, label='Experimental data'
)

# Ru 그래프 스타일링
ax.set_xlabel("Temperature (°C)", fontsize=20)
#ax.set_ylabel(r"$\sqrt{\mathrm{NH_3\ production\ rate\ (mol\ g^{-1}\ h^{-1})}}$", fontsize=35)
ax.set_ylabel('NH$_{3}$ production rate (mol g$^{-1}$ h$^{-1}$)', fontsize=20)
ax.legend(fontsize=20)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
ax.grid(linestyle='--', alpha=0.7)
ax.set_title("Ru-based", fontsize=20)
plt.tight_layout()
wd = os.getcwd()
saving_path = wd+"\par_fit_figure\Synthesis_Ru T vs rate (org scale)"
plt.savefig(saving_path)  
# Ru 그래프 출력
plt.show()
