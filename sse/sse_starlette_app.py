# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi==0.141.1",
#     "sse-starlette==3.4.8",
#     "uvicorn==0.52.4",
# ]
# ///
"""Finite async SSE example using sse-starlette.

Run:
    uv run sse_starlette_app.py

Connect from another terminal:
    curl -N http://127.0.0.1:8000/events

Run `kill -TERM <pid>` in the 3rd terminal before all 10 events have been sent.
sse-starlette observes Uvicorn's shutdown and cancels the stream by default.
"""

import asyncio
from collections.abc import AsyncIterator

import uvicorn
from fastapi import FastAPI
from sse_starlette import EventSourceResponse

app = FastAPI(title="Finite SSE with sse-starlette")


async def generate_events() -> AsyncIterator[dict[str, str]]:
    for number in range(1, 11):
        yield {"data": f"Event {number}"}
        await asyncio.sleep(1)


@app.get("/events")
async def events() -> EventSourceResponse:
    return EventSourceResponse(generate_events())


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        # timeout_graceful_shutdown=None,  # Default is None
    )
