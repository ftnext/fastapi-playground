# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi==0.141.1",
#     "uvicorn==0.52.4",
# ]
# ///
"""Finite async SSE example using FastAPI's built-in SSE support.

https://fastapi.tiangolo.com/tutorial/server-sent-events/

Run:
    uv run fastapi_builtin_sse_app.py

Connect from another terminal:
    curl -N http://127.0.0.1:8000/events

Run `kill -TERM <pid>` in the 3rd terminal before all 10 events have been sent.
With Uvicorn's default unlimited graceful-shutdown wait, the finite stream
continues until all 10 events have been sent.
"""

import asyncio
from collections.abc import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent

app = FastAPI(title="Finite SSE with FastAPI")


@app.get("/events", response_class=EventSourceResponse)
async def events() -> AsyncIterator[ServerSentEvent]:
    for number in range(1, 11):
        yield ServerSentEvent(data=f"Event {number}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        # timeout_graceful_shutdown=None,  # Default is None
    )
