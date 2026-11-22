import numpy as np, pandas as pd, xarray as xr

def _qc_to_str(a):
    return np.array([q.decode() if isinstance(q, bytes) else str(q) for q in a])

def _clean(ds, var, i):
    """Prefer adjusted values; keep only QC flags 1 (good) and 2 (probably good)."""
    if var not in ds:
        return None
    val = ds[var].isel(N_PROF=i).values.astype(float)
    qc = _qc_to_str(ds[f"{var}_QC"].isel(N_PROF=i).values) if f"{var}_QC" in ds else None
    adj_name = f"{var}_ADJUSTED"
    if adj_name in ds and f"{adj_name}_QC" in ds:
        adj = ds[adj_name].isel(N_PROF=i).values.astype(float)
        adj_qc = _qc_to_str(ds[f"{adj_name}_QC"].isel(N_PROF=i).values)
        use = np.isfinite(adj)
        val = np.where(use, adj, val)
        qc = np.where(use, adj_qc, qc) if qc is not None else adj_qc
    if qc is None:
        return None
    return np.where(np.isin(qc, ["1", "2"]), val, np.nan)

def process_file(path):
    """One Argo profile file -> clean DataFrame (or None if unusable)."""
    try:
        with xr.open_dataset(path) as ds:
            frames = []
            for i in range(ds.sizes["N_PROF"]):
                pres = _clean(ds, "PRES", i)
                temp = _clean(ds, "TEMP", i)
                if pres is None or temp is None:
                    continue
                psal = _clean(ds, "PSAL", i)
                if psal is not None:
                    psal = np.where((psal < 20) | (psal > 40), np.nan, psal)
                df = pd.DataFrame({"pres": pres, "temp": temp,
                                   "psal": psal if psal is not None else np.nan})
                df["time"] = pd.Timestamp(ds["JULD"].values[i])
                df["lat"] = float(ds["LATITUDE"].values[i])
                df["lon"] = float(ds["LONGITUDE"].values[i])
                df["file"] = path.split("/")[-1]
                df = df.dropna(subset=["pres", "temp"])
                if len(df):
                    frames.append(df)
            return pd.concat(frames, ignore_index=True) if frames else None
    except Exception as e:
        print("FAILED", path, repr(e))
        return None
