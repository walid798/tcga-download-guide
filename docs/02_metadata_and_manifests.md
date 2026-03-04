# Metadata and Manifest Files in TCGA

## 1. Purpose of Metadata Files

Metadata files describe:
- Which files exist
- Which case each file belongs to
- File type, format, size, and access level

Metadata is essential for:
- Mapping files to cases
- Building manifests
- Organizing downloaded data
- Reproducibility

---

## 2. Core Metadata File Types

### 2.1 Files Metadata (`Files_TCGA-*.json`)

Contains one entry per file in a TCGA project.

Key fields:
- `file_id` (UUID)
- `file_name`
- `data_category`
- `data_type`
- `data_format`
- `cases.submitter_id`

This file is the **authoritative source** for mapping:

UUID → filename → case


---

### 2.2 Clinical Metadata (`Clinical_TCGA-*.json`)

Contains patient-level information:
- Demographics
- Diagnosis
- Tumor stage
- Survival data

This file must be:
- Flattened
- Normalized
- Cleaned into a CSV

---

### 2.3 Annotations (`Annotation_TCGA-*.json`)

Contains curated notes and flags:
- Sample quality issues
- Known artifacts
- Exclusion warnings

Annotations should be joined with case-level tables
to flag problematic data.

---

## 3. Manifest Files (`*_Manifest.txt`)

A **manifest** is a TSV file used by the GDC Data Transfer Tool.

Each row corresponds to one file and includes:
- UUID
- File size
- Checksum

Manifests allow:
- Resumable downloads
- Verification
- Reproducibility

---

## 4. How Metadata and Manifests Work Together

Workflow:
1. Use metadata to identify files of interest
2. Generate or download a manifest
3. Use the manifest to download large files
4. Use metadata again to organize downloaded files

---

## 5. Recommended Storage Layout

```text
metadata/
  raw/
    Files_TCGA-BRCA.json
    Clinical_TCGA-BRCA.json
    Annotation_TCGA-BRCA.json
  manifests/
    BRCA_Manifest.txt

These files should be preserved unchanged.

## Troubleshooting: "Can't move files" (GDC Transfer Tool / gdc-client on Windows)

On Windows, the GDC Transfer Tool may **download into a temporary cache on `C:`** first, then **move** files to your target directory.  
If `C:` is low on space (or the TEMP directory is locked), you may see errors like **"can't move the files"**.

### Quick fix (temporary, recommended): set TEMP/TMP to the target drive (one session)

1. Create a temp folder on the same drive where you want to store downloads (example: `D:`).
2. Set `TEMP` and `TMP` for the current PowerShell session.
3. Launch the Transfer Tool from the same terminal (so it inherits the variables).

```powershell
# Example: target drive is D:
mkdir D:\TempTCGA -Force | Out-Null
$env:TEMP="D:\TempTCGA"
$env:TMP="D:\TempTCGA"

# Option A: if you use gdc-client CLI
gdc-client download -m manifest.txt -d D:\TCGA

# Option B: if you use the GUI Transfer Tool, launch it from here
# & "C:\Path\To\GDCTransferTool.exe"
