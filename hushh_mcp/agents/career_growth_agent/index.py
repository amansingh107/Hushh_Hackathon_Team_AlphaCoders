from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from hushh_mcp.consent.token import issue_token, validate_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.agents.career_growth_agent.career import CareerGrowthAgent
from hushh_mcp.agents.career_growth_agent.linkedin import parse_linkedin_zip
from hushh_mcp.agents.career_growth_agent.skills_gap import extract_job_skills_from_postings, compute_skill_gaps
from hushh_mcp.agents.career_growth_agent.resume import parse_resume
from hushh_mcp.agents.career_growth_agent.github import parse_github_repo
from hushh_mcp.agents.career_growth_agent.job_fetcher import fetch_job_descriptions
from hushh_mcp.agents.career_growth_agent.job_recommender import fetch_combined_jobs

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


USER_SKILL_DB = {}
USER_TOKENS = {}  # user_id -> token string


def ensure_token(user_id: str):
    if user_id not in USER_TOKENS:
        token = issue_token(user_id=user_id, agent_id="career_growth_agent", scope=ConsentScope.CUSTOM_TEMPORARY)
        USER_TOKENS[user_id] = token.token


class SkillAnalyzerAgent:
    required_scope = ConsentScope.CUSTOM_TEMPORARY

    def validate(self, user_id: str):
        token = USER_TOKENS.get(user_id)
        if not token:
            raise PermissionError("Token not found for user.")
        valid, reason, parsed = validate_token(token, expected_scope=self.required_scope)
        if not valid:
            raise PermissionError(f"Invalid token: {reason}")
        if parsed.user_id != user_id:
            raise PermissionError("Token user mismatch")


class JobRecommenderAgent:
    required_scope = ConsentScope.CUSTOM_TEMPORARY

    def validate(self, user_id: str):
        token = USER_TOKENS.get(user_id)
        if not token:
            raise PermissionError("Token not found for user.")
        valid, reason, parsed = validate_token(token, expected_scope=self.required_scope)
        if not valid:
            raise PermissionError(f"Invalid token: {reason}")
        if parsed.user_id != user_id:
            raise PermissionError("Token user mismatch")


@app.post("/upload_linkedin/")
async def upload_linkedin(user_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are supported.")
    file_bytes = await file.read()

    # Only issue token if not already present
    ensure_token(user_id)

    # Manually validate for LinkedIn upload scope
    token_str = USER_TOKENS[user_id]
    parsed_data = parse_linkedin_zip(file_bytes)

    skills, experience = parsed_data

    USER_SKILL_DB.setdefault(user_id, {"skills": set(), "experience": []})
    USER_SKILL_DB[user_id]["skills"].update(skills)
    USER_SKILL_DB[user_id]["experience"].extend(experience)

    return {"message": "LinkedIn archive parsed successfully.", "parsed_data": parsed_data}


@app.post("/resume/")
async def upload_resume(user_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf resumes are supported.")
    file_bytes = await file.read()
    parsed_data = parse_resume(file_bytes)

    ensure_token(user_id)

    USER_SKILL_DB.setdefault(user_id, {"skills": set(), "experience": []})
    USER_SKILL_DB[user_id]["skills"].update(parsed_data.get("skills", []))
    USER_SKILL_DB[user_id]["experience"].extend(parsed_data.get("experience", []))

    return {"message": "Resume parsed successfully.", "parsed_data": parsed_data}


@app.post("/parse_github/")
async def parse_github(user_id: str = Form(...), github_username: str = Form(...)):
    parsed_data = await parse_github_repo(github_username)

    ensure_token(user_id)

    USER_SKILL_DB.setdefault(user_id, {"skills": set(), "experience": []})
    USER_SKILL_DB[user_id]["skills"].update(parsed_data.get("skills", []))
    USER_SKILL_DB[user_id]["experience"].extend(parsed_data.get("experience", []))

    return {"message": "GitHub profile parsed successfully.", "parsed_data": parsed_data}


@app.post("/analyze_skill_gap/")
async def analyze_skill_gap(user_id: str = Form(...), job_title: str = Form(...)):
    agent = SkillAnalyzerAgent()
    agent.validate(user_id)

    if user_id not in USER_SKILL_DB:
        raise HTTPException(status_code=404, detail="No user skill data found. Please upload resume, LinkedIn, or GitHub first.")

    user_skills = USER_SKILL_DB[user_id]["skills"]
    descriptions = await fetch_job_descriptions(job_title)
    job_skills = extract_job_skills_from_postings(descriptions)
    skill_gaps = compute_skill_gaps(user_skills, job_skills)

    USER_SKILL_DB[user_id]["skill_gaps"] = skill_gaps
    USER_SKILL_DB[user_id]["job_title"] = job_title

    return {
        "user_id": user_id,
        "job_title": job_title,
        "user_skills": list(user_skills),
        "job_required_skills": list(job_skills),
        "skill_gaps": list(skill_gaps)
    }


@app.post("/recommend_jobs/")
async def recommend_jobs(user_id: str = Form(...)):
    agent = JobRecommenderAgent()
    agent.validate(user_id)

    if user_id not in USER_SKILL_DB:
        raise HTTPException(status_code=404, detail="No skill data found for this user.")

    skills = list(USER_SKILL_DB[user_id]["skills"])
    job_results = []

    for skill in skills:
        try:
            jobs = await fetch_combined_jobs(skill)
            job_results.extend(jobs)
        except Exception as e:
            print(f"Error fetching jobs for skill {skill}: {str(e)}")

    return {"recommended_jobs": job_results}
