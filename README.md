<div align="center">

# 🧬 TCGA Download Guide

**A comprehensive, reproducible toolkit for downloading and organizing TCGA data from the GDC portal**

[![Python](https://img.shields.io/badge/Python-≥3.8-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GDC](https://img.shields.io/badge/Data-NCI%20GDC-orange)](https://portal.gdc.cancer.gov/)
[![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/YOUR_REPO?style=social)](https://github.com/YOUR_USERNAME/YOUR_REPO)

*Focused on WSI acquisition • Case-centric organization • Zero preprocessing overhead*

</div>

---

## 📌 Overview

This repository provides a clean, minimal workflow for **downloading and organizing TCGA data**, with a strong emphasis on **Whole-Slide Images (WSI)** and a **case-centric folder structure**.

> **Scope is intentionally narrow:**
> ```
> Download  →  Verify  →  Organize
> ```
> No modeling. No tiling. No feature extraction. Just reliable, reproducible data acquisition.

**What you get:**
- ✅ Step-by-step documentation from metadata to organized slides
- ✅ Minimal, well-commented Python scripts
- ✅ Clean mapping tables ready for downstream pipelines
- ✅ GDC UUID-based structure preserved throughout

**What this repo does NOT do:**
- ❌ Train ML models or perform statistical analysis
- ❌ Tile, preprocess, or modify raw TCGA data
- ❌ Perform feature extraction or survival analysis

---

## 📁 Repository Structure

```
TCGA-DOWNLOAD-GUIDE/
│
├── docs/                                    # Step-by-step documentation
│   ├── 01_tcga_overview.md                  # TCGA concepts & identifiers
│   ├── 01-complete_download_guide.md        # End-to-end overview
│   ├── 02_metadata_and_manifests.md         # Files metadata & manifests
│   ├── 03_slide_download_with_gdc_client.md # Downloading .svs files safely
│   └── 04_post_download_organization.md    # Organizing slides by case
│
├── scripts/                                 # Minimal automation scripts
│   ├── S00_paths_config.py                  # Central path configuration
│   ├── S01_parse_files_json_build_slide_map.py
│   ├── S02_index_raw_gdc_slides.py
│   └── S03_organize_slides_by_case.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙️ Prerequisites

| Requirement | Details |
|---|---|
| **Python** | ≥ 3.8 |
| **Dependencies** | `pandas`, `tqdm` |
| **GDC Client** | [gdc-data-transfer-tool](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool) |

```bash
pip install -r requirements.txt
```

---

## 📖 Recommended Reading Order

Read the documentation sequentially for the smoothest experience:

| Step | File | Description |
|------|------|-------------|
| 1 | `docs/01_tcga_overview.md` | TCGA concepts, identifiers, data categories |
| 2 | `docs/01-complete_download_guide.md` | End-to-end overview |
| 3 | `docs/02_metadata_and_manifests.md` | Files metadata and manifests |
| 4 | `docs/03_slide_download_with_gdc_client.md` | Downloading `.svs` files safely |
| 5 | `docs/04_post_download_organization.md` | Organizing slides by case |

---

## 🚀 Typical Workflow — TCGA-BRCA Example

### Step 1 — Download Metadata from GDC Portal

From the [GDC Data Portal](https://portal.gdc.cancer.gov/), download:
- `Files_TCGA-BRCA.json` — files metadata
- `Clinical_TCGA-BRCA.json` — clinical metadata
- *(Optional)* Annotations

Store these under a dedicated project metadata folder.

---

### Step 2 — Download & Verify Slides

```bash
# Download slides
gdc-client download \
  -m BRCA_Manifest.txt \
  -d raw_gdc/

# Verify integrity
gdc-client verify \
  -m BRCA_Manifest.txt \
  -d raw_gdc/
```

> ⚠️ Ensure **no `.svs.partial` files** remain before proceeding.

---

### Step 3 — Configure Paths

Edit `scripts/S00_paths_config.py` and set:

```python
RAW_GDC_DIR   = "/path/to/raw_gdc/"
ORGANIZED_DIR = "/path/to/organized/"
# + metadata file paths
```

---

### Step 4 — Build Slide-to-Case Mapping

```bash
python scripts/S01_parse_files_json_build_slide_map.py
```

**Output:** `organized/tables/slide_case_map.csv`

---

### Step 5 — Index Downloaded Slides

```bash
python scripts/S02_index_raw_gdc_slides.py
```

**Output:** `organized/tables/raw_gdc_slide_index.csv`

---

### Step 6 — Organize Slides by Case

```bash
# Dry run first — inspect the report
python scripts/S03_organize_slides_by_case.py

# Then rerun with copying enabled
```

---

## 📂 Final Output Structure

```
organized/
├── slides/
│   ├── TCGA-XX-YYYY/
│   │   ├── slide1.svs
│   │   └── slide2.svs
│   └── TCGA-XX-ZZZZ/
│       └── slide1.svs
└── tables/
    ├── slide_case_map.csv
    ├── raw_gdc_slide_index.csv
    └── slide_organization_report.csv
```

- Multiple slides per case are fully supported
- The original `raw_gdc/` directory remains **untouched**

---

## 🔁 Reproducibility & Best Practices

- 🗂️ Keep raw GDC downloads **unchanged** at all times
- 📌 Version-control only small tables and scripts — not raw data
- 🔖 Reuse manifests to guarantee **exact reproducibility**
- 📝 Document project-specific assumptions externally

---

## 🌟 Support This Project

If this repository saved you time or helped your research, please consider:

<div align="center">

**⭐ Starring the repository** — it helps others discover this toolkit and motivates continued maintenance.

[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/YOUR_REPO?style=for-the-badge&logo=github&color=yellow)](https://github.com/walid798/tcga-download-guide)

</div>

You can also contribute by:
- 🐛 Opening an [issue](https://github.com/walid798/tcga-download-guide/issues) to report bugs or suggest improvements
- 🔀 Submitting a pull request with enhancements
- 📣 Sharing this repo with colleagues working with TCGA data

---

## 📜 Acknowledgments

This toolkit builds on infrastructure provided by:

- **The TCGA Research Network** — for making large-scale cancer genomics data publicly available
- **NCI Genomic Data Commons (GDC)** — for the data portal and transfer tooling

> If you use TCGA data in a publication, please acknowledge the TCGA Research Network per their [citation guidelines](https://www.cancer.gov/tcga).

---

<div align="center">
  <sub>Built for reproducible cancer genomics research · Contributions welcome</sub>
</div>