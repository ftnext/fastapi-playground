# uvx --with fastapi uvicorn app:app --log-level info --reload
import json
import logging

from fastapi import APIRouter, Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

logger = logging.getLogger("uvicorn.myapp")  # hack to easy logging


class LoggingRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            request_json = await request.json()
            response: Response = await original_route_handler(request)
            logger.info(
                "%s", {"request": request_json, "response": json.loads(response.body)}
            )
            return response

        return custom_route_handler


app = FastAPI()
router = APIRouter(route_class=LoggingRoute)


@app.get("/")
async def hello():
    return {"message": "Hello World"}


@router.post("/")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}


app.include_router(router)
