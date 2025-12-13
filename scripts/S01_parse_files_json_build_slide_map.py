# scripts/brca/01_parse_files_json_build_slide_map.py
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

from scripts.S00_paths_config import FILES_JSON, TABLES_DIR, ensure_dirs

def _normalize_case_id(x: str) -> str:
    if not isinstance(x, str):
        return ""
    return x.strip().upper().replace("_", "-")

def load_files_json(files_json: Path) -> list[dict]:
    with open(files_json, "r", encoding="utf-8") as f:
        obj = json.load(f)
    # Common patterns: {"data": {"hits":[...]}} or direct list
    if isinstance(obj, dict) and "data" in obj and "hits" in obj["data"]:
        return obj["data"]["hits"]
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict) and "hits" in obj:
        return obj["hits"]
    raise ValueError("Unrecognized Files JSON structure.")

def build_slide_case_map(files_hits: list[dict]) -> pd.DataFrame:
    rows = []
    for h in files_hits:
        data_type = h.get("data_type")
        if data_type != "Slide Image" and data_type != "Diagnostic Slide":
            continue

        file_id = h.get("file_id", "")
        file_name = h.get("file_name", "")
        data_category = h.get("data_category", "")
        data_format = h.get("data_format", "")
        access = h.get("access", "")

        cases = h.get("cases", []) or []
        if not cases:
            continue

        # Usually one case; if multiple, keep the first and note count.
        case0 = cases[0] if isinstance(cases, list) else cases
        case_submitter_id = _normalize_case_id(case0.get("submitter_id", ""))
        project_id = ""
        try:
            project_id = case0.get("project", {}).get("project_id", "")
        except Exception:
            project_id = ""

        rows.append({
            "file_id": file_id,
            "file_name": file_name,
            "case_submitter_id": case_submitter_id,
            "project_id": project_id,
            "data_category": data_category,
            "data_type": data_type,
            "data_format": data_format,
            "access": access,
            "n_cases_linked": len(cases) if isinstance(cases, list) else 1,
        })

    df = pd.DataFrame(rows).drop_duplicates()
    df = df.sort_values(["case_submitter_id", "file_name"]).reset_index(drop=True)
    return df

def main():
    ensure_dirs()
    hits = load_files_json(FILES_JSON)
    df_slide = build_slide_case_map(hits)

    out_csv = TABLES_DIR / "brca_slide_case_map.csv"
    df_slide.to_csv(out_csv, index=False)
    print(f"[OK] Wrote: {out_csv}")
    print(df_slide["data_type"].value_counts(dropna=False))
    print("Slides:", len(df_slide), "Unique cases:", df_slide["case_submitter_id"].nunique())

if __name__ == "__main__":
    main()
