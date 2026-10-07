from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "transactions_clean.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "screenshots"
    / "05_validation_results.png"
)


# ---------------------------------------------------------
# Load cleaned dataset
# ---------------------------------------------------------

df = pd.read_csv(CLEANED_FILE)

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)


# ---------------------------------------------------------
# Allowed business values
# ---------------------------------------------------------

valid_states = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "Unknown"
}

valid_statuses = {
    "Completed",
    "Pending",
    "Failed",
    "Reversed",
    "Unknown"
}

valid_transaction_types = {
    "Debit",
    "Credit"
}

valid_categories = {
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
}

valid_payment_methods = {
    "Credit Card",
    "Debit Card",
    "ACH",
    "Wire Transfer",
    "Cash",
    "Check",
    "Unknown"
}


# ---------------------------------------------------------
# Run validation checks
# ---------------------------------------------------------

duplicate_rows = int(df.duplicated().sum())

missing_values = int(df.isna().sum().sum())

duplicate_transaction_ids = int(
    df["transaction_id"].duplicated().sum()
)

invalid_dates = int(
    (
        df["transaction_date"].isna()
        |
        (df["transaction_date"] < pd.Timestamp("2025-01-01"))
        |
        (df["transaction_date"] > pd.Timestamp("2026-09-25"))
    ).sum()
)

invalid_amounts = int(
    (
        (df["amount"] <= 0)
        |
        (df["amount"] > 5000)
    ).sum()
)

invalid_states = int(
    (~df["state"].isin(valid_states)).sum()
)

invalid_statuses = int(
    (~df["status"].isin(valid_statuses)).sum()
)

invalid_transaction_types = int(
    (~df["transaction_type"].isin(valid_transaction_types)).sum()
)

invalid_categories = int(
    (~df["category"].isin(valid_categories)).sum()
)

invalid_payment_methods = int(
    (~df["payment_method"].isin(valid_payment_methods)).sum()
)


# ---------------------------------------------------------
# Validation results
# ---------------------------------------------------------

validation_results = [
    ("Duplicate Rows", duplicate_rows),
    ("Missing Values", missing_values),
    ("Duplicate Transaction IDs", duplicate_transaction_ids),
    ("Invalid Dates", invalid_dates),
    ("Invalid Amounts", invalid_amounts),
    ("Invalid States", invalid_states),
    ("Invalid Statuses", invalid_statuses),
    ("Invalid Transaction Types", invalid_transaction_types),
    ("Invalid Categories", invalid_categories),
    ("Invalid Payment Methods", invalid_payment_methods)
]


passed_checks = sum(
    value == 0
    for _, value in validation_results
)

total_checks = len(validation_results)

failed_checks = total_checks - passed_checks

overall_status = (
    "PASS"
    if failed_checks == 0
    else "FAIL"
)


# ---------------------------------------------------------
# Print results to console
# ---------------------------------------------------------

print("=" * 60)
print("DATA QUALITY VALIDATION RESULTS")
print("=" * 60)

print(f"\nDataset rows: {len(df):,}")
print(f"Dataset columns: {len(df.columns)}")

print("\nValidation Checks:")

for check_name, value in validation_results:

    status = "PASS" if value == 0 else "FAIL"

    print(
        f"{check_name:<35}"
        f"{value:<10}"
        f"{status}"
    )

print("\n" + "=" * 60)

print(
    f"Checks Passed: "
    f"{passed_checks}/{total_checks}"
)

print(
    f"Checks Failed: "
    f"{failed_checks}"
)

print(
    f"Overall Data Quality Status: "
    f"{overall_status}"
)

print("=" * 60)


# ---------------------------------------------------------
# Create portfolio visual
# ---------------------------------------------------------

fig = plt.figure(
    figsize=(14, 9),
    dpi=150
)

fig.patch.set_facecolor("white")


# ---------------------------------------------------------
# Main title
# ---------------------------------------------------------

fig.text(
    0.05,
    0.94,
    "Financial Transaction Data Quality Validation",
    fontsize=22,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.05,
    0.905,
    "Automated validation confirms the cleaned dataset meets defined business and data quality rules.",
    fontsize=11,
    ha="left"
)


# ---------------------------------------------------------
# Dataset summary
# ---------------------------------------------------------

