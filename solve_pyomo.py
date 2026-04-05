import pyomo.environ as pyo

from vars import (
    TIMEPERIOD_HOURS,
    HOURLY_DEMAND_KG,
    TANK_SIZE_KG,
    P_RATED_KW,
    P_BOP_KW,
)
from functional import (
    hydrogen_production,
    hydrogen_production_cost,
    generate_electricity_price,
)

electricity_prices = generate_electricity_price()

model = pyo.ConcreteModel()
model.T = pyo.RangeSet(0, TIMEPERIOD_HOURS - 1)

model.c_electricity = pyo.Param(
    model.T, initialize=lambda m, t: float(electricity_prices[t])
)
model.p_set = pyo.Var(
    model.T, within=pyo.NonNegativeReals, bounds=(P_BOP_KW, P_RATED_KW)
)


def min_prod_rule(m, t):
    return (
        sum(hydrogen_production(m.p_set[tau]) for tau in range(t + 1))
        >= HOURLY_DEMAND_KG * t
    )


def max_prod_rule(m, t):
    return (
        sum(hydrogen_production(m.p_set[tau]) for tau in range(t + 1))
        <= HOURLY_DEMAND_KG * t + TANK_SIZE_KG
    )


model.min_production = pyo.Constraint(model.T, rule=min_prod_rule)
model.max_production = pyo.Constraint(model.T, rule=max_prod_rule)


def obj_rule(m):
    return sum(
        hydrogen_production_cost(m.p_set[t], m.c_electricity[t]) for t in m.T
    )


model.objective = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

# HiGHS via highspy (pip install highspy) — no separate GLPK/CBC binary needed
solver = pyo.SolverFactory("appsi_highs")
if not solver.available():
    raise RuntimeError("Install HiGHS bindings: pip install highspy")
results = solver.solve(model, load_solutions=False)
model.solutions.load_from(results)
print("Objective (EUR):", pyo.value(model.objective))
for t in model.T:
    print(f"p_set[{t}] = {pyo.value(model.p_set[t]):.6g} kW")
