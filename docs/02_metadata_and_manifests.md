# 02 · Metadata and Manifest Files

Two small files drive the whole workflow. Download **both** for the same selection of files.

| File     | Format         | Used by          | Purpose                                  |
| -------- | -------------- | ---------------- | ---------------------------------------- |
| Manifest | TSV (`.txt`) | `gdc-client`   | Which files to download                  |
| Metadata | JSON           | `S01`–`S04` | Map each file UUID to its slide and case |

---

## 1. Selecting the slides in the GDC portal

1. Open [https://portal.gdc.cancer.gov/](https://portal.gdc.cancer.gov/) → **Repository**.
2. Filter the **Cases** panel: Program = `TCGA`, Project = e.g. `TCGA-BRCA`.
3. Filter the **Files** panel:
   - Data Category = `Biospecimen`
   - Data Type = `Slide Image`
   - Experimental Strategy = `Diagnostic Slide` (DX) and/or `Tissue Slide` (TS/BS)
   - *(optional)* Data Format = `SVS`
4. Add all files to the **Cart**.
5. From the Cart, download:
   - the **Manifest** → save as `manifests/gdc_manifest_TCGA-BRCA_slides.txt`
   - the **Metadata** (JSON) → save as `metadata/Metadata_TCGA-BRCA.json`

> **Naming matters.** The scripts look for `METADATA_DIR/Metadata_<PROJECT_ID>.json`.

---

## 2. Manifest file

A tab-separated file read by `gdc-client`. One row per file:

```
id	filename	md5	size	state
5e92f89e-5470-4f37-9002-0bb397e7281b	TCGA-E9-A1N9-01Z-00-DX1.982C83A6-....svs	5bbdf578...	514738671	released
```

The manifest makes downloads **resumable**, **verifiable** (md5 + size) and **reproducible** (the same manifest always gives the same files).

---

## 3. Metadata JSON

One record per file. The fields the scripts use:

```json
{
  "file_id": "5e92f89e-5470-4f37-9002-0bb397e7281b",
  "file_name": "TCGA-E9-A1N9-01Z-00-DX1.982C83A6-0E06-47B3-A7C7-1773A2CD1771.svs",
  "data_category": "Biospecimen",
  "data_type": "Slide Image",
  "experimental_strategy": "Diagnostic Slide",
  "md5sum": "5bbdf57893a688b24d219c4cc712bc7d",
  "file_size": 514738671,
  "associated_entities": [
    { "entity_type": "slide", "entity_submitter_id": "TCGA-E9-A1N9-01Z-00-DX1", "case_id": "994ca1f5-..." }
  ]
}
```

- **Case ID** = first three parts of `entity_submitter_id` → `TCGA-E9-A1N9`.
- `associated_entities[].case_id` is the case **UUID**, not the case submitter ID.
- Some projects also include an `annotations` list (curated notes, e.g. prior malignancy).
  `S01` counts them in the `n_annotations` column so you can review those cases.

`S01` also accepts a GDC **API** `/files` response (records with `cases[].submitter_id`).

---

## 4. Recommended storage layout

```text
TCGA_Projects/TCGA-BRCA/
├── manifests/
│   └── gdc_manifest_TCGA-BRCA_slides.txt
├── metadata/
│   └── Metadata_TCGA-BRCA.json
├── raw_gdc/          # gdc-client output — keep unchanged
└── organized/        # created by the scripts
```

Keep manifests and metadata unchanged; they are the record of exactly what you downloaded.

Next: [03 · Downloading slides with gdc-client](03_slide_download_with_gdc_client.md)
