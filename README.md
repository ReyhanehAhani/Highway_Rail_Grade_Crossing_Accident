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
