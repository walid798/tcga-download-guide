<div align="center">

# 🧬 TCGA Download Guide

**A reproducible toolkit for downloading and organizing TCGA whole-slide images (WSI) from the NCI GDC portal**

[![Python](https://img.shields.io/badge/Python-≥3.9-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![GDC](https://img.shields.io/badge/Data-NCI%20GDC-orange)](https://portal.gdc.cancer.gov/)
[![Stars](https://img.shields.io/github/stars/walid798/tcga-download-guide?style=social)](https://github.com/walid798/tcga-download-guide)

*Download → Verify → Organize · Case-centric folders · Raw data kept intact*

</div>

---

## 📌 Overview

A small, reliable workflow to **download TCGA whole-slide images** with `gdc-client` and
**organize them into one folder per patient (case)**, plus an optional link to pathology-report text.

**What you get**
- ✅ Step-by-step docs from portal selection to organized slides
- ✅ Four short Python scripts driven by one config file
- ✅ Clean CSV tables (slide ↔ case ↔ report) for downstream pipelines
- ✅ Multi-project support (e.g. KIRC + KIRP + KICH in one run)
- ✅ Example metadata for 7 TCGA projects

**Out of scope:** model training, tiling, preprocessing, feature extraction.

---

## 📁 Repository Structure

```
tcga-download-guide/
├── docs/
│   ├── 01_tcga_overview.md                  # TCGA identifiers and data categories
│   ├── 02_metadata_and_manifests.md         # Selecting files; manifest + metadata JSON
│   ├── 03_slide_download_with_gdc_client.md # Downloading and verifying .svs files
│   └── 04_post_download_organization.md     # Running S01–S04
├── scripts/
│   ├── S00_config.py                        # All paths and settings (edit this)
│   ├── S01_build_slide_case_map.py          # metadata JSON → slide_case_map.csv
│   ├── S02_index_raw_slides.py              # raw_gdc/ → raw_gdc_slide_index.csv
│   ├── S03_organize_slides_by_case.py       # → organized/slides/<CASE_ID>/
│   └── S04_link_reports.py                  # (optional) pathology report text per case
├── metadata/                                # Example GDC metadata (slide images)
│   └── Metadata_TCGA-{BRCA,LUAD,LUSC,KIRC,KIRP,KICH,PRAD}.json
├── reports/
│   ├── TCGA_Reports.csv                     # OCR'd TCGA pathology reports
│   └── tcga_patient_to_cancer_type.csv      # case ID → cancer type
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙️ Prerequisites

| Requirement | Details |
|---|---|
| **Python** | ≥ 3.9 |
| **Packages** | `pandas`, `tqdm` |
| **GDC Data Transfer Tool** | [`gdc-client`](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool) |

```bash
git clone https://github.com/walid798/tcga-download-guide.git
cd tcga-download-guide
pip install -r requirements.txt
```

---

## 📖 Documentation

| Step | File | Content |
|---|---|---|
| 1 | [`docs/01_tcga_overview.md`](docs/01_tcga_overview.md) | Case IDs, slide barcodes, file UUIDs |
| 2 | [`docs/02_metadata_and_manifests.md`](docs/02_metadata_and_manifests.md) | Selecting slides; manifest and metadata |
| 3 | [`docs/03_slide_download_with_gdc_client.md`](docs/03_slide_download_with_gdc_client.md) | Download, resume, verify, troubleshooting |
| 4 | [`docs/04_post_download_organization.md`](docs/04_post_download_organization.md) | Organizing slides and reports |

---

## 🚀 Quick Start — TCGA-BRCA

**1. Get the manifest and metadata** from the [GDC portal](https://portal.gdc.cancer.gov/)
(Repository → Project `TCGA-BRCA` → Data Type `Slide Image` → add to cart → download
**Manifest** and **Metadata**). Save the metadata as `metadata/Metadata_TCGA-BRCA.json`.
→ [details](docs/02_metadata_and_manifests.md)

**2. Download the slides** (re-run the same command until nothing fails; it resumes and checks md5):

```bash
gdc-client download -m gdc_manifest_TCGA-BRCA_slides.txt -d /path/to/TCGA-BRCA/raw_gdc -n 4
```

**3. Configure** `scripts/S00_config.py`:

```python
PROJECT_ROOT = Path("/path/to/TCGA-BRCA")   # contains raw_gdc/; organized/ is created here
PROJECTS     = ["TCGA-BRCA"]
SLIDE_TYPES  = ["DX"]                       # diagnostic slides only; ["DX","TS","BS"] for all
```

**4. Run the pipeline** (from the repository root):

```bash
python scripts/S01_build_slide_case_map.py               # → tables/slide_case_map.csv
python scripts/S02_index_raw_slides.py                   # → tables/raw_gdc_slide_index.csv (+ .partial check)
python scripts/S03_organize_slides_by_case.py            # dry run → check slide_organization_report.csv
python scripts/S03_organize_slides_by_case.py --execute --mode hardlink   # or: copy | symlink | move
python scripts/S04_link_reports.py                       # optional → tables/report_case_map.csv
```

---

## 📂 Output

```
organized/
├── slides/
│   ├── TCGA-3C-AALI/
│   │   ├── TCGA-3C-AALI-01Z-00-DX1.<uuid>.svs
│   │   └── TCGA-3C-AALI-01Z-00-DX2.<uuid>.svs
│   └── TCGA-E9-A1N9/
│       └── TCGA-E9-A1N9-01Z-00-DX1.<uuid>.svs
├── reports/                          # only with S04 --write-txt
└── tables/
    ├── slide_case_map.csv            # file UUID ↔ slide barcode ↔ case, md5, size
    ├── raw_gdc_slide_index.csv       # where each slide is on disk
    ├── slide_organization_report.csv # status per slide
    ├── cases.csv                     # one row per case, number of slides
    └── report_case_map.csv           # reports available per case
```

- Multiple slides per case are supported; original file names are kept.
- With `copy`, `hardlink` or `symlink`, `raw_gdc/` stays unchanged.

---

## 🔁 Reproducibility

- Keep `raw_gdc/`, manifests and metadata JSONs unchanged.
- Re-using the same manifest gives exactly the same files.
- Commit only scripts and small tables — never WSIs (`.gitignore` excludes them).
- The example metadata in `metadata/` is a snapshot; GDC releases can add or retire files,
  so download fresh metadata together with your manifest.

---

## 📚 Data Credits

- **TCGA Research Network** and **NCI Genomic Data Commons** — please follow the
  [TCGA publication guidelines](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/citing).
- **`reports/`** — derived from *TCGA-Reports* (Kefeli J., Tatonetti N., 2024),
  [Mendeley Data, doi:10.17632/hyg5xkznpx.1](https://data.mendeley.com/datasets/hyg5xkznpx/1), CC BY 4.0.
  If you use the report text, cite:
  Kefeli J., Tatonetti N. *TCGA-Reports: A machine-readable pathology report resource for benchmarking
  text-based AI models.* Patterns 5(3):100933, 2024. [doi:10.1016/j.patter.2024.100933](https://doi.org/10.1016/j.patter.2024.100933)

---

## 🌟 Support

If this repository saved you time, please ⭐ **star it** — it helps others find it.

- 🐛 [Open an issue](https://github.com/walid798/tcga-download-guide/issues) for bugs or ideas
- 🔀 Pull requests are welcome


## 📜 License

Code and documentation: [Apache 2.0](LICENSE). Data in `reports/` keeps its original CC BY 4.0 license.
