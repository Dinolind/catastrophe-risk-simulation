import pandas as pd
import numpy as np


# Make simulation reproducible
np.random.seed(42)


# ---------------------------
# 1. Load historical hurricanes
# ---------------------------

hurricanes = pd.read_csv(
    "data/processed/hurricanes.csv"
)


# Use 2016-2024 because 2025 is an outlier
hurricanes = hurricanes[
    hurricanes["year"] < 2025
]


# Historical hurricane losses
historical_losses = hurricanes[
    "property_damage"
].to_numpy()


# ---------------------------
# 2. Frequency assumption
# ---------------------------

# Historical average:
# 373 hurricane records / 9 years ≈ 41.4 hurricanes/year
annual_frequency = 41.44


# ---------------------------
# 3. Simulation settings
# ---------------------------

num_simulations = 10000

annual_losses = []


# ---------------------------
# 4. Monte Carlo simulation
# ---------------------------

for simulation in range(num_simulations):

    # Number of hurricanes this year
    number_of_hurricanes = np.random.poisson(
        annual_frequency
    )

    # Randomly select historical hurricane severities
    simulated_losses = np.random.choice(
        historical_losses,
        size=number_of_hurricanes,
        replace=True
    )

    # Total catastrophe damage during the simulated year
    total_loss = simulated_losses.sum()

    annual_losses.append(total_loss)


annual_losses = np.array(annual_losses)


# ---------------------------
# 5. Risk metrics
# ---------------------------

expected_loss = annual_losses.mean()

var_95 = np.percentile(
    annual_losses,
    95
)

var_99 = np.percentile(
    annual_losses,
    99
)

tvar_99 = annual_losses[
    annual_losses >= var_99
].mean()


# ---------------------------
# 6. Print results
# ---------------------------

print("=== Monte Carlo Simulation ===")
print("Simulated years:", num_simulations)

print(
    f"\nExpected Annual Loss: ${expected_loss:,.2f}"
)

print(
    f"95% VaR: ${var_95:,.2f}"
)

print(
    f"99% VaR: ${var_99:,.2f}"
)

print(
    f"99% TVaR: ${tvar_99:,.2f}"
)


# ---------------------------
# 7. Save simulation results
# ---------------------------

results = pd.DataFrame({
    "simulation": range(1, num_simulations + 1),
    "annual_loss": annual_losses
})

results.to_csv(
    "data/processed/simulation_results.csv",
    index=False
)