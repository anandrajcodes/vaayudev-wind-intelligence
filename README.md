# VaayuDev — Day-Ahead Wind Forecast Intelligence

VaayuDev is a dashboard for analysing UK national wind generation forecasts against actual generation during January 2026. It helps users understand forecast accuracy through interactive charts and error metrics.

## Features

- Forecast vs actual wind generation visualisation
- Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and forecast bias
- Hourly forecast error analysis
- Missing-data reporting
- FastAPI backend and React dashboard
- Docker-based backend setup

## Technology Stack

- **Frontend:** React, Vite, CSS
- **Backend:** Python, FastAPI, Pandas, NumPy
- **Data source:** Elexon BMRS — FUELHH and WINDFOR datasets
- **Containerisation:** Docker and Docker Compose

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
│   └── wind_forecast_accuracy_jan2026.csv
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Run Locally

### 1. Backend

From the project root, activate your Python environment and install the dependencies:

```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend API: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 2. Frontend

Open a separate terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, normally `http://localhost:5173`.

### 3. Docker

From the project root, ensure Docker Desktop is running:

```powershell
docker compose up -d --build
```

Backend health check: `http://localhost:8000/health`

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | API status |
| `/health` | Health check |
| `/api/status` | Application and analysis information |
| `/api/chart-data` | Hourly forecast and actual generation |
| `/api/metrics` | Forecast accuracy metrics |

## Data and Methodology

The analysis focuses on UK national wind generation for 1–31 January 2026. Actual generation is filtered to the `WIND` fuel type. Half-hourly actual observations are aggregated into hourly means and matched to forecasts by delivery timestamp.

Forecast selection uses a modelling assumption of **12:00 UTC on the preceding calendar day** as the day-ahead cutoff. This is an analytical assumption and should not be interpreted as a verified electricity-market procurement deadline.

Forecast errors are calculated as:

`Error = Forecast − Actual`

- **MAE:** Average absolute forecast error.
- **RMSE:** Square root of the average squared forecast error.
- **Bias:** Average signed forecast error. A positive value indicates overforecasting.

Records without a matched forecast are reported as missing rather than treated as zero. Metrics are calculated only for matched records with valid actual and forecast values.

## Limitations

Results depend on the selected forecast cutoff, the source data returned by Elexon, and the hourly aggregation method. The results should be validated against the intended market publication and procurement rules before being used for operational purchasing decisions.

## Deployment

- **Live dashboard:** Add the deployed frontend URL here.
- **Backend API:** Add the deployed backend URL here.
- **Repository:** Add the public GitHub repository URL here.

## AI Disclosure

AI assistance was used during development for coding guidance, debugging, documentation, and project refinement. Data processing, forecast selection, and metric calculations should be validated by the project author.

## License

Add an appropriate open-source license before distributing the project.
