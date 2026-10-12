import pandas as pd
import joblib
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    precision_recall_curve
)


# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_file = Path("data/processed/diabetes_model_ready.csv")
model_file = Path("models/diabetes_risk_model.joblib")

evaluation_folder = Path("outputs/model_evaluation")
evaluation_folder.mkdir(parents=True, exist_ok=True)

report_file = evaluation_folder / "model_evaluation_report.xlsx"

confusion_matrix_file = evaluation_folder / "confusion_matrix.png"
roc_curve_file = evaluation_folder / "roc_curve.png"
precision_recall_file = evaluation_folder / "precision_recall_curve.png"
model_comparison_file = evaluation_folder / "model_comparison.png"


# --------------------------------------------------
# 2. Load dataset and saved model
# --------------------------------------------------

df = pd.read_csv(input_file)

saved_model = joblib.load(model_file)

model = saved_model["model"]
feature_columns = saved_model["features"]
target_column = saved_model["target"]
best_model_name = saved_model["best_model_name"]


# --------------------------------------------------
# 3. Prepare features and target
# --------------------------------------------------

X = df[feature_columns]
y = df[target_column]


# --------------------------------------------------
# 4. Recreate the same train-test split
# --------------------------------------------------

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

X_test = X.iloc[test_index]
y_test = y.iloc[test_index]


# --------------------------------------------------
# 5. Generate predictions
# --------------------------------------------------

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]


# --------------------------------------------------
# 6. Calculate evaluation metrics
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions
)

recall = recall_score(
    y_test,
    predictions
)

f1 = f1_score(
    y_test,
    predictions
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)


# --------------------------------------------------
# 7. Confusion Matrix
# --------------------------------------------------

cm = confusion_matrix(
    y_test,
    predictions
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Class 0", "Class 1"]
)

disp.plot()

plt.title("Diabetes Risk Model - Confusion Matrix")
plt.tight_layout()

plt.savefig(
    confusion_matrix_file,
    dpi=300
)

plt.close()


# --------------------------------------------------
# 8. ROC Curve
# --------------------------------------------------

fpr, tpr, _ = roc_curve(
    y_test,
    probabilities
)

plt.figure(figsize=(7, 5))

plt.plot(
    fpr,
    tpr,
    label=f"ROC AUC = {roc_auc:.4f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    f"ROC Curve - {best_model_name}"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    roc_curve_file,
    dpi=300
)

plt.close()


# --------------------------------------------------
# 9. Precision-Recall Curve
# --------------------------------------------------

precision_values, recall_values, _ = precision_recall_curve(
    y_test,
    probabilities
)

plt.figure(figsize=(7, 5))

plt.plot(
    recall_values,
    precision_values
)

plt.xlabel("Recall")
plt.ylabel("Precision")

plt.title(
    f"Precision-Recall Curve - {best_model_name}"
)

plt.tight_layout()

plt.savefig(
    precision_recall_file,
    dpi=300
)

plt.close()


# --------------------------------------------------
# 10. Load model comparison results
# --------------------------------------------------

training_report = Path(
    "outputs/model_training_report.xlsx"
)

comparison_df = pd.read_excel(
    training_report,
    sheet_name="Model Comparison"
)


# --------------------------------------------------
# 11. Model comparison chart
# --------------------------------------------------

plt.figure(figsize=(9, 6))

x = range(len(comparison_df))

plt.bar(
    x,
    comparison_df["ROC AUC"]
)

plt.xticks(
    x,
    comparison_df["Model"],
    rotation=15
)

plt.ylabel("ROC AUC")

plt.title("Model Comparison - ROC AUC")

plt.tight_layout()

plt.savefig(
    model_comparison_file,
    dpi=300
)

plt.close()


# --------------------------------------------------
# 12. Evaluation report
# --------------------------------------------------

metrics_df = pd.DataFrame({
    "Metric": [
        "Model",
        "Testing Records",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC AUC"
    ],
    "Value": [
        best_model_name,
        len(X_test),
        round(accuracy, 4),
        round(precision, 4),
        round(recall, 4),
        round(f1, 4),
        round(roc_auc, 4)
    ]
})


confusion_df = pd.DataFrame(
    cm,
    index=["Actual Class 0", "Actual Class 1"],
    columns=["Predicted Class 0", "Predicted Class 1"]
)


# --------------------------------------------------
# 13. Save Excel report
# --------------------------------------------------

with pd.ExcelWriter(
    report_file,
    engine="openpyxl"
) as writer:

    metrics_df.to_excel(
        writer,
        sheet_name="Evaluation Metrics",
        index=False
    )

    comparison_df.to_excel(
        writer,
        sheet_name="Model Comparison",
        index=False
    )

    confusion_df.to_excel(
        writer,
        sheet_name="Confusion Matrix"
    )


# --------------------------------------------------
# 14. Terminal status
# --------------------------------------------------

print("Model evaluation completed successfully.")
print(f"Best model evaluated: {best_model_name}")
print(f"Evaluation report: {report_file}")
print(f"Confusion matrix: {confusion_matrix_file}")
print(f"ROC curve: {roc_curve_file}")
print(f"Precision-recall curve: {precision_recall_file}")
print(f"Model comparison chart: {model_comparison_file}")