import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import win32com.client as win32
import os
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
from Economic_NH3 import *
#%% file load
parameter_data_dec_Ni = pd.read_csv('decomposition LHHW aspen parameter Ni.csv',encoding='CP949')

#%%
def sim_NH3_dec_Ni(link, ammonia_cost, d_km, cat_idx, T_C, P_bar, GHSV,
                   elec_cost, cooling_water_cost, catalyst_cost_Ni, ads_cost, NOxtreat_cost, BlueNH3_cost):
    i = cat_idx

    vol_flowrate = 5000*1e3 # #5866997*1.145 #L/h   #elec 500 kW # 1000 kW급 #An efficient process for sustainable and scalable hydrogen production from green ammonia 
    R = 8.314 # J mol−1 K−1

    cat_usage = vol_flowrate / GHSV
    void_fraction = 0.5
    cat_density = 800 #kg/m3
    reactor_volume = cat_usage / cat_density / void_fraction #m3
    L_D_ratio = 5.9 
    bed_count = 8
    D = (4*reactor_volume/bed_count/L_D_ratio/3.14)**(1/3)
    L_each = L_D_ratio * D
    L = bed_count*L_each

    #calculated
    T_K = T_C + 273.15 #°C->K
    P_atm = P_bar * 0.9869 # bar->atm


    # data input
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = -51
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = 13026

    #driving force
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= parameter_data_dec_Ni.iloc[i,0]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = parameter_data_dec_Ni.iloc[i,1]
    

    #adsorption
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = parameter_data_dec_Ni.iloc[i,2]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = parameter_data_dec_Ni.iloc[i,3]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = parameter_data_dec_Ni.iloc[i,4]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = parameter_data_dec_Ni.iloc[i,5]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/4").Value = parameter_data_dec_Ni.iloc[i,6]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/4").Value = parameter_data_dec_Ni.iloc[i,7]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/5").Value = parameter_data_dec_Ni.iloc[i,8]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/5").Value = parameter_data_dec_Ni.iloc[i,9]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/6").Value = parameter_data_dec_Ni.iloc[i,10]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/6").Value = parameter_data_dec_Ni.iloc[i,11]

    
    
    #Set operating condition
    link.Tree.FindNode("/Data/Blocks/COMP/Input/PRES").Value = P_atm
    link.Tree.FindNode("/Data/Streams/NH3/Input/TOTFLOW/MIXED").Value = vol_flowrate #L/h
    
    #Set reactor operating condition
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/FEED").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/FEED").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-2").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-2").Value = T_K # PFR Temperature # K    
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-4").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-4").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-6").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-6").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-8").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-8").Value = T_K # PFR Temperature # K    
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-10").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-10").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-12").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-12").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/PRES/NH3-14").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/MHEX/Input/VALUE/NH3-14").Value = T_K # PFR Temperature # K    
    
    
    
    
    link.Tree.FindNode("/Data/Blocks/DEC1/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC1/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC2/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC2/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC3/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC3/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC4/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC4/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC5/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC5/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC6/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC6/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC7/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC7/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/DEC8/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/DEC8/Input/DIAM").Value = D # PFR diameter # m
    
    link.Tree.FindNode("/Data/Blocks/DEC1/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC2/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC3/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC4/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC5/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC6/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC7/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/DEC8/Input/PRES").Value = P_atm # PFR pressure # atm
    
    
    #Set 2nd compressor condition
    PSA_pressure = 8 #bar
    link.Tree.FindNode("/Data/Blocks/COMP2/Input/PRES").Value = PSA_pressure* 0.9869 # bar->atm # PSA pressure # atm
    
    #Cooler
    link.Tree.FindNode("/Data/Blocks/COOLER/Input/PRES").Value = PSA_pressure* 0.9869 # bar->atm # PSA pressure # atm
    link.Tree.FindNode("/Data/Blocks/COOLER/Input/TEMP").Value = 40
    
    
    #Set NH3 sep condition (T=40C constant)
    link.Tree.FindNode("/Data/Blocks/PSANH3/Input/PRES1").Value = PSA_pressure* 0.9869 # bar->atm # PSA pressure # atm
    link.Tree.FindNode("/Data/Blocks/PSANH3/Input/PRES/NH3-REC").Value = PSA_pressure* 0.9869 # bar->atm # PSA pressure # atm
    link.Tree.FindNode("/Data/Blocks/PSANH3/Input/PRES/PSA-IN").Value = PSA_pressure* 0.9869 # bar->atm # PSA pressure # atm
    
    
    #PSA (T=40C constant)
    link.Tree.FindNode("/Data/Blocks/PSAH2/Input/PRES1").Value = PSA_pressure* 0.9869 # bar->atm # PSA pressure # atm
    PSA_recovery = 0.9 # 0.9
    PSA_purity = 0.999
    N2_fraction_ratio = (PSA_recovery * (3/4)) / ((1/4) * (PSA_purity*100 / (100-PSA_purity*100)))
    link.Tree.FindNode("/Data/Blocks/PSAH2/Input/FRACS/PSA-H2/MIXED\H2").Value = PSA_recovery
    link.Tree.FindNode("/Data/Blocks/PSAH2/Input/FRACS/PSA-H2/MIXED/N2").Value = N2_fraction_ratio
    
    link.Engine.Run2()
    
    if not link.Engine.IsRunning:
        ### fuel calculation ###
        # required heat in reactors #
        Q_required = abs(link.Tree.FindNode("\Data\Streams\HEATOUT\Output\QCALC").Value) # W
        # print('Q_required',Q_required)
        # LHV #
        H_comb_H2 = 241800 # kJ/kmol #lhv
        H_comb_NH3 = 316800 # kJ/kmol #lhv

        # heat calculation #
        NH3_in_tail = link.Tree.FindNode("/Data/Streams/NH3-REC/Output/MOLEFLOW/MIXED/NH3").Value*1e3 #mol/sec
        H2_in_tail = link.Tree.FindNode("/Data/Streams/PSA-N2/Output/MOLEFLOW/MIXED/NH3").Value*1e3 #mol/sec
        Q_generated_NH3_in_tail = H_comb_NH3 * NH3_in_tail # W
        Q_generated_H2_in_tail = H_comb_H2 * H2_in_tail # W
        
        if (Q_generated_NH3_in_tail + Q_generated_H2_in_tail) > Q_required:
            # additional NH3 fuel #
            NH3_fuel_additional = 0
            link.Tree.FindNode("/Data/Streams/NH3-FUEL/Input/TOTFLOW/MIXED").Value = NH3_fuel_additional # kmol/sec
            # O2 input #
            O2_moleflow = (0.5*H2_in_tail + 0.75*NH3_in_tail)/1e3 # kmol/sec
            link.Tree.FindNode("/Data/Streams/O2/Input/TOTFLOW/MIXED").Value = O2_moleflow # kmol/sec
            # NOx emission #
            NOx_flowrate = (link.Tree.FindNode("/Data/Streams/FUEL/Output/MASSFLOW/MIXED/NO").Value + link.Tree.FindNode("/Data/Streams/FUEL/Output/MASSFLOW/MIXED/NO2").Value)*60*60*8500 # kg/s to kg/yr
        else:
            # additional NH3 fuel #
            NH3_fuel_additional = (Q_required -(Q_generated_NH3_in_tail + Q_generated_H2_in_tail)) / H_comb_NH3 # mol/sec
            link.Tree.FindNode("/Data/Streams/NH3-FUEL/Input/TOTFLOW/MIXED").Value = NH3_fuel_additional/1e3 # kmol/sec
            # O2 input #
            O2_moleflow = (0.5*H2_in_tail + 0.75*(NH3_in_tail + NH3_fuel_additional))/1e3 # kmol/sec
            link.Tree.FindNode("/Data/Streams/O2/Input/TOTFLOW/MIXED").Value = O2_moleflow # kmol/sec
            # NOx emission #
            NOx_flowrate = (link.Tree.FindNode("/Data/Streams/FUEL/Output/MASSFLOW/MIXED/NO").Value + link.Tree.FindNode("/Data/Streams/FUEL/Output/MASSFLOW/MIXED/NO2").Value)*60*60*8500 # kg/s to kg/yr
        print('NH3_fuel_additional',NH3_fuel_additional)
        # print('O2_moleflow',O2_moleflow)
        # print('NOx_flowrate',NOx_flowrate)


        link.Engine.Run2()

        
        if not link.Engine.IsRunning:
            initial_ammonia = link.Tree.FindNode("/Data/Streams/NH3/Output/MOLEFLOW/MIXED/NH3").Value #mole
            remained_ammonia = link.Tree.FindNode("/Data/Streams/H2N2/Output/MOLEFLOW/MIXED/NH3").Value #mole
            conversion_ammonia_overall = (initial_ammonia-remained_ammonia)/initial_ammonia * 100 #%
    
                    
            ##CAPEX#
            # COMP: compressor
            if P_atm <= 1:
                Q_COMP = 0
            else:  
                Q_COMP = abs(link.Tree.FindNode("/Data/Blocks/COMP/Output/POWER_ISEN").Value) / 1000 #W to kW
            # BURNER: furnace
            # Q_BURNER = abs(link.Tree.FindNode("/Data/Blocks/MHEX/Output/QCALC2").Value) / 1000 #W to kW
            Q_BURNER = Q_required / 1000 #W to kW
            # MHEX: heat exchanger
            # Q_MHEX = abs(link.Tree.FindNode("/Data/Blocks/MHEX/Output/QCALC2").Value) #W
            Q_MHEX = Q_required #W
            # Delta_T_MHEX = abs(link.Tree.FindNode("/Data/Streams/FUEL/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/FLUE/Output/TEMP_OUT/MIXED").Value)
            Delta_T_MHEX = abs(link.Tree.FindNode("/Data/Streams/FUEL/Output/TEMP_OUT/MIXED").Value - T_K)

            # DEC: pbr
            L = L_each
            D = D
            # COMP2: compressor
            if P_bar >= PSA_pressure: #bar
                Q_COMP2 = 0
            else:
                Q_COMP2 = abs(link.Tree.FindNode("/Data/Blocks/COMP2/Output/POWER_ISEN").Value) / 1000 #W to kW
            # COOL: cooler
            Q_COOL = abs(link.Tree.FindNode("/Data/Blocks/COOLER/Output/QCALC").Value) #W
            Delta_T_COOL = abs(link.Tree.FindNode("/Data/Streams/H2N2-1/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/H2N2-2/Output/TEMP_OUT/MIXED").Value)
            # PSA: NH3sep
            V_NH3SEP = link.Tree.FindNode("\Data\Streams/H2N2-2/Output/VOLFLMX/MIXED").Value #L/h 
            #GHSV_NH3SEP = 400 # h-1 to s-1 #Two-train elevated-temperature pressure swing adsorption for high-purity hydrogen production
            n_bed_PSA = 2
            cycle_time_PSA = 180 #s
            V_NH3SEP = V_NH3SEP/3600 * cycle_time_PSA/1e3 # / GHSV_NH3SEP /1e3 #L -> m3
            # PSA: N2sep
            n_bed_PSA = 2
            cycle_time_PSA = 180 #s 180
            V_PSA = link.Tree.FindNode("\Data\Streams/PSA-IN/Output/VOLFLMX/MIXED").Value #L/h 
            #GHSV_PSA = 400 # h-1 to s-1 #Two-train elevated-temperature pressure swing adsorption for high-purity hydrogen production
            V_PSA = V_PSA/3600 * cycle_time_PSA/1e3 #/ GHSV_PSA /1e3 #L -> m3               
            
            
            #Bare module cost
            C_BM_COMP, C_BM_COMP_O = Capex.compressor(Q_COMP)
            C_BM_BURNER, C_BM_BURNER_O = Capex.furnace(Q_BURNER)
            C_BM_MHEX, C_BM_MHEX_O = Capex.heatexchanger_heat(Q_MHEX, Delta_T_MHEX)
            C_BM_DEC, C_BM_DEC_O = Capex.pbr(L,D)
            C_BM_NH3SEP, C_BM_NH3SEP_O = Capex.packedtower(V_NH3SEP)
            C_BM_PSA, C_BM_PSA_O = Capex.packedtower(V_PSA)
            C_BM_COMP2, C_BM_COMP2_O = Capex.compressor(Q_COMP2)
            C_BM_COOL, C_BM_COOL_O = Capex.cooler(Q_COOL, Delta_T_COOL)
       
            C_BM = C_BM_DEC*8 + C_BM_COMP + C_BM_BURNER + C_BM_MHEX + C_BM_NH3SEP*n_bed_PSA + C_BM_PSA*n_bed_PSA + C_BM_COMP2 + C_BM_COOL
            C_BM_O = C_BM_DEC_O*8 + C_BM_COMP_O + C_BM_BURNER_O + C_BM_MHEX_O + C_BM_NH3SEP_O*n_bed_PSA + C_BM_PSA_O*n_bed_PSA + C_BM_COMP2_O + C_BM_COOL_O
            CAPEX = (1.18*C_BM + 0.5*C_BM_O) * 800.8/397 #Cepci 2023/2001
            
            
            
            CAPEX_comp = (1.18*C_BM_COMP + 0.5*C_BM_COMP_O) * 800.8/397 + (1.18*C_BM_COMP2 + 0.5*C_BM_COMP2_O) * 800.8/397 
            CAPEX_furnace = (1.18*C_BM_BURNER + 0.5*C_BM_BURNER_O) * 800.8/397 
            CAPEX_mhex = (1.18*C_BM_MHEX + 0.5*C_BM_MHEX_O) * 800.8/397 
            CAPEX_reactor = (1.18*C_BM_DEC*8 + 0.5*C_BM_DEC_O*8) * 800.8/397 
            CAPEX_separator = (1.18*C_BM_NH3SEP + 0.5*C_BM_NH3SEP_O) * 800.8/397*n_bed_PSA + (1.18*C_BM_PSA + 0.5*C_BM_PSA_O) * 800.8/397 *n_bed_PSA
            CAPEX_cooler = (1.18*C_BM_COOL + 0.5*C_BM_COOL_O) * 800.8/397 
    
    
            
    
            
            ### OPEX ###
            elec_use_COMP = abs(link.Tree.FindNode("/Data/Blocks/COMP/Output/POWER_ISEN").Value*0.001*8500) #W to kWh
            elec_use_COMP2 = Q_COMP2*8500 #kW to kWh
            cool_use_COOLER = abs(link.Tree.FindNode("/Data/Blocks/COOLER/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
            catalyst_use_DEC = cat_usage #kg
            catalyst_use = catalyst_use_DEC #kg
            catalyst_use_dec_total = cat_usage #kg
            ammonia_use = (link.Tree.FindNode("/Data/Streams/NH3/Output/MASSFLOW/MIXED/NH3").Value)*60*60*8500 #kg/sec to kg/yr 
            ammonia_fuel_use = NH3_fuel_additional*17/1e3*60*60*8500  #  mol/s to kg/yr
            ammonia_SEP = link.Tree.FindNode("/Data/Streams/NH3-REC/Output/MOLEFLOW/MIXED/NH3").Value*1000*60*60 #kmol/sec to mol/h
            nitrogen_PSA = link.Tree.FindNode("/Data/Streams/PSA-N2/Output/MOLEFLOW/MIXED/N2").Value*1000*60*60 #kmol/sec to mol/h
            O2_use = O2_moleflow * 32*60*60*8500 # kmol/s to kg/yr
            
            
            Np = 0 #NP: the handling particles equipment
            Nnp = 14 #Nnp: the handling non-particles equipment
            
            #Opex
            elec_use_total = elec_use_COMP + elec_use_COMP2
            O_elec = Opex.elec(elec_use_total, elec_cost=elec_cost)
            O_cool = Opex.cool(cool_use_COOLER, cooling_water_cost=cooling_water_cost)
            O_cat_Ni = Opex.cataylst_Ni(catalyst_use, catalyst_cost_Ni=catalyst_cost_Ni)
            
    
            #ammonia_cost = 0.7764829369
            O_ammonia = ammonia_use * ammonia_cost
            O_ammonia_fuel = Opex.BlueNH3(ammonia_fuel_use, BlueNH3_cost = BlueNH3_cost) # blue NH3 assumed
            O_NH3adsorbent = Opex.NH3adsorbent(ammonia_SEP, ads_cost=ads_cost)/2
            O_N2adsorbent = Opex.N2adsorbent(nitrogen_PSA, ads_cost=ads_cost)/2
            O_labor = Opex.labor(Np, Nnp)
            O_main = Opex.maintenence(CAPEX)
            O_transport = Opex.transport(ammonia_use/8500, d_km) * 8500
            # O_O2 = Opex.O2(O2_use, O2_cost = O2_cost)
            O_NOxtreat = Opex.NOxTreat(NOx_flowrate, NOxTreat_cost=NOxtreat_cost)
            
            OPEX = O_elec + O_cat_Ni + O_ammonia + O_NH3adsorbent + O_N2adsorbent + O_labor + O_main + O_transport + O_cool + O_NOxtreat + O_ammonia_fuel
            OPEX_catO = O_elec + O_cat_Ni + O_ammonia + O_NH3adsorbent + O_N2adsorbent + O_labor + O_main + O_transport + O_cool + O_NOxtreat + O_ammonia_fuel
            OPEX_catX = O_elec + O_ammonia + O_NH3adsorbent + O_N2adsorbent + O_labor + O_main + O_transport + O_cool + O_NOxtreat + O_ammonia_fuel
            
            
            
            
            
            ### LCOH ###
            r = 0.07 # %/100
            n = 25 # years
            CRF = r*(1+r)**n / ((1+r)**n - 1)
            if (link.Tree.FindNode("/Data/Streams/PSA-H2/Output/MASSFLOW/MIXED/H2").Value - link.Tree.FindNode("/Data/Streams/NH3/Output/MASSFLOW/MIXED/H2").Value)*60*60*8500 < 0:
                m_produced_H2 = 1e-1
            else:
                m_produced_H2 = (link.Tree.FindNode("/Data/Streams/PSA-H2/Output/MASSFLOW/MIXED/H2").Value - link.Tree.FindNode("/Data/Streams/NH3/Output/MASSFLOW/MIXED/H2").Value)*60*60*8500 #kg/sec ro kg/yr
            LCOH_catX = (CAPEX*CRF + OPEX_catX) / m_produced_H2 
            LCOH_catO = (CAPEX*CRF + OPEX_catO) / m_produced_H2  
            
            
            
            # energy
            elec_use_kWh = elec_use_total
            heat_use_kWh = Q_MHEX*8500/1000
            SEC_heatO = (elec_use_kWh + heat_use_kWh) / m_produced_H2 #kWh/kg H2
            SEC_heatX = (elec_use_kWh) / m_produced_H2 #kWh/kg
    
            
            
                    
            #### LCA ####
            #CO2 emission facor#
            # CO2_factor_CO2 = 1 #kgCO2/kgCO2
            # CO2_factor_CH4 = 27 #kgCO2/kgCH4
            CO2_factor_shipfuel = 0.013 # 0.09 #kgCO2/tonNH3/km
            CO2_factor_elec = 0.3 #kgCO2/kWh
            CO2_factor_catalyst = 5.5 #kgCO2/kgCat
            CO2_factor_adsorbent = 1.61 #kgCO2/kgzeolite
            CO2_factor_ammonia = 0.358578061425712 # kgCO2/kgNH3 #합성에서 도출 
            CO2_factor_BlueNH3 = 1.09 #1.9 #  https://pubs.acs.org/doi/10.1021/acs.energyfuels.5c03111
            CO2_factor_cooling_water = 16.29 #70.1 #kgCO2/GJ
    
    
    
            #amount#
            ammonia_usage = ammonia_use # kg/yr
            shipfuel_usage = (ammonia_use /1000) * d_km # ton/yr*km
            elec_usage = elec_use_total  #kWh #fitting
            catalyst_usage = cat_usage #kg
            adsorbent_usage = ammonia_SEP* 0.333/2 + nitrogen_PSA/1.79/2
            cool_usage = cool_use_COOLER # GJ/yr
            
            #Calculation
            CO2_emission_shipfuel = CO2_factor_shipfuel * shipfuel_usage
            CO2_emission_ammonia = CO2_factor_ammonia * ammonia_usage
            CO2_emission_elec = CO2_factor_elec * elec_usage
            CO2_emission_catalyst = CO2_factor_catalyst * catalyst_usage
            CO2_emission_adsorbent = CO2_factor_adsorbent * adsorbent_usage
            CO2_emission_cool = CO2_factor_cooling_water * cool_usage
            CO2_emission_BlueNH3 = CO2_factor_BlueNH3 * ammonia_fuel_use
            
            CO2_emission_sum = CO2_emission_shipfuel + CO2_emission_ammonia + CO2_emission_elec + CO2_emission_catalyst + CO2_emission_adsorbent + CO2_emission_cool + CO2_emission_BlueNH3
            CO2_emission_levelized = CO2_emission_sum/m_produced_H2
            
            CO2_emission_shipfuel_levelized = CO2_emission_shipfuel/m_produced_H2
            CO2_emission_ammonia_levelized = CO2_emission_ammonia/m_produced_H2
            CO2_emission_elec_levelized = CO2_emission_elec/m_produced_H2
            CO2_emission_catalyst_levelized = CO2_emission_catalyst/m_produced_H2
            CO2_emission_adsorbent_levelized = CO2_emission_adsorbent/m_produced_H2
            CO2_emission_cool_levelized = CO2_emission_cool/m_produced_H2
            CO2_emission_BlueNH3_levelized = CO2_emission_BlueNH3/m_produced_H2

            
            print('NH3 conversion(%):', conversion_ammonia_overall)
            print('H2 production(kg/yr):', m_produced_H2)
            print('LCOH_catX($/kg):',LCOH_catX)
            print('LCOH_catO($/kg):',LCOH_catO)
            print('SEC(kWh/kg):',SEC_heatX)
            print('CO2(CO2/kg):',CO2_emission_levelized)
            print('-------------')

        
    results = {
    "Cat_info": {
        "idx": cat_idx},
    
    "condition": {
        "T (cel)": T_C,
        "P (bar)": P_bar,
        "GHSV (L/h/kg)": GHSV,
        },    
        
    "CAPEX": {
        "total": CAPEX,
        "CAPEX_comp": CAPEX_comp,
        "CAPEX_furnace": CAPEX_furnace,
        "CAPEX_mhex": CAPEX_mhex,
        "CAPEX_mhex": CAPEX_mhex,
        "CAPEX_reactor": CAPEX_reactor,
        "CAPEX_cooler": CAPEX_cooler,
        "CAPEX_separator": CAPEX_separator
    },
    
    
    
    "OPEX": {
        "catalyst_use_dec_total (kg)": catalyst_use_dec_total,
        "O_elec": O_elec,
        "O_cat": O_cat_Ni,
        "O_ammonia": O_ammonia,
        "O_adsorbent": O_NH3adsorbent + O_N2adsorbent,
        "O_NH3_fuel": O_ammonia_fuel,
        "O_labor": O_labor,
        "O_main": O_main,
        "O_transport": O_transport,
        "O_cool": O_cool,
        "O_NOxtreat": O_NOxtreat,
        "OPEX_catO": OPEX_catO,
        "OPEX_catX": OPEX_catX
    },
    
    
    "LCOH": {
        "LCOH_catO": LCOH_catO,
        "LCOH_catX": LCOH_catX
    },
    
    
    "SEC": {
        "elec_use_levelized": elec_use_kWh/m_produced_H2,
        "heat_use_levelized": heat_use_kWh/m_produced_H2,
        "SEC_heatO": SEC_heatO,
        "SEC_heatX": SEC_heatX
    },
    
    
    "CO2_emission": {
        "CO2_emission_shipfuel_levelized": CO2_emission_shipfuel_levelized,
        "CO2_emission_ammonia_levelized": CO2_emission_ammonia_levelized,
        "CO2_emission_elec_levelized": CO2_emission_elec_levelized,
        "CO2_emission_catalyst_levelized": CO2_emission_catalyst_levelized,
        "CO2_emission_adsorbent_levelized": CO2_emission_adsorbent_levelized,
        "CO2_emission_cool_levelized": CO2_emission_cool_levelized,
        "CO2_emission_BlueNH3_levelized": CO2_emission_BlueNH3_levelized,
        "CO2_emission_levelized": CO2_emission_levelized
    },
    
    "Performance": {
        "m_produced_H2 (kg/yr)": m_produced_H2,
        "conversion_ammonia_overall (%)": conversion_ammonia_overall,
    }
}
    
    return results
