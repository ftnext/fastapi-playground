# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "fastapi>=0.138.1",
#     "python-json-logger>=4.1.0",
#     "uvicorn[standard]>=0.49.0",
# ]
# ///
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/error")
def read_error():
    raise Exception("Something went wrong")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, log_config="log_config.yaml")
