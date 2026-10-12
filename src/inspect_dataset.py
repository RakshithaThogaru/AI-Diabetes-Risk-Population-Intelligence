import pandas as pd
from pathlib import Path
import os

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_file = Path("data/raw/diabetes_raw.csv")
output_folder = Path("outputs")
output_file = output_folder / "dataset_inspection.xlsx"

output_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load complete raw dataset
# --------------------------------------------------

df = pd.read_csv(input_file)

# --------------------------------------------------
# 3. Basic full-dataset information
# --------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Number of Rows",
        "Number of Columns",
        "Missing Values",
        "Exact Duplicate Rows",
        "Target Column"
    ],
    "Value": [
        df.shape[0],
        df.shape[1],
        df.isnull().sum().sum(),
        df.duplicated().sum(),
        "Diabetes_binary"
    ]
})

# --------------------------------------------------
# 4. Complete column information
# --------------------------------------------------

column_info = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Values": df.isnull().sum().values,
    "Unique Values": df.nunique().values
})

# --------------------------------------------------
# 5. Full-dataset header audit
# --------------------------------------------------

duplicate_headers = df.columns[df.columns.duplicated()].tolist()

header_row = [column.strip() for column in df.columns]

repeated_header_rows = df.astype(str).apply(
    lambda row: [value.strip() for value in row.tolist()] == header_row,
    axis=1
).sum()

header_audit = pd.DataFrame({
    "Check": [
        "Duplicate column headers",
        "Repeated header rows inside data",
        "Header audit result"
    ],
    "Result": [
        ", ".join(duplicate_headers) if duplicate_headers else "None",
        repeated_header_rows,
        "Passed" if not duplicate_headers and repeated_header_rows == 0
        else "Review needed"
    ]
})

# --------------------------------------------------
# 6. Target distribution using complete dataset
# --------------------------------------------------

target_counts = df["Diabetes_binary"].value_counts().sort_index()

target_distribution = pd.DataFrame({
    "Diabetes_binary": target_counts.index,
    "Count": target_counts.values,
    "Percentage": (target_counts.values / len(df) * 100).round(2)
})

# --------------------------------------------------
# 7. Save full inspection report to Excel
# --------------------------------------------------
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Full Dataset", index=False)

    summary.to_excel(writer, sheet_name="Dataset Summary", index=False)

    column_info.to_excel(
        writer,
        sheet_name="Column Information",
        index=False
    )

    header_audit.to_excel(
        writer,
        sheet_name="Header Audit",
        index=False
    )

    target_distribution.to_excel(
        writer,
        sheet_name="Target Distribution",
        index=False
    )


# --------------------------------------------------
# 8. Terminal status and open report
# --------------------------------------------------

print("Full dataset inspection completed successfully.")
print(f"Excel report created: {output_file}")

# os.startfile(output_file)