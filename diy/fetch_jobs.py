"""Fetch open jobs from public ATS job-board feeds. No dependencies (Python 3.9+).

Usage:
    python fetch_jobs.py greenhouse:stripe lever:palantir ashby:linear personio:personio

Supported: greenhouse, lever, ashby, workable, smartrecruiters, recruitee,
personio, breezy, rippling, teamtailor (pass the career-site host, e.g. teamtailor:jobs.example.com).
Each function returns a list of {"title", "location", "url"} dicts.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "career-site-jobs-examples/1.0 (+https://github.com/goldfoot/career-site-jobs-api)"}


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def _json(url):
    return json.loads(_get(url))


def greenhouse(slug):
    data = _json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
    return [{"title": j["title"], "location": (j.get("location") or {}).get("name"), "url": j["absolute_url"]} for j in data["jobs"]]


def lever(slug):
    data = _json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    return [{"title": j["text"], "location": j["categories"].get("location"), "url": j["hostedUrl"]} for j in data]


def ashby(slug):
    data = _json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
    return [{"title": j["title"], "location": j.get("location"), "url": j["jobUrl"]} for j in data["jobs"]]


def workable(slug):
    data = _json(f"https://apply.workable.com/api/v1/widget/accounts/{slug}")
    return [{"title": j["title"], "location": ", ".join(filter(None, [j.get("city"), j.get("country")])), "url": j["url"]} for j in data["jobs"]]


def smartrecruiters(company_id, limit=100):
    data = _json(f"https://api.smartrecruiters.com/v1/companies/{company_id}/postings?limit={limit}")
    return [{"title": j["name"], "location": (j.get("location") or {}).get("fullLocation") or (j.get("location") or {}).get("city"),
             "url": f"https://jobs.smartrecruiters.com/{company_id}/{j['id']}"} for j in data["content"]]


def recruitee(slug):
    data = _json(f"https://{slug}.recruitee.com/api/offers/")
    return [{"title": j["title"], "location": j.get("location"), "url": j["careers_url"]} for j in data["offers"]]


def personio(slug):
    root = ET.fromstring(_get(f"https://{slug}.jobs.personio.de/xml?language=en"))
    return [{"title": p.findtext("name"), "location": p.findtext("office"),
             "url": f"https://{slug}.jobs.personio.de/job/{p.findtext('id')}"} for p in root.iter("position")]


def breezy(slug):
    data = _json(f"https://{slug}.breezy.hr/json")
    return [{"title": j["name"], "location": (j.get("location") or {}).get("name"), "url": j["url"]} for j in data]


def rippling(slug):
    data = _json(f"https://ats.rippling.com/api/v2/board/{slug}/jobs?page=0&pageSize=100")
    items = data.get("items", data) if isinstance(data, dict) else data
    return [{"title": j.get("name") or j.get("title"),
             "location": ", ".join(l.get("name", "") for l in j.get("locations", [])) if isinstance(j.get("locations"), list) else None,
             "url": j.get("url")} for j in items]


def teamtailor(host):
    root = ET.fromstring(_get(f"https://{host}/jobs.rss"))
    return [{"title": i.findtext("title"), "location": None, "url": i.findtext("link")} for i in root.iter("item")]


ATS = {f.__name__: f for f in [greenhouse, lever, ashby, workable, smartrecruiters, recruitee, personio, breezy, rippling, teamtailor]}

if __name__ == "__main__":
    for arg in sys.argv[1:] or ["greenhouse:stripe", "lever:palantir", "ashby:linear"]:
        ats, _, slug = arg.partition(":")
        try:
            jobs = ATS[ats](slug)
            print(f"{arg}: {len(jobs)} jobs" + (f", e.g. {jobs[0]['title']} ({jobs[0]['location']})" if jobs else ""))
        except Exception as e:  # noqa: BLE001 - example script
            print(f"{arg}: failed ({e})")
