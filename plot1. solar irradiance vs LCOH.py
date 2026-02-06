import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'

#%%
def sizing_factor_linear(ghi):
    return -0.0002682 * ghi + 1.7864

# sizing_factor_linear(1890) --> (1890, 1.28)
# sizing_factor_linear(1068) --> (1068, 1.5)


#%%
def soalrPV_LOCE(ghi_array,
                         ghi_base=2000,
                         #cf_base=0.31/1.25,  # capacity factor at base GHI
                         CAPEX=493_000, # USD/kW,DC
                         OandM=6_800, # USD/MW,DC/yr
                         WACC=0.075,
                         lifetime=25):

    PVF = (1 - (1 + WACC) ** -lifetime) / WACC

    # Step 1: Estimate CF for each GHI (assuming linear relationship)
    DCAC_sizing_factor = -0.0002682 * ghi_array + 1.7864 #sizing_factor_linear(ghi_array)
    cf_base= 0.31 / DCAC_sizing_factor  # capacity factor at base GHI
    cf_estimated = cf_base * (ghi_array / ghi_base)

    # Step 2: Annual energy production (AC rating)
    FLH_ac = cf_estimated * 8760  # full load hours (AC basis)
    E_total = FLH_ac * 1000 * PVF  # total discounted energy per MWp,DC

    # Step 3: Total cost and LCOE
    total_cost = CAPEX + OandM * PVF
    LCOE = total_cost / E_total
    return LCOE

# GHI range
ghi_range = np.linspace(800, 2900, 100)
lcoe_cf_based = soalrPV_LOCE(ghi_range)

# Plot
plt.figure(figsize=(5, 3.5), dpi=300)
plt.plot(ghi_range, lcoe_cf_based, lw=2, color='red')
#plt.axvline(2000, color='gray', linestyle='--', label='GHI = 2000')
#plt.axhline(0.0236, color='green', linestyle='--', label='LCOE = 0.0236 USD/kWh')
plt.xlabel("Solar irradiance (kWh/m$^{2}$/yr)",fontsize=12)
plt.ylabel("LCOE (USD/kWh)",fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(linestyle='--')
plt.tight_layout()
plt.show()


#%%
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
    E_total = FLH_ac * 1000 * PVF  # total discounted energy per MWp,DC

    # Step 3: Hydrogen production per MWp over stack lifetime
    H2_total = (FLH_ac * eff_electrolyzer * stack_lifetime_hours) / LHV_H2  # kg H2/MWp
   # H2_total = (E_total * eff_electrolyzer) / LHV_H2  # kg H2/MWp

    # Step 4: Total CAPEX and OPEX
    total_CAPEX = pv_CAPEX + CAPEX_electrolyzer * 1000  # USD/MWp
    total_OPEX = pv_OandM * PVF + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF  # USD/MWp over lifetime

    total_cost = total_CAPEX + total_OPEX  # USD/MWp over project life

    total_PV_cost = (pv_CAPEX +pv_OandM * PVF) / H2_total
    total_electrolyzer_cost = (CAPEX_electrolyzer * 1000 + CAPEX_electrolyzer * 1000 * O_M_ratio * PVF) / H2_total

    # Step 5: LCOH per kg H2
    lcoh = total_cost / H2_total  # USD/kg H2
    return lcoh, total_PV_cost, total_electrolyzer_cost

# GHI range
ghi_range = np.linspace(800, 2900, 100)
lcoh_total = solarPV_LOCH(ghi_range)[0]

# Plot
plt.figure(figsize=(5, 3.5), dpi=300)
plt.plot(ghi_range, lcoh_total, lw=2, color='green')
#plt.axvline(2000, color='gray', linestyle='--', label='GHI = 2000')
plt.xlabel("Solar irradiance (kWh/m$^{2}$/yr)", fontsize=12)
plt.ylabel("LCOH (USD/kg H$_{2}$)", fontsize=12)
#plt.legend()
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(linestyle='--')
plt.tight_layout()
plt.show()



print('rich',solarPV_LOCH(2350)[0])
print('poor',solarPV_LOCH(1491)[0])
print('dif',solarPV_LOCH(1491)[0]-solarPV_LOCH(2350)[0])




#%%
irradiance_range = range(800,2900,100)
solar_LCOH_calculation_list=[]
solar_PV_total_cost_calculation_list=[] 
electrolyzer_total_cost_calculation_list=[]

for irradiance in irradiance_range:
    solar_LCOH_calculation = solarPV_LOCH(irradiance)[0]
    solar_PV_total_cost = solarPV_LOCH(irradiance)[1]
    electrolyzer_total_cost = solarPV_LOCH(irradiance)[2]
    solar_LCOH_calculation_list.append(solar_LCOH_calculation)
    solar_PV_total_cost_calculation_list.append(solar_PV_total_cost)
    electrolyzer_total_cost_calculation_list.append(electrolyzer_total_cost)


# a + b/x 형태의 함수 정의
def func(x, a, b):
    return a + b / x

# 곡선 피팅
params, params_covariance = curve_fit(func, irradiance_range, solar_LCOH_calculation_list)

# 피팅된 모델의 예측값 계산
y_pred = func(irradiance_range, *params)

# 피팅된 파라미터 출력
print(f"Fitted parameters: a = {params[0]}, b = {params[1]}")

# 피팅된 파라미터와 R² 값 계산
r2 = r2_score(solar_LCOH_calculation_list, y_pred)
#equation_text = f'y = {params[0]:.3f} + {params[1]:.1f}/x\n$R^2$ = {r2:.1f}'
equation_text = f'y = {params[0]:.3f} + {params[1]:.1f}/x'


# 그래프 그리기
plt.figure(figsize=(5, 3.5), dpi=300)
plt.plot(irradiance_range, solar_LCOH_calculation_list, color='blue', label='LCOH Calculation', linewidth=3)
#plt.plot(irradiance_range, y_pred, color='red', linestyle='--', label='Fitted Line')

# 방정식과 R² 값 표시
plt.text(0.55, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="white"))

