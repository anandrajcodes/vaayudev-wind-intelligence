
import pandas as pd
import numpy as np

# Load datasets
actuals = pd.read_csv("backend/wind_actuals_jan2026.csv")
forecasts = pd.read_csv("backend/wind_forecasts_jan2026.csv")
# Parse timestamps as UTC
actuals["startTime"] = pd.to_datetime(
    actuals["startTime"], utc=True
)
forecasts["startTime"] = pd.to_datetime(
    forecasts["startTime"], utc=True
)
forecasts["publishTime"] = pd.to_datetime(
    forecasts["publishTime"], utc=True
)

actuals["generation"] = pd.to_numeric(
    actuals["generation"], errors="coerce"
)
forecasts["generation"] = pd.to_numeric(
    forecasts["generation"], errors="coerce"
)

# Keep January 2026 actual delivery periods
start = pd.Timestamp("2026-01-01", tz="UTC")
end = pd.Timestamp("2026-02-01", tz="UTC")

actuals = actuals[
    (actuals["startTime"] >= start)
    & (actuals["startTime"] < end)
    & (actuals["fuelType"] == "WIND")
].copy()

forecasts = forecasts[
    (forecasts["startTime"] >= start)
    & (forecasts["startTime"] < end)
].copy()

# Aggregate two half-hourly actual records into hourly averages
actuals["hour"] = actuals["startTime"].dt.floor("h")

hourly_actuals = (
    actuals.groupby("hour")["generation"]
    .mean()
    .reset_index()
    .rename(columns={
        "hour": "startTime",
        "generation": "generation_actual"
    })
)

# Assumption: day-ahead purchasing decision cutoff is
# 12:00 UTC on the previous calendar day.
# This is a modelling assumption, not a verified market deadline.
forecasts["delivery_date"] = forecasts["startTime"].dt.floor("D")
forecasts["cutoff"] = (
    forecasts["delivery_date"]
    - pd.Timedelta(days=1)
    + pd.Timedelta(hours=12)
)

eligible = forecasts[
    forecasts["publishTime"] <= forecasts["cutoff"]
].copy()

# Latest forecast published by the cutoff for each delivery hour
latest = (
    eligible.sort_values("publishTime")
    .drop_duplicates(subset=["startTime"], keep="last")
    [["startTime", "generation", "publishTime"]]
    .rename(columns={
        "generation": "generation_forecast"
    })
)

# Match by hourly delivery start time
comparison = hourly_actuals.merge(
    latest,
    on="startTime",
    how="left"
)

comparison["error"] = (
    comparison["generation_forecast"]
    - comparison["generation_actual"]
)

valid = comparison.dropna(
    subset=["generation_actual", "generation_forecast"]
).copy()

print("Hourly actual periods:", len(hourly_actuals))
print("Matched forecast periods:", len(valid))
print(
    "Missing forecasts:",
    int(comparison["generation_forecast"].isna().sum())
)

if not valid.empty:
    errors = valid["error"]

    print("\nForecast accuracy metrics")
    print(f"MAE:  {errors.abs().mean():.2f}")
    print(f"RMSE: {np.sqrt((errors ** 2).mean()):.2f}")
    print(f"Bias: {errors.mean():.2f}")
else:
    print("No eligible forecasts found; metrics not calculated.")

comparison.to_csv(
    "wind_forecast_accuracy_jan2026.csv",
    index=False
)
print("\nSaved: wind_forecast_accuracy_jan2026.csv")
