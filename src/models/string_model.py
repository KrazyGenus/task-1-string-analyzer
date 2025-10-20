from pydantic import BaseModel


class StringPayload(BaseModel):
    value: str