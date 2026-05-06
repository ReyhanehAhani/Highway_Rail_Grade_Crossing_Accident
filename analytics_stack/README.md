# Pillar 1 — Analytics storytelling (Tableau · Power BI · Figma)

Notebook: `Highway_Rail_Grade_Crossing_Accident_Data.ipynb` → CSV exports → BI.

| Layer | Role |
|--------|------|
| **Notebook** | Cleaning, encoding, EDA (state/time/weather/device/severity). |
| **Exports** | Aggregates safe to share (counts, rates)—no PII. |
| **Figma** | Incident-command style layout: map + severity + filters (`figma/`). |
| **Tableau / Power BI** | Operational dashboards for trends (`tableau/`, `powerbi/`). |

## Suggested exports (adapt column names to your cleaned frame)

1. `exports/crossings_grain.csv` — modeling-grain rows after preprocessing (as in notebook).
2. `exports/severity_by_state_year.csv` — `State`, `Year`, `Incident_Count`, optional severity rate columns.
3. `exports/crossing_device_mix.csv` — crossing protection / device category vs incident share.

After cleaning in pandas, run:

```bash
pip install -r analytics_stack/requirements-analytics.txt
python scripts/export_for_bi.py path/to/crossings_clean.csv analytics_stack/exports
```

Edit `COLMAP` at the top of `scripts/export_for_bi.py` if your CSV headers differ.

## Resume

- *Translated FRA-style accident analytics into **Figma**-specced **Tableau / Power BI** views aligned with the published notebook.*
