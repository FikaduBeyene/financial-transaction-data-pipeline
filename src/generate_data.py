import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


# ----------------------------
# Configuration
# ----------------------------

RANDOM_SEED = 42
NUM_TRANSACTIONS = 100_000

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ----------------------------
# Reference data
# ----------------------------

transaction_types = [
    "Debit",
    "Credit"
]

categories = [
    "Groceries",
    "Utilities",
    "Dining",
    "Transportation",
    "Healthcare",
    "Entertainment",
    "Shopping",
    "Salary",
    "Transfer",
    "Other"
]

payment_methods = [
    "Credit Card",
    "Debit Card",
    "ACH",
    "Wire Transfer",
    "Cash",
    "Check"
]

states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "IA", "ID", "IL", "IN", "KS", "KY",
    "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS",
    "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
    "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
    "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"
]

statuses = [
    "Completed",
    "Pending",
    "Failed",
    "Reversed"
]


# ----------------------------
# Category-specific merchants
# ----------------------------

category_merchants = {
    "Groceries": [
        "Walmart",
        "Kroger",
        "Whole Foods",
        "Costco"
    ],

    "Utilities": [
        "AT&T",
        "Verizon"
    ],

    "Dining": [
        "Starbucks",
        "McDonald's",
        "Chipotle"
    ],

    "Transportation": [
        "Shell",
        "Exxon",
        "Uber"
    ],

    "Healthcare": [
        "CVS",
        "Walgreens"
    ],

    "Entertainment": [
        "Netflix",
        "Spotify"
    ],

    "Shopping": [
        "Amazon",
        "Target",
        "Walmart",
        "Home Depot"
    ],

    "Salary": [
        "Employer Payroll"
    ],

    "Transfer": [
        "Bank Transfer"
    ],

    "Other": [
        "Amazon",
        "Walmart",
        "Target"
    ]
}


# ----------------------------
# Category distribution
# ----------------------------
#
# These probabilities make the dataset
# less uniform and more representative
# of different transaction frequencies.
#
# They must add up to 1.00.

category_probabilities = {
    "Groceries": 0.14,
    "Utilities": 0.08,
    "Dining": 0.16,
    "Transportation": 0.12,
    "Healthcare": 0.06,
    "Entertainment": 0.07,
    "Shopping": 0.13,
    "Salary": 0.05,
    "Transfer": 0.08,
    "Other": 0.11
}


# ----------------------------
# Customer activity distribution
# ----------------------------
#
# Instead of giving every customer exactly
# the same chance of appearing, we create
# a more realistic uneven distribution.
#
# Some customers will have more transactions
# than others.

customer_ids = [
    f"CUST{i:06d}"
    for i in range(1, 10_001)
]

customer_weights = np.random.exponential(
    scale=1.0,
    size=len(customer_ids)
)

customer_weights = customer_weights / customer_weights.sum()


# ----------------------------
# Helper function:
# Generate realistic transaction amounts
# ----------------------------

def generate_amount(category):
    """
    Generate a realistic transaction amount
    based on the transaction category.
    """

    if category == "Groceries":
        amount = np.random.lognormal(
            mean=np.log(110),
            sigma=0.45
        )

    elif category == "Utilities":
        amount = np.random.normal(
            loc=180,
            scale=55
        )

    elif category == "Dining":
        amount = np.random.lognormal(
            mean=np.log(48),
            sigma=0.45
        )

    elif category == "Transportation":
        amount = np.random.lognormal(
            mean=np.log(70),
            sigma=0.50
        )

    elif category == "Healthcare":
        amount = np.random.lognormal(
            mean=np.log(425),
            sigma=0.70
        )

    elif category == "Entertainment":
        amount = np.random.lognormal(
            mean=np.log(55),
            sigma=0.50
        )

    elif category == "Shopping":
        amount = np.random.lognormal(
            mean=np.log(175),
            sigma=0.75
        )

    elif category == "Salary":
        amount = np.random.normal(
            loc=3_200,
            scale=650
        )

    elif category == "Transfer":
        amount = np.random.lognormal(
            mean=np.log(1_500),
            sigma=0.75
        )

    else:
        amount = np.random.lognormal(
            mean=np.log(125),
            sigma=0.70
        )

    # Keep valid transactions within our
    # project's existing business rule.
    amount = np.clip(amount, 5.00, 5_000.00)

    return round(float(amount), 2)


# ----------------------------
# Generate valid transactions
# ----------------------------

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 9, 25)

date_range_days = (end_date - start_date).days

transactions = []

category_list = list(category_probabilities.keys())
category_weights = list(category_probabilities.values())