fig.text(
    0.05,
    0.845,
    f"{len(df):,}",
    fontsize=24,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.05,
    0.815,
    "TRANSACTIONS VALIDATED",
    fontsize=9,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.28,
    0.845,
    f"{total_checks}",
    fontsize=24,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.28,
    0.815,
    "VALIDATION RULES",
    fontsize=9,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.48,
    0.845,
    f"{passed_checks}",
    fontsize=24,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.48,
    0.815,
    "CHECKS PASSED",
    fontsize=9,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.68,
    0.845,
    f"{failed_checks}",
    fontsize=24,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.68,
    0.815,
    "CHECKS FAILED",
    fontsize=9,
    fontweight="bold",
    ha="left"
)


# ---------------------------------------------------------
# Validation results box
# ---------------------------------------------------------

results_box = FancyBboxPatch(
    (0.05, 0.22),
    0.90,
    0.53,
    boxstyle="round,pad=0.015,rounding_size=0.02",
    linewidth=0.8,
    edgecolor="lightgray",
    facecolor="white"
)

fig.add_artist(results_box)


# ---------------------------------------------------------
# Validation box heading
# ---------------------------------------------------------

fig.text(
    0.08,
    0.705,
    "VALIDATION CHECK",
    fontsize=10,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.39,
    0.705,
    "ISSUES FOUND",
    fontsize=10,
    fontweight="bold",
    ha="center"
)

fig.text(
    0.50,
    0.705,
    "VALIDATION CHECK",
    fontsize=10,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.81,
    0.705,
    "ISSUES FOUND",
    fontsize=10,
    fontweight="bold",
    ha="center"
)


# ---------------------------------------------------------
# Split checks into two columns
# ---------------------------------------------------------

left_checks = validation_results[:5]
right_checks = validation_results[5:]

start_y = 0.645
row_spacing = 0.082


# ---------------------------------------------------------
# Left validation column
# ---------------------------------------------------------

for index, (check_name, value) in enumerate(left_checks):

    y = start_y - index * row_spacing

    status = "PASS" if value == 0 else "FAIL"

    fig.text(
        0.08,
        y,
        check_name,
        fontsize=10,
        ha="left"
    )

    fig.text(
        0.39,
        y,
        f"{value}",
        fontsize=10,
        fontweight="bold",
        ha="center"
    )

    fig.text(
        0.43,
        y,
        status,
        fontsize=9,
        fontweight="bold",
        ha="left"
    )


# ---------------------------------------------------------
# Right validation column
# ---------------------------------------------------------

for index, (check_name, value) in enumerate(right_checks):

    y = start_y - index * row_spacing

    status = "PASS" if value == 0 else "FAIL"

    fig.text(
        0.50,
        y,
        check_name,
        fontsize=10,
        ha="left"
    )

    fig.text(
        0.81,
        y,
        f"{value}",
        fontsize=10,
        fontweight="bold",
        ha="center"
    )

    fig.text(
        0.85,
        y,
        status,
        fontsize=9,
        fontweight="bold",
        ha="left"
    )


# ---------------------------------------------------------
# Overall result
# ---------------------------------------------------------

status_box = FancyBboxPatch(
    (0.05, 0.07),
    0.90,
    0.09,
    boxstyle="round,pad=0.015,rounding_size=0.02",
    linewidth=0.8,
    edgecolor="lightgray",
    facecolor="white"
)

fig.add_artist(status_box)

fig.text(
    0.08,
    0.115,
    "OVERALL DATA QUALITY STATUS",
    fontsize=10,
    fontweight="bold",
    ha="left",
    va="center"
)

fig.text(
    0.62,
    0.115,
    f"{passed_checks}/{total_checks} CHECKS PASSED",
    fontsize=13,
    fontweight="bold",
    ha="center",
    va="center"
)

fig.text(
    0.88,
    0.115,
    overall_status,
    fontsize=18,
    fontweight="bold",
    ha="center",
    va="center"
)


# ---------------------------------------------------------
# Save image
# ---------------------------------------------------------

plt.savefig(
    OUTPUT_FILE,
    dpi=200,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()


print("\nValidation results visual created successfully:")
print(OUTPUT_FILE)