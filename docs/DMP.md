# Data Management Plan

**Project:** Parallel processing and open publication of Argo ocean profile data
**Author:** Usman Umair, UPN Veteran Jawa Timur    **Date:** 2026-11-22    **Version:** 1.0

## 1. Data description
- **Source data:** Argo float profile files (NetCDF), temperature, salinity and pressure,
  from the Argo GDAC (data-argo.ifremer.fr). Region: 30S-30N, 40E-120E. Period: 2022.
  Retrieved on 2026-11-22. Profile index file: ar_index_global_prof.txt (retrieved 2026-11-22).
- **Derived data (published):**
  1. Cleaned profile observations in Parquet format (one row per measurement level).
  2. Monthly summary table: mean temperature and salinity per month, 5-degree box and depth bin.
- **Expected volume:** raw about 0.81 GB (11,633 NetCDF files) (not published); derived about 66 MB as Parquet (55.9 MB as uploaded to Zenodo).

## 2. Storage and backup
- Working copy: Linux (WSL2) home folder on a local drive.
- Code: Git repository on GitHub. Derived data: Zenodo (archived copy).
- Backup: code is versioned on GitHub; the final dataset is archived on Zenodo. Raw data is not backed up separately, because it can be re-downloaded from the Argo GDAC.

## 3. Organisation and naming
- Folders: data/raw, data/processed, src, results, docs.
- Parquet parts: part-00000.parquet, part-00001.parquet, ...
- Released files: argo_indian_ocean_2022_profiles_v1.0 and ..._monthly_summary_v1.0.
- Versioning: Git tags for code; Zenodo version numbers for data.

## 4. Documentation and metadata
- README with the pipeline description, how to reproduce, and column definitions with units.
- Quality control rule: only values with Argo QC flag 1 or 2; adjusted values preferred over raw.
- Provenance recorded: file list, retrieval date, software versions (requirements.txt), Git commit.
- Zenodo metadata: title, description, authors, keywords, licence, related identifiers (GitHub, Argo).

## 5. Legal and ethical
- No personal data. Argo data is free to use; credit is required (see Argo data policy).
- Derived data licence: CC BY 4.0 for the processed dataset (Argo data are free to use without restriction; acknowledgement requested). Code: MIT.
- Required acknowledgement: the Argo acknowledgement sentence and DOI (https://doi.org/10.17882/42182) are given in the README and in the Zenodo record.

## 6. Sharing and preservation
- Published on Zenodo on 2026-11-23: https://doi.org/10.5281/zenodo.24452166 (v1.0). Code is on GitHub and linked from the Zenodo record.
- Retention: Zenodo keeps the published record long-term. Local raw data is deleted once the dataset is published and verified; code and processed data stay in the repository and on Zenodo.
- Access: open, no restrictions.

## 7. Responsibilities
- Usman Umair: data processing, documentation, deposit.

