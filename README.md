# Catastrophe Risk Simulation

## Overview

This project models hurricane catastrophe risk for a synthetic homeowners insurance portfolio using Python, PostgreSQL, and Excel.

Historical NOAA Storm Events data is used to estimate hurricane frequency and geographic risk. A 10,000-policy synthetic portfolio is then subjected to a 10,000-year Monte Carlo simulation to estimate expected catastrophe losses and tail-risk measures including VaR and TVaR.

## Tools

* **Python:** data cleaning, portfolio generation, Monte Carlo simulation, sensitivity analysis
* **PostgreSQL:** catastrophe event storage, SQL analysis, historical calibration
* **Excel:** exposure reporting, scenario comparison, loss-distribution analysis, executive summary

## Portfolio

The synthetic homeowners portfolio contains:

* **10,000 policies**
* **$2.80 billion** in insured exposure
* **$22.36 million** in annual premium
* Policies are modeled across Florida, Louisiana, Texas, Georgia, North Carolina, South Carolina, and Alabama

## Model

Historical NOAA data from **2016–2024** was cleaned and analyzed in Python and PostgreSQL.

An important data-quality adjustment was made during development. NOAA `EVENT_ID` records initially overstated hurricane frequency because a single storm can generate multiple geographic event records. The model was recalibrated using distinct `EPISODE_ID` values, producing an average of approximately **4.89 damaging hurricane episodes per year**.

For each simulated year:

1. Hurricane event frequency is generated using a Poisson distribution.
2. The affected state is selected using probabilities based on historical hurricane experience.
3. A percentage of policies in that state is affected.
4. Damage ratios are simulated using a right-skewed Beta distribution.
5. Deductibles and policy coverage limits are applied.
6. Claims are aggregated into annual insurer losses.

The process is repeated for **10,000 simulated years**.

## Scenario Analysis

Three catastrophe-footprint assumptions were tested:

| Scenario | Policies Affected | Expected Loss |     99% VaR |    99% TVaR | Cat Loss Ratio |
| -------- | ----------------: | ------------: | ----------: | ----------: | -------------: |
| Low      |             1%–3% |        $6.82M |     $15.83M |     $17.38M |            30% |
| **Base** |        **1%–10%** |   **$19.28M** | **$45.65M** | **$50.77M** |        **86%** |
| High     |            5%–15% |       $34.91M |     $77.86M |     $85.70M |           156% |

Under the Base scenario, hurricane losses exceed total annual portfolio premium in approximately **35% of simulated years**.

## Key Findings

* Catastrophe losses are highly variable, with Base expected losses of about **$19.3M** compared with **$50.8M** 99% TVaR.
* Florida represents the largest historical hurricane concentration among the modeled states.
* Results are highly sensitive to catastrophe footprint assumptions, with expected losses ranging from **$6.8M to $34.9M**.
* VaR and TVaR provide a clearer view of extreme catastrophe exposure than expected loss alone.

## Project Structure

```text
catastrophe-risk-simulation/
├── data/
│   ├── raw/
│   └── processed/
├── python/
│   ├── clean_data.py
│   ├── explore_data.py
│   ├── generate_portfolio.py
│   ├── prepare_hurricane_data.py
│   └── scenario_analysis.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_create_policy_table.sql
├── reports/
│   └── catastrophe_risk_analysis.xlsx
└── README.md
```

## Limitations

This is a simplified educational catastrophe model using public historical data and synthetic insurance exposure. Policy-level geographic coordinates were unavailable, so catastrophe footprint is modeled at the state level and evaluated through sensitivity scenarios. The model does not include reinsurance, inflation, non-catastrophe claims, or production-grade vulnerability curves.

## Skills Demonstrated

**Python • SQL • PostgreSQL • Excel • Monte Carlo Simulation • Frequency-Severity Modeling • VaR • TVaR • Sensitivity Analysis • Insurance Exposure Analysis**
