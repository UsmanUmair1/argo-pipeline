import sys
import pandas as pd
import plotly.express as px
from ingest import summarize_parquet

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "data/processed/test_tmp"
    s = summarize_parquet(src) if not src.endswith(".parquet") else pd.read_parquet(src)
    s["depth_bin"] = s["depth_bin"].astype(str)
    order = ["0-50", "50-200", "200-500", "500-1000", "1000-2100"]
    s = s.sort_values("month")

    fig = px.scatter(
        s, x="lon_box", y="lat_box", color="temp_mean", animation_frame="month",
        facet_col="depth_bin", facet_col_wrap=3, category_orders={"depth_bin": order},
        color_continuous_scale="RdYlBu_r", range_color=[s.temp_mean.min(), s.temp_mean.max()],
        labels={"lon_box": "Longitude (box start)", "lat_box": "Latitude (box start)",
                "temp_mean": "Mean temp (C)"},
        title="Mean temperature by 5-degree box and depth bin (dbar)")
    fig.update_traces(marker=dict(symbol="square", size=14))
    fig.write_html("results/dashboard_map.html")

    ts = (s.assign(w=s.temp_mean * s.temp_n)
            .groupby(["month", "depth_bin"]).agg(w=("w", "sum"), n=("temp_n", "sum")).reset_index())
    ts["temp"] = ts.w / ts.n
    fig2 = px.line(ts, x="month", y="temp", color="depth_bin",
                   category_orders={"depth_bin": order},
                   labels={"temp": "Mean temp (C)"},
                   title="Monthly mean temperature by depth bin")
    fig2.write_html("results/dashboard_timeseries.html")
    print("saved results/dashboard_map.html and results/dashboard_timeseries.html")

if __name__ == "__main__":
    main()
