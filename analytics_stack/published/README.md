# Published artifacts

| File | What it is |
|------|------------|
| `dashboard.html` | **Interactive** demo dashboard (Plotly in the browser). |
| `severity_by_state_year.csv`, `crossing_device_mix.csv`, `crossings_grain_demo.csv` | Import into **Power BI** or **Tableau** — same views as the HTML reference. |
| `wireframe_dashboard.svg` | Vector wireframe for Figma / decks. |

**Note:** Grain data here is **synthetic** for a self-contained demo; your notebook methodology still describes the real FRA workflow.

## Regenerate

```bash
python tools/build_published_deliverables.py
```
