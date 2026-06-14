import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="International Debt Analysis", layout="wide")

DB_PATH = "international_debt.db"

st.title("🌍 International Debt Analysis Dashboard")

@st.cache_data
def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# KPI data
summary = run_query("""
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT country_name) AS total_countries,
    COUNT(DISTINCT indicator_name) AS total_indicators,
    MIN(year) AS min_year,
    MAX(year) AS max_year,
    SUM(debt_value) AS total_debt
FROM debt_data;
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{summary['total_records'][0]:,}")
col2.metric("Total Countries", summary["total_countries"][0])
col3.metric("Total Indicators", summary["total_indicators"][0])
col4.metric("Year Range", f"{summary['min_year'][0]} - {summary['max_year'][0]}")

st.metric("💰 Total Global Debt", f"{summary['total_debt'][0]:,.0f}")

st.divider()

# Filters
st.sidebar.header("🔎 Filters")

years = run_query("SELECT DISTINCT year FROM debt_data ORDER BY year;")
countries = run_query("SELECT DISTINCT country_name FROM debt_data ORDER BY country_name;")

selected_year = st.sidebar.selectbox("Select Year", years["year"].tolist())

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + countries["country_name"].tolist()
)

st.subheader("📂 Filtered Sample Data")

if selected_country == "All":
    filtered_query = f"""
    SELECT *
    FROM debt_data
    WHERE year = {selected_year}
    LIMIT 100;
    """
else:
    filtered_query = f"""
    SELECT *
    FROM debt_data
    WHERE year = {selected_year}
    AND country_name = '{selected_country.replace("'", "''")}'
    LIMIT 100;
    """

filtered_df = run_query(filtered_query)
st.dataframe(filtered_df)

st.divider()

# Year-wise trend
st.subheader("📈 Year-wise Total Debt Trend")

year_data = run_query("""
SELECT year,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY year
ORDER BY year;
""")

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(year_data["year"], year_data["total_debt"], marker="o")
ax1.set_title("Year-wise Total Debt Trend")
ax1.set_xlabel("Year")
ax1.set_ylabel("Total Debt")
ax1.grid(True)
st.pyplot(fig1)

st.divider()

# Top countries
st.subheader("🌍 Top 10 Countries by Total Debt")

top_countries = run_query("""
SELECT country_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;
""")

st.dataframe(top_countries)

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.bar(top_countries["country_name"], top_countries["total_debt"])
ax2.set_title("Top 10 Countries by Total Debt")
ax2.set_xlabel("Country")
ax2.set_ylabel("Total Debt")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig2)

st.divider()

# Top indicators
st.subheader("📊 Top 10 Debt Indicators")

top_indicators = run_query("""
SELECT indicator_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC
LIMIT 10;
""")

st.dataframe(top_indicators)

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.bar(top_indicators["indicator_name"], top_indicators["total_debt"])
ax3.set_title("Top 10 Debt Indicators")
ax3.set_xlabel("Indicator")
ax3.set_ylabel("Total Debt")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig3)

st.divider()

# Pie chart
st.subheader("🥧 Top 10 Countries Debt Share")

fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(
    top_countries["total_debt"],
    labels=top_countries["country_name"],
    autopct="%1.1f%%"
)
ax4.set_title("Debt Share of Top 10 Countries")
st.pyplot(fig4)

st.divider()

# Country trend
st.subheader("🔍 Country-wise Debt Trend")

country_for_trend = st.selectbox(
    "Choose Country for Trend Analysis",
    countries["country_name"].tolist()
)

country_for_trend_safe = country_for_trend.replace("'", "''")

country_year_data = run_query(f"""
SELECT year,
       SUM(debt_value) AS total_debt
FROM debt_data
WHERE country_name = '{country_for_trend_safe}'
GROUP BY year
ORDER BY year;
""")

fig5, ax5 = plt.subplots(figsize=(12, 5))
ax5.plot(country_year_data["year"], country_year_data["total_debt"], marker="o")
ax5.set_title(f"Debt Trend for {country_for_trend}")
ax5.set_xlabel("Year")
ax5.set_ylabel("Total Debt")
ax5.grid(True)
st.pyplot(fig5)

st.divider()

# Search
st.subheader("🔎 Search Country")

search_country = st.text_input("Enter country name")

if search_country:
    search_safe = search_country.replace("'", "''")

    search_result = run_query(f"""
    SELECT *
    FROM debt_data
    WHERE country_name LIKE '%{search_safe}%'
    LIMIT 100;
    """)

    st.dataframe(search_result)

st.divider()

# Download sample
st.subheader("⬇️ Download Sample Data")

sample_df = run_query("""
SELECT *
FROM debt_data
LIMIT 5000;
""")

csv_data = sample_df.to_csv(index=False)

st.download_button(
    label="Download Sample Dataset",
    data=csv_data,
    file_name="sample_debt_data.csv",
    mime="text/csv"
)

st.success("✅ Optimized Dashboard Loaded Successfully!")