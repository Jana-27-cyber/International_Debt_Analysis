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


st.sidebar.title("🌍 Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "🏠 Overview",
        "📊 Visual Analysis",
        "🧾 SQL Questions",
        "🔍 Country Analysis",
        "⬇️ Download"
    ]
)


# ================= OVERVIEW =================

if menu == "🏠 Overview":

    st.header("📊 Dataset Overview")

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

    st.subheader("📌 Sample Data")

    sample_data = run_query("""
    SELECT *
    FROM debt_data
    LIMIT 20;
    """)

    st.dataframe(sample_data, use_container_width=True)


# ================= VISUAL ANALYSIS =================

elif menu == "📊 Visual Analysis":

    st.header("📈 Visual Analysis")

    st.subheader("🔎 Filters")

    regions = run_query("SELECT DISTINCT region FROM debt_data ORDER BY region;")
    years = run_query("SELECT DISTINCT year FROM debt_data ORDER BY year;")
    income_groups = run_query("SELECT DISTINCT income_group FROM debt_data ORDER BY income_group;")
    countries = run_query("SELECT DISTINCT country_name FROM debt_data ORDER BY country_name;")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_region = st.selectbox(
            "🌍 Select Region",
            ["All"] + regions["region"].dropna().tolist()
        )

    with col2:
        selected_year = st.selectbox(
            "📅 Select Year",
            ["All"] + years["year"].tolist()
        )

    with col3:
        selected_income = st.selectbox(
            "💼 Select Income Group",
            ["All"] + income_groups["income_group"].dropna().tolist()
        )

    with col4:
        selected_country = st.selectbox(
            "🏳️ Select Country",
            ["All"] + countries["country_name"].dropna().tolist()
        )

    conditions = []

    if selected_region != "All":
        safe_region = selected_region.replace("'", "''")
        conditions.append(f"region = '{safe_region}'")

    if selected_year != "All":
        conditions.append(f"year = {selected_year}")

    if selected_income != "All":
        safe_income = selected_income.replace("'", "''")
        conditions.append(f"income_group = '{safe_income}'")

    if selected_country != "All":
        safe_country = selected_country.replace("'", "''")
        conditions.append(f"country_name = '{safe_country}'")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    st.info(f"Applied Filter: {where_clause if where_clause else 'No Filter Applied'}")

    st.subheader("📌 Filtered Data Preview")

    filtered_sample = run_query(f"""
    SELECT *
    FROM debt_data
    {where_clause}
    LIMIT 100;
    """)

    st.dataframe(filtered_sample, use_container_width=True)

    st.divider()

    st.subheader("📈 Year-wise Total Debt Trend")

    year_data = run_query(f"""
    SELECT year,
           SUM(debt_value) AS total_debt
    FROM debt_data
    {where_clause}
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

    st.subheader("🌍 Top 10 Countries by Total Debt")

    top_countries = run_query(f"""
    SELECT country_name,
           SUM(debt_value) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY country_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """)

    st.dataframe(top_countries, use_container_width=True)

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.bar(top_countries["country_name"], top_countries["total_debt"])
    ax2.set_title("Top 10 Countries by Total Debt")
    ax2.set_xlabel("Country")
    ax2.set_ylabel("Total Debt")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)

    st.subheader("🗺️ Region-wise Debt Distribution")

    region_data = run_query(f"""
    SELECT region,
           SUM(debt_value) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY region
    ORDER BY total_debt DESC;
    """)

    st.dataframe(region_data, use_container_width=True)

    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.bar(region_data["region"], region_data["total_debt"])
    ax3.set_title("Region-wise Total Debt")
    ax3.set_xlabel("Region")
    ax3.set_ylabel("Total Debt")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig3)

    st.subheader("💼 Income Group-wise Debt Analysis")

    income_data = run_query(f"""
    SELECT income_group,
           SUM(debt_value) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY income_group
    ORDER BY total_debt DESC;
    """)

    st.dataframe(income_data, use_container_width=True)

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.bar(income_data["income_group"], income_data["total_debt"])
    ax4.set_title("Income Group-wise Total Debt")
    ax4.set_xlabel("Income Group")
    ax4.set_ylabel("Total Debt")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig4)

    st.subheader("📊 Top 10 Debt Indicators")

    top_indicators = run_query(f"""
    SELECT indicator_name,
           SUM(debt_value) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY indicator_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """)

    st.dataframe(top_indicators, use_container_width=True)

    fig5, ax5 = plt.subplots(figsize=(12, 5))
    ax5.bar(top_indicators["indicator_name"], top_indicators["total_debt"])
    ax5.set_title("Top 10 Debt Indicators")
    ax5.set_xlabel("Indicator")
    ax5.set_ylabel("Total Debt")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig5)


# ================= SQL QUESTIONS =================

elif menu == "🧾 SQL Questions":

    st.header("🧾 SQL Analytical Questions")

    sql_questions = {
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

        "Intermediate 10. Rank countries based on total debt.": """
SELECT country_name,
       SUM(debt_value) AS total_debt,
       RANK() OVER (ORDER BY SUM(debt_value) DESC) AS debt_rank
FROM debt_data
GROUP BY country_name
ORDER BY debt_rank;
""",

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
            st.dataframe(result, use_container_width=True)

        except Exception as e:
            st.error(f"Query Error: {e}")


# ================= COUNTRY ANALYSIS =================

elif menu == "🔍 Country Analysis":

    st.header("🔍 Country-wise Debt Analysis")

    countries = run_query("""
    SELECT DISTINCT country_name
    FROM debt_data
    ORDER BY country_name;
    """)

    selected_country = st.selectbox(
        "Choose Country",
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

    st.dataframe(country_data, use_container_width=True)

    fig6, ax6 = plt.subplots(figsize=(12, 5))
    ax6.plot(country_data["year"], country_data["total_debt"], marker="o")
    ax6.set_title(f"Debt Trend for {selected_country}")
    ax6.set_xlabel("Year")
    ax6.set_ylabel("Total Debt")
    ax6.grid(True)
    st.pyplot(fig6)

    st.subheader("Sample Records")

    records = run_query(f"""
    SELECT *
    FROM debt_data
    WHERE country_name = '{safe_country}'
    LIMIT 100;
    """)

    st.dataframe(records, use_container_width=True)


# ================= DOWNLOAD =================

elif menu == "⬇️ Download":

    st.header("⬇️ Download Data")

    st.write("For performance, dashboard downloads sample data only.")

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

st.success("✅ Dashboard Loaded Successfully!")