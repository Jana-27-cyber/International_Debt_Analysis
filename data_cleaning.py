import pandas as pd

# 1. Load dataset
df = pd.read_csv(
    "data/IDS_ALLCountries_Data.csv",
    encoding="latin1"
)

print("Original Shape:", df.shape)

# 2. Remove duplicate rows
print("\nDuplicate rows before:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate rows after:", df.duplicated().sum())

# 3. Select year columns from 2000 to 2024 only
year_cols = [
    col for col in df.columns
    if col.isdigit() and 2000 <= int(col) <= 2024
]

print("\nYear columns used:")
print(year_cols)

# 4. Null count before filling
print("\nNull values before filling:")
print(df[year_cols].isnull().sum())

# 5. Forward fill + Backward fill row-wise
df[year_cols] = df[year_cols].ffill(axis=1).bfill(axis=1)

# 6. Null count after filling
print("\nNull values after forward fill and backward fill:")
print(df[year_cols].isnull().sum())

# 7. Text columns null handling
text_cols = ["Country Name", "Country Code", "Series Name", "Series Code"]
df[text_cols] = df[text_cols].fillna("Unknown")

# 8. Convert wide format to long format
df_long = df.melt(
    id_vars=text_cols,
    value_vars=year_cols,
    var_name="year",
    value_name="debt_value"
)

# 9. Rename columns
df_long = df_long.rename(columns={
    "Country Name": "country_name",
    "Country Code": "country_code",
    "Series Name": "indicator_name",
    "Series Code": "indicator_code"
})

# 10. Convert data types
df_long["year"] = df_long["year"].astype(int)
df_long["debt_value"] = pd.to_numeric(
    df_long["debt_value"],
    errors="coerce"
).fillna(0)

# 11. Save cleaned transformed dataset
df_long.to_csv("data/cleaned_debt.csv", index=False)

print("\nFinal Transformed Shape:", df_long.shape)

print("\nFinal Null Check:")
print(df_long.isnull().sum())

print("\nFinal Table Preview:")
print(df_long.head())

print("\nCleaned file created successfully: data/cleaned_debt.csv")

print("\nRemaining Null Values:")
print(df_long.isnull().sum())

print("\nTotal Remaining Null Values:")
print(df_long.isnull().sum().sum())

print(df_long.duplicated().sum())

df_long = df_long.drop_duplicates()

print("\nShape After Removing Duplicates:")
print(df.shape)

print("\nYear Columns:")
print(year_cols)

print("\nNumber of Year Columns:")
print(len(year_cols))

print(df_long.columns)
print(df_long.shape)

print("\nDebt Value Statistics:")
print(df_long["debt_value"].describe())

print("\nNegative Debt Values:")
print((df_long["debt_value"] < 0).sum())

print("\nZero Debt Values:")
print((df_long["debt_value"] == 0).sum())

print("\nFirst 10 Rows:")
print(df_long.head(10))

cleaned_df = pd.read_csv("data/cleaned_debt.csv")

print(cleaned_df.head(10))
print(cleaned_df.shape)