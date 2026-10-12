import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

raw_file = Path("data/raw/diabetes_raw.csv")

processed_folder = Path("data/processed")
output_folder = Path("outputs")

processed_file = processed_folder / "diabetes_model_ready.csv"
report_file = output_folder / "cleaning_report.xlsx"

processed_folder.mkdir(parents=True, exist_ok=True)
output_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load original raw dataset
# --------------------------------------------------

df = pd.read_csv(raw_file)

original_rows = len(df)

# --------------------------------------------------
# 3. Validate full dataset
# --------------------------------------------------

binary_columns = [
    "HighBP", "HighChol", "CholCheck", "Smoker", "Stroke",
    "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
    "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost",
    "DiffWalk", "Sex", "Diabetes_binary"
]

range_rules = {
    "GenHlth": (1, 5),
    "MentHlth": (0, 30),
    "PhysHlth": (0, 30),
    "Age": (1, 13),
    "Education": (1, 6),
    "Income": (1, 8)
}

validation_rows = []

for column in binary_columns:
    invalid_count = (~df[column].isin([0, 1])).sum()

    validation_rows.append({
        "Column": column,
        "Rule": "Allowed values: 0 or 1",
        "Invalid Values": int(invalid_count)
    })

for column, (minimum, maximum) in range_rules.items():
    invalid_count = (~df[column].between(minimum, maximum)).sum()

    validation_rows.append({
        "Column": column,
        "Rule": f"Allowed range: {minimum} to {maximum}",
        "Invalid Values": int(invalid_count)
    })

validation_report = pd.DataFrame(validation_rows)

# --------------------------------------------------
# 4. Duplicate analysis only — do not delete rows
# --------------------------------------------------

feature_columns = [
    column for column in df.columns
    if column != "Diabetes_binary"
]

exact_duplicate_rows = int(df.duplicated().sum())

duplicate_feature_rows = int(
    df.duplicated(subset=feature_columns).sum()
)

conflicting_patterns = int(
    (df.groupby(feature_columns)["Diabetes_binary"].nunique() > 1).sum()
)

# --------------------------------------------------
# 5. Save validated processed copy
# --------------------------------------------------

# No rows are removed.
# Raw file remains unchanged.
df.to_csv(processed_file, index=False)

# --------------------------------------------------
# 6. Create cleaning report
# --------------------------------------------------

cleaning_summary = pd.DataFrame({
    "Metric": [
        "Rows in raw dataset",
        "Rows removed",
        "Rows in processed dataset",
        "Missing values",
        "Exact duplicate rows retained",
        "Duplicate feature rows retained",
        "Feature patterns with conflicting targets",
        "Cleaning decision"
    ],
    "Value": [
        original_rows,
        0,
        len(df),
        int(df.isnull().sum().sum()),
        exact_duplicate_rows,
        duplicate_feature_rows,
        conflicting_patterns,
        "No rows removed. Original participant records retained."
    ]
})

with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
    cleaning_summary.to_excel(
        writer,
        sheet_name="Cleaning Summary",
        index=False
    )

    validation_report.to_excel(
        writer,
        sheet_name="Validation Checks",
        index=False
    )

# --------------------------------------------------
# 7. Terminal status
# --------------------------------------------------

print("Full dataset cleaning and validation completed.")
print(f"Processed dataset saved: {processed_file}")
print(f"Cleaning report saved: {report_file}")