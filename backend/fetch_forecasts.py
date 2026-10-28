
import requests
import pandas as pd

URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR"

all_records = []

for day in pd.date_range("2025-12-31", "2026-01-31"):
    date = day.strftime("%Y-%m-%d")

    params = {
        "publishDateTimeFrom": f"{date}T00:00:00Z",
        "publishDateTimeTo": f"{date}T23:59:59Z",
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()

    records = response.json().get("data", [])
    all_records.extend(records)

    print(f"{date}: {len(records)} forecast records")

df = pd.DataFrame(all_records)

if not df.empty:
    df = df.drop_duplicates(
        subset=["publishTime", "startTime"]
    )
    df = df.sort_values(["publishTime", "startTime"])

    df.to_csv("wind_forecasts_jan2026.csv", index=False)

print("Total forecast records:", len(df))
print("CSV saved: wind_forecasts_jan2026.csv")
