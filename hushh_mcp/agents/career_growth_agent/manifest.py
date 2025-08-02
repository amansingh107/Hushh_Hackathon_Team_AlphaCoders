# hushh_mcp/agents/career_growth_agent/manifest.py
# hushh_mcp/agents/career_growth_agent/manifest.py

manifest = [
    {
        "id": "agent_skill_gap",
        "name": "Skill Gap Analyzer",
        "description": "Analyzes missing skills from user's resume, LinkedIn or GitHub for a given job title.",
        "scopes": ["custom.linkedin.upload", "custom.resume.upload", "custom.temporary"],
        "version": "0.1.0"
    },
    {
        "id": "agent_job_recommender",
        "name": "Job Recommender",
        "description": "Recommends jobs using extracted user skills by fetching real-time postings.",
        "scopes": ["custom.temporary"],
        "version": "0.1.0"
    }
]
    

# This manifest defines the Career Growth Agent, which is responsible for analyzing user data
# and providing recommendations for career advancement. It requires access to the user's profile,