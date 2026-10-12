import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_file = Path("data/processed/diabetes_model_ready.csv")

output_folder = Path("outputs")
chart_folder = output_folder / "feature_charts"

report_file = output_folder / "feature_analysis_report.xlsx"

output_folder.mkdir(parents=True, exist_ok=True)
chart_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load full processed dataset
# --------------------------------------------------

df = pd.read_csv(input_file)

target_column = "Diabetes_binary"

feature_columns = [
    column for column in df.columns
    if column != target_column
]

# --------------------------------------------------
# 3. Correlation with target
# --------------------------------------------------

correlation_values = df.corr(numeric_only=True)[target_column]

feature_ranking = correlation_values.drop(
    target_column
).reset_index()

feature_ranking.columns = [
    "Feature",
    "Correlation_with_Diabetes_binary"
]

feature_ranking["Absolute_Correlation"] = (
    feature_ranking["Correlation_with_Diabetes_binary"]
    .abs()
)

feature_ranking = feature_ranking.sort_values(
    by="Absolute_Correlation",
    ascending=False
)

feature_ranking["Rank"] = range(
    1,
    len(feature_ranking) + 1
)

feature_ranking = feature_ranking[
    [
        "Rank",
        "Feature",
        "Correlation_with_Diabetes_binary",
        "Absolute_Correlation"
    ]
]

feature_ranking[
    "Correlation_with_Diabetes_binary"
] = feature_ranking[
    "Correlation_with_Diabetes_binary"
].round(4)

feature_ranking["Absolute_Correlation"] = (
    feature_ranking["Absolute_Correlation"].round(4)
)

# --------------------------------------------------
# 4. Feature-category diabetes rate analysis
# --------------------------------------------------

feature_results = []

for column in feature_columns:
    grouped_data = df.groupby(column)[target_column].agg(
        Total_Records="count",
        Class_1_Count="sum",
        Class_1_Rate="mean"
    ).reset_index()

    grouped_data.insert(0, "Feature", column)

    grouped_data["Class_1_Rate"] = (
        grouped_data["Class_1_Rate"] * 100
    ).round(2)

    feature_results.append(grouped_data)

feature_category_analysis = pd.concat(
    feature_results,
    ignore_index=True
)

# --------------------------------------------------
# 5. BMI quartile analysis
# --------------------------------------------------

df["BMI_Quartile"] = pd.qcut(
    df["BMI"],
    q=4,
    duplicates="drop"
)

bmi_quartile_analysis = df.groupby(
    "BMI_Quartile",
    observed=False
)[target_column].agg(
    Total_Records="count",
    Class_1_Count="sum",
    Class_1_Rate="mean"
).reset_index()

bmi_quartile_analysis["BMI_Quartile"] = (
    bmi_quartile_analysis["BMI_Quartile"].astype(str)
)

bmi_quartile_analysis["Class_1_Rate"] = (
    bmi_quartile_analysis["Class_1_Rate"] * 100
).round(2)

# --------------------------------------------------
# 6. Charts
# --------------------------------------------------

chart_data = feature_ranking.sort_values(
    by="Correlation_with_Diabetes_binary"
)

colors = [
    "#E45756" if value > 0 else "#4C78A8"
    for value in chart_data[
        "Correlation_with_Diabetes_binary"
    ]
]

plt.figure(figsize=(10, 8))

plt.barh(
    chart_data["Feature"],
    chart_data["Correlation_with_Diabetes_binary"],
    color=colors
)

plt.title("Feature Correlation with Diabetes_binary")
plt.xlabel("Correlation")
plt.ylabel("Feature")

plt.tight_layout()

plt.savefig(
    chart_folder / "feature_correlation_ranking.png",
    dpi=300
)

plt.close()

plt.figure(figsize=(8, 5))

plt.bar(
    bmi_quartile_analysis["BMI_Quartile"],
    bmi_quartile_analysis["Class_1_Rate"],
    color="#E45756"
)

plt.title("Class 1 Rate by BMI Quartile")
plt.xlabel("BMI Quartile")
plt.ylabel("Diabetes_binary = 1 Rate (%)")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    chart_folder / "risk_by_bmi_quartile.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 7. Save Excel report
# --------------------------------------------------

with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
    feature_ranking.to_excel(
        writer,
        sheet_name="Feature Ranking",
        index=False
    )

    feature_category_analysis.to_excel(
        writer,
        sheet_name="Category Analysis",
        index=False
    )

    bmi_quartile_analysis.to_excel(
        writer,
        sheet_name="BMI Quartiles",
        index=False
    )

# --------------------------------------------------
# 8. Terminal status
# --------------------------------------------------

print("Full dataset feature analysis completed successfully.")
print(f"Feature report saved: {report_file}")
print(f"Feature charts saved in: {chart_folder}")