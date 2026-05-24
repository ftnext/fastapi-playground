from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/foo")
async def foo(request: Request):
    return {"path": request.url.path}


client = TestClient(app)
response = client.get("/foo", headers={"host": "example.com/abc?bar="})

assert response.json()["path"] == "/foo", f'{response.json()["path"]=}'
