import pandas as pd
import numpy as np

# ============================================================
# FILES
# ============================================================

MAIN_FILE = "nassau_candy_distributor.xlsx"
DISTANCE_FILE = "customer_factory_distances.xlsx"
OUTPUT_FILE = "final_factory_analysis.xlsx"

COST_PER_KM = 1.00


# ============================================================
# READ DATA
# ============================================================

transactions = pd.read_excel(
    MAIN_FILE,
    sheet_name="Nassau Candy Distributor"
)

distances = pd.read_excel(
    DISTANCE_FILE
)

print("Transaction rows:", len(transactions))
print("Distance rows:", len(distances))


# ============================================================
# CREATE LOCATION KEY
# ============================================================

def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def create_location_key(df, city, state, zip_code, country):

    return (
        df[city].apply(clean_text)
        + "|"
        + df[state].apply(clean_text)
        + "|"
        + df[zip_code].astype(str).str.strip()
        + "|"
        + df[country].apply(clean_text)
    )


transactions["Location Key"] = create_location_key(
    transactions,
    "City of customer",
    "State/province of customer",
    "Postal code / zip code of customer",
    "Country or region of customer"
)

distances["Location Key"] = create_location_key(
    distances,
    "City of customer",
    "State/province of customer",
    "Postal code / zip code of customer",
    "Country or region of customer"
)



# ============================================================
# FACTORY DISTANCE COLUMNS
# ============================================================

factory_distances = {
    "Lot's O' Nuts": "Distance to Lot's O' Nuts (km)",
    "Wicked Choccy's": "Distance to Wicked Choccy's (km)",
    "Sugar Shack": "Distance to Sugar Shack (km)",
    "Secret Factory": "Distance to Secret Factory (km)",
    "The Other Factory": "Distance to The Other Factory (km)"
}


# ============================================================
# CHECK DISTANCE COLUMNS
# ============================================================

for factory, column in factory_distances.items():

    if column not in distances.columns:
        raise ValueError(
            f"Missing distance column: {column}"
        )


# ============================================================
# KEEP ONE DISTANCE RECORD PER LOCATION
# ============================================================

distance_columns = [
    "Location Key",
    "Latitude",
    "Longitude"
] + list(factory_distances.values())

distance_lookup = distances[distance_columns].drop_duplicates(
    subset=["Location Key"]
)


# ============================================================
# MERGE TRANSACTIONS WITH DISTANCES
# ============================================================

result = transactions.merge(
    distance_lookup,
    on="Location Key",
    how="left"
)

print(
    "Transactions matched with distance data:",
    result["Latitude"].notna().sum()
)

print(
    "Transactions without distance data:",
    result["Latitude"].isna().sum()
)


# ============================================================
# TRANSPORTATION COST FOR EACH FACTORY
# ============================================================

for factory, distance_column in factory_distances.items():

    cost_column = f"Transportation Cost - {factory} ($)"

    result[cost_column] = (
        result[distance_column] * COST_PER_KM
    )


# ============================================================
# FIND RECOMMENDED FACTORY
# ============================================================

cost_columns = [
    f"Transportation Cost - {factory} ($)"
    for factory in factory_distances
]

result["Minimum Transportation Cost ($)"] = (
    result[cost_columns].min(axis=1)
)


# ============================================================
# FIND RECOMMENDED FACTORY
# ============================================================

def find_recommended_factory(row):

    costs = row[cost_columns]

    # If all factory costs are missing
    if costs.isna().all():
        return "Location Data Missing"

    # Find lowest available cost
    lowest_column = costs.idxmin()

    # Convert cost column name to factory name
    factory_name = (
        lowest_column
        .replace("Transportation Cost - ", "")
        .replace(" ($)", "")
    )

    return factory_name


result["Recommended Factory"] = result.apply(
    find_recommended_factory,
    axis=1
)


# ============================================================
# CURRENT FACTORY COST
# ============================================================

def current_factory_cost(row):

    current_factory = clean_text(
        row["Factory Names"]
    )

    for factory in factory_distances:

        if clean_text(factory) in current_factory:

            cost_column = (
                f"Transportation Cost - {factory} ($)"
            )

            return row[cost_column]

    return np.nan


result["Current Factory Transportation Cost ($)"] = (
    result.apply(
        current_factory_cost,
        axis=1
    )
)


# ============================================================
# CURRENT DISTANCE
# ============================================================

result["Current Factory Distance (km)"] = (
    result["Current Factory Transportation Cost ($)"]
    / COST_PER_KM
)


# ============================================================
# POTENTIAL SAVINGS
# ============================================================

result["Potential Transportation Savings ($)"] = (
    result["Current Factory Transportation Cost ($)"]
    - result["Minimum Transportation Cost ($)"]
)


# ============================================================
# FACTORY CHANGE
# ============================================================

# ============================================================
# FACTORY CHANGE
# ============================================================

# ============================================================
# FINAL FACTORY DECISION
# ============================================================

def factory_decision(row):

    recommended = clean_text(row["Recommended Factory"])
    current = clean_text(row["Factory Names"])

    if recommended == "location data missing":
        return "Location Data Missing"

    # Normalize factory names
    if "lot's o' nuts" in current:
        current = "lot's o' nuts"
    elif "wicked choccy's" in current:
        current = "wicked choccy's"
    elif "sugar shack" in current:
        current = "sugar shack"
    elif "secret factory" in current:
        current = "secret factory"
    elif "the other factory" in current:
        current = "the other factory"

    if current == recommended:
        return "No Change Required"

    return "Consider Reassignment"


result["Factory Decision"] = result.apply(
    factory_decision,
    axis=1
)


# ============================================================
# REMOVE TECHNICAL KEY
# ============================================================

result.drop(
    columns=["Location Key"],
    inplace=True
)


# ============================================================
# SAVE
# ============================================================

result.to_excel(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("==========================================")
print("FINAL FACTORY ANALYSIS COMPLETED")
print("==========================================")

print("Output:", OUTPUT_FILE)

print(
    "Total transaction rows:",
    len(result)
)

print(
    "Rows with coordinates:",
    result["Latitude"].notna().sum()
)

print(
    "Rows without coordinates:",
    result["Latitude"].isna().sum()
)

result["Factory Change Required"] = np.where(
    result["Factory Names"] != result["Recommended Factory"],
    "Yes",
    "No"
)

print(
    "Factory changes recommended:",
    (result["Factory Change Required"] == "Yes").sum()
)

print(
    "Total potential savings ($):",
    round(
        result[
            "Potential Transportation Savings ($)"
        ].clip(lower=0).sum(),
        2
    )
)

print()
print("Recommended factory distribution:")

print(
    result["Recommended Factory"]
    .value_counts()
)

print()
print("==========================================")