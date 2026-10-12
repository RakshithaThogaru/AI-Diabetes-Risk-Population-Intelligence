from ucimlrepo import fetch_ucirepo
import pandas as pd

# Fetch the CDC Diabetes Health Indicators dataset
cdc_diabetes = fetch_ucirepo(id=891)

# Get features and target
X = cdc_diabetes.data.features
y = cdc_diabetes.data.targets

# Combine features and target
raw_data = pd.concat([X, y], axis=1)

# Save the original dataset inside data/raw
raw_data.to_csv("data/raw/diabetes_raw.csv", index=False)

print("Dataset downloaded successfully!")
print("Rows:", raw_data.shape[0])
print("Columns:", raw_data.shape[1])
print("File saved as: data/raw/diabetes_raw.csv")