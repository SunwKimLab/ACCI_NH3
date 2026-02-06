import pickle
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import win32com.client as win32
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import csv
from Economic_NH3 import *
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.ticker import FormatStrFormatter  # 상단에 추가


from Decomposition_Ni_def_recycleX import *
from Decomposition_Ru_def_recycleX import *

from Synthesis_Fe_def import *
from Synthesis_Ru_def import *

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'


#%%
# 저장된 파일 디렉토리
wd = os.getcwd()
base_dir = os.path.join(wd, "Optimization_results_catO/Syn", f"Fe_T,P,GHSV") #Fe_T,P,GHSV3600

# 결과 저장 딕셔너리
results_dict = {}

LCOA_op_Fe_list = []

# 범위 설정
for j in range(0, len(parameter_data_syn_Fe)):  # 필요한 범위로 수정
    file_path = os.path.join(base_dir, f"cat{j}.pkl")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            results_dict[j] = pickle.load(f)
        print(f"✅ cat{j}.pkl 불러오기 완료")
        LCOA_op_Fe = results_dict[j]['LCOA']['LCOA_catO'] # j=1
        LCOA_op_Fe_list.append(LCOA_op_Fe)
    else:
        print(f"⚠️ cat{j}.pkl 파일 없음")


#%% optimal LCOA 결과 저장
# numpy 배열로 변환
LCOA_op_Fe_arr = np.array(LCOA_op_Fe_list)

# 양수 값의 인덱스 중 최소값을 가지는 인덱스 찾기
positive_indices = np.where(LCOA_op_Fe_arr > 0)[0]
if len(positive_indices) > 0:
    min_positive_index = positive_indices[np.argmin(LCOA_op_Fe_arr[positive_indices])]
    min_positive_value = LCOA_op_Fe_arr[min_positive_index]

    # CSV 저장
    output_csv_path = os.path.join(wd, 'affcatcost/syn/optimal_LCOA_syn_Fe_index.csv')
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'Optimal LCOA (USD/kg NH3)'])
        writer.writerow([min_positive_index, min_positive_value])

    print(f"✅ 최소 LCOA 저장 완료: index={min_positive_index}, value={min_positive_value:.4f}")
else:
    print("⚠️ 양수 LCOH 값이 없습니다.")
    


#%%
T_C = 647.6865842204488
P_bar = 7.988250816778675
GHSV = 5233.011287748348


distance_aus_ulsan = 7065 # km
d_km = distance_aus_ulsan

solar_irr_aus_Hedlnad = 2351.25
solar_irr_kor_ulsan = 1420 #1492.29
solar_irr_rich = solar_irr_aus_Hedlnad
solar_irr_poor = solar_irr_kor_ulsan


cat_idx_dec = 0 # 10wt% Ni/Al2O3
elec_cost= 0.065
cooling_water_cost= 0.35
catalyst_cost_Ni= 47.02
ads_cost= 3.41
NOxtreat_cost= 2
BlueNH3_cost = 0.25

#%%
# # link aspen file
# path = os.getcwd()
# file_path = '4. Aspen_file_overall_scaleup/Ammonia decomposition_overall_v5.apw'
# link = win32.gencache.EnsureDispatch("Apwn.Document")
# link.InitFromArchive2(os.path.abspath(file_path))
# link.Visible = False

#%%
# LCOA_list = []
# LCOH_difference_list = []
# aff_cat_cost_syn_list = []
# cat_use_syn_list = []

# for j in range(0, len(parameter_data_syn_Fe)):
        
#     LCOA = results_dict[j]['LCOA']['LCOA_catX'] # j=1
#     ammonia_cost = LCOA
#     LCOA_list.append(LCOA)
    
#     results = sim_NH3_dec_Ni(link, ammonia_cost, d_km, cat_idx_dec, T_C, P_bar, GHSV, elec_cost, cooling_water_cost, catalyst_cost_Ni, ads_cost, NOxtreat_cost, BlueNH3_cost)
    
#     LCOH_import = results['LCOH']['LCOH_catO']
    
#     LCOH_domestic = Opex.solarPV_LOCH(solar_irr_poor)[0]
    
    
#     LCOH_difference = LCOH_domestic - LCOH_import 
#     LCOH_difference_list.append(LCOH_difference)
    
#     total_cost = LCOH_difference * results['Performance']['m_produced_H2 (kg/yr)']

    
#     cat_use_syn = results_dict[j]['OPEX']['catalyst_use_syn_total (kg)'] # kg
#     cat_use_syn_list.append(cat_use_syn)
    
#     aff_cat_cost_syn = total_cost / cat_use_syn
#     aff_cat_cost_syn_list.append(aff_cat_cost_syn)

