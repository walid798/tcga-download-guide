"""
S03_organize_slides_by_case.py - place slides into case-centric folders.

Inputs : tables/slide_case_map.csv  (S01)
         tables/raw_gdc_slide_index.csv  (S02)
Outputs: organized/slides/<CASE_ID>/<slide>.svs
         tables/slide_organization_report.csv
         tables/cases.csv  (one row per case: project, number of slides)

Slides are matched by file UUID (the gdc-client folder name), falling back to file name.

Modes (--mode):
  copy      safest; raw_gdc stays untouched; needs double disk space   [default]
  hardlink  no extra space; raw_gdc untouched; same drive/partition only
  symlink   no extra space; links break if raw_gdc is moved
  move      no extra space; EMPTIES raw_gdc (gdc-client can no longer resume/verify)

The default is a DRY RUN. Inspect the report, then re-run with --execute.

Run:  python scripts/S03_organize_slides_by_case.py                     # dry run
      python scripts/S03_organize_slides_by_case.py --execute --mode hardlink
"""
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from S00_config import (CASES_CSV, ORGANIZATION_REPORT_CSV, RAW_SLIDE_INDEX_CSV,
                        SLIDE_CASE_MAP_CSV, SLIDES_OUT_DIR, ensure_dirs)

MODES = ("copy", "hardlink", "symlink", "move")


def transfer(src: Path, dst: Path, mode: str) -> None:
    if mode == "copy":
        shutil.copy2(src, dst)
    elif mode == "hardlink":
        os.link(src, dst)
    elif mode == "symlink":
        os.symlink(src, dst)
    elif mode == "move":
        shutil.move(str(src), str(dst))


def main(execute: bool, mode: str, overwrite: bool) -> None:
    ensure_dirs()
    for f, step in ((SLIDE_CASE_MAP_CSV, "S01"), (RAW_SLIDE_INDEX_CSV, "S02")):
        if not f.exists():
            raise FileNotFoundError(f"Missing {f} (run {step} first)")

    df_map = pd.read_csv(SLIDE_CASE_MAP_CSV)
    df_idx = pd.read_csv(RAW_SLIDE_INDEX_CSV)

    by_id = df_idx.groupby("file_id")["abs_path"].apply(list).to_dict()
    by_name = df_idx.groupby("file_name")["abs_path"].apply(list).to_dict()

    report = []
    for row in tqdm(df_map.itertuples(index=False), total=len(df_map), desc="Organizing slides"):
        candidates = by_id.get(row.file_id) or by_name.get(row.file_name, [])
        rec = {"project_id": row.project_id, "case_id": row.case_submitter_id,
               "file_id": row.file_id, "file_name": row.file_name, "src_path": None, "dst_path": None}

        if not candidates:
            report.append({**rec, "status": "missing_source"})
            continue
        if len(candidates) > 1:
            report.append({**rec, "src_path": " | ".join(candidates), "status": "ambiguous_source"})
            continue

        src = Path(candidates[0])
        dst = SLIDES_OUT_DIR / row.case_submitter_id / row.file_name
        rec.update(src_path=str(src), dst_path=str(dst))

        if dst.exists() and not overwrite:
            status = "exists"
        elif not execute:
            status = f"planned_{mode}"
        else:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists() or dst.is_symlink():
                    dst.unlink()
                transfer(src, dst, mode)
                status = f"done_{mode}"
            except OSError as e:
                status = f"error: {e}"
        report.append({**rec, "status": status})

    df_rep = pd.DataFrame(report)
    df_rep.to_csv(ORGANIZATION_REPORT_CSV, index=False)

    ok = df_rep[df_rep["status"].str.startswith(("done", "exists", "planned"))]
    cases = (ok.groupby(["case_id", "project_id"]).size().rename("n_slides").reset_index()
               .sort_values(["project_id", "case_id"]))
    cases.to_csv(CASES_CSV, index=False)

    print(f"[OK] Wrote: {ORGANIZATION_REPORT_CSV}")
    print(f"[OK] Wrote: {CASES_CSV} ({len(cases)} cases)")
    print(df_rep["status"].value_counts().to_string())
    if not execute:
        print("\n[DRY RUN] Nothing was changed. Re-run with --execute to apply.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--execute", action="store_true", help="apply changes (default: dry run)")
    ap.add_argument("--mode", choices=MODES, default="copy", help="how to place slides (default: copy)")
    ap.add_argument("--overwrite", action="store_true", help="replace slides that already exist")
    a = ap.parse_args()
    main(execute=a.execute, mode=a.mode, overwrite=a.overwrite)
