import os, shutil, glob
import numpy as np, pandas as pd
from pipeline import chunked, process_chunk

def ingest_chunk(task):
    """Process a chunk of files and write one Parquet part. Returns row count."""
    i, files, outdir = task
    df = process_chunk(files)
    if df is None:
        return 0
    df["file"] = df["file"].astype("category")
    for c in ["pres", "temp", "psal", "lat", "lon"]:
        df[c] = df[c].astype("float32")
    df.to_parquet(f"{outdir}/part-{i:05d}.parquet", index=False)
    return len(df)

def run_ingest(files, n, outdir, backend="mp", chunk=200):
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    tasks = [(i, c, outdir) for i, c in enumerate(chunked(files, chunk))]
    if backend == "serial":
        counts = [ingest_chunk(t) for t in tasks]
    elif backend == "mp":
        from multiprocessing import Pool
        with Pool(n) as pool:
            counts = pool.map(ingest_chunk, tasks, chunksize=1)
    elif backend == "dask":
        import dask
        dask.config.set({"multiprocessing.context": "fork"})  # avoids re-importing in each worker
        counts = dask.compute(*[dask.delayed(ingest_chunk)(t) for t in tasks],
                              scheduler="processes", num_workers=n)
    else:
        raise ValueError(backend)
    return sum(counts)

def summarize_parquet(outdir):
    """Monthly mean T and S per 5-degree box and depth bin, one part at a time (low memory)."""
    bins = [0, 50, 200, 500, 1000, 2100]
    labels = ["0-50", "50-200", "200-500", "500-1000", "1000-2100"]
    partials = []
    for p in sorted(glob.glob(f"{outdir}/part-*.parquet")):
        d = pd.read_parquet(p)
        d["file"] = d["file"].astype(str)
        d["month"] = d.time.dt.to_period("M").astype(str)
        d["lat_box"] = (np.floor(d.lat / 5) * 5).astype(int)
        d["lon_box"] = (np.floor(d.lon / 5) * 5).astype(int)
        d["depth_bin"] = pd.cut(d.pres, bins=bins, labels=labels, right=False)
        g = d.groupby(["month", "lat_box", "lon_box", "depth_bin"], observed=True)
        partials.append(g.agg(temp_sum=("temp", "sum"), temp_n=("temp", "count"),
                              psal_sum=("psal", "sum"), psal_n=("psal", "count"),
                              n_profiles=("file", "nunique")).reset_index())
    t = pd.concat(partials).groupby(["month", "lat_box", "lon_box", "depth_bin"], observed=True).sum().reset_index()
    t["temp_mean"] = t.temp_sum / t.temp_n
    t["psal_mean"] = t.psal_sum / t.psal_n.where(t.psal_n > 0)
    return t.drop(columns=["temp_sum", "psal_sum"])
