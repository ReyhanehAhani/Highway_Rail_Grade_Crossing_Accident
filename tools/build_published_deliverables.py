#!/usr/bin/env python3
"""Synthetic-but-structured FRA-style aggregates + interactive HTML (no PII).

Run from repo root:
  python tools/build_published_deliverables.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(7)
STATES = [
    "TX",
    "CA",
    "IL",
    "NE",
    "FL",
    "KS",
    "IA",
    "MN",
    "MO",
    "OH",
    "GA",
    "LA",
    "AL",
    "MS",
    "WI",
    "IN",
    "AR",
    "TN",
    "OK",
    "KY",
]
YEARS = list(range(2018, 2024))
DEVICES = ["None", "Xings", "Lights", "Gates", "Other"]


def synthetic_crossings(n_grain: int = 3500) -> pd.DataFrame:
    rows = []
    for _ in range(n_grain):
        st = str(RNG.choice(STATES))
        yr = int(RNG.choice(YEARS))
        dev = str(RNG.choice(DEVICES))
        severity = int(RNG.choice([0, 0, 0, 1, 1, 2]))
        rows.append(
            {
                "State": st,
                "Year": yr,
                "Warning_Device": dev,
                "Severity_Bucket": severity,
            }
        )
    return pd.DataFrame(rows)


def write_html(path: Path, by_sy: pd.DataFrame, mix: pd.DataFrame) -> None:
    trend = by_sy.groupby("Year", as_index=False)["Incident_Count"].sum().sort_values("Year")
    payload = {
        "trend": trend.to_dict("records"),
        "top_states": by_sy.groupby("State", as_index=False)["Incident_Count"].sum().nlargest(12, "Incident_Count").to_dict("records"),
        "devices": mix.to_dict("records"),
        "kpis": {
            "incidents": int(by_sy["Incident_Count"].sum()),
            "states": int(by_sy["State"].nunique()),
            "years": int(by_sy["Year"].nunique()),
        },
    }
    blob = json.dumps(payload)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Rail-highway crossings — published dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
body {{ font-family: system-ui, sans-serif; margin:0; background:#f5f9fc; color:#1d1d1f; }}
header {{ padding:1.25rem 1.5rem; background:#fff; border-bottom:1px solid #e2e8f0; }}
h1 {{ margin:0; font-size:1.2rem; }}
.sub {{ color:#6e6e73; font-size:0.88rem; margin-top:0.35rem; }}
main {{ max-width:1150px; margin:0 auto; padding:1rem 1.25rem 2rem; }}
.kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:10px; margin-bottom:14px; }}
.kpi {{ background:#fff; border-radius:14px; padding:12px 14px; border:1px solid #e2e8f0; }}
.kpi label {{ font-size:0.68rem; text-transform:uppercase; letter-spacing:0.06em; color:#6e6e73; }}
.kpi strong {{ font-size:1.25rem; }}
.grid2 {{ display:grid; gap:12px; }}
@media(min-width:880px){{ .grid2 {{ grid-template-columns:1fr 1fr; }} }}
.panel {{ background:#fff; border-radius:14px; padding:8px; border:1px solid #e2e8f0; min-height:300px; }}
footer {{ font-size:0.8rem; color:#6e6e73; max-width:1150px; margin:0 auto; padding:0 1.25rem 2rem; }}
</style>
</head>
<body>
<header>
  <h1>Highway–rail grade crossing risk — demo dashboard</h1>
  <div class="sub">Demo aggregates only. Use <code>severity_by_state_year.csv</code> + <code>crossing_device_mix.csv</code> in Power BI / Tableau.</div>
</header>
<main>
  <div class="kpis" id="k"></div>
  <div class="grid2">
    <div class="panel" id="p1"></div>
    <div class="panel" id="p2"></div>
  </div>
  <div class="panel" id="p3" style="margin-top:12px; min-height:280px;"></div>
</main>
<footer>Synthetic illustrative data — methodology matches the Jupyter notebook narrative.</footer>
<script>
const D = {blob};
document.getElementById('k').innerHTML = `
  <div class="kpi"><label>Incident rows (grain)</label><strong>${{D.kpis.incidents.toLocaleString()}}</strong></div>
  <div class="kpi"><label>States</label><strong>${{D.kpis.states}}</strong></div>
  <div class="kpi"><label>Years covered</label><strong>${{D.kpis.years}}</strong></div>`;
Plotly.newPlot('p1', [{{
  x: D.trend.map(r => r.Year),
  y: D.trend.map(r => r.Incident_Count),
  type:'scatter', mode:'lines+markers',
  line:{{color:'#2b7fd4',width:3}}
}}], {{
  title:'Incidents by year',
  margin:{{t:36,b:40,l:48,r:16}},
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'#fbfcfe'
}}, {{responsive:true}});
Plotly.newPlot('p2', [{{
  x: D.top_states.map(r => r.Incident_Count),
  y: D.top_states.map(r => r.State),
  type:'bar', orientation:'h',
  marker:{{color:'#2b7fd4'}}
}}], {{
  title:'Top states (incident count)',
  margin:{{t:36,b:32,l:44,r:16}},
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'#fbfcfe'
}}, {{responsive:true}});
Plotly.newPlot('p3', [{{
  labels: D.devices.map(r => r.Warning_Device),
  values: D.devices.map(r => r.Incident_Count),
  type:'pie',
  hole:0.35,
  marker:{{colors:['#2b7fd4','#5a9bd5','#8fb8e0','#b9d4ec','#dceaf7']}}
}}], {{
  title:'Share by warning-device bucket',
  margin:{{t:36,b:24,l:24,r:24}},
  paper_bgcolor:'rgba(0,0,0,0)'
}}, {{responsive:true}});
</script>
</body>
</html>"""
    path.write_text(html, encoding="utf-8")


