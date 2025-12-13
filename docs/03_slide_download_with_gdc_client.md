# Downloading TCGA Slides with the GDC Data Transfer Tool

## 1. Why Use the GDC Data Transfer Tool?

Whole-slide images (.svs) are large (hundreds of MBs to GBs).
They must be downloaded using the official **GDC Data Transfer Tool**.

Advantages:
- Resume interrupted downloads
- Verify file integrity
- Handle large datasets safely

---

## 2. Preparing a Slide Manifest

### Option A: GDC Portal (Recommended)

1. Go to the GDC Portal
2. Filter:
   - Project: TCGA-XXXX
   - Data Category: Biospecimen
   - Data Type: Slide Image
3. Add all files to cart
4. Download the manifest

## 3. Running the Download

### Phase 1. Install GDC Data Transfer Tool


1. Download the latest version from here: https://gdc.cancer.gov/access-data/gdc-data-transfer-tool
2. Move to a directory in your PATH
3. Verify installation: cmd: gdc-client --version



### Phase 2: Download Metadata

**Goal**: Download all small metadata files that describe the available data.


This includes information about ALL files available for download.


We can download the metadata of specific cases by following these steps:
1. Go to: https://portal.gdc.cancer.gov
2. Select "Repository": https://portal.gdc.cancer.gov/analysis_page?app=Downloads
3. Expand the cases and select TCGA program
4. After that you can select any project type (eg,. BRCA, LUAD,...)
5. Now the number of cases are filtered to the selection we did.
6. Form left panel we need to filter and choose the type of data we need from the shown categories (Experimental Strategy, Wgs Coverage, Data Category, Data Type, Data Format, Workflow Type, ...)
7. For downloading Download slides (.svs), In Experimental Strategy we choose Diagnostic Slide. (Optional File Format: SVS)
8. Download Manifest file for the selected data.
9. Save as (for example): D:\TCGA_Projects\TCGA-BRCA\manifest_brca_slides.txt


### Phase 3: Download slides (.svs) with gdc-client
1. Extract and save the downloaded GDC Data Transfer Tool in the location you want to save the slides in.
2. Open the terminal in the same location and write the command:
gdc-client download -m D:\TCGA_Projects\TCGA-BRCA\manifest_brca_slides.txt  -d D:\TCGA_Projects\TCGA-BRCA\raw_gdc
-   -m >> manifest
-   -d >> save directory 
3. Directory structure created by gdc-client:
After (or during) download, raw_gdc will look like:

D:\TCGA_Projects\TCGA-BRCA\raw_gdc\
    b201cdba-9dbd-4a5d-b507-d1acd9aeecb5\
        b201cdba-9dbd-4a5d-b507-d1acd9aeecb5.log
        TCGA-B2-4099-01A-02-BS2.cda80782-5212-4aef-80dc-abebaa70621e.svs.partial
    3e482a11-...\
        3e482a11-....log
        TCGA-...something.svs.partial
    ...
4. Key points:
-   Each file UUID (e.g. b201cdba-9dbd-4a5d-b507-d1acd9aeecb5) gets its own folder.
-   Inside each folder:
-   A *.log file with transfer logs.
-   The actual slide file:
- While downloading: *.svs.partial
- Once complete: *.svs (the .partial suffix disappears).

5. Verify completion: Ensure that:
-   No files are reported as missing or corrupted.
-   There are no *.partial files left.
-   If .partial remains, the download was interrupted; re-run gdc-client download with the same manifest and directory, it will resume.
-   At this point, all slides are present in raw_gdc in the official GDC structure.
