#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "analytics_stack" / "published"


def main() -> int:
    errs: list[str] = []
    sy = pd.read_csv(PUB / "severity_by_state_year.csv")
    if not {"State", "Year", "Incident_Count"} <= set(sy.columns):
        errs.append("severity_by_state_year schema wrong")
    elif (sy["Incident_Count"] <= 0).any():
        errs.append("non-positive Incident_Count")
    dv = pd.read_csv(PUB / "crossing_device_mix.csv")
    if abs(dv["share"].sum() - 1.0) > 0.02:
        errs.append(f"device mix shares sum to {dv['share'].sum()}")
    cg = pd.read_csv(PUB / "crossings_grain_demo.csv")
    if not {"State", "Year", "Warning_Device", "Severity_Bucket"} <= set(cg.columns):
        errs.append("crossings_grain schema wrong")
    elif not cg["Severity_Bucket"].isin([0, 1, 2]).all():
        errs.append("severity bucket out of 0..2")
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 1
    print("OK: highway published tables passed quality checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
