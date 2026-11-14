# Company career-site jobs API: examples (Greenhouse, Lever, Ashby, Personio, Teamtailor…)

Get **every open job from a company's own career site** as clean JSON, whichever applicant tracking system (ATS) it uses. This repo shows two ways:

1. **DIY:** call the public job-board feeds yourself. [`diy/fetch_jobs.py`](diy/fetch_jobs.py) is a dependency-free Python script for 10 ATS: `python diy/fetch_jobs.py greenhouse:stripe personio:personio`.
2. **Managed:** use the [Career Site Jobs Scraper](https://apify.com/goldfoot/ats-jobs-feed) on Apify ([`managed/`](managed/)). It covers 10 ATS platforms, auto-detects the board from a plain domain, normalizes all fields (salary, remote, location…) and has an "only new jobs" monitoring mode. *(Disclosure: I built it.)*

## Public feeds per ATS (DIY)

| ATS | Endpoint |
|---|---|
| Greenhouse | `GET https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true` |
| Lever | `GET https://api.lever.co/v0/postings/{slug}?mode=json` |
| Ashby | `GET https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true` |
| Workable | `GET https://apply.workable.com/api/v1/widget/accounts/{slug}?details=true` |
| SmartRecruiters | `GET https://api.smartrecruiters.com/v1/companies/{id}/postings` |
| Recruitee | `GET https://{slug}.recruitee.com/api/offers/` |
| Personio | `GET https://{slug}.jobs.personio.de/xml?language=en` |
| Rippling | `GET https://ats.rippling.com/api/v2/board/{slug}/jobs` |
| Breezy HR | `GET https://{slug}.breezy.hr/json` |
| Teamtailor | `GET https://{career-site-host}/jobs.rss` |

Each returns a different format. Normalizing them, finding the right slug for a company, and tracking which jobs are new is the tedious part.

## Managed example (Python) — [`managed/python_example.py`](managed/python_example.py)

```python
# pip install apify-client
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("goldfoot/ats-jobs-feed").call(run_input={
    "companies": ["stripe.com", "linear.app", "personio.de", "jobs.lever.co/palantir"],
    "titleKeywords": ["engineer"],
    "locations": ["Germany", "remote"],
    "onlyNewJobs": True,          # remember jobs between runs → alerts
    "monitorId": "my-watchlist",
})
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(job["companyName"], "|", job["title"], "|", job["location"], "|", job["url"])
```

## Managed example (JavaScript) — [`managed/node_example.mjs`](managed/node_example.mjs)

```js
// npm i apify-client
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('goldfoot/ats-jobs-feed').call({
  companies: ['https://boards.greenhouse.io/stripe', 'ashby:linear'],
  remoteOnly: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((j) => ({ company: j.companyName, title: j.title, salary: j.salaryText })));
```

## Use cases
Job alerts for target companies · hiring signals for sales and recruiting · competitor hiring intelligence · niche job boards · labour-market research.

## Finding the ATS of a company
Look at the links on its careers page (`boards.greenhouse.io/…`, `jobs.lever.co/…`, `*.jobs.personio.de`, `jobs.ashbyhq.com/…`) or the `src` of embedded job widgets. The managed Actor does this automatically from a plain domain.

## Not supported
Workday, SuccessFactors, iCIMS and Taleo don't offer an open public feed, so they're out of scope here.

MIT licensed. Contributions welcome.