# 라벨 설정 및 기타 설정
plt.xlabel('Solar irradiance (kWh/m$^{2}$/yr)', fontsize=12)
plt.ylabel('LCOH (USD/kg H$_{2}$)', fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=12)
plt.grid(linestyle='--')
#plt.legend(fontsize=12)y
plt.show()


#%%#%% breakdown 모양 구분
irradiance_range = range(800,2900,100)
solar_LCOH_calculation_list=[]
solar_PV_total_cost_calculation_list=[] 
electrolyzer_total_cost_calculation_list=[]

for irradiance in irradiance_range:
    solar_LCOH_calculation = solarPV_LOCH(irradiance)[0]
    solar_PV_total_cost = solarPV_LOCH(irradiance)[1]
    electrolyzer_total_cost = solarPV_LOCH(irradiance)[2]
    solar_LCOH_calculation_list.append(solar_LCOH_calculation)
    solar_PV_total_cost_calculation_list.append(solar_PV_total_cost)
    electrolyzer_total_cost_calculation_list.append(electrolyzer_total_cost)


x_labels = [str(x) for x in irradiance_range]
x = np.arange(len(x_labels))  # x 위치

plt.figure(figsize=(13, 3.5), dpi=300)

# 예시 색상
solar_color = '#ff9999'        # pastel red
electrolyzer_color = '#a7c7e7' # pastel blue
line_color = 'black'

# 막대 그래프 생성 (색상 기반)
plt.bar(x, solar_PV_total_cost_calculation_list,
        label='Solar PV', color=solar_color)

plt.bar(x, electrolyzer_total_cost_calculation_list,
        bottom=solar_PV_total_cost_calculation_list,
        label='Electrolysis', color=electrolyzer_color)

# 합산된 비용 점 플롯
bar_tops = [solar_PV_total_cost_calculation_list[i] + electrolyzer_total_cost_calculation_list[i]
            for i in range(len(x))]

plt.plot(x, bar_tops, 'o-', color=line_color,
         label='Total Cost', linewidth=2, markersize=8)

