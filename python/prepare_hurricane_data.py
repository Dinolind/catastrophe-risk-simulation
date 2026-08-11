import pandas as pd


# Load cleaned catastrophe data
catastrophe = pd.read_csv(
    "data/processed/catastrophe_events.csv"
)


# Keep hurricanes from 2016-2024
hurricanes = catastrophe[
    (catastrophe["EVENT_TYPE"] == "Hurricane (Typhoon)") &
    (catastrophe["year"] < 2025)
].copy()


# Aggregate multiple NOAA records belonging to the same hurricane
hurricanes = (
    hurricanes
    .groupby("EVENT_ID", as_index=False)
    .agg(
        event_type=("EVENT_TYPE", "first"),
        year=("year", "first"),
        property_damage=("property_damage", "max")
    )
)


# Save hurricane-level dataset
hurricanes.to_csv(
    "data/processed/hurricanes.csv",
    index=False
)


print("=== Hurricane Dataset ===")
print("Unique hurricanes:", len(hurricanes))
print("Hurricanes with reported damage:",
      (hurricanes["property_damage"] > 0).sum())

print("\n=== First 10 Hurricanes ===")
print(hurricanes.head(10))

print("\n=== Damage Statistics ===")
print(
    hurricanes["property_damage"].describe()
)