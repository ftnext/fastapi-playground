# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "opentelemetry-sdk",
#     "opentelemetry-instrumentation-httpx",
# ]
# ///
import httpx
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

set_tracer_provider(TracerProvider())
get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


async def async_request_hook(span, request):
    try:
        # ref: https://github.com/encode/httpx/blob/0.28.1/tests/test_content.py#L32-L33
        body_content = b"".join([s async for s in request.stream])
        if body_content:
            body = body_content.decode("utf-8")
            span.set_attribute("http.request.body", body)
    except Exception as e:
        span.set_attribute("http.request.body.error", str(e))


HTTPXClientInstrumentor().instrument(async_request_hook=async_request_hook)


async def post(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"name": "awesome", "price": 100})
        response.raise_for_status()
        return response


if __name__ == "__main__":
    import asyncio

    url = "http://localhost:8000/items/"
    response = asyncio.run(post(url))
    assert response.json() == {"name": "awesome", "price": 100}