# 라벨 및 스타일 설정
plt.xlabel('Solar irradiance (kWh/m$^{2}$/yr)', fontsize=17)
plt.ylabel('H$_{2}$ production cost\n(USD/kg H$_{2}$)', fontsize=17)
plt.xticks(x, x_labels, rotation=45, fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()




#%%
# =========================================================
# Solar irradiance vs H2 production cost (breakdown + regions)
# =========================================================
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Model-based cost calculation over irradiance range
# ---------------------------------------------------------
irradiance_range = range(800, 2900, 100)

solar_LCOH_calculation_list = []
solar_PV_total_cost_calculation_list = []
electrolyzer_total_cost_calculation_list = []

for irradiance in irradiance_range:
    solar_LCOH, solar_PV_cost, electrolyzer_cost = solarPV_LOCH(irradiance)
    solar_LCOH_calculation_list.append(solar_LCOH)
    solar_PV_total_cost_calculation_list.append(solar_PV_cost)
    electrolyzer_total_cost_calculation_list.append(electrolyzer_cost)

x_labels = [str(x) for x in irradiance_range]
x = np.arange(len(x_labels))

# ---------------------------------------------------------
# 2. Plot setup
# ---------------------------------------------------------
plt.figure(figsize=(13, 3.5), dpi=300)

solar_color = '#ff9999'
electrolyzer_color = '#a7c7e7'
line_color = 'black'

# ---------------------------------------------------------
# 3. Stacked bar plot (cost breakdown)
# ---------------------------------------------------------
plt.bar(x, solar_PV_total_cost_calculation_list,
        label='Solar PV', color=solar_color)

plt.bar(x, electrolyzer_total_cost_calculation_list,
        bottom=solar_PV_total_cost_calculation_list,
        label='Electrolysis', color=electrolyzer_color)

bar_tops = [
    solar_PV_total_cost_calculation_list[i] +
    electrolyzer_total_cost_calculation_list[i]
    for i in range(len(x))
]

plt.plot(x, bar_tops, 'o-', color=line_color,
         linewidth=2, markersize=7, label='Total cost')

# ---------------------------------------------------------
# 4. Region-specific H2 cost ranges
# ---------------------------------------------------------
region_data = {
    "Australia": (2351.25, None, None, 2.0, 4.0, "IRENA (2023)"),
    "Chile":     (1895.09, None, None, 2.5, 4.5, "IRENA (2023)"),
    "USA":       (1993.03, None, None, 2.5, 4.5, "IRENA (2023)"),
    "Japan":     (1588.63, None, None, 3.0, 5.0, "IRENA (2023)"),

    # Europe: irradiance range → horizontal error bar
    "EU":    (1261.06, 1097.07, 1425.05, 4.6, 9.1, "IRENA (2022)"),
}


def irradiance_to_x(val, irradiance_range):
    step = irradiance_range[1] - irradiance_range[0]
    return (val - irradiance_range[0]) / step

for region, (irr_c, irr_min, irr_max, low, high, source) in region_data.items():

    x_pos = irradiance_to_x(irr_c, irradiance_range)
    y_mid = 0.5 * (low + high)

    y_err = [[y_mid - low], [high - y_mid]]

    # 색상
    color = 'green' if source == "IRENA (2023)" else 'darkorange'

    # x-error (Europe only)
    if irr_min is not None and irr_max is not None:
        x_err = [[(irr_c - irr_min) / 100], [(irr_max - irr_c) / 100]]
    else:
        x_err = None

    plt.errorbar(
        x_pos,
        y_mid,
        xerr=x_err,          # 🔹 가로 에러바
        yerr=y_err,          # 🔹 세로 에러바
        fmt='o',
        color=color,
        ecolor=color,
        elinewidth=2,
        capsize=5,
        markersize=7
    )

    plt.text(
        x_pos - 0.3,
        y_mid - 1.5,
        region,
        fontsize=12,
        verticalalignment='center'
    )

# ---------------------------------------------------------
# 5. Legend handles for different IRENA sources
# ---------------------------------------------------------
plt.errorbar([], [], yerr=[[0], [0]],
             fmt='o', color='green',
             label='IRENA (2023)')

plt.errorbar([], [], yerr=[[0], [0]],
             fmt='o', color='darkorange',
             label='IRENA (2022)')

# ---------------------------------------------------------
# 6. Labels, legend, grid
# ---------------------------------------------------------
plt.xlabel('Solar irradiance (kWh/m$^{2}$/yr)', fontsize=17)
plt.ylabel('H$_2$ production cost\n(USD/kg H$_2$)', fontsize=17)

plt.xticks(x, x_labels, rotation=45, fontsize=15)
plt.yticks(fontsize=15)

plt.legend(fontsize=15, frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()





