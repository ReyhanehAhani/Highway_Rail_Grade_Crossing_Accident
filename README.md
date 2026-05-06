# Highway Rail Grade Crossing Accident Analysis

This project analyzes accident risks at highway-rail grade crossings in the United States, using publicly available datasets and machine learning techniques to model and predict accident severity.

---

## Dataset

- **Source**: [FRA (Federal Railroad Administration)](https://railroads.dot.gov/)
- **Contents**: Accident records with over 50 features including:
  - Environmental factors (weather, light, road condition)
  - Vehicle and train attributes
  - Crossing protection type
  - Temporal features (hour, day, month)
  - Casualties, damage, and other consequences

---

## Objective

The main goal is to predict the **severity of accidents** (e.g., fatalities, injuries, or major damage) based on available features, and explore which factors contribute most to dangerous incidents.

---

## Preprocessing

- Removed irrelevant or redundant columns
- Converted categorical data to numerical form (e.g., OneHotEncoding, LabelEncoding)
- Removed outliers and handled missing values
- Engineered useful features (e.g., time of day, season, presence of warning devices)

---

## Exploratory Data Analysis

- Visualized accident frequency by state and time
- Analyzed trends over the years (seasonal vs. non-seasonal patterns)
- Examined risk factors such as **warning device types**, **road surface conditions**, and **driver actions**

---

## Modeling

- Applied various classification and regression models:
  - Random Forest
  - XGBoost
  - Logistic Regression
  - Support Vector Machines (SVM)
- Evaluated models using:
  - Accuracy, Precision, Recall
  - Confusion matrix
  - ROC-AUC curves

---

## Files

- `Highway_Rail_Grade_Crossing_Accident_Data.ipynb` – Main notebook for analysis
- `high way.pdf` – Final PDF report with visualizations and conclusions

---

## Tools Used

- Python, Pandas, Scikit-learn, Matplotlib, Seaborn, Plotly
- Jupyter Notebook
- GitHub for version control and sharing
- **Tableau, Power BI, Figma** — see `analytics_stack/` (exports, Figma IA, BI recipes) and `scripts/export_for_bi.py`
- **Published demo pack** — `analytics_stack/published/dashboard.html` (interactive), SVG wireframe, CSVs for BI import (`tools/build_published_deliverables.py` to regenerate)

---

## Portfolio stack — Pillar 1 (storytelling)

- `analytics_stack/README.md` — CSV export bridge from the notebook
- `analytics_stack/figma/dashboard_wireframe.md` — dashboard information architecture
- `analytics_stack/tableau/` and `analytics_stack/powerbi/` — workbook instructions
- `scripts/export_for_bi.py` — tune `COLMAP`, emit `severity_by_state_year.csv` / device mix (`pip install -r analytics_stack/requirements-analytics.txt`)

---

## SQL + KPI + quality + modeling + report + Pages

```bash
pip install -r requirements-analytics-stack.txt
python analytics/quality/validate_published.py
python analytics/run_sql_kpis.py
python modeling/train_eval_explain.py    # baselines, metrics, confusion, errors, permutation (+ optional SHAP)
python analytics/reports/build_report.py
python tools/build_docs.py
```

Workflow: `.github/workflows/data-stack.yml` (sets `CI=1` so SHAP is skipped in automation).

---