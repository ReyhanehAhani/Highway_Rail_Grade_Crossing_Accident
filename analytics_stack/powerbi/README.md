# Power BI — Highway rail grade crossings

1. **Get data** from `exports/severity_by_state_year.csv` and related aggregates.
2. **Model:** mark `Year` as whole number, `State` as text; add a date table only if you build true time intelligence.

## Measures (patterns)

```dax
Incidents = SUM('severity_by_state_year'[Incident_Count])
YoY Incidents =
    VAR y = MAX('severity_by_state_year'[Year])
    RETURN
        CALCULATE([Incidents], 'severity_by_state_year'[Year] = y)
            - CALCULATE([Incidents], 'severity_by_state_year'[Year] = y - 1)
```

Rename table to match your import.

## Pages

1. Executive: map or top states + trend + slicers.
2. Factors: device / condition breakdowns.
