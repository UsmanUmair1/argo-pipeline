import pandas as pd

idx = pd.read_csv("data/raw/ar_index_global_prof.txt", comment="#")
idx["date"] = pd.to_datetime(idx["date"].astype("Int64").astype(str),
                             format="%Y%m%d%H%M%S", errors="coerce")
idx = idx.dropna(subset=["date", "latitude", "longitude"])
print("total profiles in index:", len(idx))

# Indian Ocean + Indonesian seas (edit these to change the region/years)
LAT_MIN, LAT_MAX = -30, 30
LON_MIN, LON_MAX = 40, 120
START, END = "2018-01-01", "2023-01-01"

sel = idx[idx.latitude.between(LAT_MIN, LAT_MAX)
          & idx.longitude.between(LON_MIN, LON_MAX)
          & (idx.date >= START) & (idx.date < END)]
print("profiles in selection:", len(sel))
print(sel.groupby(sel.date.dt.year).size())

sel.file.to_csv("data/raw/filelist_all.txt", index=False, header=False)
sel.sample(300, random_state=0).file.to_csv("data/raw/filelist_sample.txt",
                                            index=False, header=False)
