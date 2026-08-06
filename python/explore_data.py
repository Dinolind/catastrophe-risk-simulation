import pandas as pd
import glob

files = glob.glob("data/raw/*.csv.gz")

storms = pd.concat(
    [pd.read_csv(file, low_memory=False) for file in files],
    ignore_index=True
)

print("Total rows:", len(storms))

print("\n=== First Five Rows ===")
print(storms.head())

print("\n=== Dataset Information ===")
storms.info()

print("\n=== Column Names ===")
for column in storms.columns:
    print(column)

print("\n=== Dataset Size ===")
print("Rows:", len(storms))
print("Columns:", len(storms.columns))

important_columns = [
    "EVENT_ID",
    "EVENT_TYPE",
    "BEGIN_DATE_TIME",
    "STATE",
    "MAGNITUDE",
    "DAMAGE_PROPERTY",
    "DAMAGE_CROPS"
]

print("\n=== Important Columns Preview ===")
print(storms[important_columns].head())

print("\n=== Event Types ===")
print(storms["EVENT_TYPE"].value_counts().head(20))

print("\n=== Tropical Events ===")

tropical_events = storms[
    storms["EVENT_TYPE"].str.contains(
        "Tropical|Hurricane|Storm Surge|Cyclone",
        case=False,
        na=False
    )
]

print(tropical_events["EVENT_TYPE"].value_counts())