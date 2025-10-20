from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timezone
import httpx
from models.string_model import StringPayload
from controllers.create_string import create_and_save_string, get_payload_by_id, delete_payload_by_id
from pydantic import BaseModel, ValidationError


app = FastAPI()



@app.get('/')
async def root():
    return {"root": "welcome to root!"}

@app.post('/strings', status_code=201)
async def create_string(payload: dict):
    try:
        data = StringPayload(**payload)
        StringPayload.validate_existence(data.value)
        response_payload = await create_and_save_string(data)
        return response_payload
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data type for "value" (must be string)'
        )

@app.get('/strings/{string_value}', status_code=200)
async def get_string(string_value:str):
    fetched_payload = await get_payload_by_id(string_value)
    if fetched_payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    return fetched_payload

@app.delete('/strings/{string_value}', status_code=204)
async def delete_string(string_value:str):
    fetched_payload = await delete_payload_by_id(string_value)
    if fetched_payload is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
