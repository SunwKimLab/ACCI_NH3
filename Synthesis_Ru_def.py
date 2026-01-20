# Ammonia synthesis overall results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import os
import time
from Economic_NH3 import *

#%% data load
parameter_data_syn_Ru = pd.read_csv('synthesis LHHW aspen parameter Ru.csv',encoding='CP949')

#%%
def sim_NH3_syn_Ru(link, solar_irradiance_rich, cat_idx, T_C, P_bar, GHSV,
                   elec_cost, cooling_water_cost, catalyst_cost_Ru, lcon):
    i = cat_idx
    vol_flowrate = 127737002 #L/h # 500MW electorlysis 기준 H2 8.88 ton/h
    R = 8.314 # J mol−1 K−1
    cat_usage = vol_flowrate / GHSV #kg
    void_fraction = 0.5
    cat_density = 800 #kg/m3
    reactor_volume = cat_usage / cat_density / void_fraction #m3
    L_D_ratio = 5.9 #
    D = (4*reactor_volume/3/L_D_ratio/3.14)**(1/3)
    L_each = L_D_ratio * D
    L = 3*L_each
                
                
    #calculated
    T_K = T_C + 273.15 #°C->K
    P_atm = P_bar * 0.9869 # bar->atm
    

    # data input
    #driving force
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF1_A/1").Value = 0
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_A/1").Value = 5.056
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_B/1").Value = -4609
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_C/1").Value = 2.69
    link.Tree.FindNode("\Data\Reactions\Reactions\LHHW\Input\DF2_D/1").Value = 0.000127
    
    # data input
    #driving force
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/PRE_EXP/1").Value= parameter_data_syn_Ru.iloc[i,0] # A_f = 100000
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ACT_ENERGY/1").Value = parameter_data_syn_Ru.iloc[i,1] #J/mol # Ea_f=100000
    
    
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/2").Value = parameter_data_syn_Ru.iloc[i,2]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/2").Value = parameter_data_syn_Ru.iloc[i,3]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_A/1/3").Value = parameter_data_syn_Ru.iloc[i,4]
    link.Tree.FindNode("/Data/Reactions/Reactions/LHHW/Input/ADS_B/1/3").Value = parameter_data_syn_Ru.iloc[i,5]
    
    #Set condition
    link.Tree.FindNode("/Data/Streams/H2N2/Input/TOTFLOW/MIXED").Value = vol_flowrate # L h-1  
    
    
    link.Tree.FindNode("/Data/Blocks/COMP1/Input/PRES").Value = P_atm # comp pressure # atm P=150
    
    link.Tree.FindNode("/Data/Blocks/COOL1/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/COOL1/Input/TEMP").Value = T_K # PFR Temperature # K T=600
    link.Tree.FindNode("/Data/Blocks/COOL2/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/COOL2/Input/TEMP").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/COOL3/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/COOL3/Input/TEMP").Value = T_K # PFR Temperature # K
    link.Tree.FindNode("/Data/Blocks/SYN1/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/SYN1/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/SYN2/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/SYN2/Input/DIAM").Value = D # PFR diameter # m
    link.Tree.FindNode("/Data/Blocks/SYN3/Input/LENGTH").Value = L_each # PFR length # m
    link.Tree.FindNode("/Data/Blocks/SYN3/Input/DIAM").Value = D # PFR diameter # m
    
    link.Tree.FindNode("/Data/Blocks/COOL4/Input/PRES").Value = P_atm # PFR pressure # atm
    link.Tree.FindNode("/Data/Blocks/FLASH1/Input/PRES/RECYCLE1").Value = P_atm
    
    
    
    link.Engine.Run2()
    
    if not link.Engine.IsRunning:
        initial_hydrogen = link.Tree.FindNode("/Data/Streams/H2N2/Output/MOLEFLOW/MIXED/H2").Value #mole
        remained_hydrogen = link.Tree.FindNode("/Data/Streams/RECYCLE1/Output/MOLEFLOW/MIXED/H2").Value #mole
        makeup_hydrogen = initial_hydrogen - remained_hydrogen
        
        conversion_hydrogen_overall = (initial_hydrogen - remained_hydrogen)/initial_hydrogen * 100 #%
    
        
        error_index = link.Tree.FindNode("/Data/Results Summary/Run-Status/Output/PER_ERROR").Value #1==error, 0=ok
        
        # COMP1: compressor
        #Q_COMP1 = abs(link.Tree.FindNode("/Data/Blocks/COMP1/Output/POWER_ISEN").Value) / 1000 * makeup_hydrogen/initial_hydrogen #W to kW
        Q_COMP1 = abs(link.Tree.FindNode("/Data/Blocks/COMP1/Output/POWER_ISEN").Value) / 1000 * makeup_hydrogen/initial_hydrogen #W to kW
        Q_COMP2 = abs(link.Tree.FindNode("/Data/Blocks/COMP1/Output/POWER_ISEN").Value) / 1000 * remained_hydrogen/initial_hydrogen #W to kW

        
        # SYN1: packed tower
        L_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/LENGTH").Value # m
        D_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/DIAM").Value #m
        # SYN2: packed tower
        L_SYN2 = link.Tree.FindNode("/Data/Blocks/SYN2/Input/LENGTH").Value # m
        D_SYN2 = link.Tree.FindNode("/Data/Blocks/SYN2/Input/DIAM").Value #m
        # SYN3: packed tower
        L_SYN3 = link.Tree.FindNode("/Data/Blocks/SYN3/Input/LENGTH").Value # m
        D_SYN3 = link.Tree.FindNode("/Data/Blocks/SYN3/Input/DIAM").Value #m
        # COOL1: cooler
        Q_COOL1 = abs(link.Tree.FindNode("/Data/Blocks/COOL1/Output/QCALC").Value) #W
        Delta_T_COOL1 = abs(link.Tree.FindNode("/Data/Streams/H2N2-2/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/H2N2-3/Output/TEMP_OUT/MIXED").Value)
        # COOL2: cooler
        Q_COOL2 = abs(link.Tree.FindNode("/Data/Blocks/COOL2/Output/QCALC").Value) #W
        Delta_T_COOL2 = abs(link.Tree.FindNode("/Data/Streams/NH3-1/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/NH3-2/Output/TEMP_OUT/MIXED").Value)
        # COOL3: cooler
        Q_COOL3 = abs(link.Tree.FindNode("/Data/Blocks/COOL3/Output/QCALC").Value) #W
        Delta_T_COOL3 = abs(link.Tree.FindNode("/Data/Streams/NH3-3/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/NH3-4/Output/TEMP_OUT/MIXED").Value)
        # COOL4: cooler
        Q_COOL4 = abs(link.Tree.FindNode("/Data/Blocks/COOL4/Output/QCALC").Value) #W
        Delta_T_COOL4 = abs(link.Tree.FindNode("/Data/Streams/NH3-5/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/NH3-6/Output/TEMP_OUT/MIXED").Value)
        # Flash1: vertical vessel
        V_FLASH = link.Tree.FindNode("/Data/Streams/NH3-6/Output/VOLFLMX/MIXED").Value /1000 /3600 #L/h to m3/sec
        Q_FLASH = abs(link.Tree.FindNode("/Data/Blocks/FLASH1/Output/QCALC").Value) #W
        
    
        #Bare module cost
        C_BM_COMP1, C_BM_COMP1_O = Capex.compressor(Q_COMP1)
        C_BM_COMP2, C_BM_COMP2_O = Capex.compressor(Q_COMP2)

        C_BM_SYN1, C_BM_SYN1_O = Capex.pbr(L_SYN1,D_SYN1)
        C_BM_SYN2, C_BM_SYN2_O = Capex.pbr(L_SYN2,D_SYN2)
        C_BM_SYN3, C_BM_SYN3_O = Capex.pbr(L_SYN3,D_SYN3)
        C_BM_COOL1, C_BM_COOL1_O = Capex.cooler(Q_COOL1, Delta_T_COOL1)
        C_BM_COOL2, C_BM_COOL2_O = Capex.cooler(Q_COOL2, Delta_T_COOL2)
        C_BM_COOL3, C_BM_COOL3_O = Capex.cooler(Q_COOL3, Delta_T_COOL3)
        C_BM_COOL4, C_BM_COOL4_O = Capex.cooler(Q_COOL4, Delta_T_COOL4)
        C_BM_Flash1, C_BM_Flash1_O = Capex.separator(V_FLASH)
        
        C_BM = C_BM_COMP1  + C_BM_SYN1 + C_BM_SYN2 + C_BM_SYN3 + C_BM_COOL1 + C_BM_COOL2 +C_BM_COOL3 +C_BM_COOL4 +C_BM_Flash1 + C_BM_COMP2
        C_BM_O = C_BM_COMP1_O  + C_BM_SYN1_O + C_BM_SYN2_O + C_BM_SYN3_O + C_BM_COOL1_O + C_BM_COOL2_O +C_BM_COOL3_O +C_BM_COOL4_O +C_BM_Flash1_O + C_BM_COMP2_O
        CAPEX = (1.18*C_BM + 0.5*C_BM_O) * 800.8/397 #Cepci 2023/2001
        
        CAPEX_comp = (1.18*C_BM_COMP1 + 0.5*C_BM_COMP1_O) * 800.8/397 + (1.18*C_BM_COMP2 + 0.5*C_BM_COMP2_O) * 800.8/397 
        CAPEX_reactor = (1.18*C_BM_SYN1 + 0.5*C_BM_SYN1_O) * 800.8/397 + (1.18*C_BM_SYN2 + 0.5*C_BM_SYN2_O) * 800.8/397 + (1.18*C_BM_SYN3 + 0.5*C_BM_SYN3_O) * 800.8/397 
        CAPEX_cooler = (1.18*C_BM_COOL1 + 0.5*C_BM_COOL1_O) * 800.8/397 + (1.18*C_BM_COOL2 + 0.5*C_BM_COOL2_O) * 800.8/397 + (1.18*C_BM_COOL3 + 0.5*C_BM_COOL3_O) * 800.8/397 + (1.18*C_BM_COOL4 + 0.5*C_BM_COOL4_O) * 800.8/397 
        CAPEX_separator = (1.18*C_BM_Flash1 + 0.5*C_BM_Flash1_O) * 800.8/397 
        
        
        
        
        ### OPEX ###
        elec_use_COMP1 = abs(link.Tree.FindNode("/Data/Blocks/COMP1/Output/POWER_ISEN").Value*0.001*8500) * makeup_hydrogen/initial_hydrogen  #W to kWh
        elec_use_COMP2 = abs(link.Tree.FindNode("/Data/Blocks/COMP1/Output/POWER_ISEN").Value*0.001*8500) * remained_hydrogen/initial_hydrogen #W to kWh

        elec_use = elec_use_COMP1 + elec_use_COMP2  #kWh
        cool_use_COOL1 = abs(link.Tree.FindNode("/Data/Blocks/COOL1/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
        cool_use_COOL2 = abs(link.Tree.FindNode("/Data/Blocks/COOL2/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
        cool_use_COOL3 = abs(link.Tree.FindNode("/Data/Blocks/COOL3/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
        cool_use_COOL4 = abs(link.Tree.FindNode("/Data/Blocks/COOL4/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
        cool_use_flash = abs(link.Tree.FindNode("/Data/Blocks/FLASH1/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
        cool_use = cool_use_COOL1 + cool_use_COOL2 + cool_use_COOL3 +cool_use_COOL4 +cool_use_flash #GJ/yr
      
        catalyst_use_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/CAT_RHO").Value * link.Tree.FindNode("/Data/Blocks/SYN1/Input/BED_VOIDAGE").Value *  L_SYN1 * 3.14 * (D_SYN1/2)**2 #kg
        catalyst_use_SYN2 = link.Tree.FindNode("/Data/Blocks/SYN2/Input/CAT_RHO").Value * link.Tree.FindNode("/Data/Blocks/SYN2/Input/BED_VOIDAGE").Value *  L_SYN2 * 3.14 * (D_SYN2/2)**2 #kg
        catalyst_use_SYN3 = link.Tree.FindNode("/Data/Blocks/SYN3/Input/CAT_RHO").Value * link.Tree.FindNode("/Data/Blocks/SYN3/Input/BED_VOIDAGE").Value *  L_SYN3 * 3.14 * (D_SYN3/2)**2 #kg
        catalyst_use_syn_total = catalyst_use_SYN1 + catalyst_use_SYN2 + catalyst_use_SYN3 #kg
        
        
        hydrogen_flowrate = (link.Tree.FindNode("/Data/Streams/H2N2/Output/MASSFLOW/MIXED/H2").Value - link.Tree.FindNode("/Data/Streams/RECYCLE1/Output/MASSFLOW/MIXED/H2").Value)*60*60*8500 #kg/sec to kg/yr
        nitrogen_flowrate = (link.Tree.FindNode("/Data/Streams/H2N2/Output/MASSFLOW/MIXED/N2").Value - link.Tree.FindNode("/Data/Streams/RECYCLE1/Output/MASSFLOW/MIXED/N2").Value)*60*60*8500 #kg/sec to kg/yr
        Np = 0 #NP: the handling particles equipment
        Nnp = 10 #Nnp: the handling non-particles equipment
        
        
        #Opex
        O_renew_elec = Opex.renew_elec(elec_use, elec_cost = elec_cost)
        O_cool = Opex.cool(cool_use, cooling_water_cost = cooling_water_cost)
        O_cat_Ru = Opex.cataylst_Ru(catalyst_use_syn_total, catalyst_cost_Ru=catalyst_cost_Ru)/1 #교체주기 1년
        O_hydrogen = Opex.solarPV_LOCH(solar_irradiance_rich)[0] *hydrogen_flowrate  # Opex.hydrogen(solar_irradiance_rich, hydrogen_flowrate)
        O_nitrogen = Opex.nitrogen(nitrogen_flowrate, lcon = lcon)
        O_labor = Opex.labor(Np, Nnp)
        O_main = Opex.maintenence(CAPEX)
        
        
        
        OPEX_catO = O_renew_elec + O_cool + O_cat_Ru + O_hydrogen + O_nitrogen + O_labor + O_main
        OPEX_catX = O_renew_elec + O_cool + O_hydrogen + O_nitrogen + O_labor + O_main
    
        ### LCOA ###
        r = 0.07 # %/100
        n = 25 # years
        CRF = r*(1+r)**n / ((1+r)**n - 1)
        m_liq_NH3 = link.Tree.FindNode("/Data/Streams/LIQNH3-1/Output/MASSFLOW/MIXED/NH3").Value*60*60*8500 #kg/sec ro kg/yr
        LCOA_catX = (CAPEX*CRF + OPEX_catX) / m_liq_NH3 
        LCOA_catO = (CAPEX*CRF + OPEX_catO) / m_liq_NH3 

        
        #energy
        elec_use_kWh = elec_use
        cool_use_kWh = cool_use*1e9/3.6e6
        SEC_coolO = (elec_use_kWh + cool_use_kWh) / m_liq_NH3  # i를 행 인덱스로 지정
        SEC_coolX = (elec_use) / m_liq_NH3  
        
        
        ### LCA ###
        #CO2 emission facor#
        CO2_factor_renew_elec = 0 #0.082 #kgCO2/kWh
        CO2_factor_cooling_water = 16.29 #70.1 #kgCO2/GJ
        CO2_factor_catalyst = 5.5 #kgCO2/kgCat
        CO2_factor_hydrogen = 0 #2.8 #kgCO2/kgH2
        CO2_factor_nitrogen = 0.2 #0.447 #kgCO2/kgN2
        

        #amount#
        renew_elec_usage = elec_use #kWh
        cooling_water_usage = cool_use #GJ/yr
        catalyst_usage = cat_usage/1 #kg #replacement ration 4year
        hydrogen_usage = hydrogen_flowrate #kg/yr
        nitrogen_usage = nitrogen_flowrate #kg/yr
           
        #Calculation
        CO2_emission_renew_elec = CO2_factor_renew_elec * renew_elec_usage
        CO2_emission_cooling_water = CO2_factor_cooling_water * cooling_water_usage
        CO2_emission_catalyst = CO2_factor_catalyst * catalyst_usage
        CO2_emission_hydrogen = CO2_factor_hydrogen * hydrogen_usage
        CO2_emission_nitrogen = CO2_factor_nitrogen * nitrogen_usage
        CO2_emission_sum = CO2_emission_renew_elec + CO2_emission_cooling_water + CO2_emission_catalyst + CO2_emission_hydrogen + CO2_emission_nitrogen
        CO2_emission_levelized = CO2_emission_sum/m_liq_NH3
        
        CO2_emission_renew_elec_levelized = CO2_emission_renew_elec/m_liq_NH3
        CO2_emission_cooling_water_levelized = CO2_emission_cooling_water/m_liq_NH3
        CO2_emission_catalyst_levelized = CO2_emission_catalyst/m_liq_NH3
        CO2_emission_hydrogen_levelized =CO2_emission_hydrogen/m_liq_NH3
        CO2_emission_nitrogen_levelized =  CO2_emission_nitrogen/m_liq_NH3
        
        
    print('H2 conversion(%):',conversion_hydrogen_overall)
    print('NH3 production(kg/yr):', m_liq_NH3)
    print('LCOA_catX($/kg):',LCOA_catX)
    print('LCOA_catO($/kg):',LCOA_catO)
    print('SEC(kWh/kg):',SEC_coolX)
    print('CO2(CO2/kg):',CO2_emission_levelized)
    print('error_index:',error_index)
    
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
        "CAPEX_reactor": CAPEX_reactor,
        "CAPEX_cooler": CAPEX_cooler,
        "CAPEX_separator": CAPEX_separator
    },
    "OPEX": {
        "catalyst_use_syn_total (kg)": catalyst_use_syn_total,
        "O_renew_elec": O_renew_elec,
        "O_cool": O_cool,
        "O_cat_Ru": O_cat_Ru,
        "O_hydrogen": O_hydrogen,
        "O_nitrogen": O_nitrogen,
        "O_labor": O_labor,
        "O_main": O_main,
        "OPEX_catO": OPEX_catO,
        "OPEX_catX": OPEX_catX
    },
    "LCOA": {
        "LCOA_catO": LCOA_catO,
        "LCOA_catX": LCOA_catX
    },
    "SEC": {
        "elec_use_levelized": elec_use_kWh/m_liq_NH3,
        "cool_use_levelized": cool_use_kWh/m_liq_NH3,
        "SEC_coolO": SEC_coolO,
        "SEC_coolX": SEC_coolX
    },
    "CO2_emission": {
        "CO2_emission_renew_elec_levelized": CO2_emission_renew_elec_levelized,
        "CO2_emission_cooling_water_levelized": CO2_emission_cooling_water_levelized,
        "CO2_emission_catalyst_levelized": CO2_emission_catalyst_levelized,
        "CO2_emission_hydrogen_levelized": CO2_emission_hydrogen_levelized,
        "CO2_emission_nitrogen_levelized": CO2_emission_nitrogen_levelized,
        "CO2_emission_levelized": CO2_emission_levelized
    },
    "Performance": {
        "m_liq_NH3 (kg/yr)": m_liq_NH3,
        "conversion_hydrogen_overall (%)": conversion_hydrogen_overall,
        "error_index": error_index
    }
}

    return results
    
