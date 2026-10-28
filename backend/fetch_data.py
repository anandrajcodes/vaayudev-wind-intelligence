
import requests
import pandas as pd

URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

all_records = []

for day in pd.date_range("2026-01-01", "2026-01-31"):
    date = day.strftime("%Y-%m-%d")

    params = {
        "settlementDateFrom": date,
        "settlementDateTo": date,
        "fuelType": "WIND",
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()

    records = response.json().get("data", [])
    all_records.extend(records)

    print(f"{date}: {len(records)} records")

df = pd.DataFrame(all_records)

if not df.empty:
    df = df.drop_duplicates(
        subset=["startTime", "fuelType"]
    )
    df = df.sort_values("startTime")

    df.to_csv("wind_actuals_jan2026.csv", index=False)

print("Total records:", len(df))
print("CSV saved: wind_actuals_jan2026.csv")
