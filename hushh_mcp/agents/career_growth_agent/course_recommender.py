import os
import httpx
import asyncio
from typing import List, Dict

# === ✅ API Keys ===
GOOGLE_API_KEY = os.getenv("YOUTUBE_API_KEY", "your-google-api-key")
RAPIDAPI_KEY = "3e5f2f4104msh339df466f6ee521p13c1e2jsn5c2c837525d6"

# === ✅ YouTube ===
async def fetch_youtube_courses(skill: str) -> List[Dict]:
    query = f"{skill} tutorial"
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&q={query}&type=video&maxResults=5&key={GOOGLE_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"⚠️ YouTube error for '{skill}': {e}")
            return []

    results = []
    for item in data.get("items", []):
        video_id = item["id"].get("videoId")
        title = item["snippet"].get("title")
        if video_id and title:
            results.append({
                "platform": "YouTube",
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "skill": skill
            })

    return results

# === ✅ Udemy ===
async def fetch_udemy_courses(skill: str) -> List[Dict]:
    url = f"https://udemy-api2.p.rapidapi.com/v1/udemy/category/{skill.lower()}"
    headers = {
        "content-type": "application/json",
        "x-rapidapi-host": "udemy-api2.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    payload = {
        "page": 1,
        "page_size": 5,
        "sort": "popularity",
        "locale": "en_US",
        "extract_pricing": True
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 429:
                print(f"⚠️ Udemy rate limited for '{skill}'")
                return []
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"⚠️ Udemy error for '{skill}': {e}")
            return []

    if not isinstance(data, dict):
        print(f"⚠️ Udemy response not a dict for '{skill}': {type(data)}")
        return []

    results = []
    for course in data.get("data", [])[:5]:
        title = course.get("title") or f"{skill} Course"
        course_url = course.get("url") or ""
        results.append({
            "platform": "Udemy",
            "title": title,
            "url": f"https://www.udemy.com{course_url}",
            "skill": skill
        })

    return results
async def fetch_coursera_courses(skill: str) -> List[Dict]:
    url = "https://collection-for-coursera-courses.p.rapidapi.com/rapidapi/course/get_institution.php"
    headers = {
        "x-rapidapi-host": "collection-for-coursera-courses.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"⚠️ Coursera error for '{skill}': {e}")
            return []

    if not isinstance(data, list):  # Fix here
        print(f"⚠️ Coursera response not a list for '{skill}': {type(data)}")
        return []

    results = []
    for item in data[:5]:
        title = item if isinstance(item, str) else item.get("title", f"{skill} Course")
        course_url = "https://www.coursera.org"
        results.append({
            "platform": "Coursera",
            "title": title,
            "url": course_url,
            "skill": skill
        })

    return results


# === ✅ Main Aggregator ===
async def fetch_all_courses(skill_gaps: List[str], total_limit: int = 15) -> List[Dict]:
    all_courses = []
    seen = set()

    for skill in skill_gaps:
        if len(all_courses) >= total_limit:
            break

        combined = []

        # try:
        #     yt = await fetch_youtube_courses(skill)
        #     await asyncio.sleep(1)
        #     combined.extend(yt)
        # except Exception as e:
        #     print(f"⚠️ YouTube fetch failed for '{skill}': {e}")

        try:
            coursera = await fetch_coursera_courses(skill)
            await asyncio.sleep(1)
            combined.extend(coursera)
        except Exception as e:
            print(f"⚠️ Coursera fetch failed for '{skill}': {e}")

        # try:
        #     udemy = await fetch_udemy_courses(skill)
        #     await asyncio.sleep(1)
        #     combined.extend(udemy)
        # except Exception as e:
        #     print(f"⚠️ Udemy fetch failed for '{skill}': {e}")

        for course in combined:
            key = (course["platform"], course["title"])
            if key not in seen:
                seen.add(key)
                all_courses.append(course)
            if len(all_courses) >= total_limit:
                break

    return all_courses


#https://chatgpt.com/share/6883d6b1-5cb4-800b-bbf3-7b37599e9453