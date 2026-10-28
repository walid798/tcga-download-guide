"""
S04_link_reports.py - (optional) link pathology-report text to the organized cases.

Inputs : tables/slide_case_map.csv  (S01)
         REPORTS_CSV = reports/TCGA_Reports.csv  (columns: patient_filename, text)
Outputs: tables/report_case_map.csv  (one row per report of a case in your cohort)
         organized/reports/<CASE_ID>/<report_uuid>.txt   (only with --write-txt)

`patient_filename` has the form <CASE_ID>.<report_file_uuid>, e.g.
TCGA-BP-5195.25c0b433-5557-4165-922e-2c1eac9c26f0

Run:  python scripts/S04_link_reports.py [--write-txt]
"""
from __future__ import annotations

import argparse

import pandas as pd

from S00_config import REPORT_CASE_MAP_CSV, REPORTS_CSV, REPORTS_OUT_DIR, SLIDE_CASE_MAP_CSV, ensure_dirs


def main(write_txt: bool) -> None:
    ensure_dirs()
    for f, hint in ((SLIDE_CASE_MAP_CSV, "run S01 first"), (REPORTS_CSV, "set REPORTS_CSV in S00_config.py")):
        if not f.exists():
            raise FileNotFoundError(f"Missing {f} ({hint})")

    cases = (pd.read_csv(SLIDE_CASE_MAP_CSV)[["case_submitter_id", "project_id"]]
               .drop_duplicates("case_submitter_id"))

    rep = pd.read_csv(REPORTS_CSV)
    parts = rep["patient_filename"].str.split(".", n=1, expand=True)
    rep["case_submitter_id"] = parts[0].str.strip().str.upper()
    rep["report_file_id"] = parts[1]
    rep["n_chars"] = rep["text"].fillna("").str.len()

    df = rep.merge(cases, on="case_submitter_id", how="inner")
    df = df.sort_values(["project_id", "case_submitter_id"]).reset_index(drop=True)
    df[["project_id", "case_submitter_id", "report_file_id", "n_chars"]].to_csv(REPORT_CASE_MAP_CSV, index=False)

    if write_txt:
        for r in df.itertuples(index=False):
            out = REPORTS_OUT_DIR / r.case_submitter_id / f"{r.report_file_id}.txt"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(str(r.text), encoding="utf-8")
        print(f"[OK] Wrote {len(df)} report text files under {REPORTS_OUT_DIR}")

    n_cases = cases["case_submitter_id"].nunique()
    n_with = df["case_submitter_id"].nunique()
    print(f"[OK] Wrote: {REPORT_CASE_MAP_CSV}")
    print(f"Cases with slides: {n_cases} | with a report: {n_with} ({n_with / max(n_cases, 1):.1%})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write-txt", action="store_true", help="also write one .txt per report into organized/reports/")
    main(write_txt=ap.parse_args().write_txt)
