#!/usr/bin/env python3
"""Export BI-friendly aggregates from a cleaned highway-rail accident CSV.

Your notebook may use different column names. Edit COLMAP below to match the cleaned export.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

# Map logical roles → your CSV column names (change after you inspect df.columns)
COLMAP = {
    "state": "State",
    "year": "Year",
    "device": None,  # optional, e.g. "Warning_Device"
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", type=Path)
    ap.add_argument("out_dir", type=Path, nargs="?", default=Path("analytics_stack/exports"))
    args = ap.parse_args()

    if not args.input_csv.is_file():
        print("Missing", args.input_csv, file=sys.stderr)
        sys.exit(1)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input_csv)

    st = COLMAP["state"]
    yr = COLMAP["year"]
    if not st or st not in df.columns or not yr or yr not in df.columns:
        print(
            "Set COLMAP['state'] and COLMAP['year'] in this script to real columns present in your CSV.",
            file=sys.stderr,
        )
        print("Found columns:", list(df.columns), file=sys.stderr)
        sys.exit(1)

    by_sy = df.groupby([st, yr], as_index=False).size().rename(columns={"size": "Incident_Count"})
    by_sy.to_csv(args.out_dir / "severity_by_state_year.csv", index=False)

    df.to_csv(args.out_dir / "crossings_grain.csv", index=False)

    dev = COLMAP.get("device")
    if dev and dev in df.columns:
        mix = df.groupby(dev, as_index=False).size().rename(columns={"size": "Incident_Count"})
        mix["share"] = mix["Incident_Count"] / mix["Incident_Count"].sum()
        mix.to_csv(args.out_dir / "crossing_device_mix.csv", index=False)

    print("Wrote aggregates to", args.out_dir.resolve())


if __name__ == "__main__":
    main()
