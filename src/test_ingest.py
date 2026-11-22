import time
from pipeline import get_files
from ingest import run_ingest, summarize_parquet

def main():
    files = get_files(500)
    print("files:", len(files))
    t0 = time.perf_counter()
    rows = run_ingest(files, 4, "data/processed/test_tmp", "mp")
    print("rows:", rows, "| seconds:", round(time.perf_counter() - t0, 1))
    print(summarize_parquet("data/processed/test_tmp").head())

if __name__ == "__main__":
    main()
