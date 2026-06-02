import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from config import PROCESSED_DIR, REPORT_DIR, MODEL_DIR, RANDOM_STATE


def load_processed() -> pd.DataFrame:
    parquet_path = PROCESSED_DIR / "urbanev_processed.parquet"
    csv_path = PROCESSED_DIR / "urbanev_processed.csv"
    if parquet_path.exists():
        return pd.read_parquet(parquet_path)
    return pd.read_csv(csv_path, parse_dates=["datetime"])


def build_hourly_model_table(df: pd.DataFrame) -> pd.DataFrame:
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["hour_datetime"] = df["datetime"].dt.floor("h")

    hourly = df.groupby(["station_id", "hour_datetime"]).agg(
        demand_volume=("volume", "sum"),
        avg_occupancy=("occupancy", "mean"),
        avg_duration=("duration", "mean"),
        avg_raw_price=("raw_price", "mean"),
        utilization_rate=("utilization_rate", "mean"),
        queue_length_proxy=("queue_length_proxy", "mean"),
        capacity=("capacity", "max"),
        hour=("hour", "first"),
        dayofweek=("dayofweek", "first"),
        is_weekend=("is_weekend", "first"),
        is_peak_hour=("is_peak_hour", "first"),
        CBD=("CBD", "first"),
        dynamic_pricing=("dynamic_pricing", "first"),
    ).reset_index()

    hourly = hourly.sort_values(["station_id", "hour_datetime"])
    grouped = hourly.groupby("station_id")
    hourly["lag_1h_demand"] = grouped["demand_volume"].shift(1)
    hourly["lag_24h_demand"] = grouped["demand_volume"].shift(24)
    hourly["rolling_3h_demand"] = grouped["demand_volume"].shift(1).rolling(3).mean().reset_index(level=0, drop=True)
    hourly["rolling_24h_demand"] = grouped["demand_volume"].shift(1).rolling(24).mean().reset_index(level=0, drop=True)
    hourly["lag_1h_utilization"] = grouped["utilization_rate"].shift(1)
    hourly = hourly.dropna().reset_index(drop=True)
    return hourly


def train_agent():
    df = load_processed()
    hourly = build_hourly_model_table(df)
    hourly.to_csv(PROCESSED_DIR / "hourly_model_table.csv", index=False)

    feature_cols = [
        "avg_occupancy", "avg_duration", "avg_raw_price", "utilization_rate",
        "queue_length_proxy", "capacity", "hour", "dayofweek", "is_weekend",
        "is_peak_hour", "CBD", "dynamic_pricing", "lag_1h_demand",
        "lag_24h_demand", "rolling_3h_demand", "rolling_24h_demand",
        "lag_1h_utilization",
    ]
    target_col = "demand_volume"

    split_time = hourly["hour_datetime"].quantile(0.80)
    train_df = hourly[hourly["hour_datetime"] <= split_time].copy()
    test_df = hourly[hourly["hour_datetime"] > split_time].copy()

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]

    models = {
        "hist_gradient_boosting": HistGradientBoostingRegressor(random_state=RANDOM_STATE, max_iter=250),
        "random_forest": RandomForestRegressor(n_estimators=80, random_state=RANDOM_STATE, n_jobs=-1, max_depth=16),
    }

    results = {}
    best_name = None
    best_rmse = float("inf")
    best_model = None

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        pred = np.clip(pred, 0, None)
        mse = mean_squared_error(y_test, pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, pred)
        r2 = r2_score(y_test, pred)
        results[name] = {"RMSE": float(rmse), "MAE": float(mae), "R2": float(r2)}
        if rmse < best_rmse:
            best_rmse = rmse
            best_name = name
            best_model = model

    print(f"Best model: {best_name}")
    joblib.dump(best_model, MODEL_DIR / "demand_prediction_agent.joblib")

    test_df = test_df.copy()
    test_df["predicted_demand_volume"] = np.clip(best_model.predict(X_test), 0, None)
    test_df["predicted_utilization_rate"] = (test_df["predicted_demand_volume"] / test_df["capacity"].replace(0, np.nan)).clip(0, 2)
    test_df["predicted_congestion_probability"] = (test_df["predicted_utilization_rate"] >= 0.80).astype(float)
    test_df.to_csv(REPORT_DIR / "demand_predictions.csv", index=False)

    with open(REPORT_DIR / "demand_model_metrics.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Saved model, predictions, and metrics.")


if __name__ == "__main__":
    train_agent()
