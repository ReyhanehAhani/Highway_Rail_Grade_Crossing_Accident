# Highway–rail crossings — mixed analyst + modeling case study

## Analyst layer

- **SQL:** `analytics/sql/kpis.sql` executed via `analytics/run_sql_kpis.py` (DuckDB on published CSVs).  
- **Quality:** `analytics/quality/validate_published.py` guards schemas and label ranges.  
- **Demo data:** `analytics_stack/published/` is **synthetic** for a self-contained repo; swap in FRA-aligned exports from your notebook for real narratives.

## Modeling layer

- **Task:** Multiclass `Severity_Bucket` with classes 0, 1, and 2 from `State`, `Year`, `Warning_Device`.
- **Baselines:** `DummyClassifier` (stratified) vs `LogisticRegression` vs `RandomForestClassifier`.  
- **Evaluation:** Accuracy, macro-F1, confusion matrix, per-class recall (see `modeling/artifacts/`).  
- **Error analysis:** Misclassified rows exported for review.  
- **Interpretability:** `permutation_importance` (always) plus optional SHAP on the forest when `CI` is not set.

Run locally:

```bash
pip install -r requirements-analytics-stack.txt
python modeling/train_eval_explain.py
python analytics/run_sql_kpis.py
```
