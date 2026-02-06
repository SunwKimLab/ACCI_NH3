# Economic model: NH3 Synthesis process
import numpy as np

#%%
class Capex():
    def heater(Q,P_atm): #kW, atm #[1200, 9400 kW] # Steam boiler
        #P_HX1 = link.Tree.FindNode("/Data/Blocks/HX1/Input/PRES").Value #atm
        #Q_HX1 = link.Tree.FindNode("/Data/Blocks/HX1/Output/QCALC").Value*(10**(-3)) #W to kW    
        C = [6.9617, -1.4800, 0.3161]
    
        if Q > 9400:
            Q_ref = 9400
            logCpO_heater_ref = C[0] + C[1]*np.log10(Q_ref) + C[2]*np.log10(Q_ref)**2
            CpO_heater_ref=10**(logCpO_heater_ref)
            
            n = int(Q / Q_ref) #2
            
            Q_add = Q - (Q_ref*n)  #500
            logCpO_heater_add = C[0] + C[1] * np.log10(Q_add) + C[2] * np.log10(Q_add)**2
            CpO_heater_add = 10**logCpO_heater_add
            CpO_heater = CpO_heater_ref * n + CpO_heater_add
        
    
        elif 1200 <= Q <= 9400:
            logCpO = C[0] + C[1] * np.log10(Q) + C[2] * np.log10(Q)**2
            CpO_heater = 10**logCpO
        
        else:
            logCpO_ref = C[0] + C[1] * np.log10(1200) + C[2] * np.log10(1200)**2
            CpO_ref = 10**logCpO_ref
            CpO_heater = CpO_ref * (Q / 1200)**0.6
        
        
        #Pressure factors
        P_barg = P_atm* 1.01325 - 1.01325 #atm -> bar -> barg
        if P_barg < 2:
            P = [0, 0, 0]
            logFp=0
        else:
            P = [2.594072, -4.23476, 1.722404]
            logFp = P[0] + P[1]*np.log10(P_barg) + P[2]*np.log10(P_barg)**2
        Fp = 10**logFp #Pressure factor
        
        
        FBM = 2.2 #Brae modlue factor
        FT = 1 #Temp factor
        C_BM_heater = CpO_heater*FBM*Fp*FT
        C_BM_heater_O = CpO_heater*FBM
        
        return C_BM_heater, C_BM_heater_O
    
    def heatexchanger_heat(Q, Delta_T): #[10, 1000m2] #Flat plate # W, deltT
        #Q_HX2 = abs(link.Tree.FindNode("/Data/Blocks/HX2/Output/QCALC").Value) #W
        #Delta_T_HX2 = abs(link.Tree.FindNode("/Data/Streams/NH3-1/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/NH3-2/Output/TEMP_OUT/MIXED").Value)
        C = [4.6656, -0.1557, 0.1547]
        Overall_heat_coefficient = 3500
        if Delta_T == 0:
            Area = 0
        else:
            Area = Q / (Delta_T * Overall_heat_coefficient) #m2
    
        Area = Area or 0  # None이면 0으로 설정
            
            
        if Area > 1000:
            Area_ref = 1000
            logCpO_heatexchanger_ref = C[0] + C[1]*np.log10(Area_ref) + C[2]*np.log10(Area_ref)**2
            CpO_heatexchanger_ref=10**(logCpO_heatexchanger_ref)
            
            n = int(Area / Area_ref) #2
        
            Area_add = Area - (Area_ref*n)  #500
            logCpO_heatexchanger_add = C[0] + C[1] * np.log10(Area_add) + C[2] * np.log10(Area_add)**2
            CpO_heatexchanger_add = 10**logCpO_heatexchanger_add
            CpO_heatexchanger = CpO_heatexchanger_ref * n + CpO_heatexchanger_add
    
    
        elif 10 <= Area <= 1000:
            logCpO = C[0] + C[1] * np.log10(Area) + C[2] * np.log10(Area)**2
            CpO_heatexchanger = 10**logCpO
    
        else:
            Area_ref = 10
            logCpO_ref = C[0] + C[1] * np.log10(Area_ref) + C[2] * np.log10(Area_ref)**2
            CpO_ref = 10**logCpO_ref
            CpO_heatexchanger = CpO_ref * (Area / Area_ref)**0.6
    


        Fp = 1 #Pressure factor
        Fm = 1 #Material factor #Carbon steel. 
        B = [0.96, 1.21] #Bare module factor
        C_BM_heatexchanger = CpO_heatexchanger*(B[0] + B[1]*Fm*Fp)
        C_BM_heatexchanger_O = CpO_heatexchanger*(B[0] + B[1])
        
        return C_BM_heatexchanger, C_BM_heatexchanger_O
    
    def packedtower(V): #packed tower #[0.3 520]
        #V = volume #m3 
    
        C = [3.4974, 0.4485, 0.1074]
        
        if V > 520:
            V_ref = 520
            logCpO_ref = C[0] + C[1] * np.log10(V_ref) + C[2] * np.log10(V_ref)**2
            CpO_pbr_ref = 10**logCpO_ref
            
            n = int(V / V_ref) #2
        
            V_add = V - (V_ref*n)  #500
            logCpO_add = C[0] + C[1] * np.log10(V_add) + C[2] * np.log10(V_add)**2
            CpO_pbr_add = 10**logCpO_add
            CpO_pbr = CpO_pbr_ref * n + CpO_pbr_add
        
        elif 0.3 <= V <= 520:
            logCpO = C[0] + C[1] * np.log10(V) + C[2] * np.log10(V)**2
            CpO_pbr = 10**logCpO
             
        else:
            V_ref = 0.3
            logCpO_ref = C[0] + C[1]*np.log10(V_ref) + C[2]*np.log10(V_ref)**2
            CpO_ref=10**(logCpO_ref)
            CpO_pbr=CpO_ref*(V/V_ref)**0.6
            
        FBM = 4.1 #Bare module factor
        C_BM_pbr = CpO_pbr*FBM
        C_BM_pbr_O = CpO_pbr*FBM     
        
        return C_BM_pbr, C_BM_pbr_O
    
    def pbr(L,D): #packed tower #[0.3 520]
        #L_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/LENGTH").Value # m
        #D_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/DIAM").Value #m
        V = np.pi*L*(D/2)**2 #volume #m3 
        
        C = [3.4974, 0.4485, 0.1074]
        
        if V > 520:
            V_ref = 520
            logCpO_ref = C[0] + C[1] * np.log10(V_ref) + C[2] * np.log10(V_ref)**2
            CpO_pbr_ref = 10**logCpO_ref
            
            n = int(V / V_ref) #2
        
            V_add = V - (V_ref*n)  #500
            logCpO_add = C[0] + C[1] * np.log10(V_add) + C[2] * np.log10(V_add)**2
            CpO_pbr_add = 10**logCpO_add
            CpO_pbr = CpO_pbr_ref * n + CpO_pbr_add
        
        elif 0.3 <= V <= 520:
            logCpO = C[0] + C[1] * np.log10(V) + C[2] * np.log10(V)**2
            CpO_pbr = 10**logCpO
             
        else:
            V_ref = 0.3
            logCpO_ref = C[0] + C[1]*np.log10(V_ref) + C[2]*np.log10(V_ref)**2
            CpO_ref=10**(logCpO_ref)
            CpO_pbr=CpO_ref*(V/V_ref)**0.6
            
        FBM = 4.1 #Bare module factor
        C_BM_pbr = CpO_pbr*FBM
        C_BM_pbr_O = CpO_pbr*FBM     
        
        return C_BM_pbr, C_BM_pbr_O
    
    def cooler(Q, Delta_T): #[10, 1000m2] #Flat plate
        #Q_HX2 = abs(link.Tree.FindNode("/Data/Blocks/HX2/Output/QCALC").Value) #W
        #Delta_T_HX2 = abs(link.Tree.FindNode("/Data/Streams/NH3-1/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/NH3-2/Output/TEMP_OUT/MIXED").Value)
        C = [4.6656, -0.1557, 0.1547]
        Overall_heat_coefficient = 3500
        if Delta_T == 0:
            Area = 0
        else:
            Area = Q / (Delta_T * Overall_heat_coefficient) #m2
    
    
        if Area > 1000:
            Area_ref = 1000
            logCpO_cooler_ref = C[0] + C[1]*np.log10(Area_ref) + C[2]*np.log10(Area_ref)**2
            CpO_cooler_ref=10**(logCpO_cooler_ref)
            
            n = int(Area / Area_ref) #2
        
            Area_add = Area - (Area_ref*n)  #500
            logCpO_cooler_add = C[0] + C[1] * np.log10(Area_add) + C[2] * np.log10(Area_add)**2
            CpO_cooler_add = 10**logCpO_cooler_add
            CpO_cooler = CpO_cooler_ref * n + CpO_cooler_add
    
    
        elif 10 <= Area <= 1000:
            logCpO = C[0] + C[1] * np.log10(Area) + C[2] * np.log10(Area)**2
            CpO_cooler = 10**logCpO
    
        else:
            Area_ref = 10
            logCpO_ref = C[0] + C[1] * np.log10(Area_ref) + C[2] * np.log10(Area_ref)**2
            CpO_ref = 10**logCpO_ref
            CpO_cooler = CpO_ref * (Area / Area_ref)**0.6
    
            

        Fp = 1 #Pressure factor
        Fm = 1 #Material factor #Carbon steel. 
        B = [0.96, 1.21] #Bare module factor
        C_BM_cooler = CpO_cooler*(B[0] + B[1]*Fm*Fp)
        C_BM_cooler_O = CpO_cooler*(B[0] + B[1])
        
        return C_BM_cooler, C_BM_cooler_O
    
    
    def compressor(Q): #Centrifugal #[450 3000] #kW
        #Q = abs(link.Tree.FindNode("/Data/Blocks/HX2/Output/QCALC").Value) / 1000 #W to kW
    
        C = [2.2897, 1.3604, -0.1027]
    
        if Q > 3000:            
            Q_ref = 3000
            logCpO_ref = C[0] + C[1] * np.log10(3000) + C[2] * np.log10(3000)**2
            CpO_ref = 10**logCpO_ref
    
            n = int(Q / Q_ref) #2
        
            Q_add = Q - (Q_ref*n)  #500
            logCpO_add = C[0] + C[1] * np.log10(Q_add) + C[2] * np.log10(Q_add)**2
            CpO_compressor_add = 10**logCpO_add
            CpO_compressor = CpO_ref * n + CpO_compressor_add
            
            
            
        elif 450 <= Q <= 3000:
            logCpO = C[0] + C[1] * np.log10(Q) + C[2] * np.log10(Q)**2
            CpO_compressor = 10**logCpO
        
        else:
            Q_ref = 450
            logCpO_ref = C[0] + C[1] * np.log10(450) + C[2] * np.log10(450)**2
            CpO_ref = 10**logCpO_ref
            CpO_compressor = CpO_ref * (Q / Q_ref)**0.6
            
        FBM = 2.8 #Bare module factor
        C_BM_compressor = CpO_compressor*FBM
        C_BM_compressor_O = CpO_compressor*FBM     
        
        return C_BM_compressor, C_BM_compressor_O
        
    

    
    def heatexchanger(Area): #[10, 1000m2] #Flat plate
        #Q_HX2 = abs(link.Tree.FindNode("/Data/Blocks/HX2/Output/QCALC").Value) #W
        #Delta_T_HX2 = abs(link.Tree.FindNode("/Data/Streams/NH3-1/Output/TEMP_OUT/MIXED").Value - link.Tree.FindNode("/Data/Streams/NH3-2/Output/TEMP_OUT/MIXED").Value)
        C = [4.6656, -0.1557, 0.1547]
        #Overall_heat_coefficient = 3500
        #if Delta_T == 0:
        #    Area = 1
        #else:
        #    Area = Q / (Delta_T * Overall_heat_coefficient) #m2
    
        Area = Area or 0  # None이면 0으로 설정
            
            
        if Area > 1000:
            Area_ref = 1000
            logCpO_heatexchanger_ref = C[0] + C[1]*np.log10(Area_ref) + C[2]*np.log10(Area_ref)**2
            CpO_heatexchanger_ref=10**(logCpO_heatexchanger_ref)
            
            n = int(Area / Area_ref) #2
        
            Area_add = Area - (Area_ref*n)  #500
            logCpO_heatexchanger_add = C[0] + C[1] * np.log10(Area_add) + C[2] * np.log10(Area_add)**2
            CpO_heatexchanger_add = 10**logCpO_heatexchanger_add
            CpO_heatexchanger = CpO_heatexchanger_ref * n + CpO_heatexchanger_add
    
    
        elif 10 <= Area <= 1000:
            logCpO = C[0] + C[1] * np.log10(Area) + C[2] * np.log10(Area)**2
            CpO_heatexchanger = 10**logCpO
    
        else:
            Area_ref = 10
            logCpO_ref = C[0] + C[1] * np.log10(Area_ref) + C[2] * np.log10(Area_ref)**2
            CpO_ref = 10**logCpO_ref
            CpO_heatexchanger = CpO_ref * (Area / Area_ref)**0.6
    


        Fp = 1 #Pressure factor
        Fm = 1 #Material factor #Carbon steel. 
        B = [0.96, 1.21] #Bare module factor
        C_BM_heatexchanger = CpO_heatexchanger*(B[0] + B[1]*Fm*Fp)
        C_BM_heatexchanger_O = CpO_heatexchanger*(B[0] + B[1])
        
        return C_BM_heatexchanger, C_BM_heatexchanger_O
    
    
    
    
    def separator(V): #m3 #[0.3 520m3] #vertical process vessel #gas -> gas, gas

        C = [3.4974, 0.4485, 0.1074]
        
        
        if V > 520:
            V_ref = 520
            logCpO_ref = C[0] + C[1]*np.log10(V_ref) + C[2]*np.log10(V_ref)**2
            CpO_ref=10**(logCpO_ref)
    
            n = int(V / V_ref) #2
        
            V_add = V - (V_ref*n)  #500
            logCpO_add = C[0] + C[1] * np.log10(V_add) + C[2] * np.log10(V_add)**2
            CpO_sep_add = 10**logCpO_add
            CpO_sep = CpO_ref * n + CpO_sep_add
            

        elif 0.3 <= V <= 520:
            logCpO = C[0] + C[1] * np.log10(V) + C[2] * np.log10(V)**2
            CpO_sep = 10**logCpO
            
        else:
            V_ref = 0.3
            logCpO_ref = C[0] + C[1] * np.log10(0.3) + C[2] * np.log10(0.3)**2
            CpO_ref = 10**logCpO_ref
            CpO_sep = CpO_ref * (V / V_ref)**0.6
        
        
        Fp =1 #Pressure factors
        Fm = 1 #Material factor #Carbon steel. 
        B = [2.25, 1.82] #Bare module factor
        C_BM_sep = CpO_sep*(B[0] + B[1]*Fm*Fp)
        C_BM_sep_O = CpO_sep*(B[0] + B[1])
        
        return C_BM_sep, C_BM_sep_O
    
    def furnace(Q): #Nonreactive fired heater #[1,000 100,000] #kW
        #Q = #kW
        C = [7.3488, -1.1666, 0.2028]
        
        
        if Q > 100000:
            Q_ref = 100000
            logCpO_ref = C[0] + C[1]*np.log10(Q_ref) + C[2]*np.log10(Q_ref)**2
            CpO_ref=10**(logCpO_ref)
    
            n = int(Q / Q_ref) #2
        
            Q_add = Q - (Q_ref*n)  #500
            logCpO_add = C[0] + C[1] * np.log10(Q_add) + C[2] * np.log10(Q_add)**2
            CpO_furnace_add = 10**logCpO_add
            CpO_furnace = CpO_ref * n + CpO_furnace_add
            
        elif 1000 <= Q <= 100000:
            logCpO_furnace = C[0] + C[1]*np.log10(Q) + C[2]*np.log10(Q)**2
            CpO_furnace = 10**(logCpO_furnace)
            
        
        else:
            Q_ref = 1000
            logCpO_ref = C[0] + C[1]*np.log10(Q_ref) + C[2]*np.log10(Q_ref)**2
            CpO_ref=10**(logCpO_ref)
            CpO_furnace=CpO_ref*(Q/Q_ref)**0.6
            

        FBM = 2.8
        C_BM_furnace = CpO_furnace*FBM
        C_BM_furnace_O = CpO_furnace*FBM     
    
        return C_BM_furnace, C_BM_furnace_O

    

        
        
