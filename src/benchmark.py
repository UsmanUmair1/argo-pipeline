import sys, time, csv, os
from pipeline import get_files
from ingest import run_ingest

OUT = "data/processed/bench_tmp"
REPEATS = 3

def main():
    n_files = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    files = get_files(n_files)
    print("files:", len(files), flush=True)
    os.makedirs("results", exist_ok=True)

    run_ingest(files, 1, OUT, "serial")          # warm-up (fills disk cache), not recorded
    configs = [("serial", 1)] + [(b, n) for b in ("mp", "dask") for n in (1, 2, 4, 8)]
    with open("results/timings.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["backend", "workers", "repeat", "files", "rows", "seconds"])
        for backend, n in configs:
            for r in range(REPEATS):
                t0 = time.perf_counter()
                rows = run_ingest(files, n, OUT, backend)
                dt = time.perf_counter() - t0
                w.writerow([backend, n, r, len(files), rows, round(dt, 2)]); f.flush()
                print(f"{backend:7s} n={n} run={r} {dt:7.1f}s rows={rows}", flush=True)

if __name__ == "__main__":
    main()
