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

# Historical damaging hurricane episode counts by state
states = [
    "FLORIDA",
    "LOUISIANA",
    "TEXAS",
    "GEORGIA",
    "NORTH CAROLINA",
    "ALABAMA",
    "SOUTH CAROLINA"
]

state_probabilities = [
    13 / 37,
    7 / 37,
    6 / 37,
    4 / 37,
    3 / 37,
    2 / 37,
    2 / 37
]

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
        affected_state = np.random.choice(
            states,
            p=state_probabilities
        )

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

        # Simulate damage ratios. Most affected properties experience modest damage, while severe damage remains possible but less common.
        damage_ratios = np.random.beta(
            a=1.5,
            b=8,
            size=affected_count
        )

        damage_ratios = np.clip(
        damage_ratios,
        0.01,
        0.75
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
std_loss = annual_losses.std()
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

prob_zero_loss = np.mean(
    annual_losses == 0
)

prob_loss_above_premium = np.mean(
    annual_losses > annual_premium
)


print("=== Insurer Catastrophe Simulation ===")

print(f"Expected Annual Loss: ${expected_loss:,.2f}")
print(f"Annual Loss Standard Deviation: ${std_loss:,.2f}")
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

print(
    f"Probability of Zero Cat Loss: "
    f"{prob_zero_loss:.1%}"
)

print(
    f"Probability Cat Loss Exceeds Premium: "
    f"{prob_loss_above_premium:.1%}"
)

results = pd.DataFrame({
    "simulation": range(1, num_simulations + 1),
    "annual_loss": annual_losses
})

results.to_csv(
    "data/processed/insurer_simulation_results.csv",
    index=False
)

test_damage = np.random.beta(
    1.5,
    8,
    100000
)

print("\n=== Damage Ratio Check ===")
print("Mean:", test_damage.mean())
print("Median:", np.median(test_damage))
print("90th percentile:", np.percentile(test_damage, 90))
print("99th percentile:", np.percentile(test_damage, 99))