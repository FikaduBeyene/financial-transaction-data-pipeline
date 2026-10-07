from pathlib import Path

import pandas as pd


# ----------------------------
# Valid U.S. state abbreviations
# ----------------------------

valid_states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "IA", "ID", "IL", "IN", "KS", "KY",
    "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS",
    "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
    "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
    "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"
]


# ----------------------------
# Load raw dataset
# ----------------------------

raw_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "transactions_raw.csv"
)

df = pd.read_csv(raw_file)

print("Raw dataset loaded successfully.")
print("Dataset shape:", df.shape)


# ----------------------------
# Create cleaning baseline
# ----------------------------

original_row_count = len(df)
original_duplicate_count = df.duplicated().sum()
original_missing_values = df.isnull().sum().sum()

print("\nCleaning baseline:")
print("Original rows:", original_row_count)
print("Original duplicate rows:", original_duplicate_count)
print("Original missing values:", original_missing_values)


# ----------------------------
# Remove exact duplicate rows
# ----------------------------

df = df.drop_duplicates().copy()

print("\nAfter removing exact duplicates:")
print("Dataset shape:", df.shape)
print("Duplicate rows remaining:", df.duplicated().sum())


# ----------------------------
# Standardize transaction types
# ----------------------------

df["transaction_type"] = (
    df["transaction_type"]
    .str.strip()
    .str.title()
)

print("\nTransaction types after standardization:")
print(df["transaction_type"].value_counts())

# ----------------------------
# Standardize categories
# ----------------------------

df["category"] = (
    df["category"]
    .str.strip()
    .str.title()
)

print("\nCategories after standardization:")
print(df["category"].value_counts())

# ----------------------------
# Standardize payment methods
# ----------------------------

df["payment_method"] = (
    df["payment_method"]
    .str.strip()
    .str.title()
)

df["payment_method"] = df["payment_method"].replace({
    "Ach": "ACH"
})

print("\nPayment methods after standardization:")
print(df["payment_method"].value_counts())


# ----------------------------
# Convert transaction dates
# ----------------------------

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

print("\nTransaction date data type:")
print(df["transaction_date"].dtype)

print("\nInvalid or missing transaction dates:")
print(df["transaction_date"].isna().sum())


# ----------------------------
# Identify out-of-range dates
# ----------------------------

business_start_date = pd.Timestamp("2025-01-01")
business_end_date = pd.Timestamp("2026-09-25")

out_of_range_dates = (
    df["transaction_date"].notna()
    & (
        (df["transaction_date"] < business_start_date)
        | (df["transaction_date"] > business_end_date)
    )
)

print("\nOut-of-range transaction dates:")
print(out_of_range_dates.sum())


# ----------------------------
# Remove invalid transaction dates
# ----------------------------

valid_date_mask = (
    df["transaction_date"].notna()
    & (df["transaction_date"] >= business_start_date)
    & (df["transaction_date"] <= business_end_date)
)

invalid_date_count = (~valid_date_mask).sum()

df = df.loc[valid_date_mask].copy()

print("\nAfter removing invalid transaction dates:")
print("Rows removed:", invalid_date_count)
print("Dataset shape:", df.shape)
print("Invalid dates remaining:", (
    df["transaction_date"].isna()
    | (df["transaction_date"] < business_start_date)
    | (df["transaction_date"] > business_end_date)
).sum())


# ----------------------------
# Standardize state values
# ----------------------------

df["state"] = df["state"].replace({
    "Missouri": "MO",
    "KANSAS": "KS",
    "California": "CA"
})

invalid_states = ~df["state"].isin(valid_states) & df["state"].notna()

print("\nInvalid state values before remediation:")
print(df.loc[invalid_states, "state"].value_counts())


# ----------------------------
# Handle unresolvable states
# ----------------------------

df.loc[
    df["state"].isin(["XX", "123"]),
    "state"
] = pd.NA

print("\nState values after remediation:")
print("Invalid states remaining:",
      (~df["state"].isin(valid_states) & df["state"].notna()).sum())

print("Missing state values:", df["state"].isna().sum())


# ----------------------------
# Standardize transaction statuses
# ----------------------------

df["status"] = df["status"].replace({
    "Complete": "Completed"
})