for i in range(1, NUM_TRANSACTIONS + 1):

    # Generate transaction date
    transaction_date = start_date + timedelta(
        days=random.randint(0, date_range_days)
    )

    # Select customer using uneven activity distribution
    customer_id = np.random.choice(
        customer_ids,
        p=customer_weights
    )

    # Select category using realistic probabilities
    category = random.choices(
        category_list,
        weights=category_weights,
        k=1
    )[0]

    # ----------------------------
    # Transaction type
    # ----------------------------

    if category == "Salary":
        transaction_type = "Credit"

    elif category == "Transfer":
        transaction_type = random.choices(
            ["Debit", "Credit"],
            weights=[0.60, 0.40],
            k=1
        )[0]

    else:
        transaction_type = "Debit"

    # ----------------------------
    # Payment method
    # ----------------------------

    if category == "Salary":
        payment_method = "ACH"

    elif category == "Transfer":
        payment_method = random.choices(
            ["ACH", "Wire Transfer"],
            weights=[0.75, 0.25],
            k=1
        )[0]

    elif category == "Utilities":
        payment_method = random.choices(
            ["ACH", "Credit Card", "Debit Card"],
            weights=[0.45, 0.35, 0.20],
            k=1
        )[0]

    elif category in ["Groceries", "Dining", "Shopping"]:
        payment_method = random.choices(
            ["Credit Card", "Debit Card", "Cash"],
            weights=[0.50, 0.40, 0.10],
            k=1
        )[0]

    elif category == "Healthcare":
        payment_method = random.choices(
            ["Credit Card", "Debit Card", "ACH", "Cash"],
            weights=[0.40, 0.30, 0.20, 0.10],
            k=1
        )[0]

    else:
        payment_method = random.choices(
            payment_methods,
            weights=[0.30, 0.30, 0.15, 0.05, 0.15, 0.05],
            k=1
        )[0]

    # ----------------------------
    # Merchant
    # ----------------------------

    merchant = random.choice(
        category_merchants[category]
    )

    # ----------------------------
    # Transaction amount
    # ----------------------------

    amount = generate_amount(category)

    # ----------------------------
    # Transaction status
    # ----------------------------

    status = random.choices(
        statuses,
        weights=[0.94, 0.03, 0.02, 0.01],
        k=1
    )[0]

    # ----------------------------
    # Build transaction
    # ----------------------------

    transaction = {
        "transaction_id": f"TXN{i:06d}",
        "customer_id": customer_id,
        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
        "transaction_type": transaction_type,
        "category": category,
        "amount": amount,
        "payment_method": payment_method,
        "state": random.choice(states),
        "status": status,
        "merchant": merchant
    }

    transactions.append(transaction)


df = pd.DataFrame(transactions)


# Keep a copy of the clean baseline for comparison
df_clean_baseline = df.copy()


# ----------------------------
# Introduce duplicate records
# ----------------------------

duplicate_count = 1_000

duplicates = df.sample(
    n=duplicate_count,
    random_state=RANDOM_SEED
)

df = pd.concat(
    [df, duplicates],
    ignore_index=True
)

print("\nAfter introducing duplicates:")
print("Dataset shape:", df.shape)


# ----------------------------
# Introduce missing values
# ----------------------------

missing_value_count = 500

missing_columns = [
    "transaction_date",
    "category",
    "payment_method",
    "state",
    "merchant"
]

for column in missing_columns:

    missing_indices = df.sample(
        n=missing_value_count,
        random_state=RANDOM_SEED + missing_columns.index(column)
    ).index

    df.loc[missing_indices, column] = np.nan


print("\nAfter introducing missing values:")
print(df[missing_columns].isnull().sum())


# ----------------------------
# Introduce inconsistent text formatting
# ----------------------------

inconsistent_count = 300


# Transaction type inconsistencies
indices = df.sample(
    n=inconsistent_count,
    random_state=100
).index

df.loc[indices, "transaction_type"] = df.loc[
    indices, "transaction_type"
].str.lower()


# Category inconsistencies
indices = df.sample(
    n=inconsistent_count,
    random_state=101
).index

df.loc[indices, "category"] = df.loc[
    indices, "category"
].str.lower()


# Payment method inconsistencies
indices = df.sample(
    n=inconsistent_count,
    random_state=102
).index

df.loc[indices, "payment_method"] = df.loc[
    indices, "payment_method"
].str.upper()


print("\nAfter introducing inconsistent text values:")

print("\nTransaction types:")
print(df["transaction_type"].value_counts())

print("\nCategories:")
print(df["category"].value_counts())

print("\nPayment methods:")
print(df["payment_method"].value_counts())


# ----------------------------
# Introduce invalid transaction dates
# ----------------------------

invalid_date_count = 300

invalid_date_indices = df.sample(
    n=invalid_date_count,
    random_state=200
).index

invalid_dates = [
    "2024-12-15",
    "2027-01-10",
    "not-a-date",
    "2025-13-45",
    "2026-02-30"
]

df.loc[invalid_date_indices, "transaction_date"] = [
    invalid_dates[i % len(invalid_dates)]
    for i in range(len(invalid_date_indices))
]

