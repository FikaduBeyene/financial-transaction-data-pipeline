from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# ----------------------------
# File locations
# ----------------------------

processed_file = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "transactions_clean.csv"
)

print("Cleaned dataset:")
print(processed_file)


# ----------------------------
# Load cleaned dataset
# ----------------------------

df = pd.read_csv(processed_file)

print("\nCleaned dataset loaded successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Shape:", df.shape)


# ----------------------------
# SQL Server connection
# ----------------------------

server = "."
database = "FinancialDataPipeline"

connection_string = (
    "mssql+pyodbc://"
    f"{server}/{database}"
    "?trusted_connection=yes"
    "&driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(connection_string)

# ----------------------------
# Test SQL Server connection
# ----------------------------

with engine.connect() as connection:
    print("\nSQL Server connection successful.")


# ----------------------------
# Load data into SQL Server
# ----------------------------

print("\nLoading data into SQL Server...")

df.to_sql(
    name="transactions",
    con=engine,
    schema="dbo",
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Data loaded successfully.")
print(f"Rows loaded: {len(df):,}")


