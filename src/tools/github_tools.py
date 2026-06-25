import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.tools import tool
from github import Github
from config import GITHUB_TOKEN


def get_github_client():
    return Github(GITHUB_TOKEN)


@tool
def get_recent_commits(repo_name: str, hours_before: int = 3) -> str:
    """Get recent commits from a GitHub repo to find what changed before the incident."""
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        commits = repo.get_commits()
        result = f"Recent commits for {repo_name}:\n"
        count = 0
        for commit in commits:
            if count >= 5:
                break
            result += f"-[{commit.sha[:7]}] {commit.commit.message[:80]} by {commit.commit.author.name} at {commit.commit.author.date}\n"
            count+=1
        return result
    except Exception as e:
        return f"Could not fetch commits:{str(e)}"

@tool
def get_commit_diff(repo_name:str,commit_hash:str)->str:
    """Get the file changes in a specific commit to identify what code changed."""
    try:
        g=get_github_client()
        repo = g.get_repo(repo_name)
        commit = repo.get_commit(commit_hash)
        result = f"Changes in commit {commit_hash[:7]}:\n"
        for file in commit.files:
            result += f"- {file.filename} ({file.status}) + {file.additions} - {file.deletions} lines \n"
        return result
    except Exception as e:
        return f"Could not fetch commit diff:{str(e)}"

@tool
def get_repo_info(repo_name:str) -> str:
    """Get basic info about a GitHub repository."""
    try:
        g = get_gethub_client()
        repo = g.get_repo(repo_name)
        return f"Repo:{repo.full_name} | Language:{repo.language}|Last Updated:{repo.updated_at}| Open issues:{repo.open_issues_count}"
    
    except Exception as e:
        return f"Could not fetch repo info: {str(e)}"



