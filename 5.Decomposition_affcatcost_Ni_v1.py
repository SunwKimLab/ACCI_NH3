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

GHSV = 36000


#%%
d_km = 7065


ammonia_cost = 0.6198258568850152 # KM1

distance_aus_ulsan = 7065 # km
d_km = distance_aus_ulsan

solar_irr_aus_Hedlnad = 2351.25
solar_irr_kor_ulsan = 1420 #1492.29
solar_irr_rich = solar_irr_aus_Hedlnad
solar_irr_poor = solar_irr_kor_ulsan

#%%
# 저장된 파일 디렉토리
wd = os.getcwd()
base_dir = os.path.join(wd, "Optimization_results_catO/Dec", f"Ni_T,P,GHSV") #Ni_T,P,GHSV36000

# 결과 저장 딕셔너리
results_dict = {}

# 범위 설정
for j in range(0, len(parameter_data_dec_Ni)):  # 필요한 범위로 수정
    file_path = os.path.join(base_dir, f"cat{j}.pkl")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            results_dict[j] = pickle.load(f)
        print(f"✅ cat{j}.pkl 불러오기 완료")
    else:
        print(f"⚠️ cat{j}.pkl 파일 없음")
#%%
LCOH_difference_list = []
aff_cat_cost_dec_list = []
cat_use_dec_list = []
total_cost_list = []
LCOH_op_Ni_list = []
LCOH_op_Ni_list_catO = []

for j in range(0, len(parameter_data_dec_Ni)):  # 필요한 범위로 수정

    LCOA = ammonia_cost# j=1
    ammonia_cost = LCOA
    
    LCOH_import = results_dict[j]['LCOH']['LCOH_catX']
    LCOH_import_catO = results_dict[j]['LCOH']['LCOH_catO']
    LCOH_op_Ni_list.append(LCOH_import)
    LCOH_op_Ni_list_catO.append(LCOH_import_catO)

    
    LCOH_domestic = Opex.solarPV_LOCH(solar_irr_poor)[0]
    
    
    LCOH_difference = LCOH_domestic - LCOH_import 
    LCOH_difference_list.append(LCOH_difference)
    
    
    total_cost = LCOH_difference * results_dict[j]['Performance']['m_produced_H2 (kg/yr)']
    total_cost_list.append(total_cost)

    cat_use_dec = results_dict[j]['OPEX']['catalyst_use_dec_total (kg)'] # kg
    cat_use_dec_list.append(cat_use_dec)
    
    aff_cat_cost_dec = total_cost / cat_use_dec
    aff_cat_cost_dec_list.append(aff_cat_cost_dec)

#%%
# 전체 list를 pkl로 저장
save_path = os.path.join(wd, f"affcatcost/Dec/aff_cat_cost_dec_list_Ni_opt_cond.pkl")
with open(save_path, 'wb') as f:
    pickle.dump(aff_cat_cost_dec_list, f)
print(f"✅ 전체 aff_cat_cost_dec_list 저장 완료: {save_path}")

#%% optimal affcatcost 결과 저장
# numpy 배열로 변환
aff_cat_cost_dec_arr = np.array(aff_cat_cost_dec_list)

# 양수 값의 인덱스 중 최대값을 가지는 인덱스 찾기
positive_indices = np.where(aff_cat_cost_dec_arr > 0)[0]
if len(positive_indices) > 0:
    max_positive_index = positive_indices[np.argmax(aff_cat_cost_dec_arr[positive_indices])]
    max_positive_value = aff_cat_cost_dec_arr[max_positive_index]

    # CSV 저장
    output_csv_path = os.path.join(wd, 'affcatcost/dec/optimal_affcatcost_dec_Ni_index.csv')
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'Affordable Catalyst Cost (USD/kg)'])
        writer.writerow([max_positive_index, max_positive_value])

    print(f"✅ 최대 양수 affordable catalyst cost 저장 완료: index={max_positive_index}, value={max_positive_value:.2f}")
