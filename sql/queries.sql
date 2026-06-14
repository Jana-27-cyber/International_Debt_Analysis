-- Total records
SELECT COUNT(*) FROM debt_data;

-- Top 10 countries by total debt
SELECT country_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;

-- Average debt by country
SELECT country_name,
       AVG(debt_value) AS avg_debt
FROM debt_data
GROUP BY country_name
ORDER BY avg_debt DESC
LIMIT 10;

-- Top indicators
SELECT indicator_name,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY indicator_name
ORDER BY total_debt DESC
LIMIT 10;

-- Debt trend by year
SELECT year,
       SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY year
ORDER BY year;