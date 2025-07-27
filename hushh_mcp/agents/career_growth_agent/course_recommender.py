import httpx
from typing import List, Dict
from bs4 import BeautifulSoup

# Replace with your actual key
RAPIDAPI_KEY = "3e5f2f4104msh339df466f6ee521p13c1e2jsn5c2c837525d6"

async def fetch_youtube_courses(skill: str, job_title: str) -> List[Dict]:
    query = f"{skill} tutorial".replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for vid in soup.select("a#video-title")[:5]:
        title = vid.get("title")
        href = vid.get("href")
        if title and href:
            results.append({
                "platform": "YouTube",
                "title": title.strip(),
                "url": f"https://www.youtube.com{href}",
                "skill": skill,
                "job_title": job_title
            })
    return results

async def fetch_coursera_courses(skill: str, job_title: str) -> List[Dict]:
    query = skill.replace(" ", "%20")
    url = f"https://coursera-courses2.p.rapidapi.com/courses?query={query}&limit=5"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "coursera-courses2.p.rapidapi.com"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Coursera API error for {skill}: {resp.status_code}")
            return []

        data = resp.json().get("courses", [])
        results = []
        for item in data:
            results.append({
                "platform": "Coursera",
                "title": item.get("name"),
                "url": item.get("url") or f"https://www.coursera.org{item.get('slug', '')}",
                "skill": skill,
                "job_title": job_title
            })
        return results

async def fetch_udemy_courses(skill: str, job_title: str) -> List[Dict]:
    query = skill.replace(" ", "%20")
    url = f"https://udemy-course-search.p.rapidapi.com/search?query={query}&page_size=5"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "udemy-course-search.p.rapidapi.com"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Udemy API error for {skill}: {resp.status_code}")
            return []

        data = resp.json().get("courses", [])
        results = []
        for item in data:
            results.append({
                "platform": "Udemy",
                "title": item.get("title"),
                "url": item.get("url"),
                "skill": skill,
                "job_title": job_title
            })
        return results
