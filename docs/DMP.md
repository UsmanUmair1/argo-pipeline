# Data Management Plan

**Project:** Parallel processing and open publication of Argo ocean profile data
**Author:** [Your name], [University]    **Date:** 2026-11-22    **Version:** 1.0

## 1. Data description
- **Source data:** Argo float profile files (NetCDF), temperature, salinity and pressure,
  from the Argo GDAC (data-argo.ifremer.fr). Region: 30S-30N, 40E-120E. Period: 2020-2022.
  Retrieved on [DATE]. Profile index file: ar_index_global_prof.txt (retrieved [DATE]).
- **Derived data (published):**
  1. Cleaned profile observations in Parquet format (one row per measurement level).
  2. Monthly summary table: mean temperature and salinity per month, 5-degree box and depth bin.
- **Expected volume:** raw about [X] GB (not published); derived about [Y] GB.

## 2. Storage and backup
- Working copy: Linux (WSL2) home folder on a local drive.
- Code: Git repository on GitHub. Derived data: Zenodo (archived copy).
- Raw data is not backed up, because it can be re-downloaded from the GDAC using the saved file list.
- Backup: [second copy, e.g. external drive or cloud storage], updated [after each major step].

## 3. Organisation and naming
- Folders: data/raw, data/processed, src, results, docs.
- Parquet parts: part-00000.parquet, part-00001.parquet, ...
- Released files: argo_indian_ocean_2020-2022_profiles_v1.0 and ..._monthly_summary_v1.0.
- Versioning: Git tags for code; Zenodo version numbers for data.

## 4. Documentation and metadata
- README with the pipeline description, how to reproduce, and column definitions with units.
- Quality control rule: only values with Argo QC flag 1 or 2; adjusted values preferred over raw.
- Provenance recorded: file list, retrieval date, software versions (requirements.txt), Git commit.
- Zenodo metadata: title, description, authors, keywords, licence, related identifiers (GitHub, Argo).

## 5. Legal and ethical
- No personal data. Argo data is free to use; credit is required (see Argo data policy).
- Derived data licence: [e.g. CC BY 4.0, confirm it is compatible with the Argo data policy].
- Required acknowledgement: check the exact wording on argo.ucsd.edu and cite the Argo DOI.

## 6. Sharing and preservation
- Published on Zenodo with a DOI after the pipeline is validated. Code archived via GitHub-Zenodo release.
- Retention: Zenodo keeps records long-term; local copies kept for [e.g. 5 years].
- Access: open, no restrictions.

## 7. Responsibilities
- [Your name]: data processing, documentation, deposit.
- [Supervisor, if any]: review before publication.
