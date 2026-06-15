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


def safe_num(value):
    if value is None:
        return 0
    return value


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
        COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data;
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📌 Total Records", f"{safe_num(summary['total_records'][0]):,}")
    col2.metric("🌍 Total Countries", safe_num(summary["total_countries"][0]))
    col3.metric("📊 Total Indicators", safe_num(summary["total_indicators"][0]))
    col4.metric("📅 Year Range", f"{summary['min_year'][0]} - {summary['max_year'][0]}")

    st.metric("💰 Total Global Debt", f"{safe_num(summary['total_debt'][0]):,.0f}")

    st.subheader("📌 Sample Data")

    sample_data = run_query("""
    SELECT *
    FROM debt_data
    LIMIT 20;
    """)

    st.dataframe(sample_data, use_container_width=True)


# ================= ADVANCED VISUAL ANALYSIS =================

elif menu == "📊 Visual Analysis":

    st.header("📊 Advanced Visual Analysis")

    st.subheader("🔎 Dashboard Filters")

    years = run_query("""
    SELECT DISTINCT year
    FROM debt_data
    WHERE year IS NOT NULL
    ORDER BY year;
    """)

    countries = run_query("""
    SELECT DISTINCT country_name
    FROM debt_data
    WHERE country_name IS NOT NULL
    ORDER BY country_name;
    """)

    indicators = run_query("""
    SELECT DISTINCT indicator_name
    FROM debt_data
    WHERE indicator_name IS NOT NULL
    ORDER BY indicator_name;
    """)

    if years.empty or countries.empty or indicators.empty:
        st.error("Database-la data illa. First db_insert.py run panni data insert pannunga.")
        st.stop()

    min_year = int(years["year"].min())
    max_year = int(years["year"].max())

    col1, col2, col3 = st.columns(3)

    with col1:
        year_range = st.slider(
            "📅 Select Year Range",
            min_year,
            max_year,
            (min_year, max_year)
        )

    with col2:
        selected_country = st.selectbox(
            "🌍 Select Country",
            ["All"] + countries["country_name"].tolist()
        )

    with col3:
        selected_indicator = st.selectbox(
            "📌 Select Indicator",
            ["All"] + indicators["indicator_name"].tolist()
        )

    conditions = [
        f"year BETWEEN {year_range[0]} AND {year_range[1]}"
    ]

    if selected_country != "All":
        safe_country = selected_country.replace("'", "''")
        conditions.append(f"country_name = '{safe_country}'")

    if selected_indicator != "All":
        safe_indicator = selected_indicator.replace("'", "''")
        conditions.append(f"indicator_name = '{safe_indicator}'")

    where_clause = "WHERE " + " AND ".join(conditions)

    st.info(f"Applied Filter: {where_clause}")

    # KPI Cards
    kpi = run_query(f"""
    SELECT 
        COUNT(*) AS total_records,
        COUNT(DISTINCT country_name) AS total_countries,
        COUNT(DISTINCT indicator_name) AS total_indicators,
        COALESCE(SUM(debt_value), 0) AS total_debt,
        COALESCE(AVG(debt_value), 0) AS average_debt
    FROM debt_data
    {where_clause};
    """)

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("📌 Records", f"{safe_num(kpi['total_records'][0]):,}")
    k2.metric("🌍 Countries", safe_num(kpi["total_countries"][0]))
    k3.metric("📊 Indicators", safe_num(kpi["total_indicators"][0]))
    k4.metric("💰 Total Debt", f"{safe_num(kpi['total_debt'][0]):,.0f}")

    st.divider()

    # 1. Year-wise Trend
    st.subheader("📈 Year-wise Debt Trend")

    year_data = run_query(f"""
    SELECT year,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY year
    ORDER BY year;
    """)

    if not year_data.empty:
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        ax1.plot(year_data["year"], year_data["total_debt"], marker="o")
        ax1.set_title("Debt Trend Over Years")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Total Debt")
        ax1.grid(True)
        st.pyplot(fig1)
    else:
        st.warning("No data available for selected filter.")

    # 2. Top 10 Countries - Horizontal Bar
    st.subheader("🏆 Top 10 Countries by Debt")

    top_countries = run_query(f"""
    SELECT country_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY country_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """)

    st.dataframe(top_countries, use_container_width=True)

    if not top_countries.empty:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.barh(top_countries["country_name"], top_countries["total_debt"])
        ax2.set_title("Top 10 Countries by Total Debt")
        ax2.set_xlabel("Total Debt")
        ax2.set_ylabel("Country")
        ax2.invert_yaxis()
        st.pyplot(fig2)

    # 3. Top 10 Indicators - Horizontal Bar
    st.subheader("📌 Top 10 Debt Indicators")

    top_indicators = run_query(f"""
    SELECT indicator_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    {where_clause}
    GROUP BY indicator_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """)

    st.dataframe(top_indicators, use_container_width=True)

    if not top_indicators.empty:
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        ax3.barh(top_indicators["indicator_name"], top_indicators["total_debt"])
        ax3.set_title("Top 10 Indicators by Debt")
        ax3.set_xlabel("Total Debt")
        ax3.set_ylabel("Indicator")
        ax3.invert_yaxis()
        st.pyplot(fig3)

    # 4. Pie Chart
    st.subheader("🥧 Debt Share of Top 5 Countries")

    top5 = top_countries.head(5)

    if not top5.empty:
        fig4, ax4 = plt.subplots(figsize=(8, 8))
        ax4.pie(
            top5["total_debt"],
            labels=top5["country_name"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax4.set_title("Top 5 Countries Debt Share")
        st.pyplot(fig4)

    # 5. Scatter Plot
    st.subheader("🔵 Debt Distribution Over Years")

    scatter_data = run_query(f"""
    SELECT year,
           debt_value
    FROM debt_data
    {where_clause}
    LIMIT 5000;
    """)

    if not scatter_data.empty:
        fig5, ax5 = plt.subplots(figsize=(12, 5))
        ax5.scatter(
            scatter_data["year"],
            scatter_data["debt_value"],
            alpha=0.5
        )
        ax5.set_title("Debt Value Distribution Over Years")
        ax5.set_xlabel("Year")
        ax5.set_ylabel("Debt Value")
        ax5.grid(True)
        st.pyplot(fig5)

    # 6. Top 5 Countries Trend Comparison
    st.subheader("📊 Top 5 Countries Trend Comparison")

    trend_data = run_query(f"""
    SELECT year,
           country_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    WHERE country_name IN (
        SELECT country_name
        FROM debt_data
        {where_clause}
        GROUP BY country_name
        ORDER BY SUM(debt_value) DESC
        LIMIT 5
    )
    AND year BETWEEN {year_range[0]} AND {year_range[1]}
    GROUP BY year, country_name
    ORDER BY year;
    """)

    if not trend_data.empty:
        fig6, ax6 = plt.subplots(figsize=(12, 6))

        for country in trend_data["country_name"].unique():
            temp = trend_data[trend_data["country_name"] == country]
            ax6.plot(temp["year"], temp["total_debt"], marker="o", label=country)

        ax6.set_title("Top 5 Countries Debt Trend Comparison")
        ax6.set_xlabel("Year")
        ax6.set_ylabel("Total Debt")
        ax6.legend()
        ax6.grid(True)
        st.pyplot(fig6)

    # 7. Heatmap Style Table
    st.subheader("🔥 Year vs Top Countries Debt Heatmap")

    heatmap_data = run_query(f"""
    SELECT year,
           country_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    WHERE country_name IN (
        SELECT country_name
        FROM debt_data
        {where_clause}
        GROUP BY country_name
        ORDER BY SUM(debt_value) DESC
        LIMIT 10
    )
    AND year BETWEEN {year_range[0]} AND {year_range[1]}
    GROUP BY year, country_name;
    """)

    if not heatmap_data.empty:
        pivot_df = heatmap_data.pivot(
            index="country_name",
            columns="year",
            values="total_debt"
        ).fillna(0)

        st.dataframe(
            pivot_df.style.background_gradient(cmap="Blues"),
            use_container_width=True
        )

    # 8. Filtered Preview
    st.subheader("📋 Filtered Data Preview")

    sample = run_query(f"""
    SELECT *
    FROM debt_data
    {where_clause}
    LIMIT 100;
    """)

    st.dataframe(sample, use_container_width=True)


# ================= SQL QUESTIONS =================

elif menu == "🧾 SQL Questions":

    st.header("🧾 SQL Analytical Questions")

    sql_questions = {
        "Basic 1. Retrieve all distinct country names": """
SELECT DISTINCT country_name
FROM debt_data
ORDER BY country_name;
""",

        "Basic 2. Count total countries": """
SELECT COUNT(DISTINCT country_name) AS total_countries
FROM debt_data;
""",

        "Basic 3. Count total indicators": """
SELECT COUNT(DISTINCT indicator_name) AS total_indicators
FROM debt_data;
""",

        "Basic 4. Display first 10 records": """
SELECT *
FROM debt_data
LIMIT 10;
""",

        "Basic 5. Calculate total global debt": """
SELECT COALESCE(SUM(debt_value), 0) AS total_global_debt
FROM debt_data;
""",

        "Basic 6. List unique indicator names": """
SELECT DISTINCT indicator_name
FROM debt_data
ORDER BY indicator_name;
""",

        "Basic 7. Number of records for each country": """
SELECT country_name,
       COUNT(*) AS record_count
FROM debt_data
GROUP BY country_name
ORDER BY record_count DESC;
""",

        "Basic 8. Records where debt is greater than 1 billion USD": """
SELECT *
FROM debt_data
WHERE debt_value > 1000000000
LIMIT 100;
""",

        "Basic 9. Minimum, maximum, and average debt values": """
SELECT 
    MIN(debt_value) AS minimum_debt,
    MAX(debt_value) AS maximum_debt,
    AVG(debt_value) AS average_debt
FROM debt_data;
""",

        "Basic 10. Count total records": """
SELECT COUNT(*) AS total_records
FROM debt_data;
""",

        "Intermediate 1. Total debt for each country": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC;
""",

        "Intermediate 2. Top 10 countries with highest total debt": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;
""",

        "Intermediate 3. Average debt per country": """
SELECT country_name,
       AVG(debt_value) AS average_debt
FROM debt_data
GROUP BY country_name
ORDER BY average_debt DESC;
""",

        "Intermediate 4. Total debt for each indicator": """
SELECT indicator_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC;
""",

        "Intermediate 5. Highest debt contributing indicator": """
SELECT indicator_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC
LIMIT 1;
""",

        "Intermediate 6. Country with lowest total debt": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt ASC
LIMIT 1;
""",

        "Intermediate 7. Total debt for each country and indicator": """
SELECT country_name,
       indicator_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY country_name, indicator_name
ORDER BY total_debt DESC
LIMIT 100;
""",

        "Intermediate 8. Indicator count for each country": """
SELECT country_name,
       COUNT(DISTINCT indicator_name) AS indicator_count
FROM debt_data
GROUP BY country_name
ORDER BY indicator_count DESC;
""",

        "Intermediate 9. Countries above global average debt": """
WITH country_debt AS (
    SELECT country_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
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

        "Intermediate 10. Rank countries by total debt": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt,
       RANK() OVER (ORDER BY SUM(debt_value) DESC) AS debt_rank
FROM debt_data
GROUP BY country_name
ORDER BY debt_rank;
""",

        "Advanced 1. Top 5 indicators contributing most to global debt": """
SELECT indicator_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC
LIMIT 5;
""",

        "Advanced 2. Percentage contribution of each country": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt,
       ROUND(
           COALESCE(SUM(debt_value), 0) * 100.0 /
           (SELECT COALESCE(SUM(debt_value), 1) FROM debt_data),
           2
       ) AS percentage_contribution
FROM debt_data
GROUP BY country_name
ORDER BY percentage_contribution DESC;
""",

        "Advanced 3. Top 3 countries for each indicator": """
WITH ranked_indicator AS (
    SELECT indicator_name,
           country_name,
           COALESCE(SUM(debt_value), 0) AS total_debt,
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

        "Advanced 4. Difference between maximum and minimum debt": """
SELECT country_name,
       MAX(debt_value) AS maximum_debt,
       MIN(debt_value) AS minimum_debt,
       MAX(debt_value) - MIN(debt_value) AS debt_difference
FROM debt_data
GROUP BY country_name
ORDER BY debt_difference DESC;
""",

        "Advanced 5. Top 10 countries view result": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;
""",

        "Advanced 6. Categorize countries into High, Medium, Low Debt": """
WITH country_debt AS (
    SELECT country_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
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

        "Advanced 7. Cumulative debt per country": """
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
           COALESCE(SUM(debt_value), 0) AS yearly_debt
    FROM debt_data
    GROUP BY country_name, year
)
ORDER BY country_name, year;
""",

        "Advanced 8. Indicators above overall average debt": """
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

        "Advanced 9. Countries contributing more than 5% global debt": """
SELECT country_name,
       COALESCE(SUM(debt_value), 0) AS total_debt,
       ROUND(
           COALESCE(SUM(debt_value), 0) * 100.0 /
           (SELECT COALESCE(SUM(debt_value), 1) FROM debt_data),
           2
       ) AS contribution_percentage
FROM debt_data
GROUP BY country_name
HAVING contribution_percentage > 5
ORDER BY contribution_percentage DESC;
""",

        "Advanced 10. Most dominant indicator for each country": """
WITH dominant_indicator AS (
    SELECT country_name,
           indicator_name,
           COALESCE(SUM(debt_value), 0) AS total_debt,
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
            result = run_query(selected_sql)
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
    WHERE country_name IS NOT NULL
    ORDER BY country_name;
    """)

    selected_country = st.selectbox(
        "Choose Country",
        countries["country_name"].tolist()
    )

    safe_country = selected_country.replace("'", "''")

    country_data = run_query(f"""
    SELECT year,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    WHERE country_name = '{safe_country}'
    GROUP BY year
    ORDER BY year;
    """)

    st.dataframe(country_data, use_container_width=True)

    if not country_data.empty:
        fig7, ax7 = plt.subplots(figsize=(12, 5))
        ax7.plot(country_data["year"], country_data["total_debt"], marker="o")
        ax7.set_title(f"Debt Trend for {selected_country}")
        ax7.set_xlabel("Year")
        ax7.set_ylabel("Total Debt")
        ax7.grid(True)
        st.pyplot(fig7)

    st.subheader("🏆 Top Indicators in Selected Country")

    country_indicators = run_query(f"""
    SELECT indicator_name,
           COALESCE(SUM(debt_value), 0) AS total_debt
    FROM debt_data
    WHERE country_name = '{safe_country}'
    GROUP BY indicator_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """)

    st.dataframe(country_indicators, use_container_width=True)

    if not country_indicators.empty:
        fig8, ax8 = plt.subplots(figsize=(12, 6))
        ax8.barh(country_indicators["indicator_name"], country_indicators["total_debt"])
        ax8.set_title(f"Top Indicators in {selected_country}")
        ax8.set_xlabel("Total Debt")
        ax8.set_ylabel("Indicator")
        ax8.invert_yaxis()
        st.pyplot(fig8)

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