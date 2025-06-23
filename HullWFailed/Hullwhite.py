import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
from datetime import datetime
import matplotlib.pyplot as plt

# Define bond data as a dictionary
bond_data = {'SU26207RMFS9': {'Maturity': '2027-02-03', 'YTM': 15.86},
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
 'SU26245RMFS9': {'Maturity': '2035-09-26', 'YTM': 15.24}}
#Set current date (as per problem context)

# Set the current date (assumed as today's date)
current_date = datetime(2025, 6, 21)  # Adjust this date as necessary

# Calculate maturities and YTMs (corrected date parsing)
maturities = []
ytms = []
for bond in bond_data.values():
    # Corrected format string (removed extra space)
    maturity_date = datetime.strptime(bond['Maturity'], '%Y-%m-%d')
    if maturity_date > current_date:
        T = (maturity_date - current_date).days / 365.25
        maturities.append(T)
        ytms.append(bond['YTM'] / 100)  # Convert to decimal

maturities = np.array(maturities)
ytms = np.array(ytms)

# Define integrand for A(0,T) computation (CORRECT)
def integrand(s, T, a, sigma, alpha, beta):
    B_s_T = (1 - np.exp(-a * (T - s))) / a
    theta_s = alpha + beta * s
    return theta_s * B_s_T - (sigma**2 / (2 * a**2)) * (1 - np.exp(-a*(T-s)))**2

# Compute zero-coupon bond price P(0,T) (FIXED)
def bond_price(T, r0, a, sigma, alpha, beta):
    if T <= 1e-6:  # Handle near-zero maturity
        return 1.0
        
    B = (1 - np.exp(-a * T)) / a
    integral, _ = quad(integrand, 0, T, args=(T, a, sigma, alpha, beta))
    
    # CORRECTED Hull-White formula:
    return np.exp(integral - B * r0)

# Compute yield-to-maturity (FIXED)
def ytm(T, r0, a, sigma, alpha, beta):
    if T <= 1e-6:
        return r0
    P = bond_price(T, r0, a, sigma, alpha, beta)
    # Explicit formula for clarity:
    return (-1/T) * np.log(P)

# Objective function (CORRECT)
def objective(params):
    r0, a, sigma, alpha, beta = params
    sse = 0
    for T, y_obs in zip(maturities, ytms):
        y_pred = ytm(T, r0, a, sigma, alpha, beta)
        sse += (y_pred - y_obs)**2
    return sse

# Better initial parameters for high-yield market
initial_params = [0.05,   # r0 (10% initial guess)
                  0.1,    # a (mean reversion)
                  0.005,   # sigma (5% volatility)
                  0.05,   # alpha (long-term mean level)
                  0.001]  # beta (slope)

# More realistic bounds
bounds = [
    (0.05, 0.20),    # r0: 5-20%
    (0.01, 5.0),     # a: weak to strong mean reversion
    (0.01, 0.20),    # sigma: 1-20% volatility
    (0.05, 0.25),    # alpha: long-term rate level
    (-0.05, 0.05)    # beta: gentle slope
]

# Optimize with more robust method
result = minimize(
    objective, 
    initial_params, 
    bounds=bounds, 
    method='trust-constr',  # Better for constrained problems
    options={'maxiter': 1000}
)

# Extract and print results (same as before)
r0_opt, a_opt, sigma_opt, alpha_opt, beta_opt = result.x
print(f"Optimized Parameters:\nr0={r0_opt:.4f}\na={a_opt:.4f}\nsigma={sigma_opt:.4f}")
print(f"alpha={alpha_opt:.4f}\nbeta={beta_opt:.4f}\nSSE={result.fun:.6f}")

# Compute and compare yields
fitted_yields = [ytm(T, r0_opt, a_opt, sigma_opt, alpha_opt, beta_opt) 
                for T in maturities]
print("\nMaturity (Yrs) | Observed YTM | Fitted YTM | Difference")
for T, y_obs, y_fit in zip(maturities, ytms, fitted_yields):
    print(f"{T:.2f} | {y_obs:.4f} | {y_fit:.4f} | {y_fit-y_obs:.4f}")


print(f"Estimated parameters:")
print(f"r0 (short-term interest rate): {r0_opt:.4f}")
print(f"a (speed of mean reversion): {a_opt:.4f}")
print(f"sigma (volatility): {sigma_opt:.4f}")
print(f"alpha (long-term level): {alpha_opt:.4f}")
print(f"beta (slope): {beta_opt:.4f}")

# Calculate YTM for a range of maturities
T_values = np.arange(0.01, 30, 0.1)
ytm_values = [ytm(T, r0_opt, a_opt, sigma_opt, alpha_opt, beta_opt) for T in T_values]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(T_values, np.array(ytm_values) * 100, 
         label='Hull-White Model Yield Curve', linewidth=2.5, color='navy')
plt.scatter(maturities, np.array(ytms) * 100, 
            color='red', s=70, label='Observed Bond YTMs', zorder=5)

# Add annotations for selected bonds
annotated_bonds = ['SU26219RMFS4', 'SU26229RMFS3', 'SU26238RMFS4']
for bond_id, data in bond_data.items():
    if bond_id in annotated_bonds:
        maturity_date = datetime.strptime(data['Maturity'], '%Y-%m-%d')
        T = (maturity_date - current_date).days / 365.25
        y = data['YTM']
        plt.annotate(f'{bond_id}\n{data["Maturity"]}', 
                     (T, y), 
                     xytext=(T+1, y-0.5), 
                     arrowprops=dict(arrowstyle='->', color='gray'),
                     fontsize=9)

plt.xlim(0, 30)
plt.ylim(10, 25)
plt.xlabel("Maturity (years)", fontsize=12)
plt.ylabel("Yield (%)", fontsize=12)
plt.title("Hull-White Model Yield Curve Fitted to Russian Corporate Bonds", fontsize=14)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('hull_white_yield_curve.png', dpi=300)
plt.show()