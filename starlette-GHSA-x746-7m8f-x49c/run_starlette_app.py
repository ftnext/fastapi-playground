from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient


class MyEndpoint(HTTPEndpoint):
    async def get(self, request: Request) -> PlainTextResponse:
        return PlainTextResponse("GET handler")

    async def _do_delete(self, request: Request) -> PlainTextResponse:
        print("_do_delete() was called")
        return PlainTextResponse("_do_delete handler")


app = Starlette(routes=[Route("/", MyEndpoint)])

client = TestClient(app)
response = client.request("_DO_DELETE", "/")
print(f"{response.status_code=}, {response.text=}")