print("\nTransaction statuses after standardization:")
print(df["status"].value_counts(dropna=False))


# ----------------------------
# Handle unresolvable statuses
# ----------------------------

df.loc[
    df["status"].isin(["CANCELLED", "Unknown", "N/A"]),
    "status"
] = pd.NA

print("\nStatus values after remediation:")
print(
    "Invalid statuses remaining:",
    (~df["status"].isin([
        "Completed",
        "Pending",
        "Failed",
        "Reversed"
    ]) & df["status"].notna()).sum()
)

print("Missing status values:", df["status"].isna().sum())


# ----------------------------
# Validate transaction amounts
# ----------------------------

invalid_amounts = (
    (df["amount"] <= 0)
    | (df["amount"] > 5000)
)

print("\nInvalid transaction amounts before remediation:")
print("Invalid amounts:", invalid_amounts.sum())

print("\nInvalid amount examples:")
print(df.loc[invalid_amounts, "amount"].value_counts())


# ----------------------------
# Remove invalid transaction amounts
# ----------------------------

df = df.loc[~invalid_amounts].copy()

print("\nAfter removing invalid transaction amounts:")
print("Rows removed:", invalid_amounts.sum())
print("Dataset shape:", df.shape)

print(
    "Invalid amounts remaining:",
    (
        (df["amount"] <= 0)
        | (df["amount"] > 5000)
    ).sum()
)


# ----------------------------
# Handle remaining missing values
# ----------------------------

missing_value_columns = [
    "category",
    "payment_method",
    "state",
    "status",
    "merchant"
]

print("\nMissing values before remediation:")

for column in missing_value_columns:
    print(f"{column}: {df[column].isna().sum()}")

# Replace missing values with an explicit Unknown category
for column in missing_value_columns:
    df[column] = df[column].fillna("Unknown")

print("\nMissing values after remediation:")

for column in missing_value_columns:
    print(f"{column}: {df[column].isna().sum()}")


# ----------------------------
# Detailed duplicate ID investigation
# ----------------------------

print("\n" + "=" * 50)
print("DETAILED DUPLICATE ID INVESTIGATION")
print("=" * 50)

duplicate_id_mask = df["transaction_id"].duplicated(keep=False)

duplicate_id_groups = (
    df.loc[duplicate_id_mask]
    .sort_values("transaction_id")
)

# Find transaction IDs where the duplicated rows are not identical
duplicate_id_summary = (
    duplicate_id_groups
    .groupby("transaction_id")
    .agg(
        row_count=("transaction_id", "size"),
        unique_customers=("customer_id", "nunique"),
        unique_dates=("transaction_date", "nunique"),
        unique_types=("transaction_type", "nunique"),
        unique_categories=("category", "nunique"),
        unique_amounts=("amount", "nunique"),
        unique_payment_methods=("payment_method", "nunique"),
        unique_states=("state", "nunique"),
        unique_statuses=("status", "nunique"),
        unique_merchants=("merchant", "nunique")
    )
)

# IDs where at least one field differs
conflicting_duplicate_ids = duplicate_id_summary[
    (duplicate_id_summary["unique_customers"] > 1)
    | (duplicate_id_summary["unique_dates"] > 1)
    | (duplicate_id_summary["unique_types"] > 1)
    | (duplicate_id_summary["unique_categories"] > 1)
    | (duplicate_id_summary["unique_amounts"] > 1)
    | (duplicate_id_summary["unique_payment_methods"] > 1)
    | (duplicate_id_summary["unique_states"] > 1)
    | (duplicate_id_summary["unique_statuses"] > 1)
    | (duplicate_id_summary["unique_merchants"] > 1)
]

print("\nTotal duplicate transaction IDs:")
print(len(duplicate_id_summary))

print("\nDuplicate IDs with conflicting transaction details:")
print(len(conflicting_duplicate_ids))

print("\nConflicting duplicate transaction IDs:")
print(conflicting_duplicate_ids)

print("\nDetailed records for conflicting IDs:")

conflicting_ids = conflicting_duplicate_ids.index

print(
    df.loc[
        df["transaction_id"].isin(conflicting_ids)
    ].sort_values("transaction_id").to_string(index=False)
)


# ----------------------------
# Identify true conflicting duplicate records
# ----------------------------

