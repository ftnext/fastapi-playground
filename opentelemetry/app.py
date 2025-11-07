# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi",
#     "opentelemetry-sdk",
#     "opentelemetry-instrumentation-fastapi",
#     "uvicorn",
# ]
# ///
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from pydantic import BaseModel

set_tracer_provider(TracerProvider())
get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}


@app.post("/items/")
async def create_item(item: Item):
    return item


FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
