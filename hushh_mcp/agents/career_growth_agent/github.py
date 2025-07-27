# hushh_mcp/agents/career_growth_agent/github_parser.py

import httpx
from fastapi import HTTPException

async def parse_github_repo(username: str):
    github_api = f"https://api.github.com/users/{username}/repos"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(github_api)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch GitHub repos: {response.json().get('message', 'Unknown error')}"
            )

        repos_data = response.json()

        repo_summaries = []
        for repo in repos_data:
            repo_summaries.append({
                "name": repo["name"],
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "url": repo.get("html_url"),
            })

        return {
            "total_repos": len(repos_data),
            "repos": repo_summaries
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub parsing failed: {str(e)}")
