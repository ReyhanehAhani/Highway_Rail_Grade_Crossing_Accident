#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "analytics" / "reports" / "case_study.md"
SQL = ROOT / "analytics" / "reports" / "sql_kpi_summary.txt"
OUT = ROOT / "analytics" / "reports" / "ANALYST_DS_REPORT.html"
DOCS = ROOT / "docs" / "report.html"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_to_html(md: str) -> str:
    parts: list[str] = []
    for block in md.split("\n\n"):
        b = block.strip()
        if not b:
            continue
        if b.startswith("# "):
            parts.append(f"<h1>{esc(b[2:])}</h1>")
        elif b.startswith("## "):
            parts.append(f"<h2>{esc(b[3:])}</h2>")
        elif b.startswith("```"):
            parts.append(f"<pre>{esc(block)}</pre>")
        else:
            if all(line.startswith("- ") for line in b.split("\n") if line.strip()):
                items = "".join(f"<li>{esc(l[2:])}</li>" for l in b.split("\n") if l.strip())
                parts.append("<ul>" + items + "</ul>")
            else:
                parts.append("<p>" + esc(b).replace("\n", "<br/>") + "</p>")
    return "\n".join(parts)


def main() -> None:
    body = md_to_html(MD.read_text(encoding="utf-8"))
    sqlb = f"<h2>SQL snapshot</h2><pre>{esc(SQL.read_text(encoding='utf-8'))}</pre>" if SQL.exists() else ""
    mlink = "<h2>Modeling artifacts</h2><ul><li><a href='../modeling/artifacts/metrics.json'>metrics.json</a></li><li><a href='../modeling/artifacts/confusion_matrix.png'>confusion matrix</a></li><li><a href='../modeling/artifacts/permutation_importance.png'>permutation importance</a></li><li><a href='../modeling/artifacts/error_sample.csv'>error sample</a></li><li><a href='../modeling/artifacts/shap_summary.png'>SHAP summary (optional)</a></li></ul>"
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Highway crossings — report</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 840px; margin: 2rem auto; padding: 0 1rem; line-height: 1.55; }}
pre {{ background: #f5f9fc; padding: 1rem; overflow: auto; border-radius: 8px; font-size: 0.8rem; }}
a {{ color: #2b7fd4; }}
</style></head><body>
<p><a href="index.html">← Hub</a> · <a href="dashboard.html">Dashboard</a></p>
{body}{sqlb}{mlink}
</body></html>"""
    OUT.write_text(html, encoding="utf-8")
    DOCS.parent.mkdir(parents=True, exist_ok=True)
    # For Pages, duplicate artifacts path won't work — embed links to GitHub raw optional
    DOCS.write_text(html, encoding="utf-8")
    print("Wrote report")


if __name__ == "__main__":
    main()
