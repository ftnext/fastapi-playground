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

HTTPXClientInstrumentor().instrument()

url = "http://localhost:8000/"
with httpx.Client() as client:
    response = client.get(url)
    response.raise_for_status()
    assert response.json() == {"message": "Hello World"}
