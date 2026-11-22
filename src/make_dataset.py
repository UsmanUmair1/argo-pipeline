import time, json
from pipeline import get_files
from ingest import run_ingest, summarize_parquet

def main():
    with open("data/raw/filelist_2022.txt") as f:
        listed = sum(1 for line in f if line.strip())
    files = get_files()
    print(f"files listed: {listed} | on disk: {len(files)}", flush=True)
    t0 = time.perf_counter()
    rows = run_ingest(files, 4, "data/processed/profiles", "mp")
    t_ingest = time.perf_counter() - t0
    s = summarize_parquet("data/processed/profiles")
    s.to_parquet("data/processed/monthly_summary.parquet", index=False)
    s.to_csv("data/processed/monthly_summary.csv", index=False)
    stats = {"files_listed": listed, "files_processed": len(files), "rows": rows,
             "summary_rows": len(s), "ingest_seconds_4_workers": round(t_ingest, 1)}
    json.dump(stats, open("results/dataset_stats.json", "w"), indent=2)
    print(stats)

if __name__ == "__main__":
    main()
