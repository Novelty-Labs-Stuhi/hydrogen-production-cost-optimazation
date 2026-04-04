import math 
import numpy as np

def generate_electricity_price(N, sigma_cycle, sigma_noise, mu, dt):
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
    n_periods = N*24/dt
    times = np.arange(0, n_periods*dt, dt)
    noise = np.random.normal(0, sigma_noise, int(n_periods))
    cycle= sigma_cycle * np.sin(2*math.pi*times/24)
    price = mu + cycle + noise
    return price

def hydrogen_production(l,stack_efficiency,e_hhv,p_rated,time_step): 
    return time_step*l*p_rated*stack_efficiency/e_hhv

def hydrogen_production_cost(l,p_rated,time_step,price):
    electricity_cost=l*p_rated*price*time_step
    opex=1
    capex=1
    return electricity_cost+opex+capex
def objective_function(prices,production):
    return sum([hydrogen_production_cost(production[t],STACK_EFFICIENCY,E_HHV,P_RATED_KW,TIMESTEP,prices[t]) for t in range(len(prices))])
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

