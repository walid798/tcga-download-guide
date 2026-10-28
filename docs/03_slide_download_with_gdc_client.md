# 03 · Downloading Slides with the GDC Data Transfer Tool

Whole-slide images are large (hundreds of MB to several GB each). Use the official **GDC Data Transfer Tool** (`gdc-client`): it resumes interrupted downloads and checks each file's md5 checksum automatically.

---

## 1. Install `gdc-client`

1. Download it for your OS: [https://gdc.cancer.gov/access-data/gdc-data-transfer-tool](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)
2. Unzip it and put the executable in a folder on your `PATH`.
3. Check the installation:

```bash
gdc-client --version
```

> The tool can live anywhere; the download location is set with `-d`.

---

## 2. Download

```bash
gdc-client download -m manifests/gdc_manifest_TCGA-BRCA_slides.txt  -d raw_gdc/ -n 4 --retry-amount 5
```

| Option               | Meaning                                         |
| -------------------- | ----------------------------------------------- |
| `-m`               | Manifest file                                   |
| `-d`               | Output directory                                |
| `-n`               | Number of parallel connections                  |
| `--retry-amount`   | Retries per failed file                         |
| `--no-annotations` | Do not save annotation files next to each slide |

Windows example:

```powershell
gdc-client download -m D:\TCGA_Projects\TCGA-BRCA\manifests\gdc_manifest_TCGA-BRCA_slides.txt -d D:\TCGA_Projects\TCGA-BRCA\raw_gdc
```

---

## 3. What `raw_gdc/` looks like

```text
raw_gdc/
├── 5e92f89e-5470-4f37-9002-0bb397e7281b/
│   ├── 5e92f89e-5470-4f37-9002-0bb397e7281b.log
│   └── TCGA-E9-A1N9-01Z-00-DX1.982C83A6-0E06-47B3-A7C7-1773A2CD1771.svs
├── d46167af-6c29-49c7-95cf-3a801181aca4/
│   ├── d46167af-6c29-49c7-95cf-3a801181aca4.log
│   └── TCGA-3C-AALI-01Z-00-DX1.F6E9A5DF-D8FB-45CF-B4BD-C6B76294C291.svs.partial   ← still downloading
└── ...
```

- One folder per **file UUID**.
- While downloading, the slide ends with `.svs.partial`; when complete, `.partial` is removed.
- Some folders may also contain an `annotations.txt` file.

---

## 4. Verify the download

`gdc-client` has **no separate `verify` command**. Integrity is checked during download:

1. **Re-run the same command.** Completed files are skipped and `.partial` files resume.
   Repeat until the run reports no failures.
2. **Check that no `.partial` files remain:**
   ```bash
   python scripts/S02_index_raw_slides.py          # reports any *.partial files
   ```
3. *(Optional)* **Re-check md5 checksums** against the metadata:
   ```bash
   python scripts/S02_index_raw_slides.py --md5    # slow: reads every file
   ```

---

## 5. Troubleshooting

### "Can't move files" on Windows

`gdc-client` may write into a temporary folder on `C:` first and then move the file. If `C:` is full or the TEMP folder is locked, the move fails. Point TEMP to the target drive for the current PowerShell session, then run `gdc-client` from **the same window**:

```powershell
mkdir D:\TempTCGA -Force | Out-Null
$env:TEMP = "D:\TempTCGA"
$env:TMP  = "D:\TempTCGA"
gdc-client download -m manifest.txt -d D:\TCGA_Projects\TCGA-BRCA\raw_gdc
```

### Other common issues

| Problem                      | Fix                                                                 |
| ---------------------------- | ------------------------------------------------------------------- |
| Download stops or times out  | Re-run the same command; it resumes                                 |
| Disk fills up                | Check total size first (sum of the `size` column in the manifest) |
| Controlled-access files fail | Slides are open access; controlled data need `-t token.txt`       |

Next: [04 · Post-download organization](04_post_download_organization.md)
