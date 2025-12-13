# TCGA Download Guide

**A comprehensive, step-by-step toolkit for downloading and organizing TCGA data from the GDC portal**

# TCGA Download & Organization Guide

A focused, reproducible workflow for **downloading and organizing TCGA data**  
with an emphasis on **whole-slide images (WSI)** and **case-centric structure**.

This repository provides:
- Step-by-step documentation
- Minimal, reliable scripts
- A clean post-download organization strategy

**Scope is intentionally limited** to:
> Download → Verify → Organize  
No analysis, no modeling, no preprocessing beyond organization.

---

## 1. What This Repository Does

This repository helps you:

- Download TCGA metadata (files, clinical, annotations)
- Download large files (WSI `.svs`) using the **GDC Data Transfer Tool**
- Verify download integrity
- Organize slides into **case-level folders**
- Preserve original GDC UUID-based structure
- Produce clean mapping tables for downstream use

---

## 2. What This Repository Does NOT Do

This repository does **not**:
- Train machine learning models
- Tile or preprocess slides
- Perform feature extraction
- Modify raw TCGA data
- Perform statistical or survival analysis

Those steps are intentionally left to downstream pipelines.

---

## 3. Repository Structure

```text
TCGA-DOWNLOAD-GUIDE/
├─ docs/                      # Step-by-step documentation
│  ├─ 01_tcga_overview.md
│  ├─ 01-complete_download_guide.md
│  ├─ 02_metadata_and_manifests.md
│  ├─ 03_slide_download_with_gdc_client.md
│  └─ 04_post_download_organization.md
│
├─ scripts/                   # Minimal automation scripts
│  ├─ S00_paths_config.py
│  ├─ S01_parse_files_json_build_slide_map.py
│  ├─ S02_index_raw_gdc_slides.py
│  └─ S03_organize_slides_by_case.py
│
├─ LICENSE
├─ README.md
└─ requirements.txt

```

## 4. Prerequisites
Software

- Python ≥ 3.8
- pandas, tqdm
- GDC Data Transfer Tool (gdc-client)
- Install Python dependencies: pip install -r requirements.txt
- Install gdc-client from: https://gdc.cancer.gov/access-data/gdc-data-transfer-tool

5. Recommended Reading Order

Read the documentation in order:

1. docs/01_tcga_overview.md
-   TCGA concepts, identifiers, data categories
2. docs/01-complete_download_guide.md
-   End-to-end overview
3. docs/02_metadata_and_manifests.md
-   Files metadata and manifests
4. docs/03_slide_download_with_gdc_client.md
-   Downloading .svs files safely
5. docs/04_post_download_organization.md
-   Organizing slides by case


6. Typical Workflow (Use Case: BRCA)
Step 1 — Download metadata from GDC Portal

- Files metadata (Files_TCGA-BRCA.json)
- Clinical metadata (Clinical_TCGA-BRCA.json)
- (Optional) Annotations
- Store under a project metadata folder.

Step 2 — Download slides with gdc-client


gdc-client download \
  -m BRCA_Manifest.txt \
  -d raw_gdc/

Verify:

gdc-client verify \
  -m BRCA_Manifest.txt \
  -d raw_gdc/


Ensure:

No .svs.partial files remain


Step 3 — Configure paths

Edit:

scripts/S00_paths_config.py


Set:
- RAW_GDC_DIR
- ORGANIZED_DIR
- Metadata file paths

Step 4 — Build slide-to-case mapping
python scripts/S01_parse_files_json_build_slide_map.py


Output:

organized/tables/slide_case_map.csv

Step 5 — Index downloaded slides
python scripts/S02_index_raw_gdc_slides.py


Output:

organized/tables/raw_gdc_slide_index.csv

Step 6 — Organize slides by case (dry run)
python scripts/S03_organize_slides_by_case.py


Inspect the report.
If correct, rerun with copying enabled.

7. Final Output Structure


organized/
  slides/
    TCGA-XX-YYYY/
      slide1.svs
      slide2.svs
  tables/
    slide_case_map.csv
    raw_gdc_slide_index.csv
    slide_organization_report.csv


- Multiple slides per case are supported
- Original raw_gdc/ remains untouched



8. Reproducibility and Best Practices
- Always keep raw GDC downloads unchanged
- Version-control only small tables and scripts
- Reuse manifests for exact reproducibility
- Document project-specific assumptions externally




10. Citation / Acknowledgment

- If you find this repository useful, please star it and acknowledge:
- The TCGA Research Network
- The NCI Genomic Data Commons (GDC)














