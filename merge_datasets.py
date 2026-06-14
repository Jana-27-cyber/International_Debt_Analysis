import pandas as pd

# Load cleaned debt data
debt = pd.read_csv("data/cleaned_debt.csv")

# Load country metadata
country_meta = pd.read_csv(
    "data/IDS_CountryMetaData.csv",
    encoding="latin1"
)

# Load series metadata
series_meta = pd.read_csv(
    "data/IDS_SeriesMetaData.csv",
    encoding="latin1"
)

# Select useful country columns
country_meta = country_meta[
    ["Code", "Long Name", "Income Group", "Region", "Lending category", "Currency Unit"]
]

country_meta = country_meta.rename(columns={
    "Code": "country_code",
    "Long Name": "country_full_name",
    "Income Group": "income_group",
    "Region": "region",
    "Lending category": "lending_category",
    "Currency Unit": "currency_unit"
})

# Select useful series columns
series_meta = series_meta[
    ["Code", "Short definition", "Long definition", "Source", "Topic"]
]

series_meta = series_meta.rename(columns={
    "Code": "indicator_code",
    "Short definition": "short_definition",
    "Long definition": "long_definition",
    "Source": "source",
    "Topic": "topic"
})

# Merge debt data with country metadata
final_df = debt.merge(
    country_meta,
    on="country_code",
    how="left"
)

# Merge with series metadata
final_df = final_df.merge(
    series_meta,
    on="indicator_code",
    how="left"
)

# Fill metadata null values
final_df = final_df.fillna("Unknown")

# Save final master dataset
final_df.to_csv("data/final_master_dataset.csv", index=False)

print("Final master dataset created successfully!")
print("Shape:", final_df.shape)

print("\nColumns:")
print(final_df.columns.tolist())

print("\nFirst 5 Rows:")
print(final_df.head())

print("\nNull Values:")
print(final_df.isnull().sum())