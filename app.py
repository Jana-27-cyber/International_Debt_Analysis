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


# ================= KPI SECTION =================
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


# ================= MAIN CHART =================
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


# ================= SQL QUESTIONS =================
st.subheader("📊 SQL Analytical Questions (30)")

sql_questions = {
    # BASIC QUERIES
    "Basic 1. Retrieve all distinct country names from the dataset.": """
SELECT DISTINCT country_name
FROM debt_data
ORDER BY country_name;
""",

    "Basic 2. Count the total number of countries available.": """
SELECT COUNT(DISTINCT country_name) AS total_countries
FROM debt_data;
""",

    "Basic 3. Find the total number of indicators present.": """
SELECT COUNT(DISTINCT indicator_name) AS total_indicators
FROM debt_data;
""",

    "Basic 4. Display the first 10 records of the dataset.": """
SELECT *
FROM debt_data
LIMIT 10;
""",

    "Basic 5. Calculate the total global debt.": """
SELECT SUM(debt_value) AS total_global_debt
FROM debt_data;
""",

    "Basic 6. List all unique indicator names.": """
SELECT DISTINCT indicator_name
FROM debt_data
ORDER BY indicator_name;
""",

    "Basic 7. Find the number of records for each country.": """
SELECT country_name,
       COUNT(*) AS record_count
FROM debt_data
GROUP BY country_name
ORDER BY record_count DESC;
""",

    "Basic 8. Display all records where debt is greater than 1 billion USD.": """
SELECT *
FROM debt_data
WHERE debt_value > 1000000000
LIMIT 100;
""",

    "Basic 9. Find the minimum, maximum, and average debt values.": """
SELECT 
    MIN(debt_value) AS minimum_debt,
    MAX(debt_value) AS maximum_debt,
    AVG(debt_value) AS average_debt
FROM debt_data;
""",

    "Basic 10. Count total number of records in the dataset.": """
SELECT COUNT(*) AS total_records
FROM debt_data;
""",

    # INTERMEDIATE QUERIES
    "Intermediate 1. Find the total debt for each country.": """
SELECT country_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC;
""",

    "Intermediate 2. Display the top 10 countries with the highest total debt.": """
SELECT country_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;
""",

    "Intermediate 3. Find the average debt per country.": """
SELECT country_name,
       AVG(debt_value) AS average_debt
FROM debt_data
GROUP BY country_name
ORDER BY average_debt DESC;
""",

    "Intermediate 4. Calculate total debt for each indicator.": """
SELECT indicator_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC;
""",

    "Intermediate 5. Identify the indicator contributing the highest total debt.": """
SELECT indicator_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC
LIMIT 1;
""",

    "Intermediate 6. Find the country with the lowest total debt.": """
SELECT country_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt ASC
LIMIT 1;
""",

    "Intermediate 7. Calculate total debt for each country and indicator combination.": """
SELECT country_name,
       indicator_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name, indicator_name
ORDER BY total_debt DESC
LIMIT 100;
""",

    "Intermediate 8. Count how many indicators each country has.": """
SELECT country_name,
       COUNT(DISTINCT indicator_name) AS indicator_count
FROM debt_data
GROUP BY country_name
ORDER BY indicator_count DESC;
""",

    "Intermediate 9. Display countries whose total debt is above the global average.": """
WITH country_debt AS (
    SELECT country_name,
           SUM(debt_value) AS total_debt
    FROM debt_data
    GROUP BY country_name
)
SELECT country_name,
       total_debt
FROM country_debt
WHERE total_debt > (
    SELECT AVG(total_debt)
    FROM country_debt
)
ORDER BY total_debt DESC;
""",

    "Intermediate 10. Rank countries based on total debt (highest to lowest).": """
SELECT country_name,
       SUM(debt_value) AS total_debt,
       RANK() OVER (ORDER BY SUM(debt_value) DESC) AS debt_rank
FROM debt_data
GROUP BY country_name
ORDER BY debt_rank;
""",

    # ADVANCED QUERIES
    "Advanced 1. Find the top 5 indicators contributing most to global debt.": """
SELECT indicator_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC
LIMIT 5;
""",

    "Advanced 2. Calculate percentage contribution of each country to total global debt.": """
SELECT country_name,
       SUM(debt_value) AS total_debt,
       ROUND(
           SUM(debt_value) * 100.0 / (SELECT SUM(debt_value) FROM debt_data),
           2
       ) AS percentage_contribution
FROM debt_data
GROUP BY country_name
ORDER BY percentage_contribution DESC;
""",

    "Advanced 3. Identify the top 3 countries for each indicator based on debt.": """
WITH ranked_indicator AS (
    SELECT indicator_name,
           country_name,
           SUM(debt_value) AS total_debt,
           RANK() OVER (
               PARTITION BY indicator_name
               ORDER BY SUM(debt_value) DESC
           ) AS rank_no
    FROM debt_data
    GROUP BY indicator_name, country_name
)
SELECT indicator_name,
       country_name,
       total_debt,
       rank_no
FROM ranked_indicator
WHERE rank_no <= 3
ORDER BY indicator_name, rank_no;
""",

    "Advanced 4. Find the difference between maximum and minimum debt for each country.": """
SELECT country_name,
       MAX(debt_value) AS maximum_debt,
       MIN(debt_value) AS minimum_debt,
       MAX(debt_value) - MIN(debt_value) AS debt_difference
FROM debt_data
GROUP BY country_name
ORDER BY debt_difference DESC;
""",

    "Advanced 5. Create a view for the top 10 countries with highest debt.": """
DROP VIEW IF EXISTS top_10_debt_countries;

CREATE VIEW top_10_debt_countries AS
SELECT country_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT *
FROM top_10_debt_countries;
""",

    "Advanced 6. Categorize countries into High Debt, Medium Debt, Low Debt.": """
WITH country_debt AS (
    SELECT country_name,
           SUM(debt_value) AS total_debt
    FROM debt_data
    GROUP BY country_name
)
SELECT country_name,
       total_debt,
       CASE
           WHEN total_debt >= 10000000000000 THEN 'High Debt'
           WHEN total_debt >= 1000000000000 THEN 'Medium Debt'
           ELSE 'Low Debt'
       END AS debt_category
FROM country_debt
ORDER BY total_debt DESC;
""",

    "Advanced 7. Use window functions to calculate cumulative debt per country.": """
SELECT country_name,
       year,
       yearly_debt,
       SUM(yearly_debt) OVER (
           PARTITION BY country_name
           ORDER BY year
       ) AS cumulative_debt
FROM (
    SELECT country_name,
           year,
           SUM(debt_value) AS yearly_debt
    FROM debt_data
    GROUP BY country_name, year
)
ORDER BY country_name, year;
""",

    "Advanced 8. Find indicators where average debt is higher than overall average debt.": """
SELECT indicator_name,
       AVG(debt_value) AS average_debt
FROM debt_data
GROUP BY indicator_name
HAVING AVG(debt_value) > (
    SELECT AVG(debt_value)
    FROM debt_data
)
ORDER BY average_debt DESC;
""",

    "Advanced 9. Identify countries contributing more than 5% of global debt.": """
SELECT country_name,
       SUM(debt_value) AS total_debt,
       ROUND(
           SUM(debt_value) * 100.0 / (SELECT SUM(debt_value) FROM debt_data),
           2
       ) AS contribution_percentage
FROM debt_data
GROUP BY country_name
HAVING contribution_percentage > 5
ORDER BY contribution_percentage DESC;
""",

    "Advanced 10. Find the most dominant indicator for each country.": """
WITH dominant_indicator AS (
    SELECT country_name,
           indicator_name,
           SUM(debt_value) AS total_debt,
           RANK() OVER (
               PARTITION BY country_name
               ORDER BY SUM(debt_value) DESC
           ) AS rank_no
    FROM debt_data
    GROUP BY country_name, indicator_name
)
SELECT country_name,
       indicator_name,
       total_debt
FROM dominant_indicator
WHERE rank_no = 1
ORDER BY total_debt DESC;
"""
}

