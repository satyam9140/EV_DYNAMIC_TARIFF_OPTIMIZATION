import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from config import RAW_DIR, PROCESSED_DIR


def read_csv_file(name: str) -> pd.DataFrame:
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return pd.read_csv(path)


def build_timestamp_table() -> pd.DataFrame:
    time_df = read_csv_file("time.csv")
    time_df = time_df.copy()
    time_df["timestamp"] = np.arange(1, len(time_df) + 1)
    time_df["datetime"] = pd.to_datetime(
        dict(
            year=time_df["year"],
            month=time_df["month"],
            day=time_df["day"],
            hour=time_df["hour"],
            minute=time_df["minute"],
            second=time_df["second"],
        ),
        errors="coerce",
    )
    time_df["date"] = time_df["datetime"].dt.date.astype(str)
    time_df["hour"] = time_df["datetime"].dt.hour
    time_df["dayofweek"] = time_df["datetime"].dt.dayofweek
    time_df["is_weekend"] = time_df["dayofweek"].isin([5, 6]).astype(int)
    time_df["is_peak_hour"] = time_df["hour"].isin([8, 9, 10, 17, 18, 19, 20]).astype(int)
    return time_df[["timestamp", "datetime", "date", "hour", "dayofweek", "is_weekend", "is_peak_hour"]]


def wide_to_long(file_name: str, value_name: str) -> pd.DataFrame:
    df = read_csv_file(file_name)
    id_col = "timestamp"
    station_cols = [c for c in df.columns if c != id_col]
    long_df = df.melt(id_vars=id_col, value_vars=station_cols, var_name="station_id", value_name=value_name)
    long_df["station_id"] = long_df["station_id"].astype(str)
    return long_df


def preprocess_urbanev() -> pd.DataFrame:
    print("Building timestamp table...")
    time_df = build_timestamp_table()

    print("Melting wide time-series files into long format...")
    volume = wide_to_long("volume.csv", "volume")
    occupancy = wide_to_long("occupancy.csv", "occupancy")
    duration = wide_to_long("duration.csv", "duration")
    price = wide_to_long("price.csv", "raw_price")

    print("Merging volume, occupancy, duration, and price...")
    df = volume.merge(occupancy, on=["timestamp", "station_id"], how="left")
    df = df.merge(duration, on=["timestamp", "station_id"], how="left")
    df = df.merge(price, on=["timestamp", "station_id"], how="left")
    df = df.merge(time_df, on="timestamp", how="left")

    print("Adding station/grid metadata...")
    info = read_csv_file("information.csv")
    info["station_id"] = info["grid"].astype(str)
    keep_cols = ["station_id", "count", "fast_count", "slow_count", "area", "lon", "la", "CBD", "dynamic_pricing"]
    df = df.merge(info[keep_cols], on="station_id", how="left")

    print("Engineering operational features...")
    df["capacity"] = df["count"].replace(0, np.nan)
    df["utilization_rate"] = df["occupancy"] / df["capacity"]
    df["utilization_rate"] = df["utilization_rate"].replace([np.inf, -np.inf], np.nan).clip(lower=0, upper=2)
    df["queue_length_proxy"] = (df["occupancy"] - df["capacity"]).clip(lower=0)
    df["congestion_probability_proxy"] = (df["utilization_rate"] >= 0.80).astype(int)
    df["off_peak_low_utilization"] = (df["utilization_rate"] < 0.30).astype(int)
    df["baseline_tariff_inr"] = 15.0
    df["baseline_revenue"] = df["volume"] * df["baseline_tariff_inr"]
    df["energy_cost_proxy"] = df["raw_price"]
    df["revenue_per_capacity"] = df["baseline_revenue"] / df["capacity"]

    print("Handling missing values...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df.groupby("station_id")[numeric_cols].transform(lambda x: x.fillna(x.median()))
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    output_path = PROCESSED_DIR / "urbanev_processed.parquet"
    try:
        df.to_parquet(output_path, index=False)
    except Exception:
        output_path = PROCESSED_DIR / "urbanev_processed.csv"
        df.to_csv(output_path, index=False)

    print(f"Saved processed UrbanEV data to: {output_path}")
    return df


def preprocess_acn() -> pd.DataFrame:
    path = RAW_DIR / "acndata_sessions.json.xlsx"
    if not path.exists():
        print("ACN file not found. Skipping ACN preprocessing.")
        return pd.DataFrame()

    print("Reading ACN session file...")
    acn = pd.read_excel(path)
    acn = acn.dropna(how="all")

    for col in ["connectionTime", "disconnectTime", "doneChargingTime"]:
        if col in acn.columns:
            acn[col] = pd.to_datetime(acn[col], errors="coerce")

    if {"connectionTime", "disconnectTime"}.issubset(acn.columns):
        acn["session_duration_hours"] = (
            acn["disconnectTime"] - acn["connectionTime"]
        ).dt.total_seconds() / 3600

    if {"kWhDelivered", "session_duration_hours"}.issubset(acn.columns):
        acn["avg_power_kw"] = acn["kWhDelivered"] / acn["session_duration_hours"].replace(0, np.nan)

    output_path = PROCESSED_DIR / "acn_sessions_processed.csv"
    acn.to_csv(output_path, index=False)
    print(f"Saved processed ACN data to: {output_path}")
    return acn


if __name__ == "__main__":
    preprocess_urbanev()
    preprocess_acn()
