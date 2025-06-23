import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
# Bond data
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

# Current date
current_date = datetime(2025, 6, 21)

# Calculate maturities in years
maturities = []
market_ytms = []
for bond, data in bond_data.items():
    maturity_date = datetime.strptime(data['Maturity'], '%Y-%m-%d')
    time_to_maturity = (maturity_date - current_date).days / 365.25
    if time_to_maturity > 0:
        maturities.append(time_to_maturity)
        market_ytms.append(data['YTM'] / 100)
maturities = np.array(maturities)
market_ytms = np.array(market_ytms)

# Fixed Vasicek parameters
#r0 = 0.2339
r0 = 0.2
a = 5.3480
b = 0.1527
sigma = 0.5921

# Theta function
def theta(s, abar, sigma_bar):
    term1 = -a * (r0 - b) * np.exp(-a * s)
    term2 = -(sigma**2 / a) * (1 - np.exp(-a * s)) * np.exp(-a * s)
    term3 = abar * (b + (r0 - b) * np.exp(-a * s) - (sigma**2 / (2 * a**2)) * (1 - np.exp(-a * s))**2)
    term4 = (sigma_bar**2 / (2 * abar)) * (1 - np.exp(-2 * abar * s))
    return term1 + term2 + term3 + term4

# Integrand for bond price
def integrand(s, T, abar, sigma_bar):
    B_s_T = (1 - np.exp(-abar * (T - s))) / abar
    theta_s = theta(s, abar, sigma_bar)
    return theta_s * B_s_T - (sigma_bar**2 / 2) * B_s_T**2

# Bond price function
def bond_price(T, abar, sigma_bar):
    integral, _ = quad(integrand, 0, T, args=(T, abar, sigma_bar), epsabs=1e-6)
    B_0_T = (1 - np.exp(-abar * T)) / abar
    return np.exp(integral - B_0_T * r0)

# Model YTM function
def model_ytm(T, abar, sigma_bar):
    if T <= 0:
        return r0
    P = bond_price(T, abar, sigma_bar)
    return -np.log(P) / T

# Objective function (SSE)
def objective(params):
    abar, sigma_bar = params
    model_yields = np.array([model_ytm(T, abar, sigma_bar) for T in maturities])
    return np.sum((model_yields - market_ytms)**2)

# Calibrate using np.minimize
bounds = [(0.01, 10.0), (0.05, 2.0)]
result = differential_evolution(objective, bounds, strategy='best1bin', maxiter=300, popsize=100)

if result.success:
    abar_opt, sigma_bar_opt = result.x
    print(f"Calibrated Hull-White Parameters: abar = {abar_opt:.4f}, sigma_bar = {sigma_bar_opt:.4f}")
    print(f"Objective Function Value: {result.fun:.6f}")
else:
    print("Optimization failed:", result.message)

# Monte Carlo simulation for 30 days
num_paths = 10
days = 30
T = days / 365.25  # Time in years
N = days  # One step per day
dt = T / N
time_grid = np.linspace(0, T, N + 1)
days_grid = np.linspace(0, days, N + 1)

# Initialize paths
paths = np.zeros((num_paths, N + 1))
paths[:, 0] = r0

# Simulate paths
for i in range(N):
    t = time_grid[i]
    theta_t = theta(t, abar_opt, sigma_bar_opt)
    dr = (theta_t - abar_opt * paths[:, i]) * dt + sigma_bar_opt * np.sqrt(dt) * np.random.normal(size=num_paths)
    paths[:, i + 1] = paths[:, i] + dr  # No positivity constraint, allowing negative rates

# Plot simulated paths
plt.figure(figsize=(10, 6))
for k in range(num_paths):
    plt.plot(days_grid, paths[k, :] * 100, lw=1, label=f'Path {k+1}' if k < 5 else None)  # Limit legend entries
plt.xlabel('Time (Days)')
plt.ylabel('Short Rate (%)')
plt.title('Hull-White Short Rate Paths over 30 Days')
plt.grid(True)
plt.legend()
plt.show()