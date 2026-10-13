# AI Diabetes Risk & Population Intelligence Platform

## Project Overview
An end-to-end data analytics and machine learning project that analyzes diabetes health indicators, explores population-level risk factors, evaluates a predictive model, and presents insights through Power BI and Tableau dashboards.

## Objectives
- Analyze diabetes-related health indicators.
- Explore patterns across demographic and lifestyle factors.
- Build and evaluate a machine learning classification model.
- Store and validate raw and processed data using MySQL.
- Present analytical insights through interactive BI dashboards.

## Technology Stack
- **Programming:** Python
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, Logistic Regression
- **Database:** MySQL
- **Visualization:** Matplotlib, Power BI, Tableau
- **Tools:** MySQL Workbench, VS Code, Git, GitHub

## Dataset
The project uses the CDC Diabetes Health Indicators dataset available through the UCI Machine Learning Repository.

- Records analyzed: 253,680
- Features: 21 input features
- Target variable: `Diabetes_binary`

The raw and processed CSV datasets are kept locally and are not included in this public repository.

## Machine Learning
A Logistic Regression classification model was trained and evaluated.

| Metric | Result |
|---|---:|
| Accuracy | 73.32% |
| Precision | 31.22% |
| Recall | 76.21% |
| F1-score | 44.30% |
| ROC-AUC | 82.18% |

These results reflect the current model evaluation. The model is for educational and analytical purposes and is not intended for medical diagnosis.

## Key Project Components
- Data inspection and cleaning
- Exploratory data analysis
- Feature analysis and model explainability
- Model training and evaluation
- MySQL raw and processed data validation scripts
- Power BI and Tableau dashboard files
- Visual reports and analytical charts
 ## Dashboard Previews

### Power BI Dashboard

### Tableau Dashboard

## Repository Structure
```text
AI-Diabetes-Risk-Population-Intelligence/
├── models/
├── outputs/
│   ├── dashboards/
│   │   ├── powerbi/
│   │   └── tableau/
│   ├── eda_charts/
│   ├── feature_charts/
│   └── model_evaluation/
├── sql/
├── src/
└── .gitignore
```

## How to Use
1. Clone or download this repository.
2. Install the required Python packages used by the source scripts.
3. Obtain the dataset from its original source and place the files in the expected local data folders.
4. Configure MySQL locally and use the SQL scripts for data validation.
5. Open the Power BI and Tableau files using their respective desktop applications.

Dataset source: [UCI Machine Learning Repository — CDC Diabetes Health Indicators](https://doi.org/10.24432/C53919)

## Disclaimer
This project is for learning, data analysis, and machine learning demonstration only. It does not provide medical advice or clinical diagnosis.
