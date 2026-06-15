import pandas as pd
import sqlite3

CSV_FILE = "data/final_master_dataset.csv"
DB_FILE = "international_debt.db"
TABLE_NAME = "debt_data"

conn = sqlite3.connect(DB_FILE)

chunk_size = 50000
total_rows = 0

print("Reading and inserting data in chunks...")

for i, chunk in enumerate(pd.read_csv(CSV_FILE, chunksize=chunk_size)):
    if_exists_value = "replace" if i == 0 else "append"

    chunk.to_sql(
        TABLE_NAME,
        conn,
        if_exists=if_exists_value,
        index=False
    )

    total_rows += len(chunk)
    print(f"Inserted rows: {total_rows}")

conn.commit()

count = pd.read_sql("SELECT COUNT(*) AS total FROM debt_data", conn)
print("Final Inserted Rows:", count["total"][0])

conn.close()

print("Database updated successfully!")