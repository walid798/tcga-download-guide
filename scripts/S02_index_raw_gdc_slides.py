# scripts/brca/04_index_raw_gdc_slides.py
from __future__ import annotations

from pathlib import Path
import pandas as pd

from scripts.S00_paths_config import RAW_GDC_DIR, TABLES_DIR, ensure_dirs

def main():
    ensure_dirs()
    if not RAW_GDC_DIR.exists():
        raise FileNotFoundError(f"RAW_GDC_DIR not found: {RAW_GDC_DIR}")

    rows = []
    for p in RAW_GDC_DIR.rglob("*.svs"):
        rows.append({
            "file_name": p.name,
            "abs_path": str(p.resolve()),
            "uuid_folder": p.parent.name,  # usually UUID folder
            "rel_path": str(p.relative_to(RAW_GDC_DIR)),
        })

    df = pd.DataFrame(rows).sort_values(["file_name", "rel_path"]).reset_index(drop=True)
    out_csv = TABLES_DIR / "brca_raw_gdc_slide_index.csv"
    df.to_csv(out_csv, index=False)

    print(f"[OK] Wrote: {out_csv}")
    print("Slides indexed:", len(df))

if __name__ == "__main__":
    main()
