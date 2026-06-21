from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient


async def endpoint(request):
    return PlainTextResponse(request.url.path)


app = Starlette(routes=[Route("/foo", endpoint)])

client = TestClient(app)
response = client.get("/foo", headers={"host": "example.com/abc?bar="})

assert response.text == "/foo", f"{response.text=}"
