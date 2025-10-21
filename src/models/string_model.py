from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError


class StringPayload(BaseModel):
    value: str

    @classmethod
    def validate_existence(cls, value: str):
        if len(value.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid request body or missing "value" field'
            )
        return value
