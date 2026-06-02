import pandas as pd
import matplotlib.pyplot as plt
from config import PROCESSED_DIR, FIGURE_DIR, REPORT_DIR


def load_processed() -> pd.DataFrame:
    parquet_path = PROCESSED_DIR / "urbanev_processed.parquet"
    csv_path = PROCESSED_DIR / "urbanev_processed.csv"
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)
    return pd.read_csv(csv_path, parse_dates=["datetime"])


def save_plot(fig, name: str):
    path = FIGURE_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved figure: {path}")


def run_eda():
    df = load_processed()
    df["datetime"] = pd.to_datetime(df["datetime"])

    print("Creating hourly demand trend...")
    hourly = df.groupby(df["datetime"].dt.floor("h"))["volume"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(hourly["datetime"], hourly["volume"])
    ax.set_title("Total EV Charging Demand Over Time")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Charging Volume")
    save_plot(fig, "01_total_demand_trend.png")

    print("Creating intraday demand profile...")
    intraday = df.groupby("hour")[["volume", "utilization_rate"]].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(intraday["hour"], intraday["volume"], marker="o")
    ax.set_title("Average Demand by Hour of Day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Charging Volume")
    save_plot(fig, "02_intraday_demand.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(intraday["hour"], intraday["utilization_rate"], marker="o")
    ax.axhline(0.80, linestyle="--", label="Surge threshold 80%")
    ax.axhline(0.30, linestyle="--", label="Discount threshold 30%")
    ax.set_title("Average Utilization by Hour of Day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Utilization Rate")
    ax.legend()
    save_plot(fig, "03_intraday_utilization.png")

    print("Creating top overloaded stations plot...")
    station_summary = df.groupby("station_id").agg(
        avg_utilization=("utilization_rate", "mean"),
        avg_queue_proxy=("queue_length_proxy", "mean"),
        total_volume=("volume", "sum"),
    ).reset_index()
    top = station_summary.sort_values("avg_utilization", ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(top["station_id"], top["avg_utilization"])
    ax.set_title("Top 20 Overloaded Stations by Average Utilization")
    ax.set_xlabel("Station/Grid ID")
    ax.set_ylabel("Average Utilization")
    ax.tick_params(axis="x", rotation=70)
    save_plot(fig, "04_top_overloaded_stations.png")

    print("Saving station summary...")
    station_summary.to_csv(REPORT_DIR / "station_level_eda_summary.csv", index=False)
    intraday.to_csv(REPORT_DIR / "hourly_behavior_summary.csv", index=False)


if __name__ == "__main__":
    run_eda()
