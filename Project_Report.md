# 🌍 International Debt Analysis System - Project Report

## 1. Introduction

The International Debt Analysis System is a data analytics project developed using Python, SQLite, Streamlit, and SQL.

This project analyzes debt information of different countries and indicators and provides meaningful insights using SQL analytical queries and interactive dashboards.

---

## 2. Problem Statement

International debt data contains a large number of records across countries and indicators.

Analyzing this data manually is difficult because:

* Large volume of data
* Missing values
* Multiple metadata files
* Difficult to compare countries and indicators
* Hard to identify debt trends

Therefore, an automated system is required to clean, process, analyze, and visualize the data.

---

## 3. Objectives

The main objectives of this project are:

* Clean and preprocess debt datasets
* Handle missing values
* Convert data from wide format to long format
* Merge metadata files
* Store data in SQLite database
* Perform SQL analytical queries
* Build an interactive dashboard

---

## 4. Dataset Description

The project uses the following datasets:

1. IDS_ALLCountries_Data.csv
2. IDS_CountryMetaData.csv
3. IDS_SeriesMetaData.csv
4. IDS_FootNoteMetaData.csv
5. Country-Series - Metadata.csv

After cleaning and merging:

* Total Records: 1,574,525
* Total Columns: 15

---

## 5. Data Preprocessing

The following preprocessing steps were performed:

### Step 1: Null Value Analysis

* Checked null values in all year columns
* Identified missing data

### Step 2: Missing Value Handling

* Forward Fill (ffill)
* Backward Fill (bfill)

### Step 3: Data Transformation

* Converted wide format to long format using Pandas `melt()`.

### Step 4: Metadata Integration

Merged:

* Country Metadata
* Series Metadata

to create a final master dataset.

---

## 6. Database Creation

SQLite database named:

```text
international_debt.db
```

was created.

The cleaned dataset was inserted into:

```text
debt_data
```

table.

Database verification and SQL queries were performed using DBeaver.

---

## 7. SQL Analytical Questions

The dashboard supports:

### Basic Queries

* Country count
* Indicator count
* Global debt
* Unique indicators
* Record count

### Intermediate Queries

* Top 10 countries
* Average debt
* Debt by indicator
* Country ranking
* Countries above global average

### Advanced Queries

* Top 5 indicators
* Percentage contribution
* Window functions
* Debt categorization
* Dominant indicator

Total Questions Implemented:

**30 SQL Analytical Questions**

---

## 8. Dashboard Features

The Streamlit dashboard contains:

* KPI Metrics
* Dataset Overview
* Year-wise Debt Trend
* Top Countries by Debt
* Top Indicators
* SQL Questions Explorer
* Country-wise Debt Analysis
* Download Sample Dataset

---

## 9. Technologies Used

* Python
* Pandas
* SQLite
* DBeaver
* Streamlit
* Matplotlib
* Git
* GitHub

---

## 10. Conclusion

The International Debt Analysis System successfully analyzes international debt data using Python, SQL, SQLite, and Streamlit.

The project provides:

* Efficient data cleaning
* Database management
* SQL analytical insights
* Interactive visualizations
* User-friendly dashboard

This system helps users understand global debt trends effectively and interactively.

---

## Author

**Terrax Jana**

BE Biomedical Engineering
Final Year Student
