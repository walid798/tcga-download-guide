# 04 . Post-Download Organization

`raw_gdc/` is **file-centric** (one folder per file UUID). Analysis needs a **case-centric** view. The scripts below build that view from the metadata JSON, no extra downloads are needed.

```text
metadata JSON ──S01──► slide_case_map.csv ─┐
                                           ├──S03──► organized/slides/<CASE_ID>/*.svs
raw_gdc/      ──S02──► raw_gdc_slide_index.csv ┘
reports CSV   ──S04──► report_case_map.csv (+ organized/reports/<CASE_ID>/*.txt)
```

---

## 0. Configure

Edit `scripts/S00_config.py`:

```python
PROJECT_ROOT = Path("D:/TCGA_Projects/TCGA-BRCA")   # raw_gdc/ and organized/ live here
METADATA_DIR = REPO_ROOT / "metadata"               # folder with Metadata_<PROJECT>.json
PROJECTS     = ["TCGA-BRCA"]                        # or ["TCGA-KIRC", "TCGA-KIRP", "TCGA-KICH"]
SLIDE_TYPES  = ["DX", "TS", "BS"]                   # ["DX"] = diagnostic slides only
```

Check the values with `python scripts/S00_config.py`. Every path can also be set by an environment variable (see the file header).

All commands below are run from the **repository root**.

---

## 1. S01 - Slide-to-case map

```bash
python scripts/S01_build_slide_case_map.py
```

Reads `Metadata_<PROJECT>.json` for every project in `PROJECTS` and writes `organized/tables/slide_case_map.csv`:

| project_id | case_submitter_id | slide_barcode           | sample_type_code | slide_type | file_id     | file_name                          | file_size | md5sum     | experimental_strategy | access | n_annotations |
| ---------- | ----------------- | ----------------------- | ---------------- | ---------- | ----------- | ---------------------------------- | --------- | ---------- | --------------------- | ------ | ------------- |
| TCGA-BRCA  | TCGA-E9-A1N9      | TCGA-E9-A1N9-01Z-00-DX1 | 01               | DX         | 5e92f89e-… | TCGA-E9-A1N9-01Z-00-DX1.982C….svs | 514738671 | 5bbdf578… | Diagnostic Slide      | open   | 0             |

---

## 2. S02 - Index slides on disk

```bash
python scripts/S02_index_raw_slides.py          # add --md5 to re-check checksums
```

Scans `raw_gdc/` and writes `organized/tables/raw_gdc_slide_index.csv`
(`file_id`, `file_name`, `abs_path`, `rel_path`, `size_on_disk`). It warns about any `*.partial` files.

---

## 3. S03 - Organize slides by case

```bash
# 1) Dry run — nothing changes; inspect tables/slide_organization_report.csv
python scripts/S03_organize_slides_by_case.py

# 2) Apply
python scripts/S03_organize_slides_by_case.py --execute --mode copy
```

Slides are matched by **file UUID** (the `raw_gdc` folder name), with file name as a fallback.

| `--mode`             | Extra disk space | `raw_gdc/` after | Notes                                                                    |
| ---------------------- | ---------------- | ------------------ | ------------------------------------------------------------------------ |
| `copy` *(default)* | 100 %            | unchanged          | Safest                                                                   |
| `hardlink`           | none             | unchanged          | Same drive/partition only — **recommended for large cohorts**     |
| `symlink`            | none             | unchanged          | Links break if `raw_gdc/` moves; Windows may need admin/Developer Mode |
| `move`               | none             | emptied            | `gdc-client` can no longer resume or skip these files                  |

Outputs:

- `organized/slides/<CASE_ID>/<slide>.svs` — one folder per case, original file names kept
- `tables/slide_organization_report.csv` — status per slide:
  `planned_*`, `done_*`, `exists`, `missing_source`, `ambiguous_source`, `error: …`
- `tables/cases.csv` — `case_id`, `project_id`, `n_slides`

Re-running is safe: slides already in place are reported as `exists` (use `--overwrite` to replace).

---

## 4. S04 - Link pathology reports (optional)

```bash
python scripts/S04_link_reports.py               # add --write-txt to save one .txt per report
```

Uses `reports/TCGA_Reports.csv` (OCR'd TCGA pathology reports, see README → Data credits). Writes `tables/report_case_map.csv` for the cases in your cohort and prints report coverage. With `--write-txt`, the text goes to `organized/reports/<CASE_ID>/<report_uuid>.txt`.

To organize the original report **PDFs** instead, download them with a second manifest (Data Category = `Clinical`, Data Type = `Pathology Report`) and follow the same steps.

---

## 5. Final structure

```text
organized/
├── slides/
│   ├── TCGA-E9-A1N9/
│   │   └── TCGA-E9-A1N9-01Z-00-DX1.982C83A6-….svs
│   └── TCGA-3C-AALI/
│       ├── TCGA-3C-AALI-01Z-00-DX1.F6E9A5DF-….svs
│       └── TCGA-3C-AALI-01Z-00-DX2.CF4496E0-….svs
├── reports/                      # only with S04 --write-txt
│   └── TCGA-E9-A1N9/<report_uuid>.txt
└── tables/
    ├── slide_case_map.csv
    ├── raw_gdc_slide_index.csv
    ├── slide_organization_report.csv
    ├── cases.csv
    └── report_case_map.csv
```
