import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt


# Project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Model path
MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "diabetes_risk_model.joblib"
)

# Output folder
OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "outputs"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# Load saved model package
model_package = joblib.load(MODEL_PATH)

print("Model package loaded successfully.")


# Get the trained Pipeline
pipeline = model_package["model"]

# Get feature names saved during training
feature_names = model_package["features"]

# Get the Logistic Regression model inside the Pipeline
logistic_model = pipeline.named_steps["model"]


print("Pipeline loaded successfully.")
print("Model used:", model_package["best_model_name"])
print("Number of features:", len(feature_names))


# Get Logistic Regression coefficients
coefficients = logistic_model.coef_[0]


# Create explainability table
feature_analysis = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})


# Positive coefficient = higher predicted diabetes risk
# Negative coefficient = lower predicted diabetes risk
feature_analysis["Direction"] = feature_analysis["Coefficient"].apply(
    lambda x: "Positive influence" if x > 0 else "Negative influence"
)


# Absolute coefficient shows strength of influence
feature_analysis["Absolute_Importance"] = (
    feature_analysis["Coefficient"].abs()
)


# Sort strongest features first
feature_analysis = feature_analysis.sort_values(
    "Absolute_Importance",
    ascending=False
)


# Save Excel file
excel_path = os.path.join(
    OUTPUT_DIR,
    "logistic_regression_feature_explainability.xlsx"
)

feature_analysis.to_excel(
    excel_path,
    index=False
)


# Display top 15 features
print("\nTop features influencing diabetes-risk prediction:\n")

print(
    feature_analysis[
        ["Feature", "Coefficient", "Direction"]
    ].head(15).to_string(index=False)
)


# Select top 15 features for visualization
top_features = feature_analysis.head(15).sort_values(
    "Coefficient"
)


# Create chart
plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Coefficient"]
)

plt.axvline(
    x=0,
    linewidth=1
)

plt.xlabel("Logistic Regression Coefficient")
plt.ylabel("Feature")
plt.title(
    "Top Features Influencing Diabetes Risk Prediction"
)

plt.tight_layout()


# Save chart
chart_path = os.path.join(
    OUTPUT_DIR,
    "logistic_regression_feature_explainability.png"
)

plt.savefig(
    chart_path,
    dpi=300
)

plt.close()


print("\nExplainability completed successfully.")
print("Excel output:", excel_path)
print("Chart output:", chart_path)