#     print('LCOH_difference',LCOH_difference)
#     print('aff_cat_cost_syn',aff_cat_cost_syn)

# # 전체 list를 pkl로 저장
# save_path = os.path.join(wd, f"affcatcost/syn/aff_cat_cost_syn_list_Fe_opt_cond.pkl")
# with open(save_path, 'wb') as f:
#     pickle.dump(aff_cat_cost_syn_list, f)
# print(f"✅ 전체 results_dict_LCOH_Ru 저장 완료: {save_path}")



# if link is not None:
#     link.Close()
# else:
#     pass



#%% optimal affcatcost 결과 저장


# # numpy 배열로 변환
# aff_cat_cost_syn_arr = np.array(aff_cat_cost_syn_list)

# # 양수 값의 인덱스 중 최대값을 가지는 인덱스 찾기
# positive_indices = np.where(aff_cat_cost_syn_arr > 0)[0]
# if len(positive_indices) > 0:
#     max_positive_index = positive_indices[np.argmax(aff_cat_cost_syn_arr[positive_indices])]
#     max_positive_value = aff_cat_cost_syn_arr[max_positive_index]

#     # CSV 저장
#     output_csv_path = os.path.join(wd, 'affcatcost/syn/optimal_affcatcost_syn_Fe_index.csv')
#     with open(output_csv_path, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['index', 'Affordable Catalyst Cost (USD/kg)'])
#         writer.writerow([max_positive_index, max_positive_value])

#     print(f"✅ 최대 양수 affordable catalyst cost 저장 완료: index={max_positive_index}, value={max_positive_value:.2f}")
# else:
#     print("⚠️ 양수 affordable catalyst cost 값이 없습니다.")



#%% file 불러오기

# 작업 디렉토리 설정
loading_path_template = wd + "/Guideline table_syn/{}_{}.pkl"  # 파일 경로 템플릿

# 온도 및 촉매 리스트 정의
T_values = range(300, 510, 10)  # 300부터 500까지 10 단위 증가
catalysts = ["Fe"]  # 사용할 촉매 종류

# 모든 조합의 pickle 파일을 로드하여 전역 변수로 저장
for T in T_values:
    for cat in catalysts:
        dict_name = f"dict_syn_table_{T}_{cat}"  # 동적 변수명 생성
        load_file = loading_path_template.format(T, cat)  # 파일 경로 생성
        
        try:
            with open(load_file, 'rb') as file:
                globals()[dict_name] = pickle.load(file)  # 전역 변수에 저장
            print(f"로드 완료: {dict_name} ({load_file})")
        except FileNotFoundError:
            print(f"파일 없음: {load_file}")
            
#%% aff cat cost 불러오기


# 저장된 경로
load_path = os.path.join(wd, "affcatcost/syn/aff_cat_cost_syn_list_Fe_opt_cond.pkl")

# 불러오기
with open(load_path, 'rb') as f:
    aff_cat_cost_syn_list = pickle.load(f)

print(f"✅ 파일 로드 완료: {load_path}")



#%% 촉매 이름 불러오기
cat_Fe_name = pd.read_csv('synthesis catalyst name Fe_2.csv',encoding='CP949')

cat_Ru_name = pd.read_csv('synthesis catalyst name Ru_2.csv',encoding='CP949')

#%% Fe 49개: lab scale: 온도에 따른 전환율 & optimal aff cat cost
temperatures = range(300, 510, 10)  # 300부터 500까지 10 단위 증가
GHSV_list = [12000, 18000, 24000, 36000, 60000, 72000]

