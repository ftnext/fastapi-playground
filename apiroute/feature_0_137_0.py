# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi>=0.137.0",
#     "httpx2>=2.4.0",
# ]
# ///
# ref: https://github.com/fastapi/fastapi/releases/tag/0.137.0
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

router = APIRouter()
app = FastAPI()
app.include_router(router, prefix="/api")


@router.get("/late")
def late_added_route():
    return {"ok": True}


client = TestClient(app)
response = client.get("/api/late")
# "fastapi<0.137.0" causes 404
assert response.status_code == 200, f"{response.status_code=}"
