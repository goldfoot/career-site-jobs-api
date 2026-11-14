"""Fetch normalized jobs for a list of companies via the Apify Actor goldfoot/ats-jobs-feed.

pip install apify-client
export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("goldfoot/ats-jobs-feed").call(run_input={
    "companies": ["stripe.com", "linear.app", "personio.de", "jobs.lever.co/palantir"],
    "titleKeywords": ["engineer"],
    "locations": ["Germany", "remote"],
    "includeDescription": False,
    "onlyNewJobs": True,          # remembers jobs between runs -> perfect for alerts
    "monitorId": "my-watchlist",
})
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(job["companyName"], "|", job["title"], "|", job["location"], "|", job["url"])