print("\n" + "=" * 50)
print("TRUE DUPLICATE CONFLICT CHECK")
print("=" * 50)

duplicate_records = df[
    df["transaction_id"].duplicated(keep=False)
].copy()

duplicate_records = duplicate_records.sort_values("transaction_id")

comparison_columns = [
    "customer_id",
    "transaction_date",
    "transaction_type",
    "category",
    "amount",
    "payment_method",
    "state",
    "status",
    "merchant"
]

true_conflicts = []

for transaction_id, group in duplicate_records.groupby("transaction_id"):

    for column in comparison_columns:

        known_values = group[column][
            group[column] != "Unknown"
        ].dropna().unique()

        if len(known_values) > 1:
            true_conflicts.append({
                "transaction_id": transaction_id,
                "column": column,
                "values": list(known_values)
            })

true_conflicts_df = pd.DataFrame(true_conflicts)

print("\nTrue conflicting transaction IDs:")

if true_conflicts_df.empty:
    print("None")
else:
    print(true_conflicts_df.to_string(index=False))

print("\nNumber of true conflicting fields:")
print(len(true_conflicts_df))


# ----------------------------
# Resolve duplicate transaction IDs
# ----------------------------

deduplication_columns = [
    "customer_id",
    "transaction_date",
    "transaction_type",
    "category",
    "amount",
    "payment_method",
    "state",
    "status",
    "merchant"
]

# Count how many fields contain known values for each record.
# "Unknown" represents a value that could not be recovered.
df["_known_value_count"] = sum(
    (df[column] != "Unknown").astype(int)
    for column in deduplication_columns
)

duplicate_id_count_before = df["transaction_id"].duplicated().sum()

# Sort so the most complete record for each transaction ID comes first.
df = (
    df.sort_values(
        ["transaction_id", "_known_value_count"],
        ascending=[True, False]
    )
    .drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )
    .drop(columns="_known_value_count")
    .copy()
)

duplicate_id_count_after = df["transaction_id"].duplicated().sum()

print("\nDuplicate transaction ID remediation:")
print("Duplicate transaction IDs before remediation:",
      duplicate_id_count_before)

print("Duplicate transaction IDs after remediation:",
      duplicate_id_count_after)

print("Rows removed during duplicate ID remediation:",
      duplicate_id_count_before - duplicate_id_count_after)

print("Dataset shape after duplicate ID remediation:",
      df.shape)


# ----------------------------
# Final data quality validation
# ----------------------------

print("\n" + "=" * 50)
print("FINAL DATA QUALITY VALIDATION")
print("=" * 50)

# ----------------------------
# Row count
# ----------------------------

print("\nFinal dataset shape:")
print(df.shape)

# ----------------------------
# Duplicate validation
# ----------------------------

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows remaining:")
print(duplicate_count)

# ----------------------------
# Missing-value validation
# ----------------------------

total_missing_values = df.isnull().sum().sum()

print("\nTotal missing values remaining:")
print(total_missing_values)

# ----------------------------
# Transaction ID validation
# ----------------------------

duplicate_transaction_ids = df["transaction_id"].duplicated().sum()

print("\nDuplicate transaction IDs remaining:")
print(duplicate_transaction_ids)

# ----------------------------
# Date validation
# ----------------------------

invalid_dates_remaining = (
    df["transaction_date"].isna()
    | (df["transaction_date"] < business_start_date)
    | (df["transaction_date"] > business_end_date)
).sum()

print("\nInvalid transaction dates remaining:")
print(invalid_dates_remaining)

# ----------------------------
# Amount validation
# ----------------------------

invalid_amounts_remaining = (
    (df["amount"] <= 0)
    | (df["amount"] > 5000)
).sum()

print("\nInvalid transaction amounts remaining:")
print(invalid_amounts_remaining)

# ----------------------------
# State validation
# ----------------------------

valid_states_for_validation = valid_states + ["Unknown"]

invalid_states_remaining = (
    ~df["state"].isin(valid_states_for_validation)
).sum()

print("\nInvalid states remaining:")
print(invalid_states_remaining)

# ----------------------------
# Status validation
# ----------------------------

valid_statuses = [
    "Completed",
    "Pending",
    "Failed",
    "Reversed",
    "Unknown"
]

