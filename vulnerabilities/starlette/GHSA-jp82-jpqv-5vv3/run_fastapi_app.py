# https://github.com/Kludex/starlette/security/advisories/GHSA-jp82-jpqv-5vv3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi>=0.137.2",
#     "starlette<1.3.0",
#     "uvicorn>=0.49.0",
# ]
# ///
# Fixed at starlette>=1.3.0
from fastapi import Request
from fastapi.responses import PlainTextResponse


async def app(scope, receive, send):
    request = Request(scope, receive)
    body = "\n".join(
        [
            f"{scope["path"]=}",
            f"{request.url=}",
            f"{request.url.netloc=}",
            f"{request.url.hostname=}",
            f"{request.url.path=}",
        ]
    )
    response = PlainTextResponse(body)
    await response(scope, receive, send)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
