# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx2>=2.6.0",
#     "starlette==1.7.0",
# ]
# ///
# https://starlette.dev/endpoints/#httpendpoint
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient


class Homepage(HTTPEndpoint):
    async def query(self, request):
        return PlainTextResponse("Hello, query!")


routes = [Route("/", Homepage)]
app = Starlette(routes=routes)

client = TestClient(app)
response = client.query("/")
assert response.status_code == 200
assert response.text == "Hello, query!"
