P_RATED_KW=1*10**3 # KW (from Jacob's letter: 1MW)
CAPEX_TOTAL_EUR=2*10**6 # EUR (from Jacob's letter: 2M EUR)



TIMEPERIOD_DAYS=7
TIMEPERIOD_HOURS=TIMEPERIOD_DAYS*24
TIMESTEP=1
HOURLY_DEMAND_KG=10
TANK_SIZE_KG=10000

STACK_EFFICIENCY=0.55 # source3
E_HHV=141.8*10**3 # kJ/kg
P_BOP_KW=P_RATED_KW*0.10 # source4


COST_STACK_EUR_KW=(1071-384)/2 # source:
COST_STACK_EUR=COST_STACK_EUR_KW*P_RATED_KW

COST_BOP_EUR=CAPEX_TOTAL_EUR-COST_STACK_EUR
LIFETIME_STACK_KWH=4*10**6 # source2 
LIFETIME_BOP_H=15*365*24 # Jacob's letter: 15 years

#Electricity prices
N=7
SIGMA_CYCLE=10
SIGMA_NOISE=10
MU=100



#SOURCES:
#Source 1: https://www.researchgate.net/publication/371160750_Present_and_future_cost_of_alkaline_and_PEM_electrolyser_stacks/link/64a56fab95bbbe0c6e16aa45/download?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19
#Source 2: https://cordis.europa.eu/project/id/256721/reporting#:~:text=Economical%20use%20of%20PEM%20fuel,as%20the%20initial%20investment%20cost.
#Source 3: https://www.sciencedirect.com/science/article/abs/pii/S0360319924034852
#Source 4: https://reference-global.com/download/article/10.2478/lpts-2026-0011.pdf "BOP inefficiencies can reduce net system efficiency by up to 10 percentage points"