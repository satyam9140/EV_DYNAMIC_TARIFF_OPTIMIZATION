import json
import pandas as pd
from config import REPORT_DIR, SURGE_UTIL_THRESHOLD, DISCOUNT_UTIL_THRESHOLD


def run_monitoring_agent():
    path = REPORT_DIR / "dynamic_tariff_decisions.csv"
    if not path.exists():
        raise FileNotFoundError("Run 04_tariff_pricing_agent.py first.")

    df = pd.read_csv(path)

    before_congestion_rate = (df["predicted_utilization_rate"] >= SURGE_UTIL_THRESHOLD).mean()
    after_congestion_rate = (df["post_pricing_utilization_rate"] >= SURGE_UTIL_THRESHOLD).mean()

    before_queue = df["queue_length_proxy"].mean()
    after_queue = df["post_pricing_queue_proxy"].mean()

    off_peak_before = df[df["predicted_utilization_rate"] < DISCOUNT_UTIL_THRESHOLD]["predicted_demand_volume"].mean()
    off_peak_after = df[df["predicted_utilization_rate"] < DISCOUNT_UTIL_THRESHOLD]["elasticity_adjusted_volume"].mean()
    off_peak_uplift_pct = 100 * (off_peak_after - off_peak_before) / off_peak_before if off_peak_before else 0

    pricing_efficiency_before = df["old_revenue_fixed_tariff"].sum() / df["predicted_demand_volume"].sum()
    pricing_efficiency_after = df["new_revenue_dynamic_tariff"].sum() / df["elasticity_adjusted_volume"].sum()

    metrics = {
        "total_fixed_revenue": float(df["old_revenue_fixed_tariff"].sum()),
        "total_dynamic_revenue": float(df["new_revenue_dynamic_tariff"].sum()),
        "overall_revenue_gain_pct": float(100 * (df["new_revenue_dynamic_tariff"].sum() - df["old_revenue_fixed_tariff"].sum()) / df["old_revenue_fixed_tariff"].sum()),
        "before_congestion_rate": float(before_congestion_rate),
        "after_congestion_rate": float(after_congestion_rate),
        "congestion_reduction_pct_points": float(100 * (before_congestion_rate - after_congestion_rate)),
        "average_waiting_time_proxy_before": float(before_queue),
        "average_waiting_time_proxy_after": float(after_queue),
        "average_waiting_time_proxy_reduction_pct": float(100 * (before_queue - after_queue) / before_queue) if before_queue else 0,
        "off_peak_uplift_pct": float(off_peak_uplift_pct),
        "pricing_efficiency_before_revenue_per_kwh": float(pricing_efficiency_before),
        "pricing_efficiency_after_revenue_per_kwh": float(pricing_efficiency_after),
    }

    with open(REPORT_DIR / "monitoring_learning_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    station_policy = df.groupby("station_id").agg(
        avg_dynamic_tariff=("dynamic_tariff_inr", "mean"),
        avg_revenue_gain_pct=("revenue_gain_pct", "mean"),
        avg_post_utilization=("post_pricing_utilization_rate", "mean"),
        surge_count=("pricing_action", lambda x: (x == "SURGE_PRICE").sum()),
        discount_count=("pricing_action", lambda x: (x == "DISCOUNT_PRICE").sum()),
    ).reset_index()
    station_policy.to_csv(REPORT_DIR / "station_pricing_policy_summary.csv", index=False)

    print("Monitoring & Learning Agent Results:")
    print(json.dumps(metrics, indent=4))


if __name__ == "__main__":
    run_monitoring_agent()
