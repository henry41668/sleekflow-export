import requests
import os
import json

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

BASE_ENDPOINT = "https://api.sleekflow.io/api/customObjects/crm_campaign_replies/records"

headers = {
    "Accept": "application/json",
    "X-Sleekflow-Api-Key": API_KEY
}

print("=" * 50)
print("REQUESTING FIRST PAGE")
print("=" * 50)

response = requests.get(
    BASE_ENDPOINT,
    headers=headers,
    params={
        "limit": 1000
    }
)

print("Status Code:", response.status_code)

response.raise_for_status()

data = response.json()

print("\nTOP LEVEL KEYS:")
print(list(data.keys()))

print("\nNEXT TOKEN PREVIEW:")
token = data.get("nextContinuationToken")

print(type(token))

if token:
    print("Length:", len(token))
    print("First 300 chars:")
    print(token[:300])

print("\nSAVING RESPONSE...")

with open(
    "first_response.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Done.")
