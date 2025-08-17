import os

import httpx

graphql_query = """
query Q($name: String!, $owner: String!, $answered: Boolean) {
  repository(name: $name, owner: $owner) {
    discussions(answered: $answered) {
      totalCount
    }
  }
}
"""


async def get_github_discussion_count(owner: str, name: str, answered: bool):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.github.com/graphql",
            json={
                "query": graphql_query,
                "variables": {"name": name, "owner": owner, "answered": answered},
            },
            headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
            timeout=httpx.Timeout(5, read=10),
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    import asyncio

    data = asyncio.run(get_github_discussion_count("fastapi", "fastapi", True))
    print(data)