else:
    print("⚠️ 양수 affordable catalyst cost 값이 없습니다.")
    
    

#%% optimal LCOH 결과 저장
# numpy 배열로 변환
LCOH_op_Ni_arr = np.array(LCOH_op_Ni_list_catO)

# 양수 값의 인덱스 중 최소값을 가지는 인덱스 찾기
positive_indices = np.where(LCOH_op_Ni_arr > 0)[0]
if len(positive_indices) > 0:
    min_positive_index = positive_indices[np.argmin(LCOH_op_Ni_arr[positive_indices])]
    min_positive_value = LCOH_op_Ni_arr[min_positive_index]

    # CSV 저장
    output_csv_path = os.path.join(wd, 'affcatcost/dec/optimal_LCOH_dec_Ni_index.csv')
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'Optimal LCOH (USD/kg H2)'])
        writer.writerow([min_positive_index, min_positive_value])

    print(f"✅ 최소 LCOH 저장 완료: index={min_positive_index}, value={min_positive_value:.4f}")
else:
    print("⚠️ 양수 LCOH 값이 없습니다.")





#%% file 불러오기

# 작업 디렉토리 설정
loading_path_template = wd + "/Guideline table_dec/{}_{}.pkl"  # 파일 경로 템플릿

# 온도 및 촉매 리스트 정의
T_values = range(400, 710, 10)  # 300부터 500까지 10 단위 증가
catalysts = ["Ni"]  # 사용할 촉매 종류

# 모든 조합의 pickle 파일을 로드하여 전역 변수로 저장
for T in T_values:
    for cat in catalysts:
        dict_name = f"dict_dec_table_{T}_{cat}"  # 동적 변수명 생성
        load_file = loading_path_template.format(T, cat)  # 파일 경로 생성
        
        try:
            with open(load_file, 'rb') as file:
                globals()[dict_name] = pickle.load(file)  # 전역 변수에 저장
            print(f"로드 완료: {dict_name} ({load_file})")
        except FileNotFoundError:
            print(f"파일 없음: {load_file}")





#%% 촉매 이름 불러오기

cat_Ni_name = pd.read_csv('decomposition catalyst name Ni_2.csv',encoding='CP949')

cat_Ru_name = pd.read_csv('decomposition catalyst name Ru_2.csv',encoding='CP949')




#%%% Ni:

temperatures = range(500, 710, 10) 

GHSV_list = [36000] # [6000, 12000, 18000, 24000, 30000, 36000]

for GHSV in GHSV_list:

    n = len(parameter_data_dec_Ni)
    lowest_indices = np.argsort(aff_cat_cost_dec_list)[-n:]

    # 음수가 아닌 값만 컬러맵 기준으로 사용
    valid_affcatcosts = [aff_cat_cost_dec_list[i] for i in lowest_indices if aff_cat_cost_dec_list[i] >= 0]

    # 컬러맵 범위 지정
    if valid_affcatcosts:  # 비어있지 않다면
        vmin = min(valid_affcatcosts)
        vmax = max(valid_affcatcosts)
    else:
        vmin, vmax = 0, 1  # fallback

    cmap = cm.get_cmap('coolwarm')
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    catalyst_names = [cat_Ni_name.iloc[i, 0] for i in lowest_indices]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    max_y_value = float('-inf')

    for i in lowest_indices:
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_dec_table_{temp}_Ni"
                y_value = globals()[key][GHSV]['NH3 Conversion exp PFR(%)'][i]
                y_values.append(y_value)

                if y_value > max_y_value:
                    max_y_value = y_value

            except KeyError as e:
                print(f"KeyError for {temp} °C and i={i}: {e}")
            except Exception as e:
                print(f"Error for {temp} °C and i={i}: {e}")
                y_values.append(None)

        if len(y_values) == len(temperatures) and all(val is not None for val in y_values):
            if aff_cat_cost_dec_list[i] >= 0:
                color = cmap(norm(aff_cat_cost_dec_list[i]))
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
                   color=('gray' if aff_cat_cost_dec_list[i] < 0 else cmap(norm(aff_cat_cost_dec_list[i]))),
                   lw=2,
                   label=f"{catalyst_names[j]}")
        for j, i in reversed(list(enumerate(lowest_indices)))
    ]
    legend = ax.legend(
        handles=handles,
        title="Catalyst Names",
        fontsize=13,
        loc='upper right',
        title_fontsize=17,
        bbox_to_anchor=(1.8, 1.1),
        ncol=1
    )

    # 그래프에 GHSV 텍스트 추가
    ax.text(
        0.96, 0.07, 
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
    ax.set_ylabel("Lab-scale NH$_{3}$ Conversion (%)", fontsize=25)
    ax.set_title("Ni-based", fontsize=25)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=23)

    plt.show()



