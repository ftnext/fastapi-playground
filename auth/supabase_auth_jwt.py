# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fastapi>=0.141.1",
#     "supabase>=2.31.0",
#     "uvicorn>=0.52.4",
# ]
# ///
import asyncio
import os
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ValidationError
from supabase import create_async_client as create_supabase_async_client
from supabase_auth.errors import AuthError

app = FastAPI()

client = asyncio.run(
    create_supabase_async_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_PUBLISHABLE_KEY"]
    )
)

bearer = HTTPBearer()


class CurrentUser(BaseModel):
    id: UUID
    email: str | None = None


async def get_claims(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
) -> dict:
    try:
        claims = await client.auth.get_claims(credentials.credentials)
    except (AuthError, ValidationError, KeyError) as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return claims["claims"]


@app.get("/me")
async def me(claims: Annotated[dict, Depends(get_claims)]) -> CurrentUser:
    return CurrentUser(id=claims["sub"], email=claims.get("email"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
