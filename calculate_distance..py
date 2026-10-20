import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# =========================
# FILE SETTINGS
# =========================

INPUT_FILE = "customer_data_with_coordinates.xlsx"
OUTPUT_FILE = "customer_factory_distances.xlsx"

# =========================
# FACTORY COORDINATES
# =========================

factories = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.119140, -96.181150),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.117500, -89.971107)
}

# =========================
# READ CUSTOMER DATA
# =========================

df = pd.read_excel(INPUT_FILE)

# =========================
# HAVERSINE FUNCTION
# =========================

def haversine(lat1, lon1, lat2, lon2):

    R = 6371  # Earth radius in km

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# =========================
# CALCULATE DISTANCES
# =========================

distance_columns = {}

for factory, (factory_lat, factory_lon) in factories.items():

    column_name = f"Distance to {factory} (km)"

    df[column_name] = df.apply(
        lambda row: haversine(
            row["Latitude"],
            row["Longitude"],
            factory_lat,
            factory_lon
        ),
        axis=1
    )

    distance_columns[factory] = column_name

# =========================
# FIND CLOSEST FACTORY
# =========================

distance_df = df[list(distance_columns.values())]

df["Closest Factory"] = distance_df.idxmin(axis=1)

# Remove "Distance to " and "(km)" from factory name
df["Closest Factory"] = (
    df["Closest Factory"]
    .str.replace("Distance to ", "", regex=False)
    .str.replace(" (km)", "", regex=False)
)

# Minimum distance
df["Minimum Distance (km)"] = distance_df.min(axis=1)

# =========================
# SAVE RESULT
# =========================
# =========================
# TRANSPORTATION COST
# =========================

FREIGHT_RATE_PER_KM = 1.00

for factory, distance_column in distance_columns.items():

    cost_column = f"Transportation Cost - {factory} ($)"

    df[cost_column] = (
        df[distance_column] * FREIGHT_RATE_PER_KM
    )

# Cost using the closest factory
df["Minimum Transportation Cost ($)"] = (
    df["Minimum Distance (km)"] * FREIGHT_RATE_PER_KM
)

# =========================
# TRANSPORTATION COST
# =========================

FREIGHT_RATE_PER_KM = 1.00

for factory, distance_column in distance_columns.items():

    cost_column = f"Transportation Cost - {factory} ($)"

    df[cost_column] = (
        df[distance_column] * FREIGHT_RATE_PER_KM
    )

df["Minimum Transportation Cost ($)"] = (
    df["Minimum Distance (km)"] * FREIGHT_RATE_PER_KM
)

df.to_excel(OUTPUT_FILE, index=False)

print("===================================")
print("DONE")
print("===================================")
print(f"Output file: {OUTPUT_FILE}")
print("Closest factory calculation completed.")
print("Minimum distance calculated.")
print("===================================")