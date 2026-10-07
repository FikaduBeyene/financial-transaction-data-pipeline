from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "screenshots" / "04_cleaning_results.png"


# ---------------------------------------------------------
# Actual project results
# ---------------------------------------------------------

raw_rows = 101_000
clean_rows = 99_153
rows_removed = 1_847

retention_rate = 98.17
removal_rate = 1.83

exact_duplicates_removed = 911
invalid_dates_removed = 796
invalid_amounts_removed = 93
duplicate_ids_resolved = 47

validation_checks_passed = 10
validation_checks_total = 10


# ---------------------------------------------------------
# Create figure
# ---------------------------------------------------------

fig = plt.figure(figsize=(14, 9), dpi=150)
fig.patch.set_facecolor("white")


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

fig.text(
    0.05,
    0.94,
    "Financial Transaction Data Cleaning Results",
    fontsize=22,
    fontweight="bold",
    ha="left"
)

fig.text(
    0.05,
    0.905,
    "Raw financial transaction data transformed into a validated, analytics-ready dataset.",
    fontsize=11,
    ha="left"
)


# ---------------------------------------------------------
# Data volume chart
# ---------------------------------------------------------

ax = fig.add_axes([0.08, 0.49, 0.84, 0.34])

stages = ["Raw Data", "Clean Data"]
row_counts = [raw_rows, clean_rows]

bars = ax.bar(
    stages,
    row_counts,
    width=0.55
)

ax.set_title(
    "Data Volume Before and After Cleaning",
    fontsize=14,
    fontweight="bold",
    loc="left",
    pad=15
)

ax.set_ylabel("Transaction Rows")

ax.set_ylim(0, 110_000)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.25
)

ax.set_axisbelow(True)


# ---------------------------------------------------------
# Bar labels
# ---------------------------------------------------------

for bar, value in zip(bars, row_counts):

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2_000,
        f"{value:,}",
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold"
    )


# ---------------------------------------------------------
# Cleaning summary
# ---------------------------------------------------------

fig.text(
    0.50,
    0.455,
    f"{rows_removed:,} rows removed  •  "
    f"{removal_rate:.2f}% removed  •  "
    f"{retention_rate:.2f}% retained",
    ha="center",
    fontsize=11,
    fontweight="bold"
)


# ---------------------------------------------------------
# KPI card function
# ---------------------------------------------------------

def add_kpi_card(x, y, width, height, title, value):

    card = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        linewidth=0.8,
        edgecolor="lightgray",
        facecolor="white"
    )

    fig.add_artist(card)

    fig.text(
        x + width / 2,
        y + height * 0.65,
        title,
        ha="center",
        va="center",
        fontsize=9
    )

    fig.text(
        x + width / 2,
        y + height * 0.30,
        f"{value:,}",
        ha="center",
        va="center",
        fontsize=17,
        fontweight="bold"
    )


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------

card_width = 0.19
card_height = 0.095
card_y = 0.325

card_positions = [
    0.05,
    0.275,
    0.50,
    0.725
]

add_kpi_card(
    card_positions[0],
    card_y,
    card_width,
    card_height,
    "Exact Duplicates Removed",
    exact_duplicates_removed
)

add_kpi_card(
    card_positions[1],
    card_y,
    card_width,
    card_height,
    "Invalid Dates Removed",
    invalid_dates_removed
)

add_kpi_card(
    card_positions[2],
    card_y,
    card_width,
    card_height,
    "Invalid Amounts Removed",
    invalid_amounts_removed
)

add_kpi_card(
    card_positions[3],
    card_y,
    card_width,
    card_height,
    "Duplicate IDs Resolved",
    duplicate_ids_resolved
)


# ---------------------------------------------------------
# Final data quality box
# ---------------------------------------------------------

validation_box = FancyBboxPatch(
    (0.05, 0.065),
    0.90,
    0.205,
    boxstyle="round,pad=0.015,rounding_size=0.02",
    linewidth=0.8,
    edgecolor="lightgray",
    facecolor="white"
)

fig.add_artist(validation_box)


# ---------------------------------------------------------
# Section title
# ---------------------------------------------------------

fig.text(
    0.08,
    0.235,
    "FINAL DATA QUALITY",
    fontsize=12,
    fontweight="bold",
    ha="left"
)


# ---------------------------------------------------------
# Validation results
# ---------------------------------------------------------

validation_items_left = [
    "Missing Values: 0",
    "Duplicate Rows: 0",
    "Duplicate Transaction IDs: 0",
    "Invalid Dates: 0",
    "Invalid Amounts: 0"
]

validation_items_right = [
    "Invalid States: 0",
    "Invalid Statuses: 0",
    "Invalid Transaction Types: 0",
    "Invalid Categories: 0",
    "Invalid Payment Methods: 0"
]


# Left column

for index, item in enumerate(validation_items_left):

    fig.text(
        0.08,
        0.195 - index * 0.027,
        "✓  " + item,
        fontsize=8.5,
        ha="left"
    )


# Right column

for index, item in enumerate(validation_items_right):

    fig.text(
        0.48,
        0.195 - index * 0.027,
        "✓  " + item,
        fontsize=8.5,
        ha="left"
    )


# ---------------------------------------------------------
# Checks passed indicator
# ---------------------------------------------------------

fig.text(
    0.82,
    0.155,
    f"{validation_checks_passed}/{validation_checks_total}",
    fontsize=21,
    fontweight="bold",
    ha="center"
)

fig.text(
    0.82,
    0.125,
    "CHECKS PASSED",
    fontsize=8.5,
    fontweight="bold",
    ha="center"
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


print("Cleaning results visual created successfully:")
print(OUTPUT_FILE)