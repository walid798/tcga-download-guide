"""
S02_index_raw_slides.py - index the slides that gdc-client downloaded.

Input : RAW_GDC_DIR/<file_uuid>/<slide>.svs
Output: organized/tables/raw_gdc_slide_index.csv

Also reports unfinished downloads (*.partial). Use --md5 to verify each file
against the md5sum in slide_case_map.csv (slow for large cohorts).

Run:  python scripts/S02_index_raw_slides.py [--md5]
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from S00_config import RAW_GDC_DIR, RAW_SLIDE_INDEX_CSV, SLIDE_CASE_MAP_CSV, SLIDE_EXTS, ensure_dirs


def md5_of(path: Path, chunk: int = 8 * 1024 * 1024) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def main(check_md5: bool = False) -> None:
    ensure_dirs()
    if not RAW_GDC_DIR.exists():
        raise FileNotFoundError(f"RAW_GDC_DIR not found: {RAW_GDC_DIR}")

    partial = sorted(RAW_GDC_DIR.rglob("*.partial"))
    if partial:
        print(f"[WARN] {len(partial)} unfinished downloads (*.partial). "
              "Re-run gdc-client with the same manifest to resume them.")

    rows = []
    for p in RAW_GDC_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in SLIDE_EXTS:
            rows.append({
                "file_id": p.parent.name,          # gdc-client folder = file UUID
                "file_name": p.name,
                "abs_path": str(p.resolve()),
                "rel_path": str(p.relative_to(RAW_GDC_DIR)),
                "size_on_disk": p.stat().st_size,
            })

    df = pd.DataFrame(rows, columns=["file_id", "file_name", "abs_path", "rel_path", "size_on_disk"])

    if check_md5 and not df.empty:
        if not SLIDE_CASE_MAP_CSV.exists():
            raise FileNotFoundError(f"Missing {SLIDE_CASE_MAP_CSV} (run S01 first)")
        expected = pd.read_csv(SLIDE_CASE_MAP_CSV).set_index("file_id")["md5sum"].to_dict()
        df["md5_ok"] = [
            (md5_of(Path(p)) == expected[fid]) if fid in expected else None
            for fid, p in tqdm(zip(df["file_id"], df["abs_path"]), total=len(df), desc="Checking md5")
        ]
        print(f"[INFO] md5 mismatches: {(df['md5_ok'] == False).sum()}")  # noqa: E712

    df = df.sort_values(["file_name", "rel_path"]).reset_index(drop=True)
    df.to_csv(RAW_SLIDE_INDEX_CSV, index=False)

    print(f"[OK] Wrote: {RAW_SLIDE_INDEX_CSV}")
    print(f"Slides indexed: {len(df)} | Partial files: {len(partial)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--md5", action="store_true", help="verify md5 checksums against slide_case_map.csv")
    main(check_md5=ap.parse_args().md5)
