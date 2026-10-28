# VaayuDev — Day-Ahead Wind Forecast Intelligence

VaayuDev is a dashboard for analysing UK national wind generation and evaluating day-ahead forecasts against actual generation for January 2026.

## Features

- Forecast vs actual wind generation visualisation
- Forecast accuracy metrics: MAE, RMSE and bias
- Hourly forecast error analysis
- Data quality reporting for matched and missing hourly records
- FastAPI backend and React dashboard
- Docker-based backend deployment

## Technology Stack

- **Frontend:** React, Vite, CSS
- **Backend:** Python, FastAPI, Pandas, NumPy
- **Data source:** Elexon BMRS — FUELHH and WINDFOR datasets
- **Containerisation:** Docker and Docker Compose

## Analysis Period

January 1–31, 2026 (UTC).

The analysis uses national wind generation only. Half-hourly actual generation records are aggregated into hourly averages and matched to hourly forecast delivery periods.

## Forecast Selection Methodology

For each delivery hour, the analysis selects the latest forecast published on or before 12:00 UTC on the previous calendar day.

**Important:** The 12:00 UTC cutoff is a modelling assumption used for this analysis; it has not been independently verified as the applicable market purchasing deadline.

Forecast error is calculated as:

`Error = Forecast generation − Actual generation`

Metrics:

- **MAE:** Mean Absolute Error
- **RMSE:** Root Mean Squared Error
- **Bias:** Mean forecast error; positive values indicate overforecasting.

Missing forecasts are reported as missing rather than being treated as zero.

## Project Structure

```text
VaayuDev/
├── backend/
│   ├── main.py
│   ├── fetch_data.py
│   ├── fetch_forecasts.py
│   ├── analyze_forecasts.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── wind_actuals_jan2026.csv
│   ├── wind_forecasts_jan2026.csv
│   └── wind_forecast_accuracy_jan2026.csv
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Run Locally

### 1. Start the backend with Docker

Install and start Docker Desktop, then run these commands from the project root:

```bash
docker compose up -d --build
```

Backend API: `http://localhost:8000`

Health check: `http://localhost:8000/health`

Metrics: `http://localhost:8000/api/metrics`

Chart data: `http://localhost:8000/api/chart-data`

Stop the backend:

```bash
docker compose down
```

### 2. Start the frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`.

## Accuracy Results

Results are calculated from the generated analysis CSV. Run the analysis script again after updating the source data:

```bash
python backend/analyze_forecasts.py
```

Current local analysis reports 744 matched hourly periods and no missing forecasts. Reported metrics are:

- **MAE:** 2,017.92 MW
- **RMSE:** 2,477.04 MW
- **Bias:** +1,806.23 MW

These are results under the stated forecast-selection assumption and should not be interpreted as a guarantee of real-world procurement performance.

## Deployment

- **Live application:** Add the public deployment URL here.
- **Public GitHub repository:** Add the repository URL here.

The local development URLs above are not public deployment links.

## AI Disclosure

AI assistance was used during development for coding guidance, debugging, documentation, and project methodology review. The implementation and results should be reviewed and validated before use in operational procurement decisions.
