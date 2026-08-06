import pandas as pd
import glob


# Load all NOAA files
files = glob.glob("data/raw/*.csv.gz")

storms = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in files],
    ignore_index=True
)


# Filter tropical events
tropical = storms[
    storms["EVENT_TYPE"].str.contains(
        "Tropical|Hurricane|Storm Surge",
        case=False,
        na=False
    )
]


# Convert NOAA damage format into dollars
def convert_damage(value):
    if pd.isna(value):
        return 0

    value = str(value).strip()

    multiplier = 1

    if value.endswith("K"):
        multiplier = 1_000
        value = value[:-1]

    elif value.endswith("M"):
        multiplier = 1_000_000
        value = value[:-1]

    elif value.endswith("B"):
        multiplier = 1_000_000_000
        value = value[:-1]

    try:
        return float(value) * multiplier
    except:
        return 0


# Create cleaned dataset
catastrophe = tropical[
    [
        "EVENT_ID",
        "EVENT_TYPE",
        "BEGIN_DATE_TIME",
        "STATE",
        "CZ_NAME",
        "DAMAGE_PROPERTY"
    ]
].copy()


# Clean damage values
catastrophe["property_damage"] = (
    catastrophe["DAMAGE_PROPERTY"]
    .apply(convert_damage)
)


# Create year variable
catastrophe["year"] = pd.to_datetime(
    catastrophe["BEGIN_DATE_TIME"]
).dt.year


# Remove original damage column
catastrophe = catastrophe.drop(
    columns=["DAMAGE_PROPERTY"]
)


# Save processed dataset
catastrophe.to_csv(
    "data/processed/catastrophe_events.csv",
    index=False
)


print("Cleaned catastrophe dataset created!")
print("Rows:", len(catastrophe))
print(catastrophe.head())