import os, random
import numpy as np, pandas as pd
from multiprocessing import Pool
from process import process_file

RAW = "data/raw"

def get_files(n=None, seed=0):
    """Files from the 2020-2022 list that are already downloaded."""
    with open(f"{RAW}/filelist_2022.txt") as f:
        paths = [f"{RAW}/mirror/dac/{line.strip()}" for line in f if line.strip()]
    paths = [p for p in paths if os.path.exists(p)]
    if n is not None and n < len(paths):
        random.Random(seed).shuffle(paths)   # fixed seed: same files every run
        paths = sorted(paths[:n])
    return paths

def process_chunk(files):
    parts = [p for f in files if (p := process_file(f)) is not None]
    return pd.concat(parts, ignore_index=True) if parts else None

def chunked(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]

def _join(parts):
    return pd.concat([p for p in parts if p is not None], ignore_index=True)

def run_serial(files):
    return process_chunk(files)

def run_mp(files, n, chunk=100):
    with Pool(n) as pool:
        return _join(pool.map(process_chunk, chunked(files, chunk), chunksize=1))

def run_dask(files, n, chunk=100):
    import dask
    tasks = [dask.delayed(process_chunk)(c) for c in chunked(files, chunk)]
    return _join(dask.compute(*tasks, scheduler="processes", num_workers=n))

def summarize(df):
    """Monthly mean T and S per 5-degree box and depth bin."""
    bins = [0, 50, 200, 500, 1000, 2100]
    labels = ["0-50", "50-200", "200-500", "500-1000", "1000-2100"]
    d = df.assign(
        month=df.time.dt.to_period("M").astype(str),
        lat_box=(np.floor(df.lat / 5) * 5).astype(int),
        lon_box=(np.floor(df.lon / 5) * 5).astype(int),
        depth_bin=pd.cut(df.pres, bins=bins, labels=labels, right=False),
    )
    return (d.groupby(["month", "lat_box", "lon_box", "depth_bin"], observed=True)
              .agg(temp_mean=("temp", "mean"), psal_mean=("psal", "mean"),
                   n_obs=("temp", "size"), n_profiles=("file", "nunique"))
              .reset_index())
