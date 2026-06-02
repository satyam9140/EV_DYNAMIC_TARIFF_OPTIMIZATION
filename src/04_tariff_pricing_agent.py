import json
import numpy as np
import pandas as pd
from config import REPORT_DIR, BASE_TARIFF_INR, MIN_TARIFF_INR, MAX_TARIFF_INR, SURGE_UTIL_THRESHOLD, DISCOUNT_UTIL_THRESHOLD


def tariff_formula(row):
    util = row["predicted_utilization_rate"]
    peak = row["is_peak_hour"]
    offpeak = 1 if util < DISCOUNT_UTIL_THRESHOLD else 0
    congestion = 1 if util > SURGE_UTIL_THRESHOLD else 0

    multiplier = 1 + 0.35 * util + 0.15 * peak + 0.20 * congestion - 0.18 * offpeak
    tariff = BASE_TARIFF_INR * multiplier
    return float(np.clip(tariff, MIN_TARIFF_INR, MAX_TARIFF_INR))


def pricing_label(row):
    if row["predicted_utilization_rate"] > SURGE_UTIL_THRESHOLD:
        return "SURGE_PRICE"
    if row["predicted_utilization_rate"] < DISCOUNT_UTIL_THRESHOLD:
        return "DISCOUNT_PRICE"
    return "NORMAL_DYNAMIC_PRICE"


def run_tariff_agent():
    pred_path = REPORT_DIR / "demand_predictions.csv"
    if not pred_path.exists():
        raise FileNotFoundError("Run 03_demand_prediction_agent.py before tariff pricing agent.")

    df = pd.read_csv(pred_path)
    df["dynamic_tariff_inr"] = df.apply(tariff_formula, axis=1)
    df["pricing_action"] = df.apply(pricing_label, axis=1)

    elasticity = -0.25
    price_change_ratio = (df["dynamic_tariff_inr"] - BASE_TARIFF_INR) / BASE_TARIFF_INR
    df["elasticity_adjusted_volume"] = df["predicted_demand_volume"] * (1 + elasticity * price_change_ratio)
    df["elasticity_adjusted_volume"] = df["elasticity_adjusted_volume"].clip(lower=0)

    df["old_revenue_fixed_tariff"] = df["predicted_demand_volume"] * BASE_TARIFF_INR
    df["new_revenue_dynamic_tariff"] = df["elasticity_adjusted_volume"] * df["dynamic_tariff_inr"]
    df["revenue_gain"] = df["new_revenue_dynamic_tariff"] - df["old_revenue_fixed_tariff"]
    df["revenue_gain_pct"] = 100 * df["revenue_gain"] / df["old_revenue_fixed_tariff"].replace(0, np.nan)

    df["post_pricing_utilization_rate"] = (df["elasticity_adjusted_volume"] / df["capacity"].replace(0, np.nan)).clip(0, 2)
    df["post_pricing_congestion"] = (df["post_pricing_utilization_rate"] >= SURGE_UTIL_THRESHOLD).astype(int)
    df["post_pricing_queue_proxy"] = (df["post_pricing_utilization_rate"] - 1).clip(lower=0) * df["capacity"]

    output_path = REPORT_DIR / "dynamic_tariff_decisions.csv"
    df.to_csv(output_path, index=False)

    summary = {
        "average_dynamic_tariff_inr": float(df["dynamic_tariff_inr"].mean()),
        "average_revenue_gain_pct": float(df["revenue_gain_pct"].replace([np.inf, -np.inf], np.nan).mean()),
        "total_fixed_revenue": float(df["old_revenue_fixed_tariff"].sum()),
        "total_dynamic_revenue": float(df["new_revenue_dynamic_tariff"].sum()),
        "surge_actions": int((df["pricing_action"] == "SURGE_PRICE").sum()),
        "discount_actions": int((df["pricing_action"] == "DISCOUNT_PRICE").sum()),
        "normal_actions": int((df["pricing_action"] == "NORMAL_DYNAMIC_PRICE").sum()),
    }

    with open(REPORT_DIR / "tariff_pricing_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print(f"Saved tariff decisions to: {output_path}")
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    run_tariff_agent()
