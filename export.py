import requests
import pandas as pd
import os

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

BASE_ENDPOINT = (
    "https://api.sleekflow.io/api/customObjects/"
    "crm_campaign_replies/records"
)

headers = {
    "Accept": "application/json",
    "X-Sleekflow-Api-Key": API_KEY
}

all_records = []
next_token = None
page = 1

while True:

    params = {
        "limit": 1000
    }

    if next_token:
        params["ContinuationToken"] = next_token

    print("=" * 50)
    print(f"Requesting page {page}")

    if next_token:
        print(
            f"ContinuationToken Length: {len(next_token)}"
        )

    response = requests.get(
        BASE_ENDPOINT,
        headers=headers,
        params=params
    )

    print(f"HTTP Status: {response.status_code}")

    if response.status_code != 200:
        print("Response Text:")
        print(response.text[:3000])

    response.raise_for_status()

    data = response.json()

    records = data.get(
        "records",
        []
    )

    print(
        f"Records Retrieved: {len(records)}"
    )

    all_records.extend(records)

    next_token = data.get(
        "nextContinuationToken"
    )

    if not next_token:
        print("No more pages.")
        break

    page += 1

print("=" * 50)
print(
    f"Total Records Retrieved: {len(all_records)}"
)

rows = []

for record in all_records:

    property_values = record.get(
        "