print("\nAfter introducing invalid dates:")
print(
    df.loc[
        invalid_date_indices,
        "transaction_date"
    ].value_counts()
)


# ----------------------------
# Introduce invalid transaction amounts
# ----------------------------

invalid_amount_count = 93

invalid_amount_indices = df.sample(
    n=invalid_amount_count,
    random_state=300
).index

invalid_amounts = [
    -25.50,
    0.00,
    -1500.00,
    9999999.99,
    -500.00
]

df.loc[invalid_amount_indices, "amount"] = [
    invalid_amounts[i % len(invalid_amounts)]
    for i in range(len(invalid_amount_indices))
]

print("\nAfter introducing invalid amounts:")
print(
    df.loc[
        invalid_amount_indices,
        "amount"
    ].value_counts()
)


# ----------------------------
# Introduce invalid state values
# ----------------------------

invalid_state_count = 87

invalid_state_indices = df.sample(
    n=invalid_state_count,
    random_state=400
).index

invalid_states = [
    "Missouri",
    "KANSAS",
    "XX",
    "123",
    "California"
]

df.loc[invalid_state_indices, "state"] = [
    invalid_states[i % len(invalid_states)]
    for i in range(len(invalid_state_indices))
]

print("\nAfter introducing invalid state values:")
print(
    df.loc[
        invalid_state_indices,
        "state"
    ].value_counts()
)


# ----------------------------
# Introduce invalid transaction statuses
# ----------------------------

invalid_status_count = 73

invalid_status_indices = df.sample(
    n=invalid_status_count,
    random_state=500
).index

invalid_statuses = [
    "Complete",
    "CANCELLED",
    "Unknown",
    "N/A"
]

df.loc[invalid_status_indices, "status"] = [
    invalid_statuses[i % len(invalid_statuses)]
    for i in range(len(invalid_status_indices))
]

print("\nAfter introducing invalid transaction statuses:")
print(
    df.loc[
        invalid_status_indices,
        "status"
    ].value_counts()
)


# ----------------------------
# Raw data quality summary
# ----------------------------

print("\n" + "=" * 50)
print("RAW DATA QUALITY SUMMARY")
print("=" * 50)

print(f"\nTotal rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")


print("\nDuplicate rows:")
print(df.duplicated().sum())


print("\nMissing values by column:")
print(df.isnull().sum())


print("\nInvalid amounts (<= 0 or > 5000):")
print(
    (
        (df["amount"] <= 0)
        | (df["amount"] > 5000)
    ).sum()
)


print("\nPotential invalid states:")
valid_states = set(states)

print(
    (
        ~df["state"].isin(valid_states)
        & df["state"].notna()
    ).sum()
)


print("\nPotential invalid statuses:")
valid_statuses = set(statuses)

print(
    (
        ~df["status"].isin(valid_statuses)
        & df["status"].notna()
    ).sum()
)


print("\nPotential invalid dates:")

parsed_dates = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

missing_dates = (
    df["transaction_date"]
    .isna()
    .sum()
)

unparseable_dates = (
    parsed_dates.isna()
    & df["transaction_date"].notna()
).sum()

out_of_range_dates = (
    parsed_dates.notna()
    & (
        (parsed_dates < pd.Timestamp(start_date))
        | (parsed_dates > pd.Timestamp(end_date))
    )
).sum()

print("Missing dates:", missing_dates)
print("Unparseable dates:", unparseable_dates)
print(
    "Dates outside business range:",
    out_of_range_dates
)


print("\nPotential inconsistent transaction types:")
print(
    (
        ~df["transaction_type"].isin(transaction_types)
        & df["transaction_type"].notna()
    ).sum()
)


print("\nPotential inconsistent categories:")
print(
    (
        ~df["category"].isin(categories)
        & df["category"].notna()
    ).sum()
)


print("\nPotential inconsistent payment methods:")
print(
    (
        ~df["payment_method"].isin(payment_methods)
        & df["payment_method"].notna()
    ).sum()
)


# ----------------------------
# Inspect generated dataset
# ----------------------------

print("\n" + "=" * 50)
print("GENERATED DATASET")
print("=" * 50)

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())


# ----------------------------
# Business distribution preview
# ----------------------------
#
# Use the clean baseline here.
# The raw dataframe intentionally contains
# data-quality problems that should not be
# used for business analysis.

print("\n" + "=" * 50)
print("BUSINESS DISTRIBUTION PREVIEW")
print("=" * 50)

print("\nTransactions by category:")

category_preview = (
    df_clean_baseline.groupby("category")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .sort_values(
        "total_amount",
        ascending=False
    )
)

print(category_preview)

# ----------------------------
# Save raw dataset
# ----------------------------

raw_data_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
)

raw_data_path.mkdir(
    parents=True,
    exist_ok=True
)

raw_file = raw_data_path / "transactions_raw.csv"

df.to_csv(
    raw_file,
    index=False
)

print("\nRaw dataset saved successfully:")
print(raw_file)