#%%% Ni: LCOH

temperatures = range(500, 710, 10) 

GHSV_list = [36000] # [6000, 12000, 18000, 24000, 30000, 36000]

for GHSV in GHSV_list:
    n = len(parameter_data_dec_Ni)
    lowest_indices = np.argsort(LCOH_op_Ni_list_catO)[-n:]

    # LCOH ≤ 4.78인 값만 컬러맵 범위 기준으로 사용
    cut_value = 5.4
    valid_affcatcosts = [LCOH_op_Ni_list_catO[i] for i in lowest_indices if LCOH_op_Ni_list_catO[i] <= cut_value]

    vmin = min(valid_affcatcosts) if valid_affcatcosts else 0
    vmax = max(valid_affcatcosts) if valid_affcatcosts else 1

    cmap = cm.get_cmap('PiYG')
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    catalyst_names = [cat_Ni_name.iloc[i, 0] for i in lowest_indices]

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    max_y_value = float('-inf')

    for i in lowest_indices:
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_dec_table_{temp}_Ni"
                y_value = globals()[key][GHSV]['NH3 Conversion exp PFR(%)'][i]
                y_values.append(y_value)

                if y_value > max_y_value:
                    max_y_value = y_value

            except KeyError as e:
                print(f"KeyError for {temp} °C and i={i}: {e}")
            except Exception as e:
                print(f"Error for {temp} °C and i={i}: {e}")
                y_values.append(None)

        if len(y_values) == len(temperatures) and all(val is not None for val in y_values):
            if LCOH_op_Ni_list_catO[i] <= cut_value:
                color = cmap(norm(LCOH_op_Ni_list_catO[i]))
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

    # 범례 설정 (4.78 이하만 컬러, 초과는 회색)
    handles = [
        plt.Line2D([0], [0],
                   color=(cmap(norm(LCOH_op_Ni_list_catO[i])) if LCOH_op_Ni_list_catO[i] <= cut_value else 'gray'),
                   lw=2,
                   label=f"{catalyst_names[j]}")
        for j, i in enumerate(lowest_indices)
    ]
    legend = ax.legend(
        handles=handles,
        title="Catalyst Names",
        fontsize=13,
        loc='upper right',
        title_fontsize=17,
        bbox_to_anchor=(1.8, 1.1),
        ncol=1
    )

    ax.text(
        0.96, 0.07, 
        f"GHSV = {GHSV} Lh$^{{-1}}$kg$^{{-1}}$", 
        fontsize=20, 
        transform=ax.transAxes, 
        va='center', 
        ha='right',
        bbox=dict(facecolor='white', edgecolor='gray', alpha=0.5, boxstyle='round,pad=0.3')
    )

    if valid_affcatcosts:
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label("LCOH (USD/kg H$_2$)", fontsize=20, labelpad=15)
        cbar.ax.tick_params(labelsize=20)

    ax.set_xlabel("Temperature (°C)", fontsize=25)
    ax.set_ylabel("Lab-scale NH$_{3}$ Conversion (%)", fontsize=25)
    ax.set_title("Ni-based", fontsize=25)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=23)

    plt.show()




#%%
temperatures = range(500, 710, 10)
GHSV_list = [36000]
temperatures_50 = [500, 550, 600, 650, 700]
highlight_label_coords = [(600, 85), (600, 70), (600, 43), (600, 27), (600, 15)]  # 직접 조정한 텍스트 좌표

