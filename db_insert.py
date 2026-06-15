import pandas as pd
import sqlite3

CSV_FILE = "data/final_master_dataset.csv"
DB_FILE = "international_debt.db"
TABLE_NAME = "debt_data"

print("Reading final master dataset...")
df = pd.read_csv(CSV_FILE)

print("Columns:")
print(df.columns.tolist())

conn = sqlite3.connect(DB_FILE)

print("Inserting data into SQLite...")
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

conn.close()

print("Database updated successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])