invalid_statuses_remaining = (
    ~df["status"].isin(valid_statuses)
).sum()

print("\nInvalid statuses remaining:")
print(invalid_statuses_remaining)

# ----------------------------
# Transaction type validation
# ----------------------------

valid_transaction_types = [
    "Debit",
    "Credit"
]

invalid_transaction_types_remaining = (
    ~df["transaction_type"].isin(valid_transaction_types)
).sum()

print("\nInvalid transaction types remaining:")
print(invalid_transaction_types_remaining)

# ----------------------------
# Category validation
# ----------------------------

valid_categories = [
    "Groceries",
    "Utilities",
    "Dining",
    "Transportation",
    "Healthcare",
    "Entertainment",
    "Shopping",
    "Salary",
    "Transfer",
    "Other",
    "Unknown"
]

invalid_categories_remaining = (
    ~df["category"].isin(valid_categories)
).sum()

print("\nInvalid categories remaining:")
print(invalid_categories_remaining)

# ----------------------------
# Payment method validation
# ----------------------------

valid_payment_methods = [
    "Credit Card",
    "Debit Card",
    "ACH",
    "Wire Transfer",
    "Cash",
    "Check",
    "Unknown"
]

invalid_payment_methods_remaining = (
    ~df["payment_method"].isin(valid_payment_methods)
).sum()

print("\nInvalid payment methods remaining:")
print(invalid_payment_methods_remaining)

# ----------------------------
# Final validation result
# ----------------------------

validation_checks = {
    "Duplicate rows": duplicate_count,
    "Missing values": total_missing_values,
    "Duplicate transaction IDs": duplicate_transaction_ids,
    "Invalid dates": invalid_dates_remaining,
    "Invalid amounts": invalid_amounts_remaining,
    "Invalid states": invalid_states_remaining,
    "Invalid statuses": invalid_statuses_remaining,
    "Invalid transaction types": invalid_transaction_types_remaining,
    "Invalid categories": invalid_categories_remaining,
    "Invalid payment methods": invalid_payment_methods_remaining
}

validation_passed = all(
    value == 0
    for value in validation_checks.values()
)

print("\n" + "=" * 50)
print("VALIDATION RESULT")
print("=" * 50)

if validation_passed:
    print("PASS - All data quality checks passed.")
else:
    print("FAIL - One or more data quality checks failed.")

print("=" * 50)


# ----------------------------
# Save cleaned dataset
# ----------------------------

processed_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "transactions_clean.csv"
)

processed_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    processed_file,
    index=False
)

print("\nCleaned dataset saved successfully:")
print(processed_file)


# ----------------------------
# Verify saved dataset
# ----------------------------

saved_df = pd.read_csv(processed_file)

print("\nSaved dataset verification:")
print("Rows:", len(saved_df))
print("Columns:", len(saved_df.columns))
print("Shape:", saved_df.shape)

print("\nSaved dataset columns:")
print(saved_df.columns.tolist())


# ----------------------------
# Cleaning summary
# ----------------------------

rows_removed_total = original_row_count - len(df)

retention_rate = (
    len(df) / original_row_count
) * 100

removal_rate = (
    rows_removed_total / original_row_count
) * 100

print("\n" + "=" * 50)
print("CLEANING SUMMARY")
print("=" * 50)

print(f"\nOriginal rows: {original_row_count:,}")
print(f"Final rows: {len(df):,}")
print(f"Total rows removed: {rows_removed_total:,}")

print(f"\nRetention rate: {retention_rate:.2f}%")
print(f"Removal rate: {removal_rate:.2f}%")

print("\nKey remediation results:")
print(f"Exact duplicate rows removed: {original_duplicate_count:,}")
print(f"Invalid date rows removed: {invalid_date_count:,}")
print(f"Invalid amount rows removed: {invalid_amounts.sum():,}")
print(f"Duplicate transaction IDs resolved: {duplicate_id_count_before:,}")

print("\nFinal data quality:")
print(f"Missing values remaining: {df.isnull().sum().sum():,}")
print(f"Duplicate rows remaining: {df.duplicated().sum():,}")
print(f"Duplicate transaction IDs remaining: "
      f"{df['transaction_id'].duplicated().sum():,}")

print("=" * 50)


