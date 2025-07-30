import asyncio
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from hushh_mcp.agents.career_growth_agent.career import CareerGrowthAgent
from hushh_mcp.consent.token import issue_token
from hushh_mcp.types import ConsentScope
from .linkedin import parse_linkedin_zip
from .skills_gap import extract_job_skills_from_postings, compute_skill_gaps
from .course_recommender import fetch_coursera_courses, fetch_udemy_courses , fetch_all_courses
from .resume import parse_resume
from .github import parse_github_repo
from ...constants import ConsentScope
import os
import tempfile
from fastapi import FastAPI, Form, HTTPException
import asyncio
from .job_recommender import fetch_combined_jobs
from .job_fetcher import fetch_job_descriptions

app = FastAPI()

# In-memory skill cache per user (use Redis/DB in production)
USER_SKILL_DB = {}

@app.post("/upload_linkedin/")
async def upload_linkedin(user_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are supported.")
    file_bytes = await file.read()
    token = issue_token(user_id=user_id, agent_id="Career Growth Agent", scope=ConsentScope.CUSTOM_LINKEDIN_UPLOAD)

    parsed_data = CareerGrowthAgent().extract_career_data(user_id, token.token, file_bytes)
    skills, experience = parsed_data

    # Save skills
    USER_SKILL_DB.setdefault(user_id, {"skills": set(), "experience": []})
    USER_SKILL_DB[user_id]["skills"].update(skills)
    USER_SKILL_DB[user_id]["experience"].extend(experience)

    return {
        "message": "LinkedIn archive parsed successfully.",
        "parsed_data": parsed_data
    }

@app.post("/resume/")
async def upload_resume(user_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf resumes are supported.")
    file_bytes = await file.read()
    parsed_data = parse_resume(file_bytes)

    USER_SKILL_DB.setdefault(user_id, {"skills": set(), "experience": []})
    USER_SKILL_DB[user_id]["skills"].update(parsed_data.get("skills", []))
    USER_SKILL_DB[user_id]["experience"].extend(parsed_data.get("experience", []))

    return {
        "message": "Resume parsed successfully.",
        "parsed_data": parsed_data
    }

@app.post("/parse_github/")
async def parse_github(user_id: str = Form(...), github_username: str = Form(...)):
    token = issue_token(user_id=user_id, agent_id="agent_github_parser", scope=ConsentScope.CUSTOM_TEMPORARY)
    parsed_data = await parse_github_repo(github_username)

    USER_SKILL_DB.setdefault(user_id, {"skills": set(), "experience": []})
    USER_SKILL_DB[user_id]["skills"].update(parsed_data.get("skills", []))
    USER_SKILL_DB[user_id]["experience"].extend(parsed_data.get("experience", []))

    return {
        "message": "GitHub profile parsed successfully.",
        "parsed_data": parsed_data
    }
@app.post("/analyze_skill_gap/")
async def analyze_skill_gap(user_id: str = Form(...), job_title: str = Form(...)):
    if user_id not in USER_SKILL_DB:
        raise HTTPException(status_code=404, detail="No user skill data found. Please upload resume, LinkedIn, or GitHub first.")
    
    user_skills = USER_SKILL_DB[user_id]["skills"]

  # Fetch real-time job descriptions and extract job skill demands
    print("Fetching job descriptions for:", job_title)
    descriptions = await fetch_job_descriptions(job_title)
    print(f"Fetched {len(descriptions)} job descriptions.")
    job_skills = extract_job_skills_from_postings(descriptions)
    print(f"Extracted {len(job_skills)} unique job skills.")
    skill_gaps = compute_skill_gaps(user_skills, job_skills)

    # Save skill gaps for this user
    USER_SKILL_DB[user_id]["skill_gaps"] = skill_gaps
    USER_SKILL_DB[user_id]["job_title"] = job_title

    return {
        "user_id": user_id,
        "job_title": job_title,
        "user_skills": list(user_skills),
        "job_required_skills": list(job_skills),
        "skill_gaps": list(skill_gaps)
    }


@app.post("/recommend_courses/")
async def recommend_courses(user_id: str = Form(...)):
    if user_id not in USER_SKILL_DB or "skill_gaps" not in USER_SKILL_DB[user_id]:
        raise HTTPException(status_code=404, detail="Missing user or skill gap data.")

    skill_gaps: List[str] = list(USER_SKILL_DB[user_id]["skill_gaps"])[:20]

    recommended_courses = await fetch_all_courses(skill_gaps, total_limit=15)

    return {
        "recommended_courses": recommended_courses
    }
@app.post("/recommend_jobs/")
async def recommend_jobs(user_id: str = Form(...)):
    
    if user_id not in USER_SKILL_DB:
        raise HTTPException(status_code=404, detail="No skill data found for this user.")

    skills = list(USER_SKILL_DB[user_id]["skills"])  
    job_results = []

    for skill in skills:
        try:
            jobs = await fetch_combined_jobs(skill)  # ✅ Await the coroutine
            job_results.extend(jobs)
        except Exception as e:
            print(f"Error fetching jobs for skill {skill}: {str(e)}")

    return {"recommended_jobs": job_results}  # ✅ Now it's serializable
