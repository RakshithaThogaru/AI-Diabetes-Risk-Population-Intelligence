USE ai_diabetes_db;

-- 1. Verify processed data row count
SELECT COUNT(*) AS processed_rows
FROM diabetes_model_ready;

-- 2. Verify processed data column count
SELECT COUNT(*) AS total_columns
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ai_diabetes_db'
  AND TABLE_NAME = 'diabetes_model_ready';

-- 3. View first 5 processed records
SELECT *
FROM diabetes_model_ready;

-- 4. Verify both tables exist
SHOW TABLES;
