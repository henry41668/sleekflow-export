import requests
import pandas as pd
import os

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

BASE_URL = (
    "https://api.sleekflow.io/api/customObjects/"
    "crm_campaign_replies/records?limit=1000"
)

headers = {
    "Accept": "application/json",
    "X-Sleekflow-Api-Key": API_KEY
}

all_records = []
next_token = None

while True:

    url = BASE_URL

    if next_token:
        url += f"&continuationToken={next_token}"

    print(f"Calling: {url}")

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    records = data.get(
        "records",
        []
    )

    all_records.extend(records)

    next_token = data.get(
        "nextContinuationToken"
    )

    print(
        f"Retrieved {len(records)} rows"
    )

    if not next_token:
        break

rows = []

for record in all_records:

    pv = record.get(
        "propertyValues",
        {}
    )

    rows.append({
        "primaryPropertyValue":
            record.get(
                "primaryPropertyValue"
            ),

        "team_code":
            pv.get("team_code"),

        "campaign_code":
            pv.get("campaign_code"),

        "enquiry_item":
            pv.get("enquiry_item"),

        "ec_member_id":
            pv.get("ec_member_id"),

        "incoming_channel":
            pv.get("incoming_channel"),

        "referencedUserProfileId":
            record.get(
                "referencedUserProfileId"
            ),

        "createdAt":
            record.get(
                "createdAt"
            ),

        "updatedAt":
            record.get(
                "updatedAt"
            )
    })

df = pd.DataFrame(rows)

df.to_csv(
    "SleekFlow.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Finished. Total rows: {len(df)}"
)
