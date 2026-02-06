import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import win32com.client as win32
import os
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import csv
from Economic_NH3 import *
from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
import time
from pymoo.core.callback import Callback
from pymoo.core.problem import ElementwiseProblem
from pymoo.termination import get_termination
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize

from Synthesis_Ru_def import *

wd = os.getcwd()

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Arial'

#%%

solar_irradiance_rich = 2351.25 #set #하나로 고정하고 돌려보기


#%%
# 🔹 Aspen 연결하는 함수
def connect_aspen(file_path):
    link = win32.gencache.EnsureDispatch("Apwn.Document")
    link.InitFromArchive2(os.path.abspath(file_path))
    link.Visible = False
    return link

# 🔹 Aspen 닫는 함수
def close_aspen(link):
    if link is not None:
        link.Close()

# 🔹 Aspen 파일 경로
path = os.getcwd()
file_path = '4. Aspen_file_overall_scaleup/Ammonia synthesis_overall_scaleup_v2.apw'



# 🔹 사용자 정의 콜백 (세대가 끝날 때마다 아스펜을 재연결)
class CustomCallback(Callback):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path  # 아스펜 파일 경로
        self.link = None  # 아스펜 연결

    def notify(self, algorithm):
        global link
        close_aspen(link)  # 아스펜 닫기
        time.sleep(2)  # 안정성을 위해 약간의 딜레이
        link = connect_aspen(self.file_path)  # 다시 연결
        print(f"Aspen 재연결 완료 (세대: {algorithm.n_gen})")





#%%
for j in range(0,len(parameter_data_syn_Ru),1): #len(parameter_data) #  j=0
    cat_idx = j
   
    # 🔹 첫 연결
    link = connect_aspen(file_path)
    
    from pymoo.core.problem import ElementwiseProblem 
    
    class MyProblem(ElementwiseProblem):
        def __init__(self, **kwargs):
            xl = np.array([250, 10, 100])   # T, P, GHSV
            xu = np.array([700, 300, 72000])  # T, P, GHSV
            
            super().__init__(n_var=3, n_obj=1, n_constr=0, xl=xl, xu=xu, **kwargs)
    
        def _evaluate(self, X, out, *args, **kwargs):
            T = X[0]
            P = X[1]
            GHSV = X[2]
    

            result = sim_NH3_syn_Ru(link, solar_irradiance_rich, cat_idx, T, P, GHSV)
            
            # 목적함수 
            f1 = np.nan_to_num(result['LCOA']['LCOA_catO'], nan=1e6, posinf=1e6, neginf=1e6)
    
            # 제약조건
            #g1 = target_pu - result[1]
    
            out["F"] = [f1]
            #out["G"] = [g1]
            
    
                                                
    
    problem = MyProblem()
    
    from pymoo.termination import get_termination
    termination = get_termination("n_gen", 15)
    
    #Initilized algorithm
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.operators.crossover.sbx import SBX
    from pymoo.operators.mutation.pm import PM
    from pymoo.operators.sampling.rnd import FloatRandomSampling
    
    algorithm = NSGA2(
        pop_size=30,
        n_offsprings=30,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )
    callback = CustomCallback(file_path)  # 🔹 Callback 추가


    start = time.time()
    from pymoo.optimize import minimize
    print("start optimization")
    res = minimize(problem,
                   algorithm,
                  termination,
                  seed=1,
                   save_history=True,
                   verbose=True,
                   callback=callback)  # 🔹 Callback 적용
    
    hist = res.history
    
    
    X1 = res.X
    
    X1 = res.X
    if X1.ndim == 1 or X1.shape[1] == 1:  # X1이 1차원 배열이거나 열이 1개인 경우
        T_opt = X1[0]
        P_opt = X1[1]
        GHSV_opt = X1[2]
    else:  # X1이 2차원이고, 열이 2개 이상인 경우
        T_opt = X1[0,0]
        P_opt = X1[0,1]
        GHSV_opt = X1[0,2]
        
    # 최적 지점에서의 파라미터로 재계산
    best_result = sim_NH3_syn_Ru(link, solar_irradiance_rich, cat_idx, T_opt, P_opt, GHSV_opt)



    # 결과 저장 경로 설정
    wd = os.getcwd()
    save_path = os.path.join(wd, f"Optimization_results_catX/Syn/Ru_v3/cat{j}.pkl")
    # pkl로 저장
    with open(save_path, 'wb') as f:
        pickle.dump(best_result, f)


    close_aspen(link)  # 마지막으로 아스펜 닫기

