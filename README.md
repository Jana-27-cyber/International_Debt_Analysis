# International Debt Analysis System

## Project Overview
This project analyzes international debt data using Python, SQL, and Streamlit.

## Technologies Used
- Python
- Pandas
- SQLite
- DBeaver
- Streamlit
- Matplotlib

## Data Cleaning
- Null values handled using Forward Fill and Backward Fill
- Duplicate records removed
- Year columns filtered (2000–2024)

## Data Transformation
Wide format converted to Long format:

country_name
country_code
indicator_name
indicator_code
year
debt_value

## Database
SQLite database created and loaded with cleaned data.

## Dashboard Features
- KPI Metrics
- Year-wise Debt Trend
- Top 10 Countries
- Top 10 Indicators
- Country-wise Analysis
- Search Functionality
- Download Option

## Key Insights
- Debt trends increased significantly across years.
- Some countries contribute major portions of global debt.
- Several indicators dominate total debt contribution.