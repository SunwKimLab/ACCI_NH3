import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'

#%%
# Ishimoto et al. Large-scale production and transport of hydrogen from Norway to Europe and Japan: Value chain analysis and comparison of liquid hydrogen and ammonia as energy carriers. International Journal of Hydrogen Energy. 2020. 58. 32865-32883
# Salmon et al. Green ammonia as a spatial energy vector: a review. Sustainable Energy & Fuels. 2021. 5. 2814-2839

def transport(m_nh3, d_km): #m_nh3: nh3 kg #d_km: distance between country
    cost = 5e-6*d_km + 0.015 #$/NH3 kg    
    O_transport = m_nh3 * cost 
    return O_transport

#%%
distance_range = range(5000,25000,100)
transport_cost_calculation_list=[]
CAPEX_calculation_list=[]
OPEX_calculation_list=[]
BOG_calculation_list=[]

for distance in distance_range:
    transport_cost_calculation = transport(1, distance)
    CAPEX_calculation = transport_cost_calculation * 24/(24 + 24.3 + 4.5) # Comparativecostassessmentofsustainableenergycarriersproduced fromnaturalgasaccountingforboil-offgasandsocialcostofcarbon
    OPEX_calculation = transport_cost_calculation * 24.3/(24 + 24.3 + 4.5)
    BOG_calculation = transport_cost_calculation * 4.5/(24 + 24.3 + 4.5)
    transport_cost_calculation_list.append(transport_cost_calculation)
    CAPEX_calculation_list.append(CAPEX_calculation)
    OPEX_calculation_list.append(OPEX_calculation)
    BOG_calculation_list.append(BOG_calculation)
    
    
equation_text = f'y = {5e-6}x + {0.015}'
    
    
# 그래프 그리기
plt.figure(figsize=(7, 5.5), dpi=300)
plt.plot(distance_range, transport_cost_calculation_list, color='orange', label='transport_cost_calculation', linewidth=3)
#plt.plot(irradiance_range, y_pred, color='red', linestyle='--', label='Fitted Line')

# 방정식과 R² 값 표시
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=20,
         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="white"))

# 라벨 설정 및 기타 설정
plt.xlabel('Shipping distance (km)', fontsize=20)
plt.ylabel('Shipping cost (USD/kg NH$_{3}$)', fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=17)
plt.grid(linestyle='--')
#plt.legend(fontsize=12)
plt.show()



#%%
distance_range = range(5000,26000,1000)
transport_cost_calculation_list=[]
CAPEX_calculation_list=[]
OPEX_calculation_list=[]
BOG_calculation_list=[]

for distance in distance_range:
    transport_cost_calculation = transport(1, distance)
    CAPEX_calculation = transport_cost_calculation * 24/(24 + 24.3 + 4.5) # Comparative cost assessment
    OPEX_calculation = transport_cost_calculation * 24.3/(24 + 24.3 + 4.5)
    BOG_calculation = transport_cost_calculation * 4.5/(24 + 24.3 + 4.5)
    transport_cost_calculation_list.append(transport_cost_calculation)
    CAPEX_calculation_list.append(CAPEX_calculation)
    OPEX_calculation_list.append(OPEX_calculation)
    BOG_calculation_list.append(BOG_calculation)

x_labels = [str(x) for x in distance_range]
x = np.arange(len(x_labels))  # x 위치

# 파스텔 톤 색상 정의
capex_color = '#66c2a5'     # 약간 짙은 민트 계열 (green-teal)
opex_color = '#8da0cb'     # 부드러운 푸른 계열 (pastel blue) 
bog_color  = '#fc8d62'      # 오렌지와 살구 사이 (pastel orange)
total_line_color = 'black'

plt.figure(figsize=(13, 3.5), dpi=300)

# 막대 그래프 생성
plt.bar(x, CAPEX_calculation_list, label='CAPEX of shipment', color=capex_color)
plt.bar(x, OPEX_calculation_list, bottom=CAPEX_calculation_list, label='OPEX of shipment', color=opex_color)
plt.bar(
    x,
    BOG_calculation_list,
    bottom=[CAPEX_calculation_list[i] + OPEX_calculation_list[i] for i in range(len(x))],
    label='Boil-off gas',
    color=bog_color
)

# 각 bar의 맨 위 값 계산
bar_tops = [CAPEX_calculation_list[i] + OPEX_calculation_list[i] + BOG_calculation_list[i] for i in range(len(x))]

# 점 추가
plt.plot(x, bar_tops, 'o-', color=total_line_color, label='Total Cost', linewidth=2, markersize=8)

# 라벨 추가
plt.xlabel('Shipping distance (km)', fontsize=17)
plt.ylabel('Shipping cost\n(USD/kg NH$_{3}$)', fontsize=17)
plt.xticks(x, x_labels, rotation=45, fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

#%%
distance_range = range(5000,26000,1000)
transport_cost_calculation_list=[]
CAPEX_calculation_list=[]
OPEX_calculation_list=[]
BOG_calculation_list=[]

def transport(cost, distance):
    return cost * distance * 0.001  # Example function, adjust accordingly

for distance in distance_range:
    transport_cost_calculation = transport(1, distance)
    CAPEX_calculation = transport_cost_calculation * 24/(24 + 24.3 + 4.5) # Comparative cost assessment
    OPEX_calculation = transport_cost_calculation * 24.3/(24 + 24.3 + 4.5)
    BOG_calculation = transport_cost_calculation * 4.5/(24 + 24.3 + 4.5)
    transport_cost_calculation_list.append(transport_cost_calculation)
    CAPEX_calculation_list.append(CAPEX_calculation)
    OPEX_calculation_list.append(OPEX_calculation)
    BOG_calculation_list.append(BOG_calculation)

x_labels = [str(x) for x in distance_range]
x = np.arange(len(x_labels))  # x 위치

plt.figure(figsize=(13, 3.5), dpi=300)

# 막대 그래프 생성
plt.bar(x, CAPEX_calculation_list, label='CAPEX', color='white', edgecolor='black', hatch='/////')
plt.bar(x, OPEX_calculation_list, bottom=CAPEX_calculation_list, label='OPEX', color='white', edgecolor='black', hatch='......')
plt.bar(x, BOG_calculation_list, bottom=[CAPEX_calculation_list[i] + OPEX_calculation_list[i] for i in range(len(x))], label='Boil-off gas', color='white', edgecolor='black',  hatch='|||||')

# 각 bar의 맨 위 값 계산
bar_tops = [CAPEX_calculation_list[i] + OPEX_calculation_list[i] + BOG_calculation_list[i] for i in range(len(x))]

# 점 추가
plt.plot(x, bar_tops, 'o-', color='blue', label='Total Cost', linewidth=2, markersize=8)

# 라벨 추가
plt.xlabel('Shipping distance (km)', fontsize=17)
plt.ylabel('Shipping cost\n(USD/kg NH$_{3}$)', fontsize=17)
plt.xticks(x, x_labels, rotation=45, fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
