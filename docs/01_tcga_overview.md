# TCGA Overview and Data Landscape

## 1. What is TCGA?

The Cancer Genome Atlas (TCGA) is a landmark cancer genomics program that
characterized over 20,000 primary cancer and matched normal samples across
33 cancer types. TCGA data are hosted and maintained by the
**NCI Genomic Data Commons (GDC)**.

TCGA provides multi-modal data including:
- Whole-slide pathology images (WSI, `.svs`)
- Clinical and demographic data
- Biospecimen metadata
- Molecular profiling (RNA-seq, DNA methylation, CNV, mutations)
- Pathology reports and annotations

This repository focuses on **data engineering workflows** to download,
organize, and harmonize TCGA data for research and machine learning.

---

## 2. TCGA Identifiers (Critical Concepts)

### 2.1 Case / Patient Identifiers

A TCGA case is identified by a **submitter ID**, for example: TCGA-B2-4099


This ID is consistent across:
- Clinical data
- Biospecimen data
- Slide images
- Reports and annotations

### 2.2 File Identifiers (UUIDs)

Every file in GDC is assigned a **UUID**, for example: b201cdba-9dbd-4a5d-b507-d1acd9aeecb5



This UUID:
- Is used by the GDC Data Transfer Tool
- Appears as a folder name during downloads
- Must be mapped back to the case submitter ID

---

## 3. Data Categories in GDC

Common GDC data categories used in TCGA projects:

| Category | Description |
|--------|------------|
| Biospecimen | Slide images, sample metadata |
| Clinical | Patient-level clinical data |
| Annotation | Quality flags and curated notes |
| Transcriptome Profiling | RNA-seq expression |
| Copy Number Variation | CNV data |
| Simple Nucleotide Variation | Somatic mutations |

---

## 4. Why a Structured Workflow is Required

TCGA data:
- Are distributed across multiple APIs and download methods
- Use nested JSON structures
- Separate metadata from physical file downloads
- Require explicit mapping between UUIDs and cases

This repository provides:
- Reproducible metadata parsing
- Safe handling of large files
- Clean per-case organization
- Ready-to-use tables for analysis

---

## 5. Repository Philosophy

Key design principles:
- **Never modify raw GDC downloads**
- **Always preserve UUID-based structures**
- **Organize clean views per case**
- **Commit only small, processed tables to GitHub**
- **Support multiple cancer types consistently**

---

## 6. Supported Cancer Types (Examples)

This workflow applies to any TCGA project, including:
- TCGA-BRCA (Breast)
- TCGA-KIRC / KIRP / KICH (Kidney)
- TCGA-LUAD / LUSC (Lung)
- TCGA-PRAD (Prostate)

Only the project ID changes; the workflow remains the same.


