import math 
import numpy as np

from vars import COST_STACK_EUR, COST_BOP_EUR, LIFETIME_STACK_KWH, LIFETIME_BOP_H, TIMESTEP, P_BOP_KW, STACK_EFFICIENCY, E_HHV, P_RATED_KW, N, SIGMA_CYCLE, SIGMA_NOISE, MU



def hydrogen_production_cost(p_set,c_electricity):
    "Return the cost of hydrogen production in EUR"
    capex=COST_BOP_EUR*(LIFETIME_BOP_H/TIMESTEP)
    opex=p_set*TIMESTEP*COST_STACK_EUR/LIFETIME_STACK_KWH
    electricity=p_set*c_electricity*TIMESTEP
    return capex+opex+electricity
def hydrogen_production(p_set):
    "Return the amount of hydrogen produced in kg"
    return (p_set-P_BOP_KW)*3600*STACK_EFFICIENCY*TIMESTEP/E_HHV


def generate_electricity_price():
    """
    Generate a random electricity price using simply sinusoid + Gaussian noise on N days (periods) with time step dt.
    parameters:
        N: number of days (periods)
        sigma: standard deviation of the Gaussian noise
        mu: mean of the sinusoid
        dt: time step (hours)
    returns:
        a list of electricity prices
    """
    n_periods = N*24/TIMESTEP
    times = np.arange(0, n_periods*TIMESTEP, TIMESTEP)
    noise = np.random.normal(0, SIGMA_NOISE, int(n_periods))
    cycle= SIGMA_CYCLE * np.sin(2*math.pi*times/24)
    price = MU + cycle + noise
    return price


if __name__ == "__main__":
    N = 7
    sigma_cycle = 10
    sigma_noise = 10
    mu = 100
    dt = 1 # 1 hour
    prices = generate_electricity_price(N, sigma_cycle, sigma_noise, mu, dt)
    import matplotlib.pyplot as plt
    plt.plot(prices)
    plt.show() 
    print(prices)

