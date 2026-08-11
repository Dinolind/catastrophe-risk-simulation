import pandas as pd
import numpy as np

np.random.seed(42)

# Load portfolio
policies = pd.read_csv(
    "data/processed/policies.csv"
)

# Split portfolio by state once
policies_by_state = {
    state: group.reset_index(drop=True)
    for state, group in policies.groupby("state")
}

states = list(policies_by_state.keys())

num_simulations = 1000

# Average annual number of distinct damaging
# hurricane episodes from NOAA, 2016-2024
annual_frequency = 4.89

annual_losses = []

for simulation in range(num_simulations):

    yearly_loss = 0

    # Simulate number of hurricanes
    number_of_hurricanes = np.random.poisson(
        annual_frequency
    )

    for event in range(number_of_hurricanes):

        # Randomly choose an affected state
        affected_state = np.random.choice(states)

        state_policies = policies_by_state[affected_state]

        # Percentage of policies affected by this hurricane
        affected_percent = np.random.uniform(
            0.01,
            0.10
        )

        affected_count = max(
            1,
            int(len(state_policies) * affected_percent)
        )

        affected_policies = state_policies.sample(
            n=affected_count,
            replace=False
        )

        # Damage ratio between 5% and 60%
        damage_ratios = np.random.uniform(
            0.05,
            0.60,
            affected_count
        )

        gross_damage = (
            affected_policies["property_value"].to_numpy()
            * damage_ratios
        )

        # Apply deductible
        claims = np.maximum(
            gross_damage
            - affected_policies["deductible"].to_numpy(),
            0
        )

        # Apply coverage limit
        claims = np.minimum(
            claims,
            affected_policies["coverage_amount"].to_numpy()
        )

        yearly_loss += claims.sum()

    annual_losses.append(yearly_loss)


annual_losses = np.array(annual_losses)

expected_loss = annual_losses.mean()
var_95 = np.percentile(annual_losses, 95)
var_99 = np.percentile(annual_losses, 99)

tvar_99 = annual_losses[
    annual_losses >= var_99
].mean()

annual_premium = 22_362_474.53

expected_loss_ratio = (
    expected_loss / annual_premium
)

var_95_loss_ratio = (
    var_95 / annual_premium
)

var_99_loss_ratio = (
    var_99 / annual_premium
)


print("=== Insurer Catastrophe Simulation ===")

print(f"Expected Annual Loss: ${expected_loss:,.2f}")
print(f"95% VaR: ${var_95:,.2f}")
print(f"99% VaR: ${var_99:,.2f}")
print(f"99% TVaR: ${tvar_99:,.2f}")

print(
    f"Expected Cat Loss Ratio: "
    f"{expected_loss_ratio:.1%}"
)

print(
    f"95% VaR Loss Ratio: "
    f"{var_95_loss_ratio:.1%}"
)

print(
    f"99% VaR Loss Ratio: "
    f"{var_99_loss_ratio:.1%}"
)

results = pd.DataFrame({
    "simulation": range(1, num_simulations + 1),
    "annual_loss": annual_losses
})

results.to_csv(
    "data/processed/insurer_simulation_results.csv",
    index=False
)