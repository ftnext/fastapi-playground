# https://github.com/Kludex/starlette/security/advisories/GHSA-82w8-qh3p-5jfq
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx2>=2.4.0",
#     "python-multipart>=0.0.32",
#     "starlette<1.3.1",
# ]
# ///
# Fixed at starlette>=1.3.1
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient


async def form_endpoint(request):
    form = await request.form()
    return JSONResponse(
        {"content_type": request.headers.get("content-type"), "field_count": len(form)}
    )


app = Starlette(routes=[Route("/form", form_endpoint, methods=["POST"])])

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
