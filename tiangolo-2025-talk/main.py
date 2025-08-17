from fastapi import FastAPI

from call_github import get_github_discussion_count

app = FastAPI()


@app.get("/counts/{owner}/{repo}")
async def get_counts(owner: str, repo: str):
    unanswered_data = await get_github_discussion_count(owner, repo, answered=False)
    answered_data = await get_github_discussion_count(owner, repo, answered=True)
    unanswered = unanswered_data["data"]["repository"]["discussions"]["totalCount"]
    answered = answered_data["data"]["repository"]["discussions"]["totalCount"]
    total = unanswered + answered
    return {"unanswered": unanswered, "answered": answered, "total": total}