selected_question = st.selectbox(
    "Select an SQL Analytical Question",
    list(sql_questions.keys())
)

selected_sql = sql_questions[selected_question]

st.write("### SQL Query")
st.code(selected_sql, language="sql")

if st.button("Run Selected Query"):
    try:
        conn = sqlite3.connect(DB_PATH)

        if "CREATE VIEW" in selected_sql or "DROP VIEW" in selected_sql:
            cursor = conn.cursor()
            cursor.executescript(selected_sql)
            result = pd.read_sql("SELECT * FROM top_10_debt_countries;", conn)
        else:
            result = pd.read_sql(selected_sql, conn)

        conn.close()

        st.write("### Query Result")
        st.dataframe(result)

    except Exception as e:
        st.error(f"Query Error: {e}")

st.divider()


# ================= COUNTRY TREND =================
st.subheader("🔍 Country-wise Debt Trend")

countries = run_query("""
SELECT DISTINCT country_name
FROM debt_data
ORDER BY country_name;
""")

selected_country = st.selectbox(
    "Choose Country for Trend Analysis",
    countries["country_name"].tolist()
)

safe_country = selected_country.replace("'", "''")

country_data = run_query(f"""
SELECT year,
       SUM(debt_value) AS total_debt
FROM debt_data
WHERE country_name = '{safe_country}'
GROUP BY year
ORDER BY year;
""")

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(country_data["year"], country_data["total_debt"], marker="o")
ax2.set_title(f"Debt Trend for {selected_country}")
ax2.set_xlabel("Year")
ax2.set_ylabel("Total Debt")
ax2.grid(True)
st.pyplot(fig2)

st.success("✅ Dashboard Loaded Successfully!")