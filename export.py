import requests
import pandas as pd
import os

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

BASE_ENDPOINT = "https://api.sleekflow.io/api/customObjects/crm_campaign_replies/records"

headers = {
    "Accept": "application/json",
    "X-Sleekflow-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

all_records = []
next_token = None
page = 1

while True:

    print("=" * 50)
    print(f"Requesting Page {page}")

    if page == 1:

        response = requests.get(
            BASE_ENDPOINT,
            headers=headers,
            params={
                "limit": 1000
            }
        )

    else:

        response = requests.get(
            BASE_ENDPOINT,
            headers=headers,
            json={
                "ContinuationToken": next_token
            }
        )

    print(f"HTTP Status: {response.status_code}")

    if response.status_code != 200:
        print(response.text)

    response.raise_for_status()

    data = response.json()

    records = data.get("records", [])

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
        "propertyValues",
        {}
    )

    rows.append({

        "primaryPropertyValue":
            record.get("primaryPropertyValue"),

        "referencedUserProfileId":
            record.get("referencedUserProfileId"),

        "createdAt":
            record.get("createdAt"),

        "updatedAt":
            record.get("updatedAt"),

        "team_code":
            property_values.get("team_code"),

        "campaign_code":
            property_values.get("campaign_code"),

        "enquiry_item":
            property_values.get("enquiry_item"),

        "ec_member_id":
            property_values.get("ec_member_id"),

        "incoming_channel":
            property_values.get("incoming_channel")
    })

df = pd.DataFrame(rows)

df.to_csv(
    "SleekFlow.csv",
    index=False,
    encoding="utf-8-sig"
)

print("=" * 50)
print(f"CSV created successfully")
print(f"Rows exported: {len(df)}")
