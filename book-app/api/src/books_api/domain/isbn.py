from pydantic import BaseModel


class ISBN(BaseModel, frozen=True):
    value: str
