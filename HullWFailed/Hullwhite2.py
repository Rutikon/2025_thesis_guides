import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution

# Define bond data as a dictionary
bond_data = {
    'SU26207RMFS9': {'Maturity': '2027-02-03', 'YTM': 15.86},
    'SU26212RMFS9': {'Maturity': '2028-01-19', 'YTM': 15.1},
    'SU26218RMFS6': {'Maturity': '2031-09-17', 'YTM': 14.82},
    'SU26219RMFS4': {'Maturity': '2026-09-16', 'YTM': 16.18},
    'SU26221RMFS0': {'Maturity': '2033-03-23', 'YTM': 14.93},
    'SU26224RMFS4': {'Maturity': '2029-05-23', 'YTM': 14.76},
    'SU26225RMFS1': {'Maturity': '2034-05-10', 'YTM': 14.92},
    'SU26226RMFS9': {'Maturity': '2026-10-07', 'YTM': 16.12},
    'SU26228RMFS5': {'Maturity': '2030-04-10', 'YTM': 14.86},
    'SU26229RMFS3': {'Maturity': '2025-11-12', 'YTM': 18.4},
    'SU26230RMFS1': {'Maturity': '2039-03-16', 'YTM': 14.88},
    'SU26232RMFS7': {'Maturity': '2027-10-06', 'YTM': 15.53},
    'SU26233RMFS5': {'Maturity': '2035-07-18', 'YTM': 15.0},
    'SU26235RMFS0': {'Maturity': '2031-03-12', 'YTM': 14.83},
    'SU26236RMFS8': {'Maturity': '2028-05-17', 'YTM': 14.8},
    'SU26237RMFS6': {'Maturity': '2029-03-14', 'YTM': 14.81},
    'SU26238RMFS4': {'Maturity': '2041-05-15', 'YTM': 14.8},
    'SU26239RMFS2': {'Maturity': '2031-07-23', 'YTM': 14.87},
    'SU26240RMFS0': {'Maturity': '2036-07-30', 'YTM': 14.82},
    'SU26241RMFS8': {'Maturity': '2032-11-17', 'YTM': 14.88},
    'SU26242RMFS6': {'Maturity': '2029-08-29', 'YTM': 14.76},
    'SU26243RMFS4': {'Maturity': '2038-05-19', 'YTM': 15.19},
    'SU26244RMFS2': {'Maturity': '2034-03-15', 'YTM': 14.89},
    'SU26245RMFS9': {'Maturity': '2035-09-26', 'YTM': 15.24}
}

current_date = datetime(2025, 6, 21)

# Calculate maturities in years
maturities = []
market_ytms = []
for bond, data in bond_data.items():
    maturity_date = datetime.strptime(data['Maturity'], '%Y-%m-%d')
    time_to_maturity = (maturity_date - current_date).days / 365.25
    if time_to_maturity > 0:
        maturities.append(time_to_maturity)
        market_ytms.append(data['YTM'] / 100)  # Convert percentage to decimal

maturities = np.array(maturities)
market_ytms = np.array(market_ytms)

# Hull-White model functions
def integrand(s, T, a, sigma, b):
    B_s_T = (1 - np.exp(-a * (T - s))) / a
    theta_s = a * b + (2 * sigma**2 / a) * (np.exp(-a * s) - np.exp(-2 * a * s))
    return theta_s * B_s_T - (sigma**2 / (2 * a**2)) * (1 - np.exp(-a * (T - s)))**2

def bond_price(T, r0, a, sigma, b):
    B = (1 - np.exp(-a * T)) / a
    integral, _ = quad(integrand, 0, T, args=(T, a, sigma, b))
    return np.exp(integral - B * r0)

def model_ytm(T, r0, a, sigma, b):
    P = bond_price(T, r0, a, sigma, b)
    return -np.log(P) / T

# Objective function for calibration
def objective(params):
    r0, a, sigma, b = params
    model_yields = np.array([model_ytm(T, r0, a, sigma, b) for T in maturities])
    return np.sum((model_yields - market_ytms)**2)

# Parameter bounds: [r0, a, sigma, b]
bounds = [(0, 0.2), (0.01, 1.0), (0.01, 0.5), (-0.1, 0.1)]

# Optimize using differential_evolution for global minimum
result = differential_evolution(objective, bounds, strategy='best1bin', maxiter=1000, popsize=15)
r0_opt, a_opt, sigma_opt, b_opt = result.x

# Generate yield curve
T_range = np.linspace(0.1, max(maturities) + 1, 100)
yield_curve = [model_ytm(T, r0_opt, a_opt, sigma_opt, b_opt) * 100 for T in T_range]  # Convert to percentage

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(T_range, yield_curve, label='Hull-White Yield Curve', color='blue')
plt.scatter(maturities, market_ytms * 100, color='red', label='Market YTMs', zorder=5)
for i, bond in enumerate(bond_data.keys()):
    plt.annotate(bond, (maturities[i], market_ytms[i] * 100), xytext=(5, 5), textcoords='offset points')
plt.xlabel('Time to Maturity (Years)')
plt.ylabel('Yield to Maturity (%)')
plt.title('Hull-White Model Yield Curve')
plt.legend()
plt.grid(True)
plt.show()

print(f"Calibrated Parameters: r0 = {r0_opt:.4f}, a = {a_opt:.4f}, sigma = {sigma_opt:.4f}, b = {b_opt:.4f}")