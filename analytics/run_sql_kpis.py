#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = (ROOT / "analytics_stack" / "published").resolve()
OUT = ROOT / "analytics" / "reports" / "sql_kpi_summary.txt"


def main() -> int:
    if not (PUBLISHED / "severity_by_state_year.csv").exists():
        print("Missing published CSVs. Run: python tools/build_published_deliverables.py", file=sys.stderr)
        return 1
    raw = (ROOT / "analytics" / "sql" / "kpis.sql").read_text(encoding="utf-8")
    sql = raw.replace("{{PUBLISHED}}", str(PUBLISHED).replace("\\", "/"))
    con = duckdb.connect(":memory:")
    blocks = [b.strip() for b in re.split(r";", sql) if b.strip() and not b.strip().startswith("--")]
    lines: list[str] = []
    for block in blocks:
        if block.upper().startswith("CREATE "):
            con.execute(block)
            continue
        if block.upper().startswith(("SELECT", "WITH")):
            lines.append(block.split("\n")[0][:100] + " …")
            df = con.execute(block).fetchdf()
            lines.append(df.to_string(index=False))
            lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
