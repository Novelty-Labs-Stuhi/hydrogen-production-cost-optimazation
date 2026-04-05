# Lavoit Linear Programming

The idea is to optimize the hydrogen production over the week, given the electricity price preditions.

I saw an opportunity to turn the setup into Linear Porgramming problem, through assuming a list of constants:

The constants are these:

- `TIMEPERIOD_DAYS`: how many days we optimize for.
- `TIMEPERIOD_HOURS`: the full horizon in hours.
- `TIMESTEP = \Delta t`: the size of one optimization step.
- `P_{\mathrm{rated}}`: rated power of the electrolyser.
- `P_{\mathrm{BOP}}`: the balance-of-plant power that is sort of always there.
- `D`: the hourly hydrogen demand.
- `T`: the max hydrogen tank size.
- `\eta`: stack efficiency.
- `E_{\mathrm{HHV}}`: hydrogen higher heating value, used in the production formula.
- `C_{\mathrm{stack}}`: stack cost.
- `C_{\mathrm{BOP}}`: balance-of-plant cost.
- `L_{\mathrm{stack}}`: stack lifetime in kWh terms.
- `L_{\mathrm{BOP}}`: BOP lifetime in hours.
- `c_t`: electricity price at time `t`.
- `N`: number of days used to generate the electricity price signal.
- `\mu`: average electricity price level.
- `\sigma_{\mathrm{cycle}}`: amplitude of the daily sinusoidal price cycle.
- `\sigma_{\mathrm{noise}}`: random noise on top of the cycle.

The two key functions of the process are Costs and Hydrogen Production.

The Costs vary with productiona and electricity price as follows:

$$
\mathrm{Cost}_t = \mathrm{CAPEX} + \mathrm{OPEX}_t + \mathrm{Electricity}_t
$$

$$
\mathrm{OPEX}_t = p_t \cdot \Delta t \cdot \frac{C_{\mathrm{stack}}}{L_{\mathrm{stack}}}
$$

$$
\mathrm{Electricity}_t = p_t \cdot c_t \cdot \Delta t
$$

The Production can be modeled through:

$$
\mathrm{H}_t = \frac{(p_t - P_{\mathrm{BOP}})\cdot \eta \cdot \Delta t}{E_{\mathrm{HHV}}}
$$

We assume some constant hourly demand, therefore the optimzation target is the total costs of producing the required hydrogen.

There is lower constraint on production: the demand must be satisified - either through direct production or tank storage.

$$
\sum_{\tau=0}^{t} \mathrm{H}_{\tau} \geq D \cdot t
$$

There is upper constraint on production: can't produc more than demand & maximum size of the tank.

$$
\sum_{\tau=0}^{t} \mathrm{H}_{\tau} \leq D \cdot t + T
$$

We can write the statement of the problem as:

$$
\min_{p_t} \sum_{t=0}^{N-1} \mathrm{Cost}_t
$$

subject to

$$
P_{\mathrm{BOP}} \leq p_t \leq P_{\mathrm{rated}}
$$

$$
\sum_{\tau=0}^{t} \mathrm{H}_{\tau} \geq D \cdot t
$$

$$
\sum_{\tau=0}^{t} \mathrm{H}_{\tau} \leq D \cdot t + T
$$
