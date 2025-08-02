import os
import httpx
import asyncio
from typing import List, Dict

import asyncio
import httpx
import os
from typing import List, Dict
# === ✅ API Keys ===
RAPIDAPI_KEY = "a43d7864c4msh8b60316af0d6629p115275jsn7f45da6ced7c"


# Load your RapidAPI key from environment or fallback
# RapidAPI hosts
UD_HOST = "udemy-api2.p.rapidapi.com"
CO_HOST = "collection-for-coursera-courses.p.rapidapi.com"



# ✅ FIXED: Udemy using search endpoint
async def fetch_udemy_courses(skill: str) -> List[Dict]:
    query = skill.lower().replace(" ", "%20")
    url = f"https://{UD_HOST}/v1/udemy/search/{query}"

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Host": UD_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"⚠️ Udemy error for '{skill}': {e}")
            return []

    if not isinstance(data, dict):
        print(f"⚠️ Udemy response not dict for '{skill}': {type(data)}")
        return []

    courses = []
    for item in data.get("courses", [])[:3]:
        courses.append({
            "platform": "Udemy",
            "title": item.get("title"),
            "url": item.get("url"),
            "skill": skill
        })
    return courses


# ✅ FIXED: Coursera response handling
async def fetch_coursera_courses(skill: str) -> List[Dict]:
    url = f"https://{CO_HOST}/rapidapi/course/get_institution.php"
    headers = {
        "X-RapidAPI-Host": CO_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }
    params = {
        "institution": "coursera",
        "skill": skill
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"⚠️ Coursera error for '{skill}': {e}")
            return []

    courses = []
    if isinstance(data, list):  # handle raw list
        for item in data[:3]:
            courses.append({
                "platform": "Coursera",
                "title": item.get("name", f"{skill} Course"),
                "url": item.get("url", "https://www.coursera.org"),
                "skill": skill
            })
    elif isinstance(data, dict):
        for item in data.get("data", [])[:3]:
            courses.append({
                "platform": "Coursera",
                "title": item.get("name", f"{skill} Course"),
                "url": item.get("url", "https://www.coursera.org"),
                "skill": skill
            })
    else:
        print(f"⚠️ Coursera unknown response format for '{skill}': {type(data)}")

    return courses

# === ✅ Combined Course Recommender ===
async def fetch_all_courses(skill_gaps: List[str], total_limit: int = 15) -> List[Dict]:
    all_courses = []
    seen = set()

    for skill in skill_gaps:
        if len(all_courses) >= total_limit:
            break

        combined = []

        try:
            udemy = await fetch_udemy_courses(skill)
            await asyncio.sleep(1)
            combined.extend(udemy)
        except Exception as e:
            print(f"⚠️ Udemy fetch failed for '{skill}': {e}")

        try:
            coursera = await fetch_coursera_courses(skill)
            await asyncio.sleep(1)
            combined.extend(coursera)
        except Exception as e:
            print(f"⚠️ Coursera fetch failed for '{skill}': {e}")

        for course in combined:
            key = (course["platform"], course["title"])
            if key not in seen:
                seen.add(key)
                all_courses.append(course)
            if len(all_courses) >= total_limit:
                break

    return all_courses
