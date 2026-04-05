P_RATED_KW=1*10**3 # KW (from Jacob's letter: 1MW)
CAPEX_TOTAL_EUR=2*10**6 # EUR (from Jacob's letter: 2M EUR)



TIMEPERIOD_DAYS=7
TIMEPERIOD_HOURS=TIMEPERIOD_DAYS*24
TIMESTEP=1
HOURLY_DEMAND_KG=10
TANK_SIZE_KG=100
TANK_COST_EUR_KG=150 # source5

STACK_EFFICIENCY=0.55 # source3
E_HHV=141.8*10**3 # kJ/kg
P_BOP_KW=P_RATED_KW*0.10 # source4


COST_STACK_EUR_KW=(1071-384)/2 # source:
COST_STACK_EUR=COST_STACK_EUR_KW*P_RATED_KW

COST_BOP_EUR=CAPEX_TOTAL_EUR-COST_STACK_EUR
LIFETIME_STACK_KWH=4*10**6 # source2 
LIFETIME_BOP_H=15*365*24 # Jacob's letter: 15 years

#Electricity prices
N=TIMEPERIOD_DAYS
SIGMA_CYCLE=0.1 # EUR/kWh, about 100 EUR/MWh daily swing
SIGMA_NOISE=0.01 # EUR/kWh, about 10 EUR/MWh random noise
MU=0.07 # EUR/kWh, about 70 EUR/MWh average electricity price



#SOURCES:
#Source 1: https://www.researchgate.net/publication/371160750_Present_and_future_cost_of_alkaline_and_PEM_electrolyser_stacks/link/64a56fab95bbbe0c6e16aa45/download?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19
#Source 2: https://cordis.europa.eu/project/id/256721/reporting#:~:text=Economical%20use%20of%20PEM%20fuel,as%20the%20initial%20investment%20cost.
#Source 3: https://www.sciencedirect.com/science/article/abs/pii/S0360319924034852
#Source 4: https://reference-global.com/download/article/10.2478/lpts-2026-0011.pdf "BOP inefficiencies can reduce net system efficiency by up to 10 percentage points"
#Source 5: https://www.researchgate.net/post/Good_evening_Does_anyone_have_any_ideas_on_the_price_of_hydrogen_tanks_per_kg_and_the_price_of_fuel_cells_per_kW_and_the_price_of_electrolyzer#:~:text=Hydrogen%20storage%20tanks%E2%80%94especially%20those,techniques%2C%20and%20mass%20production%20strategies.