#%%
class Opex():
    def renew_elec(elec_use, elec_cost = 0.035):
        #elec_use_flash = abs(link.Tree.FindNode("/Data/Blocks/FLASH1/Output/QCALC").Value*0.001*8500) #W to kWh
        #elec_cost = 0.035 #$/kWh
        O_renew_elec = elec_use * elec_cost
        return O_renew_elec
        
    def elec(elec_use, elec_cost = 0.065):
        #elec_use_flash = abs(link.Tree.FindNode("/Data/Blocks/FLASH1/Output/QCALC").Value*0.001*8500) #W to kWh
        #elec_cost = 0.065 #$/kWh
        O_elec = elec_use * elec_cost
        return O_elec
    
    def cool(cool_use, cooling_water_cost = 0.35):
        #cool_use_HX2 = abs(link.Tree.FindNode("/Data/Blocks/HX2/Output/QCALC").Value*0.001*0.001*0.001*60*60*8500) #W to GJ/yr
        #cooling_water_cost = 0.35 #$/GJ
        O_cool = cool_use * cooling_water_cost
        return O_cool
    
    def heat(heat_use, heating_utility_cost = 1.9*10**(-6)):
        #heat_use = link.Tree.FindNode("/Data/Blocks/HX1/Output/QCALC").Value * 0.001*60*60*8500 #W to KJ/yr
        #heating_utility_cost = 1.9*10**(-6) #$/KJ
        O_heat = heat_use * heating_utility_cost
        return O_heat
    
    def cataylst_Ru(catalyst_use, catalyst_cost_Ru = 321.04):
        #catalyst_use_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/CATWT").Value #kg
        #catalyst_cost_Ru = 321.04 #$/kg # Economies of scale in ammonia synthesis loops embedded with iron- and ruthenium-based catalysts
        O_cat_Ru = catalyst_use * catalyst_cost_Ru
        return O_cat_Ru
    
    def cataylst_Fe(catalyst_use, catalyst_cost_Fe = 4.2):
        #catalyst_use_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/CATWT").Value #kg
        #catalyst_cost_Fe = 4.2 #0.18 #$/kg # Ammonia synthesis catalyst 100 years: Practice, enlightenment and challenge
        O_cat_Fe = catalyst_use * catalyst_cost_Fe
        return O_cat_Fe
    
    def cataylst_Ni(catalyst_use, catalyst_cost_Ni = 47.02):
        #catalyst_use_SYN1 = link.Tree.FindNode("/Data/Blocks/SYN1/Input/CATWT").Value #kg
        #catalyst_cost_Ni = 47.02 #$/kg #Estimating Precommercial Heterogeneous Catalyst Price: A Simple Step-Based Method
        O_cat_Ni = catalyst_use * catalyst_cost_Ni
        return O_cat_Ni
    

    
    def nitrogen(nitrogen_flowrate, lcon = 0.01):
        #nitrogen_flowrate = link.Tree.FindNode("/Data/Streams/H2N2/Output/MASSFLOW/MIXED/N2").Value*60*60*8500 #kg/sec to kg/yr
        #lcon = 0.01 #$/kg #Optimal design and integration of a cryogenic Air Separation Unit (ASU) with Liquefied Natural Gas (LNG) as heat sink, thermodynamic and economic analyses #소영 LCON: 0.0189 $/kgN2 (mole flow rateN2 : 8845.78 kmol/hrO2 : 2307.98 kmol/hrmass flow rateN2 : 249064 kg/hrO2 : 73944.3 kg/hr) 
        O_nitrogen = lcon * nitrogen_flowrate
        return O_nitrogen
    
    
    def labor(Np, Nnp):
        #Np = 0 #NP: the handling particles equipment
        #Nnp = 8 #Nnp: the handling non-particles equipment
        N_OL = 4.5*(6.29 + 31.7*Np + 0.23*Nnp)**0.5 
        C_labor = 52700 #Annual salary per operator #$
        O_labor = C_labor * N_OL
        return O_labor
    
    def maintenence(Capex):
        O_main = Capex * 2.75 / 100
        return O_main

        
    def NH3adsorbent(ammonia_flowrate, ads_cost = 3.41): #output NH3 mol #8500h 기준
        usage = 0.333 #kg zeolite/NH3 mol
        #cost = 3.41 #$/kg zeolite
        O_NH3adsorbent = ammonia_flowrate * usage * ads_cost
        return O_NH3adsorbent
        
        
    def N2adsorbent(nitrogen_flowrate, ads_cost = 3.41): #output N2 mol #8500h 기준
        usage = 1.79 #mol N2/zeolite kg
        #cost = 3.41 #$/kg zeolite
        O_N2adsorbent = nitrogen_flowrate / usage * ads_cost
        return O_N2adsorbent
    
    def CH4(CH4_flowrate, CH4_cost = 0.140): #CH4 kg #8500h 기준
        #CH4_cost = 0.140 #$/kg
        O_CH4 = CH4_cost * CH4_flowrate
        return O_CH4
        
    
    def transport(m_nh3, d_km): #m_nh3: nh3 kg #d_km: distance between country
        cost = 5e-6*d_km + 0.015 #$/NH3 kg    
        O_transport = m_nh3 * cost 
        return O_transport
    
    def O2(O2_flowrate, O2_cost = 0.177): #O2 kg
        # O2_cost = 0.177 #$/kg #https://www.sciencedirect.com/science/article/pii/S0959652623040672#tbl6
        O_O2 = O2_cost * O2_flowrate
        return O_O2

    def NOxTreat(NOx_flowrate, NOxTreat_cost = 2): #O2 kg
        # NOxTreat_cost = 2 #$/kg #https://www.sciencedirect.com/science/article/pii/S0959652623040672#tbl6
        O_NOxTreat = NOxTreat_cost * NOx_flowrate
        return O_NOxTreat
    
    def BlueNH3(NH3_flowrate, BlueNH3_cost = 0.3): #O2 kg
        # BlueNH3_cost = 0.4 #$/kg #https://www.sciencedirect.com/science/article/pii/S0959652623040672#tbl6
        O_BlueNH3 = BlueNH3_cost * NH3_flowrate
        return O_BlueNH3
    
    
    
    
    
    
    
    def solarPV_LOCH(ghi_array,
                            ghi_base=2000,
                            pv_CAPEX=493_000,     # USD/MWp,DC
                            pv_OandM=6_800,       # USD/year/MWp,DC
                            pv_WACC=0.075,
                            pv_lifetime=25,
                            LHV_H2=33.3,          # kWh/kg H2
                            eff_electrolyzer=0.67,
                            CAPEX_electrolyzer=655,  # USD/kW
                            O_M_ratio=0.015,
                            stack_lifetime_hours=8760):
        """
        Calculate LCOH using total CAPEX and OPEX (PV + Electrolyzer), per kg H2.
        """
    
        # Present Value Factor
        PVF = (1 - (1 + pv_WACC) ** -pv_lifetime) / pv_WACC
    
        # Step 1: PV Energy generation (discounted)
        DCAC_sizing_factor = -0.0002682 * ghi_array + 1.7864 #sizing_factor_linear(ghi_array)
        cf_base= 0.31 / DCAC_sizing_factor  # capacity factor at base GHI
        cf_estimated = cf_base * (ghi_array / ghi_base)
        FLH_ac = cf_estimated * 8760  # hours/year
    
        # Step 3: Hydrogen production per MWp over stack lifetime
        H2_total = (FLH_ac * eff_electrolyzer * stack_lifetime_hours) / LHV_H2  # kg H2/MWp
    
        # Step 4: Total CAPEX and OPEX
        total_CAPEX = pv_CAPEX + CAPEX_electrolyzer * 1000  # USD/MWp
        total_OPEX = pv_OandM * PVF + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF  # USD/MWp over lifetime
    
        total_cost = total_CAPEX + total_OPEX  # USD/MWp over project life
    
        total_PV_cost = (pv_CAPEX +pv_OandM * PVF) / H2_total
        total_electrolyzer_cost = (CAPEX_electrolyzer * 1000 + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF) / H2_total
    
        # Step 5: LCOH per kg H2
        lcoh = total_cost / H2_total  # USD/kg H2
        return lcoh, total_PV_cost, total_electrolyzer_cost
    

    def solarPV_LOCH_2025(ghi_array,
                            ghi_base=2000,
                            pv_CAPEX=493_000,     # USD/MWp,DC
                            pv_OandM=6_800,       # USD/year/MWp,DC
                            pv_WACC=0.075,
                            pv_lifetime=25,
                            LHV_H2=33.3,          # kWh/kg H2
                            eff_electrolyzer=0.67,
                            CAPEX_electrolyzer=655,  # USD/kW
                            O_M_ratio=0.015,
                            stack_lifetime_hours=8760):
        """
        Calculate LCOH using total CAPEX and OPEX (PV + Electrolyzer), per kg H2.
        """

        # Present Value Factor
        PVF = (1 - (1 + pv_WACC) ** -pv_lifetime) / pv_WACC

        # Step 1: PV Energy generation (discounted)
        DCAC_sizing_factor = -0.0002682 * ghi_array + 1.7864 #sizing_factor_linear(ghi_array)
        cf_base= 0.31 / DCAC_sizing_factor  # capacity factor at base GHI
        cf_estimated = cf_base * (ghi_array / ghi_base)
        FLH_ac = cf_estimated * 8760  # hours/year

        # Step 3: Hydrogen production per MWp over stack lifetime
        H2_total = (FLH_ac * eff_electrolyzer * stack_lifetime_hours) / LHV_H2  # kg H2/MWp

        # Step 4: Total CAPEX and OPEX
        total_CAPEX = pv_CAPEX + CAPEX_electrolyzer * 1000  # USD/MWp
        total_OPEX = pv_OandM * PVF + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF  # USD/MWp over lifetime

        total_cost = total_CAPEX + total_OPEX  # USD/MWp over project life

        total_PV_cost = (pv_CAPEX +pv_OandM * PVF) / H2_total
        total_electrolyzer_cost = (CAPEX_electrolyzer * 1000 + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF) / H2_total

        # Step 5: LCOH per kg H2
        lcoh = total_cost / H2_total  # USD/kg H2
        return lcoh, total_PV_cost, total_electrolyzer_cost
    
    
    def solarPV_LOCH_2030(ghi_array,
                            ghi_base=2000,
                            pv_CAPEX=410_000,     # USD/MWp,DC
                            pv_OandM=6_200,       # USD/year/MWp,DC
                            pv_WACC=0.075,
                            pv_lifetime=25,
                            LHV_H2=33.3,          # kWh/kg H2
                            eff_electrolyzer=0.69,
                            CAPEX_electrolyzer=540,  # USD/kW
                            O_M_ratio=0.015,
                            stack_lifetime_hours=8760):
        """
        Calculate LCOH using total CAPEX and OPEX (PV + Electrolyzer), per kg H2.
        """
    
        # Present Value Factor
        PVF = (1 - (1 + pv_WACC) ** -pv_lifetime) / pv_WACC
    
        # Step 1: PV Energy generation (discounted)
        DCAC_sizing_factor = -0.0002682 * ghi_array + 1.7864 #sizing_factor_linear(ghi_array)
        cf_base= 0.32 / DCAC_sizing_factor  # capacity factor at base GHI
        cf_estimated = cf_base * (ghi_array / ghi_base)
        FLH_ac = cf_estimated * 8760  # hours/year
    
        # Step 3: Hydrogen production per MWp over stack lifetime
        H2_total = (FLH_ac * eff_electrolyzer * stack_lifetime_hours) / LHV_H2  # kg H2/MWp
    
        # Step 4: Total CAPEX and OPEX
        total_CAPEX = pv_CAPEX + CAPEX_electrolyzer * 1000  # USD/MWp
        total_OPEX = pv_OandM * PVF + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF  # USD/MWp over lifetime
    
        total_cost = total_CAPEX + total_OPEX  # USD/MWp over project life
    
        total_PV_cost = (pv_CAPEX +pv_OandM * PVF) / H2_total
        total_electrolyzer_cost = (CAPEX_electrolyzer * 1000 + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF) / H2_total
    
        # Step 5: LCOH per kg H2
        lcoh = total_cost / H2_total  # USD/kg H2
        return lcoh, total_PV_cost, total_electrolyzer_cost
     
    def solarPV_LOCH_2035(ghi_array,
                            ghi_base=2000,
                            pv_CAPEX=386_000,     # USD/MWp,DC
                            pv_OandM=5_950,       # USD/year/MWp,DC
                            pv_WACC=0.075,
                            pv_lifetime=25,
                            LHV_H2=33.3,          # kWh/kg H2
                            eff_electrolyzer=0.72,
                            CAPEX_electrolyzer=488,  # USD/kW
                            O_M_ratio=0.015,
                            stack_lifetime_hours=8760):
        """
        Calculate LCOH using total CAPEX and OPEX (PV + Electrolyzer), per kg H2.
        """
    
        # Present Value Factor
        PVF = (1 - (1 + pv_WACC) ** -pv_lifetime) / pv_WACC
    
        # Step 1: PV Energy generation (discounted)
        DCAC_sizing_factor = -0.0002682 * ghi_array + 1.7864 #sizing_factor_linear(ghi_array)
        cf_base= 0.32 / DCAC_sizing_factor  # capacity factor at base GHI
        cf_estimated = cf_base * (ghi_array / ghi_base)
        FLH_ac = cf_estimated * 8760  # hours/year
    
        # Step 3: Hydrogen production per MWp over stack lifetime
        H2_total = (FLH_ac * eff_electrolyzer * stack_lifetime_hours) / LHV_H2  # kg H2/MWp
    
        # Step 4: Total CAPEX and OPEX
        total_CAPEX = pv_CAPEX + CAPEX_electrolyzer * 1000  # USD/MWp
        total_OPEX = pv_OandM * PVF + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF  # USD/MWp over lifetime
    
        total_cost = total_CAPEX + total_OPEX  # USD/MWp over project life
    
        total_PV_cost = (pv_CAPEX +pv_OandM * PVF) / H2_total
        total_electrolyzer_cost = (CAPEX_electrolyzer * 1000 + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF) / H2_total
    
        # Step 5: LCOH per kg H2
        lcoh = total_cost / H2_total  # USD/kg H2
        return lcoh, total_PV_cost, total_electrolyzer_cost 
     
    def solarPV_LOCH_2040(ghi_array,
                            ghi_base=2000,
                            pv_CAPEX=363_000,     # USD/MWp,DC
                            pv_OandM=5_700,       # USD/year/MWp,DC
                            pv_WACC=0.075,
                            pv_lifetime=25,
                            LHV_H2=33.3,          # kWh/kg H2
                            eff_electrolyzer=0.74,
                            CAPEX_electrolyzer=435,  # USD/kW
                            O_M_ratio=0.015,
                            stack_lifetime_hours=8760):
        """
        Calculate LCOH using total CAPEX and OPEX (PV + Electrolyzer), per kg H2.
        """
    
        # Present Value Factor
        PVF = (1 - (1 + pv_WACC) ** -pv_lifetime) / pv_WACC
    
        # Step 1: PV Energy generation (discounted)
        DCAC_sizing_factor = -0.0002682 * ghi_array + 1.7864 #sizing_factor_linear(ghi_array)
        cf_base= 0.31 / DCAC_sizing_factor  # capacity factor at base GHI
        cf_estimated = cf_base * (ghi_array / ghi_base)
        FLH_ac = cf_estimated * 8760  # hours/year
    
        # Step 3: Hydrogen production per MWp over stack lifetime
        H2_total = (FLH_ac * eff_electrolyzer * stack_lifetime_hours) / LHV_H2  # kg H2/MWp
    
        # Step 4: Total CAPEX and OPEX
        total_CAPEX = pv_CAPEX + CAPEX_electrolyzer * 1000  # USD/MWp
        total_OPEX = pv_OandM * PVF + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF  # USD/MWp over lifetime
    
        total_cost = total_CAPEX + total_OPEX  # USD/MWp over project life
    
        total_PV_cost = (pv_CAPEX +pv_OandM * PVF) / H2_total
        total_electrolyzer_cost = (CAPEX_electrolyzer * 1000 + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF) / H2_total
    
        # Step 5: LCOH per kg H2
        lcoh = total_cost / H2_total  # USD/kg H2
        return lcoh, total_PV_cost, total_electrolyzer_cost  
     
     
    
    
    
    
    
#%%
class Profit():
    def oxygen(oxygen_flowrate):
        #nitrogen_flowrate = link.Tree.FindNode("/Data/Streams/H2N2/Output/MASSFLOW/MIXED/N2").Value*60*60*8500 #kg/sec to kg/yr
        lcoo = 0.177 #$/kg #Techno-economic comparison of green ammonia production processes #0.0189 #$/kg  #소영 LCON: 0.0189 $/kgN2 (mole flow rateN2 : 8845.78 kmol/hrO2 : 2307.98 kmol/hrmass flow rateN2 : 249064 kg/hrO2 : 73944.3 kg/hr) 
        P_oxygen = lcoo * oxygen_flowrate
        return P_oxygen
