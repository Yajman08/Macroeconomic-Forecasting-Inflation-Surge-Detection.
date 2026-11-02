"""
Build a combined monthly semiconductor/electronics forecasting dataset from FRED.

Run:
    pip install pandas
    python build_semiconductor_dataset.py

Outputs:
    semiconductor_electronics_forecasting_dataset.csv
    fred_raw/ individual downloaded series

Important:
- This creates a historical modeling dataset, not a real-time-vintage dataset.
- Verify each series ID and metadata on its FRED page before making research claims.
- Some IDs can be invalid or have sparse coverage. The script reports download errors
  rather than silently fabricating values.
"""

from pathlib import Path
from io import BytesIO
from urllib.request import Request, urlopen
import time
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "fred_raw"
RAW_DIR.mkdir(exist_ok=True)

# User-selected series. Verify IDs/definitions on their FRED series pages.
SERIES = {
    "PCU3344133441": "semiconductor_component_price_index",
    "IPG3344S": "semiconductor_industrial_production",
    "CAPUTLG3344S": "semiconductor_capacity_utilization",
    "PCU3344133344131": "integrated_circuit_package_price_index",
    "PCOPPUSDM": "copper_price_usd_per_metric_ton",
    "PCU3353133531": "electrical_equipment_producer_price_index",
}

def download_fred_series(series_id: str, column: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        raw = pd.read_csv(BytesIO(response.read()))

    # FRED CSV normally uses observation_date and the series ID as columns.
    if len(raw.columns) < 2:
        raise ValueError(f"Unexpected CSV format for {series_id}: {raw.columns.tolist()}")

    date_col = raw.columns[0]
    value_col = series_id if series_id in raw.columns else raw.columns[1]
    frame = raw[[date_col, value_col]].copy()
    frame.columns = ["date", column]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=["date"]).sort_values("date")
    frame = frame.drop_duplicates("date")

    frame.to_csv(RAW_DIR / f"{series_id}.csv", index=False)
    return frame

def main():
    frames = []
    failed = []

    for series_id, column in SERIES.items():
        try:
            print(f"Downloading {series_id} -> {column}")
            frames.append(download_fred_series(series_id, column))
            time.sleep(0.25)
        except Exception as exc:
            failed.append((series_id, str(exc)))
            print(f"FAILED {series_id}: {exc}")

    if not frames:
        raise RuntimeError(
            "No series downloaded. Check your internet connection and FRED series IDs."
        )

    # Outer join preserves all available dates. Different start dates/frequencies
    # can leave missing values; these are inspected below, not filled blindly.
    df = frames[0]
    for frame in frames[1:]:
        df = df.merge(frame, on="date", how="outer")

    df = df.sort_values("date").drop_duplicates("date")
    df = df.set_index("date").resample("MS").mean()

    # Monthly change features. Keep price-index levels as well as changes.
    target = "semiconductor_component_price_index"
    if target in df.columns:
        df["semiconductor_price_index_mom_pct"] = df[target].pct_change() * 100
        df["semiconductor_price_index_yoy_pct"] = df[target].pct_change(12) * 100
        # Predict the future price index 3 months ahead.
        df["target_price_index_3m_ahead"] = df[target].shift(-3)
        # Also provide a future YoY change target.
        df["target_price_index_yoy_3m_ahead"] = (
            df["semiconductor_price_index_yoy_pct"].shift(-3)
        )

    if "copper_price_usd_per_metric_ton" in df.columns:
        df["copper_price_mom_pct"] = (
            df["copper_price_usd_per_metric_ton"].pct_change() * 100
        )

    # Do not forward-fill here: that could hide different release frequencies
    # or create unrealistic observations. Preserve missing values for inspection.
    df = df.reset_index()
    output = BASE_DIR / "semiconductor_electronics_forecasting_dataset.csv"
    df.to_csv(output, index=False)

    print("\nSaved:", output)
    print("Shape:", df.shape)
    print("Date range:", df["date"].min(), "to", df["date"].max())
    print("\nMissing values by column:")
    print(df.isna().sum().to_string())
    print("\nColumns:")
    print(df.columns.tolist())

    if failed:
        print("\nSeries that failed to download:")
        for series_id, error in failed:
            print(f" - {series_id}: {error}")
        print(
            "\nThe output contains only successfully downloaded series. "
            "Check failed series IDs and rerun."
        )

if __name__ == "__main__":
    main()
