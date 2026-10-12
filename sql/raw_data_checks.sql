USE ai_diabetes_db;

-- 1. Verify raw data row count
SELECT COUNT(*) AS total_raw_rows
FROM diabetes_raw;

-- 2. Verify raw data column count
SELECT COUNT(*) AS total_raw_columns
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ai_diabetes_db'
  AND TABLE_NAME = 'diabetes_raw';

-- 3. Check diabetes target distribution
SELECT
    Diabetes_binary,
    COUNT(*) AS record_count
FROM diabetes_raw
GROUP BY Diabetes_binary
ORDER BY Diabetes_binary;

-- 4. Check missing values in raw data
SELECT
    SUM(HighBP IS NULL) AS HighBP_nulls,
    SUM(HighChol IS NULL) AS HighChol_nulls,
    SUM(CholCheck IS NULL) AS CholCheck_nulls,
    SUM(BMI IS NULL) AS BMI_nulls,
    SUM(Smoker IS NULL) AS Smoker_nulls,
    SUM(Stroke IS NULL) AS Stroke_nulls,
    SUM(HeartDiseaseorAttack IS NULL) AS HeartDiseaseorAttack_nulls,
    SUM(PhysActivity IS NULL) AS PhysActivity_nulls,
    SUM(Fruits IS NULL) AS Fruits_nulls,
    SUM(Veggies IS NULL) AS Veggies_nulls,
    SUM(HvyAlcoholConsump IS NULL) AS HvyAlcoholConsump_nulls,
    SUM(AnyHealthcare IS NULL) AS AnyHealthcare_nulls,
    SUM(NoDocbcCost IS NULL) AS NoDocbcCost_nulls,
    SUM(GenHlth IS NULL) AS GenHlth_nulls,
    SUM(MentHlth IS NULL) AS MentHlth_nulls,
    SUM(PhysHlth IS NULL) AS PhysHlth_nulls,
    SUM(DiffWalk IS NULL) AS DiffWalk_nulls,
    SUM(Sex IS NULL) AS Sex_nulls,
    SUM(Age IS NULL) AS Age_nulls,
    SUM(Education IS NULL) AS Education_nulls,
    SUM(Income IS NULL) AS Income_nulls,
    SUM(Diabetes_binary IS NULL) AS Diabetes_binary_nulls
FROM diabetes_raw;

-- 5. Display available tables
SHOW TABLES;

