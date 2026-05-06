# Tableau — Highway rail grade crossings

1. Export `severity_by_state_year.csv` and `crossing_device_mix.csv` (see `analytics_stack/README.md`).
2. **Connect** to CSV; if multiple files, define relationships on `State` / `Year` as needed.
3. Build:
   - **Trend sheet:** `Year` vs incident count (line).
   - **State ranking:** horizontal bar sorted by count or severity rate.
   - **Device mix:** 100% stacked bar or treemap.

## Actions

- Use dashboard actions to filter by `State` and device type across sheets.
