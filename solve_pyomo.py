import pyomo.environ as pyo

from functional import (
    generate_electricity_price,
    hydrogen_production,
    hydrogen_production_cost,
)
from vars import (
    HOURLY_DEMAND_KG,
    P_BOP_KW,
    P_RATED_KW,
    TANK_SIZE_KG,
    TIMEPERIOD_HOURS,
)


P_BOP_SHARE = P_BOP_KW / P_RATED_KW


def solve_hydrogen_schedule(
    tank_size_kg,
    p_rated_kw,
    demand_kg_per_hour,
    electricity_prices=None,
):
    if electricity_prices is None:
        electricity_prices = generate_electricity_price()

    if len(electricity_prices) < TIMEPERIOD_HOURS:
        raise ValueError(
            "electricity_prices must contain at least TIMEPERIOD_HOURS values"
        )

    p_bop_kw = P_BOP_SHARE * p_rated_kw

    model = pyo.ConcreteModel()
    model.T = pyo.RangeSet(0, TIMEPERIOD_HOURS - 1)

    model.c_electricity = pyo.Param(
        model.T, initialize=lambda m, t: float(electricity_prices[t])
    )
    model.p_set = pyo.Var(
        model.T, within=pyo.NonNegativeReals, bounds=(p_bop_kw, p_rated_kw)
    )

    def min_prod_rule(m, t):
        return (
            sum(
                hydrogen_production(m.p_set[tau], p_bop_kw=p_bop_kw)
                for tau in range(t + 1)
            )
            >= demand_kg_per_hour * t
        )

    def max_prod_rule(m, t):
        return (
            sum(
                hydrogen_production(m.p_set[tau], p_bop_kw=p_bop_kw)
                for tau in range(t + 1)
            )
            <= demand_kg_per_hour * t + tank_size_kg
        )

    model.min_production = pyo.Constraint(model.T, rule=min_prod_rule)
    model.max_production = pyo.Constraint(model.T, rule=max_prod_rule)

    def obj_rule(m):
        return sum(
            hydrogen_production_cost(
                m.p_set[t], m.c_electricity[t], tank_size_kg=tank_size_kg
            )
            for t in m.T
        )

    model.objective = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

    solver = pyo.SolverFactory("appsi_highs")
    if not solver.available():
        raise RuntimeError("Install HiGHS bindings: pip install highspy")

    results = solver.solve(model, load_solutions=False)
    if results.solver.termination_condition != pyo.TerminationCondition.optimal:
        raise RuntimeError(
            f"Solver did not find an optimal solution: {results.solver.termination_condition}"
        )

    model.solutions.load_from(results)

    p_set_schedule = [pyo.value(model.p_set[t]) for t in model.T]
    hydrogen_cost_eur = pyo.value(model.objective)
    return p_set_schedule, hydrogen_cost_eur


if __name__ == "__main__":
    p_set_schedule, hydrogen_cost_eur = solve_hydrogen_schedule(
        tank_size_kg=TANK_SIZE_KG,
        p_rated_kw=P_RATED_KW,
        demand_kg_per_hour=HOURLY_DEMAND_KG,
    )
    print("Objective (EUR):", hydrogen_cost_eur)
    for t, p_set in enumerate(p_set_schedule):
        print(f"p_set[{t}] = {p_set:.6g} kW")
