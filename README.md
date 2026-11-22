# Parallel processing of Argo ocean profiles (Indian Ocean, 2022)

A Python pipeline that cleans Argo float temperature/salinity profiles, stores them as Parquet,
computes monthly regional summaries, and benchmarks serial vs. parallel processing
(multiprocessing and Dask) on an 8-core laptop under WSL2 (Ubuntu 24.04).

## Data
- Source: Argo GDAC (https://data-argo.ifremer.fr), core profile files (NetCDF).
- Region: 30S-30N, 40E-120E (Indian Ocean and Indonesian seas). Period: 2022.
- Retrieved: [DATE]. Profiles in selection: 11,633 (from the global profile index).
- Cleaning: adjusted values preferred over raw; only QC flags 1 and 2 kept; rows without pressure or temperature dropped.

## Pipeline
| Step | Script |
|---|---|
| Select profiles from the index | src/select_subset.py |
| Read and clean one profile file | src/process.py |
| Parallel ingest to Parquet, monthly summary | src/ingest.py, src/pipeline.py |
| Benchmark and plot | src/benchmark.py, src/plot_benchmark.py |
| Final dataset | src/make_dataset.py |
| Dashboard | src/dashboard.py |

## Benchmark
[TO FILL IN after the benchmark: sample size, serial time, speedup table, figure results/speedup.png, and a short explanation of the result.]

## Reproduce
Always run scripts from the project root.

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    # download the profile index and the files listed in data/raw/filelist_2022.txt
    python src/benchmark.py 10000
    python src/plot_benchmark.py
    python src/make_dataset.py

## Acknowledgement
[Check the exact Argo acknowledgement and DOI at argo.ucsd.edu and paste them here.]

## Licence
[Choose a licence for the code (for example MIT) and for the data (confirm against the Argo data policy).]
