# Post-Download Organization of TCGA Data

## Overview

After completing slide downloads and verification using the GDC Data Transfer Tool,
the downloaded data are stored in a **UUID-based directory structure** that is not
convenient for analysis or machine learning.

This document describes:
1. What files are required to organize TCGA slides by case
2. How to obtain those files (if not already available)
3. How to safely organize slides into **case-centric folders**
4. How to extend the same organization logic to reports and other files

This step **does not modify or delete** the original GDC downloads.

---

## 1. What We Have After Download Verification

our directory typically looks like this:


raw_gdc/
  b201cdba-9dbd-4a5d-b507-d1acd9aeecb5/
    b201cdba-9dbd-4a5d-b507-d1acd9aeecb5.log
    TCGA-B2-4099-01A-02-BS2.cda80782-5212-4aef-80dc-abebaa70621e.svs
  3e482a11-xxxx-xxxx-xxxx-xxxxxxxxxxxx/
    ...


### Important characteristics:

- Each file UUID has its own folder
- Slides are stored as .svs
- Logs are stored per UUID
- The directory structure is file-centric, not case-centric

This layout is correct and must be preserved.


## Goal of Post-Download Organization

The objective is to create a clean, human-readable view of the data,
organized by TCGA case (patient).

Target structure:

organized/
  slides/
    TCGA-B2-4099/
      slide_1.svs
      slide_2.svs
    TCGA-BH-AB28/
      slide_1.svs
  reports/
    TCGA-B2-4099/
      pathology_report.pdf
  tables/
    slide_case_map.csv
    clinical_clean.csv
    training_table.csv


Key principles:

- Raw GDC downloads remain untouched (or we can move them instead of copying)
- Organized data is a derived view
- Multiple slides per case are supported
- The same logic applies to reports and other files

### Files Required for Organization (and How to Get Them)

To organize slides by case, We need metadata, not additional downloads.

- Required File: File Metadata (Critical): We need a file-level metadata table that contains:

- file_id (UUID)
- file_name
- data_type (e.g., Slide Image)
- cases.submitter_id (TCGA case ID)


## Building the Slide-to-Case Mapping


Using the file metadata:

1. Filter rows where:
-   data_type == "Slide Image"
2. Extract:
-   file_id
-   file_name
-   cases.submitter_id



This produces a table like:

file_id | file_name | case_submitter_id
--------------------------------------
b201cdba-... | TCGA-B2-4099-01A-02-BS2....svs | TCGA-B2-4099


Save this as: tables/slide_case_map.csv

This table drives all organization steps.


## Indexing the Downloaded Files on Disk


Next, scan the raw_gdc directory to determine:

- Where each .svs file physically lives
- Its absolute path

This produces a disk index:
file_name | abs_path
--------------------
TCGA-B2-4099-01A-02-BS2....svs | raw_gdc/b201cdba-.../TCGA-B2-4099-01A-02-BS2....svs


## Organizing Slides into Case-Centric Folders

For each row in slide_case_map.csv:

1. Locate the slide file on disk using file_name
2. Create a folder named after case_submitter_id
3. Copy the .svs file into that folder

Example result:

organized/slides/TCGA-B2-4099/
  TCGA-B2-4099-01A-02-BS2....svs
  TCGA-B2-4099-01A-01-BS1....svs

Notes:

- A case may have multiple slides
- Filenames are preserved
- No UUID folders are modified or removed

## Extending the Same Logic to Reports and Other Files

- The same organization workflow applies to:
- Pathology reports
- XML annotations
- Other small clinical files


Steps:

1. Filter file metadata by data_type
2. Build a report_case_map.csv
3. Index downloaded files
4. Copy into: organized/reports/{CASE_ID}/










