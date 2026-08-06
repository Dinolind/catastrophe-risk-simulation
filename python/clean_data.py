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


# Select useful columns
catastrophe = tropical[
    [
        "EVENT_ID",
        "EVENT_TYPE",
        "BEGIN_DATE_TIME",
        "STATE",
        "CZ_NAME",
        "MAGNITUDE",
        "DAMAGE_PROPERTY",
        "DAMAGE_CROPS"
    ]
]


print(catastrophe.head())

print("\nRows:")
print(len(catastrophe))


# Save processed file
catastrophe.to_csv(
    "data/processed/catastrophe_events.csv",
    index=False
)