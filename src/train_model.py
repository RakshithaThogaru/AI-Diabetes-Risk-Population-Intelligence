import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_file = Path("data/processed/diabetes_model_ready.csv")

output_folder = Path("outputs")
models_folder = Path("models")

report_file = output_folder / "model_training_report.xlsx"
model_file = models_folder / "diabetes_risk_model.joblib"

output_folder.mkdir(parents=True, exist_ok=True)
models_folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load full processed dataset
# --------------------------------------------------

df = pd.read_csv(input_file)

target_column = "Diabetes_binary"

feature_columns = [
    column for column in df.columns
    if column != target_column
]

X = df[feature_columns]
y = df[target_column]

# --------------------------------------------------
# 3. Train-test split
# --------------------------------------------------

# Keeps identical feature patterns in only train or test.
# This avoids evaluation leakage from repeated records.
groups = pd.util.hash_pandas_object(
    X,
    index=False
)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_index, test_index = next(
    splitter.split(X, y, groups=groups)
)

X_train = X.iloc[train_index]
X_test = X.iloc[test_index]

y_train = y.iloc[train_index]
y_test = y.iloc[test_index]

# --------------------------------------------------
# 4. Define ML models
# --------------------------------------------------

models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        (
            "model",
            LogisticRegression(
                class_weight="balanced",
                max_iter=2000,
                random_state=42
            )
        )
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}

# --------------------------------------------------
# 5. Train and compare models
# --------------------------------------------------

results = []
trained_models = {}

for model_name, model in models.items():
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    results.append({
        "Model": model_name,
        "Accuracy": round(
            accuracy_score(y_test, predictions), 4
        ),
        "Precision": round(
            precision_score(y_test, predictions), 4
        ),
        "Recall": round(
            recall_score(y_test, predictions), 4
        ),
        "F1 Score": round(
            f1_score(y_test, predictions), 4
        ),
        "ROC AUC": round(
            roc_auc_score(y_test, probabilities), 4
        )
    })

    trained_models[model_name] = model

results_df = pd.DataFrame(results)

# --------------------------------------------------
# 6. Select and save best model by ROC AUC
# --------------------------------------------------

best_model_name = results_df.loc[
    results_df["ROC AUC"].idxmax(),
    "Model"
]

best_model = trained_models[best_model_name]

joblib.dump(
    {
        "model": best_model,
        "features": feature_columns,
        "target": target_column,
        "best_model_name": best_model_name
    },
    model_file
)

# --------------------------------------------------
# 7. Save training report
# --------------------------------------------------

split_summary = pd.DataFrame({
    "Metric": [
        "Total records",
        "Training records",
        "Testing records",
        "Training Class 1 percentage",
        "Testing Class 1 percentage",
        "Best model"
    ],
    "Value": [
        len(df),
        len(X_train),
        len(X_test),
        round(y_train.mean() * 100, 2),
        round(y_test.mean() * 100, 2),
        best_model_name
    ]
})

with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
    split_summary.to_excel(
        writer,
        sheet_name="Train Test Split",
        index=False
    )

    results_df.to_excel(
        writer,
        sheet_name="Model Comparison",
        index=False
    )

# --------------------------------------------------
# 8. Terminal status
# --------------------------------------------------

print("ML model training completed successfully.")
print(f"Best model: {best_model_name}")
print(f"Saved model: {model_file}")
print(f"Training report: {report_file}")