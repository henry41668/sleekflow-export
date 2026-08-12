import requests
import os

API_KEY = os.environ["SLEEKFLOW_API_KEY"]

BASE_ENDPOINT = (
    "https://api.sleekflow.io/api/customObjects/"
    "crm_campaign_replies/records"
)

headers = {
    "Accept": "application/json",
    "X-Sleekflow-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# PAGE 1

response = requests.get(
    BASE_ENDPOINT,
    headers=headers,
    params={
        "limit": 1000
    }
)

response.raise_for_status()

data = response.json()

token = data.get("nextContinuationToken")

print("PAGE1 STATUS:", response.status_code)
print("TOKEN LENGTH:", len(token))

# PAGE 2

response2 = requests.request(
    "GET",
    BASE_ENDPOINT,
    headers=headers,
    params={
        "limit": 1000
    },
    json={
        "ContinuationToken": token
    }
)

print("PAGE2 STATUS:")
print(response2.status_code)

print("PAGE2 RESPONSE:")
print(response2.text[:5000])
