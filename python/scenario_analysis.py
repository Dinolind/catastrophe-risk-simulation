import pandas as pd
import numpy as np


np.random.seed(42)


# ---------------------------
# Load portfolio
# ---------------------------

policies = pd.read_csv(
    "data/processed/policies.csv"
)


policies_by_state = {
    state: group.reset_index(drop=True)
    for state, group in policies.groupby("state")
}


# Historical state probabilities
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


# Historical damaging hurricane episode frequency
annual_frequency = 4.89

# Total annual premium from portfolio
annual_premium = policies["annual_premium"].sum()

# Number of simulated years
num_simulations = 10000


# ---------------------------
# Simulation function
# ---------------------------

def run_simulation(
    scenario_name,
    affected_min,
    affected_max
):
    np.random.seed(42)

    annual_losses = []

    for simulation in range(num_simulations):

        yearly_loss = 0

        number_of_hurricanes = np.random.poisson(
            annual_frequency
        )

        for event in range(number_of_hurricanes):

            affected_state = np.random.choice(
                states,
                p=state_probabilities
            )

            state_policies = policies_by_state[
                affected_state
            ]

            affected_percent = np.random.uniform(
                affected_min,
                affected_max
            )

            affected_count = max(
                1,
                int(
                    len(state_policies)
                    * affected_percent
                )
            )

            affected_policies = state_policies.sample(
                n=affected_count,
                replace=False
            )

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
                affected_policies[
                    "property_value"
                ].to_numpy()
                * damage_ratios
            )

            claims = np.maximum(
                gross_damage
                - affected_policies[
                    "deductible"
                ].to_numpy(),
                0
            )

            claims = np.minimum(
                claims,
                affected_policies[
                    "coverage_amount"
                ].to_numpy()
            )

            yearly_loss += claims.sum()

        annual_losses.append(yearly_loss)


    annual_losses = np.array(
        annual_losses
    )


    expected_loss = annual_losses.mean()

    std_loss = annual_losses.std()

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

    expected_loss_ratio = (
        expected_loss
        / annual_premium
    )

    prob_zero_loss = np.mean(
        annual_losses == 0
    )

    prob_loss_above_premium = np.mean(
        annual_losses
        > annual_premium
    )


    return {
        "scenario": scenario_name,
        "affected_min": affected_min,
        "affected_max": affected_max,
        "expected_loss": expected_loss,
        "std_loss": std_loss,
        "var_95": var_95,
        "var_99": var_99,
        "tvar_99": tvar_99,
        "expected_loss_ratio": expected_loss_ratio,
        "prob_zero_loss": prob_zero_loss,
        "prob_loss_above_premium": prob_loss_above_premium
    }, annual_losses


# ---------------------------
# Run scenarios
# ---------------------------

scenarios = [
    ("Low", 0.01, 0.03),
    ("Base", 0.01, 0.10),
    ("High", 0.05, 0.15)
]


results = []

for name, minimum, maximum in scenarios:

    result, losses = run_simulation(
    name,
    minimum,
    maximum
    )

    results.append(result)

    if name == "Base":

        base_losses = losses

# ---------------------------
# Save results
# ---------------------------

results_df = pd.DataFrame(
    results
)


results_df.to_csv(
    "data/processed/scenario_results.csv",
    index=False
)

base_results = pd.DataFrame({
    "simulation": range(
        1,
        num_simulations + 1
    ),
    "annual_loss": base_losses
})

base_results.to_csv(
    "data/processed/base_simulation_results.csv",
    index=False
)


# ---------------------------
# Print results
# ---------------------------

pd.set_option(
    "display.float_format",
    lambda x: f"{x:,.2f}"
)

print("\n=== Scenario Analysis ===")

print(
    results_df[
        [
            "scenario",
            "expected_loss",
            "var_95",
            "var_99",
            "tvar_99",
            "expected_loss_ratio",
            "prob_loss_above_premium"
        ]
    ]
)