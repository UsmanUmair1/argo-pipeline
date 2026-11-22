import time
from pipeline import *

files = get_files(500)
print("files:", len(files))
for name, fn in [("serial", lambda: run_serial(files)),
                 ("mp x4", lambda: run_mp(files, 4)),
                 ("dask x4", lambda: run_dask(files, 4))]:
    t0 = time.perf_counter()
    df = fn()
    print(f"{name:8s} {time.perf_counter() - t0:6.1f}s  rows={len(df)}  temp_sum={df.temp.sum():.3f}")
s = summarize(df)
print(s.head()); print("summary rows:", len(s))
