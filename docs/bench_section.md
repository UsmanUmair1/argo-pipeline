## Benchmark

**Setup.** A fixed random sample of 10,000 of the 11,633 profile files was ingested (read, cleaned, written to Parquet in chunks of 200 files). Hardware: laptop with 8 logical cores and 7.6 GB RAM, running Ubuntu 24.04 under WSL2, data on a local drive. Each setting was run 3 times after one untimed warm-up run, and the table shows the median. Every one of the 27 runs produced exactly 7,117,858 rows, so all methods give identical output.

| Method | Workers | Median time (s) | Speedup vs serial | Speedup vs own 1-worker run |
|---|---|---|---|---|
| serial | 1 | 511 | 1.0x | |
| multiprocessing | 1 | 419 | 1.2x | 1.0x |
| multiprocessing | 2 | 227 | 2.3x | 1.9x |
| multiprocessing | 4 | 147 | 3.5x | 2.8x |
| multiprocessing | 8 | 177 | 2.9x | 2.4x |
| Dask | 1 | 312 | 1.6x | 1.0x |
| Dask | 2 | 241 | 2.1x | 1.3x |
| Dask | 4 | 195 | 2.6x | 1.6x |
| Dask | 8 | 189 | 2.7x | 1.7x |

![Speedup](results/speedup.png)

**Findings.**
- Multiprocessing was fastest at 4 workers (about 2.8x faster than its own 1-worker run). At 8 workers it was slower than at 4 and the three repeats varied widely (119 to 194 s). The cause was not investigated. Possible explanations are that the 8 logical cores share fewer physical cores, that disk reads or the limited RAM are the bottleneck, or thermal throttling.
- Dask did not beat multiprocessing at any worker count in this setup.

**Limitations.**
- Run-to-run noise on this laptop is large. The three serial runs took 464, 511 and 538 s, and the 1-worker runs were faster than serial although they do the same work. The speedup vs serial is therefore uncertain by roughly 10 to 30%, and the speedup vs the method's own 1-worker run is the safer comparison.
- The benchmark was run before the salinity plausibility filter (see below) was added to the cleaning step. The filter is a cheap array operation, but the benchmark was not repeated with it.
- One machine, one dataset, one chunk size (200 files). Results may differ elsewhere.
