import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime

# Bond data as provided
#bond_data = {
 #   'SU26207RMFS9': {'Maturity': '2027-02-03', 'YTM': 16.15},
  #  'SU26212RMFS2': {'Maturity': '2030-08-15', 'YTM': 15.75},
    # Add more bonds as per your dataset
#}

bond_data = {'SU26207RMFS9': {'Maturity': '2027-02-03', 'YTM': 16.15},
 'SU26212RMFS9': {'Maturity': '2028-01-19', 'YTM': 15.42},
 'SU26218RMFS6': {'Maturity': '2031-09-17', 'YTM': 15.22},
 'SU26219RMFS4': {'Maturity': '2026-09-16', 'YTM': 16.77},
 'SU26221RMFS0': {'Maturity': '2033-03-23', 'YTM': 15.24},
 'SU26224RMFS4': {'Maturity': '2029-05-23', 'YTM': 15.11},
 'SU26225RMFS1': {'Maturity': '2034-05-10', 'YTM': 15.15},
 'SU26226RMFS9': {'Maturity': '2026-10-07', 'YTM': 16.66},
 'SU26228RMFS5': {'Maturity': '2030-04-10', 'YTM': 15.19},
 'SU26229RMFS3': {'Maturity': '2025-11-12', 'YTM': 18.31},
 'SU26230RMFS1': {'Maturity': '2039-03-16', 'YTM': 15.06},
 'SU26232RMFS7': {'Maturity': '2027-10-06', 'YTM': 15.81},
 'SU26233RMFS5': {'Maturity': '2035-07-18', 'YTM': 15.25},
 'SU26235RMFS0': {'Maturity': '2031-03-12', 'YTM': 15.17},
 'SU26236RMFS8': {'Maturity': '2028-05-17', 'YTM': 15.08},
 'SU26237RMFS6': {'Maturity': '2029-03-14', 'YTM': 15.2},
 'SU26238RMFS4': {'Maturity': '2041-05-15', 'YTM': 14.89},
 'SU26239RMFS2': {'Maturity': '2031-07-23', 'YTM': 15.23},
 'SU26240RMFS0': {'Maturity': '2036-07-30', 'YTM': 15.07},
 'SU26241RMFS8': {'Maturity': '2032-11-17', 'YTM': 15.17},
 'SU26242RMFS6': {'Maturity': '2029-08-29', 'YTM': 15.2},
 'SU26243RMFS4': {'Maturity': '2038-05-19', 'YTM': 15.39},
 'SU26244RMFS2': {'Maturity': '2034-03-15', 'YTM': 15.21},
 'SU26245RMFS9': {'Maturity': '2035-09-26', 'YTM': 15.5}}
# Set current date (as per problem context)
current_date = datetime(2025, 6, 18)

# Calculate time to maturity in years
maturities = []
ytms = []
for bond in bond_data.values():
    maturity_date = datetime.strptime(bond['Maturity'], '%Y-%m-%d')
    T = (maturity_date - current_date).days / 365.25
    if T > 0:  # Ensure bond has not matured
        maturities.append(T)
        ytms.append(bond['YTM'] / 100)  # Convert YTM from % to decimal

# Define Vasicek model functions
def B(T, a):
    return (1 - np.exp(-a * T)) / a

def A(T, a, b, sigma):
    term1 = (b - sigma**2 / (2 * a**2)) * (B(T, a) - T)
    term2 = (sigma**2 / (4 * a)) * B(T, a)**2
    return np.exp(term1 - term2)

def P(T, r0, a, b, sigma):
    return A(T, a, b, sigma) * np.exp(-B(T, a) * r0)

def ytm(T, r0, a, b, sigma):
    if T == 0:
        return r0
    else:
        return -np.log(P(T, r0, a, b, sigma)) / T

# Define objective function for optimization
def objective(params):
    r0, a, b, sigma = params
    sse = 0
    for T, y in zip(maturities, ytms):
        predicted_ytm = ytm(T, r0, a, b, sigma)
        sse += (predicted_ytm - y)**2
    return sse

# Initial parameter guesses
initial_params = [0.05, 1, 0.05, 0.01]  # [r0, a, b, sigma]

# Define bounds: r0 >= 0, a > 0, b >= 0, sigma > 0
bounds = [(0, None), (0.001, None), (0, None), (0.001, None)]

# Minimize the objective function
result = minimize(objective, initial_params, method='L-BFGS-B', bounds=bounds)

# Extract estimated parameters
r0, a, b, sigma = result.x

# Print estimated parameters
print(f"Estimated parameters:")
print(f"r0 (short-term interest rate): {r0:.4f}")
print(f"a (speed of mean reversion): {a:.4f}")
print(f"b (long-term mean): {b:.4f}")
print(f"sigma (volatility): {sigma:.4f}")

# Calculate YTM for a range of maturities
T_values = np.arange(0.01, 30, 0.1)
ytm_values = [ytm(T, r0, a, b, sigma) for T in T_values]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(T_values, np.array(ytm_values) * 100, label='Vasicek Model Yield Curve')
plt.scatter(maturities, np.array(ytms) * 100, color='red', label='Observed Bond YTMs')
plt.xlim(0, 30)
plt.ylim(0, 25)
plt.xlabel("Maturity (years)")
plt.ylabel("Yield (%)")
plt.title("Vasicek Model Yield Curve Fitted to Bond Data")
plt.legend()
plt.grid(True)
plt.savefig('vasicek_yield_curve_bonds.png')
plt.show()
