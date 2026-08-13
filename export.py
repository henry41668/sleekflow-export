import requests
import pandas as pd
import os
from datetime import datetime

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

BASE_ENDPOINT = (
    "https://api.sleekflow.io/api/customObjects/"
    "crm_campaign_replies/records"
)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Sleekflow-Api-Key": API_KEY
}

all_records = []
continuation_token = None
page = 1

while True:

    print("=" * 60)
    print(f"Processing Page {page}")

    params = {
        "limit": 1000
    }

    if continuation_token is None:

        response = requests.get(
            BASE_ENDPOINT,
            headers=headers,
            params=params
        )

    else:

        response = requests.request(
            "GET",
            BASE_ENDPOINT,
            headers=headers,
            params=params,
            json={
                "ContinuationToken":
                    continuation_token
            }
        )

    response.raise_for_status()

    data = response.json()

    records = data.get(
        "records",
        []
    )

    print(
        f"Retrieved {len(records)} records"
    )

    all_records.extend(records)

    continuation_token = data.get(
        "nextContinuationToken"
    )

    if not continuation_token:
        print("No more pages.")
        break

    page += 1

print("=" * 60)
print(
    f"Total Records: {len(all_records)}"
)

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
            pv.get(
                "team_code"
            ),

        "campaign_code":
            pv.get(
                "campaign_code"
            ),

        "enquiry_item":
            pv.get(
                "enquiry_item"
            ),

        "ec_member_id":
            pv.get(
                "ec_member_id"
            ),

        "incoming_channel":
            pv.get(
                "incoming_channel"
            ),

        "cs_follow_date":
            pv.get(
                "cs_follow_date"
            ),

        "msp_entry_y_n":
            pv.get(
                "msp_entry_y_n"
            ),

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

today = datetime.now().strftime(
    "%Y%m%d"
)

filename = (
    f"SleekFlow_CustomObject_{today}.csv"
)

df.to_csv(
    filename,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 60)
print(
    f"CSV Generated: {filename}"
)
print(
    f"Rows Exported: {len(df)}"
)