for GHSV in GHSV_list:
    n = len(parameter_data_syn_Fe)
    lowest_indices = np.argsort(aff_cat_cost_syn_list)[-n:]

    # 0보다 큰 값만 컬러맵 기준으로 사용
    valid_affcatcosts = [aff_cat_cost_syn_list[i] for i in lowest_indices if aff_cat_cost_syn_list[i] > 0]

    # 컬러맵 범위 지정
    vmin = min(valid_affcatcosts) if valid_affcatcosts else 0
    vmax = max(valid_affcatcosts) if valid_affcatcosts else 1

    cmap = cm.get_cmap('coolwarm')
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    catalyst_names = [cat_Fe_name.iloc[i, 0] for i in lowest_indices]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    max_y_value = float('-inf')

    for i in lowest_indices:
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_syn_table_{temp}_Fe"
                y_value = globals()[key][GHSV]['H2 Conversion exp PFR(%)'][i]
                y_values.append(y_value)

                if y_value > max_y_value:
                    max_y_value = y_value

            except KeyError as e:
                print(f"KeyError for {temp} °C and i={i}: {e}")
            except Exception as e:
                print(f"Error for {temp} °C and i={i}: {e}")
                y_values.append(None)

        if len(y_values) == len(temperatures) and all(val is not None for val in y_values):
            if aff_cat_cost_syn_list[i] > 0:
                color = cmap(norm(aff_cat_cost_syn_list[i]))
            else:
                color = 'gray'

            ax.plot(
                temperatures,
                y_values,
                color=color,
                linewidth=1.5,
                alpha=0.8
            )

    ax.set_ylim(-0.2, max_y_value + 1)

    # 범례 설정 (거꾸로 나열 + gray 포함)
    handles = [
        plt.Line2D([0], [0],
                   color=(cmap(norm(aff_cat_cost_syn_list[i])) if aff_cat_cost_syn_list[i] > 0 else 'gray'),
                   lw=2,
                   label=f"{catalyst_names[j]}")
        for j, i in reversed(list(enumerate(lowest_indices)))
    ]
    ax.legend(
        handles=handles,
        title="Catalyst Names",
        fontsize=13,
        loc='upper right',
        title_fontsize=17,
        bbox_to_anchor=(1.85, 0.99),
        ncol=1
    )

    ax.text(
        0.96, 0.94,
        f"GHSV = {GHSV} Lh$^{{-1}}$kg$^{{-1}}$",
        fontsize=20,
        transform=ax.transAxes,
        va='center',
        ha='right',
        bbox=dict(facecolor='white', edgecolor='gray', alpha=0.5, boxstyle='round,pad=0.3')
    )

    # 컬러바 설정 (유효 값 있을 때만 추가)
    if valid_affcatcosts:
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label("ACCI (USD/kg catalyst)", fontsize=20, labelpad=15)
        cbar.ax.tick_params(labelsize=20)

    ax.set_xlabel("Temperature (°C)", fontsize=25)
    ax.set_ylabel("Lab-scale H$_{2}$ Conversion (%)", fontsize=25)
    ax.set_title("Fe-based", fontsize=25)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=23)

    plt.show()


#%% Fe 49개: lab scale: 온도에 따른 전환율 & LCOA
temperatures = range(300, 510, 10)  # 300부터 500까지 10 단위 증가

GHSV_list = [12000,18000,24000,36000,60000,72000]

for GHSV in GHSV_list:
    n = len(parameter_data_syn_Fe)
    lowest_indices = np.argsort(LCOA_op_Fe_list)[-n:]

    # 음수가 아닌 값만 컬러맵 기준으로 사용
    valid_LCOA = [LCOA_op_Fe_list[i] for i in lowest_indices if LCOA_op_Fe_list[i] >= 0]

    # 컬러맵 범위 지정
    if valid_LCOA:  # 비어있지 않다면
        vmin = min(valid_LCOA)
        vmax = max(valid_LCOA)
    else:
        vmin, vmax = 0, 1  # fallback

    cmap = cm.get_cmap('PiYG')
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    catalyst_names = [cat_Fe_name.iloc[i, 0] for i in lowest_indices]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    max_y_value = float('-inf')

    for i in lowest_indices:
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_syn_table_{temp}_Fe"
                y_value = globals()[key][GHSV]['H2 Conversion exp PFR(%)'][i]
                y_values.append(y_value)

                if y_value > max_y_value:
                    max_y_value = y_value

            except KeyError as e:
                print(f"KeyError for {temp} °C and i={i}: {e}")
            except Exception as e:
                print(f"Error for {temp} °C and i={i}: {e}")
                y_values.append(None)

        if len(y_values) == len(temperatures) and all(val is not None for val in y_values):
            if LCOA_op_Fe_list[i] >= 0:
                color = cmap(norm(LCOA_op_Fe_list[i]))
            else:
                color = 'gray'

            ax.plot(
                temperatures,
                y_values,
                color=color,
                linewidth=1.5,
                alpha=0.8
            )

    ax.set_ylim(-0.2, max_y_value + 1)

    # 범례 설정
    handles = [
        plt.Line2D([0], [0],
                   color=('gray' if LCOA_op_Fe_list[i] < 0 else cmap(norm(LCOA_op_Fe_list[i]))),
                   lw=2,
                   label=f"{catalyst_names[j]}")
        for j, i in enumerate(lowest_indices)
    ]
    ax.legend(
        handles=handles,
        title="Catalyst Names",
        fontsize=13,
        loc='upper right',
        title_fontsize=17,
        bbox_to_anchor=(1.85, 0.99),
        ncol=1
    )

    ax.text(
        0.96, 0.94,
        f"GHSV = {GHSV} Lh$^{{-1}}$kg$^{{-1}}$",
        fontsize=20,
        transform=ax.transAxes,
        va='center',
        ha='right',
        bbox=dict(facecolor='white', edgecolor='gray', alpha=0.5, boxstyle='round,pad=0.3')
    )

    # 컬러바 설정 (유효 값 있을 때만 추가)
    if valid_LCOA:
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label("LCOA (USD/kg NH$_{3}$)", fontsize=20, labelpad=15)
        cbar.ax.tick_params(labelsize=20)

    ax.set_xlabel("Temperature (°C)", fontsize=25)
    ax.set_ylabel("Lab-scale H$_{2}$ Conversion (%)", fontsize=25)
    ax.set_title("Fe-based", fontsize=25)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=23)

    plt.show()
    



