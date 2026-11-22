## Data
- Source: Argo GDAC (https://data-argo.ifremer.fr), core profile files (NetCDF).
- Region: 30S-30N, 40E-120E (Indian Ocean and Indonesian seas). Period: 2022.
- Retrieved: 2026-11-22. Profiles selected from the global profile index: 11,633 (0.81 GB of NetCDF).
- Result: 11,253 files contributed rows; 380 files (3.3%) contributed none after filtering. The cleaned dataset has 8,332,260 rows (65 MB as Parquet).

**Cleaning rules**
- Adjusted values are preferred over raw values where available.
- Only values with Argo QC flag 1 (good) or 2 (probably good) are kept.
- Rows without pressure or temperature are dropped.
- Salinity outside 20 to 40 is set to missing. These bounds are my own plausibility check for this region, not an Argo standard. It affected 8,434 rows (0.10%), nearly all from float 1902198, whose salinity values of about 1.9 are physically implausible despite a good QC flag.

**Known limitations**
- 1,959,969 rows (23.5%) have no salinity. This is likely because some floats carry no salinity sensor, but I have not verified that.
- The monthly summary only uses pressure from 0 to 2100 dbar. 67,183 rows (0.8%) are deeper and 24 rows have a slightly negative pressure. They stay in the profile files but not in the summary.
- Summary bins: month, 5-degree latitude and longitude boxes, and depth bins 0-50, 50-200, 200-500, 500-1000, 1000-2100 dbar. Means are over all measurements in a bin, so floats with more levels weigh more.

**Columns (profile files)**
- pres: pressure (dbar); temp: temperature (degrees C); psal: practical salinity; time: UTC time of the profile; lat, lon: position (degrees); file: source file name.
