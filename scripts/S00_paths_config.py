# scripts/brca/00_paths_config.py
from __future__ import annotations
from pathlib import Path

# ---- Update these paths ----
PROJECT_ID = "TCGA-BRCA"

# Where gdc-client downloaded slides (UUID folders)
RAW_GDC_DIR = Path(r"D:\TCGA_Projects\TCGA-BRCA\raw_gdc")

# Where we store portal-downloaded metadata JSONs
RAW_METADATA_DIR = Path(r"D:\TCGA_Projects\TCGA-BRCA\metadata\raw")

# Output folder for organized (derived) dataset
ORGANIZED_DIR = Path(r"D:\TCGA_Projects\TCGA-BRCA\organized")

# Processed tables folder
TABLES_DIR = ORGANIZED_DIR / "tables"

# ---- Input files we download from portal (recommended) ----
FILES_JSON = RAW_METADATA_DIR / "Files_TCGA-BRCA.json"
CLINICAL_JSON = RAW_METADATA_DIR / "Clinical_TCGA-BRCA.json"  # if we have it
ANNOTATIONS_JSON = RAW_METADATA_DIR / "Annotation_TCGA-BRCA.json"  # optional