#%%
LCOA_opt_list = []
cat_use_syn_list = []

for j in range(0, len(parameter_data_syn_Fe)):
        
    LCOA = results_dict[j]['LCOA']['LCOA_catO'] # j=1
    ammonia_cost = LCOA
    LCOA_opt_list.append(LCOA)
    

    cat_use_syn = results_dict[j]['OPEX']['catalyst_use_syn_total (kg)'] # kg
    cat_use_syn_list.append(cat_use_syn)
    

#%%
# 설정
temperatures = range(300, 510, 10)
GHSV_list = [36000]
temperatures_50 = [300, 350, 400, 450, 500]
highlight_label_coords = [(425, 4.6), (475, 1.9), (400, 0.6), (450, 0.7), (500, 0.7)]  # 수동 조정 좌표

for GHSV in GHSV_list:
    n = len(parameter_data_syn_Fe)
    
    valid_indices = [i for i in range(n) if aff_cat_cost_syn_list[i] > 0 and LCOA_opt_list[i] > 0]

    # valid_indices = list(range(n))  # 전체 인덱스 사용
    sorted_by_lcoa = sorted(valid_indices, key=lambda i: LCOA_opt_list[i])
    n_valid = len(sorted_by_lcoa)

    quantile_indices = [
        sorted_by_lcoa[0],
        sorted_by_lcoa[n_valid // 4],
        sorted_by_lcoa[n_valid // 2],
        sorted_by_lcoa[3 * n_valid // 4],
        sorted_by_lcoa[-1]
    ]

    selected_affcatcost = [aff_cat_cost_syn_list[i] for i in quantile_indices]
    vmin, vmax = min(selected_affcatcost), max(selected_affcatcost)
    cmap = cm.get_cmap('coolwarm')
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

    for i in valid_indices:
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_syn_table_{temp}_Fe"
                y_value = globals()[key][GHSV]['H2 Conversion exp PFR(%)'][i]
                y_values.append(y_value)
            except KeyError:
                y_values.append(None)
        if all(v is not None for v in y_values):
            ax.plot(temperatures, y_values, color="gray", linewidth=1.5, alpha=0.5)

    legend_elements = []
    for idx, i in enumerate(quantile_indices):
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_syn_table_{temp}_Fe"
                y_value = globals()[key][GHSV]['H2 Conversion exp PFR(%)'][i]
                y_values.append(y_value)
            except KeyError:
                y_values.append(None)

        if all(v is not None for v in y_values):
            color = cmap(norm(aff_cat_cost_syn_list[i]))
            ax.plot(temperatures, y_values, color=color, linewidth=3, alpha=0.9)

            # 여기에서 직접 좌표로 텍스트 위치 지정
            label_x, label_y = highlight_label_coords[idx]
            ax.text(
                label_x, label_y, f"{aff_cat_cost_syn_list[i]:.2f}",
                fontsize=30, fontweight='bold', color=color,
                ha='center', va='center', rotation=0,
                bbox=dict(facecolor='white', edgecolor='none', alpha=1, boxstyle='round,pad=0')
            )

            catalyst_name = cat_Fe_name.iloc[i, 0]
            legend_elements.append(Line2D([0], [0], color=color, linewidth=4, label=catalyst_name))

    ax.set_xlabel("Temperature (°C)", fontsize=35)
    ax.set_ylabel("Lab-scale\nH$_{2}$ Conversion (%)", fontsize=35)
    ax.set_title("Fe-based", fontsize=35)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=30)

    ax.text(
        0.47, 0.93,
        f"GHSV = {GHSV} Lh$^{{-1}}$kg$^{{-1}}$",
        fontsize=25,
        transform=ax.transAxes,
        va='center',
        ha='right',
        bbox=dict(facecolor='white', edgecolor='gray', alpha=0.5, boxstyle='round,pad=0.3')
    )

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("ACCI (USD/kg catalyst)", fontsize=35, labelpad=15)
    cbar.ax.tick_params(labelsize=30)

    ax.legend(
        handles=legend_elements,
        fontsize=30,
        loc='center left',
        bbox_to_anchor=(-0.1, -0.4),
        frameon=True,
        ncol=2
    )

    plt.show()
    
    




