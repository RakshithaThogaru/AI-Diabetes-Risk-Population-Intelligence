import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_file = Path("data/processed/diabetes_model_ready.csv")

output_folder = Path("outputs")
chart_folder = output_folder / "eda_charts"

report_file = output_folder / "eda_report.xlsx"

output_folder.mkdir(parents=True, exist_ok=True)
chart_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load complete processed dataset
# --------------------------------------------------

df = pd.read_csv(input_file)

target_column = "Diabetes_binary"

feature_columns = [
    column for column in df.columns
    if column != target_column
]

# --------------------------------------------------
# 3. Overall EDA summary
# --------------------------------------------------

target_counts = df[target_column].value_counts().sort_index()

overall_summary = pd.DataFrame({
    "Metric": [
        "Rows analyzed",
        "Columns analyzed",
        "Missing values",
        "Diabetes_binary = 0 count",
        "Diabetes_binary = 1 count",
        "Diabetes_binary = 1 percentage"
    ],
    "Value": [
        len(df),
        len(df.columns),
        int(df.isnull().sum().sum()),
        int(target_counts[0]),
        int(target_counts[1]),
        round((target_counts[1] / len(df)) * 100, 2)
    ]
})

# --------------------------------------------------
# 4. Statistics for all 22 columns
# --------------------------------------------------

numerical_summary = df.describe().T.reset_index()

numerical_summary = numerical_summary.rename(
    columns={"index": "Column"}
)

# --------------------------------------------------
# 5. Diabetes_binary rate for every feature category
# --------------------------------------------------

feature_results = []

for column in feature_columns:
    grouped_data = df.groupby(column)[target_column].agg(
        Total_Records="count",
        Diabetes_Positive="sum",
        Diabetes_Rate="mean"
    ).reset_index()

    grouped_data.insert(0, "Feature", column)

    grouped_data["Diabetes_Rate"] = (
        grouped_data["Diabetes_Rate"] * 100
    ).round(2)

    feature_results.append(grouped_data)

feature_vs_diabetes = pd.concat(
    feature_results,
    ignore_index=True
)

# --------------------------------------------------
# 6. BMI comparison by target class
# --------------------------------------------------

bmi_by_target = df.groupby(target_column)["BMI"].agg(
    Count="count",
    Mean_BMI="mean",
    Median_BMI="median",
    Minimum_BMI="min",
    Maximum_BMI="max"
).reset_index()

bmi_by_target["Mean_BMI"] = bmi_by_target["Mean_BMI"].round(2)
bmi_by_target["Median_BMI"] = bmi_by_target["Median_BMI"].round(2)

# --------------------------------------------------
# 7. Create charts using complete dataset
# --------------------------------------------------

plt.figure(figsize=(7, 5))

plt.bar(
    ["Class 0", "Class 1"],
    target_counts.values,
    color=["#4C78A8", "#E45756"]
)

plt.title("Diabetes_binary Distribution")
plt.xlabel("Target Class")
plt.ylabel("Number of Participants")

plt.tight_layout()

plt.savefig(
    chart_folder / "target_distribution.png",
    dpi=300
)

plt.close()

# Age is a category code from 1 to 13
age_rate = df.groupby("Age")[target_column].mean() * 100

plt.figure(figsize=(8, 5))

plt.plot(
    age_rate.index,
    age_rate.values,
    marker="o",
    color="#E45756"
)

plt.title("Diabetes_binary = 1 Rate by Age Category")
plt.xlabel("Age Category Code")
plt.ylabel("Class 1 Rate (%)")

plt.xticks(age_rate.index)

plt.tight_layout()

plt.savefig(
    chart_folder / "risk_by_age_category.png",
    dpi=300
)

plt.close()

# Income is a category code from 1 to 8
income_rate = df.groupby("Income")[target_column].mean() * 100

plt.figure(figsize=(8, 5))

plt.bar(
    income_rate.index.astype(str),
    income_rate.values,
    color="#59A14F"
)

plt.title("Diabetes_binary = 1 Rate by Income Category")
plt.xlabel("Income Category Code")
plt.ylabel("Class 1 Rate (%)")

plt.tight_layout()

plt.savefig(
    chart_folder / "risk_by_income_category.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 8. Save EDA Excel report
# --------------------------------------------------

with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
    overall_summary.to_excel(
        writer,
        sheet_name="EDA Summary",
        index=False
    )

    numerical_summary.to_excel(
        writer,
        sheet_name="Numerical Summary",
        index=False
    )

    feature_vs_diabetes.to_excel(
        writer,
        sheet_name="Feature vs Diabetes",
        index=False
    )

    bmi_by_target.to_excel(
        writer,
        sheet_name="BMI by Target",
        index=False
    )

# --------------------------------------------------
# 9. Terminal result
# --------------------------------------------------

print("Full dataset EDA completed successfully.")
print(f"EDA report saved: {report_file}")
print(f"EDA charts saved in: {chart_folder}")