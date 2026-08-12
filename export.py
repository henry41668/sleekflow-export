import requests
import os

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

response = requests.get(
    "https://api.sleekflow.io/api/customObjects/crm_campaign_replies/records",
    headers={
        "Accept": "application/json",
        "X-Sleekflow-Api-Key": API_KEY
    },
    params={
        "limit": 1000
    }
)

response.raise_for_status()

data = response.json()

token = data.get("nextContinuationToken")

print("TOKEN LENGTH:")
print(len(token))

print("\nTOKEN PREVIEW:")
print(token[:1000])
