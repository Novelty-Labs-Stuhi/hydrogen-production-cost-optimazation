import matplotlib.pyplot as plt

from functional import generate_electricity_price, hydrogen_production
from solve_pyomo import solve_hydrogen_schedule
from vars import P_RATED_KW, TIMEPERIOD_HOURS


TANK_SIZES_KG = list(range(0, 101, 20))
DEMAND_RATIOS = [step / 10 for step in range(1, 11)]


def compare_tank_and_demand():
    electricity_prices = generate_electricity_price()
    rated_hourly_hydrogen_kg = hydrogen_production(P_RATED_KW)
    results = []

    for tank_size_kg in TANK_SIZES_KG:
        for demand_ratio in DEMAND_RATIOS:
            demand_kg_per_hour = demand_ratio * rated_hourly_hydrogen_kg
            total_demand_kg = demand_kg_per_hour * (TIMEPERIOD_HOURS - 1)
            p_set_schedule, hydrogen_cost_eur = solve_hydrogen_schedule(
                tank_size_kg=tank_size_kg,
                p_rated_kw=P_RATED_KW,
                demand_kg_per_hour=demand_kg_per_hour,
                electricity_prices=electricity_prices,
            )
            results.append(
                {
                    "tank_size_kg": tank_size_kg,
                    "demand_ratio": demand_ratio,
                    "demand_kg_per_hour": demand_kg_per_hour,
                    "total_demand_kg": total_demand_kg,
                    "p_set_schedule": p_set_schedule,
                    "hydrogen_cost_eur": hydrogen_cost_eur,
                    "hydrogen_cost_eur_per_kg": hydrogen_cost_eur / total_demand_kg,
                }
            )

    return results


def plot_hydrogen_cost_vs_demand_share(results):
    for tank_size_kg in TANK_SIZES_KG:
        tank_results = [
            result for result in results if result["tank_size_kg"] == tank_size_kg
        ]
        tank_results.sort(key=lambda result: result["demand_ratio"])

        demand_ratios = [result["demand_ratio"] for result in tank_results]
        hydrogen_costs = [
            result["hydrogen_cost_eur_per_kg"] for result in tank_results
        ]

        plt.plot(demand_ratios, hydrogen_costs, marker="o", label=f"{tank_size_kg} kg")

    plt.xlabel("Demand share")
    plt.ylabel("Hydrogen cost (EUR/kg)")
    plt.title("Hydrogen Cost per kg vs Demand Share for Different Tank Sizes")
    plt.legend(title="Tank size")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = compare_tank_and_demand()
    for result in results:
        print(
            f"tank_size_kg={result['tank_size_kg']}, "
            f"demand_ratio={result['demand_ratio']:.1f}, "
            f"demand_kg_per_hour={result['demand_kg_per_hour']:.6f}, "
            f"hydrogen_cost_eur={result['hydrogen_cost_eur']:.6f}, "
            f"hydrogen_cost_eur_per_kg={result['hydrogen_cost_eur_per_kg']:.6f}"
        )
    plot_hydrogen_cost_vs_demand_share(results)
