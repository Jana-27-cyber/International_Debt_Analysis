USE international_debt_db;

DROP TABLE IF EXISTS debt_data;

CREATE TABLE debt_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100),
    country_code VARCHAR(10),
    indicator_name VARCHAR(255),
    indicator_code VARCHAR(100),
    year INT,
    debt_value DOUBLE
);