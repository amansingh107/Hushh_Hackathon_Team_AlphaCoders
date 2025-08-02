# hushh_mcp/agents/career_growth_agent/skill_gap_agent.py

from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from .skills_gap import compute_skill_gaps, extract_job_skills_from_postings
from .job_fetcher import fetch_job_descriptions
import asyncio
class SkillGapAgent:
    required_scope = ConsentScope.CUSTOM_TEMPORARY  # or another appropriate scope

    def handle(self, user_id: str, token: str, job_title: str, user_skills: set):
        valid, reason, parsed = validate_token(token, expected_scope=self.required_scope)
        if not valid or parsed.user_id != user_id:
            raise PermissionError(f"❌ Invalid token or user mismatch: {reason}")
        
        job_descs = asyncio.run(fetch_job_descriptions(job_title))
        job_skills = extract_job_skills_from_postings(job_descs)
        skill_gaps = compute_skill_gaps(user_skills, job_skills)

        return {
            "job_title": job_title,
            "user_skills": list(user_skills),
            "job_required_skills": list(job_skills),
            "skill_gaps": list(skill_gaps)
        }
