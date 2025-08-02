# hushh_mcp/agents/career_growth_agent/job_recommender_agent.py

from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from ..career_growth_agent.job_recommender import fetch_combined_jobs

class JobRecommenderAgent:
    required_scope = ConsentScope.CUSTOM_TEMPORARY  # Set proper scope as per your token

    def handle(self, user_id: str, token: str, user_skills: set):
        valid, reason, parsed = validate_token(token, expected_scope=self.required_scope)
        if not valid or parsed.user_id != user_id:
            raise PermissionError(f"❌ Invalid token or user mismatch: {reason}")

        job_results = []
        for skill in list(user_skills)[:10]:  # limit for performance
            try:
                jobs = fetch_combined_jobs(skill)  # This is assumed to be sync; wrap in asyncio if async
                job_results.extend(jobs)
            except Exception as e:
                print(f"⚠️ Failed to fetch jobs for '{skill}': {e}")

        return {"recommended_jobs": job_results}
# This manifest defines the Job Recommender Agent, which is responsible for recommending jobs
# based on the user's skills. It requires temporary consent to access the user's skill data.
# The agent fetches job postings related to the user's skills and returns a list of recommended jobs.       