def wire_svg(p: Path) -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="400" viewBox="0 0 900 400">
<rect width="100%" height="100%" fill="#f5f9fc"/>
<text x="22" y="34" font-size="19" font-weight="600" font-family="system-ui,sans-serif" fill="#1d1d1f">Crossing risk dashboard — wireframe</text>
<text x="22" y="56" font-size="12" fill="#6e6e73" font-family="system-ui,sans-serif">Trend + state ranking + device mix (Figma handoff vector)</text>
<rect x="20" y="78" width="150" height="64" rx="10" fill="#fff" stroke="#e2e8f0"/>
<rect x="186" y="78" width="150" height="64" rx="10" fill="#fff" stroke="#e2e8f0"/>
<rect x="352" y="78" width="150" height="64" rx="10" fill="#fff" stroke="#e2e8f0"/>
<rect x="20" y="158" width="420" height="210" rx="12" fill="#fff" stroke="#e2e8f0"/>
<rect x="458" y="158" width="420" height="210" rx="12" fill="#fff" stroke="#e2e8f0"/>
<text x="36" y="118" font-size="11" fill="#6e6e73" font-family="system-ui,sans-serif">KPI: Incidents</text>
<text x="400" y="188" font-size="12" font-weight="600" fill="#2b7fd4" font-family="system-ui,sans-serif">Year trend</text>
<text x="820" y="188" font-size="12" font-weight="600" fill="#2b7fd4" font-family="system-ui,sans-serif" text-anchor="end">Device mix</text>
</svg>"""
    p.write_text(svg, encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    pub = root / "analytics_stack" / "published"
    pub.mkdir(parents=True, exist_ok=True)

    grain = synthetic_crossings(3500)
    grain.to_csv(pub / "crossings_grain_demo.csv", index=False)

    by_sy = grain.groupby(["State", "Year"], as_index=False).size().rename(columns={"size": "Incident_Count"})
    by_sy.to_csv(pub / "severity_by_state_year.csv", index=False)

    mix = grain.groupby("Warning_Device", as_index=False).size().rename(columns={"size": "Incident_Count"})
    mix["share"] = mix["Incident_Count"] / mix["Incident_Count"].sum()
    mix.to_csv(pub / "crossing_device_mix.csv", index=False)

    write_html(pub / "dashboard.html", by_sy, mix)
    wire_svg(pub / "wireframe_dashboard.svg")
    print("Wrote", pub)


if __name__ == "__main__":
    main()
