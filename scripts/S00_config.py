"""
S00_config.py — central configuration shared by all scripts.

Edit the paths below (or override them with environment variables) before
running S01–S04. Every script imports from this file, so paths are defined once.

Environment-variable overrides (optional):
    TCGA_PROJECT_ROOT, TCGA_RAW_GDC_DIR, TCGA_METADATA_DIR,
    TCGA_ORGANIZED_DIR, TCGA_REPORTS_CSV
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 1) Paths — UPDATE THESE
# ---------------------------------------------------------------------------
# Root folder of your local TCGA workspace (example: D:/TCGA_Projects/TCGA-BRCA)
PROJECT_ROOT = Path(os.getenv("TCGA_PROJECT_ROOT", "D:/TCGA_Projects/TCGA-BRCA"))

# Folder where gdc-client downloaded the slides (one sub-folder per file UUID)
RAW_GDC_DIR = Path(os.getenv("TCGA_RAW_GDC_DIR", PROJECT_ROOT / "raw_gdc"))

# Folder holding the GDC portal "Metadata" JSON files (Metadata_TCGA-*.json).
# Defaults to the example files shipped with this repository.
METADATA_DIR = Path(os.getenv("TCGA_METADATA_DIR", REPO_ROOT / "metadata"))

# Output folder for the organized (derived) dataset
ORGANIZED_DIR = Path(os.getenv("TCGA_ORGANIZED_DIR", PROJECT_ROOT / "organized"))

# Optional: OCR'd pathology reports (TCGA-Reports, Kefeli et al., 2024)
REPORTS_CSV = Path(os.getenv("TCGA_REPORTS_CSV", REPO_ROOT / "reports" / "TCGA_Reports.csv"))

# ---------------------------------------------------------------------------
# 2) Project selection
# ---------------------------------------------------------------------------
# Projects to process. Each needs a matching METADATA_DIR/Metadata_<PROJECT>.json.
# Use several to build one combined dataset, e.g. ["TCGA-KIRC", "TCGA-KIRP", "TCGA-KICH"].
PROJECTS: list[str] = ["TCGA-BRCA"]

# Slide types to keep (parsed from the slide barcode suffix):
#   "DX" = diagnostic (FFPE) slide, "TS"/"BS" = frozen top/bottom tissue slide.
# Use ["DX"] for diagnostic slides only, or ["DX", "TS", "BS"] for everything.
SLIDE_TYPES: list[str] = ["DX", "TS", "BS"]

# Slide file extensions recognised on disk
SLIDE_EXTS: tuple[str, ...] = (".svs",)

# ---------------------------------------------------------------------------
# 3) Derived paths — do not edit
# ---------------------------------------------------------------------------
TABLES_DIR = ORGANIZED_DIR / "tables"
SLIDES_OUT_DIR = ORGANIZED_DIR / "slides"
REPORTS_OUT_DIR = ORGANIZED_DIR / "reports"

SLIDE_CASE_MAP_CSV = TABLES_DIR / "slide_case_map.csv"
RAW_SLIDE_INDEX_CSV = TABLES_DIR / "raw_gdc_slide_index.csv"
ORGANIZATION_REPORT_CSV = TABLES_DIR / "slide_organization_report.csv"
CASES_CSV = TABLES_DIR / "cases.csv"
REPORT_CASE_MAP_CSV = TABLES_DIR / "report_case_map.csv"


def metadata_file(project_id: str) -> Path:
    """Path of the portal metadata JSON for one project."""
    return METADATA_DIR / f"Metadata_{project_id}.json"


def ensure_dirs() -> None:
    """Create output folders if they do not exist."""
    for d in (ORGANIZED_DIR, TABLES_DIR):
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    for name in ("PROJECT_ROOT", "RAW_GDC_DIR", "METADATA_DIR", "ORGANIZED_DIR",
                 "REPORTS_CSV", "PROJECTS", "SLIDE_TYPES"):
        print(f"{name:14s} = {globals()[name]}")
