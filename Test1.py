import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

df = pd.read_excel('RC_F30_04_2010_T01_04_2021.xlsx')

# sort by DT in ascending order 
df = df.sort_values(by='DT')

# extract the ruo column and convert from percentage to decimal
ruonia = df['ruo'].values / 100

#define the time step (assuming 252 trading days per year)
dt = 1 / 252qws

#define likelihood function for the Vasicek model
def neg_log_likelihood(params):
    a, b, sigma = params
    # Penalize invalid parameters (a and sigma must be positive)
    if a <= 0 or sigma <= 0:
        return np.inf
    # calculate mean and variance since we deal with Normal distribution we can express pdf in mean and var params.
    mean = ruonia[:-1] * np.exp(-a * dt) + b * (1 - np.exp(-a * dt))
    variance = (sigma**2 / (2 * a)) * (1 - np.exp(-2 * a * dt))
    #compute the likelihood
    log_lik = -0.5 * np.sum(np.log(2 * np.pi * variance) + (ruonia[1:] - mean)**2 / variance)
    return -log_lik

#initial parameter guesses
initial_params = [1, np.mean(ruonia), 1]

#define bounds: a > 0 b >= 0 , sigma > 0
bounds = [(0.001, None), (0, None), (0.001, None)]

# minimize the negative log-likelihood
result = minimize(neg_log_likelihood, initial_params, method='L-BFGS-B', bounds=bounds)

# extract the estimated parameters
a, b, sigma = result.x
#.x - atribute to show the solution for parameters 


print(f"Estimated parameters:")
print(f"a (speed of mean reversion): {a:.4f}")
print(f"b (long-term mean): {b:.4f}")
print(f"sigma (volatility): {sigma:.4f}")

#PART2

r0 = float(df['ruo'][0])/100
print(r0)
# Define Vasicek model functions
def B(T, a):
    return (1 - np.exp(-a * T)) / a

def A(T, a, b, sigma):
    term1 = (b - sigma**2 / (2 * a**2)) * (B(T, a) - T)
    term2 = (sigma**2 / (4 * a)) * B(T, a)**2
    return np.exp(term1 - term2)

def P(T, r0, a, b, sigma):
    return A(T, a, b, sigma) * np.exp(-B(T, a) * r0)
#ytm derivation
def ytm(T, r0, a, b, sigma):
    if T == 0:
        return r0
    else:
        return -np.log(P(T, r0, a, b, sigma)) / T

# Calculate YTM for a range of maturities
T_values = np.arange(0.01, 30, 0.1)
ytm_values = [ytm(T, r0, a, b, sigma) for T in T_values]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(T_values, np.array(ytm_values) * 100)  #convert yield to percentage
plt.xlim(0, 30)  #X-axis 
plt.ylim(0, 25)  #Y-axis
plt.xlabel("Maturity (years)")  # -axis
plt.ylabel("Yield (%)")  #Y-axis 
plt.title("Vasicek Model Yield Curve")
plt.grid(True)
plt.savefig('vasicek_yield_curve.png')  #Save