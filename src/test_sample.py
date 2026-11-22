import glob, time
import pandas as pd
from process import process_file

files = sorted(glob.glob("data/raw/mirror/**/*.nc", recursive=True))[:300]
t0 = time.perf_counter()
parts = [p for f in files if (p := process_file(f)) is not None]
df = pd.concat(parts, ignore_index=True)
print("files used:", len(parts), "of", len(files))
print("rows:", len(df), "| seconds:", round(time.perf_counter() - t0, 2))
print(df.describe().T[["count", "min", "max"]])
print(df.head())
