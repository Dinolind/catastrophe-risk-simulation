import pandas as pd
import numpy as np


# Make results reproducible
np.random.seed(42)


# Number of policies
n = 10000


# States in the simulated portfolio
states = [
    "FLORIDA",
    "LOUISIANA",
    "TEXAS",
    "GEORGIA",
    "NORTH CAROLINA",
    "SOUTH CAROLINA",
    "ALABAMA"
]

# Generate policy data
portfolio = pd.DataFrame({
    "policy_id": range(1, n + 1),

    "state": np.random.choice(
        states,
        size=n
    ),

    "property_value": np.random.normal(
        350000,
        100000,
        n
    ).astype(int)
})


# Make sure property values aren't unrealistically low
portfolio["property_value"] = portfolio["property_value"].clip(
    lower=100000
)


# Coverage is 80% of property value
portfolio["coverage_amount"] = (
    portfolio["property_value"] * 0.80
).astype(int)


# $5,000 deductible
portfolio["deductible"] = 5000


# Simplified premium assumption
portfolio["annual_premium"] = (
    portfolio["coverage_amount"] * 0.008
).round(2)


# Save portfolio
portfolio.to_csv(
    "data/processed/policies.csv",
    index=False
)


# Display results
print("=== Portfolio Created ===")
print("Number of policies:", len(portfolio))

print("\n=== First 5 Policies ===")
print(portfolio.head())

print("\n=== Average Values ===")
print(
    portfolio[
        [
            "property_value",
            "coverage_amount",
            "deductible",
            "annual_premium"
        ]
    ].mean()
)

print("\n=== Policies by State ===")
print(
    portfolio["state"]
    .value_counts()
)