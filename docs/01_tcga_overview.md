# 01 · TCGA Overview and Identifiers

## 1. What is TCGA?

The Cancer Genome Atlas (TCGA) characterized over 20,000 primary cancer and matched normal samples across 33 cancer types. All TCGA data are hosted by the **NCI Genomic Data Commons (GDC)**: [https://portal.gdc.cancer.gov/](https://portal.gdc.cancer.gov/).

TCGA provides multimodal data, including:

- Whole-slide images (WSI, `.svs`)
- Clinical and demographic data
- Biospecimen metadata
- Molecular profiles (RNA-seq, DNA methylation, copy number, mutations)
- Pathology reports (PDF) and annotations

This repository covers only **download → verify → organize** for slides, plus an optional link to OCR'd pathology-report text.

---

## 2. Identifiers you must know

### 2.1 Case (patient) ID

A TCGA case is identified by its **case submitter ID** (12 characters):

```
TCGA-E9-A1N9
│    │  └── participant
│    └───── tissue source site (TSS)
└────────── program
```

This ID links clinical data, biospecimens, slides and reports.

### 2.2 Slide barcode

Every slide has a longer barcode that starts with the case ID:

```
TCGA-E9-A1N9-01Z-00-DX1
             │ │     │ └─ slide number
             │ │     └─── slide type: DX = diagnostic (FFPE)
             │ │                      TS / BS = frozen top / bottom tissue slide
             │ └───────── vial
             └─────────── sample type: 01 = primary tumor, 06 = metastatic, 11 = solid normal
```

The slide file name is `<slide barcode>.<slide UUID>.svs`, for example `TCGA-E9-A1N9-01Z-00-DX1.982C83A6-0E06-47B3-A7C7-1773A2CD1771.svs`.

### 2.3 File UUID (`file_id`)

Every GDC file has a **file UUID**, for example `5e92f89e-5470-4f37-9002-0bb397e7281b`.

- The manifest lists files by this UUID.
- `gdc-client` creates one folder per UUID.
- The metadata JSON maps each UUID back to its slide barcode and case ID.

---

## 3. Data categories used here

| GDC Data Category | Data Type           | Used for                                  |
| ----------------- | ------------------- | ----------------------------------------- |
| Biospecimen       | Slide Image         | WSIs (`.svs`) — the focus of this repo |
| Clinical          | Pathology Report    | Pathology report PDFs                     |
| Clinical          | Clinical Supplement | Clinical/demographic data                 |

Slide images are split by **Experimental Strategy**: `Diagnostic Slide` (DX, FFPE) and `Tissue Slide` (TS/BS, frozen).
Most computational-pathology studies use **diagnostic slides**.

---

## 4. Design principles

- Never modify raw GDC downloads (unless you choose `--mode move`, see doc 04).
- Keep the UUID-based structure as the source of truth.
- Build case-centric folders as a **derived view**.
- Commit only small tables and scripts to Git - never WSIs.
- Use the same workflow for every project; only the project ID changes.

---

## 5. Projects with example metadata in this repo

| Project                           | Organ    | Metadata file                                           |
| --------------------------------- | -------- | ------------------------------------------------------- |
| TCGA-BRCA                         | Breast   | `metadata/Metadata_TCGA-BRCA.json`                    |
| TCGA-LUAD / TCGA-LUSC             | Lung     | `metadata/Metadata_TCGA-LUAD.json`, `..._LUSC.json` |
| TCGA-KIRC / TCGA-KIRP / TCGA-KICH | Kidney   | `metadata/Metadata_TCGA-KIRC.json`, ...               |
| TCGA-PRAD                         | Prostate | `metadata/Metadata_TCGA-PRAD.json`                    |

Next: [02 · Metadata and manifests](02_metadata_and_manifests.md)
