import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

t = pd.read_csv("results/timings.csv")
med = t.groupby(["backend", "workers"]).seconds.median().reset_index()
base = med[(med.backend == "serial")].seconds.iloc[0]
med["speedup"] = base / med.seconds
med["efficiency"] = med.speedup / med.workers
print(f"serial baseline: {base:.1f} s")
print(med.to_string(index=False))
med.to_csv("results/speedup_table.csv", index=False)

fig, ax = plt.subplots(figsize=(6, 4.5))
for b, g in med[med.backend != "serial"].groupby("backend"):
    ax.plot(g.workers, g.speedup, marker="o", label=b)
ax.plot([1, 8], [1, 8], "k--", lw=1, label="ideal")
ax.set_xlabel("workers (CPU cores)"); ax.set_ylabel("speedup vs serial")
ax.set_title("Argo ingest speedup (median of 3 runs)"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("results/speedup.png", dpi=150)
print("saved results/speedup.png")
