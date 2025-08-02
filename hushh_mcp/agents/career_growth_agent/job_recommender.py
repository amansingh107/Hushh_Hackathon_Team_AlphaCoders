
### `job_recommender.py`
import httpx
from typing import List, Dict
import asyncio

# Adzuna credentials
ADZUNA_APP_ID = "e12359b5"     # Replace with your actual App ID
ADZUNA_APP_KEY = "710cbf3e82002bf2461c64b13ae2e23c"   # Replace with your actual App Key
COUNTRY = "IN"  # Use "in" for India, "us" for USA, "gb" for UK, etc.

from typing import List, Dict
import httpx


# RapidAPI credentials
RAPIDAPI_KEY = "3e5f2f4104msh339df466f6ee521p13c1e2jsn5c2c837525d6"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
JSEARCH_HOST = "jsearch.p.rapidapi.com"
LINKEDIN_HOST = "linkedin-job-search-api.p.rapidapi.com"

async def fetch_jobs_jsearch(skill: str, max_results: int = 10) -> List[Dict]:
    url = f"https://{JSEARCH_HOST}/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": JSEARCH_HOST
    }
    params = {
        "query": f"{skill} jobs",
        "page": 1,
        "num_pages": 1,
        "country": "in",
        "date_posted": "all"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

    jobs = []
    for job in data.get("data", [])[:max_results]:
        jobs.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "url": job.get("job_apply_link"),
            "skill": skill,
            "source": "JSearch"
        })

    return jobs


async def fetch_jobs_linkedin(max_results: int = 10) -> List[Dict]:
    url = f"https://{LINKEDIN_HOST}/active-jb-1h"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": LINKEDIN_HOST
    }
    params = {
        "offset": 0
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

    jobs = []
    for job in data.get("data", [])[:max_results]:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("companyName"),
            "location": job.get("location"),
            "url": job.get("jobUrl"),
            "skill": None,
            "source": "LinkedIn"
        })

    return jobs


async def fetch_jobs_adzuna(max_results: int = 10) -> List[Dict]:
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": max_results,
        "content-type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    jobs = []
    for job in data.get("results", [])[:max_results]:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "url": job.get("redirect_url"),
            "skill": None,
            "source": "Adzuna"
        })

    return jobs
async def fetch_combined_jobs(skill: str, total_limit: int = 30) -> List[Dict]:
    jsearch_limit = total_limit // 3
    linkedin_limit = total_limit // 3
    adzuna_limit = total_limit - jsearch_limit - linkedin_limit

    tasks = [
        # fetch_jobs_jsearch(skill, jsearch_limit),
        # fetch_jobs_linkedin(linkedin_limit),
        fetch_jobs_adzuna(adzuna_limit),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    combined_jobs = []
    for result in results:
        if isinstance(result, Exception):
            # Log or print the error if needed
            print(f"Error while fetching jobs: {str(result)}")
        else:
            combined_jobs.extend(result)

    return combined_jobs
