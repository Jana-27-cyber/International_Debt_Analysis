import pandas as pd
import sqlite3

df = pd.read_csv("data/cleaned_debt.csv")

conn = sqlite3.connect("international_debt.db")

df.to_sql(
    "debt_data",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Data inserted successfully!")
print(df.shape)