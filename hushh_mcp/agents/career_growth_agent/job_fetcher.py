import httpx
from typing import List

ADZUNA_APP_ID = "e12359b5"     # Replace with your actual App ID
ADZUNA_APP_KEY = "710cbf3e82002bf2461c64b13ae2e23c"   # Replace with your actual App Key
COUNTRY = "in"  # Use "in" for India, "us" for USA, "gb" for UK, etc.

async def fetch_job_descriptions(job_title: str, num_pages: int = 1) -> List[str]:
    descriptions = []

    async with httpx.AsyncClient() as client:
        for page in range(1, num_pages + 1):
            url = (
                f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
                f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
                f"&what={job_title}&content-type=application/json"
            )
            try:
                response = await client.get(url)
                data = response.json()
                for job in data.get("results", []):
                    desc = job.get("description")
                    if desc:
                        descriptions.append(desc)
            except Exception as e:
                print(f"⚠️ Failed to fetch page {page}: {e}")
                continue

    return descriptions