for GHSV in GHSV_list:
    n = len(parameter_data_dec_Ni)
    valid_indices = [i for i in range(n) if aff_cat_cost_dec_list[i] > 0 and LCOH_op_Ni_list_catO[i] > 0]
    sorted_by_lcoh = sorted(valid_indices, key=lambda i: LCOH_op_Ni_list_catO[i])
    n_valid = len(sorted_by_lcoh)

    quantile_indices = [
        # sorted_by_lcoh[0],
        # sorted_by_lcoh[n_valid // 4],
        # sorted_by_lcoh[n_valid // 2],
        # sorted_by_lcoh[3 * n_valid // 4],
        # sorted_by_lcoh[-1]
        sorted_by_lcoh[0],
        sorted_by_lcoh[4],
        sorted_by_lcoh[10],
        sorted_by_lcoh[12],
        sorted_by_lcoh[-5]

    ]

    highlighted_affcatcost = [aff_cat_cost_dec_list[i] for i in quantile_indices]
    vmin = min(highlighted_affcatcost)
    vmax = max(highlighted_affcatcost)
    cmap = cm.get_cmap('coolwarm')
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

    for i in valid_indices:
        y_values = []
        for temp in temperatures:
            try:
                key = f"dict_dec_table_{temp}_Ni"
                y_value = globals()[key][GHSV]['NH3 Conversion exp PFR(%)'][i]
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
                key = f"dict_dec_table_{temp}_Ni"
                y_value = globals()[key][GHSV]['NH3 Conversion exp PFR(%)'][i]
                y_values.append(y_value)
            except KeyError:
                y_values.append(None)

        if all(v is not None for v in y_values):
            color = cmap(norm(aff_cat_cost_dec_list[i]))
            adjusted_x, adjusted_y = highlight_label_coords[idx]

            gradients = np.gradient(np.array(y_values, dtype=np.float64), np.array(temperatures, dtype=np.float64))
            closest_idx = np.searchsorted(temperatures, adjusted_x) - 1
            if closest_idx < 0: closest_idx = 0
            x1, y1 = temperatures[:closest_idx + 1], y_values[:closest_idx + 1]
            x2, y2 = temperatures[closest_idx:], y_values[closest_idx:]

            ax.plot(x1, y1, color=color, linewidth=3, alpha=0.9)
            ax.plot(x2, y2, color=color, linewidth=3, alpha=0.9)

            ax.text(
                adjusted_x, adjusted_y, f"{aff_cat_cost_dec_list[i]:.0f}",
                fontsize=30, fontweight='bold', color=color,
                ha='center', va='center', rotation=0,
                bbox=dict(facecolor='white', edgecolor='none', alpha=1, boxstyle='round,pad=0')
            )

            catalyst_name = cat_Ni_name.iloc[i, 0]
            legend_elements.append(Line2D([0], [0], color=color, linewidth=4, label=catalyst_name))

    ax.set_xlabel("Temperature (°C)", fontsize=35)
    ax.set_ylabel("Lab-scale\nNH$_{3}$ Conversion (%)", fontsize=35)
    ax.set_title("Ni-based", fontsize=35)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', labelsize=30)

    ax.text(
        0.48, 0.88,
        f"GHSV = {GHSV} Lh$^{{-1}}$kg$^{{-1}}$",
        fontsize=25,
        transform=ax.transAxes,
        va='bottom',
        ha='right',
        bbox=dict(facecolor='white', edgecolor='gray', alpha=0.5, boxstyle='round,pad=0.3')
    )

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("ACCI (USD/kg catalyst)", fontsize=35, labelpad=15)
    cbar.ax.tick_params(labelsize=30)
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    ax.legend(
        handles=legend_elements,
        fontsize=30,
        loc='center left',
        bbox_to_anchor=(-0.1, -0.4),
        frameon=True,
        ncol=2
    )

    plt.show()


