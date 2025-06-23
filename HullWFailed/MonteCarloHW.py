import numpy as np
import matplotlib.pyplot as plt

# Parameters from your calibration (replace with actual values)
abar_opt = 0.1326  # Replace with your calibrated abar_opt value
sigma_bar_opt =  1.2313  # Replace with your calibrated sigma_bar_opt value

# Fixed Vasicek parameters from your code
r0 = 0.2339  # Initial short rate
a_vasicek = 5.3480
b = 0.1527
sigma_vasicek = 0.5921

# Hull-White parameters
a = abar_opt  # Mean reversion speed
sigma = sigma_bar_opt  # Volatility

# Define theta function as in your code
def theta(s, abar, sigma_bar):
    term1 = -a_vasicek * (r0 - b) * np.exp(-a_vasicek * s)
    term2 = - (sigma_vasicek**2 / a_vasicek) * (1 - np.exp(-a_vasicek * s)) * np.exp(-a_vasicek * s)
    term3 = abar * (b + (r0 - b) * np.exp(-a_vasicek * s) - (sigma_vasicek**2 / (2 * a_vasicek**2)) * (1 - np.exp(-a_vasicek * s))**2)
    term4 = (sigma_bar**2 / (2 * abar)) * (1 - np.exp(-2 * abar * s))
    return term1 + term2 + term3 + term4

# Simulation parameters
num_paths = 10  # Decreased to 10 paths as requested
T = 1 / 12  # 1 month in years (approximately 30 days)
N = 30  # Number of time steps (daily steps)
dt = T / N  # Time step size
times = np.linspace(0, T, N + 1)  # Time grid in years

# Simulate paths
paths = np.zeros((num_paths, N + 1))
paths[:, 0] = r0  # Initialize all paths with r0

for i in range(N):
    t_i = times[i]
    theta_i = theta(t_i, a, sigma)  # Compute theta at current time (same for all paths)
    drift = (theta_i - a * paths[:, i]) * dt  # Drift term (uses same theta_i for all paths)
    diffusion = sigma * np.sqrt(dt) * np.random.normal(size=num_paths)  # Diffusion term (random for each path)
    paths[:, i + 1] = paths[:, i] + drift + diffusion  # Update short rate
    # Ensure non-negative rates by setting negative values to zero
    paths[:, i + 1] = np.maximum(paths[:, i + 1], 0.0)

# Plot the simulated paths
plt.figure(figsize=(10, 6))
for path in paths:
    plt.plot(times, path, lw=1, alpha=0.6)
plt.xlabel('Time (Years)')
plt.ylabel('Short Rate')
plt.title('10 Simulated Hull-White Short Rate Paths Over 1 Month (Positive Rates)')
plt.grid(True)
plt.show()

# Optional: Print a sample path for verification
print("Sample Path (first path):")
print(paths[0])