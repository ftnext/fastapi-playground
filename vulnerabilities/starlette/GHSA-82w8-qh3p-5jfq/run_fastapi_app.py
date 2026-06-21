# https://github.com/Kludex/starlette/security/advisories/GHSA-82w8-qh3p-5jfq
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi>=0.137.2",
#     "httpx2>=2.4.0",
#     "python-multipart>=0.0.32",
#     "starlette<1.3.1",
# ]
# ///
# Fixed at starlette>=1.3.1
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/form")
async def form_endpoint(request: Request):
    form = await request.form()
    return {
        "content_type": request.headers.get("content-type"),
        "field_count": len(form),
    }


client = TestClient(app)

body = "&".join(f"f{i}=v{i}" for i in range(1000 + 1))
response = client.post(
    "/form", content=body, headers={"content-type": "application/x-www-form-urlencoded"}
)
assert response.status_code == 400, f"{response.status_code=}, {response.text=}"

body = f"field={'x' * (1024 * 1024 + 1)}"
response = client.post(
    "/form", content=body, headers={"content-type": "application/x-www-form-urlencoded"}
)
assert response.status_code == 400, f"{response.status_code=}, {response.text=}"
