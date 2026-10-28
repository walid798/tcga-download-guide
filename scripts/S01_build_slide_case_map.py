"""
S01_build_slide_case_map.py - build the slide -> case mapping table.

Input : METADATA_DIR/Metadata_<PROJECT>.json  (GDC portal: Cart -> Download -> Metadata)
Output: organized/tables/slide_case_map.csv

Supported JSON layouts:
  * GDC portal "Metadata" export   -> list of files with `associated_entities`
  * GDC API /files response         -> {"data": {"hits": [...]}} with `cases`
  * plain list of API hits          -> [...] with `cases`

Run:  python scripts/S01_build_slide_case_map.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from S00_config import PROJECTS, SLIDE_CASE_MAP_CSV, SLIDE_TYPES, ensure_dirs, metadata_file

# Slide barcode, e.g. TCGA-E9-A1N9-01Z-00-DX1
BARCODE_RE = re.compile(r"^(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4})-(\d{2})[A-Z]?-\d{2}-([A-Z]{2})(\d+)$")


def load_hits(path: Path) -> list[dict]:
    """Return the list of file records from any supported JSON layout."""
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        if isinstance(obj.get("data"), dict) and "hits" in obj["data"]:
            return obj["data"]["hits"]
        if "hits" in obj:
            return obj["hits"]
    raise ValueError(f"Unrecognized metadata JSON structure: {path}")


def slide_barcode(hit: dict) -> str:
    """Slide barcode from the portal export (associated_entities) or the file name."""
    for ent in hit.get("associated_entities") or []:
        if ent.get("entity_type") == "slide" and ent.get("entity_submitter_id"):
            return ent["entity_submitter_id"].strip().upper()
    # Fallback: file names look like <barcode>.<uuid>.svs
    return str(hit.get("file_name", "")).split(".")[0].strip().upper()


def case_id_of(hit: dict, barcode: str) -> str:
    """TCGA case (patient) ID, e.g. TCGA-E9-A1N9."""
    cases = hit.get("cases") or []
    if cases and cases[0].get("submitter_id"):
        return cases[0]["submitter_id"].strip().upper()
    return "-".join(barcode.split("-")[:3])


def build_slide_case_map(project_id: str, hits: list[dict]) -> pd.DataFrame:
    rows = []
    for h in hits:
        if h.get("data_type") != "Slide Image":
            continue
        barcode = slide_barcode(h)
        m = BARCODE_RE.match(barcode)
        rows.append({
            "project_id": project_id,
            "case_submitter_id": case_id_of(h, barcode),
            "slide_barcode": barcode,
            "sample_type_code": m.group(2) if m else "",   # 01 = primary tumor, 11 = normal, ...
            "slide_type": m.group(3) if m else "",         # DX / TS / BS
            "file_id": h.get("file_id", ""),
            "file_name": h.get("file_name", ""),
            "file_size": h.get("file_size"),
            "md5sum": h.get("md5sum", ""),
            "experimental_strategy": h.get("experimental_strategy", ""),
            "access": h.get("access", ""),
            "n_annotations": len(h.get("annotations") or []),
        })
    return pd.DataFrame(rows)


def main() -> None:
    ensure_dirs()
    frames = []
    for project_id in PROJECTS:
        path = metadata_file(project_id)
        if not path.exists():
            print(f"[WARN] Metadata not found, skipping: {path}")
            continue
        df = build_slide_case_map(project_id, load_hits(path))
        print(f"[INFO] {project_id}: {len(df)} slide files")
        frames.append(df)

    if not frames:
        raise SystemExit("[ERROR] No metadata loaded. Check METADATA_DIR and PROJECTS in S00_config.py")

    df = pd.concat(frames, ignore_index=True).drop_duplicates(subset="file_id")
    df = df[df["slide_type"].isin(SLIDE_TYPES)]
    df = df.sort_values(["project_id", "case_submitter_id", "file_name"]).reset_index(drop=True)
    df.to_csv(SLIDE_CASE_MAP_CSV, index=False)

    print(f"[OK] Wrote: {SLIDE_CASE_MAP_CSV}")
    print(df.groupby(["project_id", "slide_type"]).size().to_string())
    print(f"Slides: {len(df)} | Unique cases: {df['case_submitter_id'].nunique()}")


if __name__ == "__main__":
    main()
