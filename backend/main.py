from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WindSight API",
    description="UK wind generation forecast analysis",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vaayudev-wind-intelligence.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "WindSight API is running",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/status")
def api_status():
    return {
        "app": "WindSight",
        "status": "running",
        "data_source": "Elexon BMRS",
        "period": "January 2026",
    }

@app.get("/api/chart-data")
def chart_data():
    csv_path = Path(__file__).parent / "wind_forecast_accuracy_jan2026.csv"

    if not csv_path.exists():
        return {"data": [], "message": "Analysis CSV not found"}

    df = pd.read_csv(csv_path)
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)

    df = df.dropna(
        subset=["generation_actual", "generation_forecast"]
    ).sort_values("startTime")

    # Return at most 168 hourly points (one week)


    data = []
    for _, row in df.iterrows():
        data.append({
            "time": row["startTime"].strftime("%d %b %H:%M"),
            "actual": round(float(row["generation_actual"]), 2),
            "forecast": round(float(row["generation_forecast"]), 2),
            "error": round(float(row["generation_forecast"])- float(row["generation_actual"]),2),
        })

    return {"data": data}

@app.get("/api/metrics")
def get_metrics():
    import pandas as pd
    from pathlib import Path

    csv_path = Path(__file__).parent / "wind_forecast_accuracy_jan2026.csv"

    if not csv_path.exists():
        return {"error": "Analysis CSV file not found"}

    df = pd.read_csv(csv_path)

    valid = df.dropna(subset=["generation_actual", "generation_forecast"])
    if valid.empty:
        return {"error": "No matched forecast records available"}

    errors = valid["generation_forecast"] - valid["generation_actual"]

    return {
        "period": "January 2026",
        "matched_records": int(len(valid)),
        "missing_forecasts": int(df["generation_forecast"].isna().sum()),
        "mae": round(float(errors.abs().mean()), 2),
        "rmse": round(float((errors ** 2).mean() ** 0.5), 2),
        "bias": round(float(errors.mean()), 2),
    }