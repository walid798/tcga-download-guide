# scripts/brca/05_organize_slides_by_case.py
from __future__ import annotations

import shutil
from pathlib import Path
import pandas as pd
from tqdm import tqdm

from scripts.S00_paths_config import RAW_GDC_DIR, ORGANIZED_DIR, TABLES_DIR, ensure_dirs

def main(dry_run: bool = True, overwrite: bool = False):
    ensure_dirs()

    slide_map_csv = TABLES_DIR / "brca_slide_case_map.csv"
    index_csv = TABLES_DIR / "brca_raw_gdc_slide_index.csv"

    if not slide_map_csv.exists():
        raise FileNotFoundError(f"Missing: {slide_map_csv} (run 01 first)")
    if not index_csv.exists():
        raise FileNotFoundError(f"Missing: {index_csv} (run 04 first)")

    df_map = pd.read_csv(slide_map_csv)
    df_idx = pd.read_csv(index_csv)

    # Map file_name -> list of abs paths (handle duplicates)
    name_to_paths = {}
    for _, r in df_idx.iterrows():
        name_to_paths.setdefault(r["file_name"], []).append(r["abs_path"])

    dst_slides_root = ORGANIZED_DIR / "slides"
    dst_slides_root.mkdir(parents=True, exist_ok=True)

    report_rows = []
    for _, row in tqdm(df_map.iterrows(), total=len(df_map), desc="Organizing slides"):
        case_id = str(row["case_submitter_id"]).strip()
        file_name = str(row["file_name"]).strip()

        candidates = name_to_paths.get(file_name, [])
        if len(candidates) == 0:
            report_rows.append({
                "case_id": case_id,
                "file_name": file_name,
                "src_path": None,
                "dst_path": None,
                "status": "missing_source",
            })
            continue

        src_path = Path(candidates[0])
        ambiguous = len(candidates) > 1

        case_dir = dst_slides_root / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        dst_path = case_dir / file_name

        if dst_path.exists() and not overwrite:
            status = "exists"
        else:
            if not dry_run:
                shutil.copy2(src_path, dst_path)
            status = "copied" if not dry_run else "planned"
            if ambiguous:
                status = "ambiguous_" + status

        report_rows.append({
            "case_id": case_id,
            "file_name": file_name,
            "src_path": str(src_path),
            "dst_path": str(dst_path),
            "status": status,
        })

    df_rep = pd.DataFrame(report_rows)
    out_report = TABLES_DIR / "brca_slide_organization_report.csv"
    df_rep.to_csv(out_report, index=False)

    print(f"[OK] Wrote: {out_report}")
    print(df_rep["status"].value_counts(dropna=False))

if __name__ == "__main__":
    # First run with dry_run=True, then set False
    main(dry_run=True, overwrite=False)
