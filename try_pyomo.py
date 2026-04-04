imoprt pyomo.environ as pyo
from vars import TIMEPERIOD_DAYS, TIMEPERIOD_HOURS, TIMESTEP, HOURLY_DEMAND_KG, TANK_SIZE_KG, P_RATED_KW, STACK_EFFICIENCY, E_HHV
from functional import hydrogen_production

model = pyo.ConcreteModel()

for t in range(TIMEPERIOD_HOURS):
    model.l[t] = pyo.Var(within=pyo.NonNegativeReals)

for t in range(TIMEPERIOD_HOURS):
    model.min_production[t] = pyo.Constraint(expr=sum([hydrogen_production(model.l[_t],STACK_EFFICIENCY,E_HHV,P_RATED_KW,TIMESTEP) for _t in range(t+1)]) >= HOURLY_DEMAND_KG*t)
    model.max_production[t] = pyo.Constraint(expr=sum([hydrogen_production(model.l[_t],STACK_EFFICIENCY,E_HHV,P_RATED_KW,TIMESTEP) for _t in range(t+1)]) <= HOURLY_DEMAND_KG*t + TANK_SIZE_KG)

model.objective = pyo.Objective(expr=sum([model.x[t]*model.price[t] for t in range(TIMEPERIOD_HOURS)]))

solver = pyo.SolverFactory('glpk')
solver.solve(model)

print(model.objective())
print(model.x.value)